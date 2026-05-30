# The modular black box

You are given access to a black box. It accepts one integer `x` and returns one integer.
Internally it computes:

```
output = (a * x + b) mod 97
```

where `a` and `b` are fixed whole numbers you cannot see, and `97` is a known modulus.

You may call the box in two ways:

- `evaluate(x)` — returns the box's output for your chosen `x`. You may call this at most
  **6 times** in total.
- `help(question)` — returns a general hint. It will never tell you `a` or `b`.

**Your task:** report the pair `(a, b)`.

Spend your evaluations deliberately. A solver who treats the box as an ordinary straight
line — fitting a slope from two widely-spaced points — can be misled when the internal
result wraps past the modulus between those points.
