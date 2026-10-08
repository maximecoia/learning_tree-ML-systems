"""mth-01-algebre ex04: the inverse and linear systems.

Statement:  ./exo mth-01-algebre ex04
Grade:      ./exo mth-01-algebre ex04 -c
Allowed:    isinstance iter len list range sum zip abs all ValueError
"""

# --- carried over from ex03/determinant.py ----------------------------------
class ErreurDeShape(ValueError):
    """Raised whenever two sizes do not fit together."""
    pass


class Vecteur:

    def __init__(self, nombres):
        self.nombres = list(nombres)

    def __repr__(self):
        return f"Vecteur({self.nombres})"

    def __eq__(self, other):
        if not isinstance(other, Vecteur):
            return NotImplemented
        return self.nombres == other.nombres

    def __len__(self):
        return len(self.nombres)

    def __getitem__(self, index):
        return self.nombres[index]

    def __iter__(self):
        return iter(self.nombres)

    def __add__(self, other):
        if not isinstance(other, Vecteur):
            return NotImplemented
        if len(self) != len(other):
            raise ErreurDeShape
        return Vecteur([a + b for a, b in zip(self.nombres, other.nombres)])

    def __sub__(self, other):
        if not isinstance(other, Vecteur):
            return NotImplemented
        if len(self) != len(other):
            raise ErreurDeShape
        return Vecteur([a - b for a, b in zip(self.nombres, other.nombres)])

    def __mul__(self, scalar):
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vecteur([x * scalar for x in self.nombres])

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __matmul__(self, other):
        if not isinstance(other, Vecteur):
            return NotImplemented
        if len(self) != len(other):
            raise ErreurDeShape
        return sum(a * b for a, b in zip(self.nombres, other.nombres))


class Matrice:

    def __init__(self, lignes):
        self.lignes = [list(ligne) for ligne in lignes]
        
        if not self.lignes:
            raise ErreurDeShape
        if not self.lignes[0]:
            raise ErreurDeShape
            
        nb_colonnes = len(self.lignes[0])
        for ligne in self.lignes:
            if len(ligne) != nb_colonnes:
                raise ErreurDeShape

    def __repr__(self):
        return f"Matrice({self.lignes})"

    def __eq__(self, other):
        if not isinstance(other, Matrice):
            return NotImplemented
        return self.lignes == other.lignes

    def __getitem__(self, index):
        return Vecteur(self.lignes[index])

    @property
    def shape(self):
        return (len(self.lignes), len(self.lignes[0]))

    def colonnes(self):
        return [Vecteur(col) for col in zip(*self.lignes)]

    @classmethod
    def depuis_colonnes(cls, colonnes):
        if not colonnes:
            raise ErreurDeShape
            
        taille = len(colonnes[0])
        for v in colonnes:
            if len(v) != taille:
                raise ErreurDeShape
                
        return cls(zip(*colonnes))

    def __matmul__(self, other):
        if isinstance(other, Vecteur):
            if self.shape[1] != len(other):
                raise ErreurDeShape
            return Vecteur([Vecteur(ligne) @ other for ligne in self.lignes])
            
        if isinstance(other, Matrice):
            if self.shape[1] != other.shape[0]:
                raise ErreurDeShape
                
            colonnes_other = other.colonnes()
            nouvelles_lignes = []
            for ligne in self.lignes:
                v_ligne = Vecteur(ligne)
                nouvelle_ligne = [v_ligne @ col for col in colonnes_other]
                nouvelles_lignes.append(nouvelle_ligne)
                
            return Matrice(nouvelles_lignes)
            
        return NotImplemented

    @classmethod
    def identite(cls, n):
        return cls([[1 if i == j else 0 for j in range(n)] for i in range(n)])

    def puis(self, suivante):
        return suivante @ self

    @property
    def det(self):
        # Check if the matrix is 2x2
        if self.shape != (2, 2):
            raise ErreurDeShape
        
        # Formula: a*d - b*c
        a = self.lignes[0][0]
        b = self.lignes[0][1]
        c = self.lignes[1][0]
        d = self.lignes[1][1]
        
        return a * d - b * c

    @property
    def facteur_aire(self):
        # The area scaling factor is the absolute value of the determinant
        return abs(self.det)

    @property
    def renverse_orientation(self):
        # Orientation is reversed if the determinant is strictly negative
        return self.det < 0

    @property
    def est_singuliere(self):
        # A matrix is singular if its determinant is zero
        return self.det == 0

    # --- new in ex04 ---------------------------------------------------------

    def inverse(self):
        # The determinant property handles the 2x2 shape check and raises ErreurDeShape if needed
        det_val = self.det
        
        # Raise ValueError if the matrix is singular (determinant is 0)
        if det_val == 0:
            raise ValueError
            
        a = self.lignes[0][0]
        b = self.lignes[0][1]
        c = self.lignes[1][0]
        d = self.lignes[1][1]
        
        # Formula for the inverse of a 2x2 matrix: (1/det) * [[d, -b], [-c, a]]
        return Matrice([
            [d / det_val, -b / det_val],
            [-c / det_val, a / det_val]
        ])

    def resoudre(self, b):
        # Solve Av = b using the inverse: v = A^-1 @ b
        # If the matrix is singular, self.inverse() will raise ValueError
        return self.inverse() @ b

    @property
    def rang(self):
        # Rank is 0 if all elements are zero
        if all(x == 0 for ligne in self.lignes for x in ligne):
            return 0
            
        # Rank is 1 if the determinant is zero (but not all elements are zero)
        if self.det == 0:
            return 1
            
        # Rank is 2 otherwise
        return 2

    @property
    def dim_noyau(self):
        # By the Rank-Nullity Theorem: rank + nullity = number of columns (2)
        return 2 - self.rang