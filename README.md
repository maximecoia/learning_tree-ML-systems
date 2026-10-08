<div align="center">

# ML Systems

**From a blank file to a contribution in an inference engine, and the public
trace of the work as it happens.**

`prep` → `inference` → `C++ & concurrency` → `parallelism & contribution` → `CUDA` → `common core` → `specialisation`

Phase 2 of 8 · October 2026

</div>

---

## What this is

ML systems is the part of machine learning where the model is taken as given
and the questions are about running it: what it costs, where the time goes,
what saturates first, and what a change actually buys. It is where an inference
server, a scheduler, a cache or a kernel decides whether a model is usable at
all.

This repository is the public trace of a roadmap toward that field, eight
phases and 94 sub-modules, from a prep before the 42 school to a second
internship. It aims at three things a reader can check from outside:

- the saturation curve of an unknown inference server, produced in half a day;
- a pull request in vLLM or SGLang, on the scheduler or the cache, whose review
  a maintainer takes up;
- a CUDA kernel that beats the reference on a bounded case, with the harness
  that proves the gain survives a replay.

What lands here is the work in the form that survives being read by someone
else: code that runs, checks that can fail, and a write-up of what each
decision cost.

## How it is built

- **Two layers run in parallel.** The imposed layer is the 42 common core,
  which buys the title and the time. The added layer is what produces anything
  rare, and it is what this repository holds. A phase counts as done when both
  are.
- **A phase ends on a binary test, named in advance.** Not on a feeling, and
  not on a date: phase 1 closed on 2 October 2026, when `gpt.py`, written
  from a blank file, passed the seven gates of
  [its acceptance test](#the-acceptance-test).
- **Nothing is graded by its own author alone.** The route borrows its steps
  from existing work: the first ships its own grader, the chapters after it
  are graded by tests written against what each chapter states, and all of
  them lead to an acceptance test written before the work, whose failure
  values are published. A lesson marked by the person who wrote it has no
  outside referent.
- **Running is not the bar.** Being able to write it again from a blank file
  is.
- **Every check has been seen to fail.** Each one is broken on purpose before
  it is trusted, because a check that cannot fail is worse than no check.

The measurements behind these rules, and every decision that changed the
roadmap, are in [`DECISIONS.md`](DECISIONS.md).

## The roadmap

| Phase | Window | What it buys | Sub-modules |
|---|---|---|---|
| [`ms-00-prepa`](ms-00-prepa) — the prep, C and Python | Sept–Oct 2026 | enter the school with the libft done and a GPT trained by hand | 9 |
| **[`ms-01-inference`](ms-01-inference)** — graded C, measured inference | weeks 1–8 | the saturation curve of an unknown inference server produced in half a day, then an inference engine written in C and placed on a roofline | 16 |
| [`ms-02-cpp-concurrence`](ms-02-cpp-concurrence) — C++ and concurrency | weeks 9–20 | concurrent code whose freedom from starvation is shown by measurement, and an unknown execution timeline read in ten minutes | 21 |
| [`ms-03-parallelisme`](ms-03-parallelisme) — parallelism, first kernel, entering vLLM | weeks 21–34 | say before writing a kernel whether it will be compute- or memory-bound, and a PR in vLLM or SGLang on the scheduler or the cache, review taken up by a maintainer | 20 |
| [`ms-04-cuda`](ms-04-cuda) — CUDA properly | weeks 35–46 | a kernel that beats the reference on a bounded case, gain reproducible with its standard deviation and where it loses too, then the harness that proves it, run against an agent and shown rejecting a bad submission | 17 |
| [`ms-05-fin-tronc-commun`](ms-05-fin-tronc-commun) — the end of the common core | weeks 47–57 | the last imposed project, crossed fast and with nothing added for pleasure | 1 |
| [`ms-06-specialisation`](ms-06-specialisation) — specialisation, first internship | 2028 onward | numerical precision, multi-GPU, operations and evaluation, then a page of deliverables that reads without explanation | 9 |
| [`ms-07-stage-2`](ms-07-stage-2) — second internship | after the first | the European arm of an American company in the field | 1 |

The windows are the plan's own, not a commitment. A phase opens on its
prerequisites rather than on a date, so the order is fixed and the pace is not.
Each phase has its own page, generated from the curriculum, with its
sub-modules in the order of the work and the state of each.

## Where the work stands

<!-- compteurs: written by carte_phases.py from the graders. Do not edit by hand. -->
Phase 2, [`ms-01-inference`](ms-01-inference), is the one in progress: **23 of 58 graded exercises** pass. Its window is weeks 1–8; [`ms-00-prepa`](ms-00-prepa) closed on 2 October 2026. Every number in this section is read from a grader by `carte_phases.py`, and [the phase page](ms-01-inference/README.md#what-to-do-in-order) lists the work in order with the next step marked.

| Track | State | |
|---|---|---|
| The C of the common core, milestones 1 to 3 | 0 of 12 exercises, kept out of this repository | [below](#what-is-not-here) |
| Measuring performance | ✓ 16 of 16 exercises, complete | [the phase page](ms-01-inference/README.md#what-to-do-in-order) |
| Measured inference | 6 of 23 exercises | [the phase page](ms-01-inference/README.md#what-to-do-in-order) |
| The inference engine in C | 1 of 7 exercises | [the phase page](ms-01-inference/README.md#what-to-do-in-order) |
| L2, the throughput and latency curve | a person grades it, not a terminal | [the phase page](ms-01-inference/README.md#what-to-do-in-order) |

The denominator leaves out `l2-01-courbe` (a public write-up, graded by a reader, not by a terminal).
<!-- /compteurs -->

## What is already here

- **[The Python socle](PYTHON.md)**, 26 exercises in three modules, from input
  you do not control to a command installed on the PATH.
- **[The maths](MATHS.md)**, 20 exercises in three modules, in plain Python:
  linear algebra up to a 2D transformation engine, probability held against
  closed forms, and statistics that count their own error rate.
- **[Tensor Puzzles](ms-00-prepa/rte-01-puzzles)**, Sasha Rush's twenty-one
  puzzles, each solved in one expression.
- **[The route's chapters 2 to 5](ms-00-prepa/rte-route-l1)**, answers to
  Raschka's book, each with tests that assert what its chapter states.
- **[The acceptance test of phase 1](ms-00-prepa/l1-01-gpt-corpus/verifier.py)**,
  black-box, written before the model it grades.

Before the roadmap, and in its own repository:
**[`unix-toolbox`](https://github.com/maximecoia/unix-toolbox)**, four Unix
utilities rebuilt in C on the system calls, `mini_echo`, `mini_cat`, `mini_cp`
and `mini_wc`. The rule that every check is seen to fail holds there too: the
utilities were broken on purpose fourteen ways in all, and the tests catch
thirteen. That includes the short writes and failing reads no shell test can
provoke, reached by rebuilding the utilities with `write()` redirected at
compile time, and `mini_cp` with `read()` as well.

## Phase 1: a GPT trained by hand

The prep is graded on one object: a causal GPT written from a blank file, in
`torch`, with the attention written by hand rather than called. The route to it
borrows each step from existing work:

| | Step | What grades it |
|---|---|---|
| 1 | Tensor Puzzles — 21 puzzles, one expression each, twenty of them inside eighty columns | the checker inside the notebook |
| 2 | Text data: tokenizer, sliding window, embeddings | `test_ch02.py`: upstream's test and four of mine |
| 3 | Causal attention: scores, mask, multiple heads | `test_ch03.py` |
| 4 | The GPT: blocks, normalisation, residuals, logits | `test_ch04.py` |
| 5 | Pretraining: the loop, train and validation loss, sampling | `test_ch05.py` |

Raschka's book ships almost no assertions, so the tests of steps 2 to 5 are
written here, against what each chapter states, and each suite was broken on
purpose to prove it can fail ([why](DECISIONS.md#borrowed-graders-not-written-lessons)).
They sit beside each answer, in
[`ms-00-prepa/rte-route-l1`](ms-00-prepa/rte-route-l1), and run once that
directory is copied into a clone of the book. The first assignment of CS336 used
to be step 6, and it left the route on 2026-09-30: its fifteen
architecture-agnostic adapters graded steps 2 to 5 a second time
([why](DECISIONS.md#cs336-and-why-it-left-the-prep)). Its three pieces that
belong to Llama rather than to GPT-2, RMSNorm, SwiGLU and RoPE, moved to
[`ms-01-inference`](ms-01-inference/README.md).

### The acceptance test

It is black-box, already written, and it states what breaking each check costs,
measured against a reference implementation:
[`ms-00-prepa/l1-01-gpt-corpus/verifier.py`](ms-00-prepa/l1-01-gpt-corpus/verifier.py).
It reads tensors in and tensors out, never the architecture, so any number of
layers, heads or norms passes as long as the model is a causal language model.

| Gate | What has to land |
|---|---|
| 1 | `(B,T) → (B,T,V)`, and no loss when no target is given |
| 2 | loss at initialisation inside `[4.12, 4.92]`, where `ln(65) = 4.1744` |
| 3 | drift **exactly 0.0** when tokens after position `t` change; dropping the mask gives 1.42e-01 |
| 4 | 0.0010 on a task only position can solve; without position embeddings it sits at 3.4658 |
| 5 | 0.0108 after 400 steps overfitting 32 fixed sequences |
| 6 | `generate` survives a context longer than the block size |
| 7 | the trained weights, measured on dev, land 0.10 below a counted bigram on the same split: 2.0856 against a bar of 2.3743, and weights never trained sit at 4.3370 |

Gates 1 to 6 grade the model, gate 7 its training: without it, a `gpt.py` that
was never trained would pass the other six.

### What closes L1

L1 comes in two parts. The phase closes on the first, and L1 itself needs both.

1. **The model.** `gpt.py`, written from a blank file, passes the seven gates
   above. A terminal grades it, through `./exo` or `python3 verifier.py`.
2. **The public write-up**, the curriculum's `l1-01-gpt-corpus`. A person
   grades it, and its one criterion is that someone else replays it without
   asking a question. It lands here with the model, and holds:
   - the chosen corpus, with its source, its licence, and a preparation script
     that rebuilds the same split;
   - the training run on that corpus, with the seed, the hyperparameters and
     the dependency versions committed, and the weights attached to a release
     rather than kept in the git history;
   - train and validation loss on one graph, the whole curve, with the step
     kept and why;
   - several unsorted samples, with their seed;
   - every number beside a baseline: validation loss against `ln(V)` and the
     bigram, the parameter count and how it was counted, the training time and
     the machine;
   - what was not tried, the bugs found afterwards, and what they change;
   - a token's path to the logits drawn from memory with its shapes, in a
     report that holds up without the code on screen.

## What is not here

**The 42 subjects.** The libft and the projects that follow it are the school's
subjects, and publishing a solution to one is against its charter. This
repository is also the tree the grader reads, so finishing one here would
publish it by accident. The `.gitignore` refuses them by name, from the
curriculum's own list. What is built on top of them, like the C inference
engine, lands here.

**Other people's assignments.** The book, its corpus and CS336 stay in their
own repositories; only my answers to them are here, credited below.

**The private corpus.** The notes, lessons and study sheets that produce this
work stay private. What is published is the code typed by hand and the checks
that grade it.

## How this is verified

[`tools/check.py`](tools/check.py) asks three questions of this repository,
using nothing but this repository: does the published Python parse, do the
links between these pages resolve, anchors included, and does `.gitignore`
agree with what git actually tracks. Each question was proven able to fail
before being trusted, and a workflow runs the three on every push.

The pages that describe the work are generated rather than written: the phase
pages, the counters above and the tree below are read from the curriculum,
from the graders and from what git publishes. Each time this page drifted in
the past, the cause was a figure copied by hand, and a page that reads its
sources cannot drift without them.

## Layout

One folder per phase, and inside it one folder per sub-module.

<!-- arbre: written by carte_phases.py from what git publishes. Do not edit by hand. -->
```
.github/                   the workflow that runs tools/check.py on every push
.gitignore                 what stays out, and why: 42 subjects above all
DECISIONS.md               the decisions that changed the roadmap, with their evidence
LICENSE                    MIT, and the credits owed are in Sources and licence below
MATHS.md                   the maths, module by module, and what they measured
PYTHON.md                  the Python socle, exercise by exercise
README.md                  this page: what ML Systems is, the roadmap, and where it stands
tools/                     the checks this repository can run on itself
ms-00-prepa/               the prep — Sept–Oct 2026
    README.md              its sub-modules in the order of the work, and their state
    l1-01-gpt-corpus/      the acceptance test, written before the work it grades
    mth-01-algebre/        vectors and matrices by hand, before any library
    mth-02-probas/         a simulator held against its closed forms
    mth-03-statistiques/   whether two series really differ, and how often that is wrong
    py-01-basics/          correct answers out of input you do not control
    py-02-advanced/        types that make the wrong answer unrepresentable
    py-03-livrer/          the result, installable and on the PATH
    rte-01-puzzles/        Sasha Rush's twenty-one puzzles, solved and credited
    rte-route-l1/          the route's chapters, answers to Raschka's book
ms-01-inference/ … ms-07-stage-2/
    README.md              the same page, for a phase not yet opened
```
<!-- /arbre -->

## Sources and licence

The route: Sebastian Raschka, *Build a Large Language Model (From Scratch)*
([`rasbt/LLMs-from-scratch`](https://github.com/rasbt/LLMs-from-scratch)) ·
Sasha Rush, [Tensor Puzzles](https://github.com/srush/Tensor-Puzzles).

Further on: Stanford CS336, *Language Modeling from Scratch*
([`stanford-cs336`](https://github.com/stanford-cs336)), whose first
assignment grades three pieces of `ms-01-inference` and whose second is planned
in `ms-06-specialisation`.

The road that was taken off, [described here](DECISIONS.md#zero-to-hero-and-why-it-left):
the Zero to Hero lectures, notebooks and datasets are Andrej Karpathy's, MIT
licensed: [karpathy/nn-zero-to-hero](https://github.com/karpathy/nn-zero-to-hero),
[karpathy/micrograd](https://github.com/karpathy/micrograd),
[karpathy/makemore](https://github.com/karpathy/makemore). What was built from
them here was typed, not copied, and it remains in this repository's history.

Everything else is original work, under the MIT licence.
