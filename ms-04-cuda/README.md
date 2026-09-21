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

---

← [ms-03-parallelisme](../ms-03-parallelisme) · [the roadmap](../README.md) · [ms-05-fin-tronc-commun](../ms-05-fin-tronc-commun) →
