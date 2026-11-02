"""rapport.py: a readable text report from an attribution."""

from instrumentation import douteuses


def classer(attribution):
    """Names sorted by decreasing self time; ties keep attribution order."""
    return sorted(attribution, key=lambda name: attribution[name]["propre"], reverse=True)


def rapport(attribution, cout_evenement=0.0, marge=10, combien=5):
    """At most combien ranking lines, then the verdict; lines joined
    by a newline, with no trailing newline. The report text itself stays
    in French, as the exercise specifies it word for word."""
    if combien < 1:
        raise ValueError("combien below 1")
    if not attribution:
        return "aucune fonction mesurée"

    total = sum(stats["propre"] for stats in attribution.values())
    noisy = set(douteuses(attribution, cout_evenement, marge))
    order = classer(attribution)

    lines = []
    for name in order[:combien]:
        stats = attribution[name]
        share = stats["propre"] / total * 100 if total else 0.0
        line = (f"{name} propre={stats['propre']:.3f} ({share:.1f} %) "
                f"cumule={stats['cumule']:.3f} appels={stats['appels']}")
        if name in noisy:
            line += " [sous le bruit de la mesure]"
        lines.append(line)

    top_share = attribution[order[0]]["propre"] / total * 100 if total else 0.0
    if top_share >= 50:
        lines.append(f"{order[0]} domine avec {top_share:.1f} % du temps propre")
    else:
        lines.append("aucune fonction ne domine: le temps est réparti")

    return "\n".join(lines)
