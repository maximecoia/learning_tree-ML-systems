class MontantInvalide(ValueError):
    pass


class LigneInvalide(ValueError):
    pass


class Montant:
    def __init__(self, centimes):
        if not isinstance(centimes, int) or centimes < 0:
            raise MontantInvalide("montant invalide")
        self.centimes = centimes

    @property
    def euros(self):
        return self.centimes / 100

    @property
    def est_nul(self):
        return self.centimes == 0

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

    @classmethod
    def depuis_euros(cls, euros):
        return cls(round(euros * 100))

    @staticmethod
    def est_texte_valide(texte):
        morceaux = texte.strip().split(",")

        if len(morceaux) == 1:
            return morceaux[0].isdigit()

        if len(morceaux) == 2:
            return (
                morceaux[0].isdigit()
                and morceaux[1].isdigit()
                and len(morceaux[1]) == 2
            )

        return False

    @classmethod
    def depuis_texte(cls, texte):
        if not cls.est_texte_valide(texte):
            raise MontantInvalide("montant invalide")

        morceaux = texte.strip().split(",")
        euros = int(morceaux[0])
        centimes = 0

        if len(morceaux) == 2:
            centimes = int(morceaux[1])

        return cls(euros * 100 + centimes)


def tries(montants):
    return sorted(montants)


def le_plus_grand(montants):
    if not montants:
        return None
    return max(montants)


def montant_ou_zero(texte):
    try:
        return Montant.depuis_texte(texte)
    except MontantInvalide:
        return Montant(0)


class Ligne:
    def __init__(self, article, quantite, prix):
        if not isinstance(quantite, int) or quantite < 1:
            raise LigneInvalide("quantite invalide")

        if not isinstance(prix, Montant):
            raise LigneInvalide("prix invalide")

        self.article = article
        self.quantite = quantite
        self.prix = prix

    @property
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
            self.prix,
        ) == (
            autre.article,
            autre.quantite,
            autre.prix,
        )

    def __lt__(self, autre):
        if not isinstance(autre, Ligne):
            return NotImplemented
        return self.total < autre.total

    @classmethod
    def depuis_texte(cls, texte):
        morceaux = texte.split(":")

        if len(morceaux) != 2:
            raise LigneInvalide("ligne invalide")

        article = morceaux[0].strip().lower()

        if article == "":
            raise LigneInvalide("ligne invalide")

        droite = morceaux[1].split("x")

        if len(droite) != 2:
            raise LigneInvalide("ligne invalide")

        quantite_texte = droite[0].strip()

        if not quantite_texte.isdigit():
            raise LigneInvalide("ligne invalide")

        quantite = int(quantite_texte)

        try:
            prix = Montant.depuis_texte(droite[1])
        except MontantInvalide:
            raise LigneInvalide("ligne invalide")

        return cls(article, quantite, prix)


def total_des_lignes(lignes):
    return sum((ligne.total for ligne in lignes), Montant(0))


class Facture:
    def __init__(self):
        self.lignes = {}

    def ajouter(self, ligne):
        article = ligne.article

        if article not in self.lignes:
            self.lignes[article] = ligne
            return

        ancienne = self.lignes[article]

        if ancienne.prix != ligne.prix:
            raise ValueError("prix différent")

        self.lignes[article] = Ligne(
            article,
            ancienne.quantite + ligne.quantite,
            ancienne.prix,
        )

    def __len__(self):
        return len(self.lignes)

    def __iter__(self):
        return iter(self.lignes.values())

    def __getitem__(self, article):
        return self.lignes[article]

    def __contains__(self, article):
        return article in self.lignes

    @property
    def total(self):
        return sum((ligne.total for ligne in self), Montant(0))


class LigneRemisee(Ligne):
    def __init__(self, article, quantite, prix, remise):
        super().__init__(article, quantite, prix)

        if not isinstance(remise, int) or remise < 0 or remise > 100:
            raise LigneInvalide("remise invalide")

        self.remise = remise

    @property
    def total(self):
        centimes = (
            super().total.centimes
            * (100 - self.remise)
            // 100
        )

        return Montant(centimes)

    def __repr__(self):
        return (
            f"LigneRemisee("
            f"{self.article!r}, "
            f"{self.quantite}, "
            f"{self.prix!r}, "
            f"{self.remise})"
        )