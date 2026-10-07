# comparer.py, ex02: compare engines under an identical protocol.
# Allowed: protocole, sorted, len, list, min, max, float, str, ValueError.
# (NOT statistics nor time: we READ the records, we recompute nothing)

from protocole import mesurer   # the protocol written in ex01


def comparer(moteurs, modele, invite, repetitions=10, echauffement=3,
             max_jetons=None, essais=3):
    if len(moteurs) < 2:                    # comparing a single engine compares nothing
        raise ValueError("at least two engines are required")

    mesures = {}                            # engine name -> its full record
    for nom in moteurs:                     # each engine, one after the other
        mesures[nom] = mesurer(moteurs[nom], modele, invite,  # SAME protocol
                               repetitions=repetitions,       # for every engine:
                               echauffement=echauffement,     # same numbers
                               max_jetons=max_jetons,         # of discarded
                               essais=essais)                 # and counted calls
        # no try: one engine going down takes down the WHOLE comparison

    classement = sorted(mesures, key=lambda nom: mesures[nom]["mediane"])
    # the names, fastest to slowest, judged on the median alone

    rapide = mesures[classement[0]]["mediane"]   # the lowest median
    lente = mesures[classement[-1]]["mediane"]   # the highest median
    ecart = lente / rapide                       # ratio of the extremes: >= 1
    gagnant = classement[0] if ecart >= 1.05 else None   # under 1.05: none

    return {"protocole": mesures[classement[0]]["protocole"],  # the same everywhere
            "mesures": mesures,          # keep everything, so it can be contradicted
            "classement": classement,    # ordered by increasing median
            "gagnant": gagnant,          # or None: that is an answer, not a gap
            "ecart": ecart}              # always at least 1


def rapport(resultat):
    p = resultat["protocole"]               # line 1: enough to replay the record
    lignes = [f"protocole: modele={p['modele']} invite='{p['invite']}' "
              f"repetitions={p['repetitions']} echauffement={p['echauffement']} "
              f"max_jetons={p['max_jetons']}"]
    for nom in resultat["classement"]:      # the engines, in ranking order
        m = resultat["mesures"][nom]
        lignes.append(f"{nom} mediane={m['mediane']:.3f} p90={m['p90']:.3f} "
                      f"min={m['min']:.3f} max={m['max']:.3f} "
                      f"moyenne={m['moyenne']:.3f} n={m['n']}")
    if resultat["gagnant"] is None:         # gap too small to conclude
        lignes.append(f"gagnant: aucun, écart de {resultat['ecart']:.2f}x "
                      f"sous le seuil de 1.05x")
    else:                                   # the winner, against the LAST one:
        lignes.append(f"gagnant: {resultat['classement'][0]}, "     # it is the one
                      f"{resultat['ecart']:.2f}x plus rapide que "  # that carries the gap
                      f"{resultat['classement'][-1]}")
    return "\n".join(lignes)                # a single text, compared line by line