"""End-to-end saturation analysis: concurrency sweep, breakpoint detection,
physical limit diagnosis, CSV/SVG generation, and 5-line executive report."""

import decrochage
import limite
import sortie


def analyser(base_url, modele, invite, niveaux, total, echauffement=0,
             max_jetons=None, gain_min=decrochage.GAIN_MIN,
             seuil_latence=decrochage.SEUIL_LATENCE):
    """Run the concurrency sweep in ascending order, locate the saturation point,
    and diagnose the physical limit. Raise ValueError if `niveaux` is empty."""
    if not niveaux:
        raise ValueError("no concurrency levels provided")

    niveaux_ranges = sorted(niveaux)

    # 1. Sweep the server across all concurrency levels.
    courbe = sortie.balayer(
        base_url, modele, invite,
        niveaux_ranges, total,
        echauffement=echauffement, max_jetons=max_jetons,
    )

    # 2. Find the breakpoint using the a priori rule and passed thresholds.
    decroche = decrochage.decrochage(
        courbe, gain_min=gain_min, seuil_latence=seuil_latence,
    )

    # 3. Diagnose the physical bottleneck at the breakpoint.
    diagnostic = limite.diagnostiquer(courbe, decroche)

    protocole = {
        "niveaux": niveaux_ranges,
        "total": total,
        "echauffement": echauffement,
        "max_jetons": max_jetons,
    }

    return {
        "protocole": protocole,
        "courbe": courbe,
        "decrochage": decroche,
        "diagnostic": diagnostic,
    }


def ecrire(analyse, chemin_csv, chemin_svg):
    """Write the sweep curve to `chemin_csv` and the exact matching SVG to
    `chemin_svg` without any trailing newline."""
    courbe = analyse["courbe"]
    sortie.ecrire_csv(chemin_csv, courbe)

    texte_svg = sortie.svg(courbe)
    with open(chemin_svg, "w", encoding="utf-8") as f:
        f.write(texte_svg)


def rapport(analyse):
    """Format the 5-line plain-ASCII diagnostic report from `analyse`."""
    proto = analyse["protocole"]
    dec = analyse["decrochage"]
    diag = analyse["diagnostic"]
    palier = dec["avant"]

    # Format the sorted levels list without calling str.join() to keep AST calls
    # strictly within the allowed list.
    niveaux_texte = ""
    premier = True
    for n in proto["niveaux"]:
        if premier:
            niveaux_texte = str(n)
            premier = False
        else:
            niveaux_texte = niveaux_texte + ", " + str(n)

    # Line 1: Protocol
    ligne_1 = (
        f"balayage: {niveaux_texte} en vol, "
        f"{proto['total']} requetes par niveau, "
        f"{proto['echauffement']} jetees"
    )

    # Line 2: Breakpoint (decrochage)
    cap = dec["decrochage"]
    if dec["tient_jusqu_au_bout"]:
        ligne_2 = f"decrochage: aucun jusqu'a {cap} en vol"
    else:
        apres_c = dec["apres"]["concurrence"]
        ligne_2 = (
            f"decrochage: {cap} en vol, "
            f"raison {dec['raison']}, "
            f"casse a {apres_c}"
        )

    # Line 3: Named physical limit
    nom_limite = diag["limite"]
    if nom_limite == "file bornée":
        ligne_3 = f"limite: file bornee, capacite {cap} en vol"
    elif nom_limite == "temps de service":
        pente_ms = diag["pente_latence"] * 1000.0
        asymptote = diag["debit_asymptotique"]
        ligne_3 = (
            f"limite: temps de service, "
            f"{pente_ms:.1f} ms par requete en file, "
            f"asymptote {asymptote:.0f} req/s"
        )
    elif nom_limite == "débit plafonné":
        ligne_3 = f"limite: debit plafonne a {diag['debit_mesure']:.0f} req/s"
    else:
        ligne_3 = (
            f"limite: balayage trop court, "
            f"le serveur tient encore a {cap} en vol"
        )

    # Line 4: Throughput and Little's Law efficiency
    deb_mes = diag["debit_mesure"]
    deb_theo = diag["debit_theorique"]
    eff_pct = diag["efficacite"] * 100.0
    ligne_4 = (
        f"debit: {deb_mes:.1f} req/s mesure, "
        f"{deb_theo:.1f} req/s par la loi de Little, "
        f"efficacite {eff_pct:.0f}%"
    )

    # Line 5: Latency at the breakpoint (palier) in integer milliseconds
    p50_ms = palier["p50"] * 1000.0
    p95_ms = palier["p95"] * 1000.0
    ligne_5 = f"latence: p50 {p50_ms:.0f} ms, p95 {p95_ms:.0f} ms au palier"

    return f"{ligne_1}\n{ligne_2}\n{ligne_3}\n{ligne_4}\n{ligne_5}"
