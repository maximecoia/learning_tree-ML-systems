"""Bigram language model, road two: one linear layer, trained by gradient descent."""
import torch
import torch.nn.functional as F

# road two reuses road one's alphabet, unchanged
from bigram_count import VOCAB, SEED, load, alphabet

# measured, not guessed: see the loss surface in s22
LEARNING_RATE = 50.0
STEPS = 100
REGULARISATION = 0.01


# the same pairs road one counted, listed instead
def dataset(words, stoi):
    xs, ys = [], []
    for w in words:
        chs = ['.'] + list(w) + ['.']
        for ch1, ch2 in zip(chs, chs[1:]):
            xs.append(stoi[ch1])
            ys.append(stoi[ch2])
    return torch.tensor(xs), torch.tensor(ys)


def forward(xs, W):
    # integers become rows with a single 1
    xenc = F.one_hot(xs, num_classes=VOCAB).float()
    # (N,27) @ (27,27) -> (N,27): 27 raw scores per example
    logits = xenc @ W
    # exp makes them positive; read them as log-counts
    counts = logits.exp()
    # keepdims: divide each row by ITS own total
    return counts / counts.sum(1, keepdims=True)


def train(xs, ys, steps=STEPS, rate=LEARNING_RATE,
          regularisation=REGULARISATION, seed=SEED, verbose=False):
    g = torch.Generator().manual_seed(seed)
    W = torch.randn((VOCAB, VOCAB), generator=g, requires_grad=True)
    # built once, outside the loop: it never changes
    rows = torch.arange(xs.nelement())

    for step in range(steps):
        probs = forward(xs, W)
        # the probability of what actually came next
        nll = -probs[rows, ys].log().mean()
        # the penalty is NOT part of the comparable number
        loss = nll + regularisation * (W**2).mean()

        # backward accumulates; clear it or the steps grow
        W.grad = None
        # 729 derivatives, one per weight
        loss.backward()
        # downhill: opposite sign to the gradient
        W.data += -rate * W.grad

        if verbose and step % 20 == 0:
            print(f'step {step:<4} loss {loss.item():.4f}')

    # both numbers: one to watch, one to compare
    return W, loss.item(), nll.item()


def sample(W, itos, count=5, seed=SEED):
    g = torch.Generator().manual_seed(seed)
    names = []
    for _ in range(count):
        out, ix = [], 0
        while True:
            # one character in, 27 probabilities out
            probs = forward(torch.tensor([ix]), W)
            ix = torch.multinomial(probs, num_samples=1, replacement=True, generator=g).item()
            out.append(itos[ix])
            if ix == 0:
                break
        names.append(''.join(out[:-1]))
    return names


if __name__ == '__main__':
    words = load()
    stoi, itos = alphabet(words)
    xs, ys = dataset(words, stoi)
    print('examples', xs.nelement())

    W, loss, nll = train(xs, ys, verbose=True)
    print(f'displayed  {loss:.4f}')
    print(f'nll alone  {nll:.4f}')
    print(f'penalty    {loss - nll:.4f}')

    _, plain, _ = train(xs, ys, regularisation=0.0)
    print(f'no penalty {plain:.4f}')

    print('samples', ' '.join(sample(W, itos)))
