"""Bigram language model, road one: count the pairs, normalise, sample, score."""
import torch

# 26 letters plus one boundary token
VOCAB = 27
# the lesson's seed, kept so the names are reproducible
SEED = 2147483647


# one name per line, no blank line at the end
def load(path='names.txt'):
    return open(path, 'r').read().splitlines()


def alphabet(words):
    # sorted, because a set has no guaranteed order
    chars = sorted(list(set(''.join(words))))
    stoi = {s: i + 1 for i, s in enumerate(chars)}
    # index 0 was left free by the +1 above
    stoi['.'] = 0
    itos = {i: s for s, i in stoi.items()}
    return stoi, itos


def counts(words, stoi):
    # integers: this counts, it does not measure
    N = torch.zeros((VOCAB, VOCAB), dtype=torch.int32)
    for w in words:
        chs = ['.'] + list(w) + ['.']
        for ch1, ch2 in zip(chs, chs[1:]):
            N[stoi[ch1], stoi[ch2]] += 1      # two indices name one cell
    return N


def probabilities(N, smoothing=1):
    # smoothing=1 lifts the 102 empty cells off zero
    P = (N + smoothing).float()
    # keepdim keeps the (27,1) shape: divide row by row
    P /= P.sum(1, keepdim=True)
    # every row is a distribution, checked not assumed
    assert torch.allclose(P.sum(1), torch.ones(VOCAB))
    return P


def sample(P, itos, count=5, seed=SEED):
    g = torch.Generator().manual_seed(seed)
    names = []
    for _ in range(count):
        out, ix = [], 0
        while True:
            # sample from the row, weighted; not the argmax
            ix = torch.multinomial(P[ix], num_samples=1, replacement=True, generator=g).item()
            out.append(itos[ix])
            # the boundary token was drawn: the name is over
            if ix == 0:
                break
        # drop the trailing boundary token before printing
        names.append(''.join(out[:-1]))
    return names


def average_nll(P, words, stoi):
    total = 0.0
    count = 0
    for w in words:
        chs = ['.'] + list(w) + ['.']
        for ch1, ch2 in zip(chs, chs[1:]):
            # accumulate in float64: 228146 additions add up
            total += torch.log(P[stoi[ch1], stoi[ch2]]).double()
            count += 1
    # negative, and per bigram, so corpora compare
    return (-total / count).item()


if __name__ == '__main__':
    words = load()
    stoi, itos = alphabet(words)
    N = counts(words, stoi)

    print('names   ', len(words))
    print('bigrams ', int(N.sum()))
    print('empty   ', int((N == 0).sum()), 'of', VOCAB * VOCAB)

    for smoothing in (0, 1, 5, 1000000):
        loss = average_nll(probabilities(N, smoothing), words, stoi)
        print(f'smoothing {smoothing:<8} loss {loss:.4f}  perplexity {torch.tensor(loss).exp():.2f}')

    print('samples ', ' '.join(sample(probabilities(N, 1), itos)))
