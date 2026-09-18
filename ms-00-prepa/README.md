<!-- Généré par carte_phases.py. Ne pas éditer à la main. -->

# Phase 1 — The prep, C and Python

`ms-00-prepa` · Sept–Oct 2026 · 7 sub-modules

**What it buys.** enter the school with the libft done, a GPT trained by hand, and a C inference engine whose throughput is measured and placed on a roofline

| Sub-module | Graded by | Where the work is |
|---|---|---|
| `py-01-basics` | a grader | [in this repository](py-01-basics) |
| `py-02-advanced` | a grader | [in this repository](py-02-advanced) |
| `py-03-livrer` | a grader | [in this repository](py-03-livrer) |
| `c-01-libft` | a grader | 42 subject, not published |
| `maths-01-algebre` | a grader | not started |
| `c-02-moteur` | a grader | waits for the trained model |
| `l1-01-gpt-corpus` | a quiz | not started |

## The route to the deliverable

These six steps are not curriculum sub-modules and are not graded by it. They are borrowed assignments, each arriving with its own checker, and they are the live work of this phase. They run in their own repositories, so nothing of them lands here until the model does.

| | Step | What grades it |
|---|---|---|
| 1 | Tensor Puzzles — 21 puzzles, one line each | the checker inside the notebook |
| 2 | Text data: tokenizer, sliding window, embeddings | the book's exercise solutions and chapter quiz |
| 3 | Causal attention: scores, mask, multiple heads | same, plus gate 3 below |
| 4 | The GPT: blocks, normalisation, residuals, logits | gates 1, 2, 4 and 6 below |
| 5 | Pretraining: the loop, train and validation loss, sampling | gate 5 below |
| 6 | CS336 assignment 1 — the 15 architecture-agnostic adapters | its public `pytest` suite |

The roadmap, the rule that decides what lands here and what does not, and where the phase stands are on the [main page](../README.md).
