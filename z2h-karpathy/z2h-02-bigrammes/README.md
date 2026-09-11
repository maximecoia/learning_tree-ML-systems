# Unit 2 — the bigram model, down both roads

The models from Karpathy's
[*The spelled-out intro to language modeling: building makemore*](https://www.youtube.com/watch?v=PaCmpygFfXo),
written by hand. Every function is built by a section of the written unit, and
the verification harness checks that the two copies never drift apart.

What makes this unit particular is that it builds **the same model twice**.
`bigram_count.py` gets there by counting, `bigram_nn.py` by starting from random
weights and correcting them. Both produce a matrix of 27 distributions over 27
characters, and `verifier.py` puts them face to face.

## What is here

| file | lines | what it is |
|---|---|---|
| `bigram_count.py` | 74 | road one: count the pairs, normalise, sample, score |
| `bigram_nn.py` | 79 | road two: one linear layer, trained by gradient descent |
| `verifier.py` | 39 | three checks that say in one command whether it all still holds |
| `check.py` | 6 | the environment: Python, torch, and the dataset in the right place |
| `names.txt` | 32 033 | the first names, one per line |

`bigram_nn.py` **imports** `bigram_count.py` for the alphabet, the seed and the
loading. If both files built `stoi` on their own, nothing would guarantee they
give the same indices, and the final comparison would mean nothing.

## Run

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install torch
python3 bigram_count.py
```

Three seconds. The expected output, to the digit:

```
names    32033
bigrams  228146
empty    102 of 729
smoothing 0        loss 2.4540  perplexity 11.63
smoothing 1        loss 2.4546  perplexity 11.64
smoothing 5        loss 2.4577  perplexity 11.68
smoothing 1000000  loss 3.2946  perplexity 26.97
samples  cexze momasurailezitynn konimittain llayn ka
```

Then the other road:

```bash
python3 bigram_nn.py
```

Two seconds.

```
examples 228146
step 0    loss 3.7686
step 20   loss 2.5823
step 40   loss 2.5213
step 60   loss 2.5027
step 80   loss 2.4944
displayed  2.4901
nll alone  2.4750
penalty    0.0152
no penalty 2.4729
samples cexze momasurailezityha konimittain llayn ka
```

**The last two lines are the result of the unit.** Counting reaches 2.4540,
gradient descent 2.4750, and the sampled names differ by one character across
five names. Two unrelated paths, the same object.

## Three numbers not to confuse

`bigram_nn.py` prints three because they say three different things:

| number | value | what it is |
|---|---|---|
| `displayed` | 2.4901 | what gradient descent minimises: the loss **plus** the regulariser |
| `nll alone` | **2.4750** | the negative log-likelihood alone, **the only number comparable to road one** |
| `penalty` | 0.0152 | what the `0.01 * (W**2).mean()` term adds |
| `no penalty` | 2.4729 | the same training with no regulariser at all |

Comparing 2.4901 to 2.4540 would suggest a gap of 0.036 where it is 0.021: the
penalty is the same order of magnitude as the thing being measured. That is why
`train` returns `nll` separately instead of the displayed loss alone.

## Verify

```bash
python3 verifier.py
```

```
1. counting, no smoothing          OK   expected 2.454  got 2.454
2. gradient descent, nll alone     OK   expected 2.475  got 2.475
3. names shared by both roads      OK   expected >= 4  got 4
  cexze momasurailezitynn konimittain llayn ka
  cexze momasurailezityha konimittain llayn ka
ALL OK
```

Two and a half seconds.

**Why exact values and not ranges.** Both roads are perfectly deterministic
here: counting has nothing random in it, and gradient descent works on the
**full batch** with a fixed seed. There is no noise floor to respect. Unit 3,
which draws minibatches, does not have that comfort and has to demand a range.

**The third check is the one that counts.** The first two each verify one road
on its own; the third is the only one that verifies they agree. It passes only
if the alphabet is shared, if the sampling seed is the same on both sides, and
if the two matrices are close enough that the same draw produces the same
letters.

All three were broken on purpose to confirm they can fail:

| what is broken | what the check says |
|---|---|
| `probabilities(N, 0)` becomes `probabilities(N, 1)` | `ECART expected 2.454 got 2.4546` |
| reading the displayed loss instead of `nll` | `ECART expected 2.475 got 2.4901` |
| `sample_net` is given another seed | `ECART expected >= 4 got 0` |

The second is worth knowing: the mistake it catches, confusing the displayed
loss with the log-likelihood, is exactly the one made by reading the output of
`bigram_nn.py` too quickly.

## Importing

Both files import without running anything: their
`if __name__ == '__main__'` block does not fire on import.

```python
from bigram_count import load, alphabet, counts, probabilities, average_nll
from bigram_nn import dataset, train, forward

words = load('names.txt')
stoi, itos = alphabet(words)

N = counts(words, stoi)                       # road one
P = probabilities(N, smoothing=1)
print(average_nll(P, words, stoi))

xs, ys = dataset(words, stoi)                 # road two
W, loss, nll = train(xs, ys, steps=100)
print(nll)
```

## The one knob on road one

`probabilities` takes a `smoothing` argument. Measured on this file:

| smoothing | loss | perplexity | what happens |
|---|---|---|---|
| 0 | **2.4540** | 11.63 | the exact optimum, but 102 cells are zero, and a word crossing one takes an infinite loss |
| **1** | 2.4546 | 11.64 | six ten-thousandths dearer, and no infinities left |
| 5 | 2.4577 | 11.68 | the cost starts to show |
| 1 000 000 | 3.2946 | 26.97 | the counts are drowned, the model is uniform again |

`1` is the right setting, and it is not justified by the loss, which gets worse,
but by the fact that it **removes the infinities**. The cost is 0.0006.

On road two that knob is called `regularisation` and does the same thing by
another means: pulling the weights towards zero pulls the distributions towards
uniform.

## The wall

This model looks **one** character back. The table has 27² = 729 cells, and
228 146 pairs to fill them.

| context | cells | pairs per cell |
|---|---|---|
| 1 | 729 | 312.96 |
| 2 | 19 683 | 11.59 |
| 3 | 531 441 | 0.43 |
| 10 | 5 559 060 566 555 523 | 0.00 |

At three characters of context there is already less than one observation per
cell. The table grows exponentially, the data does not: **that is the wall of
road one**, and it is where unit 3 begins.

## Reference environment

Python 3.12.8, torch 2.14.0. The results do not depend on the version; the error
messages do.

```bash
python3 check.py
```

`names.txt` is the dataset from [karpathy/makemore](https://github.com/karpathy/makemore),
MIT licensed.
