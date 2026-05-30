"""Intended solver: recover (a, b) exactly from two adjacent observations.

solve(oracle) is called by scripts/tour.py with a fresh Oracle instance.
"""


def solve(oracle):
    b = oracle.query("evaluate", x=0)              # f(0) = b mod M
    y1 = oracle.query("evaluate", x=1)             # f(1) = (a + b) mod M
    a = (y1 - b) % oracle.M                         # a = f(1) - f(0)  (mod M)
    # Validate against one more point before committing.
    y2 = oracle.query("evaluate", x=2)
    assert y2 == (a * 2 + b) % oracle.M
    return [a, b]
