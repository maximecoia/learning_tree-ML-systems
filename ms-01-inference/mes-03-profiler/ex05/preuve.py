"""preuve.py: actually profile a function, and compare two series of measurements."""

import sys
from time import perf_counter

from temps import attribuer


def profiler(f, horloge=perf_counter):
    """Call f under sys.setprofile and return the attribution of its run,
    as attribuer returns it."""
    events = []

    def hook(frame, event, argument):
        if event == "call":
            events.append(("appel", frame.f_code.co_qualname, horloge()))
        elif event == "return":
            events.append(("retour", frame.f_code.co_qualname, horloge()))

    sys.setprofile(hook)
    try:
        f()
    finally:
        sys.setprofile(None)  # removed even if f raises

    return attribuer(events)


def gain(avant, apres):
    """{'rapport': min(apres) / min(avant), 'incertain': the series overlap}."""
    if not avant or not apres:
        raise ValueError("empty list on one side or the other")
    min_before = min(avant)
    if min_before <= 0:
        raise ValueError("minimum of avant is zero or negative")

    separated = max(avant) < min(apres) or max(apres) < min(avant)
    return {
        "rapport": min(apres) / min_before,
        "incertain": not separated,
    }
