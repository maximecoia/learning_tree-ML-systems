<!-- Généré par carte_phases.py. Ne pas éditer à la main. -->

# Phase 1 — The prep, C and Python

`ms-00-prepa` · Sept–Oct 2026 · 9 sub-modules, 9 written · 56 exercises

**What it buys.** enter the school with the libft done, a GPT trained by hand, and a C inference engine whose throughput is measured and placed on a roofline

**How it ends.** Not on a feeling, on one binary test: *Tu dessines de mémoire le flux d'un token d'entrée jusqu'aux logits, avec les shapes annotées à chaque étape.*

Descriptions below are the curriculum's own `competence` field, quoted verbatim and left in French; everything else on this page is not.

| Sub-module | Layer | What it covers | Where the work is |
|---|---|---|---|
| `py-01-basics` | added | Écrire des fonctions Python avec les variables, opérateurs arithmétiques, chaînes, conditions, boucles, listes, dictionnaires et fonctions du langage | [py-01-basics](py-01-basics) · 9 exercises |
| `py-02-advanced` | added | Modéliser une donnée par une classe Python avec ses méthodes, ses opérateurs, ses propriétés et son héritage | [py-02-advanced](py-02-advanced) · 9 exercises |
| `py-03-livrer` | added | Livrer un outil Python en ligne de commande, empaqueté, testé et installable par un autre | [py-03-livrer](py-03-livrer) · 8 exercises |
| `c-01-libft` | added | Écrire une bibliothèque C statique dont chaque fonction respecte le contrat exact de la libc | 42 subject, not published · 6 exercises |
| `maths-01-algebre` | added | Implémenter les transformations vectorielles et matricielles 2D en Python | not started · 8 exercises |
| `rte-01-puzzles` | added | Écrire en une ligne, par diffusion et indexation seules, les fonctions que NumPy fournit toutes faites, et savoir pourquoi chacune tient sans boucle | [srush/Tensor-Puzzles](https://github.com/srush/Tensor-Puzzles), answers kept out · 1 exercise |
| `rte-02-cs336` | added | Écrire les briques d'un modèle de langage, sa perte, son optimiseur, ses points de reprise et son tokenizer BPE, et les faire passer la suite publique d'un cours qui ne connaît pas votre architecture | [stanford-cs336/assignment1-basics](https://github.com/stanford-cs336/assignment1-basics), answers kept out · 5 exercises |
| `c-02-moteur` | added | Écrire en C un moteur d'inférence qui charge un modèle, génère du texte, mesure son débit et se situe sur un roofline | not started · 7 exercises |
| `l1-01-gpt-corpus` | proof | Livrer publiquement un modèle de langage entraîné de bout en bout, et défendre chaque partie de son fonctionnement sans le code sous les yeux | not started · 3 exercises |

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
