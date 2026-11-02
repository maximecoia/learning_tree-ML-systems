def nettoyer(texte): 
    return texte.strip().lower()

def est_note(texte): 
    return texte.strip().isdigit()

def morceaux(ligne): 
    return ligne.split(":")

def contient(texte, morceau): 
    return morceau in texte


if __name__ == "__main__":
    print(nettoyer(" Bob "))
    print(est_note(" 12 "))
    print(est_note("-3"))
    print(est_note(""))
    print(morceaux("nom: 12"))
    print(morceaux("a:b:c"))
    print(contient("bob: 12", ":"))
    print(contient("bob", "alice"))
