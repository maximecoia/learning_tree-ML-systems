# arbitrage.py, ex03 of inf-05-quantifier: the trade-off, decided by a budget.
RAISON = "degradation au-dela du budget"


def arbitrer(vitesse, qualite, budget_degradation):
    """Pick the fastest precision within the budget and return the decision."""
    # --- Refusals, in this exact order --------------------------------
    # is None BEFORE < 0: otherwise None < 0 raises TypeError, not ValueError.
    if budget_degradation is None:
        raise ValueError(
            "budget absent: une acceleration et une degradation ne "
            "designent aucune precision tant qu'on n'a pas dit combien "
            "de qualite on accepte de perdre"
        )
    if budget_degradation < 0:
        raise ValueError("budget negatif: on n'accepte pas une degradation negative")
    # The same baseline on both sides, otherwise the ratios cannot sit side by side.
    if vitesse["reference"] != qualite["reference"]:
        raise ValueError("references differentes: les deux releves ne se recollent pas")
    # The same names on both sides, otherwise a precision gets half a row.
    if set(vitesse["mesures"]) != set(qualite["mesures"]):
        raise ValueError("precisions differentes entre les deux releves")

    reference = vitesse["reference"]
    accel = vitesse["acceleration"]
    accel_prefill = vitesse["acceleration_prefill"]
    degr = qualite["degradation"]

    # --- One row per precision, sorted by decreasing decode speed -----
    # The minus before accel[n] reverses the default order: int4 first.
    lignes = []
    for nom in sorted(accel, key=lambda n: -accel[n]):
        # The reference always fits: by definition it degrades nothing.
        # Written out, without relying on degr[reference] being 0.0.
        dans_le_budget = (nom == reference) or (degr[nom] <= budget_degradation)
        lignes.append({
            "precision": nom,
            "decode": accel[nom],
            "prefill": accel_prefill[nom],
            "perplexite": qualite["mesures"][nom]["perplexite"],
            "degradation": degr[nom],
            "retenue": dans_le_budget,
        })

    # The candidates, in row order, so from the fastest to the slowest.
    candidats = [ligne["precision"] for ligne in lignes if ligne["retenue"]]
    ecartees = {ligne["precision"]: RAISON
                for ligne in lignes if not ligne["retenue"]}

    # The rule: the fastest at decode among the candidates.
    # Since the rows are sorted, it is the first candidate.
    retenue = candidats[0]

    return {
        "budget": budget_degradation,
        "reference": reference,
        "lignes": lignes,
        "candidats": candidats,
        "ecartees": ecartees,
        "retenue": retenue,
        # The chosen precision's values, raw, as they come from the measurements.
        "acceleration": accel[retenue],
        "degradation": degr[retenue],
    }


def rapport(decision):
    """Return the report text, numbers formatted."""
    reference = decision["reference"]
    retenue = decision["retenue"]

    # Header and reference, with the percent format on the budget.
    texte = [
        f"budget: degradation acceptee jusqu'a {decision['budget']:.2%}",
        f"reference: {reference}",
    ]

    # One line per precision, in row order.
    for ligne in decision["lignes"]:
        if ligne["retenue"]:
            etat = "retenue"
        else:
            etat = f"ecartee ({RAISON})"
        texte.append(
            f"{ligne['precision']} "
            f"decode={ligne['decode']:.2f}x "
            f"prefill={ligne['prefill']:.2f}x "
            f"perplexite={ligne['perplexite']:.4f} "
            f"degradation={ligne['degradation']:+.2%} "
            f"{etat}"
        )

    # Last line: two forms, whether the reference wins or not.
    if retenue == reference:
        texte.append(
            f"decision: {retenue}, aucune precision reduite ne tient dans le budget"
        )
    else:
        texte.append(
            f"decision: {retenue}, "
            f"{decision['acceleration']:.2f}x plus rapide au decodage "
            f"pour {decision['degradation']:+.2%} de perplexite"
        )

    return "\n".join(texte)