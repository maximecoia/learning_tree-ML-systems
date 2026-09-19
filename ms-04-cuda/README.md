<!-- Généré par carte_phases.py. Ne pas éditer à la main. -->

# Phase 5 — CUDA properly

`ms-04-cuda` · weeks 35–46 · 17 sub-modules, 5 written · 15 exercises

**What it buys.** a kernel that beats the reference on a bounded case, gain reproducible with its standard deviation, and where it loses too

**How it ends.** Not on a feeling, on one binary test: *Tu produis une frise d'exécution et tu nommes le trou. Tu estimes avant de coder si un kernel sera compute- ou memory-bound.*

Descriptions below translate the curriculum's own `competence` field, one sentence per sub-module. Each translation is stored with a fingerprint of the French it was made from, so a source that changes stops this page from being rebuilt rather than outrunning it.

| Sub-module | Layer | What it covers | Where the work is |
|---|---|---|---|
| `sh-02-netpractice` | imposed | — | 42 subject, not published |
| `t42-06-pacman` | imposed | — | 42 subject, not published |
| `t42-07-rag-machine` | imposed | — | 42 subject, not published |
| `cu-03-indexation` | added | — | planned, not written yet |
| `cu-04-coalescence` | added | — | planned, not written yet |
| `cu-05-tiling` | added | — | planned, not written yet |
| `cu-06-reduction` | added | — | planned, not written yet |
| `cu-07-occupancy` | added | — | planned, not written yet |
| `cu-08-nsight-compute` | added | — | planned, not written yet |
| `cu-09-roofline` | added | — | planned, not written yet |
| `cu-11-assembleur` | added | — | planned, not written yet |
| `cu-10-battre` | proof | — | planned, not written yet |
| `cpp-06-exceptions` | added | Refuse by exception that an invalid object exist, translate an exception into a sentence where it is caught, and guarantee that a non-local exit leaves nothing alive | 42 subject, not published · 3 exercises |
| `cpp-07-casts` | added | Choose between static_cast, reinterpret_cast and dynamic_cast by what each one promises, read a literal and write it into four types saying when the conversion makes no sense, and recognise the real type behind a base | 42 subject, not published · 3 exercises |
| `cpp-08-templates` | added | Write generic code that holds for any type carrying the operations it uses, and a templated container that deep-copies and refuses an out-of-bounds index | 42 subject, not published · 3 exercises |
| `cpp-09-conteneurs` | added | Use the standard library's containers and algorithms instead of rewriting them, pick the structure that answers a question in N log N rather than N², and extend a container by inheritance without breaking what it is | 42 subject, not published · 3 exercises |
| `cpp-10-stl` | added | Pick the container that answers a question in one lookup, write a complete program that reads, validates and refuses its input, and implement a sorting algorithm described in the literature while counting its comparisons | 42 subject, not published · 3 exercises |

---

← [ms-03-parallelisme](../ms-03-parallelisme) · [the roadmap](../README.md) · [ms-05-fin-tronc-commun](../ms-05-fin-tronc-commun) →
