# everglades-first-task Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a standalone Claude Code skill, `everglades-first-task`, that onboards a net-new Project Everglades expert by giving a hands-on guided tour of one complete, frozen, known-good sample inverse task, then graduates them to `everglades-multitask`.

**Architecture:** A self-contained git repo. A `sample-task/` fixture (a synthetic "modular black box" inverse task) is the teaching object. A stdlib-only `scripts/tour.py` lets the expert run the local calibration checks themselves (`verify`/`shortcut`/`lint`/`preview`) and includes a `selftest` that guards the fixture. `SKILL.md` is the 6-stage script Claude follows; `reference/concepts.md` holds the teaching prose. No dependency on `everglades-multitask`, no API key, no network calls.

**Tech Stack:** Python 3 standard library only (`importlib`, `json`, `argparse`, `re`, `random`). Markdown for SKILL.md / docs. Git.

---

## File structure

```
everglades-first-task/
├── README.md                         # Task 1
├── .gitignore                        # Task 1
├── sample-task/
│   ├── README.md                     # Task 2  ("teaching fixture — do NOT submit")
│   ├── config.yaml                   # Task 2
│   ├── BRIEF.md                      # Task 2
│   ├── STATE.md                      # Task 2
│   ├── problem.md                    # Task 2  (solver-facing; MUST NOT contain "23" or "58")
│   ├── reasoning_trap.md             # Task 2  (solver-facing; MUST NOT contain "23" or "58")
│   ├── grader/grading_guide.md       # Task 2
│   ├── golden/expected.json          # Task 2
│   ├── runs/preview_canned.json      # Task 2
│   ├── oracle/setup.py               # Task 3  (hidden system: a=23, b=58, mod 97, budget 6)
│   └── solution/
│       ├── main.py                   # Task 3  (intended solver — PASSES)
│       └── shortcut.py               # Task 3  (naive solver — FAILS)
├── scripts/tour.py                   # Task 4  (check_answer + verify/shortcut/lint/preview/selftest)
├── reference/concepts.md             # Task 5
└── SKILL.md                          # Task 6
```

The repo and `docs/superpowers/specs/2026-05-30-everglades-first-task-onboarding-design.md` already exist (created during brainstorming). Work happens at repo root `/Users/rohitganti/Desktop/Brain/Everglades/everglades-first-task`.

**On testing:** This repo intentionally has no pytest suite (consistent with keeping it lean and expert-facing, like `everglades-multitask`). The regression guard is the single `scripts/tour.py selftest` subcommand, which asserts the fixture's invariants (verify passes / shortcut fails / lint clean / canned preview ≤2/8). Tasks are ordered so the fixture exists before the runner, and the runner is built test-first: `selftest` is written first and used as the failing→passing signal.

---

### Task 1: Repo scaffolding

**Files:**
- Create: `README.md`
- Create: `.gitignore`

- [ ] **Step 1: Write `README.md`**

```markdown
# everglades-first-task

A Claude Code skill that onboards a **net-new Project Everglades expert** — someone who
has never authored a task. It is a ~20-minute, hands-on guided tour of one complete,
known-good **sample inverse task**: you read each artifact, run the local calibration
checks yourself, and watch the signals fire. Then you graduate to
[`everglades-multitask`](https://github.com/rohitganti-hue/everglades-multitask) to build
your own first task.

This skill authors nothing you submit. The bundled `sample-task/` is a **teaching fixture**.

## Start

In Claude Code, say **"onboard me to Everglades"** or run **`/everglades-first-task`**.

Or drive the tour by hand:

```bash
python3 scripts/tour.py verify     # intended solver passes
python3 scripts/tour.py shortcut   # naive solver fails (as it must)
python3 scripts/tour.py lint       # solver-facing text never leaks the answer
python3 scripts/tour.py preview    # recorded Opus×8 calibration result (≤2/8)
python3 scripts/tour.py selftest   # asserts all of the above (fixture regression guard)
```

No API key, no config, no network — Python 3 standard library only.

## What's inside

- `sample-task/` — a domain-neutral synthetic inverse task (recover a hidden modular rule)
- `scripts/tour.py` — the hands-on driver
- `reference/concepts.md` — inverse-task concepts, the 8-step playbook, the ≤2/8 gate, AI Use Policy
- `SKILL.md` — the onboarding flow Claude follows
```

- [ ] **Step 2: Write `.gitignore`**

```
# Python
__pycache__/
*.pyc

# IDE / OS
.vscode/
.idea/
*.swp
.DS_Store
```

- [ ] **Step 3: Commit**

```bash
cd /Users/rohitganti/Desktop/Brain/Everglades/everglades-first-task
git add README.md .gitignore
git commit -m "Scaffold everglades-first-task repo (README + gitignore)"
```

---

### Task 2: Sample-task static content (the fixture's non-code files)

**Files:**
- Create: `sample-task/README.md`
- Create: `sample-task/config.yaml`
- Create: `sample-task/BRIEF.md`
- Create: `sample-task/STATE.md`
- Create: `sample-task/problem.md`
- Create: `sample-task/reasoning_trap.md`
- Create: `sample-task/grader/grading_guide.md`
- Create: `sample-task/golden/expected.json`
- Create: `sample-task/runs/preview_canned.json`

> **Invariant for solver-facing files:** `problem.md` and `reasoning_trap.md` MUST NOT contain the substrings `23` or `58` (the hidden answer values). The modulus `97` and budget `6` are known to the solver and are fine.

- [ ] **Step 1: Write `sample-task/README.md`**

```markdown
# Sample task — "the modular black box" (TEACHING FIXTURE)

**Do NOT submit this task.** It exists only so a new expert can tour a finished,
known-good inverse task. It is intentionally domain-neutral synthetic — no science
background required — so the *reasoning pattern* is what comes through.

- **Hidden rule:** the oracle computes `f(x) = (a*x + b) mod 97` for hidden integers `a`, `b`.
- **Solver's job:** recover `(a, b)` within a 6-query budget.
- **The trap:** assume the rule is an ordinary straight line and ignore the modulus.
```

- [ ] **Step 2: Write `sample-task/config.yaml`**

```yaml
direction: inverse
domain: Samples
title: The modular black box
```

- [ ] **Step 3: Write `sample-task/BRIEF.md`**

```markdown
# BRIEF — the modular black box

One paragraph, in the author's words, of what this task investigates:

> There is a black box that turns a whole number into another whole number. Under the
> hood it multiplies by one hidden constant, adds a second hidden constant, and wraps the
> result around a known modulus. The solver can poke the box a handful of times and must
> recover both hidden constants. The investigation is interesting because the wrap-around
> is invisible in the outputs — a solver who assumes a plain straight line will be fooled.
```

- [ ] **Step 4: Write `sample-task/STATE.md`**

```markdown
# STATE — the modular black box

## Why this is the only answer
The box is fully determined by the pair (a, b) under the known modulus. Two clean
observations at x=0 and x=1 pin both constants exactly: f(0) gives b, and f(1) - f(0)
gives a (mod the modulus). No other (a, b) pair reproduces those two outputs. The answer
is therefore unique and stable — it does not depend on which extra points you sample.

## Order of decisions
1. Establish the modulus is known and the form is (a*x + b) mod m. (given in problem.md)
2. Recover b first (it is the output at x=0).
3. Recover a from the change between x=0 and x=1, reduced by the modulus.
4. Validate against one more point before committing.

## State
CALIBRATED — intended solver passes, naive shortcut fails, preview recorded at 1/8.
```

- [ ] **Step 5: Write `sample-task/problem.md`** (solver-facing — no `23`/`58`)

```markdown
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
```

- [ ] **Step 6: Write `sample-task/reasoning_trap.md`** (solver-facing — no `23`/`58`)

```markdown
# Reasoning trap

The tempting shortcut: sample two convenient points far apart (say x=10 and x=30), compute
`slope = (output_30 - output_10) / (30 - 10)`, round it to get `a`, then back out `b`.

Why it loses: between two far-apart inputs the internal value `a*x + b` almost certainly
crosses a multiple of the modulus, so the *observed* difference is not `a * (30 - 10)` at
all — it has been wrapped. The naive slope is therefore wrong, and the recovered pair is a
near-miss: structurally the right shape (a slope and an intercept) but numerically wrong.

The investigation rewards a solver who recovers `b` at x=0 and the per-step change between
two *adjacent* inputs, where no wrap can hide between them.
```

- [ ] **Step 7: Write `sample-task/grader/grading_guide.md`**

```markdown
# Grading guide — the modular black box

**Golden answer:** the pair (a, b). Graded element-wise, exact (integer tolerance 0).

## Near-miss table
| Candidate answer | Looks right because | Why it loses |
|---|---|---|
| Correct (a, b) | Recovered from adjacent points x=0, x=1 | — (this is the answer) |
| Naive-slope pair | Fits a clean line through two sampled points | Ignores modular wrap-around between far-apart x; slope is wrong |
| b only (a left blank/zero) | b is easy to read off at x=0 | Incomplete — the task asks for both constants |
| Swapped (b, a) | Both numbers are present | Order matters; (a, b) is specified |
```

- [ ] **Step 8: Write `sample-task/golden/expected.json`**

```json
{
  "answer": [23, 58],
  "tolerance": 0
}
```

- [ ] **Step 9: Write `sample-task/runs/preview_canned.json`**

```json
{
  "draft": "sample-modular-black-box",
  "model": "claude-opus-4-7",
  "attempts": 8,
  "passed": 1,
  "classification": "IN_RANGE",
  "ran_at": "2026-05-28T00:00:00+00:00",
  "note": "Recorded for onboarding. 1/8 <= 2/8 means appropriately hard for the 16-model Taiga ensemble."
}
```

- [ ] **Step 10: Verify the no-leak invariant by hand**

Run: `grep -nE "\b(23|58)\b" sample-task/problem.md sample-task/reasoning_trap.md`
Expected: no matches (exit code 1, no output). If anything matches, reword that line.

- [ ] **Step 11: Commit**

```bash
git add sample-task/README.md sample-task/config.yaml sample-task/BRIEF.md sample-task/STATE.md \
        sample-task/problem.md sample-task/reasoning_trap.md sample-task/grader/grading_guide.md \
        sample-task/golden/expected.json sample-task/runs/preview_canned.json
git commit -m "Add sample-task fixture: static content (brief, state, problem, grader, golden)"
```

---

### Task 3: Sample-task code (oracle + two solvers)

**Files:**
- Create: `sample-task/oracle/setup.py`
- Create: `sample-task/solution/main.py`
- Create: `sample-task/solution/shortcut.py`

- [ ] **Step 1: Write `sample-task/oracle/setup.py`**

```python
"""Hidden system for the sample inverse task (TEACHING FIXTURE).

The box computes f(x) = (A*x + B) mod M for hidden A, B. The solver never sees A or B;
it only sees outputs from evaluate(), under a query budget, plus non-committal help().

A fresh Oracle() is created per solver run, so module-level state is never shared across
runs (the same isolation everglades-multitask's preview eval requires per attempt).
"""
import random


class Oracle:
    M = 97          # known modulus (stated in problem.md)
    BUDGET = 6      # evaluate() calls allowed
    _A = 23         # hidden
    _B = 58         # hidden

    def __init__(self):
        self._used = 0
        self._rng = random.Random(42)  # seeded: deterministic noise for the 'sample' mode

    def _spend(self):
        if self._used >= self.BUDGET:
            raise RuntimeError("Query budget exceeded (6 evaluate calls).")
        self._used += 1

    def query(self, mode, x=None):
        if mode == "evaluate":
            self._spend()
            return (self._A * x + self._B) % self.M
        if mode == "sample":
            # A noisy reading: realistic but deterministic via the seeded RNG.
            self._spend()
            noise = self._rng.choice([-1, 0, 1])
            return ((self._A * x + self._B) % self.M + noise) % self.M
        if mode == "help":
            return ("Hint: the output you read may have wrapped around the modulus. "
                    "Adjacent inputs leave no room for a hidden wrap between them. "
                    "(This hint does not reveal the constants.)")
        raise ValueError(f"Unknown mode: {mode!r}")
```

- [ ] **Step 2: Write `sample-task/solution/main.py`** (intended solver — passes)

```python
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
```

- [ ] **Step 3: Write `sample-task/solution/shortcut.py`** (naive solver — fails)

```python
"""Naive solver: fit a plain straight line from two far-apart points, ignoring the
modulus. Produces a structurally-plausible near-miss that is numerically wrong.
"""


def solve(oracle):
    y10 = oracle.query("evaluate", x=10)
    y30 = oracle.query("evaluate", x=30)
    a = round((y30 - y10) / (30 - 10))   # ignores modular wrap between x=10 and x=30
    b = y10 - a * 10                     # no modulus applied
    return [a, b]
```

- [ ] **Step 4: Sanity-check by hand (no runner yet)**

Run:
```bash
cd /Users/rohitganti/Desktop/Brain/Everglades/everglades-first-task
python3 -c "
import importlib.util
def load(p,n):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
o=load('sample-task/oracle/setup.py','o'); m=load('sample-task/solution/main.py','m'); sc=load('sample-task/solution/shortcut.py','sc')
print('main   ->', m.solve(o.Oracle()))
print('short  ->', sc.solve(o.Oracle()))
"
```
Expected: `main   -> [23, 58]` and `short  -> [<something other than [23, 58]>]`.

- [ ] **Step 5: Commit**

```bash
git add sample-task/oracle/setup.py sample-task/solution/main.py sample-task/solution/shortcut.py
git commit -m "Add sample-task code: oracle + intended solver (passes) + shortcut (fails)"
```

---

### Task 4: The hands-on driver `scripts/tour.py` (test-first via selftest)

**Files:**
- Create: `scripts/tour.py`

- [ ] **Step 1: Write `scripts/tour.py` with `check_answer`, loaders, all subcommands, and `selftest`**

```python
#!/usr/bin/env python3
"""tour.py — hands-on driver for the everglades-first-task onboarding tour.

Standard library only. No API key, no config, no network. Each subcommand prints the raw
result plus a short teaching note.

  verify    intended solver vs oracle           -> expect PASS
  shortcut  naive solver vs oracle              -> expect FAIL (as it must)
  lint      leak scan of solver-facing text     -> expect CLEAN
  preview   print the recorded Opus x8 result   -> 1/8 (<= 2/8)
  selftest  run all four and assert outcomes    -> fixture regression guard
"""
import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAMPLE = ROOT / "sample-task"


def _load(rel_path, mod_name):
    path = SAMPLE / rel_path
    spec = importlib.util.spec_from_file_location(mod_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _expected():
    return json.loads((SAMPLE / "golden" / "expected.json").read_text())


def check_answer(submitted, expected: dict) -> bool:
    """Scalar or sequence comparison with element-wise numeric tolerance."""
    target = expected["answer"]
    tol = expected.get("tolerance", 0)
    if isinstance(target, (list, tuple)):
        if not isinstance(submitted, (list, tuple)):
            return False
        if len(submitted) != len(target):
            return False
        try:
            return all(abs(float(s) - float(t)) <= tol for s, t in zip(submitted, target))
        except (TypeError, ValueError):
            return list(submitted) == list(target)
    try:
        return abs(float(submitted) - float(target)) <= tol
    except (TypeError, ValueError):
        return str(submitted).strip() == str(target).strip()


def verify() -> bool:
    oracle_mod = _load("oracle/setup.py", "sample_oracle_v")
    main_mod = _load("solution/main.py", "sample_main_v")
    result = main_mod.solve(oracle_mod.Oracle())
    ok = check_answer(result, _expected())
    print(f"verify : main.py returned {result} -> {'PASS' if ok else 'FAIL'}")
    print("  note : the intended investigation recovers the hidden rule exactly.")
    return ok


def shortcut() -> bool:
    oracle_mod = _load("oracle/setup.py", "sample_oracle_s")
    sc_mod = _load("solution/shortcut.py", "sample_shortcut_s")
    result = sc_mod.solve(oracle_mod.Oracle())
    ok = check_answer(result, _expected())
    print(f"shortcut : shortcut.py returned {result} -> {'PASS' if ok else 'FAIL'}")
    print(f"  note   : a naive solver must FAIL. It hit a near-miss; the answer was "
          f"{_expected()['answer']}.")
    return not ok  # success of this check = the shortcut failed


def lint() -> bool:
    answer_tokens = [str(v) for v in _expected()["answer"]]
    surface = ((SAMPLE / "problem.md").read_text()
               + "\n" + (SAMPLE / "reasoning_trap.md").read_text())
    leaks = [t for t in answer_tokens if re.search(rf"\b{re.escape(t)}\b", surface)]
    clean = not leaks
    print(f"lint : solver-facing text leak scan -> {'CLEAN' if clean else 'LEAK: ' + str(leaks)}")
    print("  note : the prompt and trap the solver reads never name the answer.")
    return clean


def preview() -> dict:
    data = json.loads((SAMPLE / "runs" / "preview_canned.json").read_text())
    print(f"preview : recorded {data['passed']}/{data['attempts']} pass "
          f"({data['classification']}) with {data['model']}")
    print(f"  note  : <= 2/8 means appropriately hard for the 16-model Taiga ensemble.")
    return data


def selftest() -> bool:
    print("=== selftest: asserting the fixture's invariants ===")
    v = verify()
    s = shortcut()
    l = lint()
    p = preview()
    checks = {
        "verify passes": v is True,
        "shortcut fails": s is True,
        "lint clean": l is True,
        "preview <= 2/8": p["passed"] <= 2,
    }
    print("---")
    for name, passed in checks.items():
        print(f"  [{'OK' if passed else 'XX'}] {name}")
    all_ok = all(checks.values())
    print(f"=== selftest {'PASSED' if all_ok else 'FAILED'} ===")
    return all_ok


COMMANDS = {
    "verify": lambda: verify(),
    "shortcut": lambda: shortcut(),
    "lint": lambda: lint(),
    "preview": lambda: preview(),
    "selftest": lambda: selftest(),
}


def main(argv=None):
    p = argparse.ArgumentParser(description="everglades-first-task tour driver")
    p.add_argument("command", choices=list(COMMANDS.keys()))
    args = p.parse_args(argv)
    result = COMMANDS[args.command]()
    if args.command == "selftest" and result is not True:
        sys.exit(1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run selftest — the test-first signal**

Run: `python3 scripts/tour.py selftest`
Expected: ends with `=== selftest PASSED ===`, and all four checks show `[OK]`:
`verify passes`, `shortcut fails`, `lint clean`, `preview <= 2/8`.

If `verify passes` is `[XX]`: the oracle/main mismatch — re-check Task 3. If `shortcut fails` is `[XX]`: the naive solver accidentally matched — re-check `shortcut.py` in Task 3. If `lint clean` is `[XX]`: `problem.md`/`reasoning_trap.md` contain `23` or `58` — reword (Task 2, Step 10).

- [ ] **Step 3: Run each subcommand individually to confirm the teaching output reads well**

Run:
```bash
python3 scripts/tour.py verify
python3 scripts/tour.py shortcut
python3 scripts/tour.py lint
python3 scripts/tour.py preview
```
Expected: `verify` prints `PASS`; `shortcut` prints `FAIL` with the near-miss note; `lint` prints `CLEAN`; `preview` prints `1/8 pass (IN_RANGE)`.

- [ ] **Step 4: Commit**

```bash
git add scripts/tour.py
git commit -m "Add tour.py driver: verify/shortcut/lint/preview + selftest regression guard"
```

---

### Task 5: Teaching reference `reference/concepts.md`

**Files:**
- Create: `reference/concepts.md`

- [ ] **Step 1: Write `reference/concepts.md`**

````markdown
# Everglades concepts — for your first task

## What an inverse task is
An inverse task is **not** a normal task with the answer hidden. It is a small
investigation. The solver can see the evidence, but not the rule that makes one answer
right and the others wrong. In the sample, the solver sees the box's outputs but not the
modular rule behind them.

## The 8-step Inverse Task Playbook (overview)
1. **Lock the answer first** — write the exact answer and why it's the only one. (`STATE.md`)
2. **Order the decisions** — what must be known first, what comes later. (`STATE.md`)
3. **Give each candidate a job** — for every plausible wrong answer, one line on why it
   loses; at least one should look good at first. (`grader/grading_guide.md`)
4. **Plan the wrong paths** — catalogue the shortcuts a weak solver takes. (`shortcut.py`)
5. **Build the files** — oracle + main + shortcut. Claude may help with code.
6. **Design the oracle and the budget** — observations not judgments; a budget tight
   enough that brute force loses; a help mode that doesn't recommend. (`oracle/setup.py`)
7. **Calibrate** — main passes, shortcut fails, preview ≤ 2/8.
8. **Write the prompt** — the solver-facing `problem.md`, in the expert's own words.

Map this to the sample you toured: each artifact came from one of these steps.

## The calibration signals (what tour.py shows you)
- **verify** — the intended `main.py` must recover the golden answer.
- **shortcut** — the naive `shortcut.py` must FAIL. If a shortcut passes, the task is too
  easy or leaks.
- **lint** — the solver-facing text must never name the answer.
- **preview** — Opus × 8 attempts. **≤ 2/8 pass = in range** (appropriately hard for the
  real 16-model Taiga ensemble). 3/8 is borderline; 4+/8 is too easy — go harden.

## AI Use Policy (read before your real task)
- Claude **may** help you write code: `oracle/setup.py`, `solution/main.py`,
  `solution/shortcut.py`.
- Claude **may not** write the science: your prompt (`problem.md`), your explanation, your
  grading guidance, or your reasoning-trap content. Those must be your own words.

## How a finished task reaches the platform
The skill is local-only. When a task is calibrated you copy-paste each file into the RLS
web UI (https://studio.mercor.com/) and click magic-star → STEM Software Runner there to
launch the real Taiga eval. `everglades-multitask` writes a MANIFEST telling you which file
goes in which field.
````

- [ ] **Step 2: Verify it renders and has no broken claims**

Run: `python3 -c "print(open('reference/concepts.md').read()[:200])"`
Expected: prints the first lines without error.

- [ ] **Step 3: Commit**

```bash
git add reference/concepts.md
git commit -m "Add concepts.md: inverse-task framing, 8-step playbook, signals, AI Use Policy"
```

---

### Task 6: `SKILL.md` — the onboarding flow

**Files:**
- Create: `SKILL.md`

- [ ] **Step 1: Write `SKILL.md`**

````markdown
---
name: everglades-first-task
description: Onboard a net-new Project Everglades expert who has never written a task. A ~20-minute, hands-on guided tour of one complete known-good sample inverse task — read each artifact, then run the local calibration checks yourself (verify, shortcut, lint, preview) to watch the signals fire — followed by a handoff to the everglades-multitask skill for the expert's real first task. Use when an expert says "/everglades-first-task", "onboard me to Everglades", "I've never written an Everglades task", "I'm new to Everglades", or "where do I start with Everglades". This skill makes ZERO API or network calls and authors nothing submittable; the bundled sample-task/ is a teaching fixture.
---

# Everglades First Task — onboarding

You are onboarding an expert who has **never authored an Everglades task**. Your job is to
walk them through the finished sample task in this skill, hands-on, until they have the
mental model, then graduate them to `everglades-multitask`. Be warm, concrete, and brief —
this should take about 20 minutes.

## Hard rules
- **This is a tour, not authoring.** Everything in `sample-task/` is a frozen teaching
  fixture. Do not edit it, and tell the expert it is not submittable.
- **Hands-on beats lecture.** At Stage 4, have the expert run the `tour.py` commands
  themselves and react to the real output. Do not paste output you invented.
- **No API, no network, no config.** `tour.py` is stdlib-only and needs no Anthropic key.
- **One stage at a time.** Don't dump all six stages at once. Move when they're ready.

## Reference
- `reference/concepts.md` — the teaching prose (inverse-task framing, the 8-step playbook,
  the calibration signals, the AI Use Policy, the copy-paste-to-RLS model). Pull from it;
  don't reinvent it.
- `sample-task/` — the artifacts you tour, stage by stage.

## The flow (6 stages)

### Stage 1 — Welcome + mental model
Set expectations: ~20 min, hands-on, ends by pointing them at the real tool. Then give the
core idea in your own words from `reference/concepts.md` → "What an inverse task is": *not a
normal task with the answer hidden — a small investigation; the solver sees the evidence,
not the rule.* Use the sample one-liner: a black box computing `(a*x + b) mod 97`; recover
`(a, b)`.

### Stage 2 — The finished task, top-down
Open `sample-task/BRIEF.md` then `sample-task/STATE.md`. Teach **lock the answer first**,
the **order of decisions**, and the **"why this is the only answer"** section. Connect:
this is playbook Steps 1–2.

### Stage 3 — Seen vs. hidden
Contrast what the solver sees with what's hidden:
- `sample-task/problem.md` — the solver-facing prompt (what they get).
- `sample-task/oracle/setup.py` — the hidden system: modes, the 6-query budget, the help
  mode that hints but never recommends, seeded noise.
- `sample-task/grader/grading_guide.md` — the near-miss table (playbook Step 3).
- `sample-task/golden/expected.json` — the locked answer.
Emphasize the reasoning trap in `sample-task/reasoning_trap.md`: the naive line-fit ignores
the modulus.

### Stage 4 — Hands-on: watch the signals fire
Have the expert run these one at a time from the repo root, and react to each:

```bash
python3 scripts/tour.py verify     # main.py PASSES — the investigation works
python3 scripts/tour.py shortcut   # shortcut.py FAILS — a naive solver must lose
python3 scripts/tour.py lint       # CLEAN — the prompt never names the answer
python3 scripts/tour.py preview    # 1/8 — recorded calibration result
```

After each, explain what it proves (see `concepts.md` → "The calibration signals"). The big
idea: a task is well-built when the intended solver passes, the shortcut fails, nothing
leaks, and Opus × 8 lands **≤ 2/8**.

### Stage 5 — Map back to the 8-step playbook
Walk `reference/concepts.md` → "The 8-step Inverse Task Playbook" and point at which sample
artifact each step produced. They've now seen a finished example of every step.

### Stage 6 — AI Use Policy + graduate
State the AI Use Policy (concepts.md): Claude helps with **code**, never the **science**
(prompt, explanation, grading). Then hand off:

1. Install and use `everglades-multitask`
   (https://github.com/rohitganti-hue/everglades-multitask).
2. Run its setup to pick your domain (EG-1 … EG-9).
3. Run `/everglades-ideate 1` to author your real first task — the skill scaffolds the code;
   you own the science.
4. The Everglades Hub (Notion) has the full playbook and anchor examples.

Close by reminding them: their first real task only needs to clear the same four signals
they just watched.
````

- [ ] **Step 2: Validate the frontmatter parses (name + description present)**

Run: `python3 -c "import re,sys; t=open('SKILL.md').read(); fm=re.search(r'^---\n(.*?)\n---', t, re.S).group(1); assert 'name: everglades-first-task' in fm and 'description:' in fm; print('frontmatter OK')"`
Expected: `frontmatter OK`

- [ ] **Step 3: Commit**

```bash
git add SKILL.md
git commit -m "Add SKILL.md: 6-stage onboarding flow with hands-on tour + graduation handoff"
```

---

### Task 7: Final verification + plan/spec commit

**Files:**
- (no new source files)

- [ ] **Step 1: Full self-test of the fixture**

Run: `python3 scripts/tour.py selftest`
Expected: `=== selftest PASSED ===` with all four checks `[OK]`.

- [ ] **Step 2: Confirm repo tree matches the plan**

Run: `find . -type f -not -path './.git/*' | sort`
Expected: every file listed in the "File structure" section above is present (README, .gitignore, SKILL.md, reference/concepts.md, scripts/tour.py, all of sample-task/, and the docs/ spec + plan).

- [ ] **Step 3: Commit the plan document**

```bash
git add docs/superpowers/plans/2026-05-30-everglades-first-task.md
git commit -m "Add implementation plan for everglades-first-task"
```

- [ ] **Step 4: STOP — confirm before any remote**

Do NOT create a GitHub remote or push. Creating/publishing a repo is outward-facing —
ask the user whether they want it pushed (and public vs. private) before doing so. Report
that the skill is built and `selftest` passes locally.

---

## Self-review

**Spec coverage:**
- §1 Purpose/audience/triggers → SKILL.md frontmatter description (Task 6).
- §2 Structure (standalone repo, layout) → Tasks 1–6 create exactly the spec's tree.
- §3 Sample task (domain-neutral synthetic, hidden rule, budget, help mode, seeded noise, near-miss, non-submittable label) → Tasks 2–3 (`config/BRIEF/STATE/problem/reasoning_trap/grading_guide/expected`, `oracle/setup.py` with budget+help+seeded `sample` mode, `main.py` pass, `shortcut.py` near-miss fail, `sample-task/README.md` label).
- §4 tour.py (stdlib-only; verify/shortcut/lint/preview/selftest; inline check_answer scalar+tuple tolerance) → Task 4.
- §5 SKILL.md 6-stage flow + gating, no persistent state machine → Task 6.
- §6 Error handling (stdlib only, stateless, frozen fixture) → Task 4 code + selftest.
- §7 Testing (single selftest, no pytest suite) → Task 4.
- §8 Out of scope → nothing in the plan authors the expert's task, calls APIs, or adds state.

**Placeholder scan:** No TBD/TODO; every code step shows complete code; every command shows expected output. The lint surface was made precise (solver-facing `problem.md` + `reasoning_trap.md`), resolving the spec's looser "problem.md + oracle/setup.py" wording — scanning the oracle would false-positive since it legitimately holds the answer; this is noted here intentionally.

**Type consistency:** `Oracle` class with `M`, `BUDGET`, `query(mode, x=...)` used identically in `main.py`, `shortcut.py`, and `tour.py`. `solve(oracle)` is the shared solver interface. `check_answer(submitted, expected_dict)` reads `expected["answer"]` / `expected["tolerance"]`, matching `golden/expected.json`. `preview()` returns the parsed dict; `selftest` reads `p["passed"]`.
