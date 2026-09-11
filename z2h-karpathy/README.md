<div align="center">

# Neural Networks: Zero to Hero

**The eight Karpathy lectures, rebuilt from a blank file.**

`micrograd` → `bigrams` → `MLP` → `activations` → `backprop` → `WaveNet` → `GPT` → `BPE`

3 of 8 units shipped with runnable code · 8 of 8 written up

</div>

---

## About

[Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html) builds a
language model from nothing: a scalar autograd engine, then a bigram model, then
an MLP, then the tricks that keep a deep network trainable, then a Transformer,
then the tokenizer underneath it all.

Each unit here is written up first as a long-form course, one section per
chapter of the lecture, and the code in these folders is generated from that
write-up. The write-up is the source of truth: a harness runs every code block
in reading order and compares its output character by character to what the page
prints. These files are the copy, verified identical.

The rule of the tree applies here too. Running is not the bar. Being able to
write it again from a blank file is.

## What ships here

| | Unit | Lecture | Builds | Code |
|---|---|---|---|---|
| 1 | [`z2h-01-micrograd`](z2h-01-micrograd) | 2 h 25, 22 ch. | reverse-mode autograd, by hand | **Shipped**, 3 files, no dependencies |
| 2 | [`z2h-02-bigrammes`](z2h-02-bigrammes) | 1 h 57, 24 ch. | the same bigram model twice, by counting and by gradient descent | **Shipped**, 4 files |
| 3 | [`z2h-03-mlp`](z2h-03-mlp) | 1 h 16, 19 ch. | the Bengio et al. 2003 MLP at character level | **Shipped**, 2 files |
| 4 | activations | 1 h 56, 17 ch. | initialisation, BatchNorm, the diagnostics of a sick network | Written up |
| 5 | backprop | 1 h 55, 8 ch. | the gradients by hand, `loss.backward()` deleted | Written up |
| 6 | WaveNet | 56 min, 18 ch. | a context fused two by two instead of flattened | Written up |
| 7 | GPT | 1 h 56, 30 ch. | the decoder Transformer, attention to a trained model | Written up |
| 8 | BPE | 2 h 13, 24 ch. | the tokenizer, and why a model sees neither letters nor words | Written up |

162 chapters covered, 14 h 34 of lecture. Units 4 to 8 exist as written courses;
their code is not in this repository yet.

## Run one

Unit 1 needs nothing but Python.

```bash
cd z2h-01-micrograd && python3 verifier.py
```

```
1. reference neuron, bit for bit     OK     all five exact
2. a + a gives a.grad == 2           OK     expected 2.0                   got 2
3. loss < 0.01 and 4 signs right     OK     expected < 0.01                got 0.005104
ALL OK
```

Units 2 and 3 need `torch`.

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install torch
cd z2h-03-mlp && python3 verifier.py
```

## Decisions worth naming

### A check is compared to a range, not a point

Three runs of the unit 3 MLP, everything identical except the minibatch draw,
give 2.1595, 2.1870 and 2.1899. The spread is **0.03**. That is the noise floor,
and demanding an exact value would fail a correct model one time in two.

Where there is no noise, the check is exact. Unit 2 counts, and trains on the
full batch with a fixed seed, so both its roads are deterministic and both are
held to the digit.

### Every check was broken on purpose

A check that cannot fail is worse than no check. Each one was made to fail
before being trusted, and the failure mode is recorded:

| what is broken | what the check says |
|---|---|
| `probabilities(N, 0)` becomes `probabilities(N, 1)` | `ECART expected 2.454 got 2.4546` |
| the displayed loss is read instead of `nll` | `ECART expected 2.475 got 2.4901` |
| `sample_net` is given another seed | `ECART expected >= 4 got 0` |

The second is the mistake anyone makes reading the output of `bigram_nn.py` too
fast: the displayed loss includes the regulariser, and the regulariser is the
same order of magnitude as the gap being measured.

### The lecture's advice is measured, not repeated

Bengio et al. 2003 names three improvements the lecture leaves aside. Measured
on `mlp.py`, three seeds each, median validation loss:

| advice | effect |
|---|---|
| `weight_decay = 1e-4` | **−0.048**, the only one that pays |
| early stopping | −0.003, ten times below the noise floor |
| `block_size` to 5, then 8 | **+0.043**, then **+0.165**: it costs |

The third is the one the lecture presents as most promising.

### One check per unit catches what the others cannot

Unit 3's parameter count looks redundant next to the loss range. It is not: with
a hidden layer of 100 instead of 200 the validation loss is 2.1725, squarely
inside the accepted range. Only the parameter count catches that mistake.

## Source and licence

The lectures, notebooks and datasets are Andrej Karpathy's, MIT licensed:
[karpathy/nn-zero-to-hero](https://github.com/karpathy/nn-zero-to-hero),
[karpathy/micrograd](https://github.com/karpathy/micrograd),
[karpathy/makemore](https://github.com/karpathy/makemore). `names.txt` comes
from the last of these. The code in these folders was typed, not copied, and the
written units that produced it are separate work.
