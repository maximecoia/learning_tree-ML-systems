# protocole.py, ex01: record a latency under a written protocol.
# Allowed: client, statistics, sorted, sum, len, range, list, min, max,
#          float, int, ValueError.   (NOT time: nothing is measured here)

import statistics              # median and mean: the two formulas of the record
from client import interroger  # the ex00 probe, reused as is


def mesurer(base_url, modele, invite, repetitions=10, echauffement=3,
            max_jetons=None, essais=3):
    if repetitions < 1:                       # measuring zero times is not a record
        raise ValueError("repetitions must be at least 1")
    if echauffement < 0:                      # discarding a negative number of calls
        raise ValueError("echauffement cannot be negative")

    for _ in range(echauffement):             # first the DISCARDED calls
        interroger(base_url, modele, invite,  # same question,
                   max_jetons=max_jetons, essais=essais)  # same cap
        # the result is not even stored: discarded, but declared in the protocol

    latences = []                             # service durations kept
    jetons_sortie = 0                         # will hold the last counted call's
    for _ in range(repetitions):              # then the COUNTED calls
        r = interroger(base_url, modele, invite,   # NO try: a failure
                       max_jetons=max_jetons, essais=essais)  # must propagate
        latences.append(r["secondes"])        # the SERVICE time, not the total
        jetons_sortie = r["jetons_sortie"]    # response length of the record

    triees = sorted(latences)                 # sorted copy, to read the p90
    n = len(triees)                           # number of measurements kept
    rang = -(-9 * n // 10)                    # ceil(0.9 × n) without importing math
    return {"protocole": {"modele": modele,            # enough to REPLAY the record
                          "invite": invite,
                          "max_jetons": max_jetons,
                          "repetitions": repetitions,
                          "echauffement": echauffement},
            "n": n,                                   # how many measurements kept
            "latences": latences,                    # in call order
            "mediane": statistics.median(latences),  # the ordinary request
            "moyenne": statistics.mean(latences),    # the cost of total throughput
            "p90": triees[rang - 1],                 # 1-based rank -> 0-based index
            "min": min(latences),                    # the best case
            "max": max(latences),                    # the tail, visible
            "jetons_sortie": jetons_sortie}          # comparable at equal length only