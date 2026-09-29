"""maths-01-algebre ex02: the matrix product.

Statement:  ./exo maths-01-algebre ex02
Grade:      ./exo maths-01-algebre ex02 -c
Allowed:    isinstance iter len list range sum zip
"""

# --- carried over from ex01/matrices.py -------------------------------------
# Paste ErreurDeShape and Vecteur here.


class Matrice:
    # --- carried over from ex01/matrices.py ---------------------------------
    # Paste the body of Matrice here, then extend its __matmul__: with a
    # Matrice, return the product AB for any compatible shapes, and raise
    # ErreurDeShape when A's column count differs from B's row count. With a
    # Vecteur, it does what it did.

    # --- new in ex02 ---------------------------------------------------------
    @classmethod
    def identite(cls, n):
        # The identity matrix of shape (n, n).
        ...

    def puis(self, suivante):
        # The matrix that applies self, then suivante.
        ...
