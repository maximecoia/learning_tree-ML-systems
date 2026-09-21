<!-- Généré par carte_phases.py. Ne pas éditer à la main. -->

# Phase 2 — Graded C, measured inference

`ms-01-inference` · weeks 1–8 · 14 sub-modules, 14 written · 53 exercises

**What it buys.** produce the saturation curve of an unknown inference server in half a day

**How it ends.** Not on a feeling, on one binary test: *On te donne un serveur d'inférence inconnu. Tu produis sa courbe de saturation en une demi-journée.*

Descriptions below translate the curriculum's own `competence` field, one sentence per sub-module. Each translation is stored with a fingerprint of the French it was made from, so a source that changes stops this page from being rebuilt rather than outrunning it. Rows are in the order the work goes, read from the curriculum's `apres` and `fil` fields; work done alongside the sequence comes last.

| Sub-module | Layer | What it covers | Where the work is |
|---|---|---|---|
| `c-03-libft-norme` | imposed | Bring a C repository into line with an imposed norm, revisit every null return path and every free, and keep it behind a personal test harness that knows how to fail | 42 subject, not published · 3 exercises |
| `c-04-printf` | imposed | Write a variadic formatter whose output matches the libc's, conversion by conversion | 42 subject, not published · 3 exercises |
| `c-05-gnl` | imposed | Read a stream line by line with state that survives between calls, across several descriptors and without leaking | 42 subject, not published · 3 exercises |
| `c-06-pushswap` | imposed | Sort under a constrained set of operations, and defend the algorithm's real cost by measurement | 42 subject, not published · 5 exercises |
| `mes-01-chronometre` | added | Time a function without being fooled by noise or by warm-up | not started · 7 exercises |
| `mes-02-grandeurs` | added | Estimate an order of magnitude for compute, memory and cost before writing any code | not started · 3 exercises |
| `mes-03-profiler` | added | Locate the function that costs in a slow program, and prove that fixing it helped | not started · 6 exercises |
| `inf-01-servir` | added | Query an inference engine through its API, record its latency under a written protocol, and compare two engines without concluding beyond what the measurement allows | not started · 3 exercises |
| `inf-02-prefill-decode` | added | Separate a generation's two regimes by measurement, derive a cost model from it, and use that to predict the latency of a request never measured | not started · 3 exercises |
| `inf-03-cache-kv` | added | Quantify what the key-value cache saves in time and costs in memory, recognise by measurement an engine deprived of it, say from what context length it is the cache, not the weights, that caps concurrency, and name the attention variants by what each does to the shape of the cache | not started · 3 exercises |
| `inf-04-quantifier` | added | Measure a model's quality by its perplexity on a fixed corpus, measure what reduced precision gains in decoding while gaining nothing in prefill, settle between the two against a budget set in advance, and be able to say what a perplexity on short text does not see | not started · 4 exercises |
| `inf-05-harnais` | added | Hold N requests in flight against an inference server, record throughput, percentiles and refusal rate without any of the three traps skewing the figure, and produce a CSV the graph regenerates from | not started · 4 exercises |
| `inf-06-saturation` | added | Sweep an inference server's concurrency to its breaking point, locate that point by a rule stated in advance, and name the physical limit that sets it with the numbers that prove it | not started · 3 exercises |
| `l2-01-courbe` | proof | Publish an inference server's throughput and latency curve, with its protocol, its breaking point and the physical limit that sets it, and defend it without the code in front of you | not started · 3 exercises |

---

← [ms-00-prepa](../ms-00-prepa) · [the roadmap](../README.md) · [ms-02-cpp-concurrence](../ms-02-cpp-concurrence) →
