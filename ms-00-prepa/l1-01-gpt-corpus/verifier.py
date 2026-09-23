"""Acceptance test for the blank-file GPT. Six checks, one command, no plots.

    python3 verifier.py

It imports gpt.py and invents nothing. It does not read your architecture: it
only feeds tensors in and reads tensors out, so any number of layers, heads or
norms passes as long as the model is a causal language model.

WHAT EACH CHECK COSTS TO BREAK -- measured on a reference implementation, so
you can reproduce the failure before you trust the success. V = 65, ln(V) =
4.1744, three layers, four heads, n_embd 64, block 32.

    1  shapes        a model returning (B, V) instead of (B, T, V) -- the
                     last-position-only mistake -- fails here and nowhere else
    2  loss at init  correct 4.33, ln(V)+0.16
                     head weights x3  ->  5.59, ln(V)+1.42   CAUGHT
                     head weights x20 -> 27.46, ln(V)+23.29   CAUGHT
                     head weights x2  ->  4.82, ln(V)+0.65   NOT caught, see below
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

WHAT IT DOES NOT CATCH, said plainly

    - an initialisation off by a factor of two. The band is set at ln(V)+0.75
      so that a legitimate deep stack is not flagged, and a factor of two
      lands at +0.65. Read the printed number, do not just read OK.
    - generate() sampling wrongly. It checks the shape and that a context
      longer than BLOCK_SIZE does not crash, not the distribution.
    - anything about the corpus: provenance, licence, leakage. That is L1's
      real work and no unit test replaces it.

A check that cannot fail is worse than no check at all.
"""
import math

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

print()
print('ALL OK' if all_ok else 'SOMETHING IS OFF')
if not all_ok:
    raise SystemExit(1)
