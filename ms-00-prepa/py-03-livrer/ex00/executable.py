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


if __name__ == "__main__":
    print(len(lire(sys.stdin)), "mesures")