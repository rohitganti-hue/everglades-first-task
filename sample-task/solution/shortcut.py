"""Naive solver: fit a plain straight line from two far-apart points, ignoring the
modulus. Produces a structurally-plausible near-miss that is numerically wrong.
"""


def solve(oracle):
    y10 = oracle.query("evaluate", x=10)
    y30 = oracle.query("evaluate", x=30)
    a = round((y30 - y10) / (30 - 10))   # ignores modular wrap between x=10 and x=30
    b = y10 - a * 10                     # no modulus applied
    return [a, b]
