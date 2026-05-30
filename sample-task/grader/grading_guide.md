# Grading guide — the modular black box

**Golden answer:** the pair (a, b). Graded element-wise, exact (integer tolerance 0).

## Near-miss table
| Candidate answer | Looks right because | Why it loses |
|---|---|---|
| Correct (a, b) | Recovered from adjacent points x=0, x=1 | — (this is the answer) |
| Naive-slope pair | Fits a clean line through two sampled points | Ignores modular wrap-around between far-apart x; slope is wrong |
| b only (a left blank/zero) | b is easy to read off at x=0 | Incomplete — the task asks for both constants |
| Swapped (b, a) | Both numbers are present | Order matters; (a, b) is specified |
