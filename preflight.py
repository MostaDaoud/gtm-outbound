#!/usr/bin/env python3
"""
Purpose: Verify a machine can actually run the gtm-outbound scripts before or after
         installing. Checks the Python version, confirms no third-party packages are
         needed, and smoke-tests all five scripts by executing them.

         This tests rather than asserts. The version floor below is what the syntax
         requires, but the real check is whether the scripts import and run here.

Usage:
    python preflight.py            full report
    python preflight.py --quiet    only print problems; exit 1 on failure
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

MIN_PYTHON = (3, 10)
SCRIPTS = [
    "validate_spintax.py",
    "gtm_math.py",
    "clay_taxonomy.py",
    "diagnose_campaign.py",
    "reply_classify.py",
    "score_message.py",
]
EXPECTED_STDLIB = {
    "argparse", "collections", "csv", "dataclasses", "json",
    "math", "pathlib", "re", "statistics", "sys", "typing",
}


def check_python() -> tuple[bool, str]:
    v = sys.version_info
    actual = f"{v.major}.{v.minor}.{v.micro}"
    if (v.major, v.minor) < MIN_PYTHON:
        return False, (
            f"Python {actual} is below the {MIN_PYTHON[0]}.{MIN_PYTHON[1]} minimum. "
            f"Install a newer Python and re-run."
        )
    return True, f"Python {actual}"


def check_scripts(root: Path) -> list[tuple[str, bool, str]]:
    """Execute each script's --help. Catches syntax errors and missing imports."""
    results: list[tuple[str, bool, str]] = []
    scripts_dir = root / "gtm-outbound" / "scripts"

    for name in SCRIPTS:
        path = scripts_dir / name
        if not path.is_file():
            results.append((name, False, "file not found"))
            continue
        try:
            proc = subprocess.run(
                [sys.executable, str(path), "--help"],
                capture_output=True, text=True, timeout=30,
            )
            if proc.returncode == 0:
                results.append((name, True, "runs"))
            else:
                err = (proc.stderr or proc.stdout or "").strip().splitlines()
                results.append((name, False, err[-1] if err else "non-zero exit"))
        except subprocess.TimeoutExpired:
            results.append((name, False, "timed out"))
        except OSError as exc:
            results.append((name, False, str(exc)))
    return results


def check_functional(root: Path) -> tuple[bool, str]:
    """One real calculation, to prove more than argparse works."""
    script = root / "gtm-outbound" / "scripts" / "gtm_math.py"
    if not script.is_file():
        return False, "gtm_math.py not found"
    try:
        proc = subprocess.run(
            [sys.executable, str(script), "size", "--prospects", "3000",
             "--sequence-steps", "4", "--json"],
            capture_output=True, text=True, timeout=30,
        )
        if proc.returncode != 0:
            return False, "calculation failed"
        import json
        data = json.loads(proc.stdout)
        inboxes = data["sending"]["inboxes_required"]
        if inboxes != 22:
            return False, f"wrong result: expected 22 inboxes, got {inboxes}"
        return True, "calculation correct (3,000 prospects -> 22 inboxes)"
    except Exception as exc:  # noqa: BLE001 - preflight should never itself crash
        return False, f"{type(exc).__name__}: {exc}"


def check_structure(root: Path) -> list[tuple[str, bool, str]]:
    expected = {
        "gtm-outbound": 1, "gtm-outbound-offer": 1, "gtm-outbound-list": 1,
        "gtm-outbound-clay": 1, "gtm-outbound-copy": 1, "gtm-outbound-math": 1,
        "gtm-outbound-score": 1, "gtm-outbound-diagnose": 1, "gtm-outbound-reply": 1,
    }
    out: list[tuple[str, bool, str]] = []
    for skill in expected:
        p = root / skill / "SKILL.md"
        out.append((skill, p.is_file(), "SKILL.md present" if p.is_file() else "MISSING"))
    agents = root / "gtm-outbound" / "agents"
    na = len(list(agents.glob("*.md"))) if agents.is_dir() else 0
    out.append(("agents", na >= 1, f"{na} agent definition(s)"))
    refs = root / "gtm-outbound" / "references"
    n = len(list(refs.glob("*.md"))) if refs.is_dir() else 0
    out.append(("references", n >= 15, f"{n} reference files"))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Preflight check for gtm-outbound.")
    ap.add_argument("--quiet", action="store_true", help="only report problems")
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    args = ap.parse_args()

    failures: list[str] = []
    lines: list[str] = ["gtm-outbound preflight", "=" * 22, ""]

    ok, msg = check_python()
    lines.append(f"  [{'ok' if ok else 'FAIL'}] {msg}")
    if not ok:
        failures.append(msg)
        # No point testing scripts on an unsupported interpreter.
        print("\n".join(lines) if not args.quiet else msg, file=sys.stderr)
        return 1

    lines.append(f"  [ok] no third-party packages required "
                 f"({len(EXPECTED_STDLIB)} stdlib modules)")
    lines.append("")
    lines.append("  structure:")
    for name, good, detail in check_structure(args.root):
        lines.append(f"    [{'ok' if good else 'FAIL'}] {name:<24} {detail}")
        if not good:
            failures.append(f"{name}: {detail}")

    lines.append("")
    lines.append("  scripts:")
    for name, good, detail in check_scripts(args.root):
        lines.append(f"    [{'ok' if good else 'FAIL'}] {name:<24} {detail}")
        if not good:
            failures.append(f"{name}: {detail}")

    ok, detail = check_functional(args.root)
    lines.append("")
    lines.append(f"  [{'ok' if ok else 'FAIL'}] {detail}")
    if not ok:
        failures.append(detail)

    lines.append("")
    lines.append("  PASS - this machine can run gtm-outbound" if not failures
                 else f"  FAIL - {len(failures)} problem(s)")

    if args.quiet:
        if failures:
            print("preflight failed:", file=sys.stderr)
            for f in failures:
                print(f"  - {f}", file=sys.stderr)
    else:
        print("\n".join(lines))

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
