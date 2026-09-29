"""maths-01-algebre ex00: vectors.

Statement:  ./exo maths-01-algebre ex00
Grade:      ./exo maths-01-algebre ex00 -c
Allowed:    isinstance iter len list sum zip
"""


class ErreurDeShape(ValueError):
    """Raised whenever two sizes do not fit together."""
    pass


class Vecteur:

    def __init__(self, nombres):
        # Store a copy of the list in self.nombres.
        # On utilise list() pour s'assurer que l'on stocke une copie indépendante.
        self.nombres = list(nombres)

    def __repr__(self):
        # Retourne une chaîne de caractères sous la forme Vecteur([3, -1])
        return f"Vecteur({self.nombres})"

    def __eq__(self, other):
        # Same numbers. NotImplemented for any other type.
        if not isinstance(other, Vecteur):
            return NotImplemented
        return self.nombres == other.nombres

    def __len__(self):
        # Retourne la taille du vecteur
        return len(self.nombres)

    def __getitem__(self, index):
        # Permet l'accès aux éléments via vecteur[i]
        return self.nombres[index]

    def __iter__(self):
        # Permet l'itération (ex: for x in vecteur)
        return iter(self.nombres)

    def __add__(self, other):
        # A new Vecteur. ErreurDeShape when the sizes differ.
        # On vérifie d'abord si other est bien un Vecteur pour éviter une AttributeError
        if not isinstance(other, Vecteur):
            return NotImplemented
        
        if len(self) != len(other):
            raise ErreurDeShape
            
        return Vecteur([a + b for a, b in zip(self.nombres, other.nombres)])

    def __sub__(self, other):
        # A new Vecteur. ErreurDeShape when the sizes differ.
        if not isinstance(other, Vecteur):
            return NotImplemented
            
        if len(self) != len(other):
            raise ErreurDeShape
            
        return Vecteur([a - b for a, b in zip(self.nombres, other.nombres)])

    def __mul__(self, scalar):
        # int or float only. NotImplemented for anything else.
        if not isinstance(scalar, (int, float)):
            return NotImplemented
            
        return Vecteur([x * scalar for x in self.nombres])

    def __rmul__(self, scalar):
        # Gère le cas où le scalaire est à gauche (ex: 3 * Vecteur(...))
        # On délègue simplement à __mul__ car la multiplication est commutative.
        return self.__mul__(scalar)

    def __matmul__(self, other):
        # The dot product. ErreurDeShape when the sizes differ.
        if not isinstance(other, Vecteur):
            return NotImplemented
            
        if len(self) != len(other):
            raise ErreurDeShape
            
        # Le produit scalaire est la somme des produits deux à deux
        return sum(a * b for a, b in zip(self.nombres, other.nombres))