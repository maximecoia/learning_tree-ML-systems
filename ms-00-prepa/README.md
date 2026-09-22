<!-- Généré par carte_phases.py. Ne pas éditer à la main. -->

# Phase 1 — The prep, C and Python

`ms-00-prepa` · Sept–Oct 2026 · 11 sub-modules, 11 written · 68 exercises

**What it buys.** enter the school with the libft done, a GPT trained by hand, and a C inference engine whose throughput is measured and placed on a roofline

**How it ends.** Not on a feeling, on one binary test: *Tu dessines de mémoire le flux d'un token d'entrée jusqu'aux logits, avec les shapes annotées à chaque étape.*


## What to do, in order

One table, from what is done to what waits. Every state is read from a grader, never from the presence of a file: `./exo` runs the curriculum's checkers, each borrowed assignment brings its own, and `verifier.py` holds the 6 gates of the acceptance test. The first row without a tick is the work of today, marked →. The route closes on 18 October 2026 and the phase on 31 October 2026; `./exo` prints the pace those dates imply.

| | Step | State | What grades it | Where |
|---|---|---|---|---|
| ✓ | `py-01-basics` | ✓ 9 of 9 | its grader, through `./exo` | [py-01-basics](py-01-basics) |
| ✓ | `py-02-advanced` | ✓ 9 of 9 | its grader, through `./exo` | [py-02-advanced](py-02-advanced) |
| ✓ | `py-03-livrer` | ✓ 8 of 8 | its grader, through `./exo` | [py-03-livrer](py-03-livrer) |
| ✓ | `c-01-libft` | ✓ 6 of 6 | its grader, through `./exo` | 42 subject, not published |
| ✓ | Tensor Puzzles — 21 puzzles, one line each — `rte-01-puzzles` | ✓ 1 of 1 | the checker inside the notebook | [rte-01-puzzles](rte-01-puzzles), from [srush/Tensor-Puzzles](https://github.com/srush/Tensor-Puzzles) |
| → | Text data: tokenizer, sliding window, embeddings (Raschka ch. 2) | `ex00`, 8 tests: red · `ex04`, 28 tests: red | the book's exercise solutions and chapter quiz | [rte-route-l1/ch02.py](rte-route-l1/ch02.py), from [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) |
|  | Causal attention: scores, mask, multiple heads (Raschka ch. 3) | `ex00`, 8 tests: red · gate 3: gpt.py is still the blank file | same, plus gate 3 | [rte-route-l1/ch03.py](rte-route-l1/ch03.py), from [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) |
|  | The GPT: blocks, normalisation, residuals, logits (Raschka ch. 4) | gates 1, 2, 4 and 6: gpt.py is still the blank file | gates 1, 2, 4 and 6 | [rte-route-l1/ch04.py](rte-route-l1/ch04.py), from [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) |
|  | Pretraining: the loop, train and validation loss, sampling (Raschka ch. 5) | `ex01`, 3 tests: red · `ex02`, 2 tests: red · `ex03`, 1 test: red · gate 5: gpt.py is still the blank file | gate 5 | [rte-route-l1/ch05.py](rte-route-l1/ch05.py), from [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) |
|  | CS336 assignment 1 — the 15 architecture-agnostic adapters — `rte-02-cs336` | 0 of 5 · 5 handed in, red | its public `pytest` suite | [stanford-cs336/assignment1-basics](https://github.com/stanford-cs336/assignment1-basics), answers kept out |
|  | `gpt.py` from a blank file, the acceptance test | 0 of 6 gates · gpt.py is still the blank file | `verifier.py`, [the gates](../README.md#the-acceptance-test) | lands here with the model |
|  | `l1-01-gpt-corpus` | 3 steps, a quiz · not counted here | the quiz, then the public repository | lands here with the model |
|  | `c-02-moteur` | 0 of 7 · out of the window, it needs the weights L1 produces | its grader, through `./exo` | lands here |

**Alongside, in the background.** The curriculum files these under a `fil` named « Maths en fond »: work that runs beside the sequence rather than as a step of it. `maths-01-algebre` 0 of 8 · `mth-03-probas` 0 of 6 · `mth-04-statistiques` 0 of 6.

## What each sub-module covers

Descriptions below translate the curriculum's own `competence` field, one sentence per sub-module. Each translation is stored with a fingerprint of the French it was made from, so a source that changes stops this page from being rebuilt rather than outrunning it. Rows are in the order the work goes, read from the curriculum's `apres` and `fil` fields; work done alongside the sequence comes last.

| Sub-module | Layer | What it covers | Where the work is |
|---|---|---|---|
| `py-01-basics` | added | Write Python functions using the language's variables, arithmetic operators, strings, conditionals, loops, lists, dictionaries and functions | [py-01-basics](py-01-basics) · 9 exercises |
| `py-02-advanced` | added | Model a piece of data as a Python class, with its methods, its operators, its properties and its inheritance | [py-02-advanced](py-02-advanced) · 9 exercises |
| `py-03-livrer` | added | Ship a Python command-line tool, packaged, tested and installable by someone else | [py-03-livrer](py-03-livrer) · 8 exercises |
| `c-01-libft` | added | Write a static C library whose every function honours the exact contract of the libc | 42 subject, not published · 6 exercises |
| `rte-01-puzzles` | added | Write in a single line, by broadcasting and indexing alone, the functions NumPy hands you ready-made, and know why each one holds without a loop | [rte-01-puzzles](rte-01-puzzles), from [srush/Tensor-Puzzles](https://github.com/srush/Tensor-Puzzles) · 1 exercise |
| `rte-02-cs336` | added | Write the building blocks of a language model, its loss, its optimiser, its checkpoints and its BPE tokenizer, and make them pass the public suite of a course that knows nothing of your architecture | [stanford-cs336/assignment1-basics](https://github.com/stanford-cs336/assignment1-basics), answers kept out · 5 exercises |
| `l1-01-gpt-corpus` | proof | Publish a language model trained end to end, and defend every part of how it works without the code in front of you | not started · 3 exercises |
| `c-02-moteur` | added | Write an inference engine in C that loads a model, generates text, measures its throughput and places itself on a roofline | not started · 7 exercises |
| `maths-01-algebre` | added | Implement 2D vector and matrix transformations in Python | not started · 8 exercises |
| `mth-03-probas` | added | Simulate a distribution, hold it against its closed form, and know how many measurements it takes to tell two values apart | not started · 6 exercises |
| `mth-04-statistiques` | added | Judge whether two series of measurements really differ, knowing how often you will be wrong | not started · 6 exercises |

## Reading

What each sub-module points at, straight from the curriculum. Links only: why a given one is there is written in French, next to the curriculum itself, and translating it would put the same sentence in two places waiting to disagree. A sub-module absent from this table has nothing declared yet, and a resource that lives in a repository you cannot open is left out rather than linked to a 404.

| Sub-module | Points at |
|---|---|
| `py-01-basics` | [Le tutoriel Python officiel](https://docs.python.org/3/tutorial/) · [PEP 8, le style du code Python](https://peps.python.org/pep-0008/) |
| `py-02-advanced` | [Le modèle de données Python](https://docs.python.org/3/reference/datamodel.html) · [functools, et total_ordering](https://docs.python.org/3/library/functools.html) · [Le tutoriel Python officiel, les classes](https://docs.python.org/3/tutorial/classes.html) |
| `py-03-livrer` | [argparse, le tutoriel](https://docs.python.org/3/howto/argparse.html) · [unittest](https://docs.python.org/3/library/unittest.html) · [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/) · [Writing your pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) · [Fluent Python, chapitre 1](https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/) |
| `c-01-libft` | [Sujet 42, libft](https://projects.intra.42.fr/projects/libft) · [man 3 string](https://man7.org/linux/man-pages/man3/string.3.html) · [man 3 malloc](https://man7.org/linux/man-pages/man3/malloc.3.html) |
| `rte-01-puzzles` | [srush/Tensor-Puzzles](https://github.com/srush/Tensor-Puzzles) · [Sasha Rush, la vidéo de résolution](https://youtu.be/Hafo7hIl8MU) |
| `rte-02-cs336` | [stanford-cs336/assignment1-basics](https://github.com/stanford-cs336/assignment1-basics) · [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) · [CS336, la page du cours](https://online.stanford.edu/courses/cs336-language-modeling-scratch) · [JINO-ROHIT/advanced_ml/05-tokenizers](https://github.com/JINO-ROHIT/advanced_ml/tree/main/05-tokenizers) |
| `l1-01-gpt-corpus` | [srush/Tensor-Puzzles](https://github.com/srush/Tensor-Puzzles) · [Sebastian Raschka, Build a Large Language Model (From Scratch)](https://www.manning.com/books/build-a-large-language-model-from-scratch) · [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) · [stanford-cs336/assignment1-basics](https://github.com/stanford-cs336/assignment1-basics) · [Let's reproduce GPT-2 (124M)](https://www.youtube.com/watch?v=l8pRSuU81PU) · [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT) · [hkproj/pytorch-transformer](https://github.com/hkproj/pytorch-transformer) · [JINO-ROHIT/gpt2-tamil](https://github.com/JINO-ROHIT/gpt2-tamil) |
| `c-02-moteur` | [karpathy/llama2.c](https://github.com/karpathy/llama2.c) · [karpathy/llm.c](https://github.com/karpathy/llm.c) · [ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp) · [Williams, Waterman, Patterson, Roofline: An Insightful Visual Performance Model](https://dl.acm.org/doi/10.1145/1498765.1498785) · [kipply, Transformer Inference Arithmetic](https://kipp.ly/transformer-inference-arithmetic/) · [JINO-ROHIT/inferGPT](https://github.com/JINO-ROHIT/inferGPT) · [JINO-ROHIT/nano-llama.cpp](https://github.com/JINO-ROHIT/nano-llama.cpp) |
| `maths-01-algebre` | [MIT 18.06SC, Linear Algebra (Gilbert Strang)](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/) · [3Blue1Brown, Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra) · [Deisenroth, Faisal, Ong, Mathematics for Machine Learning](https://mml-book.github.io/) · [JINO-ROHIT/ml-math-in-depth](https://github.com/JINO-ROHIT/ml-math-in-depth) |
| `mth-03-probas` | [MIT 18.05, Introduction to Probability and Statistics](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/) · [Deisenroth, Faisal, Ong, Mathematics for Machine Learning](https://mml-book.github.io/) · [3Blue1Brown, la formule de Bayes](https://www.3blue1brown.com/lessons/bayes-theorem) · [Knuth, The Art of Computer Programming, volume 2](https://www-cs-faculty.stanford.edu/~knuth/taocp.html) · [Higham, Accuracy and Stability of Numerical Algorithms](https://epubs.siam.org/doi/book/10.1137/1.9780898718027) |
| `mth-04-statistiques` | [MIT 18.05, Introduction to Probability and Statistics](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/) · [Deisenroth, Faisal, Ong, Mathematics for Machine Learning](https://mml-book.github.io/) · [Efron et Hastie, Computer Age Statistical Inference](https://hastie.su.domains/CASI/) · [Ioannidis, Why Most Published Research Findings Are False](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.0020124) · [Reinhart, Statistics Done Wrong](https://www.statisticsdonewrong.com/) |

---

[the roadmap](../README.md) · [ms-01-inference](../ms-01-inference) →
