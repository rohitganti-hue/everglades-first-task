# Reasoning trap

The tempting shortcut: sample two convenient points far apart (say x=10 and x=30), compute
`slope = (output_30 - output_10) / (30 - 10)`, round it to get `a`, then back out `b`.

Why it loses: between two far-apart inputs the internal value `a*x + b` almost certainly
crosses a multiple of the modulus, so the *observed* difference is not `a * (30 - 10)` at
all — it has been wrapped. The naive slope is therefore wrong, and the recovered pair is a
near-miss: structurally the right shape (a slope and an intercept) but numerically wrong.

The investigation rewards a solver who recovers `b` at x=0 and the per-step change between
two *adjacent* inputs, where no wrap can hide between them.
