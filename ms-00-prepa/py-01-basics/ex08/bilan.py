def bilan(lignes, minimum=0):
    par_nom = {}
    meilleur = None
    ignorees = 0

    for ligne in lignes:
        morceaux = ligne.split(":")

        if len(morceaux) != 2 or morceaux[0].strip() == "" or not morceaux[1].strip().isdigit():
            ignorees += 1
            continue

        nom = morceaux[0].strip().lower()
        note = int(morceaux[1].strip())

        if note < minimum:
            continue

        if nom not in par_nom:
            par_nom[nom] = []

        par_nom[nom].append(note)

        if meilleur is None or note > meilleur[1]:
            meilleur = (nom, note)

    moyennes = {}

    for nom, notes in par_nom.items():
        moyennes[nom] = round(sum(notes) / len(notes), 2)

    return moyennes, meilleur, ignorees

print(bilan(["alice: 14", "bob: 9", "alice: 17"]))
print(bilan([" Bob : 12 ", "", "carol: abc", "bob: 8"], minimum=10))
print(bilan(["dan: 10", "eve: 10"]))
print(bilan([]))