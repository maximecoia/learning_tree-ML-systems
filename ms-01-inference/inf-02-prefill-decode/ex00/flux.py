# flux.py — ex00 d'inf-02-prefill-decode
# Lire la réponse en flux (SSE) et séparer les deux régimes :
# le TTFT (prefill) et les écarts entre jetons (decode).
# Autorisé : client, json, statistics, time, urllib, float, max, min, range, len
import json                      # dumps le corps, loads chaque évènement
import time                      # monotonic : la seule horloge fiable
import statistics                # la médiane des écarts (itl)
import urllib.request            # Request et urlopen
import urllib.error              # HTTPError et URLError
from client import ErreurModele, REESSAYABLES
# ErreurModele : l'unique porte de sortie des échecs.
# REESSAYABLES : la tuple des codes rattrapables de client.py
# (le sujet l'appelle RETENTABLES ; même tuple, seul l'import change).

def generer(base_url, modele, invite, max_jetons=None, essais=3):
    # Même contrat qu'interroger, mais la réponse arrive en fragments.
    if essais < 1:                                   # zéro essai = zéro appel
        raise ErreurModele("aucun essai autorisé")
    url = base_url + "/v1/chat/completions"          # le chemin du dialecte
    corps = {"model": modele,
             "messages": [{"role": "user", "content": invite}],
             "stream": True}                         # LE drapeau qui ouvre le flux
    if max_jetons is not None:                       # seulement si demandé :
        corps["max_tokens"] = max_jetons             # clé absente ≠ clé à None
    donnees = json.dumps(corps).encode("utf-8")      # dict -> texte JSON -> octets

    for essai in range(1, essais + 1):               # essai = 1, 2, ..., essais
        requete = urllib.request.Request(            # reconstruite à chaque essai
            url,
            data=donnees,
            headers={"Content-Type": "application/json"},
            method="POST")
        debut = time.monotonic()                     # départ de CET essai
        try:
            reponse = urllib.request.urlopen(requete)
        except urllib.error.HTTPError as e:          # le serveur a répondu, en erreur
            if e.code not in REESSAYABLES:           # 400, 404... : jamais réessayé
                raise ErreurModele(f"code {e.code} non rattrapable") from e
            if essai == essais:                      # dernier essai atteint :
                raise ErreurModele("essais épuisés") from e   # on ne dort pas après
            attente = e.headers.get("Retry-After")   # le serveur sait mieux
            if attente is not None:
                delai = float(attente)
            else:
                delai = 0.1 * 2 ** (essai - 1)       # 0,1 s ; 0,2 s ; 0,4 s...
            time.sleep(delai)
            continue                                 # on repart en haut de boucle
        except urllib.error.URLError as e:           # APRÈS HTTPError (son enfant)
            raise ErreurModele("moteur injoignable") from e

        # ---- le flux : ligne à ligne, à mesure qu'il arrive ----
        with reponse:                                # ferme la connexion en sortant
            texte = ""                               # les fragments recollés
            jetons_sortie = 0                        # compté sur les fragments PORTANT du texte
            inter_jetons = []                        # jetons_sortie - 1 valeurs
            ttft = None                              # figé une seule fois
            precedent = None                         # instant du fragment texte précédent
            jetons_entree = 0                        # lu dans usage, une fois, à la fin
            complet = False                          # ne devient vrai qu'à [DONE]
            for ligne in reponse:                    # chaque ligne dès qu'elle arrive
                morceau = ligne.decode("utf-8").strip()   # octets -> texte
                if not morceau.startswith("data:"):  # ligne vide : séparateur SSE
                    continue
                payload = morceau[len("data:"):].strip()  # retire le préfixe "data:"
                if payload == "[DONE]":              # sentinelle : ce n'est PAS du JSON
                    complet = True                   # le flux est allé au bout
                    break
                evenement = json.loads(payload)      # un évènement, pas toute la réponse
                usage = evenement.get("usage")       # hors delta : porté par le dernier
                if usage is not None:
                    jetons_entree = usage.get("prompt_tokens", jetons_entree)
                choices = evenement.get("choices") or []
                if not choices:
                    continue
                delta = choices[0].get("delta") or {}
                fragment = delta.get("content")      # None au rôle comme à l'arrêt
                if not fragment:                     # pas de texte : pas un jeton
                    continue
                instant = time.monotonic()           # ce fragment arrive MAINTENANT
                if jetons_sortie == 0:               # premier fragment PORTEUR de texte :
                    ttft = instant - debut           #   TTFT = prefill + transport
                else:                                # les suivants :
                    inter_jetons.append(instant - precedent)  # l'écart = decode
                precedent = instant
                texte += fragment
                jetons_sortie += 1

        # ---- sorti de boucle : le flux est-il allé au bout ? ----
        if not complet:                              # pas de [DONE] : flux tronqué
            if jetons_sortie == 0 and essai < essais:
                continue                             # panne AVANT le 1er jeton : réessayable
            raise ErreurModele("flux tronqué sans [DONE]")
            # panne APRÈS le 1er jeton : jamais réessayée (doublerait le texte)
        break                                        # flux complet : on sort des essais

    # ---- le rendu : les deux régimes, séparés ----
    itl = statistics.median(inter_jetons) if inter_jetons else None
    # médiane des écarts ; None à un seul jeton, car aucun écart n'existe
    return {"texte": texte,
            "jetons_entree": jetons_entree,          # annoncé par le serveur
            "jetons_sortie": jetons_sortie,          # compté sur les fragments
            "ttft": ttft,                            # premier fragment porteur de texte
            "inter_jetons": inter_jetons,            # jetons_sortie - 1 valeurs
            "itl": itl,                              # la cadence du decode
            "secondes": time.monotonic() - debut,    # départ -> fin de lecture
            "essais": essai}                         # le numéro de l'essai gagnant