# releve

`releve` est un petit outil en ligne de commande qui lit un relevé de mesures, compte les mesures valides et produit un résumé statistique par nom.

## Installation

Depuis la racine du projet, installer l'outil avec `pip install .`.

Une fois installé, la commande `releve` est disponible dans le PATH.

## Utilisation

`releve compter FICHIER` compte les mesures valides.

`releve resume FICHIER` affiche un résumé par nom de mesure.

`releve resume FICHIER --nom NOM` limite le résumé au nom demandé.

Le chemin `-` permet de lire depuis l'entrée standard.

L'option globale `--strict` fait échouer le traitement lorsqu'une ligne de données est illisible.

`releve --version` affiche la version installée.

## Exemple

```
$ python3 -m releve resume exemple.txt
debit n=1 moy=880.00 p95=880.00 req/s
latence n=3 moy=17.67 p95=31.00 ms
```

## Développement

Créer un environnement virtuel avec `python3 -m venv .venv`, puis l'activer.

Installer les outils de développement avec `pip install -r requirements-dev.txt`.

Lancer les tests avec `python3 -m unittest test_releve`.

Le fichier `requirements.txt` décrit les dépendances d'exécution. Le projet utilise actuellement uniquement la bibliothèque standard Python.
