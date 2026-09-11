<div align="center">

# ML Systems

**A three-year roadmap from a blank file to a contribution in an inference engine,
and the public trace of the work as it happens.**

`prep` → `inference` → `C++ & concurrency` → `parallelism` → `CUDA` → `contribution`

Phase 1 of 8 · September 2026

</div>

---

## About

This repository is the public trace of a roadmap toward ML systems: the layer of
the field where the question is no longer whether a model is correct, but what
it costs to run, and where the time actually goes.

The plan is eight phases and 106 sub-modules, spread across the 42 curriculum
and the years after it. Two layers run in parallel the whole way. The imposed
layer is the 42 common core, which buys the title and the time. The added layer
is what produces anything rare. A phase counts as done when both are.

What lands here is the added layer, in the form that survives being read by
someone else: code that runs, checks that can fail, and a write-up of what each
decision cost.

**One rule holds across every track.** Running is not the bar. Being able to
write it again from a blank file is.

## The roadmap

| Phase | Window | What it buys | Sub-modules |
|---|---|---|---|
| **`ms-00-prepa`** — the prep, C and Python | Sept–Oct 2026 | enter the school with the libft done, a GPT trained by hand, and a C inference engine whose throughput is measured and placed on a roofline | 15 |
| `ms-01-inference` — graded C, measured inference | weeks 1–8 | produce the saturation curve of an unknown inference server in half a day | 18 |
| `ms-02-cpp-concurrence` — C++ and concurrency | weeks 9–20 | concurrent code whose freedom from starvation is shown by measurement, and an unknown execution timeline read in ten minutes | 20 |
| `ms-03-parallelisme` — parallelism, first kernel | weeks 21–34 | say before writing a kernel whether it will be compute- or memory-bound, and justify it to an order of magnitude | 12 |
| `ms-04-cuda` — CUDA properly | weeks 35–46 | a kernel that beats the reference on a bounded case, gain reproducible with its standard deviation, and where it loses too | 17 |
| `ms-05-contribution` — contribution to an engine | weeks 47–57 | a PR in vLLM or SGLang on the scheduler or the cache, gain measured and published, review taken up by a maintainer | 12 |
| `ms-06-specialisation` — specialisation, first internship | 2028 onward | numerical precision, multi-GPU, operations and evaluation, then a page of deliverables that reads without explanation | 11 |
| `ms-07-stage-2` — second internship | after the first | the European arm of an American company in the field | 1 |

Each phase closes on a binary test, not on a feeling. Phase 1 closes on this
one: **draw from memory the path of an input token through to the logits, with
the shapes annotated at every step.**

## Where the work stands

Phase 1, `ms-00-prepa`, is the one in progress.

| Track | State | |
|---|---|---|
| **The Python socle** | 26 of 26 exercises, complete | [`PYTHON.md`](PYTHON.md) |
| **Neural Networks: Zero to Hero** | 8 of 8 units written, 3 shipped with runnable code | [`z2h-karpathy/`](z2h-karpathy) |
| The C engine, the libft | not started here | |

### The Python socle — complete

Three modules, three questions, 26 exercises each small enough to be rebuilt
from a blank file.

| Module | Question | |
|---|---|---|
| [`py-01-basics`](py-01-basics) | Can you get a correct answer out of input you do not control? | 9 of 9 |
| [`py-02-advanced`](py-02-advanced) | Can you build a type that makes the wrong answer unrepresentable? | 9 of 9 |
| [`py-03-livrer`](py-03-livrer) | Can someone else install it and run it without asking you how? | 8 of 8 |

It ends in a command, installed and on the PATH:

```console
$ releve resume mesures.txt
debit n=1 moy=880.00 p95=880.00 req/s
latence n=3 moy=17.67 p95=31.00 ms
```

The full write-up, exercise by exercise, with the decisions that were worth
naming, is in [`PYTHON.md`](PYTHON.md).

### Zero to Hero — three units shipped

Karpathy's eight lectures, rebuilt by hand: a scalar autograd engine, a bigram
model built twice by two unrelated routes, then the Bengio MLP.

| | Unit | Builds | Code |
|---|---|---|---|
| 1 | [`z2h-01-micrograd`](z2h-karpathy/z2h-01-micrograd) | reverse-mode autograd, by hand | **Shipped**, no dependencies |
| 2 | [`z2h-02-bigrammes`](z2h-karpathy/z2h-02-bigrammes) | the same model by counting and by gradient descent | **Shipped** |
| 3 | [`z2h-03-mlp`](z2h-karpathy/z2h-03-mlp) | the Bengio et al. 2003 MLP | **Shipped** |
| 4–8 | activations, backprop, WaveNet, GPT, BPE | | written up, code to come |

```bash
cd z2h-karpathy/z2h-01-micrograd && python3 verifier.py
```

```
1. reference neuron, bit for bit     OK     all five exact
2. a + a gives a.grad == 2           OK     expected 2.0                   got 2
3. loss < 0.01 and 4 signs right     OK     expected < 0.01                got 0.005104
ALL OK
```

The module page is [`z2h-karpathy/README.md`](z2h-karpathy).

## How this is verified

Every track ships checks that can fail, and each one was broken on purpose
before being trusted. A check that cannot fail is worse than no check.

Where a result is deterministic, the check is exact to the digit. Where it is
not, the check compares against a **range** set by the measured noise floor:
three runs of the unit 3 MLP differing only in the minibatch draw give 2.1595,
2.1870 and 2.1899, so the floor is 0.03, and demanding an exact value would fail
a correct model one time in two.

The advice the sources give is measured rather than repeated. Of the three
improvements Bengio et al. 2003 names, one pays (−0.048), one is ten times below
the noise floor, and the one the lecture calls most promising costs (+0.165).

## What comes next

Unit 4, activations and BatchNorm: why a network's initial loss is 27 instead of
3.3, and the diagnostics that say it is sick before the curve does.

After Zero to Hero, phase 1 closes on the C inference engine and the token path
drawn from memory.

## Layout

```
README.md              this page: the roadmap, and where it stands
PYTHON.md              the Python socle, exercise by exercise
py-01-basics/          correct answers out of input you do not control
py-02-advanced/        types that make the wrong answer unrepresentable
py-03-livrer/          the result, installable and on the PATH
z2h-karpathy/          Neural Networks: Zero to Hero
    z2h-01-micrograd/  reverse-mode autograd
    z2h-02-bigrammes/  the bigram model, both roads
    z2h-03-mlp/        the Bengio MLP
```

## Source and licence

The Zero to Hero lectures, notebooks and datasets are Andrej Karpathy's, MIT
licensed: [karpathy/nn-zero-to-hero](https://github.com/karpathy/nn-zero-to-hero),
[karpathy/micrograd](https://github.com/karpathy/micrograd),
[karpathy/makemore](https://github.com/karpathy/makemore). The code here was
typed, not copied. Everything else is original work.
