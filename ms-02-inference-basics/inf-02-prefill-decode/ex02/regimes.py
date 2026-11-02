# regimes.py, ex01 of inf-02-prefill-decode
# Sweep the length of the question and separate the two slopes:
# the prefill's (TTFT) and the decode's (gap between tokens).
# Allowed: flux, statistics, sorted, sum, len, range, zip, list, min, max, float, int, ValueError
import flux          # reuses generer: it talks to the engine, not us
import statistics    # median: the robust summary of the repetitions

def profil(base_url, modele, invites, jetons_sortie=8, repetitions=3, echauffement=1, essais=3):
    # ---- guards: everything refused BEFORE the first request ----
    if repetitions < 1:                          # no counted call = no measurement
        raise ValueError("repetitions doit valoir au moins 1")
    if jetons_sortie < 2:                        # 1 token = 0 gaps = no measurable itl
        raise ValueError("jetons_sortie doit valoir au moins 2")
    if len(invites) < 2:                         # a single question: no line
        raise ValueError("il faut au moins deux questions")

    points_bruts = []      # (length, point) tuples: the sort comes for free
    longueurs = []         # the lengths already seen, to refuse duplicates

    for invite in invites:                       # one question at a time
        ttfts = []                               # TTFT of the counted calls only
        itls = []                                # median gaps of the counted calls
        longueur = None                          # announced by the server, never guessed
        jetons_rendus = None                     # measured on the carrying fragments
        for appel in range(echauffement + repetitions):
            r = flux.generer(base_url, modele, invite,
                             max_jetons=jetons_sortie,   # same cap at EVERY length
                             essais=essais)
            if appel == 0:                       # the very first call announces the length
                longueur = r["jetons_entree"]
                if longueur in longueurs:        # two questions, same tokens:
                    raise ValueError("deux questions de longueur identique")
                longues_vues = longueurs         # (a plain alias, for reading)
                longues_vues.append(longueur)    # no spread = no line
            if appel >= echauffement:            # warm-up dropped, counted calls kept
                ttfts.append(r["ttft"])
                itls.append(r["itl"])
                jetons_rendus = r["jetons_sortie"]
        points_bruts.append((longueur,           # the length as the tuple's 1st item
                             {"jetons_entree": longueur,
                              "ttft": statistics.median(ttfts),   # median of the prefill
                              "itl": statistics.median(itls),     # median of the decode
                              "jetons_sortie": jetons_rendus}))

    # ---- sort by increasing length: sorted compares the tuple's 1st item ----
    points = [point for longueur, point in sorted(points_bruts)]
    xs = [point["jetons_entree"] for point in points]    # the x axis: the length READ
    ys_ttft = [point["ttft"] for point in points]        # y of the prefill
    ys_itl = [point["itl"] for point in points]          # y of the decode

    # ---- least squares, 1st pass: the TTFT as a function of the length ----
    mx = sum(xs) / len(xs)                       # mean of the lengths
    my = sum(ys_ttft) / len(ys_ttft)             # mean of the median TTFTs
    numerateur = sum((x - mx) * (y - my) for x, y in zip(xs, ys_ttft))
    denominateur = sum((x - mx) * (x - mx) for x in xs)  # spread of the lengths
    pente_ttft = numerateur / denominateur       # b: seconds per question token
    origine_ttft = my - pente_ttft * mx          # a: the prefill's fixed part

    # ---- least squares, 2nd pass: the gap between tokens (same x, same denominator) ----
    my_itl = sum(ys_itl) / len(ys_itl)
    numerateur_itl = sum((x - mx) * (y - my_itl) for x, y in zip(xs, ys_itl))
    pente_itl = numerateur_itl / denominateur    # must stay ~0: the decode ignores the question

    return {"protocole": {"modele": modele,
                          "jetons_sortie": jetons_sortie,
                          "repetitions": repetitions,
                          "echauffement": echauffement,
                          "longueurs": xs},       # the declared protocol, warm-up included
            "points": points,
            "pente_ttft": pente_ttft,
            "origine_ttft": origine_ttft,
            "pente_itl": pente_itl,
            "itl_median": statistics.median(ys_itl)}
