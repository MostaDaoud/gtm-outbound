#!/usr/bin/env python3
"""Turn evals.json into a paste-and-grade run sheet for a fresh session.

The activation evals cannot be run from a session that already has the skill in context --
that is the bias the handoff warns about. This produces a checklist to work through in a
cold session instead: prompt, what to expect, assertions to tick, space for the verdict.

    python run_sheet.py                    # every eval
    python run_sheet.py --category activation collision
    python run_sheet.py --ids 17 25 29
    python run_sheet.py --md > RUN-SHEET.md
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).parent


def main() -> int:
    ap = argparse.ArgumentParser(description="Build an eval run sheet.")
    ap.add_argument("--category", nargs="*", help="Filter by category")
    ap.add_argument("--ids", nargs="*", type=int, help="Filter by eval_id")
    ap.add_argument("--md", action="store_true", help="Markdown instead of plain text")
    args = ap.parse_args()

    data = json.loads((HERE / "evals.json").read_text(encoding="utf-8"))
    evals = data["evals"]
    if args.category:
        wanted = {c.lower() for c in args.category}
        evals = [e for e in evals if e["category"].lower() in wanted]
    if args.ids:
        evals = [e for e in evals if e["eval_id"] in set(args.ids)]
    if not evals:
        print("No evals matched.", file=sys.stderr)
        return 2

    out: list[str] = []
    w = out.append
    total_assertions = sum(len(e["assertions"]) for e in evals)

    if args.md:
        w(f"# Eval run sheet — {len(evals)} evals, {total_assertions} assertions\n")
        w("Run these in a **fresh session**. A session that already has the skill in")
        w("context routes differently, which is exactly what these are testing.\n")
        for e in evals:
            trig = "should trigger" if e.get("should_trigger", True) else "must NOT trigger"
            w(f"## {e['eval_id']} · {e['eval_name']}")
            w(f"`{e['category']}` — {trig}\n")
            w("> " + e["prompt"].replace("\n", "\n> ") + "\n")
            for a in e["assertions"]:
                w(f"- [ ] **{a['name']}** — {a['check']}")
            w("\n**Result:** pass / fail — \n")
    else:
        w(f"Eval run sheet — {len(evals)} evals, {total_assertions} assertions")
        w("Run in a FRESH session; this one's context biases routing.")
        w("=" * 78)
        for e in evals:
            trig = "should trigger" if e.get("should_trigger", True) else "must NOT trigger"
            w("")
            w(f"[{e['eval_id']:>2}] {e['eval_name']}   ({e['category']}, {trig})")
            w("-" * 78)
            for line in e["prompt"].splitlines():
                w(f"  > {line}")
            w("")
            for a in e["assertions"]:
                w(f"  [ ] {a['name']}")
                for chunk in wrap(a["check"], 70):
                    w(f"      {chunk}")
            w("  RESULT: ______")
        w("")
        w("=" * 78)

    print("\n".join(out))
    return 0


def wrap(text: str, width: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for word in words:
        if len(cur) + len(word) + 1 > width:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    if cur:
        lines.append(cur)
    return lines


if __name__ == "__main__":
    raise SystemExit(main())
