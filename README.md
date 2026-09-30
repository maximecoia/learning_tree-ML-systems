<div align="center">

# ML Systems

**From a blank file to a contribution in an inference engine, and the public
trace of the work as it happens.**

`prep` → `inference` → `C++ & concurrency` → `parallelism & contribution` → `CUDA` → `common core` → `specialisation`

Phase 1 of 8 · September 2026

</div>

---

## What this is

ML systems is the part of machine learning where the model is taken as given
and the questions are about running it: what it costs, where the time goes,
what saturates first, and what a change actually buys. It is where an inference
server, a scheduler, a cache or a kernel decides whether a model is usable at
all.

This repository is the public trace of a roadmap toward that field, eight
phases and 93 sub-modules, from a prep before the 42 school to a second
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
  not on a date: phase 1 closes when `gpt.py`, written from a blank file,
  passes the seven gates of [its acceptance test](#the-acceptance-test).
- **Nothing is graded by its own author alone.** The route borrows its steps
  from existing assignments, most of which ship their own grader, and all of
  them lead to an acceptance test written before the work. A lesson marked by
  the person who wrote it has no outside referent.
- **Running is not the bar.** Being able to write it again from a blank file
  is.
- **Every check has been seen to fail.** Each one is broken on purpose before
  it is trusted, because a check that cannot fail is worse than no check.

The measurements behind these rules, and every decision that changed the
roadmap, are in [`DECISIONS.md`](DECISIONS.md).

## The roadmap

| Phase | Window | What it buys | Sub-modules |
|---|---|---|---|
| **[`ms-00-prepa`](ms-00-prepa)** — the prep, C and Python | Sept–Oct 2026 | enter the school with the libft done, a GPT trained by hand, and a C inference engine whose throughput is measured and placed on a roofline | 11 |
| [`ms-01-inference`](ms-01-inference) — graded C, measured inference | weeks 1–8 | produce the saturation curve of an unknown inference server in half a day | 13 |
| [`ms-02-cpp-concurrence`](ms-02-cpp-concurrence) — C++ and concurrency | weeks 9–20 | concurrent code whose freedom from starvation is shown by measurement, and an unknown execution timeline read in ten minutes | 18 |
| [`ms-03-parallelisme`](ms-03-parallelisme) — parallelism, first kernel, entering vLLM | weeks 21–34 | say before writing a kernel whether it will be compute- or memory-bound, and a PR in vLLM or SGLang on the scheduler or the cache, review taken up by a maintainer | 20 |
| [`ms-04-cuda`](ms-04-cuda) — CUDA properly | weeks 35–46 | a kernel that beats the reference on a bounded case, gain reproducible with its standard deviation and where it loses too, then the harness that proves it, run against an agent and shown rejecting a bad submission | 17 |
| [`ms-05-fin-tronc-commun`](ms-05-fin-tronc-commun) — the end of the common core | weeks 47–57 | the four remaining imposed projects, crossed fast and with nothing added for pleasure | 4 |
| [`ms-06-specialisation`](ms-06-specialisation) — specialisation, first internship | 2028 onward | numerical precision, multi-GPU, operations and evaluation, then a page of deliverables that reads without explanation | 9 |
| [`ms-07-stage-2`](ms-07-stage-2) — second internship | after the first | the European arm of an American company in the field | 1 |

The windows are the plan's own, not a commitment. A phase opens on its
prerequisites rather than on a date, so the order is fixed and the pace is not.
Each phase has its own page, generated from the curriculum, with its
sub-modules in the order of the work and the state of each.

## Where the work stands

<!-- compteurs: written by carte_phases.py from the graders. Do not edit by hand. -->
Phase 1, [`ms-00-prepa`](ms-00-prepa), is the one in progress: **53 of 53 graded exercises** pass. It closes on 31 October 2026, its route on 18 October 2026. Every number in this section is read from a grader by `carte_phases.py`, and [the phase page](ms-00-prepa/README.md#what-to-do-in-order) lists the work in order with the next step marked.

| Track | State | |
|---|---|---|
| The Python socle | ✓ 26 of 26 exercises, complete | [`PYTHON.md`](PYTHON.md) |
| The libft, ahead of the school | ✓ 6 of 6 exercises, complete, kept out of this repository | [below](#what-is-not-here) |
| The route to the trained GPT | 5 of 6 steps · step 6 out of the window | [the phase page](ms-00-prepa/README.md#what-to-do-in-order) |
| **L1, the trained model** | 0 of 7 gates · gpt.py is still the blank file, then the public repository | [the acceptance test](#the-acceptance-test) |
| The C inference engine | 0 of 7 · out of the window, it needs the weights L1 produces | [below](#what-is-not-here) |
| Maths, in the background | ✓ 20 of 20 exercises, complete, alongside the route | [`MATHS.md`](MATHS.md) |

The denominator leaves out `rte-02-cs336` (out of the window until 31 October, L1 comes first), `l1-01-gpt-corpus` (graded by its public repository, not by a terminal) and `c-02-moteur` (out of the window, it needs the weights L1 produces).
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

## Phase 1: a GPT trained by hand

The prep is graded on one object: a causal GPT written from a blank file, in
`torch`, with the attention written by hand rather than called. The route to it
borrows each step from an existing assignment:

| | Step | What grades it |
|---|---|---|
| 1 | Tensor Puzzles — 21 puzzles, one expression each, twenty of them inside eighty columns | the checker inside the notebook |
| 2 | Text data: tokenizer, sliding window, embeddings | `test_ch02.py`: upstream's test and four of mine |
| 3 | Causal attention: scores, mask, multiple heads | `test_ch03.py` |
| 4 | The GPT: blocks, normalisation, residuals, logits | `test_ch04.py` |
| 5 | Pretraining: the loop, train and validation loss, sampling | `test_ch05.py` |
| 6 | CS336 assignment 1 — the 15 architecture-agnostic adapters | its public `pytest` suite |

Raschka's book ships almost no assertions, so the tests of steps 2 to 5 are
written here, against what each chapter states, and each suite was broken on
purpose to prove it can fail ([why](DECISIONS.md#borrowed-graders-not-written-lessons)).
They sit beside each answer, in
[`ms-00-prepa/rte-route-l1`](ms-00-prepa/rte-route-l1), and run once that
directory is copied into a clone of the book. Step 6 grades the same material a
second way and waits until 31 October: of its 21 adapters, the 15 that do not
depend on the architecture cover exactly steps 1 to 5.

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
was never trained would pass the other six. What lands here with it is the
trained model, the corpus with its provenance, the full curves, unsorted
samples, and a write-up that holds up without the code on screen.

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
    maths-01-algebre/      vectors and matrices by hand, before any library
    mth-03-probas/         a simulator held against its closed forms
    mth-04-statistiques/   whether two series really differ, and how often that is wrong
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
Stanford CS336, *Language Modeling from Scratch*
([`stanford-cs336`](https://github.com/stanford-cs336)) · Sasha Rush,
[Tensor Puzzles](https://github.com/srush/Tensor-Puzzles).

The road that was taken off, [described here](DECISIONS.md#zero-to-hero-and-why-it-left):
the Zero to Hero lectures, notebooks and datasets are Andrej Karpathy's, MIT
licensed: [karpathy/nn-zero-to-hero](https://github.com/karpathy/nn-zero-to-hero),
[karpathy/micrograd](https://github.com/karpathy/micrograd),
[karpathy/makemore](https://github.com/karpathy/makemore). What was built from
them here was typed, not copied, and it remains in this repository's history.

Everything else is original work, under the MIT licence.
