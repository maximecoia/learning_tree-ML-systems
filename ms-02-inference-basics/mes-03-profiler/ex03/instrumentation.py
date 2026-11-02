"""instrumentation.py: the cost of the profiler itself, and how to correct for it."""

EVENEMENTS_PAR_APPEL = 2  # one entry event + one exit event per call


def surcout(evenements, cout_evenement):
    """Time attributable to the profiler: number of events × unit cost."""
    if cout_evenement < 0:
        raise ValueError("negative cost")
    return len(evenements) * cout_evenement


def corriger(attribution, cout_evenement):
    """New attribution, with times reduced by the instrumentation cost."""
    if cout_evenement < 0:
        raise ValueError("negative cost")

    corrected = {}
    for name, stats in attribution.items():
        reduction = stats["appels"] * EVENEMENTS_PAR_APPEL * cout_evenement
        corrected[name] = {
            "appels": stats["appels"],
            "propre": max(0.0, stats["propre"] - reduction),
            "cumule": max(0.0, stats["cumule"] - reduction),
        }
    return corrected


def douteuses(attribution, cout_evenement, marge=10):
    """Names, in attribution order, whose self time is below
    marge times what their instrumentation cost."""
    if marge <= 0:
        raise ValueError("zero or negative margin")
    if cout_evenement < 0:
        raise ValueError("negative cost")

    result = []
    for name, stats in attribution.items():
        instrumentation_cost = stats["appels"] * EVENEMENTS_PAR_APPEL * cout_evenement
        if stats["propre"] < marge * instrumentation_cost:
            result.append(name)
    return result
