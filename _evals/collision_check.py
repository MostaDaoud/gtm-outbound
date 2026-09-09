#!/usr/bin/env python3
"""
Purpose: Measure activation-collision risk for a new skill against every skill already
         installed. Skills compete for activation through their description text, so
         two skills whose descriptions occupy the same term space will fire on each
         other's prompts. This is measurable before installation.

Method:  TF-IDF cosine similarity over description text, plus exact-match detection on
         quoted trigger phrases (the highest-risk collision signal, since those are the
         literal strings users type).

         These two measure different risks and neither implies the other. A pair can sit
         in the low cosine band and still both claim the literal string a user types.

Usage:
    python collision_check.py --installed ~/.claude/skills --candidate ./gtm-outbound-build

    # Sibling matrix: every pair inside one family, scored against the installed corpus.
    python collision_check.py --matrix . --installed ~/.claude/skills
"""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
from collections import Counter
from itertools import combinations
from pathlib import Path

STOPWORDS = {
    "the", "and", "for", "with", "use", "when", "user", "says", "that", "this", "from",
    "into", "your", "you", "are", "not", "but", "its", "it", "a", "an", "of", "to", "in",
    "on", "or", "by", "as", "is", "be", "at", "any", "all", "can", "has", "have", "each",
    "also", "than", "then", "them", "they", "their", "what", "which", "how", "why",
    "using", "used", "via", "per", "one", "two", "three", "more", "most", "other",
    "including", "includes", "such", "like", "based", "does", "do", "will", "would",
    "should", "may", "might", "must", "before", "after", "during", "while", "about",
}

TOKEN_RE = re.compile(r"[a-z][a-z0-9\-]{2,}")
QUOTED_RE = re.compile(r'"([^"]{3,60})"')


def parse_description(skill_md: Path) -> str | None:
    """Pull the description field out of a SKILL.md frontmatter block."""
    try:
        text = skill_md.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fm = text[3:end]

    # Folded scalar: description: > followed by indented lines.
    m = re.search(r"^description:\s*[>|]\s*\n((?:[ \t]+.*\n?)+)", fm, re.MULTILINE)
    if m:
        return " ".join(line.strip() for line in m.group(1).splitlines())

    m = re.search(r'^description:\s*"?(.+?)"?\s*$', fm, re.MULTILINE)
    return m.group(1) if m else None


def tokenize(text: str) -> list[str]:
    return [t for t in TOKEN_RE.findall(text.lower()) if t not in STOPWORDS]


def tfidf(docs: dict[str, list[str]]) -> dict[str, dict[str, float]]:
    n = len(docs)
    df: Counter[str] = Counter()
    for tokens in docs.values():
        df.update(set(tokens))

    vectors: dict[str, dict[str, float]] = {}
    for name, tokens in docs.items():
        tf = Counter(tokens)
        total = sum(tf.values()) or 1
        vec = {
            term: (count / total) * math.log(n / (1 + df[term]))
            for term, count in tf.items()
        }
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        vectors[name] = {t: v / norm for t, v in vec.items()}
    return vectors


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    smaller, larger = (a, b) if len(a) < len(b) else (b, a)
    return sum(v * larger.get(t, 0.0) for t, v in smaller.items())


def collect(root: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for skill_md in sorted(root.glob("*/SKILL.md")):
        desc = parse_description(skill_md)
        if desc:
            out[skill_md.parent.name] = desc
    return out


def shared_terms(
    va: dict[str, float], vb: dict[str, float], top: int = 5
) -> list[tuple[str, float, float]]:
    """Decompose a cosine into the terms that produce it, largest first.

    Returns (term, contribution, share_of_total). Without this a score is opaque, and an
    opaque score gets acted on wrongly: a pair can sit high purely because both
    descriptions repeat one domain noun they both legitimately own, which is not a
    collision and cannot be fixed by editing. Only a spread across *claim* vocabulary
    means the two skills are actually competing for the same prompts.
    """
    contrib = sorted(
        ((t, w * vb.get(t, 0.0)) for t, w in va.items() if t in vb), key=lambda x: -x[1]
    )
    total = sum(c for _, c in contrib) or 1.0
    return [(t, round(c, 4), round(c / total, 3)) for t, c in contrib[:top]]


def is_parent_child(a: str, b: str) -> bool:
    """True when one skill name prefixes the other, e.g. gtm-outbound / gtm-outbound-copy.

    An orchestrator is *supposed* to share vocabulary with the sub-skills it routes to, so
    these pairs should not be read as collisions.
    """
    lo, hi = sorted((a, b), key=len)
    return hi.startswith(lo + "-")


def run_matrix(args: argparse.Namespace) -> int:
    """Score every pair inside one family against each other.

    --candidate answers "will this new skill fight something already installed". This
    answers "do the members of this set fight each other", which the pairwise mode
    structurally cannot see, since it never compares two candidates.
    """
    family = collect(args.matrix.expanduser())
    if len(family) < 2:
        print(f"Need at least two skills under {args.matrix}; found {len(family)}.")
        return 2

    # IDF should come from the corpus the model actually sees at activation time. Scoring
    # a family against itself alone discounts exactly the domain terms the family shares,
    # which flatters it. Fall back to that only when no corpus is given, and say so.
    corpus, note = dict(family), None
    if args.installed:
        installed = collect(args.installed.expanduser())
        for name in family:
            installed.pop(name, None)
        corpus = {**installed, **family}
    else:
        note = (
            "No --installed corpus given: IDF is computed over the family alone, which "
            "discounts shared domain terms and understates similarity. Pass --installed "
            "for numbers comparable to the pairwise mode."
        )

    vectors = tfidf({k: tokenize(v) for k, v in corpus.items()})
    quoted = {k: {q.lower() for q in QUOTED_RE.findall(v)} for k, v in corpus.items()}

    pairs = sorted(
        (
            {
                "a": a,
                "b": b,
                "similarity": round(cosine(vectors[a], vectors[b]), 4),
                "parent_child": is_parent_child(a, b),
                "shared_trigger_phrases": sorted(quoted[a] & quoted[b]),
            }
            for a, b in combinations(sorted(family), 2)
        ),
        key=lambda p: -p["similarity"],
    )

    # A family sharing a domain has a similarity floor above the 0.35 absolute threshold,
    # so that threshold cannot judge siblings. Calibrate against the family's own spread
    # instead, and only flag what also clears the low band in absolute terms.
    sims = [p["similarity"] for p in pairs]
    ranked = sorted(sims, reverse=True)
    p90 = ranked[max(0, int(len(ranked) * 0.1) - 1)]
    stats = {
        "pairs": len(pairs),
        "median": round(statistics.median(sims), 4),
        "p90": round(p90, 4),
        "max": round(max(sims), 4),
    }
    for p in pairs:
        p["above_family_floor"] = (
            p["similarity"] >= max(p90, 0.12) and not p["parent_child"]
        )
        if p["above_family_floor"]:
            p["driven_by"] = shared_terms(vectors[p["a"]], vectors[p["b"]])

    if args.json:
        print(json.dumps({"stats": stats, "note": note, "pairs": pairs}, indent=2))
        return 0

    print("Sibling collision matrix")
    print(f"  family: {len(family)} skills under {args.matrix}")
    print(f"  corpus: {len(corpus)} skills for IDF\n")
    if note:
        print(f"  NOTE: {note}\n")

    for p in pairs[: args.top_pairs]:
        marks = []
        if p["parent_child"]:
            marks.append("parent/child - expected")
        if p["above_family_floor"]:
            marks.append("ABOVE FAMILY FLOOR")
        suffix = f"   {'; '.join(marks)}" if marks else ""
        print(f"  {p['similarity']:>7.4f}  {p['a']:<26} {p['b']:<26}{suffix}")

    if len(pairs) > args.top_pairs:
        print(f"  ... {len(pairs) - args.top_pairs} further pairs below "
              f"{pairs[args.top_pairs]['similarity']:.4f}")

    print(f"\n  family spread: median {stats['median']:.4f}  "
          f"p90 {stats['p90']:.4f}  max {stats['max']:.4f}")
    print("  Siblings share a domain, so they have a similarity floor the absolute 0.35")
    print("  band cannot judge. Pairs are flagged against this family's own spread.")

    for p in (q for q in pairs if q["above_family_floor"]):
        top_term, _, top_share = p["driven_by"][0]
        print(f"\n  {p['a']} / {p['b']} at {p['similarity']:.4f} is driven by:")
        for term, contribution, share in p["driven_by"]:
            print(f"      {term:<18}{contribution:>8.4f}   {share:>5.0%} of the score")
        if top_share >= 0.5:
            print(f"    {top_share:.0%} of this is the single term \"{top_term}\". If both")
            print("    skills legitimately own that word, the score is near its floor and")
            print("    editing prose will not move it. Judge the claim overlap instead:")
            print("    the shared literal triggers below, and whether one prompt could")
            print("    reasonably want either skill.")

    # Reported separately and unconditionally: a shared literal string is a distinct
    # failure from term-space overlap, and it survives a perfectly clean cosine score.
    shared = [p for p in pairs if p["shared_trigger_phrases"]]
    print(f"\nShared literal triggers ({len(shared)} pair(s))")
    if not shared:
        print("  none - no two skills claim the same quoted phrase.")
    for p in shared:
        tag = " (parent/child - expected)" if p["parent_child"] else "  <-- REVIEW"
        print(f"  {p['a']} / {p['b']}{tag}")
        for phrase in p["shared_trigger_phrases"]:
            print(f"      \"{phrase}\"")

    flagged = [p for p in pairs if p["above_family_floor"]]
    non_pc_shared = [p for p in shared if not p["parent_child"]]
    if not flagged and not non_pc_shared:
        print("\nNothing to review: no non-sibling pair is unusually close, and no two")
        print("skills outside a parent/child relationship claim the same literal phrase.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Activation collision risk analysis.")
    ap.add_argument("--installed", type=Path,
                    help="Corpus of installed skills. Required unless --matrix is used, "
                         "where it supplies IDF and is strongly recommended.")
    ap.add_argument("--candidate", type=Path,
                    help="Skill set to score against --installed.")
    ap.add_argument("--matrix", type=Path,
                    help="Score every pair within this directory against each other, "
                         "instead of scoring a candidate against a corpus.")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--top-pairs", type=int, default=12,
                    help="Rows of the sibling matrix to print (--matrix only).")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.matrix:
        if args.candidate:
            ap.error("--matrix and --candidate are different questions; pass one.")
        return run_matrix(args)
    if not args.installed or not args.candidate:
        ap.error("--installed and --candidate are both required unless --matrix is used.")

    installed = collect(args.installed.expanduser())
    candidate = collect(args.candidate.expanduser())
    for name in candidate:
        installed.pop(name, None)  # ignore a prior install of the same skill

    if not candidate:
        print("No candidate skills found.")
        return 2

    all_docs = {**installed, **candidate}
    vectors = tfidf({k: tokenize(v) for k, v in all_docs.items()})
    quoted = {k: {q.lower() for q in QUOTED_RE.findall(v)} for k, v in all_docs.items()}

    report: dict[str, dict] = {}
    for name in candidate:
        scored = sorted(
            ((other, cosine(vectors[name], vectors[other])) for other in installed),
            key=lambda x: -x[1],
        )[: args.top]

        shared = {
            other: sorted(quoted[name] & quoted[other])
            for other in installed
            if quoted[name] & quoted[other]
        }

        report[name] = {
            "nearest": [{"skill": s, "similarity": round(v, 4)} for s, v in scored],
            "shared_trigger_phrases": shared,
            "max_similarity": round(scored[0][1], 4) if scored else 0.0,
        }

    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    print(f"Activation collision analysis")
    print(f"  candidate skills: {len(candidate)}   installed corpus: {len(installed)}\n")

    risk_found = False
    for name, data in report.items():
        print(f"{name}")
        for entry in data["nearest"]:
            sim = entry["similarity"]
            if sim >= 0.35:
                band, risk_found = "HIGH", True
            elif sim >= 0.22:
                band, risk_found = "moderate", True
            elif sim >= 0.12:
                band = "low"
            else:
                band = "-"
            print(f"    {entry['skill']:<28} {sim:>7.4f}  {band}")
        if data["shared_trigger_phrases"]:
            risk_found = True
            for other, phrases in data["shared_trigger_phrases"].items():
                print(f"    !! shares literal triggers with {other}: {phrases}")
        print()

    print(
        "Bands: HIGH >=0.35 (descriptions overlap enough to compete), "
        "moderate >=0.22, low >=0.12."
    )
    if not risk_found:
        print("No collision risk detected above the low band.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
