"""Canonical execution errors."""


def error(kind, message, hint=None):
    value = {"kind": kind, "message": message}
    if hint:
        value["hint"] = hint
    return value
