"""Output: concurrency sweep, CSV, and an SVG rebuilt from the CSV alone."""

import csv

import charge
import releve


COLONNES = [
    "concurrence", "total", "comptees", "reussies", "echouees",
    "taux_erreur", "p50", "p95", "max", "duree",
    "debit_req", "debit_jetons",
]

_ENTIERS = {"concurrence", "total", "comptees", "reussies", "echouees"}

_X0, _X1 = 40, 560
_Y0, _Y1 = 40, 360


def balayer(base_url, modele, invite, concurrences, total, echauffement=0, max_jetons=None):
    """Fire and summarize at each concurrency level, smallest to largest."""
    if not concurrences:
        raise ValueError("no concurrency level to sweep")
    releves = []
    for c in sorted(concurrences):
        comptes = charge.tirer(
            base_url, modele, invite, c, total, max_jetons,
        )
        releves.append(releve.relever(comptes, c, echauffement))
    return releves


def _formater(colonne, valeur):
    """CSV string of a value, given its column: integers as integers,
    None as an empty cell, everything else at six decimals."""
    if valeur is None:
        return ""
    if colonne in _ENTIERS:
        return str(valeur)
    return f"{valeur:.6f}"


def ecrire_csv(chemin, releves):
    """Write the COLONNES header, then one row per summary: integers as
    integers, the rest at six decimals, None as an empty cell."""
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(COLONNES)
        for r in releves:
            w.writerow([_formater(col, r[col]) for col in COLONNES])


def _convertir(colonne, cellule):
    """Typed value of a CSV cell: None if empty, int for an integer column,
    float otherwise."""
    if cellule == "":
        return None
    if colonne in _ENTIERS:
        return int(cellule)
    return float(cellule)


def lire_csv(chemin):
    """Read a CSV back into typed summaries (int, float, None); raise
    ValueError if the header is not COLONNES."""
    with open(chemin, "r", encoding="utf-8", newline="") as f:
        lecteur = csv.reader(f)
        entete = next(lecteur)
        if entete != COLONNES:
            # str is allowed, repr is not.
            raise ValueError("unexpected header: " + str(entete))
        releves = []
        for ligne in lecteur:
            r = {}
            # zip instead of range(len(...)): shorter, and allowed.
            for col, cell in zip(COLONNES, ligne):
                r[col] = _convertir(col, cell)
            releves.append(r)
    return releves


def _r6(x):
    """Round to six decimals, or None. Uses the same f-string as the CSV,
    so the value is exactly the one read back from disk."""
    if x is None:
        return None
    return float(f"{x:.6f}")


def _x_pixel(i, n):
    """Abscissa of the i-th point out of n. Centered when n == 1."""
    if n == 1:
        return (_X0 + _X1) // 2
    return _X0 + (_X1 - _X0) * i // (n - 1)


def _y_pixel(valeur, vmax):
    """SVG ordinate (y grows downward): a large value gives a small y."""
    if vmax <= 0:
        return _Y1
    return _Y1 - int((_Y1 - _Y0) * valeur / vmax)


def svg(releves):
    """SVG text of a sweep: three polylines (p50, p95, throughput), one
    point per summary, concurrency and error-rate labels."""
    if not releves:
        raise ValueError("no summary to plot")

    # 1. Round to six decimals BEFORE any scale is computed.
    rs = []
    for r in releves:
        rs.append({
            "concurrence": r["concurrence"],
            "taux_erreur": _r6(r["taux_erreur"]),
            "p50": _r6(r["p50"]),
            "p95": _r6(r["p95"]),
            "debit_req": _r6(r["debit_req"]),
        })

    n = len(rs)

    # 2. Scales, on the rounded values. p50 and p95 share one scale in
    #    seconds; throughput gets its own.
    lat_max = 0.0
    deb_max = 0.0
    for r in rs:
        if r["p50"] is not None and r["p50"] > lat_max:
            lat_max = r["p50"]
        if r["p95"] is not None and r["p95"] > lat_max:
            lat_max = r["p95"]
        if r["debit_req"] is not None and r["debit_req"] > deb_max:
            deb_max = r["debit_req"]

    # 3. Points and labels, with a manual index (range is not allowed).
    pts_p50, pts_p95, pts_deb = [], [], []
    etiquettes_x, etiquettes_err = [], []
    i = 0
    for r in rs:
        x = _x_pixel(i, n)
        yp50 = _y_pixel(r["p50"] or 0.0, lat_max)
        yp95 = _y_pixel(r["p95"] or 0.0, lat_max)
        ydeb = _y_pixel(r["debit_req"] or 0.0, deb_max)
        pts_p50.append(str(x) + "," + str(yp50))
        pts_p95.append(str(x) + "," + str(yp95))
        pts_deb.append(str(x) + "," + str(ydeb))

        etiquettes_x.append(
            '<text class="x" x="' + str(x) + '" y="395">'
            + str(r["concurrence"]) + "</text>"
        )
        te = r["taux_erreur"]
        if te is not None and te != 0.0:
            pct = int(te * 100 + 0.5)
            etiquettes_err.append(
                '<text class="erreur" x="' + str(x)
                + '" y="' + str(_Y1 - 5) + '">'
                + str(pct) + " %</text>"
            )
        i += 1

    # 4. Assembly, with a fixed attribute order.
    lignes = []
    lignes.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400">')
    lignes.append('<polyline class="p50" points="' + " ".join(pts_p50) + '"/>')
    lignes.append(
        '<polyline class="p95" points="' + " ".join(pts_p95)
        + '" stroke-dasharray="4 4"/>'
    )
    lignes.append('<polyline class="debit" points="' + " ".join(pts_deb) + '"/>')
    lignes.extend(etiquettes_x)
    lignes.extend(etiquettes_err)
    lignes.append("</svg>")
    return "\n".join(lignes)
