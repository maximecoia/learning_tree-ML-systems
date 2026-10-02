from time import perf_counter

from chrono import mesurer, duree_lisible
from bruit import resumer


def mesurer_tous(candidats, repetitions=5, echauffement=1, horloge=perf_counter):
    if len(candidats) == 0:
        raise ValueError("aucun candidat a mesurer")
    if repetitions < 1:
        raise ValueError("il faut au moins une repetition")
    if echauffement < 0:
        raise ValueError("l'echauffement ne peut pas etre negatif")
    mesures = {}
    for nom in candidats:
        mesures[nom] = []
    for _ in range(echauffement):
        for nom in candidats:
            candidats[nom]()
    for _ in range(repetitions):
        for nom in candidats:
            mesures[nom].append(mesurer(candidats[nom], horloge))
    resumes = {}
    for nom in candidats:
        resumes[nom] = resumer(mesures[nom])
    return resumes


def rapport(candidats, repetitions=5, echauffement=1, horloge=perf_counter):
    resumes = mesurer_tous(candidats, repetitions, echauffement, horloge)
    classes = sorted(resumes.items(), key=lambda item: item[1]['min'])
    lignes = []
    for nom, r in classes:
        lignes.append(f"{nom} {duree_lisible(r['min'])} (n={r['n']}, écart {duree_lisible(r['ecart'])})")
    if len(classes) == 1:
        lignes.append("un seul candidat: rien à comparer")
    else:
        nom_p, p = classes[0]
        nom_s, s = classes[1]
        if p['min'] + p['ecart'] >= s['min']:
            lignes.append(f"indécidable: {nom_p} et {nom_s} se recouvrent")
        else:
            lignes.append(f"{nom_p} devance {nom_s} de {s['min'] / p['min']:.2f}×")
    return "\n".join(lignes)