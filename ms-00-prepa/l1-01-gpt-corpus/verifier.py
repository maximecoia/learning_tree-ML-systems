"""Acceptance test for the blank-file GPT. Seven checks, one command, no plots.

    python3 verifier.py              # check 7 on the scaffolding corpus
    python3 verifier.py DATA_DIR     # check 7 on a folder prepare.py wrote

It imports gpt.py and invents nothing. It does not read your architecture: it
only feeds tensors in and reads tensors out, so any number of layers, heads or
norms passes as long as the model is a causal language model.

WHAT EACH CHECK COSTS TO BREAK -- measured on a reference implementation, so
you can reproduce the failure before you trust the success. V = 65, ln(V) =
4.1744, three layers, four heads, n_embd 64, block 32.

    1  shapes        a model returning (B, V) instead of (B, T, V) -- the
                     last-position-only mistake -- fails here and nowhere else
    2  loss at init  correct 4.33, ln(V)+0.16
                     scaling the OUTPUT head, the linear that maps the last
                     hidden state onto the vocabulary, is what moves this
                     number. Scaling the attention heads does not: it sharpens
                     where attention looks and leaves the logits' scale alone.
                     output head x3  ->  5.59, ln(V)+1.42   CAUGHT
                     output head x20 -> 27.46, ln(V)+23.29   CAUGHT
                     output head x2  ->  4.82, ln(V)+0.65   NOT caught, see below
    3  causality     correct 0.0 exactly; drop the mask -> 1.42e-01
    4  positions     fit "target = t mod V" on a constant input: with position
                     embeddings 0.0010, without them 3.4658, and it cannot go
                     lower because every position sees the same thing
    5  gradients     overfit 32 fixed sequences, 400 steps: correct 0.0108; a
                     detached graph or a frozen parameter stays near ln(V)
    6  generate      feed it block+5 tokens and ask for 10 more: correct
                     (1, block+15); a model that crops the context to the last
                     block, or that returns only what it generated, fails on
                     the shape. The sample itself is not judged -- a crash is a
                     real failure, a dull continuation is not this file's
                     business
    7  the run       loads the gpt.pt train() left beside gpt.py and measures
                     it on every full window of dev, against a counted
                     bigram, add-one smoothed, on the same split. It must
                     land 0.10 below. On the prepared Tiny Shakespeare:
                     bigram 2.4743, so the bar is 2.3743
                     correct, 2000 steps          ->  2.0856
                     weights never trained        ->  4.3370   CAUGHT, and
                                                  checks 1 to 6 all pass
                     attention returning zeros    ->  2.4885   CAUGHT, and
                                                  check 5 catches it too
                     gpt.pt missing, or from a corpus with another
                     vocabulary                   ->  CAUGHT, said in words

WHAT IT DOES NOT CATCH, said plainly

    - an initialisation off by a factor of two. The band is set at ln(V)+0.75
      so that a legitimate deep stack is not flagged, and a factor of two
      lands at +0.65. Read the printed number, do not just read OK.
    - generate() sampling wrongly. It checks the shape and that a context
      longer than BLOCK_SIZE does not crash, not the distribution.
    - anything about the corpus: provenance, licence, leakage. That is L1's
      real work and no unit test replaces it. Leakage matters to check 7 too:
      a dev split that repeats train makes the bigram easy to beat.
    - which corpus the run used, beyond its vocabulary. Without DATA_DIR,
      check 7 reads the scaffolding corpus: the reference weights, trained on
      the prepared split, pass there at 2.0976 against a bar of 2.3819, on a
      dev that overlaps their train. Pass the folder of the chosen corpus.
    - that gpt.pt came from this gpt.py's own train(). It loads what it finds.

A check that cannot fail is worse than no check at all.
"""
import json
import math
import os
import sys

import torch

try:
    from gpt import GPT, BLOCK_SIZE
except ModuleNotFoundError:
    # This file is published without the blank file it grades. A traceback is a
    # poor way to say so, and the exam is worth reading on its own.
    raise SystemExit(
        "gpt.py is not beside this file.\n\n"
        "This is the exam, not the answer. What each check costs to break is\n"
        "written at the top of this file, measured against a reference\n"
        "implementation rather than asserted, so the whole thing reads without\n"
        "running. The blank file it grades stays out until L1 is handed in."
    ) from None

V = 65                 # same vocabulary size as the scaffolding corpus
LNV = math.log(V)
SEED = 1337


def verdict(name, ok, detail):
    print('%-30s %-5s  %s' % (name, 'OK' if ok else 'ECART', detail))
    return ok


def fresh(seed=SEED):
    torch.manual_seed(seed)
    return GPT(V)


all_ok = True

# The blank file raises NotImplementedError everywhere. Say so in one line
# rather than in a traceback: before the exercise starts, that is not a bug.
try:
    fresh()
except NotImplementedError:
    print('gpt.py is still the blank file. Nothing to check yet.')
    raise SystemExit(1)

# 1. shapes. The contract, and nothing else.
model = fresh()
idx = torch.randint(0, V, (4, BLOCK_SIZE))
logits, loss = model(idx)
shape_ok = tuple(logits.shape) == (4, BLOCK_SIZE, V) and loss is None
all_ok &= verdict('1. (B,T) -> (B,T,V)', shape_ok,
                  'expected (4, %d, %d) and loss None   got %s and %s'
                  % (BLOCK_SIZE, V, tuple(logits.shape), type(loss).__name__))
if not shape_ok:
    # Every check below feeds targets of shape (B, T). Going on from here only
    # produces a traceback about a view, which hides the real answer: the
    # shape contract is not met.
    print()
    print('SOMETHING IS OFF  -- the other checks need check 1 to pass first')
    raise SystemExit(1)

# 2. the loss starts where an honest initialisation puts it.
torch.manual_seed(0)
idx = torch.randint(0, V, (16, BLOCK_SIZE))
tgt = torch.randint(0, V, (16, BLOCK_SIZE))
l0 = fresh()(idx, tgt)[1].item()
all_ok &= verdict('2. loss at init ~ ln(V)',
                  LNV - 0.05 <= l0 <= LNV + 0.75,
                  'expected [%.3f, %.3f]   got %.4f' % (LNV - 0.05, LNV + 0.75, l0))

# 3. causality. The one the loss curve never reveals.
model = fresh()
torch.manual_seed(3)
cut = BLOCK_SIZE // 2
idx = torch.randint(0, V, (4, BLOCK_SIZE))
after = idx.clone()
after[:, cut + 1:] = torch.randint(0, V, (4, BLOCK_SIZE - cut - 1))
with torch.no_grad():
    drift = (model(idx)[0][:, :cut + 1]
             - model(after)[0][:, :cut + 1]).abs().max().item()
all_ok &= verdict('3. the future is unreadable', drift < 1e-6,
                  'expected < 1e-06 when tokens after t change   got %.3e' % drift)


def fit(x, y, steps=400, lr=3e-3):
    """Train one fresh model on one fixed batch. Returns the final loss."""
    model = fresh(7)
    opt = torch.optim.AdamW(model.parameters(), lr=lr)
    for _ in range(steps):
        loss = model(x, y)[1]
        opt.zero_grad()
        loss.backward()
        opt.step()
    return loss.item()


# 4. positions. Constant input, target = t mod V: only position tells them
#    apart, so a model with no position signal is stuck at the entropy of the
#    targets and cannot descend, however long you train it.
flat = torch.zeros(8, BLOCK_SIZE, dtype=torch.long)
ramp = (torch.arange(BLOCK_SIZE) % V).unsqueeze(0).expand(8, BLOCK_SIZE).contiguous()
l_pos = fit(flat, ramp)
all_ok &= verdict('4. positions reach the model', l_pos < 0.5,
                  'expected < 0.5   got %.4f   (blind model sits near 3.47)' % l_pos)

# 5. gradients actually flow through every parameter that matters.
torch.manual_seed(11)
x = torch.randint(0, V, (32, BLOCK_SIZE))
y = torch.randint(0, V, (32, BLOCK_SIZE))
l_fit = fit(x, y)
all_ok &= verdict('5. overfits 32 sequences', l_fit < 0.15,
                  'expected < 0.15 after 400 steps   got %.4f' % l_fit)

# generate() is exercised, not judged: a crash here is a real failure, a bad
# sample is not something this file is entitled to have an opinion about.
model = fresh()
long_context = torch.randint(0, V, (1, BLOCK_SIZE + 5))
out = model.generate(long_context, 10)
all_ok &= verdict('6. generate survives T > block',
                  tuple(out.shape) == (1, BLOCK_SIZE + 15),
                  'expected (1, %d)   got %s' % (BLOCK_SIZE + 15, tuple(out.shape)))



# 7. the run. Checks 1 to 6 grade a fresh model, or one fitted for seconds on
#    a single batch. This one grades the weights train() left in gpt.pt, on
#    the corpus they were trained on, against what a model with no context
#    reaches: the counted bigram. A GPT that does not go clearly below it has
#    bought nothing with its context, whatever its curve looks like.
MARGIN = 0.10          # nats the run must gain on the bigram


def load_corpus(data_dir):
    """(train, dev, vocab_size, name) as long tensors, the way train() saw them.

    No folder: the scaffolding corpus, through corpus.py. A folder: the one
    prepare.py writes, train.txt and dev.txt encoded against vocab.json, a
    JSON list of characters. A character outside that list stops the check
    rather than being dropped, since a dropped character is a changed corpus.
    """
    if data_dir is None:
        from corpus import dataset
        train_ids, dev_ids, vocab, _, _ = dataset()
        return train_ids, dev_ids, len(vocab), 'the scaffolding corpus'
    with open(os.path.join(data_dir, 'vocab.json'), encoding='utf-8') as f:
        vocab = json.load(f)
    to_i = {c: i for i, c in enumerate(vocab)}
    splits = []
    for name in ('train', 'dev'):
        with open(os.path.join(data_dir, name + '.txt'), encoding='utf-8', newline='') as f:
            text = f.read()
        outside = sorted(set(text) - set(to_i))
        if outside:
            raise SystemExit('%s.txt holds characters outside vocab.json: %r'
                             % (name, outside[:5]))
        splits.append(torch.tensor([to_i[c] for c in text], dtype=torch.long))
    return splits[0], splits[1], len(vocab), data_dir


def bigram_dev_loss(train_ids, dev_ids, vocab_size):
    """Dev loss of a counted bigram, add-one smoothed: the model to beat."""
    counts = torch.ones(vocab_size, vocab_size)
    counts.index_put_((train_ids[:-1], train_ids[1:]),
                      torch.ones(len(train_ids) - 1), accumulate=True)
    logp = (counts / counts.sum(1, keepdim=True)).log()
    return -logp[dev_ids[:-1], dev_ids[1:]].mean().item()


@torch.no_grad()
def dev_loss(model, dev_ids):
    """Mean next-token loss over every full window of dev, none sampled."""
    n = (len(dev_ids) - 1) // BLOCK_SIZE
    x = dev_ids[:n * BLOCK_SIZE].view(n, BLOCK_SIZE)
    y = dev_ids[1:n * BLOCK_SIZE + 1].view(n, BLOCK_SIZE)
    model.eval()
    total = 0.0
    for i in range(0, n, 256):
        total += model(x[i:i + 256], y[i:i + 256])[1].item() * len(x[i:i + 256])
    return total / n


weights = os.path.join(os.path.dirname(os.path.abspath(
    sys.modules[GPT.__module__].__file__)), 'gpt.pt')
train_ids, dev_ids, v_run, name = load_corpus(sys.argv[1] if len(sys.argv) > 1 else None)
if not os.path.exists(weights):
    run_ok, detail = False, 'no gpt.pt beside gpt.py: train() has not left its weights'
else:
    try:
        model = GPT(v_run)
        model.load_state_dict(torch.load(weights, map_location='cpu', weights_only=True))
    except RuntimeError:
        run_ok, detail = False, ('gpt.pt does not load into GPT(%d): trained on another '
                                 'corpus, or by another gpt.py' % v_run)
    else:
        base = bigram_dev_loss(train_ids, dev_ids, v_run)
        got = dev_loss(model, dev_ids)
        run_ok = got < base - MARGIN
        detail = ('expected < %.4f, bigram %.4f minus %.2f   got %.4f   on %s'
                  % (base - MARGIN, base, MARGIN, got, name))
all_ok &= verdict('7. the run beats the bigram', run_ok, detail)

print()
print('ALL OK' if all_ok else 'SOMETHING IS OFF')
if not all_ok:
    raise SystemExit(1)
