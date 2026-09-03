def entier(texte): 
    return int(texte)

def flottant(texte): 
    return float(texte)

def texte(valeur): 
    return str(valeur)

def est_entier(valeur): 
    return type(valeur) == int

print(entier("14"))
print(entier("007"))
print(flottant("14"))
print(flottant("2.5"))
print(texte(14))
print(texte(2.5))
print(est_entier(14))
print(est_entier(14.0))