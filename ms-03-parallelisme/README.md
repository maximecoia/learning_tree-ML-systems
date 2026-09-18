<!-- Généré par carte_phases.py. Ne pas éditer à la main. -->

# Phase 4 — Parallelism, first kernel, entering vLLM

`ms-03-parallelisme` · weeks 21–34 · 21 sub-modules, 7 written · 24 exercises

**What it buys.** say before writing a kernel whether it will be compute- or memory-bound, and a PR in vLLM or SGLang on the scheduler or the cache, review taken up by a maintainer

**How it ends.** Not on a feeling, on one binary test: *L5 existe. Et on te décrit un kernel : tu estimes avant de coder s'il sera compute- ou memory-bound, et tu justifies par un ordre de grandeur.*

Descriptions below are the curriculum's own `competence` field, quoted verbatim and left in French; everything else on this page is not.

| Sub-module | Layer | What it covers | Where the work is |
|---|---|---|---|
| `t42-03-codexion` | imposed | — | 42 subject, not published |
| `t42-04-flyin` | imposed | — | 42 subject, not published |
| `t42-05-callmemaybe` | imposed | — | 42 subject, not published |
| `c-11-simd` | added | Décomposer un calcul en fils et mesurer le déséquilibre que la décomposition crée, écrire du code vectoriel sous masque et lire l'utilisation des voies, faire vectoriser une boucle par le compilateur et le vérifier, et relier le plafond d'un calcul à la bande passante de la machine | not started · 4 exercises |
| `c-12-ordonnancement` | added | Écrire un ordonnanceur de tâches en lots sur des fils créés une fois, mesurer le déséquilibre entre fils avant de le corriger, et exécuter des lots dépendants sans qu'aucun ne parte avant ce qu'il attend | not started · 4 exercises |
| `par-05-philosophes-warps` | added | Relier le code concurrent qu'on a écrit, fils, mutex, famine, au modèle SIMT d'un GPU, en nommant ce qui se transpose, ce qui change de nature, et ce qui n'existe plus | not started · 1 exercise |
| `cu-01-bases` | added | Écrire des kernels CUDA, du calcul élémentaire au rendu concurrent, qui s'exécutent sur l'émulation hôte du correcteur comme sur un GPU: un fil par élément avec sa borne, un scan en mémoire partagée avec ses barrières, et une décomposition qui garantit l'ordre et l'atomicité | not started · 4 exercises |
| `cu-02-divergence` | added | Chiffrer ce qu'une divergence de warp coûte, toutes choses égales par ailleurs, en lisant warp par warp lesquels ont pris les deux chemins et en appliquant le modèle SIMT | not started · 1 exercise |
| `tri-01-vecadd` | added | Écrire un kernel Triton qui ne sort jamais de son tampon, choisir sa taille de bloc en la justifiant par un compte, et fusionner plusieurs passes en une | not started · 5 exercises |
| `tri-02-softmax` | added | Écrire une softmax par ligne qui ne déborde jamais, et contrôler un kernel sur quatre axes plutôt qu'un | not started · 5 exercises |
| `tri-03-matmul` | added | — | planned, not written yet |
| `tri-04-classement` | added | — | planned, not written yet |
| `tri-05-note` | added | — | planned, not written yet |
| `inf-07-pagedattention` | added | — | planned, not written yet |
| `inf-08-fragmentation` | added | — | planned, not written yet |
| `inf-09-compiler-vllm` | added | — | planned, not written yet |
| `inf-10-chemin-requete` | added | — | planned, not written yet |
| `inf-11-reproduire-bug` | added | — | planned, not written yet |
| `inf-12-premiere-pr` | added | — | planned, not written yet |
| `inf-13-choisir-issue` | added | — | planned, not written yet |
| `l5-01-contribution` | proof | — | planned, not written yet |

---

← [ms-02-cpp-concurrence](../ms-02-cpp-concurrence) · [the roadmap](../README.md) · [ms-04-cuda](../ms-04-cuda) →
