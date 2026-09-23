<!-- Généré par carte_phases.py. Ne pas éditer à la main. -->

# Phase 4 — Parallelism, first kernel, entering vLLM

`ms-03-parallelisme` · weeks 21–34 · 20 sub-modules, 7 written · 24 exercises

**What it buys.** say before writing a kernel whether it will be compute- or memory-bound, and a PR in vLLM or SGLang on the scheduler or the cache, review taken up by a maintainer

**How it ends.** Not on a feeling, on one binary test: *L5 existe. Et on te décrit un kernel : tu estimes avant de coder s'il sera compute- ou memory-bound, et tu justifies par un ordre de grandeur.*

Descriptions below translate the curriculum's own `competence` field, one sentence per sub-module. Each translation is stored with a fingerprint of the French it was made from, so a source that changes stops this page from being rebuilt rather than outrunning it. Rows are in the order the work goes, read from the curriculum's `apres` and `fil` fields; work done alongside the sequence comes last.

| Sub-module | Layer | What it covers | Where the work is |
|---|---|---|---|
| `t42-03-codexion` | imposed | Validate `codexion` at the perimeter of its subject, adding nothing beyond what the defence requires | 42 subject, not published |
| `t42-04-flyin` | imposed | Validate `fly-in` at the perimeter of its subject, the toll's mark being the only objective | 42 subject, not published |
| `t42-05-callmemaybe` | imposed | Validate `call me maybe` and leave: the subject is a strict toll, and no hour goes into it beyond the validation | 42 subject, not published |
| `c-11-simd` | added | Split a computation across threads and measure the imbalance the split creates, write masked vector code and read lane utilisation, get the compiler to vectorise a loop and check that it did, and tie a computation's ceiling to the machine's bandwidth | not started · 4 exercises |
| `c-12-ordonnancement` | added | Write a batch task scheduler over threads created once, measure the imbalance between threads before correcting it, and run dependent batches without any starting before what it waits on | not started · 4 exercises |
| `par-05-philosophes-warps` | added | Tie the concurrent code you wrote, threads, mutexes, starvation, to a GPU's SIMT model, naming what carries over, what changes in nature, and what no longer exists | not started · 1 exercise |
| `cu-01-bases` | added | Write CUDA kernels, from elementary arithmetic to concurrent rendering, that run on the grader's host emulation as on a GPU: one thread per element with its bound, a shared-memory scan with its barriers, and a decomposition that guarantees ordering and atomicity | not started · 4 exercises |
| `cu-02-divergence` | added | Quantify what a warp divergence costs, all else being equal, by reading warp by warp which ones took both paths and applying the SIMT model | not started · 1 exercise |
| `tri-01-vecadd` | added | Write a Triton kernel that never steps outside its buffer, choose its block size and justify it by a count, and fuse several passes into one | not started · 5 exercises |
| `tri-02-softmax` | added | Write a row-wise softmax that never overflows, and check a kernel on four axes rather than one | not started · 5 exercises |
| `tri-03-matmul` | added | Write a tiled Triton matmul whose tile size is justified by a count, and compare it with the reference on a bounded case | planned, not written yet |
| `tri-05-note` | added | Write the note that says what was measured, under which protocol, and what the measurement does not allow you to conclude | planned, not written yet |
| `inf-07-pagedattention` | added | Explain the paging of the KV cache as PagedAttention defines it, and say block by block which waste it removes | planned, not written yet |
| `inf-08-fragmentation` | added | Put a percentage on the memory lost to fragmentation when the KV cache is not paged, over a trace of requests whose lengths vary | planned, not written yet |
| `inf-09-compiler-vllm` | added | Build vLLM from source and run its test suite, until you know which change forces which rebuild | planned, not written yet |
| `inf-10-chemin-requete` | added | Trace a request through vLLM, from the API entry point to the token returned, naming the components it crosses and what each one decides | planned, not written yet |
| `inf-11-reproduire-bug` | added | Reproduce an open bug of the repository from its report, and cut the reproduction down to the smallest case that still triggers it | planned, not written yet |
| `inf-12-premiere-pr` | added | Open a first pull request on vLLM and carry its review through to a merge, or to a refusal whose reason you understand | planned, not written yet |
| `inf-13-choisir-issue` | added | Pick an issue whose stake is the scheduler or the cache rather than the kernel, and justify that choice by the gain expected and by what is within reach | planned, not written yet |
| `l5-01-contribution` | proof | Open a pull request in an upstream inference engine, engage its review, and publish the measured gain it brings | planned, not written yet |

## Reading

What each sub-module points at, straight from the curriculum. Links only: why a given one is there is written in French, next to the curriculum itself, and translating it would put the same sentence in two places waiting to disagree. A sub-module absent from this table has nothing declared yet, and a resource that lives in a repository you cannot open is left out rather than linked to a 404.

| Sub-module | Points at |
|---|---|
| `c-11-simd` | [stanford-cs149/asst1](https://github.com/stanford-cs149/asst1) · assignment<br>[CS149 Stanford, cours 2, A Modern Multi-Core Processor](https://gfxcourses.stanford.edu/cs149/fall23/lecture/multicore/) · course<br>[Clang, Auto-Vectorization](https://llvm.org/docs/Vectorizers.html) · docs<br>[stanford-cs149/asst1/prog2_vecintrin/CS149intrin.h](https://github.com/stanford-cs149/asst1/blob/master/prog2_vecintrin/CS149intrin.h) · repo<br>[McCalpin, STREAM benchmark](https://www.cs.virginia.edu/stream/) · article<br>[Williams, Waterman, Patterson, Roofline: An Insightful Visual Performance Model, 2009](https://doi.org/10.1145/1498765.1498785) · paper<br>[MIT 6.S894 Accelerated Computing, les labs](https://accelerated-computing.academy/fall25/labs/) · assignment<br>[JINO-ROHIT/c-gym/neon_simd](https://github.com/JINO-ROHIT/c-gym/tree/main/neon_simd) · repo |
| `c-12-ordonnancement` | [stanford-cs149/asst2](https://github.com/stanford-cs149/asst2) · assignment<br>[CS149 Stanford, cours 4, Parallel Programming Basics](https://gfxcourses.stanford.edu/cs149/fall23/lecture/progbasics/) · course<br>[CS149 Stanford, cours 5, Performance Optimization I, Work Distribution and Scheduling](https://gfxcourses.stanford.edu/cs149/fall23/lecture/perfopt1/) · course<br>[pthread_cond_wait, manuel](https://man7.org/linux/man-pages/man3/pthread_cond_wait.3p.html) · docs<br>[Blumofe et Leiserson, Scheduling Multithreaded Computations by Work Stealing, 1999](https://doi.org/10.1145/324133.324234) · paper<br>[ThreadSanitizer, manuel Clang](https://clang.llvm.org/docs/ThreadSanitizer.html) · docs |
| `par-05-philosophes-warps` | [NVIDIA, CUDA C++ Programming Guide, SIMT Architecture](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#simt-architecture) · docs<br>[Lindholm et al., NVIDIA Tesla: A Unified Graphics and Computing Architecture, 2008](https://doi.org/10.1109/MM.2008.31) · paper<br>[CS149 Stanford, cours 2 et 3, modèles d'exécution parallèle](https://gfxcourses.stanford.edu/cs149/fall23/lecture/) · course<br>[Ancien sujet 42, philosophers](https://projects.intra.42.fr/projects/philosophers) · assignment<br>[Harris, Optimizing Parallel Reduction in CUDA](https://developer.download.nvidia.com/assets/cuda/files/reduction.pdf) · article |
| `cu-01-bases` | [stanford-cs149/asst3](https://github.com/stanford-cs149/asst3) · assignment<br>[CS149 Stanford, cours 7, GPU Architecture and CUDA Programming](https://gfxcourses.stanford.edu/cs149/fall23/lecture/gpucuda/) · course<br>[NVIDIA, CUDA C++ Programming Guide](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html) · docs<br>[Harris, Sengupta, Owens, Parallel Prefix Sum (Scan) with CUDA, GPU Gems 3](https://developer.nvidia.com/gpugems/gpugems3/part-vi-gpu-computing/chapter-39-parallel-prefix-sum-scan-cuda) · article<br>[Blelloch, Prefix Sums and Their Applications, 1990](https://www.cs.cmu.edu/~guyb/papers/Ble93.pdf) · paper<br>[MIT 6.S894 Accelerated Computing, les labs](https://accelerated-computing.academy/fall25/labs/) · assignment |
| `cu-02-divergence` | [NVIDIA, CUDA Programming Guide, Advanced Kernel Programming](https://docs.nvidia.com/cuda/cuda-programming-guide/03-advanced/advanced-kernel-programming.html) · docs<br>[NVIDIA, CUDA C++ Best Practices Guide, Branching and Divergence](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#branching-and-divergence) · docs<br>[CS149 Stanford, cours 7, GPU Architecture and CUDA Programming](https://gfxcourses.stanford.edu/cs149/fall23/lecture/gpucuda/) · course<br>[Harris, Optimizing Parallel Reduction in CUDA](https://developer.download.nvidia.com/assets/cuda/files/reduction.pdf) · article<br>[MIT 6.S894 Accelerated Computing, les labs](https://accelerated-computing.academy/fall25/labs/) · assignment |
| `tri-01-vecadd` | [Tutoriels officiels Triton, vector add](https://triton-lang.org/main/getting-started/tutorials/01-vector-add.html) · docs<br>[Tillet, Kung, Cox, Triton: An Intermediate Language and Compiler](https://dl.acm.org/doi/10.1145/3315508.3329973) · article<br>[JINO-ROHIT/gpt-triton](https://github.com/JINO-ROHIT/gpt-triton) · repo<br>[a-hamdi/GPU](https://github.com/a-hamdi/GPU) · repo |
| `tri-02-softmax` | [Tutoriels officiels Triton, fused softmax](https://triton-lang.org/main/getting-started/tutorials/02-fused-softmax.html) · docs<br>[Goldberg, What Every Computer Scientist Should Know About Floating-Point](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html) · article<br>[Milakov et Gimelshein, Online normalizer calculation for softmax](https://arxiv.org/abs/1805.02867) · article<br>[JINO-ROHIT/Flash-Attention-Series/01-softmax](https://github.com/JINO-ROHIT/Flash-Attention-Series/tree/main/01-softmax) · repo |
| `tri-03-matmul` | [Harvard CS249r, Machine Learning Systems at Scale, chapitre Performance Engineering](https://mlsysbook.ai/vol2/performance_engineering/performance_engineering.html) · book<br>[hkproj/triton-flash-attention](https://github.com/hkproj/triton-flash-attention) · repo |
| `inf-07-pagedattention` | [JINO-ROHIT/nano-paged-attention](https://github.com/JINO-ROHIT/nano-paged-attention) · repo<br>[JINO-ROHIT/ORCA](https://github.com/JINO-ROHIT/ORCA) · repo |
| `inf-08-fragmentation` | [JINO-ROHIT/nano-paged-attention](https://github.com/JINO-ROHIT/nano-paged-attention) · repo |

---

← [ms-02-cpp-concurrence](../ms-02-cpp-concurrence) · [the roadmap](../README.md) · [ms-04-cuda](../ms-04-cuda) →
