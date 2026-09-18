def grouper(paires):
    par_nom = {}
    for nom, note in paires:
        if nom not in par_nom:
            par_nom[nom] = []
        par_nom[nom].append(note)
    return par_nom


def moyennes(par_nom):
    resultat = {}
    for nom, notes in par_nom.items():
        if notes:
            resultat[nom] = round(sum(notes) / len(notes), 2)
    return resultat


def compter_mots(mots):
    compteur = {}
    for mot in mots:
        compteur[mot] = compteur.get(mot, 0) + 1
    return compteur


def valeur_ou(d, cle, defaut):
    return d.get(cle, defaut)

print(grouper([("alice", 14), ("bob", 9), ("alice", 17)]))
print(grouper([]))
print(moyennes({"alice": [14, 17], "bob": [9]}))
print(moyennes({"vide": [], "k": [7]}))
print(compter_mots(["a", "b", "a"]))
print(valeur_ou({"a": 1}, "a", 0))
print(valeur_ou({"a": 1}, "b", 0))