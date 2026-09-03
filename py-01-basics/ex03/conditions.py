def categorie(note):
    if note >= 16:
        return "excellent"
    elif note >= 12:
        return "bien"
    elif note >= 10:
        return "passable"
    else:
        return "insuffisant"

def signe(n):
    if n > 0:
        return "positif"
    elif n < 0:
        return "negatif"
    else:
        return "nul"

def est_vide(valeur):
    return not valeur

def est_valide(morceaux):
    return len(morceaux) == 2 and morceaux[0].strip() != "" and morceaux[1].strip().isdigit()