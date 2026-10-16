"""Detection of the saturation point (decrochage) on a throughput-latency curve
using an a priori rule: refusal first, then latency explosion, then flat throughput."""

GAIN_MIN = 0.10
SEUIL_LATENCE = 4.0


def ranger(courbe):
    """Sort sweep summaries by ascending concurrency.
    Raise ValueError if the curve is empty or contains duplicate concurrency levels."""
    if not courbe:
        raise ValueError("empty curve: nothing to sort")

    # Sort records by concurrency in ascending order.
    triee = sorted(courbe, key=lambda r: r["concurrence"])

    # Detect duplicate concurrency levels by comparing adjacent sorted items
    # using zip (avoids calling len(), which is not in ex00's allowed list).
    for precedent, suivant in zip(triee, triee[1:]):
        if precedent["concurrence"] == suivant["concurrence"]:
            raise ValueError("duplicate concurrency level in curve")

    return triee


def casse(avant, apres, reference, gain_min=GAIN_MIN, seuil_latence=SEUIL_LATENCE):
    """Evaluate if transitioning from `avant` to `apres` breaks the SLA/capacity.
    Priority order:
      1. 'refus'      : any non-zero error rate in `apres`.
      2. 'latence'    : `apres` p95 strictly exceeds `seuil_latence` * `reference` p95.
      3. 'debit_plat' : `apres` throughput does not strictly exceed
                        `avant` throughput * (1 + gain_min).
      4. None         : the level holds."""
    # 1. A single refusal means the server queue/cache overflowed.
    if apres["taux_erreur"] > 0:
        return "refus"

    # 2. Latency degradation is measured against the idle baseline (reference).
    if apres["p95"] > seuil_latence * reference["p95"]:
        return "latence"

    # 3. Throughput stagnation is measured marginally against the previous level.
    #    Equality is considered a break ("ne depasse pas").
    if apres["debit_req"] <= avant["debit_req"] * (1.0 + gain_min):
        return "debit_plat"

    return None


def decrochage(courbe, gain_min=GAIN_MIN, seuil_latence=SEUIL_LATENCE):
    """Locate the last concurrency level that holds before the first break.
    Raise ValueError if the curve is invalid or if the very first level already refuses."""
    triee = ranger(courbe)
    reference = triee[0]

    # If the lowest concurrency level already drops requests, the baseline p95
    # is corrupted by survivor bias and the true capacity is below our sweep range.
    if reference["taux_erreur"] > 0:
        raise ValueError(
            "the first concurrency level already refuses requests")

    # Walk adjacent pairs (avant, apres) and stop at the very first break.
    for avant, apres in zip(triee, triee[1:]):
        raison = casse(
            avant, apres, reference,
            gain_min=gain_min, seuil_latence=seuil_latence,
        )
        if raison is not None:
            return {
                "decrochage": avant["concurrence"],
                "raison": raison,
                "avant": avant,
                "apres": apres,
                "tient_jusqu_au_bout": False,
            }

    # If no break occurred across the entire sweep, the sweep was too narrow
    # to reach saturation; return the last tested level.
    dernier = triee[-1]
    return {
        "decrochage": dernier["concurrence"],
        "raison": None,
        "avant": dernier,
        "apres": None,
        "tient_jusqu_au_bout": True,
    }
