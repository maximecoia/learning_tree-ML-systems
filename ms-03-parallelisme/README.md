<!-- Généré par carte_phases.py. Ne pas éditer à la main. -->

# Phase 4 — Parallelism, first kernel, entering vLLM

`ms-03-parallelisme` · weeks 21–34 · 21 sub-modules, 7 written · 24 exercises

**What it buys.** say before writing a kernel whether it will be compute- or memory-bound, and a PR in vLLM or SGLang on the scheduler or the cache, review taken up by a maintainer

**How it ends.** Not on a feeling, on one binary test: *L5 existe. Et on te décrit un kernel : tu estimes avant de coder s'il sera compute- ou memory-bound, et tu justifies par un ordre de grandeur.*

Descriptions below translate the curriculum's own `competence` field, one sentence per sub-module. Each translation is stored with a fingerprint of the French it was made from, so a source that changes stops this page from being rebuilt rather than outrunning it.

| Sub-module | Layer | What it covers | Where the work is |
|---|---|---|---|
| `t42-03-codexion` | imposed | — | 42 subject, not published |
| `t42-04-flyin` | imposed | — | 42 subject, not published |
| `t42-05-callmemaybe` | imposed | — | 42 subject, not published |
| `c-11-simd` | added | Split a computation across threads and measure the imbalance the split creates, write masked vector code and read lane utilisation, get the compiler to vectorise a loop and check that it did, and tie a computation's ceiling to the machine's bandwidth | not started · 4 exercises |
| `c-12-ordonnancement` | added | Write a batch task scheduler over threads created once, measure the imbalance between threads before correcting it, and run dependent batches without any starting before what it waits on | not started · 4 exercises |
| `par-05-philosophes-warps` | added | Tie the concurrent code you wrote, threads, mutexes, starvation, to a GPU's SIMT model, naming what carries over, what changes in nature, and what no longer exists | not started · 1 exercise |
| `cu-01-bases` | added | Write CUDA kernels, from elementary arithmetic to concurrent rendering, that run on the grader's host emulation as on a GPU: one thread per element with its bound, a shared-memory scan with its barriers, and a decomposition that guarantees ordering and atomicity | not started · 4 exercises |
| `cu-02-divergence` | added | Quantify what a warp divergence costs, all else being equal, by reading warp by warp which ones took both paths and applying the SIMT model | not started · 1 exercise |
| `tri-01-vecadd` | added | Write a Triton kernel that never steps outside its buffer, choose its block size and justify it by a count, and fuse several passes into one | not started · 5 exercises |
| `tri-02-softmax` | added | Write a row-wise softmax that never overflows, and check a kernel on four axes rather than one | not started · 5 exercises |
| `tri-03-matmul` | added | — | planned, not written yet |
| `tri-04-classement` | added | — | planned, not written yet |
| `tri-05-note` | added | — | planned, not written yet |
| `inf-07-pagedattention` | added | — | planned, not written yet |
| `inf-08-fragmentation` | added | — | planned, not written yet |
| `inf-09-compiler-vllm` | added | — | planned, not written yet |
| `inf-10-chemin-requete` | added | — | planned, not written yet |
| `inf-11-reproduire-bug` | added | — | planned, not written yet |
| `inf-12-premiere-pr` | added | — | planned, not written yet |
| `inf-13-choisir-issue` | added | — | planned, not written yet |
| `l5-01-contribution` | proof | — | planned, not written yet |

---

← [ms-02-cpp-concurrence](../ms-02-cpp-concurrence) · [the roadmap](../README.md) · [ms-04-cuda](../ms-04-cuda) →
