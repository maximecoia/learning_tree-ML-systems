<!-- Généré par carte_phases.py. Ne pas éditer à la main. -->

# Phase 5 — CUDA properly

`ms-04-cuda` · weeks 35–46 · 16 sub-modules, 5 written · 15 exercises

**What it buys.** a kernel that beats the reference on a bounded case, gain reproducible with its standard deviation, and where it loses too

**How it ends.** Not on a feeling, on one binary test: *Tu produis une frise d'exécution et tu nommes le trou. Tu estimes avant de coder si un kernel sera compute- ou memory-bound.*

Descriptions below are the curriculum's own `competence` field, quoted verbatim and left in French; everything else on this page is not.

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
| `cu-10-battre` | proof | — | planned, not written yet |
| `cpp-06-exceptions` | added | Refuser par une exception qu'un objet invalide existe, traduire une exception en phrase là où elle se rattrape, et garantir qu'une sortie non locale ne laisse rien en vie | 42 subject, not published · 3 exercises |
| `cpp-07-casts` | added | Choisir entre static_cast, reinterpret_cast et dynamic_cast selon ce que chacun promet, lire un littéral et l'écrire dans quatre types en disant quand la conversion n'a pas de sens, et reconnaître le type réel derrière une base | 42 subject, not published · 3 exercises |
| `cpp-08-templates` | added | Écrire du code générique qui vaut pour tout type portant les opérations qu'il emploie, et un conteneur templaté qui copie en profondeur et refuse un indice hors bornes | 42 subject, not published · 3 exercises |
| `cpp-09-conteneurs` | added | Employer les conteneurs et les algorithmes de la bibliothèque standard au lieu de les réécrire, choisir la structure qui rend une question en N log N plutôt qu'en N², et étendre un conteneur par héritage sans casser ce qu'il est | 42 subject, not published · 3 exercises |
| `cpp-10-stl` | added | Choisir le conteneur qui rend une question en une recherche, écrire un programme complet qui lit, valide et refuse ses entrées, et implémenter un algorithme de tri décrit dans la littérature en comptant ses comparaisons | 42 subject, not published · 3 exercises |

---

← [ms-03-parallelisme](../ms-03-parallelisme) · [the roadmap](../README.md) · [ms-05-fin-tronc-commun](../ms-05-fin-tronc-commun) →
