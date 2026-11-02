"""Admission probe during generation: tell continuous from static batching
from the outside, thanks to a control request."""

import time
from concurrent.futures import ThreadPoolExecutor

import charge


def sonder_admission(base_url, modele, invite_longue, invite_courte,
                     jetons_longs, jetons_courts, retard=0.3, timeout=60.0):
    """Probe the scheduling policy of an inference server:
    1. Fire the short request alone on an idle server (control -> latence_seule).
    2. Start the long request, wait `retard` seconds, then start the short one.
    3. Infer the wait due to the policy and return the verdict
       ('continu' if part_attendue < 0.5, 'statique' otherwise)."""

    # 1. Check the parameters before any request is fired.
    if retard < 0:
        raise ValueError("retard must be >= 0")
    if jetons_courts < 1 or jetons_longs < 1:
        raise ValueError("token counts must be >= 1")
    if jetons_courts >= jetons_longs:
        raise ValueError("jetons_courts must be strictly below jetons_longs")

    # 2. The control: the short request fired alone on an idle server.
    #    Without it, a continuous but slow server would pass for static.
    c_seul = charge.tirer(
        base_url, modele, invite_courte,
        concurrence=1, total=1,
        max_jetons=jetons_courts, timeout=timeout,
    )[0]
    if not c_seul["ok"]:
        raise ValueError("the idle control request failed")

    latence_seule = c_seul["latence"]

    # 3. The probe under load: start the long request in the background,
    #    wait `retard` seconds, then start the short one.
    def tirer_avec_horloge(invite, max_j):
        t0 = time.monotonic()
        compte = charge.tirer(
            base_url, modele, invite,
            concurrence=1, total=1,
            max_jetons=max_j, timeout=timeout,
        )[0]
        return t0, compte

    with ThreadPoolExecutor(max_workers=2) as executeur:
        futur_long = executeur.submit(tirer_avec_horloge, invite_longue, jetons_longs)
        time.sleep(retard)
        futur_court = executeur.submit(tirer_avec_horloge, invite_courte, jetons_courts)

        t0_long, c_long = futur_long.result()
        t0_court, c_court = futur_court.result()

    # No admission policy can be read from a failed request.
    if not c_long["ok"] or not c_court["ok"]:
        raise ValueError("a request failed during the probe under load")

    # 4. Re-base the instants on the monotonic clock, relative to the long start.
    origine_long = t0_long + c_long["debut"]
    fin_long = (t0_long + c_long["fin"]) - origine_long

    debut_court = (t0_court + c_court["debut"]) - origine_long
    fin_court = (t0_court + c_court["fin"]) - origine_long

    # Time the long request still had left when the short one started.
    reste_long = fin_long - debut_court
    if reste_long <= 0:
        raise ValueError("the long request finished before the short one started")

    # 5. Isolate the wait due to the policy, then compute the verdict.
    latence_en_charge = c_court["latence"]
    attente = max(0.0, latence_en_charge - latence_seule)
    part_attendue = attente / reste_long

    verdict = "continu" if part_attendue < 0.5 else "statique"

    return {
        "latence_seule": latence_seule,
        "latence_en_charge": latence_en_charge,
        "attente": attente,
        "fin_long": fin_long,
        "fin_court": fin_court,
        "reste_long": reste_long,
        "part_attendue": part_attendue,
        "verdict": verdict,
    }