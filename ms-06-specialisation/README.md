<!-- Généré par carte_phases.py. Ne pas éditer à la main. -->

# Phase 7 — Specialisation, first internship

`ms-06-specialisation` · 2028 onward · 9 sub-modules, 1 written · 8 exercises

**What it buys.** numerical precision, multi-GPU, operations and evaluation, then a page of deliverables that reads without explanation

Descriptions below translate the curriculum's own `competence` field, one sentence per sub-module. Each translation is stored with a fingerprint of the French it was made from, so a source that changes stops this page from being rebuilt rather than outrunning it. Rows are in the order the work goes, read from the curriculum's `apres` and `fil` fields; work done alongside the sequence comes last.

| Sub-module | Layer | What it covers | Where the work is |
|---|---|---|---|
| `t42-12-specialisation` | imposed | Choose the common core's specialisation between systems, graphics and kernel, and never web | 42 subject, not published |
| `c-13-minishell` | added | Write a shell that chains fork, exec, pipes and redirections without leaking a descriptor, and whose every error exits with the expected code | 42 subject, not published |
| `num-01-precision` | added | Say in five minutes whether a bf16 regression comes from the dynamic range, from the accumulation or from the order of operations, and show it on a reproduced case | planned, not written yet |
| `dist-01-multigpu` | added | Predict, before launching, whether a multi-GPU training run will be bound by memory, by bandwidth or by the bubble, then hold the prediction against the measurement | planned, not written yet |
| `qua-01-evaluation` | added | Require the quality measurement that goes with an optimisation before accepting it, and hold a long task alongside perplexity | planned, not written yet |
| `cpp-11-moderne` | added | Read what the compiler makes of a modern C++ program, moves, instantiation, constexpr, in the assembly and in the allocation count, write concurrent code against std::atomic's memory model, and spot a hidden allocation in a hot loop | not started · 8 exercises |
| `ops-01-exploitation` | added | Keep a service running for a month, cause its failures one at a time, and write a one-page post-mortem for each | planned, not written yet |
| `dist-02-cs336` | added | Hand in CS336's assignment 2 and make its public suite pass, on parallelism and the collectives | planned, not written yet |
| `pro-01-stage-1` | proof | Land and hold a first internship in a team that does compute infrastructure or inference | planned, not written yet |

## Reading

What each sub-module points at, straight from the curriculum. Links only: why a given one is there is written in French, next to the curriculum itself, and translating it would put the same sentence in two places waiting to disagree. A sub-module absent from this table has nothing declared yet.

| Sub-module | Points at |
|---|---|
| `num-01-precision` | [MIT 6.5940, TinyML and Efficient AI Computing, Song Han](https://hanlab.mit.edu/courses/2026-fall-65940) · [JINO-ROHIT/ml-systems-notes/quantization/notes.md](https://github.com/JINO-ROHIT/ml-systems-notes/blob/main/quantization/notes.md) · [a-hamdi/GPU](https://github.com/a-hamdi/GPU) |
| `dist-01-multigpu` | [MIT 6.5940, TinyML and Efficient AI Computing, Song Han](https://hanlab.mit.edu/courses/2026-fall-65940) · [JINO-ROHIT/ml-systems-notes/distributed_techniques](https://github.com/JINO-ROHIT/ml-systems-notes/tree/main/distributed_techniques) · [hkproj/torchfeather](https://github.com/hkproj/torchfeather) · [hkproj/pytorch-transformer-distributed](https://github.com/hkproj/pytorch-transformer-distributed) |
| `qua-01-evaluation` | [MIT 6.5940, TinyML and Efficient AI Computing, Song Han](https://hanlab.mit.edu/courses/2026-fall-65940) · [JINO-ROHIT/Embedding-Quantization](https://github.com/JINO-ROHIT/Embedding-Quantization) · [hkproj/quantization-notes](https://github.com/hkproj/quantization-notes) |
| `cpp-11-moderne` | [Meyers, Effective Modern C++](https://www.oreilly.com/library/view/effective-modern-c/9781491908419/) · [Compiler Explorer](https://godbolt.org/) · [cppreference, std::memory_order](https://en.cppreference.com/w/cpp/atomic/memory_order) · [Preshing, An Introduction to Lock-Free Programming](https://preshing.com/20120612/an-introduction-to-lock-free-programming/) · [Preshing, Acquire and Release Semantics](https://preshing.com/20120913/acquire-and-release-semantics/) · [Williams, C++ Concurrency in Action, 2e édition](https://www.manning.com/books/c-plus-plus-concurrency-in-action-second-edition) · [Carruth, CppCon 2015, Tuning C++: Benchmarks, and CPUs, and Compilers! Oh My!](https://www.youtube.com/watch?v=nXaxk27zwlk) · [Clang, -Rpass et l'assembleur avec -S](https://clang.llvm.org/docs/UsersManual.html#options-to-emit-optimization-reports) |
| `ops-01-exploitation` | [JINO-ROHIT/advanced_ml/12-ml-systems](https://github.com/JINO-ROHIT/advanced_ml/tree/main/12-ml-systems) · [JINO-ROHIT/fastapi_with_celery_redis](https://github.com/JINO-ROHIT/fastapi_with_celery_redis) |
| `dist-02-cs336` | [JINO-ROHIT/ml-systems-notes/distributed_techniques](https://github.com/JINO-ROHIT/ml-systems-notes/tree/main/distributed_techniques) |

---

← [ms-05-fin-tronc-commun](../ms-05-fin-tronc-commun) · [the roadmap](../README.md) · [ms-07-stage-2](../ms-07-stage-2) →
