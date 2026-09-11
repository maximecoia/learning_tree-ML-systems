"""Acceptance test for both roads. Three checks, one command."""
from bigram_count import load, alphabet, counts, probabilities, average_nll
from bigram_count import sample as sample_counts
from bigram_nn import dataset, train
from bigram_nn import sample as sample_net


# print expected AND got: a check that hides both proves nothing
def verdict(name, expected, got, tolerance=0.0001):
    ok = abs(got - expected) <= tolerance
    print(f'{name:<34} {"OK" if ok else "ECART"}   expected {expected}  got {got}')
    return ok


words = load()
stoi, itos = alphabet(words)
N = counts(words, stoi)
xs, ys = dataset(words, stoi)

all_ok = True

# 1. road one reaches the exact optimum
all_ok &= verdict('1. counting, no smoothing',
                  # no smoothing: road one at its exact optimum
                  2.454, round(average_nll(probabilities(N, 0), words, stoi), 4))

# 2. road two gets there by gradient descent
# nll alone, without the penalty, or the comparison lies
W, _, nll = train(xs, ys)
all_ok &= verdict('2. gradient descent, nll alone', 2.475, round(nll, 4))

# 3. the two roads agree on what they generate
counting_names = sample_counts(probabilities(N, 1), itos)
network_names = sample_net(W.detach(), itos)
# the two roads must generate nearly the same names
agree = sum(a == b for a, b in zip(counting_names, network_names))
print(f'{"3. names shared by both roads":<34} '
      f'{"OK" if agree >= 4 else "ECART"}   expected >= 4  got {agree}')
print(' ', ' '.join(counting_names))
print(' ', ' '.join(network_names))
all_ok &= agree >= 4

print('ALL OK' if all_ok else 'SOMETHING IS OFF')
