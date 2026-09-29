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
        ...

    def __repr__(self):
        # Matrice([[3, -2], [1, 4]])
        ...

    def __eq__(self, other):
        ...

    def __getitem__(self, index):
        # The row at this index, as a Vecteur.
        ...

    @property
    def shape(self):
        # (rows, columns)
        ...

    def colonnes(self):
        # The list of columns, each one a Vecteur.
        ...

    @classmethod
    def depuis_colonnes(cls, colonnes):
        # The matrix whose columns are these Vecteur. ErreurDeShape when the
        # list is empty or the sizes differ.
        ...

    def __matmul__(self, other):
        # Matrice @ Vecteur: the transformed vector, for any shape.
        # ErreurDeShape when the vector size differs from the column count.
        ...
