"""makemore part 2 -- the MLP of Bengio et al. 2003, at character level.

Every function here is importable; sections 06 to 26 build them one at a time.

    from mlp import load, alphabet, dataset, split, train, evaluate, sample
"""
import random
import torch
import torch.nn.functional as F

VOCAB = 27
BLOCK = 3
EMBED = 10
HIDDEN = 200
SEED = 2147483647


def load(path='names.txt'):
    """The 32,033 names, one per line."""
    return open(path).read().splitlines()      # section 00B, line for line


def alphabet():
    """stoi and itos for the 26 letters plus '.', which is index 0."""
    letters = sorted(set('abcdefghijklmnopqrstuvwxyz'))
    # 'a' -> 1 ... 'z' -> 26
    stoi = {s: i + 1 for i, s in enumerate(letters)}
    stoi['.'] = 0                              # 0 is both start and end
    # the table, and its reverse
    return stoi, {i: s for s, i in stoi.items()}


def dataset(words, block=BLOCK):
    """One example per character, plus one per name for the ending '.'."""
    # _ : the reverse table, unused here
    stoi, _ = alphabet()
    X, Y = [], []
    for w in words:
        context = [0] * block                  # start padded with '...'
        # the final '.' is an example too
        for ch in w + '.':
            ix = stoi[ch]
            X.append(context)                  # what the model can see
            Y.append(ix)                       # what actually came next
            # slide: drop oldest, add newest
            context = context[1:] + [ix]
    return torch.tensor(X), torch.tensor(Y)    # (N, block) and (N,)


def split(words, seed=42):
    """80 / 10 / 10, on the words, after one shuffle. Never on the examples."""
    # a copy: shuffle works in place
    words = list(words)
    # a THIRD generator: the stdlib one
    random.seed(seed)
    random.shuffle(words)
    # the two cut points
    n1, n2 = int(0.8 * len(words)), int(0.9 * len(words))
    return dataset(words[:n1]), dataset(words[n1:n2]), dataset(words[n2:])


def initialise(seed=SEED):
    # explicit: same weights every run
    g = torch.Generator().manual_seed(seed)
    params = [torch.randn((VOCAB, EMBED), generator=g),         # C  (27, 10)
              # W1 (30, 200)
              torch.randn((BLOCK * EMBED, HIDDEN), generator=g),
              torch.randn(HIDDEN, generator=g),                 # b1 (200,)
              torch.randn((HIDDEN, VOCAB), generator=g),        # W2 (200, 27)
              torch.randn(VOCAB, generator=g)]                  # b2 (27,)
    for p in params:
        # track them, so backward() can fill
        p.requires_grad = True
    return params


def forward(params, X):
    # unpack the list into five names
    C, W1, b1, W2, b2 = params
    # lookup, glue, one layer
    h = torch.tanh(C[X].view(X.shape[0], -1) @ W1 + b1)
    # logits: (rows, 27), no softmax
    return h @ W2 + b2


def train(Xtr, Ytr, steps=200000, rate=0.1, decay=0.01, batch=32,
          weight_decay=0.0, seed=SEED, verbose=False):
    """One 10x rate decay at the halfway point, as the lesson does."""
    params = initialise(seed)
    for i in range(steps):
        # GLOBAL generator: unseeded
        ix = torch.randint(0, Xtr.shape[0], (batch,))
        # labels too
        loss = F.cross_entropy(forward(params, Xtr[ix]), Ytr[ix])
        # on the weights and C, not the biases
        if weight_decay:
            loss = loss + weight_decay * sum((p ** 2).sum() for p in (params[0], params[1], params[3]))
        for p in params:
            # None, not zero: torch accumulates
            p.grad = None
        loss.backward()                        # fills p.grad for every p
        # one 10x decay, halfway through
        lr = rate if i < steps // 2 else decay
        for p in params:
            # .data: the numbers, not the graph
            p.data += -lr * p.grad
        # % : remainder, so every 50k steps
        if verbose and (i + 1) % 50000 == 0:
            print('%7d %.4f' % (i + 1, loss.item()))
    return params


@torch.no_grad()
def evaluate(params, X, Y):
    """No autograd graph: the number is identical, the memory is not."""
    return F.cross_entropy(forward(params, X), Y).item()


def sample(params, n=20, seed=SEED + 10, block=BLOCK):
    # only the reverse table is needed
    _, itos = alphabet()
    # explicit: this draw IS reproducible
    g = torch.Generator().manual_seed(seed)
    C, W1, b1, W2, b2 = params
    out = []
    # no graph: we only look at numbers
    with torch.no_grad():
        for _ in range(n):
            name, context = [], [0] * block
            while True:                        # the model decides the length
                h = torch.tanh(C[torch.tensor([context])].view(1, -1) @ W1 + b1)
                # exp and normalise, safely
                probs = F.softmax(h @ W2 + b2, dim=1)
                ix = torch.multinomial(probs, num_samples=1, generator=g).item()
                context = context[1:] + [ix]   # the same window as training
                name.append(ix)
                # '.' drawn: the name is finished
                if ix == 0:
                    break
            out.append(''.join(itos[i] for i in name))
    return out


if __name__ == '__main__':
    # the global generator too, so this run is reproducible
    torch.manual_seed(SEED)
    words = load()
    (Xtr, Ytr), (Xdev, Ydev), (Xte, Yte) = split(words)
    print('names   ', len(words))
    print('split   ', Xtr.shape[0], Xdev.shape[0], Xte.shape[0])

    params = train(Xtr, Ytr)
    print('params  ', sum(p.nelement() for p in params))
    print('train   %.4f' % evaluate(params, Xtr, Ytr))
    print('dev     %.4f' % evaluate(params, Xdev, Ydev))
    print('samples ', ' '.join(sample(params, 6)))
