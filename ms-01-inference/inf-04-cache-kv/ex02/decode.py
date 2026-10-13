# decode.py, ex01 of inf-04-cache-kv: the measured gain.
# Allowed: ValueError, float, flux, int, len, list, max, min,
#          range, sorted, statistics, sum, zip
import statistics
import flux


def pente(xs, ys):
    """Least-squares slope through the points (xs, ys).

    b = Σ(xᵢ - x̄)(yᵢ - ȳ) / Σ(xᵢ - x̄)²

    The means are subtracted BEFORE multiplying.
    Raise ValueError when all the xs are equal.
    """
    n = len(xs)
    if n == 0 or len(ys) != n:
        raise ValueError("listes vides ou de tailles différentes")
    xbar = sum(xs) / n
    ybar = sum(ys) / n
    numerateur = 0.0
    denominateur = 0.0
    for x, y in zip(xs, ys):
        dx = x - xbar
        numerateur = numerateur + dx * (y - ybar)
        denominateur = denominateur + dx * dx
    if denominateur == 0.0:
        raise ValueError("tous les xs sont égaux")
    return numerateur / denominateur


def _une_generation(base_url, modele, invite, jetons_sortie, essais):
    """One generation: return (inter_token_gaps, decode_only_duration)."""
    resultat = flux.generer(
        base_url, modele, invite,
        max_jetons=jetons_sortie,
        essais=essais,
    )
    if resultat["jetons_sortie"] != jetons_sortie:
        raise ValueError("génération incomplète")
    itls = resultat["inter_jetons"]
    if len(itls) != jetons_sortie - 1:
        raise ValueError("nombre d'écarts inattendu")
    duree = resultat["secondes"] - resultat["ttft"]
    return itls, duree


def profil_decode(base_url, modele, invite, jetons_sortie=60,
                  repetitions=3, echauffement=1, essais=3):
    """Decode profile ordered by position, with the fitted line."""
    # --- guards: only the VALUE is checked, not the type ---
    if jetons_sortie < 6:
        raise ValueError("moins de six jetons de réponse")
    if repetitions < 1:
        raise ValueError("moins d'une répétition")
    if echauffement < 0:
        raise ValueError("échauffement négatif")
    if essais < 1:
        raise ValueError("moins d'un essai")

    # --- 1. the discarded generations ---
    for _ in range(echauffement):
        _une_generation(base_url, modele, invite, jetons_sortie, essais)

    # --- 2. the kept repetitions ---
    itls_par_repetition = []
    durees = []
    for _ in range(repetitions):
        itls, duree = _une_generation(base_url, modele, invite,
                                      jetons_sortie, essais)
        itls_par_repetition.append(itls)
        durees.append(duree)

    # --- 3. median RANK BY RANK ---
    itl_par_rang = []
    for i in range(jetons_sortie - 1):
        colonne = [itls_par_repetition[r][i] for r in range(repetitions)]
        itl_par_rang.append(statistics.median(colonne))

    # --- 4. slope and intercept of the fitted line ---
    positions = list(range(1, jetons_sortie))
    b = pente(positions, itl_par_rang)

    n = len(positions)
    xbar = sum(positions) / n
    ybar = sum(itl_par_rang) / n
    a = ybar - b * xbar

    # --- 5. first and last thirds ---
    tiers = len(itl_par_rang) // 3
    itl_debut = statistics.median(itl_par_rang[:tiers])
    itl_fin = statistics.median(itl_par_rang[-tiers:])
    croissance = itl_fin / itl_debut

    # --- 6. decode-only duration ---
    total_decode = statistics.median(durees)

    # --- 7. protocol, with an f-string (str is not allowed) ---
    protocole = (f"base_url={base_url} modele={modele} "
                 f"jetons_sortie={jetons_sortie} repetitions={repetitions}")

    return {
        "protocole": protocole,
        "itl_par_rang": itl_par_rang,
        "pente_itl": b,
        "origine_itl": a,
        "itl_debut": itl_debut,
        "itl_fin": itl_fin,
        "croissance": croissance,
        "total_decode": total_decode,
    }


def verdict_cache(profil, seuil=1.15):
    """Return "sans cache" when the growth reaches the threshold, "cache" otherwise."""
    if profil["croissance"] >= seuil:
        return "sans cache"
    return "cache"