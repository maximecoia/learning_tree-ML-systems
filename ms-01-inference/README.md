<!-- Généré par carte_phases.py. Ne pas éditer à la main. -->

# Phase 2 — Graded C, measured inference

`ms-01-inference` · weeks 1–8 · 18 sub-modules, 18 written · 70 exercises

**What it buys.** produce the saturation curve of an unknown inference server in half a day

**How it ends.** Not on a feeling, on one binary test: *On te donne un serveur d'inférence inconnu. Tu produis sa courbe de saturation en une demi-journée.*

Descriptions below are the curriculum's own `competence` field, quoted verbatim and left in French; everything else on this page is not.

| Sub-module | Layer | What it covers | Where the work is |
|---|---|---|---|
| `c-03-libft-norme` | imposed | Rendre un dépôt C conforme à une norme imposée, revoir chaque chemin de retour nul et chaque libération, et le garder derrière un harnais de test personnel qui sait échouer | 42 subject, not published · 3 exercises |
| `c-04-printf` | imposed | Écrire un formateur variadique dont la sortie est identique à celle de la libc, conversion par conversion | 42 subject, not published · 3 exercises |
| `c-05-gnl` | imposed | Lire un flux ligne par ligne avec un état qui survit entre les appels, sur plusieurs descripteurs et sans fuite | 42 subject, not published · 3 exercises |
| `c-06-pushswap` | imposed | Trier sous un jeu d'opérations contraint et défendre le coût réel de l'algorithme par la mesure | 42 subject, not published · 5 exercises |
| `mth-02-derivees` | added | Calculer un gradient à la main, et prouver qu'il est juste en le comparant à la mesure | not started · 6 exercises |
| `mth-05-optimisation` | added | Régler une descente de gradient en sachant ce que chaque réglage coûte, et reconnaître un point d'arrêt qui n'est pas un minimum | not started · 6 exercises |
| `mes-01-chronometre` | added | Chronométrer une fonction sans se laisser tromper par le bruit et l'échauffement | not started · 7 exercises |
| `mes-02-grandeurs` | added | Estimer un ordre de grandeur de calcul, de mémoire et de coût avant de coder | not started · 3 exercises |
| `mes-03-profiler` | added | Localiser dans un programme lent la fonction qui coûte, et prouver que la corriger a servi | not started · 6 exercises |
| `pt-01-autograd` | added | Refaire en tenseurs ce qui a été écrit à la main dans micrograd, retrouver les mêmes gradients à 1e-6 près, et dire à chaque écart s'il vient du calcul ou du framework | not started · 3 exercises |
| `pt-02-gpt` | added | Réécrire son transformeur au format idiomatique du framework, nn.Module, Dataset, DataLoader et checkpoints, et retrouver le même nombre de paramètres, les mêmes lots à graine fixée et la même perte finale à 2 % près | not started · 3 exercises |
| `inf-01-servir` | added | Interroger un moteur d'inférence par son API, relever sa latence selon un protocole écrit, et comparer deux moteurs sans conclure au-delà de ce que la mesure permet | not started · 3 exercises |
| `inf-02-prefill-decode` | added | Séparer par la mesure les deux régimes d'une génération, en tirer un modèle de coût, et s'en servir pour prédire la latence d'une requête jamais mesurée | not started · 3 exercises |
| `inf-03-cache-kv` | added | Chiffrer ce que le cache des clés et valeurs économise en temps et ce qu'il coûte en mémoire, reconnaître à la mesure un moteur qui en est privé, et dire à partir de quel contexte c'est lui, et non les poids, qui plafonne la concurrence | not started · 3 exercises |
| `inf-04-quantifier` | added | Mesurer la qualité d'un modèle par sa perplexité sur un corpus fixe, mesurer ce qu'une précision réduite fait gagner en décodage sans rien faire gagner en prefill, et trancher entre les deux avec un budget posé d'avance | not started · 4 exercises |
| `inf-05-harnais` | added | Tenir N requêtes en vol contre un serveur d'inférence, relever débit, percentiles et taux de refus sans qu'aucun des trois pièges ne fausse le chiffre, et produire un CSV depuis lequel le graphe se régénère | not started · 3 exercises |
| `inf-06-saturation` | added | Balayer la concurrence d'un serveur d'inférence jusqu'au décrochage, situer ce point par une règle dite d'avance, et nommer la limite physique qui le fixe avec les chiffres qui la prouvent | not started · 3 exercises |
| `l2-01-courbe` | proof | Livrer publiquement la courbe débit et latence d'un serveur d'inférence, avec son protocole, son point de décrochage et la limite physique qui le fixe, et la défendre sans le code sous les yeux | not started · 3 exercises |

---

← [ms-00-prepa](../ms-00-prepa) · [the roadmap](../README.md) · [ms-02-cpp-concurrence](../ms-02-cpp-concurrence) →
