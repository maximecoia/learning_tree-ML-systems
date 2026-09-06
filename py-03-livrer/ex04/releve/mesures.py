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