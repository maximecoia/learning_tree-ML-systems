"""Streaming under load: TTFT, ITL, TPOT and goodput, read from the SSE stream."""

import csv
import json
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import releve


COLONNES_FLUX = [
    "concurrence", "comptees", "reussies",
    "ttft_p50", "ttft_p95", "itl_p50", "itl_p95",
    "tpot_p50", "e2e_p50", "debit_req", "goodput", "part_slo",
]


def tirer_flux(base_url, modele, invite, concurrence, total,
               max_jetons=None, timeout=60.0):
    """Fire `total` streamed (SSE) requests, at most `concurrence` in flight,
    and return one record per request (no exception per request)."""

    if type(concurrence) is not int or concurrence < 1:
        raise ValueError("concurrence must be an integer >= 1")
    if type(total) is not int or total < 1:
        raise ValueError("total must be an integer >= 1")

    origine = time.monotonic()
    url = base_url.rstrip("/") + "/v1/chat/completions"

    corps_dict = {
        "model": modele,
        "messages": [{"role": "user", "content": invite}],
        "stream": True,
        "stream_options": {"include_usage": True},
    }
    if max_jetons is not None:
        corps_dict["max_tokens"] = max_jetons
    corps = json.dumps(corps_dict).encode("utf-8")

    def une_requete(rang):
        debut = time.monotonic() - origine
        instants = []
        premier = None
        usage_jetons = None

        try:
            requete = urllib.request.Request(
                url,
                data=corps,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(requete, timeout=timeout) as reponse:
                # Line by line, as it arrives: the only way to time each SSE event.
                for ligne in reponse:
                    ligne_propre = ligne.strip()
                    if not ligne_propre.startswith(b"data:"):
                        continue
                    charge = ligne_propre[5:].strip()
                    if charge == b"[DONE]":
                        break

                    t = time.monotonic() - origine
                    obj = json.loads(charge)

                    # usage.completion_tokens, usually in the last event.
                    usage = obj.get("usage")
                    if usage is not None:
                        ct = usage.get("completion_tokens")
                        if ct is not None:
                            usage_jetons = ct

                    # Only events that carry non-empty text are timed: the
                    # first event often carries the role alone.
                    choices = obj.get("choices")
                    if choices and len(choices) > 0:
                        delta = choices[0].get("delta") or {}
                        contenu = delta.get("content")
                        if contenu:
                            instants.append(t)
                            if premier is None:
                                premier = t

            # `fin` is the end of the request, as in charge.tirer: after
            # [DONE] and the usage event. The last token is instants[-1].
            fin = time.monotonic() - origine

            # Count tokens by usage; fall back on content events when the
            # server ignores include_usage (one event may hold several tokens).
            jetons = usage_jetons
            if jetons is None:
                jetons = len(instants)

            return {
                "rang": rang, "debut": debut, "fin": fin,
                "latence": fin - debut,
                "ok": True, "code": 200, "erreur": None,
                "instants": instants, "premier": premier, "jetons": jetons,
            }

        except urllib.error.HTTPError as e:
            fin = time.monotonic() - origine
            return {
                "rang": rang, "debut": debut, "fin": fin,
                "latence": fin - debut,
                "ok": False, "code": e.code, "erreur": f"HTTP {e.code}: {e.reason}",
                "instants": [], "premier": None, "jetons": None,
            }
        except Exception as e:
            # Unreachable host, timeout, unreadable event: noted, never raised.
            # `except Exception` is not a call, so the allowed list does not
            # cover it; a bare `except:` would also swallow Ctrl-C.
            fin = time.monotonic() - origine
            return {
                "rang": rang, "debut": debut, "fin": fin,
                "latence": fin - debut,
                "ok": False, "code": None, "erreur": f"{type(e).__name__}: {e}",
                "instants": [], "premier": None, "jetons": None,
            }

    comptes = [None] * total
    with ThreadPoolExecutor(max_workers=concurrence) as executeur:
        futurs = [executeur.submit(une_requete, rang) for rang in range(total)]
        for rang in range(total):
            comptes[rang] = futurs[rang].result()
    return comptes


def _tpot(c):
    """Time per output token after the first, from the LAST TOKEN and never
    from `fin`: (last - first) / (tokens - 1). None below two tokens."""
    jetons = c["jetons"]
    if jetons is None:
        jetons = len(c["instants"])
    if jetons < 2 or c["premier"] is None:
        return None
    return (c["instants"][-1] - c["premier"]) / (jetons - 1)


def relever_flux(comptes, concurrence, slo_ttft, slo_tpot, echauffement=0):
    """Turn streamed records into 12 summary numbers: TTFT, ITL, TPOT, e2e,
    throughput, goodput and part_slo."""

    if concurrence < 1:
        raise ValueError("concurrence must be >= 1")
    if slo_ttft <= 0 or slo_tpot <= 0:
        raise ValueError("slo_ttft and slo_tpot must be > 0")
    if len(comptes) == 0:
        raise ValueError("no record")
    if echauffement < 0:
        raise ValueError("echauffement must be >= 0")
    if echauffement >= len(comptes):
        raise ValueError("nothing left to count after the warm-up")

    # Warm-up dropped in the order of DEPARTURES.
    tries = sorted(comptes, key=lambda c: c["debut"])
    utiles = tries[echauffement:]
    comptees = len(utiles)

    reussies = [c for c in utiles if c["ok"]]
    n = len(reussies)

    if n == 0:
        return {
            "concurrence": concurrence,
            "comptees": comptees,
            "reussies": 0,
            "ttft_p50": None, "ttft_p95": None,
            "itl_p50": None, "itl_p95": None,
            "tpot_p50": None, "e2e_p50": None,
            "debit_req": 0.0, "goodput": 0.0, "part_slo": 0.0,
        }

    # TTFT: from the start to the first content token.
    ttfts = sorted([
        c["premier"] - c["debut"]
        for c in reussies if c["premier"] is not None
    ])
    if ttfts:
        ttft_p50 = releve.percentile(ttfts, 50)
        ttft_p95 = releve.percentile(ttfts, 95)
    else:
        ttft_p50 = None
        ttft_p95 = None

    # ITL: every inter-token gap pooled together, never averaged per request.
    itls = []
    for c in reussies:
        insts = c["instants"]
        for i in range(1, len(insts)):
            itls.append(insts[i] - insts[i - 1])
    if itls:
        itls_tries = sorted(itls)
        itl_p50 = releve.percentile(itls_tries, 50)
        itl_p95 = releve.percentile(itls_tries, 95)
    else:
        itl_p50 = None
        itl_p95 = None

    # TPOT per request with at least two tokens. `fin` comes after [DONE]
    # and the usage event: using it would add the stream's tail to TPOT.
    tpots = [t for t in [_tpot(c) for c in reussies] if t is not None]
    if tpots:
        tpot_p50 = releve.percentile(sorted(tpots), 50)
    else:
        tpot_p50 = None

    # End-to-end latency: the whole request, fin - debut.
    e2es = sorted([c["fin"] - c["debut"] for c in reussies])
    e2e_p50 = releve.percentile(e2es, 50)

    # Throughput window: over ALL counted records, refusals included.
    debut_fenetre = min(c["debut"] for c in utiles)
    fin_fenetre = max(c["fin"] for c in utiles)
    duree = fin_fenetre - debut_fenetre

    debit_req = n / duree

    # Goodput: successes that meet both slo_ttft and slo_tpot. A one-token
    # answer has no TPOT and is judged on its TTFT alone.
    tiennent = 0
    for c in reussies:
        if c["premier"] is None:
            continue
        if c["premier"] - c["debut"] > slo_ttft:
            continue
        tpot_c = _tpot(c)
        if tpot_c is None or tpot_c <= slo_tpot:
            tiennent += 1

    goodput = tiennent / duree
    part_slo = tiennent / comptees

    return {
        "concurrence": concurrence,
        "comptees": comptees,
        "reussies": n,
        "ttft_p50": ttft_p50, "ttft_p95": ttft_p95,
        "itl_p50": itl_p50, "itl_p95": itl_p95,
        "tpot_p50": tpot_p50, "e2e_p50": e2e_p50,
        "debit_req": debit_req, "goodput": goodput, "part_slo": part_slo,
    }


def ecrire_flux(releves, chemin):
    """Write a CSV with the COLONNES_FLUX header, one row per level,
    None written as an empty cell."""

    with open(chemin, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(COLONNES_FLUX)
        for r in releves:
            # csv.writer already writes None as an empty cell.
            w.writerow([r[col] for col in COLONNES_FLUX])
