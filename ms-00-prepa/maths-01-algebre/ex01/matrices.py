"""maths-01-algebre ex01: matrices.

Statement:  ./exo maths-01-algebre ex01
Grade:      ./exo maths-01-algebre ex01 -c
Allowed:    isinstance iter len list range sum zip
"""

# --- carried over from ex00/vecteurs.py -------------------------------------
# Paste ErreurDeShape and Vecteur here. The grader checks them again.


class Matrice:

    def __init__(self, lignes):
        # Copy the rows into self.lignes. ErreurDeShape when there is no row,
        # when a row is empty, or when the rows have different lengths.
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
        # Matrice([[3, -2], [1, 4]])
        return f"Matrice({self.lignes})"


    def __eq__(self, other):
        if not isinstance(other, Matrice):
            raise NotImplemented
        return self.nombres == other.nombres

    def __getitem__(self, index):
        # The row at this index, as a Vecteur.
        return Vecteur(self.nombres[index])

    @property
    def shape(self):
        # (rows, columns)
        return len(self.lignes), len(self.lignes[0])

    def colonnes(self):
        # The list of columns, each one a Vecteur.
         return [Vecteur(col) for col in zip(*self.lignes)]

    @classmethod
    def depuis_colonnes(cls, colonnes):
        # The matrix whose columns are these Vecteur. ErreurDeShape when the
        # list is empty or the sizes differ.
        if not colonnes:
            raise ErreurDeShape

        taille = len(colonnes[0])
        for v in colonnes:
            if len(v) != taille:
                raise ErreurDeShape

        return cls(zip(*colonnes))

    def __matmul__(self, other):
        # Matrice @ Vecteur: the transformed vector, for any shape.
        # ErreurDeShape when the vector size differs from the column count.
         if not isinstance(other, Vecteur):
            return NotImplemented

          if self.shape[1] != len(other):
            raise ErreurDeShape

        return Vecteur([Vecteur(ligne) @ other for ligne in self.lignes])
        
