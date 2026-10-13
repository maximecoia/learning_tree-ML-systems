# qualite.py, ex02 of inf-05-quantifier: the perplexity of each precision.
from perplexite import perplexite


def comparer_qualites(moteurs, modele, textes, reference, essais=3):
    """Score the same corpus on every engine and return each one's degradation."""
    # --- Refuse BEFORE any call -----------------------------------------
    # A single precision compares to nothing.
    if len(moteurs) < 2:
        raise ValueError("au moins 2 moteurs: une precision seule ne se compare pas")
    # No baseline for the degradation.
    if reference not in moteurs:
        raise ValueError("reference absente des moteurs: pas de base pour comparer")
    # Empty corpus: refused here, with a comparison message, before
    # perplexite refuses it at the first engine with a text message.
    if not textes:
        raise ValueError("corpus vide: aucune qualite a comparer")

    # --- A single call to perplexite per engine --------------------------
    # 4 texts x 3 engines = 12 requests. Never go through them twice.
    mesures = {}
    for nom in moteurs:
        mesures[nom] = perplexite(moteurs[nom], modele, textes, essais=essais)

    # --- The check that earns the right to compare ----------------------
    # A perplexity is a mean PER TOKEN. Two different tokenizations
    # give two numbers that do not cover the same predictions:
    # an engine cutting every 5 characters reports 12.8767 against 14.9301,
    # a false "improvement" of 13.75% where the model degrades by 12.19%.
    comptes = {nom: m["jetons_notes"] for nom, m in mesures.items()}
    if len(set(comptes.values())) > 1:
        raise ValueError(f"decoupages differents, comparaison impossible: {comptes}")

    # --- The degradation, a share and not a ratio -----------------------
    # -1.0 turns the ratio into a share: fp16 gives 0, int8 0.0151.
    # That is what ex03 compares to a budget written in percent.
    base = mesures[reference]["perplexite"]
    degradation = {nom: m["perplexite"] / base - 1.0
                   for nom, m in mesures.items()}

    # The least degraded first. No minus sign: ascending is the default.
    classement = sorted(mesures, key=lambda nom: degradation[nom])

    return {
        "corpus": {
            "textes": len(textes),
            "jetons_notes": mesures[reference]["jetons_notes"],
        },
        "reference": reference,
        "mesures": mesures,
        "degradation": degradation,
        "classement": classement,
    }