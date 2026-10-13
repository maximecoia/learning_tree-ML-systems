# arbitrage.py, ex02 of inf-04-cache-kv: the trade-off.
# Allowed: cache, abs, sorted, len, sum, min, max, float, int, str,
#          zip, list, ValueError
import cache


GIO = 1024 ** 3


def contexte_de_bascule(config, octets_poids, lots):
    """Context length at which the cache equals the weights.

    Integer division, rounded down. Fewer than one sequence raises ValueError.
    """
    if lots < 1:
        raise ValueError("moins d'une séquence")
    return octets_poids // (lots * cache.octets_par_jeton(config))


def plan_memoire(config, memoire_totale, parametres, octets_par_nombre,
                 reserve, contextes, lots):
    """Memory plan: the crossover, and one row per context length."""
    if not contextes:
        raise ValueError("aucun contexte")
    if lots < 1:
        raise ValueError("moins d'une séquence")

    poids = cache.octets_des_poids(parametres, octets_par_nombre)
    libre = cache.memoire_libre(memoire_totale, poids, reserve)
    bascule = contexte_de_bascule(config, poids, lots)

    lignes = []
    for contexte in sorted(contextes):
        sequences = cache.sequences_tenables(config, libre, contexte)
        cache_octets = cache.octets_du_cache(config, contexte, sequences)
        occupe = poids + cache_octets
        part = cache_octets / occupe
        lignes.append({
            "contexte": contexte,
            "sequences": sequences,
            "cache": cache_octets,
            "part_du_cache": part,
        })

    return {
        "memoire_totale": memoire_totale,
        "reserve": reserve,
        "poids": poids,
        "libre": libre,
        "lots": lots,
        "bascule": bascule,
        "lignes": lignes,
    }


def modele_de_temps(profil, seuil=1.15):
    """Extract the line itl(i) = a + b*i from the ex01 profile.

    `plat` compares itl(positions) over itl(1) with the threshold. The ratio
    has no unit and sits on the same scale as the ex01 verdict.
    """
    a = profil["origine_itl"]
    b = profil["pente_itl"]
    positions = len(profil["itl_par_rang"])
    itl_fin = a + b * positions
    itl_debut = a + b * 1
    plat = (itl_fin / itl_debut) < seuil
    return {
        "itl_origine": a,
        "itl_par_position": b,
        "plat": plat,
    }


def temps_decode_predit(modele, jetons_sortie):
    """Sum of the line over positions 1 to n-1.

    decode(n) = (n-1)*a + b*n(n-1)/2
    """
    if jetons_sortie < 1:
        raise ValueError("moins d'un jeton")
    n = jetons_sortie
    a = modele["itl_origine"]
    b = modele["itl_par_position"]
    return (n - 1) * a + b * n * (n - 1) / 2


def gain_predit(modele_sans, modele_avec, jetons_sortie):
    """Ratio of the two totals: without cache over with cache."""
    sans = temps_decode_predit(modele_sans, jetons_sortie)
    avec = temps_decode_predit(modele_avec, jetons_sortie)
    return sans / avec


def plan_temps(profil_sans, profil_avec, jetons_sortie):
    """Prediction and gain from the two profiles measured in ex01."""
    sans = temps_decode_predit(modele_de_temps(profil_sans), jetons_sortie)
    avec = temps_decode_predit(modele_de_temps(profil_avec), jetons_sortie)
    return {
        "jetons_sortie": jetons_sortie,
        "sans": sans,
        "avec": avec,
        "gain": sans / avec,
    }


def rapport(plan, temps):
    """Formatted report: sizes in GiB to 3 decimals, shares in %, gain to 2."""
    lignes = []
    lignes.append(
        f"carte: {plan['memoire_totale'] / GIO:.3f} Gio, "
        f"poids {plan['poids'] / GIO:.3f} Gio, "
        f"reserve {plan['reserve'] / GIO:.3f} Gio, "
        f"libre {plan['libre'] / GIO:.3f} Gio"
    )
    for ligne in plan["lignes"]:
        lignes.append(
            f"contexte={ligne['contexte']} "
            f"sequences={ligne['sequences']} "
            f"cache={ligne['cache'] / GIO:.3f} Gio "
            f"part={ligne['part_du_cache'] * 100:.0f}%"
        )
    lignes.append(
        f"bascule: a {plan['lots']} sequences le cache egale les poids "
        f"des {plan['bascule']} jetons de contexte"
    )
    lignes.append(
        f"temps: {temps['jetons_sortie']} jetons de reponse, "
        f"{temps['sans']:.3f} s sans cache contre "
        f"{temps['avec']:.3f} s avec, "
        f"gain {temps['gain']:.2f}x"
    )
    return "\n".join(lignes)