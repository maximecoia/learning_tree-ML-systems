"""echantillonnage.py: sampling profiler, how many samples for what confidence."""

import math


def echantillonner(piles):
    """Count, per name: 'feuille' (on top) and 'presente' (in the stack)."""
    counts = {}
    for stack in piles:
        if not stack:
            raise ValueError("empty stack")

        # create the keys in order of appearance (outermost -> deepest)
        for name in stack:
            if name not in counts:
                counts[name] = {"feuille": 0, "presente": 0}

        counts[stack[-1]]["feuille"] += 1      # the top is the LAST element
        for name in set(stack):                # once per stack, even if repeated
            counts[name]["presente"] += 1
    return counts


def parts(comptes, echantillons):
    """Share of each name: feuille divided by the number of samples."""
    if echantillons < 1:
        raise ValueError("fewer than one sample")
    return {name: stats["feuille"] / echantillons for name, stats in comptes.items()}


def assez_echantillons(part_visee, precision, confiance=2):
    """Integer number of samples needed, rounded up."""
    if not 0  <= part_visee <= 1:
        raise ValueError("share outside the range 0 to 1")
    if precision <= 0:
        raise ValueError("zero or negative precision")
    if confiance <= 0:
        raise ValueError("zero or negative confidence")
    return math.ceil(confiance ** 2 * part_visee * (1 - part_visee) / precision ** 2)
