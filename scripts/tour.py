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
