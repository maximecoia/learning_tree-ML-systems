def moyenne_de_deux(a, b): 
    return (a + b) / 2

def division_entiere(a, b): 
    return a // b

def reste(a, b): return a % b

def puissance(base, exposant): 
    return base ** exposant

def ecart(a, b): 
    return abs(a - b)

def pourcentage(partie, total): 
    return round(partie / total * 100, 2)

print(moyenne_de_deux(3, 4))
print(moyenne_de_deux(4, 4))
print(division_entiere(7, 2))
print(division_entiere(-7, 2))
print(reste(7, 2))
print(reste(-7, 2))
print(puissance(2, 10))
print(puissance(9, 0.5))
print(ecart(3, 10))
print(ecart(10, 3))
print(pourcentage(1, 3))
print(pourcentage(14, 20))