import unittest

from releve import centile95, depouiller, illisibles, lire, resumer


class TestCentile95(unittest.TestCase):
    def test_arrondi_vers_le_haut(self):
        self.assertEqual(
            centile95([1.0, 2.0, 3.0]),
            3.0,
        )

    def test_rang_pour_vingt_valeurs(self):
        valeurs = [float(i) for i in range(1, 21)]

        self.assertEqual(
            centile95(valeurs),
            19.0,
        )

    def test_trie_sans_dependre_de_lordre_initial(self):
        self.assertEqual(
            centile95([9.0, 1.0, 5.0]),
            9.0,
        )


class TestDepouiller(unittest.TestCase):
    def test_mesures_et_lignes_illisibles(self):
        self.assertEqual(
            depouiller([
                "# banc",
                "latence: 12.4 ms",
                "zut",
                "",
                "latence: 31.0 ms",
                "debit: abc",
            ]),
            (
                [
                    ("latence", 12.4, "ms"),
                    ("latence", 31.0, "ms"),
                ],
                [3, 6],
            ),
        )

    def test_numerotation_commence_a_un(self):
        self.assertEqual(
            depouiller(["zut"]),
            ([], [1]),
        )

    def test_vides_et_commentaires_ne_sont_pas_fautifs(self):
        self.assertEqual(
            depouiller(["", "   ", "# rien", "   # commentaire"]),
            ([], []),
        )


class TestLireEtIllisibles(unittest.TestCase):
    def test_lire_ne_garde_que_les_mesures_valides(self):
        self.assertEqual(
            lire([
                "a: 1",
                "zut",
                "b: 2 ms",
            ]),
            [
                ("a", 1.0, ""),
                ("b", 2.0, "ms"),
            ],
        )

    def test_illisibles_renvoie_les_bons_numeros(self):
        self.assertEqual(
            illisibles([
                "a: 1",
                "zut",
                "",
                "b: abc",
            ]),
            [2, 4],
        )


class TestResumer(unittest.TestCase):
    def test_format_et_unite(self):
        self.assertEqual(
            resumer([
                ("latence", 12.4, "ms"),
            ]),
            [
                "latence n=1 moy=12.40 p95=12.40 ms",
            ],
        )

    def test_sans_unite(self):
        self.assertEqual(
            resumer([
                ("essais", 3.0, ""),
            ]),
            [
                "essais n=1 moy=3.00 p95=3.00",
            ],
        )

    def test_noms_tries_par_ordre_alphabetique(self):
        self.assertEqual(
            resumer([
                ("b", 2.0, ""),
                ("a", 1.0, ""),
            ]),
            [
                "a n=1 moy=1.00 p95=1.00",
                "b n=1 moy=2.00 p95=2.00",
            ],
        )


if __name__ == "__main__":
    unittest.main()