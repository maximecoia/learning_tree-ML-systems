<!-- Généré par carte_phases.py. Ne pas éditer à la main. -->

# Phase 5 — CUDA properly

`ms-04-cuda` · weeks 35–46 · 17 sub-modules, 5 written · 15 exercises

**What it buys.** a kernel that beats the reference on a bounded case, gain reproducible with its standard deviation and where it loses too, then the harness that proves it, run against an agent and shown rejecting a bad submission

**How it ends.** Not on a feeling, on one binary test: *On te donne un kernel et un rapport Nsight Compute. Tu nommes la précision avant de classer le goulot, et ton propre kernel bat la référence nommée sur un cas délimité avec une mesure qui survit au rejeu : même harnais, ordre des appels changé, entrées regénérées.*

Descriptions below translate the curriculum's own `competence` field, one sentence per sub-module. Each translation is stored with a fingerprint of the French it was made from, so a source that changes stops this page from being rebuilt rather than outrunning it. Rows are in the order the work goes, read from the curriculum's `apres` and `fil` fields; work done alongside the sequence comes last.

| Sub-module | Layer | What it covers | Where the work is |
|---|---|---|---|
| `sh-02-netpractice` | imposed | Split a network into subnets that satisfy a subject's constraints, and diagnose a configuration that does not route by naming the cause | 42 subject, not published |
| `t42-06-pacman` | imposed | Validate `pacman` at the perimeter of its subject, adding nothing | 42 subject, not published |
| `t42-07-rag-machine` | imposed | Validate `RAG against the machine` at the perimeter of its subject, adding nothing and keeping it out of the showcase | 42 subject, not published |
| `cu-03-indexation` | added | Work out a thread's global index from its grid and its block, and write a kernel where every thread bounds its access whatever the size of the data | planned, not written yet |
| `cu-04-coalescence` | added | Put a figure on what an uncoalesced memory access costs, all else being equal, and reorder a kernel's accesses until the measurement moves | planned, not written yet |
| `cu-05-tiling` | added | Tile a kernel in shared memory, justify the tile size by the memory available per block, and measure the global memory traffic saved | planned, not written yet |
| `cu-06-reduction` | added | Write a reduction that stays exact whatever the input size, and say at each step how many threads are still working | planned, not written yet |
| `cu-07-occupancy` | added | Compute a kernel's occupancy from its registers and its shared memory, and show on a measurement that higher occupancy is not always faster | planned, not written yet |
| `cu-08-nsight-compute` | added | Read an Nsight Compute report and classify a kernel's bottleneck by naming the precision first, the same kernel turning from memory-bound in fp32 to compute-bound in fp8 on the same hardware | planned, not written yet |
| `cu-09-roofline` | added | Place a kernel on a roofline built from your own micro-benchmarks, and not from the figures the vendor announces | planned, not written yet |
| `cu-11-assembleur` | added | Read a kernel's SASS to explain a counter of the Nsight Compute report, and stop at reading | planned, not written yet |
| `cu-10-battre` | proof | Beat the reference with a kernel of your own on a precisely bounded case: gain measured, standard deviation shown, measurement replayed, and the cases where it loses said too | planned, not written yet |
| `cpp-06-exceptions` | added | Refuse by exception that an invalid object exist, translate an exception into a sentence where it is caught, and guarantee that a non-local exit leaves nothing alive | 42 subject, not published · 3 exercises |
| `cpp-07-casts` | added | Choose between static_cast, reinterpret_cast and dynamic_cast by what each one promises, read a literal and write it into four types saying when the conversion makes no sense, and recognise the real type behind a base | 42 subject, not published · 3 exercises |
| `cpp-08-templates` | added | Write generic code that holds for any type carrying the operations it uses, and a templated container that deep-copies and refuses an out-of-bounds index | 42 subject, not published · 3 exercises |
| `cpp-09-conteneurs` | added | Use the standard library's containers and algorithms instead of rewriting them, pick the structure that answers a question in N log N rather than N², and extend a container by inheritance without breaking what it is | 42 subject, not published · 3 exercises |
| `cpp-10-stl` | added | Pick the container that answers a question in one lookup, write a complete program that reads, validates and refuses its input, and implement a sorting algorithm described in the literature while counting its comparisons | 42 subject, not published · 3 exercises |

## Reading

What each sub-module points at, straight from the curriculum. Links only: why a given one is there is written in French, next to the curriculum itself, and translating it would put the same sentence in two places waiting to disagree. A sub-module absent from this table has nothing declared yet.

| Sub-module | Points at |
|---|---|
| `cu-03-indexation` | [Boehm, How to Optimize a CUDA Matmul Kernel for cuBLAS-like Performance: a Worklog](https://siboehm.com/articles/22/CUDA-MMM) · [a-hamdi/GPU](https://github.com/a-hamdi/GPU) |
| `cu-04-coalescence` | [Boehm, How to Optimize a CUDA Matmul Kernel for cuBLAS-like Performance: a Worklog](https://siboehm.com/articles/22/CUDA-MMM) · [JINO-ROHIT/kernels/cuda](https://github.com/JINO-ROHIT/kernels/tree/main/cuda) |
| `cu-05-tiling` | [Boehm, How to Optimize a CUDA Matmul Kernel for cuBLAS-like Performance: a Worklog](https://siboehm.com/articles/22/CUDA-MMM) · [MIT 6.S894 Accelerated Computing, les labs](https://accelerated-computing.academy/fall25/labs/) · [JINO-ROHIT/kernels/cuda/matmul](https://github.com/JINO-ROHIT/kernels/tree/main/cuda/matmul) · [JINO-ROHIT/Flash-Attention-Series/02-tiling](https://github.com/JINO-ROHIT/Flash-Attention-Series/tree/main/02-tiling) |
| `cu-06-reduction` | [JINO-ROHIT/kernels/cuda/reduction](https://github.com/JINO-ROHIT/kernels/tree/main/cuda/reduction) · [a-hamdi/GPU](https://github.com/a-hamdi/GPU) |
| `cu-07-occupancy` | [Boehm, How to Optimize a CUDA Matmul Kernel for cuBLAS-like Performance: a Worklog](https://siboehm.com/articles/22/CUDA-MMM) · [MIT 6.S894 Accelerated Computing, les labs](https://accelerated-computing.academy/fall25/labs/) |
| `cu-08-nsight-compute` | [Boehm, How to Optimize a CUDA Matmul Kernel for cuBLAS-like Performance: a Worklog](https://siboehm.com/articles/22/CUDA-MMM) |
| `cu-09-roofline` | [Harvard CS249r, Machine Learning Systems at Scale, chapitre Performance Engineering](https://mlsysbook.ai/vol2/performance_engineering/performance_engineering.html) |
| `cu-11-assembleur` | [Boehm, How to Optimize a CUDA Matmul Kernel for cuBLAS-like Performance: a Worklog](https://siboehm.com/articles/22/CUDA-MMM) · [JINO-ROHIT/kernels/cuda/matmul/01_naive_ptx.cu](https://github.com/JINO-ROHIT/kernels/blob/main/cuda/matmul/01_naive_ptx.cu) |
| `cu-10-battre` | [Boehm, How to Optimize a CUDA Matmul Kernel for cuBLAS-like Performance: a Worklog](https://siboehm.com/articles/22/CUDA-MMM) · [MIT 6.S894 Accelerated Computing, les labs](https://accelerated-computing.academy/fall25/labs/) · [JINO-ROHIT/kernels/cute_dsl/matmul](https://github.com/JINO-ROHIT/kernels/tree/main/cute_dsl/matmul) · [a-hamdi/GPU](https://github.com/a-hamdi/GPU) |
| `cpp-06-exceptions` | [Anciens sujets 42, CPP Module 05](https://projects.intra.42.fr/projects/cpp-module-05) · [cppreference, exceptions](https://en.cppreference.com/w/cpp/language/exceptions) · [cppreference, std::exception](https://en.cppreference.com/w/cpp/error/exception) · [ISO C++, FAQ exceptions](https://isocpp.org/wiki/faq/exceptions) · [Stroustrup, Exception Safety: Concepts and Techniques](https://www.stroustrup.com/except.pdf) |
| `cpp-07-casts` | [Anciens sujets 42, CPP Module 06](https://projects.intra.42.fr/projects/cpp-module-06) · [cppreference, static_cast](https://en.cppreference.com/w/cpp/language/static_cast) · [cppreference, reinterpret_cast](https://en.cppreference.com/w/cpp/language/reinterpret_cast) · [cppreference, dynamic_cast](https://en.cppreference.com/w/cpp/language/dynamic_cast) · [cppreference, std::strtod](https://en.cppreference.com/w/cpp/string/byte/strtof) · [ISO C++, FAQ casts](https://isocpp.org/wiki/faq/coding-standards#casts) |
| `cpp-08-templates` | [Anciens sujets 42, CPP Module 07](https://projects.intra.42.fr/projects/cpp-module-07) · [cppreference, templates](https://en.cppreference.com/w/cpp/language/templates) · [cppreference, class template](https://en.cppreference.com/w/cpp/language/class_template) · [cppreference, new expression, initialisation](https://en.cppreference.com/w/cpp/language/new) · [ISO C++, FAQ templates](https://isocpp.org/wiki/faq/templates) |
| `cpp-09-conteneurs` | [Anciens sujets 42, CPP Module 08](https://projects.intra.42.fr/projects/cpp-module-08) · [cppreference, la bibliothèque des conteneurs](https://en.cppreference.com/w/cpp/container) · [cppreference, std::find](https://en.cppreference.com/w/cpp/algorithm/find) · [cppreference, std::stack](https://en.cppreference.com/w/cpp/container/stack) · [cppreference, std::sort](https://en.cppreference.com/w/cpp/algorithm/sort) · [Stroustrup, The C++ Programming Language, chapitre STL](https://www.stroustrup.com/4th.html) |
| `cpp-10-stl` | [Anciens sujets 42, CPP Module 09](https://projects.intra.42.fr/projects/cpp-module-09) · [cppreference, std::map](https://en.cppreference.com/w/cpp/container/map) · [cppreference, std::stack](https://en.cppreference.com/w/cpp/container/stack) · [Knuth, The Art of Computer Programming, vol. 3, 5.3.1, merge insertion](https://www-cs-faculty.stanford.edu/~knuth/taocp.html) · [Ford et Johnson, A Tournament Problem, 1959](https://doi.org/10.2307/2308750) · [OEIS, suite de Jacobsthal A001045](https://oeis.org/A001045) |

---

← [ms-03-parallelisme](../ms-03-parallelisme) · [the roadmap](../README.md) · [ms-05-fin-tronc-commun](../ms-05-fin-tronc-commun) →
