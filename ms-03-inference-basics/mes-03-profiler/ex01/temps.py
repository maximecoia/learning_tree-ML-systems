"""temps.py: self time and cumulative time of each function."""

from profileur import verifier


def attribuer(evenements):
    """Return a dict name -> {'appels', 'propre', 'cumule'},
    in order of first call."""
    verifier(evenements)  # inconsistent trace -> ValueError

    result = {}
    stack = []  # each entry: [name, call time, time of direct children]

    for kind, name, timestamp in evenements:
        if kind == "appel":
            if name not in result:
                result[name] = {"appels": 0, "propre": 0.0, "cumule": 0.0}
            result[name]["appels"] += 1
            stack.append([name, timestamp, 0.0])
        elif kind == "retour":
            _, start, children = stack.pop()
            duration = timestamp - start

            # time spent in its own lines: the duration, minus the children
            result[name]["propre"] += duration - children

            # cumulative: an interval already inside a call of the same name
            # still open further down is not counted again (recursion)
            if all(n != name for n, _, _ in stack):
                result[name]["cumule"] += duration

            # this duration becomes child time for the caller
            if stack:
                stack[-1][2] += duration

    return result
