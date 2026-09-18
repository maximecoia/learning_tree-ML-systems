<!-- Généré par carte_phases.py. Ne pas éditer à la main. -->

# Phase 1 — The prep, C and Python

`ms-00-prepa` · Sept–Oct 2026 · 11 sub-modules, 11 written · 68 exercises

**What it buys.** enter the school with the libft done, a GPT trained by hand, and a C inference engine whose throughput is measured and placed on a roofline

**How it ends.** Not on a feeling, on one binary test: *Tu dessines de mémoire le flux d'un token d'entrée jusqu'aux logits, avec les shapes annotées à chaque étape.*

Descriptions below translate the curriculum's own `competence` field, one sentence per sub-module. Each translation is stored with a fingerprint of the French it was made from, so a source that changes stops this page from being rebuilt rather than outrunning it.

| Sub-module | Layer | What it covers | Where the work is |
|---|---|---|---|
| `py-01-basics` | added | Write Python functions using the language's variables, arithmetic operators, strings, conditionals, loops, lists, dictionaries and functions | [py-01-basics](py-01-basics) · 9 exercises |
| `py-02-advanced` | added | Model a piece of data as a Python class, with its methods, its operators, its properties and its inheritance | [py-02-advanced](py-02-advanced) · 9 exercises |
| `py-03-livrer` | added | Ship a Python command-line tool, packaged, tested and installable by someone else | [py-03-livrer](py-03-livrer) · 8 exercises |
| `c-01-libft` | added | Write a static C library whose every function honours the exact contract of the libc | 42 subject, not published · 6 exercises |
| `maths-01-algebre` | added | Implement 2D vector and matrix transformations in Python | not started · 8 exercises |
| `mth-03-probas` | added | Simulate a distribution, hold it against its closed form, and know how many measurements it takes to tell two values apart | not started · 6 exercises |
| `mth-04-statistiques` | added | Judge whether two series of measurements really differ, knowing how often you will be wrong | not started · 6 exercises |
| `rte-01-puzzles` | added | Write in a single line, by broadcasting and indexing alone, the functions NumPy hands you ready-made, and know why each one holds without a loop | [srush/Tensor-Puzzles](https://github.com/srush/Tensor-Puzzles), answers kept out · 1 exercise |
| `rte-02-cs336` | added | Write the building blocks of a language model, its loss, its optimiser, its checkpoints and its BPE tokenizer, and make them pass the public suite of a course that knows nothing of your architecture | [stanford-cs336/assignment1-basics](https://github.com/stanford-cs336/assignment1-basics), answers kept out · 5 exercises |
| `c-02-moteur` | added | Write an inference engine in C that loads a model, generates text, measures its throughput and places itself on a roofline | not started · 7 exercises |
| `l1-01-gpt-corpus` | proof | Publish a language model trained end to end, and defend every part of how it works without the code in front of you | not started · 3 exercises |

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

---

[the roadmap](../README.md) · [ms-01-inference](../ms-01-inference) →
