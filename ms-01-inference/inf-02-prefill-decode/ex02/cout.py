# cout.py, ex02 of inf-02-prefill-decode
# Allowed: regimes, abs, max, min, len, sum, sorted, zip, float, int, str, ValueError
# What must come out, copied from the statement at the top of the file:
#   predire(m,100,51) -> 0.150 (not 0.151); predire(m,100,1) -> 0.100; predire(m,100,2) -> 0.101
#   regime_dominant(m,400,2)="prefill" (m,10,201)="decode" (m,100,101)="equilibre" (m,100,141)="decode"
# NO import: the constants already live in the profil dictionary,
# and every name needed here is an allowed builtin or one of my own functions.

def modele_de_cout(profil):
    # ---- guard: a line needs at least two points ----
    points = profil["points"]                      # the sweep produced by regimes.profil
    if len(points) < 2:                            # fewer than two points: no slope
        raise ValueError("moins de deux points dans le profil")
    # ---- the three constants: READ again, never refitted (lesson 23) ----
    a = profil["origine_ttft"]                     # the prefill's fixed part, from ex01's line
    b = profil["pente_ttft"]                       # seconds per question token
    c = profil["itl_median"]                       # the decode's pace, already a median
    longueurs = [p["jetons_entree"] for p in points]   # the x values, read from the server at ex01
    # ---- the model's error: the worst relative error, as a FRACTION ----
    erreurs = [abs(a + b * p["jetons_entree"] - p["ttft"]) / p["ttft"] for p in points]
    return {"prefill_fixe": a,
            "prefill_par_jeton": b,
            "decode_par_jeton": c,
            "longueurs": longueurs,
            "erreur_max": max(erreurs)}            # 0.016 reads 1.6%: a fraction, not a percentage

def decomposer(modele, jetons_entree, jetons_sortie):
    # ---- guard: an answer of less than one token does not exist ----
    if jetons_sortie < 1:
        raise ValueError("moins d'un jeton de réponse")
    # ---- the two terms of the bill ----
    prefill = modele["prefill_fixe"] + modele["prefill_par_jeton"] * jetons_entree
    decode = modele["decode_par_jeton"] * (jetons_sortie - 1)   # the 1st token is ALREADY in the TTFT
    total = prefill + decode
    return {"prefill": prefill,
            "decode": decode,
            "total": total,
            "part_prefill": prefill / total}       # the number that decides instead of opinions

def predire(modele, jetons_entree, jetons_sortie):
    # a single line: the "output - 1" rule lives only in decomposer
    return decomposer(modele, jetons_entree, jetons_sortie)["total"]

def regime_dominant(modele, jetons_entree, jetons_sortie):
    part = decomposer(modele, jetons_entree, jetons_sortie)["part_prefill"]
    if abs(part - 0.5) < 0.05:                     # within 0.05 of one half:
        return "equilibre"                         # naming a dominant would decide on noise
    if part > 0.5:                                 # beyond the band:
        return "prefill"                           #   the question pays
    return "decode"                                #   otherwise the answer pays

def rapport(modele, cas):
    # ---- line 1: the price list, formats reverse-engineered from the statement's example ----
    lignes = [f"modele de cout: prefill = {modele['prefill_fixe']:.3f} s "
              f"+ {modele['prefill_par_jeton']:.6f} s par jeton de question, "
              f"decode = {modele['decode_par_jeton']:.6f} s par jeton de reponse, "
              f"erreur max {modele['erreur_max'] * 100:.1f}% sur {len(modele['longueurs'])} points"]
    # ---- one line per request shape ----
    for nom, entree, sortie in cas:
        d = decomposer(modele, entree, sortie)     # same terms, same formats
        lignes.append(f"{nom} entree={entree} sortie={sortie} "
                      f"prefill={d['prefill']:.3f} decode={d['decode']:.3f} "
                      f"total={d['total']:.3f} part_prefill={d['part_prefill'] * 100:.0f}% "
                      f"dominant={regime_dominant(modele, entree, sortie)}")
    return "\n".join(lignes)                       # a text, not a print: the result is returned
