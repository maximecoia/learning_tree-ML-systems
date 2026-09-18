import argparse
import sys


def lire(lignes):
    mesures = []

    for ligne in lignes:
        ligne = ligne.strip()

        if ligne == "":
            continue

        if ligne[0] == "#":
            continue

        nom, separateur, reste = ligne.partition(":")

        if separateur == "":
            continue

        nom = nom.strip().lower()

        if nom == "":
            continue

        morceaux = reste.split()

        if len(morceaux) == 0 or len(morceaux) > 2:
            continue

        try:
            valeur = float(morceaux[0])
        except ValueError:
            continue

        unite = ""

        if len(morceaux) == 2:
            unite = morceaux[1]

        mesures.append((nom, valeur, unite))

    return mesures


def centile95(valeurs):
    triees = sorted(valeurs)
    n = len(triees)
    rang = (95 * n + 99) // 100

    return triees[rang - 1]


def resumer(mesures):
    groupes = {}

    for nom, valeur, unite in mesures:
        if nom not in groupes:
            groupes[nom] = {
                "valeurs": [],
                "unite": unite,
            }

        groupes[nom]["valeurs"].append(valeur)

    lignes = []

    for nom in sorted(groupes):
        valeurs = groupes[nom]["valeurs"]
        unite = groupes[nom]["unite"]

        moyenne = sum(valeurs) / len(valeurs)
        p95 = centile95(valeurs)

        ligne = (
            f"{nom} n={len(valeurs)} "
            f"moy={moyenne:.2f} "
            f"p95={p95:.2f}"
        )

        if unite != "":
            ligne += f" {unite}"

        lignes.append(ligne)

    return lignes


def analyser(argv):
    p = argparse.ArgumentParser(
        prog="releve",
        description="Résumer un relevé.",
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


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = analyser(argv)

    with open(args.fichier) as fichier:
        mesures = lire(fichier)

    if args.commande == "compter":
        print(len(mesures), "mesures")

    if args.commande == "resume":
        if args.nom is not None:
            mesures = [
                mesure
                for mesure in mesures
                if mesure[0] == args.nom
            ]

        for ligne in resumer(mesures):
            print(ligne)


if __name__ == "__main__":
    main()