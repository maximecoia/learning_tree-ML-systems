"""Load harness: hold N requests in flight, never retry."""

import json
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor


def tirer(base_url, modele, invite, concurrence, total,
          max_jetons=None, timeout=30.0):
    """Fire `total` requests at `base_url`, at most `concurrence` in flight,
    and return a list of `total` records (no exception per request)."""

    if type(concurrence) is not int or concurrence < 1:
        raise ValueError("concurrence must be an integer >= 1")
    if type(total) is not int or total < 1:
        raise ValueError("total must be an integer >= 1")

    origine = time.monotonic()

    url = base_url.rstrip("/") + "/v1/chat/completions"
    corps_dict = {
        "model": modele,
        "messages": [{"role": "user", "content": invite}],
    }
    if max_jetons is not None:
        corps_dict["max_tokens"] = max_jetons
    corps = json.dumps(corps_dict).encode("utf-8")

    def une_requete(rang):
        # Start time is taken INSIDE the thread, right before the real send.
        debut = time.monotonic() - origine
        try:
            requete = urllib.request.Request(
                url,
                data=corps,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(requete, timeout=timeout) as reponse:
                # Line by line: no .read() that loads everything at once.
                brut = b"".join(reponse)

            fin = time.monotonic() - origine

            donnees = json.loads(brut)
            usage = donnees.get("usage") or {}
            jetons = usage.get("completion_tokens")

            return {
                "rang": rang,
                "debut": debut,
                "fin": fin,
                "latence": fin - debut,
                "ok": True,
                "code": 200,
                "erreur": None,
                "jetons_sortie": jetons,
            }

        except urllib.error.HTTPError as e:
            # A refusal is a measurement: keep its code, never retry it.
            fin = time.monotonic() - origine
            return {
                "rang": rang, "debut": debut, "fin": fin,
                "latence": fin - debut,
                "ok": False, "code": e.code, "erreur": f"HTTP {e.code}: {e.reason}",
                "jetons_sortie": None,
            }

        except Exception as e:
            # Unreachable host, timeout, malformed JSON: noted, never raised.
            # `except Exception` is not a call, so the allowed list does not
            # cover it; a bare `except:` would also swallow Ctrl-C.
            fin = time.monotonic() - origine
            return {
                "rang": rang, "debut": debut, "fin": fin,
                "latence": fin - debut,
                "ok": False, "code": None, "erreur": f"{type(e).__name__}: {e}",
                "jetons_sortie": None,
            }

    comptes = [None] * total
    with ThreadPoolExecutor(max_workers=concurrence) as executeur:
        futurs = [executeur.submit(une_requete, rang) for rang in range(total)]
        # range instead of enumerate: enumerate is not in the allowed list.
        for rang in range(total):
            comptes[rang] = futurs[rang].result()

    return comptes
