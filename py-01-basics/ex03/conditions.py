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

print(categorie(16))
print(categorie(12))
print(categorie(10))
print(categorie(9))
print(signe(-2))
print(signe(0))
print(est_vide([]))
print(est_vide([0]))
print(est_valide(["alice", " 14"]))
print(est_valide(["a", "b", "c"]))
print(est_valide(["   ", "12"]))
print(est_valide(["bob", "-3"]))