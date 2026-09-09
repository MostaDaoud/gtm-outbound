#!/usr/bin/env python3
"""
Purpose: Validate spintax syntax and merge tags in outbound email/LinkedIn sequences
         before they are loaded into a sending platform. Malformed spintax does not
         fail loudly at import time -- it renders literal braces into a prospect's
         inbox, which burns the domain and the lead simultaneously.

Input:   A markdown/text sequence file, or --stdin. Optionally a clay-table.json
         (via --vars) defining which merge variables actually exist.

Output:  Human-readable report by default; --json for machine consumption.
         Exit 0 = clean (warnings allowed), exit 1 = errors found.

Usage:
    python validate_spintax.py SEQUENCE.md
    python validate_spintax.py SEQUENCE.md --vars clay-table.json --max-words 80
    cat draft.txt | python validate_spintax.py --stdin --dialect instantly --json

Dialects:
    smartlead  (default)  {{first_name}} for merge tags, {{Hey|Hi}} for spintax.
                          Same delimiter for both -- a pipe is what distinguishes them.
    instantly             {{firstName}} for merge tags, {Hey|Hi} for spintax.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

MERGE_TAG_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.]*$")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", re.MULTILINE)
WORD_RE = re.compile(r"[A-Za-z0-9'’\-]+")

# Only sections that are actually messages get word-limited. A SEQUENCE.md also holds
# configuration tables, test design, and validator output -- word-capping those produces
# failures that mean nothing and train the user to ignore the check.
MESSAGE_HEADING_RE = re.compile(
    r"\b(email|message|dm|step|follow[\s-]?up|linkedin|connection|subject|bump|"
    r"touch|reply|note)\b",
    re.I,
)

# A spin block with this many options, multiplied across a message, produces more
# unique variants than any warmup pool can plausibly cover. Past this point you are
# not improving deliverability, you are just making the copy impossible to review.
VARIANT_WARN_THRESHOLD = 5000


@dataclass
class Issue:
    severity: str  # "error" | "warning"
    line: int
    code: str
    message: str
    excerpt: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity,
            "line": self.line,
            "code": self.code,
            "message": self.message,
            "excerpt": self.excerpt,
        }


@dataclass
class Block:
    """A {{...}} (or {...}) span found in the source text."""

    raw: str
    inner: str
    start: int
    end: int
    line: int
    depth: int
    options: list[str] = field(default_factory=list)
    kind: str = "tag"  # "tag" | "spintax"

    @property
    def is_spintax(self) -> bool:
        return self.kind == "spintax"


@dataclass
class Message:
    """One logical message in the sequence (Email 1, LinkedIn DM, etc.)."""

    title: str
    text: str
    offset: int
    line: int
    is_message: bool = True


def line_of(text: str, index: int) -> int:
    """1-indexed line number for a character offset."""
    return text.count("\n", 0, index) + 1


def excerpt_at(text: str, start: int, end: int, pad: int = 24) -> str:
    lo = max(0, start - pad)
    hi = min(len(text), end + pad)
    snippet = text[lo:hi].replace("\n", " ")
    return f"...{snippet}..." if lo > 0 or hi < len(text) else snippet


def split_options(inner: str, open_tok: str, close_tok: str) -> list[str]:
    """Split on pipes that sit at nesting depth 0 inside the block."""
    options: list[str] = []
    buf: list[str] = []
    depth = 0
    i = 0
    while i < len(inner):
        if inner.startswith(open_tok, i):
            depth += 1
            buf.append(open_tok)
            i += len(open_tok)
        elif inner.startswith(close_tok, i) and depth > 0:
            depth -= 1
            buf.append(close_tok)
            i += len(close_tok)
        elif inner[i] == "|" and depth == 0:
            options.append("".join(buf))
            buf = []
            i += 1
        else:
            buf.append(inner[i])
            i += 1
    options.append("".join(buf))
    return options


def find_blocks(
    text: str, open_tok: str, close_tok: str, issues: list[Issue]
) -> list[Block]:
    """Scan for delimiter spans, reporting unbalanced ones as errors."""
    blocks: list[Block] = []
    stack: list[int] = []
    i = 0
    while i < len(text):
        if text.startswith(open_tok, i):
            stack.append(i)
            i += len(open_tok)
        elif text.startswith(close_tok, i):
            if not stack:
                issues.append(
                    Issue(
                        "error",
                        line_of(text, i),
                        "UNMATCHED_CLOSE",
                        f"Closing '{close_tok}' with no matching '{open_tok}'.",
                        excerpt_at(text, i, i + len(close_tok)),
                    )
                )
                i += len(close_tok)
                continue
            start = stack.pop()
            end = i + len(close_tok)
            inner = text[start + len(open_tok) : i]
            blocks.append(
                Block(
                    raw=text[start:end],
                    inner=inner,
                    start=start,
                    end=end,
                    line=line_of(text, start),
                    depth=len(stack),
                    options=split_options(inner, open_tok, close_tok),
                )
            )
            i = end
        else:
            i += 1

    for orphan in stack:
        issues.append(
            Issue(
                "error",
                line_of(text, orphan),
                "UNCLOSED_BLOCK",
                f"Opening '{open_tok}' is never closed. This renders literal braces "
                f"to the prospect.",
                excerpt_at(text, orphan, orphan + len(open_tok)),
            )
        )

    return sorted(blocks, key=lambda b: b.start)


def load_allowed_vars(path: Path) -> set[str]:
    """Read allowed merge variables from a clay-table.json or a plain JSON list."""
    data = json.loads(path.read_text(encoding="utf-8"))
    allowed: set[str] = set()

    if isinstance(data, list):
        for item in data:
            if isinstance(item, str):
                allowed.add(item)
            elif isinstance(item, dict):
                for key in ("smartlead_field", "output_field", "name", "column"):
                    if isinstance(item.get(key), str):
                        allowed.add(item[key])
    elif isinstance(data, dict):
        for key in ("columns", "fields", "variables"):
            section = data.get(key)
            if isinstance(section, list):
                for item in section:
                    if isinstance(item, str):
                        allowed.add(item)
                    elif isinstance(item, dict):
                        for k in ("smartlead_field", "output_field", "name", "column"):
                            if isinstance(item.get(k), str):
                                allowed.add(item[k])
    return {v for v in allowed if v}


def segment_messages(text: str, message_pattern: re.Pattern[str] | None) -> list[Message]:
    """
    Split the sequence into sections on markdown headings; whole file if none.

    Sections are tagged as messages or not. Spintax and merge-tag checks run over the
    whole file regardless -- only the word limit is scoped to actual messages.
    """
    headings = list(HEADING_RE.finditer(text))
    if not headings:
        return [Message("(whole file)", text, 0, 1, True)]

    messages: list[Message] = []
    for idx, match in enumerate(headings):
        body_start = match.end()
        body_end = headings[idx + 1].start() if idx + 1 < len(headings) else len(text)
        title = match.group(1).strip()
        messages.append(
            Message(
                title=title,
                text=text[body_start:body_end],
                offset=body_start,
                line=line_of(text, match.start()),
                is_message=(message_pattern is None or bool(message_pattern.search(title))),
            )
        )
    return messages


SUBJECT_LINE_RE = re.compile(
    r"^[ 	]*(?:\*\*)?subject(?:\s*line)?(?:\*\*)?\s*:.*$", re.I | re.M
)


def strip_subject(text: str) -> str:
    """Drop subject lines. The word limit is a budget for the body."""
    return SUBJECT_LINE_RE.sub(" ", text)


def count_words(text: str) -> int:
    return len(WORD_RE.findall(text))


def count_words_rendered(text: str) -> int:
    """Word count with any nested block collapsed to the single word it resolves to."""
    text = re.sub(r"\{\{[^{}]*\}\}", " x ", text)
    text = re.sub(r"\{[^{}]*\}", " x ", text)
    return count_words(text)


def top_level_in(message: Message, blocks: list[Block]) -> list[Block]:
    """
    Blocks that belong to this message and are not contained inside another block.

    Containment matters because the two dialects are scanned separately: a merge tag
    sitting inside a spin option is found by its own pass and would otherwise be
    counted twice.
    """
    lo, hi = message.offset, message.offset + len(message.text)
    selected: list[Block] = []
    cursor = -1
    for b in sorted(blocks, key=lambda x: x.start):
        if b.start < lo or b.start >= hi:
            continue
        if b.start < cursor:
            continue  # nested inside the block already taken
        selected.append(b)
        cursor = b.end
    return selected


def word_bounds(message: Message, blocks: list[Block]) -> tuple[int, int]:
    """
    Shortest and longest rendered word count for a message.

    A sub-80-word rule has to hold for the *worst* variant, not for whichever one
    happens to be written first. Merge tags count as one word, since that is roughly
    what they resolve to on send.
    """
    in_range = top_level_in(message, blocks)

    def render(pick: str) -> str:
        out: list[str] = []
        cursor = message.offset
        for b in in_range:
            out.append(message.text[cursor - message.offset : b.start - message.offset])
            if b.is_spintax:
                key = count_words_rendered
                out.append(min(b.options, key=key) if pick == "min" else max(b.options, key=key))
            else:
                out.append(" x ")
            cursor = b.end
        out.append(message.text[cursor - message.offset :])
        return "".join(out)

    # Stripped AFTER rendering so spintax inside a subject resolves first, and kept
    # out of the count so a long subject never reads as bloated body copy.
    return (
        count_words_rendered(strip_subject(render("min"))),
        count_words_rendered(strip_subject(render("max"))),
    )


def variant_count(message: Message, blocks: list[Block]) -> int:
    total = 1
    for b in top_level_in(message, blocks):
        if b.is_spintax:
            total *= len(b.options)
            if total > 10**9:
                return total
    return total


def validate(
    text: str,
    dialect: str = "smartlead",
    allowed_vars: set[str] | None = None,
    max_words: int | None = None,
    max_depth: int = 1,
    message_pattern: re.Pattern[str] | None = MESSAGE_HEADING_RE,
) -> dict[str, Any]:
    issues: list[Issue] = []

    if dialect == "instantly":
        # Instantly separates the two concepts: {{firstName}} is a merge tag,
        # {a|b} is spintax. Extract tags first, then mask them with a same-length
        # filler so single-brace scanning does not re-read their inner braces --
        # equal length keeps every offset and line number intact.
        blocks = find_blocks(text, "{{", "}}", issues)
        for b in blocks:
            b.kind = "tag"
            b.options = [b.inner]
        masked = list(text)
        for b in blocks:
            for idx in range(b.start, b.end):
                masked[idx] = "\x00"
        spin_blocks = find_blocks("".join(masked), "{", "}", issues)
        for b in spin_blocks:
            b.kind = "spintax"
            # Re-read from the unmasked source so options that contain merge tags
            # keep their real text for word counting and error excerpts.
            b.raw = text[b.start : b.end]
            b.inner = text[b.start + 1 : b.end - 1]
            b.options = split_options(b.inner, "{", "}")
            if len(b.options) == 1:
                issues.append(
                    Issue(
                        "warning",
                        b.line,
                        "SINGLE_OPTION_SPIN",
                        f"'{b.raw}' has no pipe. In the Instantly dialect single braces "
                        f"mean spintax, so a merge tag here needs double braces.",
                        b.raw[:60],
                    )
                )
        blocks = sorted(blocks + spin_blocks, key=lambda b: b.start)
    else:
        # Smartlead overloads one delimiter for both. A pipe is the only thing that
        # distinguishes {{Hey|Hi}} from {{first_name}}.
        blocks = find_blocks(text, "{{", "}}", issues)
        for b in blocks:
            b.kind = "spintax" if len(b.options) > 1 else "tag"

    # An unbalanced delimiter makes every downstream depth reading meaningless: one
    # stray brace reparents the rest of the file and manufactures a pile of phantom
    # nesting errors. Report the structural break alone and stop, so the real fix is
    # the only thing on screen.
    structural = [i for i in issues if i.code in {"UNCLOSED_BLOCK", "UNMATCHED_CLOSE"}]
    if structural:
        structural.append(
            Issue(
                "warning",
                structural[0].line,
                "CHECKS_DEFERRED",
                "Remaining checks (nesting, merge tags, word counts) were skipped "
                "because unbalanced braces make them unreliable. Fix the above and "
                "re-run.",
            )
        )
        return {
            "ok": False,
            "dialect": dialect,
            "counts": {
                "blocks": len(blocks),
                "spintax_blocks": 0,
                "merge_tags": 0,
                "errors": sum(1 for i in structural if i.severity == "error"),
                "warnings": sum(1 for i in structural if i.severity == "warning"),
            },
            "messages": [],
            "issues": [i.as_dict() for i in sorted(structural, key=lambda x: x.line)],
        }

    for b in blocks:
        if b.depth >= max_depth:
            issues.append(
                Issue(
                    "error",
                    b.line,
                    "NESTED_SPINTAX",
                    f"Spintax nested {b.depth + 1} levels deep. Smartlead and Instantly "
                    f"both flatten nested blocks unpredictably -- keep nesting at 1.",
                    b.raw[:60],
                )
            )

        if b.is_spintax:
            for opt in b.options:
                if not opt.strip():
                    issues.append(
                        Issue(
                            "error",
                            b.line,
                            "EMPTY_OPTION",
                            "Empty spintax option (a stray or doubled pipe). This "
                            "renders as a missing word in a share of sends.",
                            b.raw[:60],
                        )
                    )
                    break

            stripped = [o.strip() for o in b.options]
            dupes = {o for o in stripped if stripped.count(o) > 1 and o}
            if dupes:
                issues.append(
                    Issue(
                        "warning",
                        b.line,
                        "DUPLICATE_OPTION",
                        f"Duplicate spintax options ({', '.join(sorted(dupes))}) "
                        f"reduce real variation without reducing review burden.",
                        b.raw[:60],
                    )
                )

            if any(o != o.strip() for o in b.options):
                issues.append(
                    Issue(
                        "warning",
                        b.line,
                        "OPTION_WHITESPACE",
                        "Spintax option has leading/trailing whitespace, which "
                        "produces double spaces in some rendered variants.",
                        b.raw[:60],
                    )
                )
        else:
            name = b.inner.strip()
            if name != b.inner:
                issues.append(
                    Issue(
                        "warning",
                        b.line,
                        "TAG_WHITESPACE",
                        f"Merge tag '{b.raw}' has inner whitespace. Not every platform "
                        f"trims it, and an untrimmed tag fails to resolve.",
                        b.raw[:60],
                    )
                )
            if not name:
                issues.append(
                    Issue("error", b.line, "EMPTY_TAG", "Empty merge tag.", b.raw[:60])
                )
            elif not MERGE_TAG_RE.match(name):
                issues.append(
                    Issue(
                        "error",
                        b.line,
                        "MALFORMED_TAG",
                        f"Merge tag '{name}' is not a valid variable name.",
                        b.raw[:60],
                    )
                )
            elif allowed_vars is not None and name not in allowed_vars:
                issues.append(
                    Issue(
                        "error",
                        b.line,
                        "UNKNOWN_VAR",
                        f"Merge tag '{name}' has no producing column in the supplied "
                        f"schema. It will render blank or literal on every send.",
                        b.raw[:60],
                    )
                )

    if dialect == "smartlead":
        for m in re.finditer(r"(?<!\{)\{(?!\{)([^{}\n]{1,60})\}(?!\})", text):
            issues.append(
                Issue(
                    "warning",
                    line_of(text, m.start()),
                    "SINGLE_BRACE",
                    f"Single-brace '{m.group(0)}' found. Smartlead expects double "
                    f"braces -- this will be sent as literal text.",
                    m.group(0),
                )
            )

    messages = segment_messages(text, message_pattern)
    stats: list[dict[str, Any]] = []
    for msg in messages:
        lo, hi = word_bounds(msg, blocks)
        variants = variant_count(msg, blocks)
        stats.append(
            {
                "title": msg.title,
                "line": msg.line,
                "words_min": lo,
                "words_max": hi,
                "variants": variants,
                "word_limited": msg.is_message,
            }
        )

        if max_words is not None and msg.is_message and hi > max_words:
            issues.append(
                Issue(
                    "error",
                    msg.line,
                    "WORD_LIMIT",
                    f"'{msg.title}' reaches {hi} words in its longest variant "
                    f"(limit {max_words}). Shortest variant is {lo}.",
                )
            )

        if variants > VARIANT_WARN_THRESHOLD:
            issues.append(
                Issue(
                    "warning",
                    msg.line,
                    "VARIANT_EXPLOSION",
                    f"'{msg.title}' expands to {variants:,} unique variants. Past a few "
                    f"thousand you cannot meaningfully review the copy that ships.",
                )
            )

    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]

    return {
        "ok": not errors,
        "dialect": dialect,
        "counts": {
            "blocks": len(blocks),
            "spintax_blocks": sum(1 for b in blocks if b.is_spintax),
            "merge_tags": sum(1 for b in blocks if not b.is_spintax),
            "errors": len(errors),
            "warnings": len(warnings),
        },
        "messages": stats,
        "issues": [i.as_dict() for i in sorted(issues, key=lambda x: (x.line, x.code))],
    }


def render_report(result: dict[str, Any]) -> str:
    lines: list[str] = []
    c = result["counts"]
    status = "PASS" if result["ok"] else "FAIL"
    lines.append(f"Spintax validation: {status}  (dialect: {result['dialect']})")
    lines.append(
        f"  {c['spintax_blocks']} spin blocks, {c['merge_tags']} merge tags, "
        f"{c['errors']} errors, {c['warnings']} warnings"
    )

    if result["messages"]:
        lines.append("")
        lines.append(f"  {'Message':<38} {'Words':>11}  {'Variants':>10}")
        lines.append(f"  {'-' * 38} {'-' * 11}  {'-' * 10}")
        for m in result["messages"]:
            span = (
                f"{m['words_min']}"
                if m["words_min"] == m["words_max"]
                else f"{m['words_min']}-{m['words_max']}"
            )
            title = m["title"][:37]
            if not m.get("word_limited", True):
                span = f"({span})"
            lines.append(f"  {title:<38} {span:>11}  {m['variants']:>10,}")
        if any(not m.get("word_limited", True) for m in result["messages"]):
            lines.append("  (parenthesised counts are non-message sections, not word-limited)")

    if result["issues"]:
        lines.append("")
        for i in result["issues"]:
            mark = "ERROR  " if i["severity"] == "error" else "warning"
            lines.append(f"  {mark} L{i['line']:<4} [{i['code']}] {i['message']}")
            if i["excerpt"]:
                lines.append(f"                 {i['excerpt']}")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate spintax and merge tags in an outbound sequence."
    )
    parser.add_argument("path", nargs="?", help="Sequence file (markdown or text)")
    parser.add_argument("--stdin", action="store_true", help="Read from stdin instead")
    parser.add_argument(
        "--dialect",
        choices=["smartlead", "instantly"],
        default="smartlead",
        help="Platform brace convention (default: smartlead)",
    )
    parser.add_argument(
        "--vars",
        type=Path,
        help="clay-table.json (or JSON list) of merge variables that actually exist",
    )
    parser.add_argument(
        "--max-words",
        type=int,
        help="Fail if any message's longest variant exceeds this word count",
    )
    parser.add_argument(
        "--max-depth", type=int, default=1, help="Max spintax nesting depth (default 1)"
    )
    parser.add_argument(
        "--message-pattern",
        help="Regex matching headings that are messages. Only these are word-limited. "
             "Default matches email/message/step/follow-up/LinkedIn/subject headings.",
    )
    parser.add_argument(
        "--all-sections",
        action="store_true",
        help="Word-limit every section, including configuration and notes",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    if args.stdin:
        text = sys.stdin.read()
    elif args.path:
        source = Path(args.path)
        if not source.is_file():
            print(json.dumps({"error": f"File not found: {source}"}), file=sys.stderr)
            return 2
        text = source.read_text(encoding="utf-8")
    else:
        parser.error("Provide a file path or --stdin")
        return 2

    allowed = None
    if args.vars:
        if not args.vars.is_file():
            print(json.dumps({"error": f"Vars file not found: {args.vars}"}), file=sys.stderr)
            return 2
        allowed = load_allowed_vars(args.vars)
        if not allowed:
            print(
                json.dumps({"error": f"No variables parsed from {args.vars}"}),
                file=sys.stderr,
            )
            return 2

    if args.all_sections:
        pattern = None
    elif args.message_pattern:
        try:
            pattern = re.compile(args.message_pattern, re.I)
        except re.error as exc:
            print(json.dumps({"error": f"Bad --message-pattern: {exc}"}), file=sys.stderr)
            return 2
    else:
        pattern = MESSAGE_HEADING_RE

    result = validate(
        text,
        dialect=args.dialect,
        allowed_vars=allowed,
        max_words=args.max_words,
        max_depth=args.max_depth,
        message_pattern=pattern,
    )

    print(json.dumps(result, indent=2) if args.json else render_report(result))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
