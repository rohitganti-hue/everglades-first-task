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
