class Montant:
    def __init__(self, centimes):
        if not isinstance(centimes, int) or centimes < 0:
            raise ValueError("montant invalide")
        self.centimes = centimes

    def en_euros(self):
        return self.centimes / 100

    def __repr__(self):
        return f"Montant({self.centimes})"

    def texte(self):
        euros = self.centimes // 100
        centimes = self.centimes % 100
        return f"{euros},{centimes:02d} €"

    def __eq__(self, autre):
        if not isinstance(autre, Montant):
            return NotImplemented
        return self.centimes == autre.centimes

    def __lt__(self, autre):
        if not isinstance(autre, Montant):
            return NotImplemented
        return self.centimes < autre.centimes

    def __add__(self, autre):
        if not isinstance(autre, Montant):
            return NotImplemented
        return Montant(self.centimes + autre.centimes)

    def __sub__(self, autre):
        if not isinstance(autre, Montant):
            return NotImplemented
        return Montant(self.centimes - autre.centimes)

    def __mul__(self, n):
        if not isinstance(n, int):
            return NotImplemented
        return Montant(self.centimes * n)

    def __rmul__(self, n):
        return self.__mul__(n)


def tries(montants):
    return sorted(montants)


def le_plus_grand(montants):
    if not montants:
        return None
    return max(montants)


class Ligne:
    def __init__(self, article, quantite, prix):
        if not isinstance(quantite, int) or quantite < 1:
            raise ValueError("quantite invalide")
        if not isinstance(prix, Montant):
            raise ValueError("prix invalide")

        self.article = article
        self.quantite = quantite
        self.prix = prix

    def total(self):
        return self.quantite * self.prix

    def __repr__(self):
        return f"Ligne({self.article!r}, {self.quantite}, {self.prix!r})"

    def __eq__(self, autre):
        if not isinstance(autre, Ligne):
            return NotImplemented
        return (
            self.article,
            self.quantite,
            self.prix
        ) == (
            autre.article,
            autre.quantite,
            autre.prix
        )

    def __lt__(self, autre):
        if not isinstance(autre, Ligne):
            return NotImplemented
        return self.total() < autre.total()


def total_des_lignes(lignes):
    return sum((ligne.total() for ligne in lignes), Montant(0))