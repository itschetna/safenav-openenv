def _normalize(x):
    """Ensure input is always a string"""
    if isinstance(x, list):
        return " ".join(map(str, x)).lower()
    return str(x).lower()


def grade_easy(output):
    o = _normalize(output)
    return 1.0 if "route_2" in o else 0.0


def grade_medium(output):
    o = _normalize(output)
    return 1.0 if "route_2" in o else 0.0


def grade_hard(output):
    o = _normalize(output)
    return 1.0 if ("analyze" in o and "route_2" in o) else 0.0