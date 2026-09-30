# The decisions that shaped the plan

The [roadmap](README.md) says what the plan is. This page says why it is that
plan and not another: each decision below changed the roadmap, and each one is
kept with the measurement that forced it. A decision without its evidence is an
opinion, and this repository tries not to publish those.

1. [Borrowed graders, not written lessons](#borrowed-graders-not-written-lessons)
2. [Zero to Hero, and why it left](#zero-to-hero-and-why-it-left)
3. [CS336, and why it left the prep](#cs336-and-why-it-left-the-prep)
4. [The C engine, and why it moved to phase 2](#the-c-engine-and-why-it-moved-to-phase-2)
5. [The one date I do not set](#the-one-date-i-do-not-set)
6. [What the agents changed, and what they did not](#what-the-agents-changed-and-what-they-did-not)
7. [How a check is calibrated](#how-a-check-is-calibrated)

## Borrowed graders, not written lessons

The plan used to carry its own course, and the count that ended it is short:
over eleven days it produced 141,783 lines of written lessons and 2,038 lines of
machine learning code, while zero of the thirty-four exercises that already
existed had been handed in. A lesson written by hand and then marked by its own
author has no external referent.

So every step of the route to the trained GPT is now handed to something that
already exists and can grade it: the checker inside the Tensor Puzzles
notebook, and a black-box acceptance test whose failure values are published.
The public `pytest` suite of CS336 was a third, until it left the prep for the
reasons [below](#cs336-and-why-it-left-the-prep).

Steps 2 to 5, the chapters of Raschka's book, are the exception, and it is
stated rather than left to be found. The book ships almost no assertions: its
own chapter 2 test ends on an expression that is evaluated and thrown away, so
it cannot fail. Their tests are therefore written here, against what each
chapter states in prose, and every suite has been broken on purpose to prove it
can fail. What keeps them honest is not their author but the acceptance test,
which none of them wrote and all of them lead to.

## Zero to Hero, and why it left

Three of Karpathy's lectures were rebuilt here by hand: a scalar autograd
engine, a bigram model built twice by two unrelated routes, and the Bengio MLP.
They ran, and their checks passed.

They are no longer in this repository, and the reason is one measurement:
across the fifteen sub-modules of the prep, the word `torch` appeared twice and
`numpy` never, while the acceptance test imports `torch` on its first line. The
units built on a scalar engine the exam never loads. **The layer meant to
prepare for the deliverable was not teaching the object the deliverable is
graded on**, so it was replaced rather than finished.

The work is not deleted. It is in this repository's history, and its checks
still run wherever it is kept. It is simply not the road any more.

## CS336, and why it left the prep

The first assignment of Stanford's CS336 was the route's last step: fifteen of
its twenty-one adapters, the ones that do not depend on the architecture,
graded by its public suite. It left the prep on 2026-09-30, on four
measurements.

- **It graded what was already graded.** The curriculum said so itself: the
  fifteen adapters cover exactly the material of Raschka's chapters 2 to 5.
  Those chapters have their own tests, and the seven gates of the acceptance
  test grade the same model a third time.
- **Two thirds of its tests were a tokenizer the plan had dropped.** The byte
  pair encoder carried 28 of its 42 tests, and the acceptance test takes a
  character vocabulary.
- **Its window did not exist.** Once the trained model became the only goal of
  the prep, CS336 was moved out of the window until 31 October, the day the
  phase closes.
- **Nothing depended on it.** No sub-module listed it as a prerequisite, and
  the second assignment, the systems half, ships the course's own
  implementation of the first.

What it took with it, and this is its real cost: it was the only grader on the
route written by someone else about the model itself, and it was the only one
that asked for AdamW, a learning-rate schedule, gradient clipping and a
resumable checkpoint written by hand. None of those is graded here any more.
The acceptance test trains with `torch.optim.AdamW`, and nothing in the target
asks for it to be rewritten.

**What it kept is the part the target uses.** The six adapters the route left
aside are the ones that depend on the architecture, and three of them are what
separates a Llama from the GPT-2 of the route: RMSNorm instead of LayerNorm,
SwiGLU instead of a GELU feed-forward, rotary positions instead of learned
ones. Most open models an inference engine serves are built that way. Those
three tests now grade a sub-module of `ms-01-inference`, placed before the KV
cache, because the keys that land in the cache are already rotated.

## The C engine, and why it moved to phase 2

`c-02-moteur`, an inference engine written in C that loads a model, generates,
measures its throughput and places it on a roofline, was part of the prep's
promise. Its row said it was out of the window because it needed the weights
L1 produces. It moved to `ms-01-inference` on 2026-09-30, on three findings.

- **The stated dependency was false.** Its grader never loads L1: it builds its
  own toy model from a seed, eight dimensions and two heads, and compares the
  engine against a Python reference of the same arithmetic. Its weight format
  could not load L1 anyway: one layer, RMSNorm, ReLU and learned positions,
  where the GPT of the route has several blocks, LayerNorm and GELU.
- **Its slot did not exist.** It was ordered after L1, and L1 closes on
  31 October, the day the prep closes.
- **Its lessons are the ones phase 2 teaches.** Its throughput step asks for a
  timing that ignores warm-up, which is the competence of `mes-01-chronometre`,
  now its prerequisite. Its KV cache is what `inf-03-cache-kv` measures, and
  its roofline is how `inf-02-prefill-decode` reads prefill and decode.

It now sits after the measurement modules and before the served-model ones, so
the engine is written with a stopwatch in hand, and the cache and the regimes
are then measured on a server by someone who has built both. Nothing depended
on it, so no other sub-module moved. What it costs is time in a phase that
already holds the school's graded C: seven exercises, budgeted at about thirty
hours, and not measured.

## The one date I do not set

Every other item of the roadmap opens when its prerequisites are met, which
means I choose when it starts. One does not, and it was added on 2026-09-19 for
a reason that is measured rather than felt.

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
after. That took them about 250 hours.

I read 229 of the 258 entries and classified each day by whether it carried a
result measured against an outside reference. During a competition they had
entered, one day in four did. Outside one, one day in twenty. Over their last
sixty-five days, after a newly opened competition was one they said they would
not have time for, none did: the reading and the tool-building continued, the
measuring stopped.

**The finding is about the structure, not about them.** Someone disciplined
enough to publish daily for a year, and strong enough to place top ten against
that field, still measures against an outside reference mainly when an outside
deadline asks for it. If that is what it takes there, it is certainly what it
takes here.

**So the rule is:** the first GPU MODE competition that opens after the
inference deliverable is taken, whatever phase is running and whatever vendor's
hardware it targets. Its place in `ms-02-cpp-concurrence` is a floor, not a
date. It costs two to four weeks pulled out of the running phase; entering
opens thirty dollars a month of GPU time; and the vendor does not matter, since
what came back from the most instructive competition in that record, on AMD
hardware in HIP, is reasoning and not an API.

The same reading changed one more thing. **A measured gain is only a result if
the measurement survives a replay.** GPU MODE published the anatomy of one: the
leading kernel of a competition, at 11.191 µs, counted its own invocations to
detect the timing phase, then ran the fifteen problems in a single launch and
returned cached results for the rest, and the harness divided by fifteen. On
day 172, the same record reports agents left running overnight that had slipped
such tricks past the leaderboard checks. So the kernel deliverable has to hold
up under the same harness with the call order changed and the inputs
regenerated, and a gap between the two passes is the result, not an incident.

## What the agents changed, and what they did not

Measured on 2026-09-20, because the answer moved twice inside one year and both
directions are published.

Read one way, the automation is not close.
[KernelBench-Verified](https://arxiv.org/abs/2607.16241) re-ran the benchmark
with the baseline repaired and put the best frontier model at a **0.88x**
geometric-mean speedup against PyTorch: slower, not faster. The 1.43x reported
before it came from two artefacts the paper names, TF32 left off and models
hardcoding the test's values.

Read the other way, it is already here. At the
[MLSys 2026 FlashInfer kernel contest](https://mlsys26.flashinfer.ai/), the
[winning entry](https://github.com/Dogacel/auto-gpu-kernel) in the
**no-human-in-the-loop** category averaged a **34.93x** speedup over the
FlashInfer baselines for DeepSeek Sparse Attention on a B200. Sparse attention
is a recent operator, so the baseline it beat is most likely a reference
implementation and not a tuned kernel: 34.93x over a reference is not 34.93x
over an expert.

The winner wrote down why their harness won, and it was not the kernel:

> Other harnesses usually fail on setting a good verification pipeline, the
> agents either hack it over-time, or they get stuck at local-minimums.

**So the scarce thing moved one step back, from writing the kernel to
guaranteeing the measurement, and the plan follows it.** The hand-written
kernel deliverable does not change: you do not get to validate what you cannot
produce. What is added right after it is **the harness itself**, run against an
agent on the same bounded case. It passes on two conditions: the gap between my
kernel and the agent's is published whichever way it goes, and **at least one
rejected submission is shown, with the reason it was rejected.** A pipeline
that has never rejected anything is not a pipeline, it is an intention.

## How a check is calibrated

Where a result is deterministic, a check is exact to the digit. Where it is
not, it compares against a **range** set by the measured noise floor: three runs
of an MLP differing only in the minibatch draw gave 2.1595, 2.1870 and 2.1899,
so the floor is 0.03, and demanding an exact value would fail a correct model
one time in two.

The same measuring applies to advice. Of the three improvements Bengio et al.
2003 names, one pays (−0.048), one is ten times below the noise floor, and the
one the lecture calls most promising costs (+0.165). Both runs were made in the
private corpus that produces this repository, on the Zero to Hero unit that
left it; the figures are reported here, not reproducible from this tree.
