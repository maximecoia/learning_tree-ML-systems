<div align="center">

# ML Systems

**From a blank file to a contribution in an inference engine, and the public
trace of the work as it happens.**

`prep` → `inference` → `C++ & concurrency` → `parallelism & contribution` → `CUDA` → `common core`

Phase 1 of 8 · September 2026

</div>

---

## About

This repository is the public trace of a roadmap toward ML systems: the layer of
the field where the question is no longer whether a model is correct, but what
it costs to run, and where the time actually goes.

The plan is eight phases and 95 sub-modules, spread across the 42 curriculum
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
| **[`ms-00-prepa`](ms-00-prepa)** — the prep, C and Python | Sept–Oct 2026 | enter the school with the libft done, a GPT trained by hand, and a C inference engine whose throughput is measured and placed on a roofline | 11 |
| [`ms-01-inference`](ms-01-inference) — graded C, measured inference | weeks 1–8 | produce the saturation curve of an unknown inference server in half a day | 14 |
| [`ms-02-cpp-concurrence`](ms-02-cpp-concurrence) — C++ and concurrency | weeks 9–20 | concurrent code whose freedom from starvation is shown by measurement, and an unknown execution timeline read in ten minutes | 19 |
| [`ms-03-parallelisme`](ms-03-parallelisme) — parallelism, first kernel, entering vLLM | weeks 21–34 | say before writing a kernel whether it will be compute- or memory-bound, and a PR in vLLM or SGLang on the scheduler or the cache, review taken up by a maintainer | 20 |
| [`ms-04-cuda`](ms-04-cuda) — CUDA properly | weeks 35–46 | a kernel that beats the reference on a bounded case, gain reproducible with its standard deviation and where it loses too, then the harness that proves it, run against an agent and shown rejecting a bad submission | 17 |
| [`ms-05-fin-tronc-commun`](ms-05-fin-tronc-commun) — the end of the common core | weeks 47–57 | the four remaining imposed projects, crossed fast and with nothing added for pleasure | 4 |
| [`ms-06-specialisation`](ms-06-specialisation) — specialisation, first internship | 2028 onward | numerical precision, multi-GPU, operations and evaluation, then a page of deliverables that reads without explanation | 9 |
| [`ms-07-stage-2`](ms-07-stage-2) — second internship | after the first | the European arm of an American company in the field | 1 |

The windows are the plan's own, not a commitment. A phase opens on its
prerequisites rather than on a date, so the order is fixed and the pace is not.
The aim is to close them earlier than written.

What does not move is how a phase ends: on a binary test, not on a feeling.
Phase 1 closes on this one: **draw from memory the path of an input token
through to the logits, with the shapes annotated at every step.**

## Where the work stands

<!-- compteurs: written by carte_phases.py from the graders. Do not edit by hand. -->
Phase 1, [`ms-00-prepa`](ms-00-prepa), is the one in progress: **33 of 58 graded exercises** pass. It closes on 31 October 2026, its route on 18 October 2026. Every number in this section is read from a grader by `carte_phases.py`, and [the phase page](ms-00-prepa/README.md#what-to-do-in-order) lists the work in order with the next step marked.

| Track | State | |
|---|---|---|
| The Python socle | ✓ 26 of 26 exercises, complete | [`PYTHON.md`](PYTHON.md) |
| The libft, ahead of the school | ✓ 6 of 6 exercises, complete, kept out of this repository | [below](#why-the-c-tracks-are-not-here) |
| **The route to the trained GPT** | 1 of 6 steps · now: step 2, Text data: tokenizer, sliding window, embeddings (Raschka ch. 2) | [the phase page](ms-00-prepa/README.md#what-to-do-in-order) |
| L1, the trained model | 0 of 6 gates · gpt.py is still the blank file, then a quiz | [the acceptance test](#the-acceptance-test) |
| The C inference engine | 0 of 7 · out of the window, it needs the weights L1 produces | [below](#why-the-c-tracks-are-not-here) |
| Maths, in the background | 0 of 20 exercises, alongside the route |  |
| Zero to Hero | taken off the path, and out of this repository | [below](#zero-to-hero-and-why-it-left) |

The denominator leaves out `l1-01-gpt-corpus` (a quiz no terminal grades) and `c-02-moteur` (out of the window, it needs the weights L1 produces). Zero to Hero is not in it either: the curriculum stopped declaring it, and counting an abandoned track in a ratio makes a decision look like a delay.
<!-- /compteurs -->

## The route to the trained GPT

The phase is graded on one object: a causal GPT written from a blank file, in
`torch`, with the attention written by hand rather than called.

**Nothing in this repository teaches it, and that is deliberate.** The plan used
to carry its own course, and the count that ended it is short: over eleven days
it produced 141,783 lines of written lessons and 2,038 lines of machine
learning code, while zero of the thirty-four exercises that already existed had
been handed in. A lesson written by hand and then marked by its own author has
no external referent. So every step is now handed to an assignment that already
ships its own grader.

| | Step | What grades it |
|---|---|---|
| 1 | Tensor Puzzles — 21 puzzles, one line each | the checker inside the notebook |
| 2 | Text data: tokenizer, sliding window, embeddings | the book's exercise solutions and chapter quiz |
| 3 | Causal attention: scores, mask, multiple heads | same, plus gate 3 below |
| 4 | The GPT: blocks, normalisation, residuals, logits | gates 1, 2, 4 and 6 below |
| 5 | Pretraining: the loop, train and validation loss, sampling | gate 5 below |
| 6 | CS336 assignment 1 — the 15 architecture-agnostic adapters | its public `pytest` suite |

Step 6 is the one that makes the rest checkable by something other than a
reading. Of that assignment's 21 adapters, 15 do not depend on its architecture
— softmax, cross entropy, AdamW, batching, checkpoints, attention without
positions — and those 15 cover exactly the material of steps 1 to 5. The
remaining 6 are the 2026 variants, and they come after the deliverable.

### The acceptance test

It is already written, it is black-box, and it states what breaking each check
costs, measured against a reference implementation rather than asserted.

| Gate | What has to land |
|---|---|
| 1 | `(B,T) → (B,T,V)`, and no loss when no target is given |
| 2 | loss at initialisation inside `[4.12, 4.92]`, where `ln(65) = 4.1744` |
| 3 | drift **exactly 0.0** when tokens after position `t` change — dropping the mask gives 1.42e-01 |
| 4 | 0.0010 on a task only position can solve — without position embeddings it sits at 3.4658 |
| 5 | 0.0108 after 400 steps overfitting 32 fixed sequences |
| 6 | `generate` survives a context longer than the block size |

It reads tensors in and tensors out, never the architecture, so any number of
layers, heads or norms passes as long as the model is a causal language model.
That is what let the teaching layer be replaced without touching the exam.

**What lands here is not the route.** The assignments live in their own
repositories. What lands here is the output: the trained model, the corpus with
its provenance and its deduplication, the full curves, unsorted samples, and the
write-up that has to hold up without the code on screen.

## Why the C tracks are not here

The libft and the projects that follow it are 42 subjects. Publishing a solution
to one is against the school's charter, and this repository is also the tree the
grader reads, so finishing one here would publish it by accident. The
`.gitignore` refuses them by name, and the list was built from the curriculum's
own `source` field rather than by eye. What stays publishable is what is built
*on top* of those subjects, which is the part worth showing.

## The Python socle — complete

Three modules, three questions, 26 exercises each small enough to be rebuilt
from a blank file.

| Module | Question | |
|---|---|---|
| [`py-01-basics`](ms-00-prepa/py-01-basics) | Can you get a correct answer out of input you do not control? | 9 of 9 |
| [`py-02-advanced`](ms-00-prepa/py-02-advanced) | Can you build a type that makes the wrong answer unrepresentable? | 9 of 9 |
| [`py-03-livrer`](ms-00-prepa/py-03-livrer) | Can someone else install it and run it without asking you how? | 8 of 8 |

It ends in a command, installed and on the PATH:

```console
$ releve resume mesures.txt
debit n=1 moy=880.00 p95=880.00 req/s
latence n=3 moy=17.67 p95=31.00 ms
```

The full write-up, exercise by exercise, with the decisions that were worth
naming, is in [`PYTHON.md`](PYTHON.md).

## Zero to Hero, and why it left

Three of Karpathy's lectures were rebuilt here by hand — a scalar autograd
engine, a bigram model built twice by two unrelated routes, and the Bengio MLP.
They ran, and their checks passed.

They are no longer in this repository, and the reason is one measurement: across
the fifteen sub-modules of the prep, the word `torch` appears twice and `numpy`
never, while the acceptance test imports `torch` on its first line. The units
build on a scalar engine the exam never loads. **The layer meant to prepare for
the deliverable was not teaching the object the deliverable is graded on**, so
it was replaced rather than finished, and the page stopped being organised
around it.

The work is not deleted — it is in this repository's history, and its checks
still run wherever it is kept. It is simply not the road any more, and a
showcase that keeps its abandoned road in the middle of the page is describing
the past.

## The one date I do not set

Every other item on this page opens when its prerequisites are met, which means
I choose when it starts. One does not, and it was added on 2026-09-19 for a
reason that is worth stating because it is measured rather than felt.

The source is [@levidiamode](https://x.com/levidiamode), who has posted a
`Day N/365 of GPU Programming` entry every day since 1 January 2026, starting
from no GPU, CUDA or computer architecture background and working around a job.
It is named because a claim you cannot check is not worth making, and every
figure below can be checked by reading the same public posts.

**What that record shows first is that the approach works.** Around day 71 they
entered a GPU MODE kernel competition on AMD hardware knowing none of MXFP4,
MoE or MLA, and finished roughly top fifteen of its first phase; by day 178
they placed **tenth** on a B200 QR factorisation, 1700 µs against 1200 for the
top three, and published the comparison of their kernel to the winners' the day
after. They also had a workshop paper accepted along the way. That is further
than this repository has got, and it took them about 250 hours.

I read 229 of the 258 entries and classified each day by whether it carried a
result measured against an outside reference. During a competition they had
entered, one day in four did. Outside one, one day in twenty. Over their last
sixty-five days, fully covered, after a newly opened competition was one they
said they would not have time for, none did — the reading and the tool-building
continued, the measuring stopped.

**The finding is about the structure, not about them.** Someone disciplined
enough to publish daily for a year, and strong enough to place top ten against
that field, still measures against an outside reference mainly when an outside
deadline asks for it. If that is what it takes there, it is certainly what it
takes here. The dated refusal followed by an effect is the closest thing to a
controlled comparison the record offers, and it is evidence about deadlines.

**So the rule is now:** the first GPU MODE competition that opens after the
inference deliverable is taken, whatever phase is running and whatever vendor's
hardware it targets. Its place in `ms-02-cpp-concurrence` is a floor, not a
date — that is simply the first phase entirely after the deliverable it waits
on. A competition that opens two phases later is taken two phases later.

Three things this costs and buys, all of them checkable:

- it costs two to four weeks pulled out of whatever phase is running, which is
  why the floor exists;
- entering opens thirty dollars a month of GPU time, which pays part of the
  compute line the later phases carry anyway;
- the vendor does not matter. The most instructive competition in that record
  ran on AMD hardware in HIP, and what came back from it — chiplet-aware cache
  scheduling, register pinning, why wave specialisation does not transfer from
  one vendor to the other — is reasoning, not an API.

The same reading changed one more thing here. **A measured gain is only a result
if the measurement survives a replay.** GPU MODE published the anatomy of one:
the leading kernel of a competition, at 11.191 µs, counted its own invocations
to detect the timing phase, then ran the fifteen problems in a single launch and
returned cached results for the rest, and the harness divided by fifteen.

This is not only something a cheater does. On day 172 the same record above
reports waking up to find that agents left running overnight had slipped such
tricks past the leaderboard checks, and the day went on finding and deleting the
bad submissions. The observation that came with it is the useful part: the more
exhaustively a search covers the legitimate moves, the more inventive it gets
about the illegitimate ones.

So the kernel deliverable now has to hold up under the same harness with the
call order changed and the inputs regenerated, and a gap between the two passes
is the result, not an incident.

## What the agents changed, and what they did not

Measured on 2026-09-20, because the answer moved twice inside one year and both
directions are published.

Read one way, the automation is not close.
[KernelBench-Verified](https://arxiv.org/abs/2607.16241) re-ran the benchmark
with the baseline repaired and put the best frontier model at a **0.88x**
geometric-mean speedup against PyTorch — slower, not faster. The 1.43x reported
before it came from two artefacts the paper names: TF32 left off, which
understates PyTorch on the hardware anyone actually runs, and models hardcoding
the test's values instead of computing them. Twenty-eight percent of the best
model's kernels also raised peak memory.

Read the other way, it is already here. At the
[MLSys 2026 FlashInfer kernel contest](https://mlsys26.flashinfer.ai/), closed
on 12 May, the [winning entry](https://github.com/Dogacel/auto-gpu-kernel) in
the **no-human-in-the-loop** category averaged a **34.93x** speedup over the
FlashInfer baselines for DeepSeek Sparse Attention on a B200. One limit on that
number, stated here rather than left for someone else to find: sparse attention
is a recent operator, so the baseline it beat is most likely a reference
implementation and not a tuned kernel. 34.93x over a reference is not 34.93x
over an expert, and nobody publishes the second number.

Both are true, and the reconciliation is the part worth keeping. The contest
winner wrote down why their harness won, and it was not the kernel:

> Other harnesses usually fail on setting a good verification pipeline, the
> agents either hack it over-time, or they get stuck at local-minimums.

The first trap they name is *believing noisy results to be improvements*. That
is the same failure as the 11.191 µs kernel above, and the same failure as the
overnight agents on day 172: three instances now, arriving from three
directions, of a measurement that did not defend itself.

**So the scarce thing moved one step back — from writing the kernel to
guaranteeing the measurement — and this plan follows it.** The hand-written
kernel deliverable does not change. The harness that won was built by someone
who already knew how to write the kernel, and the traps they list are not
visible from outside the craft. You do not get to validate what you cannot
produce.

What is added is a second deliverable, published, immediately after it: **the
harness itself**, run against an agent on the same bounded case the hand-written
kernel targets. It passes on two conditions, not one.

- The gap between my kernel and the agent's is published, whichever way it
  goes. The agent winning is a publishable result, and the more useful of the
  two.
- **At least one rejected submission is shown, with the reason it was
  rejected.** A pipeline that has never rejected anything is not a pipeline, it
  is an intention. That is the rule of the next section, applied to a
  deliverable instead of to a check.

The contest is also why the dated rule above now has a second family to watch:
its categories keep the agent alone and the agent seeded by a human on separate
boards, so both halves of this can be measured on the same hardware on the same
day.

## How this is verified

Every track ships checks that can fail, and each one was broken on purpose
before being trusted. A check that cannot fail is worse than no check.

You can run that claim rather than take it. [`tools/check.py`](tools/check.py)
asks three questions of this repository using nothing but this repository: does
the published Python parse, do the links between these pages resolve, and does
`.gitignore` agree with what git actually tracks. Each was proven able to fail
before being trusted — a deliberate syntax error, a link to a file that is not
there, and a `.gitignore` line naming `LICENSE` each turn it red. The third is
there because it had already gone wrong: a rule added on 2026-09-18 named two
files git was already tracking, which a rule does not untrack, so they stayed
published for five days while this repository believed them gone. A workflow
runs the three on every push.

Where a result is deterministic, the check is exact to the digit. Where it is
not, the check compares against a **range** set by the measured noise floor:
three runs of an MLP differing only in the minibatch draw gave 2.1595, 2.1870
and 2.1899, so the floor is 0.03, and demanding an exact value would fail a
correct model one time in two. That run and the one below were made in the
private corpus that produces this repository, on the Zero to Hero unit that
left it; the figures are reported here, not reproducible from this tree.

The same rule decides which sources are used at all. A source is taken when it
arrives with a grader that is not its own reader — a checker in the notebook, a
public test suite, a black-box acceptance test with published failure values. It
is the reason the six steps above are borrowed rather than written.

The advice the sources give is measured rather than repeated. Of the three
improvements Bengio et al. 2003 names, one pays (−0.048), one is ten times below
the noise floor, and the one the lecture calls most promising costs (+0.165).

## Layout

**One folder per phase, and inside it one folder per sub-module.** Each phase
carries a page listing every sub-module it declares, what grades it, and where
its work is — including the ones that are deliberately not here.

<!-- arbre: written by carte_phases.py from what git publishes. Do not edit by hand. -->
```
.github/                   the workflow that runs tools/check.py on every push
.gitignore                 what stays out, and why: 42 subjects above all
LICENSE                    MIT, and the credits owed are in Sources and licence above
PYTHON.md                  the Python socle, exercise by exercise
README.md                  this page: the roadmap, and where it stands
tools/                     the checks this repository can run on itself
ms-00-prepa/               the prep — Sept–Oct 2026
    README.md              its sub-modules in the order of the work, and their state
    py-01-basics/          correct answers out of input you do not control
    py-02-advanced/        types that make the wrong answer unrepresentable
    py-03-livrer/          the result, installable and on the PATH
    rte-01-puzzles/        Sasha Rush's twenty-one puzzles, solved and credited
    rte-route-l1/          the route's chapters, answers to Raschka's book
ms-01-inference/ … ms-07-stage-2/
    README.md              the same page, for a phase not yet opened
```
<!-- /arbre -->

The tree above and the phase pages are generated, from what git publishes and
from the curriculum, not written by hand. Three README drifts on this project
were all hand-copied figures going stale, and a page that reads its sources
cannot drift without them. This tree was the fourth: it listed three folders
under the prep while five were published, for five days, in the paragraph that
says a generated page cannot drift. A published folder with nothing said about
it now stops the build.

The 42 subjects are absent by policy, not by accident, and the route's
assignments are other people's work and stay in their own repositories. Phase 1
lands here when the trained model does.

## Sources and licence

The route: Sebastian Raschka, *Build a Large Language Model (From Scratch)*
([`rasbt/LLMs-from-scratch`](https://github.com/rasbt/LLMs-from-scratch)) ·
Stanford CS336, *Language Modeling from Scratch*
([`stanford-cs336`](https://github.com/stanford-cs336)) · Sasha Rush,
[Tensor Puzzles](https://github.com/srush/Tensor-Puzzles).

The road that was taken off: the Zero to Hero lectures, notebooks and datasets
are Andrej Karpathy's, MIT licensed —
[karpathy/nn-zero-to-hero](https://github.com/karpathy/nn-zero-to-hero),
[karpathy/micrograd](https://github.com/karpathy/micrograd),
[karpathy/makemore](https://github.com/karpathy/makemore). What was built from
them here was typed, not copied, and it remains in this repository's history.

Everything else is original work.
