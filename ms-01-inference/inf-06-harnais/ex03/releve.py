"""Summary: throughput, percentiles and error rate, without the three traps."""


def percentile(valeurs, p):
    """Nearest-rank percentile: the sorted value of rank ceil(p * n / 100)."""

    if not valeurs:
        raise ValueError("empty list: no percentile")
    if p <= 0 or p > 100:
        raise ValueError("p must be in ]0, 100]")

    triees = sorted(valeurs)
    n = len(triees)

    # 1-based rank ceil(p * n / 100), without math.ceil: -(-x // 1).
    # With a float p (99.9) the rank is a float (10.0), and a float cannot
    # index a list; int() is not in the allowed list, so count up to it.
    rang = -(-(p * n) // 100)
    index = 0
    while index + 1 < rang:
        index += 1
    return triees[index]


def relever(comptes, concurrence, echauffement=0):
    """Turn raw records into 12 summary numbers, dropping the warm-up in
    the order of departures."""

    if concurrence < 1:
        raise ValueError("concurrence must be >= 1")
    if echauffement < 0:
        raise ValueError("echauffement must be >= 0")

    total = len(comptes)
    if echauffement >= total:
        raise ValueError("nothing left to count after the warm-up")

    # 1. Drop the warm-up in the ORDER OF DEPARTURES, not of ranks.
    #    With several threads, rank 7 often leaves before rank 1:
    #    sorting by `debut` is the only honest order.
    tries = sorted(comptes, key=lambda c: c["debut"])
    utiles = tries[echauffement:]
    comptees = len(utiles)

    # 2. Split successes and failures. The error rate is over `comptees`,
    #    not `reussies`: the only denominator that hides nothing.
    reussies = [c for c in utiles if c["ok"]]
    echouees = comptees - len(reussies)
    taux_erreur = echouees / comptees

    # 3. Percentiles over successes ONLY. A refusal comes back in ~2 ms:
    #    counting it would make the server faster as it saturates.
    if reussies:
        latences = sorted([c["latence"] for c in reussies])
        p50 = percentile(latences, 50)
        p95 = percentile(latences, 95)
        maximum = max(latences)
    else:
        p50 = None
        p95 = None
        maximum = None

    # 4. Window over ALL counted records, refusals included. A refusal
    #    occupies the server and pushes back the end of the run:
    #    leaving it out would shorten the window and inflate throughput.
    debut_fenetre = min(c["debut"] for c in utiles)
    fin_fenetre = max(c["fin"] for c in utiles)
    duree = fin_fenetre - debut_fenetre

    # 5. Throughput: successes on top, the full window below. Tokens per
    #    second compare across engines whatever the answer length.
    debit_req = len(reussies) / duree
    jetons_reussis = sum(
        c["jetons_sortie"] for c in reussies if c["jetons_sortie"] is not None
    )
    debit_jetons = jetons_reussis / duree

    return {
        "concurrence": concurrence,
        "total": total,
        "comptees": comptees,
        "reussies": len(reussies),
        "echouees": echouees,
        "taux_erreur": taux_erreur,
        "p50": p50,
        "p95": p95,
        "max": maximum,
        "duree": duree,
        "debit_req": debit_req,
        "debit_jetons": debit_jetons,
    }
