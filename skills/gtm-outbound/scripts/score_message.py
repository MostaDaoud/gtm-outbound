#!/usr/bin/env python3
"""
Purpose: Score an outbound message against the criteria the reference files define.

         validate_spintax.py checks that a sequence is syntactically sound. This checks
         whether it is any good -- word budget, AI-voice markers, recipient focus,
         hedging discipline, CTA friction, and whether the message survives having its
         merge tags removed.

         Every check here is deterministic. Judgment calls (is the observation true? is
         the proof relevant?) stay with the human; this catches the mechanical failures
         that otherwise reach a prospect.

Input:   A sequence file (markdown) or --stdin. Optionally --vars from clay_taxonomy.py.
Output:  Per-message scores with line-anchored findings; --json for chaining.
         Exit 0 if every message passes, 1 if any fails.

Usage:
    python score_message.py SEQUENCE.md
    python score_message.py SEQUENCE.md --max-words 80 --min-score 70
    python score_message.py draft.txt --stdin --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", re.MULTILINE)
MESSAGE_HEADING_RE = re.compile(
    r"\b(email|message|dm|step|follow[\s-]?up|linkedin|connection|subject|bump|touch)\b",
    re.I,
)
WORD_RE = re.compile(r"[A-Za-z0-9'’\-]+")
SENTENCE_SPLIT_RE = re.compile(r"[.!?]+[\s\n]|\n\n")
BLOCK_RE = re.compile(r"\{\{[^{}]*\}\}|\{[^{}]*\}")

# --- AI-voice and low-information markers -----------------------------------------
# From copy-frameworks.md. These are editing heuristics, not authorship detection --
# a human can write every one of them. They are penalised because they carry no
# information, not because of who wrote them.
BANNED_PHRASES: list[tuple[str, str]] = [
    (r"\bi hope (this|you)\b.{0,24}\b(finds?|are) (you )?(well|doing well)\b", "ceremonial opener"),
    (r"\bi wanted to reach out\b", "ceremonial opener"),
    (r"\bi('m| am) reaching out\b", "ceremonial opener"),
    (r"\bi (came|stumbled) (across|upon) your (profile|company|website|blog|business)\b",
     "says nothing"),
    (r"\bjust (following up|checking in|bumping)\b", "adds nothing"),
    (r"\bcircle back\b|\btouch base\b|\bpick your brain\b", "filler idiom"),
    (r"\bquick (call|chat)\b", "high-friction ask dressed as low"),
    (r"\b\d{1,2}[- ]minute (call|chat|demo)\b", "calendar ask in first touch"),
    (r"\bexplore (potential )?synerg(y|ies)\b", "means nothing"),
    (r"\bgame[- ]chang(er|ing)\b|\bcutting[- ]edge\b|\bbest[- ]in[- ]class\b", "hype adjective"),
    (r"\bleverage\b|\bseamless(ly)?\b|\brobust\b|\bunlock\b", "corporate abstraction"),
    (r"\b(truly|incredibly|extremely) (impressed|excited|passionate)\b", "empty enthusiasm"),
    (r"\bi was (really |truly )?impressed\b", "generic admiration"),
    (r"\blove(d)? (what you|your)\b", "generic admiration"),
    (r"\breally resonated\b|\bstood out to me\b.{0,0}$", "false intimacy"),
    (r"\bexciting times\b", "empty enthusiasm"),
    (r"\bas you know\b", "presumes shared knowledge"),
    (r"\bi completely understand\b", "performative empathy"),
    (r"\bhope (this|that) helps\b", "filler close"),
    (r"\bworld[- ]class\b|\bindustry[- ]leading\b|\bnext[- ]generation\b", "self-praise"),
]

# --- direct-response patterns that do not survive the move to cold B2B --------------
# These four lists were derived by running this scorer over classic direct-response
# material -- headline formula sheets, broadcast-email checklists, and a widely
# circulated 5-part consulting sequence. That genre optimises a warm opted-in list; the
# techniques invert in a cold B2B inbox, where there is no relationship to spend and the
# recipient's first question is how you got their address. Every pattern below was a
# miss: real copy the scorer passed. Frameworks are credited in copy-frameworks.md.

# Manufactured urgency. The deadline is the sender's invention, and the recipient knows
# it. Nothing about a cold first contact justifies a countdown.
FALSE_SCARCITY: list[tuple[str, str]] = [
    (r"\blast chance\b", "invented deadline"),
    (r"\bfinal (chance|opportunity|reminder|notice)\b", "invented deadline"),
    (r"\b(only|just)\s+\d{1,2}\s+(spots?|slots?|seats?|places?)\b", "invented shortage"),
    (r"\bafter (that|which),?\s*it'?s gone\b", "invented deadline"),
    (r"\bexpires?\s+(in|at|on|today|tonight|tomorrow)\b", "invented deadline"),
    (r"\b(holding|held|reserv(ing|ed))\s+(a|your|the)\s+(spot|slot|place)\b", "false favour"),
    (r"\bwhile (spots|slots|places|it) last", "invented shortage"),
    (r"\bdon'?t miss out\b", "manufactured urgency"),
    (r"\bact (now|fast|today|quickly)\b", "manufactured urgency"),
    (r"\bclosing (the )?(doors?|list|offer)\b", "invented deadline"),
    (r"\bfor\s+\d{1,3}\s+more\s+(hours?|days?)\b", "invented deadline"),
]

# Guilt and breakup framing. copy-frameworks.md is explicit that the final message
# closes cleanly and stops -- no guilt, no "I'll assume you're not interested".
GUILT_CLOSE: list[tuple[str, str]] = [
    (r"\bthis (will be|is) my last (email|message|attempt)\b", "breakup framing"),
    (r"\bi'?(ll|d) assume you'?re not interested\b", "guilt close"),
    (r"\bi'?d hate to see you\b", "guilt close"),
    (r"\bi (haven'?t|have not) heard (back )?(from you)?\b", "makes silence a debt"),
    (r"\bhaven'?t received a (response|reply)\b", "makes silence a debt"),
    (r"\bi'?ve (reached out|tried|emailed)\s+(a few|several|three|\d+)\s+times\b",
     "makes silence a debt"),
    (r"\byou'?ll hate yourself\b", "guilt close"),
    (r"\bgoodbye from\b", "breakup framing"),
]

# Direct-response headline formulas. Proven in mail order and on sales pages; in a cold
# B2B subject line they read as bulk mail, which is the one thing the subject must not do.
DR_FORMULA: list[tuple[str, str]] = [
    (r"\bwho else wants\b", "mail-order formula"),
    (r"\bthe (real )?secret (to|behind)\b", "mail-order formula"),
    (r"\bdiscover the secret\b", "mail-order formula"),
    (r"\bdo you make these\b.{0,24}\bmistakes\b", "mail-order formula"),
    (r"\bdo you recognize the \d+\b", "mail-order formula"),
    (r"\bthe ugly truth about\b", "mail-order formula"),
    (r"\bwarning\b\s*[-–—:]\s*\bdo not\b", "mail-order formula"),
    (r"\bfinally,?\s+someone reveals\b", "mail-order formula"),
    (r"\bin as little as\b", "mail-order formula"),
    (r"\bquickly (and|&) easily\b", "mail-order formula"),
    (r"\bonce and for all\b", "mail-order formula"),
    (r"\bor your money back\b", "mail-order formula"),
    (r"\bthey laughed when\b", "mail-order formula"),
    (r"\bthe lazy \w+'?s?\s+way\b", "mail-order formula"),
    (r"\bhundreds now\b", "mail-order formula"),
    (r"\bsee how easily\b", "mail-order formula"),
    (r"\b\d+ ways to\b.{0,30}\beven if\b", "mail-order formula"),
    (r"\b(2|3|5|10)x your\b", "unbacked multiplier"),
    (r"\b(double|triple) your\b", "unbacked multiplier"),
]

SUBJECT_RE = re.compile(r"^\s*(?:\*\*)?subject(?:\s*line)?(?:\*\*)?\s*:\s*(.+?)\s*$", re.I | re.M)
# Same line, whole match -- used to take the subject out of the body word budget.
SUBJECT_LINE_RE = re.compile(r"^[ \t]*(?:\*\*)?subject(?:\s*line)?(?:\*\*)?\s*:.*$", re.I | re.M)
# A cold subject earns the open on its own; past this it is truncated in the client
# anyway, and length is where "written to one person" turns back into "broadcast".
SUBJECT_MAX_WORDS, SUBJECT_MAX_CHARS = 9, 60
CAPS_RE = re.compile(r"\b[A-Z]{3,}\b")
# Domain vocabulary that is legitimately upper case and must not read as shouting.
ACRONYMS = {
    "CEO", "CTO", "CFO", "COO", "CMO", "CRO", "SDR", "BDR", "ICP", "KPI", "ROI", "API",
    "CRM", "SAAS", "B2B", "B2C", "SEO", "SEM", "PPC", "USA", "UAE", "KSA", "MENA", "GCC",
    "SLA", "NPS", "ARR", "MRR", "ACV", "CAC", "LTV", "GDPR", "CASL", "CAN", "SPAM",
    "SPF", "DKIM", "DMARC", "AIDA", "TAM", "DMU", "PDF", "URL", "FAQ", "AWS", "GCP",
}

# One hedge marks a hypothesis honestly. Several make the sender sound evasive.
HEDGES = [
    r"\bit looks like\b", r"\bi may be wrong\b", r"\bi might be (wrong|off)\b",
    r"\bi'?d (expect|guess|say|assume)\b", r"\bone possibility\b", r"\busually\b",
    r"\boften\b", r"\btend(s)? to\b", r"\bmight\b", r"\bperhaps\b", r"\bpossibly\b",
    r"\bi think\b", r"\bit seems\b", r"\bcould be\b", r"\bmay be\b",
    r"\bi suspect\b", r"\bmy guess\b", r"\bprobably\b", r"\bin my experience\b",
    r"\bif i had to guess\b", r"\bnot sure (if|whether)\b",
]

# Recipient focus: second person should outweigh first person.
FIRST_PERSON = re.compile(r"\b(i|we|our|us|my|me)\b", re.I)
SECOND_PERSON = re.compile(r"\b(you|your|yours|you're|youre)\b", re.I)

SOFT_CTA = [
    r"\bworth a look\b", r"\bworth (exploring|comparing)\b", r"\buseful if i send\b",
    r"\bshall i send\b", r"\bcan i send\b", r"\bhappy to send\b", r"\bwant me to send\b",
    r"\bon your radar\b", r"\bam i reading\b", r"\bis that (showing up|right)\b",
    r"\bopen to (seeing|a look)\b", r"\bwould that be useful\b",
]
HARD_CTA = [
    r"\bbook a\b", r"\bschedule a\b", r"\bcalendar\b", r"\bcalendly\b",
    r"\bavailab(le|ility)\b", r"\bdo you have \d", r"\bfree (on|next)\b",
    r"\bset up a (call|meeting|demo)\b", r"\bjump on a call\b", r"\bhop on a call\b",
    # "Would you be open to a quick 15-minute call" is the canonical bad ask and must
    # not fall through to the softer "open to ..." patterns below.
    r"\bopen to (a|an|scheduling|booking|setting)\b[^.?]{0,40}\b(call|chat|meeting|demo)\b",
    r"\bwould you be (free|available)\b", r"\b\d{1,3}\s*(-|\s)?\s*min(ute)?s?\b",
    r"\b(a|any) time (next|this) (week|month)\b", r"\bgrab (some )?time\b",
    r"\bconnect (for|on) a (call|chat)\b", r"\bget (something )?on the books\b",
]


@dataclass
class Finding:
    severity: str  # error | warning | info
    code: str
    message: str
    excerpt: str = ""
    penalty: int = 0

    def as_dict(self) -> dict[str, Any]:
        return {
            "severity": self.severity, "code": self.code,
            "message": self.message, "excerpt": self.excerpt, "penalty": self.penalty,
        }


@dataclass
class Message:
    title: str
    text: str
    line: int
    is_message: bool = True
    findings: list[Finding] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    score: int = 100


def line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def sentences_of(text: str) -> list[str]:
    """Split into sentences keeping terminators, so a question stays identifiable."""
    return [s.strip() for s in re.findall(r"[^.!?]+[.!?]*", text) if s.strip()]


def is_title_case(subject: str) -> bool:
    """True when a subject is capitalised like a headline rather than written to a person.

    A subject that looks corporate gets treated as corporate. The first word is excluded
    because sentence case capitalises it too, and acronyms and merge tags are excluded
    because neither says anything about the author's intent.
    """
    cleaned = re.sub(r"\{\{.*?\}\}|\{.*?\}", " ", subject)
    words = re.findall(r"[A-Za-z][A-Za-z'’\-]*", cleaned)
    if len(words) < 4:
        return False
    body = [w for w in words[1:] if len(w) > 3 and w.upper() not in ACRONYMS]
    if len(body) < 3:
        return False
    return sum(1 for w in body if w[0].isupper()) / len(body) >= 0.7


def ask_profile(prose: str) -> tuple[int, int]:
    """Count (hard asks, other asks) by sentence.

    One email, one job. A closing question and a calendar link are two different asks,
    and offering both splits the response rather than doubling it. Counted per sentence
    so that one ask phrased across two clauses does not register as two.
    """
    hard = other = 0
    for s in sentences_of(prose):
        low = s.lower()
        if any(re.search(p, low) for p in HARD_CTA):
            hard += 1
        elif s.endswith("?") or any(re.search(p, low) for p in SOFT_CTA):
            other += 1
    return hard, other


def segment(text: str) -> list[Message]:
    headings = list(HEADING_RE.finditer(text))
    if not headings:
        return [Message("(whole file)", text, 1, True)]
    out: list[Message] = []
    for i, m in enumerate(headings):
        start = m.end()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        title = m.group(1).strip()
        out.append(Message(
            title=title,
            text=text[start:end],
            line=line_of(text, m.start()),
            is_message=bool(MESSAGE_HEADING_RE.search(title)),
        ))
    return out


def strip_markup(text: str) -> str:
    """Remove code fences and merge tags so prose checks see only prose."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"^\s*[|>].*$", " ", text, flags=re.M)  # tables, blockquote markers
    return text


def rendered(text: str) -> str:
    """
    Produce one concrete rendering of the message for prose analysis.

    Spintax is EXPANDED to its first option rather than collapsed -- otherwise every
    prose check is blind to whatever sits inside a spin block, and a banned phrase
    could hide there undetected. Merge tags become a single token, since that is
    roughly what they resolve to.
    """
    def pick(m: re.Match[str]) -> str:
        body = m.group(0)
        inner = body[2:-2] if body.startswith("{{") else body[1:-1]
        if "|" in inner:
            return inner.split("|", 1)[0]  # first spintax option
        return " x "  # merge tag

    return BLOCK_RE.sub(pick, text)


def count_words(text: str) -> int:
    return len(WORD_RE.findall(rendered(text)))


def analyse(msg: Message, max_words: int, allowed_vars: set[str] | None) -> None:
    raw = strip_markup(msg.text)
    prose = rendered(raw)
    # Phrase matching runs against a whitespace-flattened copy. Sequence files are hard
    # wrapped, so any multi-word pattern straddling a line break was silently invisible --
    # "I hope this finds you well" broken after "finds" passed every check. Structure
    # checks (rhythm, closing question) keep the line breaks and use `prose`.
    flat = re.sub(r"\s+", " ", prose).strip()
    low = flat.lower()

    # The word budget is a budget for the BODY. A subject line counted against it made a
    # long subject look like bloated copy and pushed the writer to cut body text that was
    # not the problem. The subject is measured on its own terms below instead.
    words = count_words(SUBJECT_LINE_RE.sub(" ", raw))
    subject_words = count_words(raw) - words
    sentences = [s.strip() for s in SENTENCE_SPLIT_RE.split(prose) if s.strip()]
    sentence_lengths = [len(WORD_RE.findall(s)) for s in sentences if WORD_RE.findall(s)]

    first = len(FIRST_PERSON.findall(prose))
    second = len(SECOND_PERSON.findall(prose))
    hedges = sum(len(re.findall(h, low)) for h in HEDGES)
    tags = re.findall(r"\{\{\s*([A-Za-z_][A-Za-z0-9_.]*)\s*\}\}", msg.text)
    has_question = "?" in prose
    soft = sum(1 for p in SOFT_CTA if re.search(p, low))
    hard = sum(1 for p in HARD_CTA if re.search(p, low))

    # An open question closing the message IS the soft CTA in Poke the Bear -- the
    # skill's own default structure. Without this the prescribed shape scores as
    # having no ask at all.
    body_lines = [ln for ln in prose.strip().splitlines() if ln.strip()]
    closing = " ".join(body_lines[-3:]) if body_lines else ""
    ends_on_question = bool(re.search(r"\?[\s\"')\]]*$", prose.strip())) or "?" in closing
    if ends_on_question and not hard:
        soft += 1

    msg.metrics = {
        "words": words,
        "subject_words": subject_words,
        "sentences": len(sentence_lengths),
        "avg_sentence_words": round(sum(sentence_lengths) / len(sentence_lengths), 1) if sentence_lengths else 0,
        "first_person": first,
        "second_person": second,
        "hedges": hedges,
        "merge_tags": sorted(set(tags)),
        "has_question": has_question,
        "cta": "hard" if hard else ("soft" if soft else "none"),
    }

    if not msg.is_message:
        return

    # --- word budget -------------------------------------------------------------
    if words > max_words:
        msg.findings.append(Finding(
            "error", "TOO_LONG",
            f"{words} words against a {max_words} limit. Cut the sentence that "
            f"explains what the message already implied.",
            penalty=25,
        ))
    elif words < 20 and words > 0:
        msg.findings.append(Finding(
            "warning", "VERY_SHORT",
            f"{words} words. Short is good, but check a signal, an interpretation and "
            f"an ask are all still present.",
            penalty=5,
        ))

    # --- banned phrases ----------------------------------------------------------
    for pattern, why in BANNED_PHRASES:
        for m in re.finditer(pattern, low):
            msg.findings.append(Finding(
                "error", "BANNED_PHRASE",
                f"{why}: \"{flat[m.start():m.end()].strip()}\"",
                excerpt=flat[max(0, m.start() - 20):m.end() + 20].replace("\n", " ").strip(),
                penalty=12,
            ))

    # --- direct-response imports that do not survive the move to cold B2B --------
    for pattern, why in FALSE_SCARCITY:
        for m in re.finditer(pattern, low):
            msg.findings.append(Finding(
                "error", "FALSE_SCARCITY",
                f"{why}: \"{flat[m.start():m.end()].strip()}\". The deadline is yours, "
                f"not theirs, and a cold recipient can tell.",
                excerpt=flat[max(0, m.start() - 20):m.end() + 20].replace("\n", " ").strip(),
                penalty=15,
            ))

    for pattern, why in GUILT_CLOSE:
        for m in re.finditer(pattern, low):
            msg.findings.append(Finding(
                "error", "GUILT_CLOSE",
                f"{why}: \"{flat[m.start():m.end()].strip()}\". Silence is not a debt. "
                f"The last message closes the loop and stops.",
                excerpt=flat[max(0, m.start() - 20):m.end() + 20].replace("\n", " ").strip(),
                penalty=12,
            ))

    subjects = SUBJECT_RE.findall(msg.text)
    for pattern, why in DR_FORMULA:
        m = re.search(pattern, low)
        if not m:
            continue
        hit = flat[m.start():m.end()].strip()
        where = "subject" if any(hit.lower() in s.lower() for s in subjects) else "body"
        msg.findings.append(Finding(
            "warning", "DR_FORMULA",
            f"{why} in the {where}: \"{hit}\". Proven on a warm opted-in list; in a cold "
            f"B2B inbox it reads as bulk.",
            penalty=8,
        ))

    for subj in subjects:
        subj_rendered = rendered(subj)
        n_words, n_chars = len(WORD_RE.findall(subj_rendered)), len(subj_rendered)
        if n_words > SUBJECT_MAX_WORDS or n_chars > SUBJECT_MAX_CHARS:
            msg.findings.append(Finding(
                "warning", "SUBJECT_TOO_LONG",
                f"Subject is {n_words} words / {n_chars} chars against "
                f"{SUBJECT_MAX_WORDS} / {SUBJECT_MAX_CHARS}. It truncates in most clients, "
                f"and length is where a subject stops reading as one person writing.",
                penalty=6,
            ))
        if is_title_case(subj):
            msg.findings.append(Finding(
                "warning", "TITLE_CASE_SUBJECT",
                f"Subject is in Title Case: \"{subj}\". Companies capitalise like that; "
                f"people writing to one person do not.",
                penalty=5,
            ))

    shouty = sorted({w for w in CAPS_RE.findall(flat) if w.upper() not in ACRONYMS})
    if shouty:
        msg.findings.append(Finding(
            "warning", "SHOUTY_CAPS",
            f"Capitalised for emphasis: {', '.join(shouty)}. Emphasis by shouting is a "
            f"promotional-tab signal; carry it in the sentence instead.",
            penalty=5,
        ))

    hard_asks, other_asks = ask_profile(flat)
    if hard_asks and hard_asks + other_asks >= 2:
        msg.findings.append(Finding(
            "warning", "MULTIPLE_ASKS",
            f"{hard_asks + other_asks} separate asks in one message. One email, one job — "
            f"offering a choice splits the response rather than doubling it.",
            penalty=8,
        ))

    # --- recipient focus ---------------------------------------------------------
    if first or second:
        if first > second:
            msg.findings.append(Finding(
                "error", "SENDER_FOCUSED",
                f"{first} first-person words against {second} second-person. The message "
                f"is about you, not them. Rewrite around their situation.",
                penalty=15,
            ))
        elif second and first / max(second, 1) > 0.7:
            msg.findings.append(Finding(
                "warning", "FOCUS_DRIFT",
                f"First-to-second person ratio {first}:{second}. Close to sender-focused.",
                penalty=5,
            ))

    # --- hedging discipline ------------------------------------------------------
    if hedges == 0 and words >= 25:
        msg.findings.append(Finding(
            "warning", "NO_HEDGE",
            "No qualifying language. If the message asserts a problem the prospect has, "
            "it is claiming knowledge you do not have. One hedge is right.",
            penalty=8,
        ))
    elif hedges > 2:
        # The references say "one hedge per message". A >3 threshold let three qualifiers
        # through unflagged -- caught in eval-21, where a message stacked "could be",
        # "could be" and "I'd guess" while asserting it contained one.
        msg.findings.append(Finding(
            "warning", "OVER_HEDGED",
            f"{hedges} hedges. One marks a hypothesis honestly; stacking them reads as "
            f"evasive and buries the point you are making.",
            penalty=8,
        ))

    # --- CTA ---------------------------------------------------------------------
    if msg.metrics["cta"] == "hard":
        msg.findings.append(Finding(
            "warning", "HARD_CTA",
            "Meeting or calendar ask detected. Correct only in a warmed thread -- in a "
            "first touch, ability is the only lever you control. See cta-design.md.",
            penalty=10,
        ))
    elif msg.metrics["cta"] == "none" and words >= 25:
        msg.findings.append(Finding(
            "warning", "NO_CTA",
            "No recognisable ask or offer. The reader does not know what to do.",
            penalty=8,
        ))

    if not has_question and words >= 25:
        msg.findings.append(Finding(
            "warning", "NO_QUESTION",
            "No question. An open question is the cheapest thing a recipient can answer.",
            penalty=6,
        ))

    # --- specificity -------------------------------------------------------------
    if allowed_vars is not None:
        unknown = [t for t in set(tags) if t not in allowed_vars]
        if unknown:
            msg.findings.append(Finding(
                "error", "UNKNOWN_VAR",
                f"Merge tag(s) with no producing column: {', '.join(sorted(unknown))}. "
                f"These render blank on every send.",
                penalty=25,
            ))

    if words >= 25 and not tags and not re.search(r"\d", prose):
        msg.findings.append(Finding(
            "warning", "NO_SPECIFICS",
            "No merge tags and no numbers. Strip the name and this could go to anyone.",
            penalty=10,
        ))

    # --- rhythm ------------------------------------------------------------------
    if len(sentence_lengths) >= 3:
        spread = max(sentence_lengths) - min(sentence_lengths)
        if spread <= 3:
            msg.findings.append(Finding(
                "info", "UNIFORM_RHYTHM",
                f"Sentence lengths within {spread} words of each other. Even cadence "
                f"reads as generated; vary one.",
                penalty=3,
            ))

    msg.score = max(0, 100 - sum(f.penalty for f in msg.findings))


def render_report(result: dict[str, Any]) -> str:
    lines = [f"Message scoring: {'PASS' if result['ok'] else 'FAIL'}", ""]
    for m in result["messages"]:
        if not m["is_message"]:
            continue
        mk = m["metrics"]
        lines.append(f"  {m['title']}  —  {m['score']}/100")
        lines.append(
            f"    {mk['words']}w body"
            + (f" (+{mk['subject_words']}w subject)" if mk.get("subject_words") else "")
            + f" · {mk['sentences']} sentences · "
            f"you/we {mk['second_person']}:{mk['first_person']} · "
            f"{mk['hedges']} hedge(s) · CTA {mk['cta']}"
            + (f" · tags: {', '.join(mk['merge_tags'])}" if mk["merge_tags"] else "")
        )
        for f in m["findings"]:
            mark = {"error": "ERROR  ", "warning": "warning", "info": "info   "}[f["severity"]]
            lines.append(f"    {mark} [{f['code']}] {f['message']}")
            if f["excerpt"]:
                lines.append(f"             …{f['excerpt']}…")
        lines.append("")
    skipped = [m["title"] for m in result["messages"] if not m["is_message"]]
    if skipped:
        lines.append(f"  Not scored (non-message sections): {', '.join(skipped)}")
    return "\n".join(lines)


def main() -> int:
    # Windows consoles default to a legacy codepage and mangle any non-ASCII in the
    # report. Reconfigure rather than restricting the output to ASCII.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

    ap = argparse.ArgumentParser(description="Score outbound messages against the skill's criteria.")
    ap.add_argument("path", nargs="?", help="Sequence file")
    ap.add_argument("--stdin", action="store_true")
    ap.add_argument("--max-words", type=int, default=80)
    ap.add_argument("--min-score", type=int, default=70, help="Fail below this (default 70)")
    ap.add_argument("--vars", type=Path, help="allowed_vars.json from clay_taxonomy.py")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.stdin:
        text = sys.stdin.read()
    elif args.path:
        p = Path(args.path)
        if not p.is_file():
            print(json.dumps({"error": f"File not found: {p}"}), file=sys.stderr)
            return 2
        text = p.read_text(encoding="utf-8", errors="replace")
    else:
        ap.error("Provide a file path or --stdin")
        return 2

    allowed: set[str] | None = None
    if args.vars:
        if not args.vars.is_file():
            print(json.dumps({"error": f"Vars file not found: {args.vars}"}), file=sys.stderr)
            return 2
        data = json.loads(args.vars.read_text(encoding="utf-8"))
        allowed = set()
        cols = data.get("columns", data) if isinstance(data, dict) else data
        for c in cols:
            if isinstance(c, str):
                allowed.add(c)
            elif isinstance(c, dict):
                for k in ("smartlead_field", "name", "output_field"):
                    if isinstance(c.get(k), str):
                        allowed.add(c[k])

    messages = segment(text)
    for m in messages:
        analyse(m, args.max_words, allowed)

    scored = [m for m in messages if m.is_message]
    # An error-severity finding fails the message regardless of total score. A 90 with a
    # merge tag that renders blank to the whole list is not a 90 -- the same hard-gate
    # rule gtm-outbound-score applies at campaign level.
    errors = sum(1 for m in scored for f in m.findings if f.severity == "error")
    ok = bool(scored) is False or (
        errors == 0 and all(m.score >= args.min_score for m in scored)
    )

    result = {
        "ok": ok,
        "min_score": args.min_score,
        "error_count": errors,
        "messages": [
            {
                "title": m.title, "line": m.line, "is_message": m.is_message,
                "score": m.score, "metrics": m.metrics,
                "findings": [f.as_dict() for f in m.findings],
            }
            for m in messages
        ],
    }

    print(json.dumps(result, indent=2) if args.json else render_report(result))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
