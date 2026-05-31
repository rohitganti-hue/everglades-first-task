# Sample task — "the modular black box" (TEACHING FIXTURE)

**Do NOT submit this task.** It exists only so a new expert can tour a finished,
known-good inverse task. It is intentionally domain-neutral synthetic — no science
background required — so the *reasoning pattern* is what comes through.

- **Hidden rule:** the oracle computes `f(x) = (a*x + b) mod 97` for hidden integers `a`, `b`.
- **Solver's job:** recover `(a, b)` within a 6-query budget.
- **The trap:** assume the rule is an ordinary straight line and ignore the modulus.

> config.yaml records the task's direction (inverse) and domain — the same metadata you
> set in the RLS UI when you submit a real task.
