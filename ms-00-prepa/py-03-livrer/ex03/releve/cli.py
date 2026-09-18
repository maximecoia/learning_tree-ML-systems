import argparse
import sys

# Import relatif :
# "mesures" désigne le module voisin dans le package releve.
from .mesures import depouiller, resumer


def analyser(argv):
    # Ce module est responsable de l'interface en ligne de commande.
    p = argparse.ArgumentParser(
        prog="releve",
        description="Résumer un relevé.",
    )

    p.add_argument(
        "--strict",
        action="store_true",
    )

    sous = p.add_subparsers(
        dest="commande",
        required=True,
    )

    compter = sous.add_parser(
        "compter",
        help="compter les mesures",
    )
    compter.add_argument("fichier")

    resume = sous.add_parser(
        "resume",
        help="résumer par nom",
    )
    resume.add_argument("fichier")
    resume.add_argument("--nom", default=None)

    return p.parse_args(argv)


def traiter(args, flux):
    # La CLI délègue le parsing réel des données à mesures.py.
    mesures, numeros_illisibles = depouiller(flux)

    if args.strict and len(numeros_illisibles) > 0:
        if args.fichier == "-":
            origine = "entrée standard"
        else:
            origine = args.fichier

        print(
            f"releve: {origine}:{numeros_illisibles[0]}: ligne illisible",
            file=sys.stderr,
        )
        return 1

    if args.commande == "compter":
        print(len(mesures), "mesures")
        return 0

    if args.commande == "resume":
        if args.nom is not None:
            mesures = [
                mesure
                for mesure in mesures
                if mesure[0] == args.nom
            ]

        for ligne in resumer(mesures):
            print(ligne)

        return 0

    return 0


def main(argv=None):
    # main orchestre uniquement la CLI :
    # analyse des arguments, choix du flux, puis traitement.
    if argv is None:
        argv = sys.argv[1:]

    args = analyser(argv)

    # "-" représente l'entrée standard.
    if args.fichier == "-":
        return traiter(args, sys.stdin)

    try:
        with open(args.fichier, encoding="utf-8") as fichier:
            return traiter(args, fichier)

    except OSError:
        print(
            f"releve: {args.fichier}: fichier introuvable",
            file=sys.stderr,
        )
        return 1