# Unit 3 — the Bengio et al. 2003 MLP, at character level

The model from Karpathy's
[*Building makemore Part 2: MLP*](https://youtu.be/TCH_1BHY58I), written by
hand, following [Bengio et al. 2003](https://www.jmlr.org/papers/volume3/bengio03a/bengio03a.pdf).
Every function in `mlp.py` is built by a section of the written unit, and the
verification harness checks that the two copies never drift apart.

## What is here

| file | lines | what it is |
|---|---|---|
| `mlp.py` | 129 | the whole model: data, initialisation, training, evaluation, sampling |
| `verifier.py` | 42 | three checks that say in one command whether it all still holds |
| `names.txt` | 32 033 | the first names, one per line |

## Run

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install torch
python3 mlp.py
```

About **46 seconds** on a laptop. The expected output, to the digit:

```
names    32033
split    182625 22655 22866
params   11897
train   2.1261
dev     2.1731
samples  carpa. zamilli. khi. miri. thay. skansh.
```

It is reproducible because `mlp.py` seeds the **global** generator
(`torch.manual_seed`) on top of the explicit generator passed to the weights.
The original lecture does only the second, which is why its names never come
back the same.

## Verify

```bash
python3 verifier.py
```

```
1. dataset, shape and dtype          OK     expected (228146, 3) int64   got (228146, 3) torch.int64
2. 11897 params, dev in [2.14, 2.20] OK     expected 11897 and the range   got 11897 and 2.1673
3. weight_decay 1e-4 gains >= 0.02   OK     expected >= 0.02              got 0.0463
ALL OK
```

Roughly two minutes: it trains twice.

**Why a range and not a point.** Three runs of the same model, everything
identical except the minibatch draw, give 2.1595, 2.1870 and 2.1899. The spread
is **0.03**: that is the noise floor. Demanding exactly `2.17` would fail a
perfectly correct model one time in two.

**The third check is the one that counts.** It passes only if the penalty
applies to the weights and to `C` but not to the biases, if evaluation runs on
the validation split and not the training one, and if the gain is read against
the noise floor. Three things in one line.

All three were broken on purpose to confirm they can fail. The second is worth
knowing: with a hidden layer of 100 instead of 200, the validation loss is
2.1725, **squarely inside the range**. Only the parameter count catches the
mistake.

## Importing

```python
from mlp import load, alphabet, dataset, split, train, evaluate, sample

words = load('names.txt')
(Xtr, Ytr), (Xdev, Ydev), (Xte, Yte) = split(words)
params = train(Xtr, Ytr, steps=50000)      # a shorter run
print(evaluate(params, Xdev, Ydev))
```

The `if __name__ == '__main__'` block does not run on import: importing does not
trigger the two hundred thousand steps.

## The one knob that pays

`train` takes a `weight_decay` argument. Measured on this file, three seeds per
value, median validation loss:

| penalty | dev | against none |
|---|---|---|
| none | 2.1692 | — |
| 1e-5 | 2.1571 | −0.012, below the noise floor |
| **1e-4** | **2.1210** | **−0.048** |
| 1e-3 | 2.2880 | +0.119, the penalty crushes the model |

`1e-4` is the exact value from the paper. The paper's two other suggestions were
measured as well: early stopping pays nothing here (0.003, ten times below the
noise floor), and a longer context **costs** (+0.043 at `block_size = 5`, +0.165
at 8). The second is the one the lecture presents as most promising.

## Reference environment

Python 3.12.8, torch 2.14.0. The results do not depend on the version; the error
messages do.

`names.txt` is the dataset from [karpathy/makemore](https://github.com/karpathy/makemore),
MIT licensed.
