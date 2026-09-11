#!/usr/bin/env python3
"""
Purpose: Programmatic 100-point CDCA Audit for Transformational Landing Pages.
Evaluates copy against Eddie Shleyner's direct-response framework:
- Clarity (25 pts): Primer + Colon, Clean Window Headline, Future Pacing, Body Copy, Art, Congruence
- Desire (25 pts): Fascination Wall, 18-Filter Variety, 9 Guardrails, Absence of work/transactional words
- Credibility (25 pts): Proof-First, Statistics, Guarantees, Whale & School Testimonials
- Action (25 pts): Immediacy (FOMO), 1 CTA Per Divider, Lean Form (Ease), Downsell
"""

import argparse
import json
import re
import sys
from pathlib import Path


FORBIDDEN_WORK_WORDS = ["learn", "study", "homework", "curriculum", "syllabus", "effort"]
FORBIDDEN_TRANSACTIONAL_WORDS = ["buy now for $", "purchase this", "spend money", "transaction"]
FUTURE_PACING_TRIGGERS = ["stop", "start", "imagine", "picture this"]


def audit_page(content: str) -> dict:
    scores = {"clarity": 0, "desire": 0, "credibility": 0, "action": 0}
    findings = []
    text_lower = content.lower()

    # --- 1. CLARITY (Max 25 pts) ---
    # Primer check (ends with colon)
    has_primer = bool(re.search(r'(primer|declared|essential|book|guide|course|video).*?:', content, re.IGNORECASE))
    if has_primer:
        scores["clarity"] += 6
        findings.append("PASS (+6): Primer copy detected ending in colon ':'")
    else:
        findings.append("WARN (-6): Missing Primer copy ending in colon ':' in Hero")

    # Headline Clean Window (Short, clear, not overly clever)
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    hero_headline_candidates = [l for l in lines if l.startswith("# ") or "headline" in l.lower()]
    if hero_headline_candidates:
        scores["clarity"] += 6
        findings.append("PASS (+6): Hero Headline detected")
    else:
        scores["clarity"] += 3
        findings.append("WARN (-3): Headline structure ambiguous")

    # Future Pacing Subhead
    has_future_pacing = any(trigger in text_lower for trigger in FUTURE_PACING_TRIGGERS)
    if has_future_pacing:
        scores["clarity"] += 5
        findings.append("PASS (+5): Future pacing detected ('stop', 'start', 'imagine', 'picture this')")
    else:
        findings.append("WARN (-5): Missing future pacing triggers in subhead")

    # Body Copy overcoming objections
    if "concise" in text_lower or "teach you how" in text_lower or "packed with" in text_lower or len(content) > 500:
        scores["clarity"] += 4
        findings.append("PASS (+4): Hero body copy explains mechanism/fulfills promise")
    else:
        findings.append("WARN (-4): Hero lacks objection-busting body copy")

    # Visual Artwork / Mockup indicator
    if "art" in text_lower or "badge" in text_lower or "cover" in text_lower or "mockup" in text_lower or "<img" in text_lower:
        scores["clarity"] += 4
        findings.append("PASS (+4): Concrete visual artwork / incentive badge represented")
    else:
        findings.append("WARN (-4): No concrete visual deliverable representation detected")

    # --- 2. DESIRE (Max 25 pts) ---
    # Fascination Wall presence
    has_fascinations = "fascination" in text_lower or "bullet" in text_lower or content.count("- Filter") >= 3 or content.count("•") >= 5
    if has_fascinations:
        scores["desire"] += 8
        findings.append("PASS (+8): Fascination Wall / Bullets detected")
    else:
        findings.append("CRITICAL (-8): Missing Fascination Wall (Divider 4)")

    # Filter variety
    filter_matches = re.findall(r'Filter #?\d+', content, re.IGNORECASE)
    filter_count = len(set(filter_matches))
    if filter_count >= 5 or content.count("What ") + content.count("Why ") + content.count("How ") >= 4:
        scores["desire"] += 7
        findings.append(f"PASS (+7): High fascination filter diversity detected ({max(filter_count, 5)}+ triggers)")
    else:
        scores["desire"] += 3
        findings.append("WARN (-4): Low fascination filter diversity; utilize more of the 18 filters")

    # Guardrails: Check for forbidden "work" words
    work_words_found = [w for w in FORBIDDEN_WORK_WORDS if re.search(rf'{w}', text_lower)]
    if not work_words_found:
        scores["desire"] += 5
        findings.append("PASS (+5): Clean guardrails: zero 'work' words detected")
    else:
        findings.append(f"WARN (-3): Detected 'work' words ({work_words_found}) in copy; replace with 'discover/uncover'")
        scores["desire"] += 2

    # Guardrails: Check for forbidden "transactional" words in bullets
    trans_words_found = [w for w in FORBIDDEN_TRANSACTIONAL_WORDS if w in text_lower]
    if not trans_words_found:
        scores["desire"] += 5
        findings.append("PASS (+5): Clean guardrails: zero transactional words in body/fascination copy")
    else:
        scores["desire"] += 2
        findings.append("WARN (-3): Detected transactional language outside of explicit CTAs")

    # --- 3. CREDIBILITY (Max 25 pts) ---
    # Statistics presence
    has_stats = bool(re.search(r'(\d+[\d,]*\s*(copies|users|teams|pages|years|million|thousand|%))', content, re.IGNORECASE))
    if has_stats:
        scores["credibility"] += 6
        findings.append("PASS (+6): Quantifiable statistics / proof numbers detected")
    else:
        findings.append("WARN (-6): Lacks specific statistics / scale indicators")

    # Logos / Brand Transfer
    has_logos = "logo" in text_lower or "company" in text_lower or "clients" in text_lower or "brands" in text_lower
    if has_logos:
        scores["credibility"] += 5
        findings.append("PASS (+5): Authority logos / proof-first placement present")
    else:
        findings.append("WARN (-5): Missing client/brand credibility logos")

    # Guarantees & Risk Reversal
    has_guarantee = "guarantee" in text_lower or "refund" in text_lower or "nothing to lose" in text_lower
    if has_guarantee:
        scores["credibility"] += 7
        findings.append("PASS (+7): Unconditional risk-reversal guarantee present")
    else:
        findings.append("CRITICAL (-7): Missing guarantee / risk reversal")

    # Whale & School Testimonials
    has_whale = "whale" in text_lower or "ogilvy" in text_lower or "founder" in text_lower or "expert" in text_lower
    has_school = "school" in text_lower or "reviews" in text_lower or content.count("★") >= 3 or "saying" in text_lower
    if has_whale and has_school:
        scores["credibility"] += 7
        findings.append("PASS (+7): Both Whale (Authority) and School (LISH) testimonials present")
    elif has_whale or has_school:
        scores["credibility"] += 4
        findings.append("WARN (-3): Only one testimonial type present; combine Whales + School Wall")
    else:
        findings.append("CRITICAL (-7): Missing testimonials")

    # --- 4. ACTION (Max 25 pts) ---
    # 1 CTA Per Divider
    cta_count = len(re.findall(r'(buy now|claim|get instant|complete order|add to cart|enroll|register)', text_lower))
    if cta_count >= 5:
        scores["action"] += 8
        findings.append(f"PASS (+8): Strong CTA cadence ({cta_count} CTAs across dividers)")
    elif cta_count >= 2:
        scores["action"] += 5
        findings.append(f"WARN (-3): Moderate CTA cadence ({cta_count} CTAs). Ensure 1 CTA per divider")
    else:
        scores["action"] += 2
        findings.append("CRITICAL (-6): Under-asking! Landing page requires 1 CTA per divider")

    # FOMO & Economic Incentive
    has_fomo = "flash sale" in text_lower or "save " in text_lower or "% off" in text_lower or "tomorrow" in text_lower or "limited" in text_lower
    if has_fomo:
        scores["action"] += 6
        findings.append("PASS (+6): Immediacy established via FOMO / Economic Incentive")
    else:
        findings.append("WARN (-6): Missing economic urgency / deadline (Flash sale / Discount)")

    # Frictionless Form (Ease)
    has_form = "form" in text_lower or "<input" in text_lower or "checkout" in text_lower
    if has_form:
        scores["action"] += 6
        findings.append("PASS (+6): Dedicated frictionless conversion form present")
    else:
        findings.append("WARN (-6): No explicit lean form detected")

    # Downsell Option
    has_downsell = "downsell" in text_lower or "chapter 1" in text_lower or "free" in text_lower or "sample" in text_lower
    if has_downsell:
        scores["action"] += 5
        findings.append("PASS (+5): Free downsell / low-friction alternative present")
    else:
        findings.append("WARN (-5): Missing free downsell option for hesitating visitors")

    total_score = sum(scores.values())

    return {
        "score": total_score,
        "categories": scores,
        "findings": findings
    }


def main():
    parser = argparse.ArgumentParser(description="CDCA 100-Point Landing Page Auditor")
    parser.add_argument("file", help="Path to Markdown or HTML landing page file")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    p = Path(args.file)
    if not p.exists():
        print(f"Error: File '{args.file}' not found.", file=sys.stderr)
        sys.exit(1)

    content = p.read_text(encoding="utf-8", errors="ignore")
    results = audit_page(content)

    if args.json:
        print(json.dumps(results, indent=2))
        return

    print("==================================================")
    print(f"  CDCA LANDING PAGE AUDIT: {p.name}")
    print(f"  OVERALL SCORE: {results['score']}/100")
    print("==================================================")
    print(f"  Clarity:     {results['categories']['clarity']}/25")
    print(f"  Desire:      {results['categories']['desire']}/25")
    print(f"  Credibility: {results['categories']['credibility']}/25")
    print(f"  Action:      {results['categories']['action']}/25")
    print("--------------------------------------------------")
    print("FINDINGS & RECOMMENDATIONS:")
    for f in results["findings"]:
        print(f"  • {f}")
    print("==================================================")


if __name__ == "__main__":
    main()
