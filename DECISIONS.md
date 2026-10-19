# The decisions that shaped the plan

The [roadmap](README.md) says what the plan is. This page says why it is that
plan and not another: each decision below changed the roadmap, and each one is
kept with the measurement that forced it. A decision without its evidence is an
opinion, and this repository tries not to publish those.

1. [Borrowed graders, not written lessons](#borrowed-graders-not-written-lessons)
2. [Zero to Hero, and why it left](#zero-to-hero-and-why-it-left)
3. [CS336, and why it left the prep](#cs336-and-why-it-left-the-prep)
4. [The C engine, and why it left the prep](#the-c-engine-and-why-it-left-the-prep)
5. [The one date I do not set](#the-one-date-i-do-not-set)
6. [What the agents changed, and what they did not](#what-the-agents-changed-and-what-they-did-not)
7. [How a check is calibrated](#how-a-check-is-calibrated)
8. [Why a number follows the order](#why-a-number-follows-the-order)
9. [The school first, the rest grafted onto it](#the-school-first-the-rest-grafted-onto-it)
10. [Why the roadmap has no dates](#why-the-roadmap-has-no-dates)

Each section is dated. Where a plan of that day changed later, the section
says so.

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
  phase was then due to close. The prep closed earlier, on 2 October.
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

## The C engine, and why it left the prep

`c-06-moteur`, an inference engine written in C that loads a model, generates,
measures its throughput and places it on a roofline, was part of the prep's
promise. Its row said it was out of the window because it needed the weights
L1 produces. It moved to `ms-01-inference` on 2026-09-30, on three findings.
On 2026-10-12 it moved again, after the common core, for the reason given at
the end of this section.

- **The stated dependency was false.** Its grader never loads L1: it builds its
  own toy model from a seed, eight dimensions and two heads, and compares the
  engine against a Python reference of the same arithmetic. Its weight format
  could not load L1 anyway: one layer, RMSNorm, ReLU and learned positions,
  where the GPT of the route has several blocks, LayerNorm and GELU.
- **Its slot did not exist.** It was ordered after L1, and L1 was then due on
  31 October, the day the prep was due to close.
- **Its lessons are the ones `ms-01-inference` teaches.** Its throughput step asks for a
  timing that ignores warm-up, which is the competence of `mes-01-chronometre`,
  now its prerequisite. Its KV cache is what `inf-04-cache-kv` measures, and
  its roofline is how `inf-02-prefill-decode` reads prefill and decode.

It was placed after the measurement modules and before the served-model ones,
so the engine would be written with a stopwatch in hand, and the cache and the
regimes then measured on a server by someone who had built both. Nothing
depended on it, so no other sub-module moved. What it cost was time in a phase
that already held the school's graded C: seven exercises, budgeted at about
thirty hours, and not measured.

That cost is what moved it a second time. Since 2026-10-12 it waits for the
end of the common core, first in the order in which deferred work comes back.
It grafts onto no school project, and its delay can be caught up later. See
[below](#the-school-first-the-rest-grafted-onto-it).

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

**So the rule was:** the first GPU MODE competition that opens after the
inference deliverable is taken, whatever phase is running and whatever vendor's
hardware it targets. Its place in the roadmap is a floor, not a date. It costs
two to four weeks pulled out of the running phase; entering opens thirty
dollars a month of GPU time; and the vendor does not matter, since what came
back from the most instructive competition in that record, on AMD hardware in
HIP, is reasoning and not an API.

**What changed on 2026-10-12.** The rule still holds, but no longer during the
common core. With about five and a half hours a week outside school, no GPU
work grafts onto a school project, so the competition moved to
`ms-06-apres-tronc` with the rest of it. Its place there is still a floor and
not a date: it is taken on remote GPUs as soon as the hours come back. The
measurement above is also what the grafts of the [school-first
rule](#the-school-first-the-rest-grafted-onto-it) rest on.

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

## Why a number follows the order

Until 2026-10-08 an identifier never changed once given. It lives in the
graders, in the private docs, in this repository and in the translations of
these pages, so each move kept its old number. The sum was visible here: the
page of `ms-01-inference` listed `inf-15-llama` between `inf-02` and `inf-03`, and
`c-02-moteur` after `c-06-pushswap`; the maths read `maths-01`, `mth-03`,
`mth-04`; the contribution, L5, fell a phase before the kernel, L4. Read in
the order of its numbers, the roadmap described a sequence the work does not
follow.

The rule is now the reverse. **Within a family, a number grows with the place
of the sub-module in the curriculum, phase after phase, from 01 and without a
gap**, and a sub-module that moves is renamed. `cpp-` starts at 00, like the
42 subjects it rebuilds. On 2026-10-08, 34 sub-modules were renamed. The
contribution became L4 and the kernel that beats the reference became L5, so
the deliverables now fall in the order of their numbers. The GPU MODE
competition left the Triton family for its own, `gpu-01`, because it opens on
its own dates whatever the vendor, and is not a Triton tutorial.

The check reads the curriculum and refuses a number that goes back, a gap, a
family that starts elsewhere than 01, and deliverables out of order. It found
23 such faults in the curriculum as it stood, none after, and it catches each
of the five breakages made on purpose to test it. Git history follows the
renamed folders; a link to an old path pasted somewhere else does not, so the
table below is the bridge.

| Before | After |
|---|---|
| `c-03-libft-norme` | `c-02-libft-norme` |
| `c-04-printf` | `c-03-printf` |
| `c-05-gnl` | `c-04-gnl` |
| `c-06-pushswap` | `c-05-pushswap` |
| `c-02-moteur` | `c-06-moteur` |
| `inf-15-llama` | `inf-03-llama` |
| `inf-03-cache-kv` | `inf-04-cache-kv` |
| `inf-04-quantifier` | `inf-05-quantifier` |
| `inf-05-harnais` | `inf-06-harnais` |
| `inf-06-saturation` | `inf-07-saturation` |
| `inf-14-speculatif` | `inf-08-speculatif` |
| `inf-07-pagedattention` | `inf-09-pagedattention` |
| `inf-08-fragmentation` | `inf-10-fragmentation` |
| `inf-09-compiler-vllm` | `inf-11-compiler-vllm` |
| `inf-10-chemin-requete` | `inf-12-chemin-requete` |
| `inf-11-reproduire-bug` | `inf-13-reproduire-bug` |
| `inf-12-premiere-pr` | `inf-14-premiere-pr` |
| `inf-13-choisir-issue` | `inf-15-choisir-issue` |
| `t42-06-pacman` | `t42-03-pacman` |
| `t42-08-inception` | `t42-04-inception` |
| `t42-07-rag-machine` | `t42-06-rag-machine` |
| `t42-03-codexion` | `t42-07-codexion` |
| `t42-04-flyin` | `t42-08-flyin` |
| `t42-10-agent-smith` | `t42-09-agent-smith` |
| `t42-09-answer-protocol` | `t42-10-answer-protocol` |
| `cu-11-assembleur` | `cu-10-assembleur` |
| `cu-10-battre` | `l5-01-battre` |
| `tri-04-classement` | `gpu-01-classement` |
| `tri-05-note` | `tri-04-note` |
| `maths-01-algebre` | `mth-01-algebre` |
| `mth-03-probas` | `mth-02-probas` |
| `mth-04-statistiques` | `mth-03-statistiques` |
| `mth-02-derivees` | `mth-04-derivees` |
| `l5-01-contribution` | `l4-01-contribution` |

## The school first, the rest grafted onto it

On 2026-10-12 the 27 subjects of the 2026 common core were read for the first
time, and the roadmap had been written without them. Four projects it listed in
C are in Python. One it called a quick formality, Agent Smith, is a coding agent
held to SWE-bench Verified, about a hundred hours alone. The core as a whole
reads at about 1,000 hours, against the 750 the plan assumed. And three of the
school's projects turned out to sit inside this field: constrained decoding on
the logits of a small model, retrieval over the vLLM repository, and a
philosophers problem with FIFO and EDF schedulers.

The added layer, meanwhile, had been planned on twenty hours a week outside
school, and the hours actually left are about five and a half for now. At that
rate the plan's own rule, that a phase counts as done when both layers are,
could not be met by any phase.

So the rule is now the other way round. **During the common core, an added
module enters only when it is cheaper done together with a school project, or
when its delay could not be caught up later.** The first case is a graft: the
measurement a school subject already asks for in its README, done properly, or
an extension built on a validated project. The second case is two things only:
closing L2, and the contribution, whose review takes weeks whatever the hours.
Everything else, the C engine, C++, CS149, the execution profile, Triton, CUDA
and the kernel, waits for the end of the core, in a fixed order. The one
measurement behind the grafts is a year of someone else's practice journal: on
days inside a competition with an external deadline, a quarter carried a
measured result; on the other days, one in twenty.

The other change is the way in. A count on 2026-10-07 found 209 European
openings in GPU infrastructure and SRE and 115 in ML platform work, against 31
for the job this plan aims at, and the first two filter far less on degrees.
The original plan called platform work a dead end; that line is withdrawn. The
inference server of L2 is now ported to Kubernetes after the school's Inception
project, with its metrics in Prometheus and its curve replayed under load. The
first step after the core is an internship at a serving or infrastructure
employer. Since 2026-10-19 the roadmap has two ends: the first job, if the
internship turns into one, and otherwise two years of work-study toward 42's
level 7 title. The school's specialisation, which leads to the level that
work-study requires, now comes right after the internship instead of waiting
behind the deferred modules.

The contribution now opens with the school's retrieval project, whose index of
the vLLM repository is the map a first contributor needs, and its target widens
to the whole vLLM organisation, Kubernetes deployment included, or llm-d. The
execution profile moved after the contribution, so the rule above renamed them:
the contribution is L3, the profile L4, the kernel still L5.

| Before | After |
|---|---|
| `ms-02-cpp-concurrence` | `ms-02-infrastructure` |
| `ms-03-parallelisme` | `ms-03-contribution` |
| `ms-04-cuda` | `ms-04-agents-reseau` |
| `ms-06-specialisation` | `ms-06-apres-tronc` |
| `ms-07-stage-2` | `ms-07-alternance` |
| `l4-01-contribution` | `l3-01-contribution` |
| `l3-01-profil` | `l4-01-profil` |
| `c-11-simd` | `c-09-simd` |
| `c-12-ordonnancement` | `c-10-ordonnancement` |
| `c-13-minishell` | `c-11-minishell` |
| `c-09-philosophers`, off the path | `c-12-philosophers` |
| `c-10-famine`, off the path | `c-13-famine` |
| `pro-02-stage-2` | `pro-02-alternance` |

What could be wrong: the graft rule rests on one person's journal; and the
contribution has now changed its number twice in four days, so a note written
before 2026-10-12 calls it L4, and one written before 2026-10-08 calls it L5.
The phase windows still assumed 750 hours of school that day; the next section
says why they are gone.

## Why the roadmap has no dates

Until 2026-10-19 each phase of the common core carried a window in weeks, from
weeks 1–8 to weeks 47–57. On that day they left the roadmap, for two reasons.

**They contradicted the plan.** Counted from the first day of school,
9 November 2026, week 57 ends on 12 December 2027. The plan's own horizon,
written on 2026-10-12 from the 2026 subjects, puts the end of the core in
September or October 2027. Two dates for one event, two months apart. Recounting
the windows was tried first: 47 weeks, shared in proportion to the 895 hours
the curriculum budgets for the school's projects. That made a tidier estimate,
and still an estimate.

**They measured nothing.** The roadmap has two layers, and neither moves by
the week. The added layer moves at my pace: the prep closed four weeks inside
its window, and the 40 measurement and inference exercises of `ms-01-inference`
were done before week 1. The imposed layer moves at the school's: what that
phase still lacks, `get_next_line` and `push_swap`, waits for the school to
grade it. A week of the calendar is the pace of neither.

So a phase now says what paces it: the school milestones it covers, or « after
the common core ». The program that writes these pages translates that from
the curriculum and refuses a [roadmap table](README.md#the-roadmap) that says
otherwise. The only dates on this site are facts: when a phase closed, and when
the school starts. The progress chart shows where the work stands, read from
the graders like every other number here.

What could be wrong: a reader looking for when I can start an internship finds
no date here. The plan still keeps an estimate for the end of the core, because
money and applications depend on it. It is simply not drawn as a schedule, and
a recruiter gets it by asking.
