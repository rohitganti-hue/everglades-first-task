# Design: `everglades-first-task` onboarding skill

**Date:** 2026-05-30
**Status:** Approved (design); pending spec review → implementation plan
**Related:** `everglades-multitask` (the tool this skill graduates experts into) — its
"When NOT to use" section already names `everglades-first-task` as the place a brand-new
expert should start.

---

## 1. Purpose & audience

A standalone Claude Code skill that onboards a Mercor Project Everglades expert who has
**never authored a task**. In one guided, hands-on session (~20 min) it gives the expert a
working mental model of an *inverse task* by touring a complete, frozen, known-good **sample
task** — having them run the local checks themselves to watch the calibration signals fire —
then hands them off to `everglades-multitask` to author their real first task.

This is a **teaching skill, not an authoring skill.** It produces no submittable task; the
expert practices on a fixture and graduates.

**Triggers:** `/everglades-first-task`, "onboard me to Everglades", "I've never written an
Everglades task", "where do I start with Everglades", "I'm new to Everglades".

**Success state:** the expert has (a) a mental model of inverse-task design, (b) seen each
artifact of a finished task and which playbook step produced it, (c) personally watched
`verify` pass / `shortcut` fail / `lint` clean / a canned `preview` come in at ≤2/8, and
(d) clear next steps to install + run `everglades-multitask` for their own first task.

---

## 2. Structure

Standalone new git repo `everglades-first-task` (not folded into `everglades-multitask`).
Matches the name already referenced by the existing skill.

```
everglades-first-task/
├── SKILL.md                      # frontmatter + the 6-stage onboarding script Claude follows
├── README.md                     # who/what/why, ~20-min promise, how to start, graduates to multitask
├── reference/
│   └── concepts.md               # inverse-task framing · 8-step overview · ≤2/8 gate · AI Use Policy · RLS copy-paste model
├── sample-task/                  # THE FIXTURE: a complete, frozen, known-good synthetic inverse task
│   ├── README.md                 # "teaching fixture — do NOT submit this"
│   ├── BRIEF.md
│   ├── STATE.md                  # "why this is the only answer" + order of decisions
│   ├── problem.md                # solver-facing prompt
│   ├── reasoning_trap.md
│   ├── config.yaml               # direction: inverse, domain: Samples
│   ├── oracle/setup.py           # hidden system: query modes + tight budget + seeded noise
│   ├── solution/main.py          # intended solver — PASSES
│   ├── solution/shortcut.py      # naive solver — FAILS (lands on a near-miss)
│   ├── grader/grading_guide.md   # near-miss table
│   ├── golden/expected.json
│   └── runs/preview_canned.json  # recorded Opus×8 = ≤2/8 result
└── scripts/
    └── tour.py                   # self-contained, stdlib-only driver
```

The repo is **self-contained**: it does NOT depend on `everglades-multitask` being installed,
because onboarding is meant to run *before* the expert has the bigger tool. (Approach A from
brainstorming.)

---

## 3. The sample task (domain-neutral synthetic)

A small "investigation" that needs no specific science background, so any expert (EG-1…EG-9)
can follow the reasoning pattern:

- A hidden deterministic rule/parameter lives inside the oracle.
- The solver may query the oracle in a few **observation modes** under a **tight query budget**,
  plus a non-committal **help mode** that gives hints but never recommends an answer.
- The correct answer is the hidden parameter (or a small tuple of parameters).
- `solution/main.py` queries strategically within budget and recovers the answer → **PASSES**.
- `solution/shortcut.py` uses a naive heuristic (e.g. assumes linearity / picks the most
  frequent observation) and lands on a **plausible near-miss** → **FAILS**.
- The budget is tight enough that brute force exhausts it before converging → demonstrates
  "a tight budget makes shortcuts lose."
- Oracle noise is **seeded** → realistic but deterministic, so the tour is reproducible.

**Authoring note:** The fixture is authored as skill content, including `problem.md` and the grading
content. This does NOT violate the Everglades AI Use Policy (which forbids an assistant from writing
the *expert's* prompt/science/grading) because the sample is instructional skill content, not a
task the expert submits. Every file in `sample-task/` is clearly labeled as a non-submittable
teaching fixture.

---

## 4. `scripts/tour.py` — the hands-on driver

Constraints: **Python 3 standard library only** — no Anthropic key, no `~/.everglades/config.json`,
no third-party deps. Must run on a fresh laptop before anything else is installed. Stateless and
idempotent; subcommands may be run in any order any number of times.

Subcommands (each prints the raw result **and** a short teaching note):

| Subcommand | Action | Expected output |
|---|---|---|
| `verify` | Run `solution/main.py` against `oracle/setup.py`, compare to `golden/expected.json` within tolerance | ✓ PASS — "the intended investigation recovers the answer" |
| `shortcut` | Run `solution/shortcut.py` against the oracle | ✗ FAIL (as it must) — "naive solver hit near-miss X; answer was Y" |
| `lint` | Leak scan of `problem.md` + `oracle/setup.py` for the answer value | ✓ clean — "the solver-facing text never leaks the answer" |
| `preview` | Print `runs/preview_canned.json` | "1/8 passed — ≤2/8 means appropriately hard for the 16-model Taiga eval" |
| `selftest` | Run verify + shortcut + lint + preview and assert expected outcomes | Pass/fail of the fixture itself (regression guard) |

Grading uses a tiny inline `check_answer(submitted, expected)` supporting scalars and tuples
with element-wise numeric tolerance — mirrors the `everglades-multitask` `grading.py` contract
but is self-contained here.

---

## 5. SKILL.md onboarding flow — 6 linear, gated stages

The flow is a script Claude follows; the teaching prose lives in `reference/concepts.md` and the
artifacts being toured live in `sample-task/`.

1. **Welcome + mental model.** "An inverse task is not a normal task with the answer hidden — it
   is a small investigation. The solver sees the evidence, but not the rule that makes one answer
   right and the others wrong." Set the ~20-min, hands-on expectation.
2. **The finished task, top-down.** Open `BRIEF.md` + `STATE.md`. Teach "lock the answer first,"
   "order of decisions," and the "why this is the only answer" section.
3. **Seen vs. hidden.** Contrast `problem.md` (what the solver sees) with `oracle/setup.py` (the
   hidden system — modes, budget, noise). Walk the near-miss table in `grader/grading_guide.md`
   and `golden/expected.json`.
4. **Hands-on: watch the signals fire.** Expert runs `tour.py verify` → `shortcut` → `lint` →
   `preview`. Claude explains each signal as part of the calibration bar.
5. **Map back to the 8-step playbook.** Now that the expert has seen the artifacts, show which of
   the 8 Inverse Task Playbook steps produced each one.
6. **AI Use Policy + graduate.** What Claude may/may not write (code yes; prompt/science/grading
   no). Then the handoff: install `everglades-multitask`, run its setup (pick domain EG-1…EG-9),
   run `/everglades-ideate 1` to author the real first task. Pointer to the Everglades Hub Notion.

**Gating:** the flow is linear; Claude tracks position in-conversation. Each hands-on step in
Stage 4 is gated on the prior command having been run. No persistent state machine is needed —
this is a read-mostly tour over a frozen fixture (unlike `everglades-multitask`, which gates a
mutable authoring pipeline with `STATE.md`).

---

## 6. Error handling

- `tour.py` runs with stdlib + Python 3 only. If `python3` is missing, print a clear message.
- Subcommands are stateless/idempotent and order-independent.
- The fixture is frozen, so `verify` always PASSES and `shortcut` always FAILS. If they don't,
  that is a repo regression — caught by `tour.py selftest`.

---

## 7. Testing

A single `tour.py selftest` subcommand is the fixture's regression guard: it asserts
verify-passes, shortcut-fails, lint-clean, and canned-preview ≤2/8. This is one self-check
script, not a broad pytest suite — consistent with keeping the repo lean and expert-facing
(the `everglades-multitask` repo's test suite was deliberately removed for the same reason).

---

## 8. Out of scope (YAGNI)

- Authoring the expert's own task — that is `everglades-multitask`'s job.
- Live Anthropic preview during onboarding — the preview is canned to avoid an API key/cost
  gate on day one.
- Any RLS or Taiga API calls.
- Multiple sample tasks or per-domain samples — one domain-neutral synthetic sample.
- Persistent progress state across sessions.

---

## 9. Open questions

None blocking. The sample task's exact synthetic premise (which hidden rule) will be chosen
during implementation to maximize clarity of the near-miss; it does not change the architecture.
