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
