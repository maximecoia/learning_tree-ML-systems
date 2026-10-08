# flux.py, ex00 of inf-02-prefill-decode: read the streamed answer (SSE)
# and separate the two regimes: the TTFT (prefill) and the gaps between
# tokens (decode).
# Allowed: client, json, statistics, time, urllib, float, max, min, range, len
import json                      # dumps the body, loads each event
import time                      # monotonic: the only reliable clock
import statistics                # the median of the gaps (itl)
import urllib.request            # Request and urlopen
import urllib.error              # HTTPError and URLError
from client import ErreurModele, REESSAYABLES
# ErreurModele: the single exit for every failure.
# REESSAYABLES: the tuple of retryable codes from client.py
# (the statement calls it RETENTABLES; same tuple, only the import differs).

def generer(base_url, modele, invite, max_jetons=None, essais=3):
    # Same contract as interroger, but the answer arrives in fragments.
    if essais < 1:                                   # zero attempts = zero calls
        raise ErreurModele("aucun essai autorisé")
    url = base_url + "/v1/chat/completions"          # the dialect's path
    corps = {"model": modele,
             "messages": [{"role": "user", "content": invite}],
             "stream": True}                         # THE flag that opens the stream
    if max_jetons is not None:                       # only if requested:
        corps["max_tokens"] = max_jetons             # absent key ≠ key set to None
    donnees = json.dumps(corps).encode("utf-8")      # dict -> JSON text -> bytes

    for essai in range(1, essais + 1):               # essai = 1, 2, ..., essais
        requete = urllib.request.Request(            # rebuilt on every attempt
            url,
            data=donnees,
            headers={"Content-Type": "application/json"},
            method="POST")
        debut = time.monotonic()                     # start of THIS attempt
        try:
            reponse = urllib.request.urlopen(requete)
        except urllib.error.HTTPError as e:          # the server answered, with an error
            if e.code not in REESSAYABLES:           # 400, 404...: never retried
                raise ErreurModele(f"code {e.code} non rattrapable") from e
            if essai == essais:                      # last attempt reached:
                raise ErreurModele("essais épuisés") from e   # no sleep after it
            attente = e.headers.get("Retry-After")   # the server knows better
            if attente is not None:
                delai = float(attente)
            else:
                delai = 0.1 * 2 ** (essai - 1)       # 0.1 s; 0.2 s; 0.4 s...
            time.sleep(delai)
            continue                                 # back to the top of the loop
        except urllib.error.URLError as e:           # AFTER HTTPError (its child)
            raise ErreurModele("moteur injoignable") from e

        # ---- the stream: line by line, as it arrives ----
        with reponse:                                # closes the connection on exit
            texte = ""                               # the fragments stitched together
            jetons_sortie = 0                        # counted on fragments CARRYING text
            inter_jetons = []                        # jetons_sortie - 1 values
            ttft = None                              # set once only
            precedent = None                         # time of the previous text fragment
            jetons_entree = 0                        # read from usage, once, at the end
            complet = False                          # becomes true only at [DONE]
            for ligne in reponse:                    # each line as soon as it arrives
                morceau = ligne.decode("utf-8").strip()   # bytes -> text
                if not morceau.startswith("data:"):  # empty line: SSE separator
                    continue
                payload = morceau[len("data:"):].strip()  # strips the "data:" prefix
                if payload == "[DONE]":              # sentinel: this is NOT JSON
                    complet = True                   # the stream went all the way
                    break
                evenement = json.loads(payload)      # one event, not the whole answer
                usage = evenement.get("usage")       # outside delta: carried by the last one
                if usage is not None:
                    jetons_entree = usage.get("prompt_tokens", jetons_entree)
                choices = evenement.get("choices") or []
                if not choices:
                    continue
                delta = choices[0].get("delta") or {}
                fragment = delta.get("content")      # None on the role and on the stop
                if not fragment:                     # no text: not a token
                    continue
                instant = time.monotonic()           # this fragment arrives NOW
                if jetons_sortie == 0:               # first fragment CARRYING text:
                    ttft = instant - debut           #   TTFT = prefill + transport
                else:                                # the following ones:
                    inter_jetons.append(instant - precedent)  # the gap = decode
                precedent = instant
                texte += fragment
                jetons_sortie += 1

        # ---- out of the loop: did the stream go all the way? ----
        if not complet:                              # no [DONE]: truncated stream
            if jetons_sortie == 0 and essai < essais:
                continue                             # failure BEFORE the 1st token: retryable
            raise ErreurModele("flux tronqué sans [DONE]")
            # failure AFTER the 1st token: never retried (it would double the text)
        break                                        # complete stream: leave the attempts

    # ---- the result: the two regimes, separated ----
    itl = statistics.median(inter_jetons) if inter_jetons else None
    # median of the gaps; None with a single token, since no gap exists
    return {"texte": texte,
            "jetons_entree": jetons_entree,          # announced by the server
            "jetons_sortie": jetons_sortie,          # counted on the fragments
            "ttft": ttft,                            # first fragment carrying text
            "inter_jetons": inter_jetons,            # jetons_sortie - 1 values
            "itl": itl,                              # the decode's pace
            "secondes": time.monotonic() - debut,    # start -> end of reading
            "essais": essai}                         # number of the winning attempt
