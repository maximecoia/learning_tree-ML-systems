# client.py, ex00: query an inference engine through its API.
# Allowed: json, time, urllib, float, int, str, len, max, min, range, dict.

import json                 # build (dumps) and read (loads) the JSON
import time                 # monotonic to measure, sleep to wait
import urllib.request       # Request and urlopen: send the HTTP request
import urllib.error         # HTTPError and URLError: the network errors


class ErreurModele(Exception):
    # Our own exception: the four ways the model can fail all leave
    # through here, so the caller catches a single error type.
    pass


REESSAYABLES = (429, 500, 502, 503, 504)
# The only codes worth another attempt (lesson 06).
# Set once, as a tuple: nobody can extend the list by accident.


def interroger(base_url, modele, invite, max_jetons=None, essais=3):
    # base_url: engine address without a trailing slash, e.g. "http://127.0.0.1:8011"
    # max_jetons=None: optional cap; None means "not requested"
    # essais=3: three ATTEMPTS at most, not three retries
    if essais < 1:                                    # hypothesis H2:
        raise ErreurModele("no attempt allowed")    # zero attempts = no call

    corps = {"model": modele,                         # the name asked of the engine
             "messages": [{"role": "user",            # a list, a single message
                            "content": invite}]}      # the question, as is
    if max_jetons is not None:                        # only if requested:
        corps["max_tokens"] = max_jetons              # a cap would cut the text

    donnees = json.dumps(corps).encode("utf-8")       # dict -> JSON str -> bytes
    url = base_url + "/v1/chat/completions"           # the dialect's path
    debut = time.monotonic()                          # timer for the WHOLE call

    for essai in range(1, essais + 1):                # essai is 1, 2, ..., essais
        requete = urllib.request.Request(             # rebuilt on every attempt
            url,                                      # destination
            data=donnees,                             # the body: bytes
            headers={"Content-Type": "application/json"},  # announces the format
            method="POST")                            # the dialect's verb
        avant = time.monotonic()                      # timer for THIS attempt
        try:
            with urllib.request.urlopen(requete) as reponse:  # send + wait
                corps_recu = ""                       # the body, stitched as it arrives
                for ligne in reponse:                 # line by line
                    corps_recu += ligne.decode("utf-8")   # bytes -> str, one line at a time
        except urllib.error.HTTPError as e:           # the server DID answer, with an error
            if e.code not in REESSAYABLES:            # 400, 404...: no point retrying
                raise ErreurModele(
                    f"code {e.code} not retryable") from e
            if essai == essais:                       # last attempt reached:
                raise ErreurModele("attempts exhausted") from e  # NO more waiting
            attente = e.headers.get("Retry-After")    # the server knows better
            if attente is not None:
                delai = float(attente)                # e.g. "1" -> 1.0 second
            else:
                delai = 0.1 * 2 ** (essai - 1)        # backoff: 0.1, 0.2, 0.4
            time.sleep(delai)                         # the wait, BETWEEN two attempts
            continue                                  # back to the top of the loop
        except urllib.error.URLError as e:            # AFTER HTTPError: unreachable
            raise ErreurModele("endpoint unreachable") from e
        apres = time.monotonic()                      # end of THIS attempt: the right one

        try:
            charge = json.loads(corps_recu)           # JSON str -> dict
            texte = charge["choices"][0]["message"]["content"]  # the answer
            jetons_entree = charge["usage"]["prompt_tokens"]    # counted by the server
            jetons_sortie = charge["usage"]["completion_tokens"]
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as e:
            raise ErreurModele("malformed response") from e  # a field is missing

        return {"texte": texte,                       # what the model said
                "jetons_entree": jetons_entree,       # usage field
                "jetons_sortie": jetons_sortie,       # usage field
                "secondes": apres - avant,           # service time, successful attempt only
                "secondes_totales": time.monotonic() - debut,  # everything, waits included
                "essais": essai}                     # number of the winning attempt