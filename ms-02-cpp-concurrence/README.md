<!-- Généré par carte_phases.py. Ne pas éditer à la main. -->

# Phase 3 — C++ and concurrency

`ms-02-cpp-concurrence` · weeks 9–20 · 20 sub-modules, 20 written · 60 exercises

**What it buys.** concurrent code whose freedom from starvation is shown by measurement, and an unknown execution timeline read in ten minutes

**How it ends.** Not on a feeling, on one binary test: *Tu lis une frise Nsight inconnue et tu nommes le trou en dix minutes.*

Descriptions below are the curriculum's own `competence` field, quoted verbatim and left in French; everything else on this page is not.

| Sub-module | Layer | What it covers | Where the work is |
|---|---|---|---|
| `t42-01-piscine-python` | imposed | Valider la piscine Python du cursus au plus vite, le contenu étant déjà acquis: la sortie exacte, l'erreur exacte, le docstring exact, sur les motifs que la moulinette corrige | 42 subject, not published · 3 exercises |
| `t42-02-amazeing` | imposed | Livrer un projet au périmètre du sujet, sans rien ajouter: une configuration lue et refusée en nommant la cause, un labyrinthe parfait ou non aux murs cohérents, un chemin le plus court, une graine qui reproduit | 42 subject, not published · 3 exercises |
| `sh-01-b2br` | imposed | Administrer une machine durcie, du partitionnement chiffré à la politique de mots de passe, et savoir défendre chaque choix: les fichiers de configuration du sujet rendus et lus, et le script de surveillance exécuté sur des doublures de commandes | 42 subject, not published · 5 exercises |
| `mth-03-probas` | added | Simuler une loi, la confronter à sa formule close, et savoir combien de mesures il faut pour distinguer deux valeurs | not started · 6 exercises |
| `mth-04-statistiques` | added | Juger si deux séries de mesures diffèrent vraiment, en connaissant la fréquence à laquelle on se trompera | not started · 6 exercises |
| `cpp-00-classes` | added | Écrire une classe avec ce qu'elle cache et ce qu'elle montre, tenir un état partagé par des membres statiques, et lire et écrire par les flux du langage jusqu'à un programme interactif qui ne tombe jamais | 42 subject, not published · 3 exercises |
| `cpp-01-allocation` | added | Choisir entre la pile et le tas et le dire par le code, distinguer une référence d'un pointeur par ce que chacun promet, et viser une méthode par un pointeur sur membre | 42 subject, not published · 3 exercises |
| `cpp-02-canonique` | added | Poser les quatre membres que le langage appelle sans qu'on les écrive, surcharger les opérateurs sans surprise pour l'appelant, et représenter un nombre à virgule fixe sans un flottant en mémoire | 42 subject, not published · 3 exercises |
| `cpp-03-heritage` | added | Dériver une classe, savoir dans quel ordre construction et destruction s'enchaînent, et faire tenir un héritage en diamant sur une seule base | 42 subject, not published · 3 exercises |
| `cpp-04-polymorphisme` | added | Employer les fonctions virtuelles pour que l'objet décide et non le pointeur, rendre les destructeurs virtuels, écrire une classe abstraite et des interfaces, et copier en profondeur sans jamais partager ni fuir | 42 subject, not published · 3 exercises |
| `cpp-05-vector-asm` | added | Lire dans l'assembleur produit par le compilateur ce qu'une réallocation de std::vector coûte réellement, allocation, copie et libération, et dire d'avance quand elle survient et comment l'éviter | not started · 2 exercises |
| `c-07-threadpool` | added | Écrire une file protégée par un mutex et des variables de condition, des fils qui la consomment, et un arrêt qui n'oublie aucune tâche, en le prouvant sous ThreadSanitizer et sous charge | not started · 3 exercises |
| `c-08-contention` | added | Mesurer ce qu'un verrou coûte quand le nombre de fils monte, sur un compteur d'abord juste, puis sur trois stratégies dont la courbe dit laquelle partage quoi | not started · 2 exercises |
| `c-09-philosophers` | added | Écrire un programme concurrent sans interblocage ni famine, où une mort s'annonce dans les dix millisecondes et où aucune ligne ne sort après elle, et le prouver par le journal et sous ThreadSanitizer | 42 subject, not published · 3 exercises |
| `c-10-famine` | added | Démontrer l'absence de famine par la distribution mesurée des délais entre repas, et non par un raisonnement sur la stratégie | not started · 2 exercises |
| `par-01-regimes` | added | Nommer les trois régimes d'un calcul, borné par la mémoire, par le calcul ou par la surcharge, et en donner un exemple mesuré de chacun contre les plafonds de la machine | not started · 1 exercise |
| `par-02-predire` | added | Prédire le régime de chaque couche d'un modèle à partir de ses flops et de ses octets avant toute mesure, puis confronter la prédiction aux mesures en nommant chaque désaccord et chaque lenteur | not started · 1 exercise |
| `par-03-nsight` | added | Lire la frise d'exécution d'une génération complète au format des profileurs, en tirer les grandeurs qu'un œil ne voit pas, taux d'occupation du GPU, latence de lancement, taille médiane d'un kernel, et la dessiner pour que l'œil voie le reste | not started · 1 exercise |
| `par-04-trou` | added | Trouver dans une frise les périodes où le GPU ne fait rien, à leurs bornes, et nommer la cause de chacune d'après ce qui l'occupe: une copie, une synchronisation, du calcul sur l'hôte, ou rien, ce qui veut dire hors trace | not started · 1 exercise |
| `l3-01-profil` | proof | Publier le profil d'exécution d'un serveur d'inférence, périmètre lu dans la frise, frise annotée, prédiction confrontée, diagnostic qui nomme une limite physique par une règle écrite, et comparaison avec le binôme, puis lire une frise inconnue et nommer son trou en un appel | not started · 6 exercises |

---

← [ms-01-inference](../ms-01-inference) · [the roadmap](../README.md) · [ms-03-parallelisme](../ms-03-parallelisme) →
