<!-- Généré par carte_phases.py. Ne pas éditer à la main. -->

# Phase 1 — The prep, C and Python

`ms-00-prepa` · Sept–Oct 2026 · 9 sub-modules, 9 written · 53 exercises

**What it buys.** enter the school with the libft done and a GPT trained by hand

**How it ends.** Not on a feeling, on one binary test: *Your `gpt.py`, written from a blank file, passes the seven gates of `verifier.py`: six on the model, the seventh on its training, whose validation loss lands 0.10 below the counted bigram.*


## What to do, in order

One table, from what is done to what waits. Every state is read from a grader, never from the presence of a file: `./exo` runs the curriculum's checkers, each borrowed assignment brings its own, and `verifier.py` holds the 7 gates of the acceptance test. The first row without a tick is the work of today, marked →. The route closes on 18 October 2026 and the phase on 31 October 2026; `./exo` prints the pace those dates imply.

| | Step | State | What grades it | Where |
|---|---|---|---|---|
| ✓ | `py-01-basics` | ✓ 9 of 9 | its grader, through `./exo` | [py-01-basics](py-01-basics) |
| ✓ | `py-02-advanced` | ✓ 9 of 9 | its grader, through `./exo` | [py-02-advanced](py-02-advanced) |
| ✓ | `py-03-livrer` | ✓ 8 of 8 | its grader, through `./exo` | [py-03-livrer](py-03-livrer) |
| ✓ | `c-01-libft` | ✓ 6 of 6 | its grader, through `./exo` | 42 subject, not published |
| ✓ | Tensor Puzzles — 21 puzzles, one expression each, twenty of them inside eighty columns — `rte-01-puzzles` | ✓ 1 of 1 | the checker inside the notebook | [rte-01-puzzles](rte-01-puzzles), from [srush/Tensor-Puzzles](https://github.com/srush/Tensor-Puzzles) |
| ✓ | Text data: tokenizer, sliding window, embeddings (Raschka ch. 2) | `test_ch02.py`, 5 tests: ✓ | `test_ch02.py`: upstream's test and four of mine | [rte-route-l1/ch02.py](rte-route-l1/ch02.py), from [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) |
| ✓ | Causal attention: scores, mask, multiple heads (Raschka ch. 3) | `test_ch03.py`, 8 tests: ✓ | `test_ch03.py` | [rte-route-l1/ch03.py](rte-route-l1/ch03.py), from [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) |
| ✓ | The GPT: blocks, normalisation, residuals, logits (Raschka ch. 4) | `test_ch04.py`, 14 tests: ✓ | `test_ch04.py` | [rte-route-l1/ch04.py](rte-route-l1/ch04.py), from [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) |
| ✓ | Pretraining: the loop, train and validation loss, sampling (Raschka ch. 5) | `test_ch05.py`, 17 tests: ✓ | `test_ch05.py` | [rte-route-l1/ch05.py](rte-route-l1/ch05.py), from [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) |
| ✓ | L1, part 1 of 2: `gpt.py`, written from a blank file, passes the acceptance test | ✓ 7 of 7 gates · gate 7 on `verne` | `verifier.py`, [the gates](../README.md#the-acceptance-test) | lands here with the model |
|  | L1, part 2 of 2: the public write-up, `l1-01-gpt-corpus`. The chosen corpus, the run, both curves, unsorted samples and the report | a person grades it, not a terminal · not counted here | a reader, who replays it without asking a question: [what it holds](../README.md#what-closes-l1) | lands here with the model |

**Alongside, in the background.** The curriculum files these under a `fil` named « Maths en fond »: work that runs beside the sequence rather than as a step of it. `maths-01-algebre` ✓ 8 of 8 · `mth-03-probas` ✓ 6 of 6 · `mth-04-statistiques` ✓ 6 of 6.

## What each sub-module covers

Descriptions below translate the curriculum's own `competence` field, one sentence per sub-module. Each translation is stored with a fingerprint of the French it was made from, so a source that changes stops this page from being rebuilt rather than outrunning it. Rows are in the order the work goes, read from the curriculum's `apres` and `fil` fields; work done alongside the sequence comes last.

| Sub-module | Layer | What it covers | Where the work is |
|---|---|---|---|
| `py-01-basics` | added | Write Python functions using the language's variables, arithmetic operators, strings, conditionals, loops, lists, dictionaries and functions | [py-01-basics](py-01-basics) · 9 exercises |
| `py-02-advanced` | added | Model a piece of data as a Python class, with its methods, its operators, its properties and its inheritance | [py-02-advanced](py-02-advanced) · 9 exercises |
| `py-03-livrer` | added | Ship a Python command-line tool, packaged, tested and installable by someone else | [py-03-livrer](py-03-livrer) · 8 exercises |
| `c-01-libft` | added | Write a static C library whose every function honours the exact contract of the libc | 42 subject, not published · 6 exercises |
| `rte-01-puzzles` | added | Write in a single line, by broadcasting and indexing alone, the functions NumPy hands you ready-made, and know why each one holds without a loop | [rte-01-puzzles](rte-01-puzzles), from [srush/Tensor-Puzzles](https://github.com/srush/Tensor-Puzzles) · 1 exercise |
| `l1-01-gpt-corpus` | proof | Publish a language model trained end to end, and defend every part of how it works without the code in front of you | [l1-01-gpt-corpus](l1-01-gpt-corpus) |
| `maths-01-algebre` | added | Implement 2D vector and matrix transformations in Python | [maths-01-algebre](maths-01-algebre) · 8 exercises |
| `mth-03-probas` | added | Simulate a distribution, hold it against its closed form, and know how many measurements it takes to tell two values apart | [mth-03-probas](mth-03-probas) · 6 exercises |
| `mth-04-statistiques` | added | Judge whether two series of measurements really differ, knowing how often you will be wrong | [mth-04-statistiques](mth-04-statistiques) · 6 exercises |

## Reading

What each sub-module points at, straight from the curriculum. Links only: why a given one is there is written in French, next to the curriculum itself, and translating it would put the same sentence in two places waiting to disagree. A sub-module absent from this table has nothing declared yet, and a resource that lives in a repository you cannot open is left out rather than linked to a 404.

| Sub-module | Points at |
|---|---|
| `py-01-basics` | [The official Python tutorial](https://docs.python.org/3/tutorial/) · docs<br>[PEP 8, the style guide for Python code](https://peps.python.org/pep-0008/) · docs |
| `py-02-advanced` | [The Python data model](https://docs.python.org/3/reference/datamodel.html) · docs<br>[functools, and total_ordering](https://docs.python.org/3/library/functools.html) · docs<br>[The official Python tutorial, classes](https://docs.python.org/3/tutorial/classes.html) · docs |
| `py-03-livrer` | [argparse, the tutorial](https://docs.python.org/3/howto/argparse.html) · docs<br>[unittest](https://docs.python.org/3/library/unittest.html) · docs<br>[Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/) · course<br>[Writing your pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) · docs<br>[Fluent Python, chapter 1](https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/) · book |
| `c-01-libft` | [42 subject, libft](https://projects.intra.42.fr/projects/libft) · assignment<br>[man 3 string](https://man7.org/linux/man-pages/man3/string.3.html) · docs<br>[man 3 malloc](https://man7.org/linux/man-pages/man3/malloc.3.html) · docs |
| `rte-01-puzzles` | [srush/Tensor-Puzzles](https://github.com/srush/Tensor-Puzzles) · repo<br>[Sasha Rush, the walkthrough video](https://youtu.be/Hafo7hIl8MU) · video |
| `l1-01-gpt-corpus` | [srush/Tensor-Puzzles](https://github.com/srush/Tensor-Puzzles) · repo<br>[Sebastian Raschka, Build a Large Language Model (From Scratch)](https://www.manning.com/books/build-a-large-language-model-from-scratch) · book<br>[rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) · repo<br>[stanford-cs336/assignment1-basics](https://github.com/stanford-cs336/assignment1-basics) · assignment<br>[Let's reproduce GPT-2 (124M)](https://www.youtube.com/watch?v=l8pRSuU81PU) · video<br>[karpathy/nanoGPT](https://github.com/karpathy/nanoGPT) · repo<br>[hkproj/pytorch-transformer](https://github.com/hkproj/pytorch-transformer) · repo<br>[JINO-ROHIT/gpt2-tamil](https://github.com/JINO-ROHIT/gpt2-tamil) · repo |
| `maths-01-algebre` | [MIT 18.06SC, Linear Algebra (Gilbert Strang)](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/) · course<br>[3Blue1Brown, Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra) · video<br>[Deisenroth, Faisal, Ong, Mathematics for Machine Learning](https://mml-book.github.io/) · book<br>[JINO-ROHIT/ml-math-in-depth](https://github.com/JINO-ROHIT/ml-math-in-depth) · repo |
| `mth-03-probas` | [MIT 18.05, Introduction to Probability and Statistics](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/) · course<br>[Deisenroth, Faisal, Ong, Mathematics for Machine Learning](https://mml-book.github.io/) · book<br>[3Blue1Brown, Bayes' theorem](https://www.3blue1brown.com/lessons/bayes-theorem) · video<br>[Knuth, The Art of Computer Programming, volume 2](https://www-cs-faculty.stanford.edu/~knuth/taocp.html) · book<br>[Higham, Accuracy and Stability of Numerical Algorithms](https://epubs.siam.org/doi/book/10.1137/1.9780898718027) · book |
| `mth-04-statistiques` | [MIT 18.05, Introduction to Probability and Statistics](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/) · course<br>[Deisenroth, Faisal, Ong, Mathematics for Machine Learning](https://mml-book.github.io/) · book<br>[Efron and Hastie, Computer Age Statistical Inference](https://hastie.su.domains/CASI/) · book<br>[Ioannidis, Why Most Published Research Findings Are False](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.0020124) · article<br>[Reinhart, Statistics Done Wrong](https://www.statisticsdonewrong.com/) · book |

---

[the roadmap](../README.md) · [ms-01-inference](../ms-01-inference) →
