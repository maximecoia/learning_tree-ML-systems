import argparse
import sys


def depouiller(lignes):
    mesures = []
    numeros_illisibles = []

    for numero, ligne in enumerate(lignes, start=1):
        ligne = ligne.strip()

        if ligne == "":
            continue

        if ligne[0] == "#":
            continue

        nom, separateur, reste = ligne.partition(":")

        if separateur == "":
            numeros_illisibles.append(numero)
            continue

        nom = nom.strip().lower()

        if nom == "":
            numeros_illisibles.append(numero)
            continue

        morceaux = reste.split()

        if len(morceaux) == 0 or len(morceaux) > 2:
            numeros_illisibles.append(numero)
            continue

        try:
            valeur = float(morceaux[0])
        except ValueError:
            numeros_illisibles.append(numero)
            continue

        unite = ""

        if len(morceaux) == 2:
            unite = morceaux[1]

        mesures.append((nom, valeur, unite))

    return mesures, numeros_illisibles


def lire(lignes):
    return depouiller(lignes)[0]


def illisibles(lignes):
    return depouiller(lignes)[1]


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
    if argv is None:
        argv = sys.argv[1:]

    args = analyser(argv)

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


if __name__ == "__main__":
    sys.exit(main())