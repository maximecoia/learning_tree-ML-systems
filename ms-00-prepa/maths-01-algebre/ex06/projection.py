"""maths-01-algebre ex06: the norm and the projection.

Statement:  ./exo maths-01-algebre ex06
Grade:      ./exo maths-01-algebre ex06 -c
Allowed:    isinstance iter len list sum zip all float ValueError
"""

# --- carried over from ex00/vecteurs.py -------------------------------------
# Paste ErreurDeShape here. No Matrice in this step.


class Vecteur:
    # --- carried over from ex00/vecteurs.py ---------------------------------
    # Paste the body of Vecteur here.

    # --- new in ex06 ---------------------------------------------------------
    @property
    def norme(self):
        # The length of the vector, as a float.
        ...

    def distance(self, autre):
        # The distance between the two points.
        ...

    def est_orthogonal(self, autre):
        # True when the two vectors are perpendicular.
        ...

    def projeter_sur(self, u):
        # The projection of the vector on the line carried by u.
        # ValueError when u is the zero vector.
        ...
