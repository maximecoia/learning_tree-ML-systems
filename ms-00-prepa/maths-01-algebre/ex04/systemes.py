"""maths-01-algebre ex04: the inverse and linear systems.

Statement:  ./exo maths-01-algebre ex04
Grade:      ./exo maths-01-algebre ex04 -c
Allowed:    isinstance iter len list range sum zip abs all ValueError
"""

# --- carried over from ex03/determinant.py ----------------------------------
# Paste ErreurDeShape and Vecteur here.


class Matrice:
    # --- carried over from ex03/determinant.py ------------------------------
    # Paste the body of Matrice here, det and its properties included.

    # --- new in ex04 ---------------------------------------------------------
    def inverse(self):
        # The inverse of a 2x2 matrix. ValueError when the determinant is 0.
        ...

    def resoudre(self, b):
        # The Vecteur v such that A @ v == b, through the inverse.
        # ValueError when the matrix is singular.
        ...

    @property
    def rang(self):
        # The rank of a 2x2 matrix: 0, 1 or 2.
        ...

    @property
    def dim_noyau(self):
        # The dimension of the kernel of a 2x2 matrix.
        ...
