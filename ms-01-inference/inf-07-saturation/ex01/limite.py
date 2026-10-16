"""Physical limit diagnosis: Little's law ceiling, ordinary least squares (OLS)
latency slope, asymptotic throughput, and verifiable explanation."""


def loi_de_little(concurrence, latence):
    """Return the theoretical throughput ceiling L / W (requests/s).
    Raise ValueError if concurrency < 1 or latency <= 0."""
    if concurrence < 1:
        raise ValueError("concurrence must be >= 1")
    if latence <= 0:
        raise ValueError("latence must be > 0")
    return concurrence / latence


def pente_latence(courbe, jusqu_a=None):
    """Compute the OLS slope of p50 (seconds per additional concurrent request)
    over levels with zero refusals and concurrency <= `jusqu_a`.
    Raise ValueError if fewer than 2 valid levels remain or variance of x is 0."""
    # Filter levels: no errors, valid p50, and up to `jusqu_a` if specified.
    retenus = [
        r for r in courbe
        if r["taux_erreur"] == 0
        if r["p50"] is not None
        if (jusqu_a is None or r["concurrence"] <= jusqu_a)
    ]

    n = len(retenus)
    if n < 2:
        raise ValueError(
            "at least two valid levels are required to fit a slope")

    moyenne_x = sum(r["concurrence"] for r in retenus) / n
    moyenne_y = sum(r["p50"] for r in retenus) / n

    numerateur = sum(
        (r["concurrence"] - moyenne_x) * (r["p50"] - moyenne_y)
        for r in retenus
    )
    denominateur = sum(
        (r["concurrence"] - moyenne_x) ** 2
        for r in retenus
    )

    if denominateur == 0:
        raise ValueError("all retained levels have the same concurrency")

    return numerateur / denominateur


def diagnostiquer(courbe, decroche):
    """Turn the curve and the output of `decrochage()` into a physical diagnosis.
    Returns limit name, capacity, measured/theoretical throughput, efficiency,
    and (for service-time limits) latency slope and asymptotic throughput."""
    palier = decroche["avant"]
    capacite = decroche["decrochage"]
    raison = decroche["raison"]

    debit_mesure = palier["debit_req"]
    debit_theorique = loi_de_little(capacite, palier["p50"])
    efficacite = debit_mesure / debit_theorique

    pente = None
    asymptote = None

    if raison == "refus":
        limite = "file bornée"
        explication = (
            f"file bornée : le serveur refuse au-delà de {capacite} en vol"
        )
    elif raison == "latence":
        limite = "temps de service"
        pente = pente_latence(courbe, jusqu_a=capacite)
        asymptote = 1.0 / pente
        pente_ms = pente * 1000.0
        explication = (
            f"temps de service : pente de {pente_ms:.1f} ms/req, "
            f"débit asymptotique plafonné à {asymptote:.0f} req/s "
            f"({asymptote:.1f} req/s)"
        )
    elif raison == "debit_plat":
        limite = "débit plafonné"
        explication = (
            f"débit plafonné à {debit_mesure:.0f} req/s "
            f"({debit_mesure:.1f} req/s) dès {capacite} en vol"
        )
    else:
        limite = "balayage trop court"
        explication = (
            f"balayage trop court : le serveur tient encore à {capacite} en vol"
        )

    return {
        "limite": limite,
        "capacite": capacite,
        "debit_mesure": debit_mesure,
        "debit_theorique": debit_theorique,
        "efficacite": efficacite,
        "pente_latence": pente,
        "debit_asymptotique": asymptote,
        "explication": explication,
    }
