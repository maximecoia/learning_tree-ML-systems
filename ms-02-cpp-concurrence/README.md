<!-- Généré par carte_phases.py. Ne pas éditer à la main. -->

# Phase 3 — C++ and concurrency

`ms-02-cpp-concurrence` · weeks 9–20 · 18 sub-modules, 18 written · 48 exercises

**What it buys.** concurrent code whose freedom from starvation is shown by measurement, and an unknown execution timeline read in ten minutes

**How it ends.** Not on a feeling, on one binary test: *Tu lis une frise Nsight inconnue et tu nommes le trou en dix minutes.*

Descriptions below translate the curriculum's own `competence` field, one sentence per sub-module. Each translation is stored with a fingerprint of the French it was made from, so a source that changes stops this page from being rebuilt rather than outrunning it.

| Sub-module | Layer | What it covers | Where the work is |
|---|---|---|---|
| `t42-01-piscine-python` | imposed | Clear the curriculum's Python pool as fast as possible, the content being already known: the exact output, the exact error, the exact docstring, on the patterns the grader checks | 42 subject, not published · 3 exercises |
| `t42-02-amazeing` | imposed | Ship a project scoped to its subject and nothing more: a configuration read and refused by naming the cause, a maze perfect or not with coherent walls, a shortest path, a seed that reproduces | 42 subject, not published · 3 exercises |
| `sh-01-b2br` | imposed | Administer a hardened machine, from encrypted partitioning to password policy, and be able to defend every choice: the subject's configuration files handed in and read, and the monitoring script run against command doubles | 42 subject, not published · 5 exercises |
| `cpp-00-classes` | added | Write a class with what it hides and what it shows, hold shared state in static members, and read and write through the language's streams up to an interactive program that never falls over | 42 subject, not published · 3 exercises |
| `cpp-01-allocation` | added | Choose between the stack and the heap and say so in the code, tell a reference from a pointer by what each one promises, and aim at a method through a pointer to member | 42 subject, not published · 3 exercises |
| `cpp-02-canonique` | added | Lay down the four members the language calls without you writing them, overload operators without surprising the caller, and represent a fixed-point number with no float in memory | 42 subject, not published · 3 exercises |
| `cpp-03-heritage` | added | Derive a class, know the order in which construction and destruction run, and make a diamond inheritance rest on a single base | 42 subject, not published · 3 exercises |
| `cpp-04-polymorphisme` | added | Use virtual functions so the object decides and not the pointer, make destructors virtual, write an abstract class and interfaces, and deep-copy without ever sharing or leaking | 42 subject, not published · 3 exercises |
| `cpp-05-vector-asm` | added | Read in the compiler's assembly what a std::vector reallocation really costs, allocation, copy and free, and say in advance when it happens and how to avoid it | not started · 2 exercises |
| `c-07-threadpool` | added | Write a queue guarded by a mutex and condition variables, threads that consume it, and a shutdown that forgets no task, proving it under ThreadSanitizer and under load | not started · 3 exercises |
| `c-08-contention` | added | Measure what a lock costs as the thread count rises, first on a counter that is correct, then on three strategies whose curves say which one shares what | not started · 2 exercises |
| `c-09-philosophers` | added | Write a concurrent program free of deadlock and starvation, where a death is announced within ten milliseconds and no line comes out after it, and prove it from the log and under ThreadSanitizer | 42 subject, not published · 3 exercises |
| `c-10-famine` | added | Demonstrate the absence of starvation from the measured distribution of intervals between meals, not from an argument about the strategy | not started · 2 exercises |
| `par-01-regimes` | added | Name a computation's three regimes, memory-bound, compute-bound or overhead-bound, and give one measured example of each against the machine's ceilings | not started · 1 exercise |
| `par-02-predire` | added | Predict each layer's regime from its flops and its bytes before any measurement, then hold the prediction against the measurements, naming every disagreement and every slowdown | not started · 1 exercise |
| `par-03-nsight` | added | Read a full generation's execution timeline in the profilers' format, extract from it the quantities the eye cannot see, GPU occupancy, launch latency, median kernel size, and draw it so the eye sees the rest | not started · 1 exercise |
| `par-04-trou` | added | Find in a timeline the periods where the GPU does nothing, with their bounds, and name each one's cause from what occupies it: a copy, a synchronisation, host-side compute, or nothing, which means outside the trace | not started · 1 exercise |
| `l3-01-profil` | proof | Publish an inference server's execution profile, scope read from the timeline, annotated timeline, prediction held against it, a diagnosis naming a physical limit by a written rule, and a comparison with your partner, then read an unknown timeline and name its gap in one call | not started · 6 exercises |

---

← [ms-01-inference](../ms-01-inference) · [the roadmap](../README.md) · [ms-03-parallelisme](../ms-03-parallelisme) →
