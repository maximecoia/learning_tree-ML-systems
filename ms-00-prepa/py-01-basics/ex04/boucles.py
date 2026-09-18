def somme_jusqu_a(n):
    total = 0
    for i in range(n):
        total += i
    return total


def compter_valides(lignes):
    compteur = 0
    for ligne in lignes:
        morceaux = ligne.split(":")
        if len(morceaux) == 2 and morceaux[0].strip() != "" and morceaux[1].strip().isdigit():
            compteur += 1
    return compteur


def plus_grande(valeurs):
    if len(valeurs) == 0:
        return -1

    indice_max = 0

    for i, valeur in enumerate(valeurs):
        if valeur > valeurs[indice_max]:
            indice_max = i

    return indice_max


def premiere_vide(lignes):
    for i, ligne in enumerate(lignes):
        if ligne == "":
            return i
    return -1
    

print(somme_jusqu_a(4))
print(somme_jusqu_a(0))
print(compter_valides(["alice: 14", "", "carol: abc", "bob: 8"]))
print(compter_valides([]))
print(plus_grande([3, 9, 9, 1]))
print(plus_grande([]))
print(premiere_vide(["a", "", "b", ""]))
print(premiere_vide(["a", "b"]))