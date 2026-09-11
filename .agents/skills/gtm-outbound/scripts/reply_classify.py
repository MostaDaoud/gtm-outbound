#!/usr/bin/env python3
"""
Purpose: Deterministic first-pass triage of inbound replies to a cold campaign.

         This script deliberately does NOT try to classify everything. It handles the
         categories where a miss is expensive and the signal is unambiguous -- opt-outs,
         auto-replies, out-of-office, bounces -- and routes everything else to human or
         model review. An opt-out decided by a language model is a compliance risk;
         an opt-out decided by an explicit phrase list is auditable.

Input:   CSV of replies. Needs a body/message column; from/email and subject help.
Output:  Per-reply classification with the matched rule, plus a suppression list.
         --json for machine use, --suppression-out to write addresses to suppress.

Usage:
    python reply_classify.py replies.csv
    python reply_classify.py replies.csv --json --suppression-out suppress.txt
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

BODY_COLUMNS = ("body", "message", "reply", "text", "content", "reply_body", "snippet")
EMAIL_COLUMNS = ("from", "email", "from_email", "sender", "prospect_email", "lead_email")
SUBJECT_COLUMNS = ("subject", "subject_line", "title")

# Ordered. The first rule that matches wins, so the compliance-critical and
# machine-generated categories are checked before anything interpretive.
RULES: list[tuple[str, str, re.Pattern[str]]] = [
    (
        "unsubscribe",
        "explicit opt-out language",
        re.compile(
            r"\b(unsubscribe|opt[\s-]?out|remove me|take me off|stop emailing|"
            r"stop contacting|do not contact|don't contact me|no longer wish|"
            r"delete my (data|details|information)|erase my data)\b",
            re.I,
        ),
    ),
    (
        "gdpr_request",
        "data subject request",
        re.compile(
            r"\b(gdpr|data protection|right to erasure|subject access request|"
            r"where did you get my (data|details|email)|how did you (get|obtain) my)\b",
            re.I,
        ),
    ),
    (
        "out_of_office",
        "automated absence notice",
        re.compile(
            r"\b(out of (the )?office|ooo\b|on (annual |parental |paternity |maternity )?leave|"
            r"on vacation|on holiday|away from my desk|currently away|"
            r"limited access to email|returning on|back on \w+day)\b",
            re.I,
        ),
    ),
    (
        "bounce",
        "delivery failure notice",
        re.compile(
            r"\b(undeliverable|delivery (has )?failed|address not found|"
            r"recipient .{0,20}(not found|rejected)|mailbox (is )?full|"
            r"no longer with|has left the (company|organi[sz]ation)|"
            r"mail delivery (subsystem|failed))\b",
            re.I,
        ),
    ),
    (
        "auto_reply",
        "generic autoresponder",
        re.compile(
            r"\b(auto[\s-]?reply|automatic reply|this is an automated|"
            r"we have received your (message|email|request)|ticket (has been )?created|"
            r"do not reply to this)\b",
            re.I,
        ),
    ),
    (
        "wrong_person",
        "routing to another owner",
        re.compile(
            r"\b(not the right person|wrong person|i don't (handle|own|manage)|"
            r"you('| a)?re (looking for|better off with)|reach out to|"
            r"that would be|speak (to|with) \w+|forwarding (this )?to)\b",
            re.I,
        ),
    ),
    (
        "referral",
        "names another contact positively",
        re.compile(r"\b(cc[' ]?ing|copying|introduce you to|connect you with|loop(ing)? in)\b", re.I),
    ),
    (
        "not_now",
        "timing deferral",
        re.compile(
            r"\b(not (right now|at the moment|a priority)|circle back|"
            r"revisit (this )?in|check back|next (quarter|year|month)|"
            r"budget (is )?(frozen|locked)|too early|bad timing)\b",
            re.I,
        ),
    ),
]

# Anything matching these is left for review rather than auto-classified -- these are
# the interpretive cases where tone carries the meaning.
NEEDS_REVIEW = "needs_review"


def find_column(fieldnames: list[str], candidates: tuple[str, ...]) -> str | None:
    lowered = {f.strip().lower().replace(" ", "_"): f for f in fieldnames}
    for candidate in candidates:
        if candidate in lowered:
            return lowered[candidate]
    return None


def classify(text: str) -> tuple[str, str]:
    for label, reason, pattern in RULES:
        if pattern.search(text):
            return label, reason
    return NEEDS_REVIEW, "no deterministic rule matched -- read this one"


def main() -> int:
    ap = argparse.ArgumentParser(description="Deterministic first-pass reply triage.")
    ap.add_argument("path", help="CSV of replies")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--suppression-out", type=Path, help="Write addresses to suppress")
    args = ap.parse_args()

    path = Path(args.path)
    if not path.is_file():
        print(json.dumps({"error": f"File not found: {path}"}), file=sys.stderr)
        return 2

    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            print(json.dumps({"error": "CSV has no header row."}), file=sys.stderr)
            return 2

        body_col = find_column(reader.fieldnames, BODY_COLUMNS)
        email_col = find_column(reader.fieldnames, EMAIL_COLUMNS)
        subject_col = find_column(reader.fieldnames, SUBJECT_COLUMNS)

        if not body_col:
            print(
                json.dumps({
                    "error": f"No body column found. Looked for {BODY_COLUMNS}. "
                             f"Header was: {reader.fieldnames}"
                }),
                file=sys.stderr,
            )
            return 2

        results: list[dict[str, Any]] = []
        for i, row in enumerate(reader, start=1):
            body = (row.get(body_col) or "").strip()
            subject = (row.get(subject_col) or "") if subject_col else ""
            label, reason = classify(f"{subject}\n{body}")
            results.append({
                "row": i,
                "email": (row.get(email_col) or "").strip() if email_col else None,
                "classification": label,
                "matched_rule": reason,
                "excerpt": body[:120].replace("\n", " "),
            })

    counts = Counter(r["classification"] for r in results)
    suppress = [
        r["email"] for r in results
        if r["classification"] in ("unsubscribe", "gdpr_request", "bounce") and r["email"]
    ]

    if args.suppression_out and suppress:
        args.suppression_out.write_text("\n".join(suppress) + "\n", encoding="utf-8")

    payload = {
        "total": len(results),
        "counts": dict(counts.most_common()),
        "needs_review": counts.get(NEEDS_REVIEW, 0),
        "suppression_list": suppress,
        "replies": results,
    }

    if args.json:
        print(json.dumps(payload, indent=2))
        return 0

    print(f"Reply triage: {len(results)} replies\n")
    for label, n in counts.most_common():
        print(f"  {label:<16} {n:>4}")
    print()
    if suppress:
        print(f"  SUPPRESS IMMEDIATELY ({len(suppress)}):")
        for addr in suppress:
            print(f"    {addr}")
        print()
    review = [r for r in results if r["classification"] == NEEDS_REVIEW]
    if review:
        print(f"  Needs your judgment ({len(review)}) -- tone decides these, not keywords:")
        for r in review[:15]:
            print(f"    row {r['row']:<4} {r['email'] or '(no address)'}")
            print(f"             {r['excerpt']}")
        if len(review) > 15:
            print(f"    ... and {len(review) - 15} more")
    return 0


if __name__ == "__main__":
    sys.exit(main())
