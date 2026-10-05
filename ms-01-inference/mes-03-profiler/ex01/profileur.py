def verifier(evenements):
    """Return the list unchanged if it balances, raise ValueError otherwise."""
    stack = []  # names of the calls currently open

    for kind, name, timestamp in evenements:
        if kind == "appel":
            stack.append(name)          # a call opens: push it
        elif kind == "retour":
            if not stack:
                raise ValueError("return with no open call")
            if stack.pop() != name:
                raise ValueError("return does not match the most recent open call")
        else:
            raise ValueError(f"unknown kind: {kind}")

    if stack:
        raise ValueError("calls still open at the end of the trace")

    return evenements


def compter(evenements):
    """Return a dict name -> number of calls, in order of first call."""
    verifier(evenements)  # inconsistent trace -> ValueError -> nothing is counted

    counts = {}
    for kind, name, timestamp in evenements:
        if kind == "appel":
            if name in counts:
                counts[name] += 1       # name already seen: one more call
            else:
                counts[name] = 1        # first call: create the key
    return counts
