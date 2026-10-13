# vitesse.py, ex01 of inf-05-quantifier: the speed of each precision.
import statistics

from flux import generer


def debit(base_url, modele, invite, jetons_sortie=20, repetitions=3,
          echauffement=1, essais=3):
    """Measure the median TTFT, ITL, throughput and total of one precision."""
    # Refuse BEFORE any call: with 1 token there is no gap,
    # and generer returns itl = None, so 1.0 / None would raise TypeError.
    if jetons_sortie < 2:
        raise ValueError("au moins 2 jetons de sortie: sinon aucun ecart")
    # Refuse BEFORE any call: the median of an empty list means nothing,
    # and statistics.median([]) would raise StatisticsError.
    if repetitions < 1:
        raise ValueError("au moins 1 repetition: sinon aucune mediane")

    protocole = {
        "modele": modele,
        "invite": invite,
        "jetons_sortie": jetons_sortie,
        "repetitions": repetitions,
        "echauffement": echauffement,
    }

    # 1. warm-up: calls thrown away, their cost measures no regime.
    for _ in range(echauffement):
        generer(base_url, modele, invite, max_jetons=jetons_sortie,
                essais=essais)

    # 2. repetitions: each quantity is kept in its own list.
    ttfts = []
    itls = []
    totaux = []
    for _ in range(repetitions):
        r = generer(base_url, modele, invite, max_jetons=jetons_sortie,
                    essais=essais)
        ttfts.append(r["ttft"])
        itls.append(r["itl"])
        totaux.append(r["secondes"])

    # 3. median quantity by quantity, not the mean.
    ttft = statistics.median(ttfts)
    itl = statistics.median(itls)
    total = statistics.median(totaux)

    return {
        "protocole": protocole,
        "ttft": ttft,
        "itl": itl,
        # 1/itl = tokens per second. Above all NOT jetons_sortie / total,
        # which would count the prefill and spread it over the 20 tokens.
        "jetons_par_seconde": 1.0 / itl,
        "total": total,
    }


def comparer_precisions(moteurs, modele, invite, reference, jetons_sortie=20,
                        repetitions=3, echauffement=1, essais=3):
    """Measure every precision with the same protocol and return the trade-off."""
    # Refuse BEFORE any measurement: no comparison without at least 2 engines,
    # and no ratio without the reference among them.
    if len(moteurs) < 2:
        raise ValueError("au moins 2 moteurs: une precision seule ne se compare pas")
    if reference not in moteurs:
        raise ValueError("reference absente des moteurs: pas de base pour les rapports")

    # The same arguments for all: that is what makes the measurements comparable.
    mesures = {}
    for nom in moteurs:
        mesures[nom] = debit(moteurs[nom], modele, invite,
                             jetons_sortie=jetons_sortie,
                             repetitions=repetitions,
                             echauffement=echauffement,
                             essais=essais)

    # Reference over measurement, never the reverse: an engine 2x faster
    # has an itl 2x smaller, so the ratio ref/measured is 2.
    itl_ref = mesures[reference]["itl"]
    ttft_ref = mesures[reference]["ttft"]
    acceleration = {nom: itl_ref / mesures[nom]["itl"] for nom in mesures}
    acceleration_prefill = {nom: ttft_ref / mesures[nom]["ttft"]
                            for nom in mesures}

    # The minus sorts from the fastest to the slowest.
    classement = sorted(mesures, key=lambda nom: -acceleration[nom])

    return {
        "protocole": mesures[reference]["protocole"],
        "reference": reference,
        "mesures": mesures,
        "acceleration": acceleration,
        "acceleration_prefill": acceleration_prefill,
        "classement": classement,
    }