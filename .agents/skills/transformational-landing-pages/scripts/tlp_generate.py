#!/usr/bin/env python3
"""
Purpose: CLI generator to scaffold a complete 7-divider Transformational Landing Page
based on Eddie Shleyner's CDCA framework.
Usage: python scripts/tlp_generate.py --product "Title" --audience "Target" --output ./page.md
"""

import argparse
import sys
from pathlib import Path


def generate_markdown(product: str, audience: str, pain: str, dream: str, offer: str) -> str:
    return f"""# {product} — Transformational Landing Page Copy

---

## DIVIDER 1: THE HERO (Clarity & Action)

**[Logo]**: {product.upper()}

**[Primer Copy]**:
A concise, battle-tested system, declared essential for {audience}:

**[Hero Headline]**:
Master {dream}, Confidently.

**[Hero Subhead]**:
Stop struggling with {pain}. Start achieving {dream} with predictability and ease.

**[Hero Body Copy]**:
This comprehensive guide—packed with timeless principles, field-tested mechanisms, and step-by-step frameworks—will teach you how to get results you are proud to deliver.

**[Primary Urgent CTA Button]**:
[Claim Your Copy -> Save 50% (Don't delay. Flash sale ends tomorrow)]

**[Secondary Downsell Link]**:
[Read Chapter 1 -> Free (Instant Digital Download)]

**[Hero Artwork & Incentive Badge]**:
[Digital Product Mockup + High-Contrast Badge: "50% OFF FLASH SALE"]

---

## DIVIDER 2: PROOF & RISK-REVERSAL (Credibility & Action)

**[Statistical Headline]**:
Over 10,000+ {audience} Transformed

**[Statistical Context Copy]**:
Proven in production across 40+ countries and thousands of implementations.

**[Client / Authority Logos]**:
[Logo 1]  |  [Logo 2]  |  [Logo 3]  |  [Logo 4]  |  [Logo 5]

**[Guarantee Seal & Copy]**:
"You don't have to believe me because I believe in myself. If you don't love {product} for any reason, simply let us know within 30 days for a full, prompt, and courteous refund."

**[Urgent CTA Button]**:
[Claim Your Copy -> Save 50% (Don't delay. Flash sale ends tomorrow)]

---

## DIVIDER 3: FAST-ACTION CONVERSION (Action & Credibility)

**[Frictionless 3-Field Conversion Form #1]**:
- Full Name: [                    ]
- Email Address: [                ]
- Payment Method: [ Credit Card / Apple Pay ]
[Complete Order -> Instant Access ($49)]

**[Whale Testimonial #1]**:
"Nobody should attempt {dream} without first studying this framework."
— Renowned Industry Authority

**[School Testimonial Strip #1]**:
- "Saved me 10 hours a week on my very first run." — Alex R.
- "The best single investment I made in my craft this year." — Lisa M.

**[Urgent CTA Button]**:
[Claim Your Copy -> Save 50% (Don't delay. Flash sale ends tomorrow)]

---

## DIVIDER 4: THE FASCINATION WALL (Desire & Action)

**[Fascination Headline]**:
{product}: 1 System. Hundreds of Profound Takeaways.

**[Context Subhead]**:
Here is a small sample of what you'll discover inside:

**[The 18-Filter Fascination Wall]**:
- **Filter #1 (Mechanism)**: The simple "3-point diagnostic" that instantly reveals where you are losing traction...
- **Filter #2 (Statement+Benefit)**: 85% of people fail at {dream} within 30 days. But did you know one subtle shift guarantees sustained progress?
- **Filter #3 (What)**: What you must do immediately before launching to eliminate unexpected surprises.
- **Filter #4 (What Never)**: What NEVER to do when communicating with prospects—and how this common blunder repels buyers.
- **Filter #5 (Right? Wrong)**: Hard work is the key to {dream}, right? Wrong! Discover the leverage principle on page 24.
- **Filter #6 (Why)**: Why traditional methods are quietly failing—and what modern practitioners are doing instead.
- **Filter #7 (When)**: When taking a step back is actually the fastest path to breakthrough speed.
- **Filter #8 (Specific Question)**: Struggling with inconsistent results? Here's the permanent solution.
- **Filter #9 (If, then)**: If you are currently feeling stuck, this single revelation will elevate your performance immediately.
- **Filter #10 (Quickest, easiest)**: The quickest, easiest way to eliminate friction without sacrificing quality.
- **Filter #11 (Number)**: 7 little-known signals of hidden inefficiency—and how to fix each in minutes.
- **Filter #12 (Big Promise)**: ACHIEVE COMPLETE CONFIDENCE IN YOUR WORK without second-guessing yourself!
- **Filter #13 (How)**: How to turn everyday challenges into your biggest competitive advantages.
- **Filter #14 (Warning)**: WARNING: Avoid these 2 outdated practices like the plague!
- **Filter #15 (Truth)**: THE TRUTH ABOUT {product.upper()}: What the industry veterans rarely disclose in public.
- **Filter #16 (Best)**: The single best exercise for mastering this skill—and why it takes less than 10 minutes a day.
- **Filter #17 (Surprising)**: Does brevity really beat thoroughness? (The surprising answer revealed on page 41).
- **Filter #18 (Are you)**: Are you making these common mistakes with your workflow?

**[Urgent CTA Button]**:
[Claim Your Copy -> Save 50% (Don't delay. Flash sale ends tomorrow)]

---

## DIVIDER 5: MID-FUNNEL PROOF (Credibility & Action)

**[Whale Testimonial #2]**:
"This is the clearest, most actionable blueprint on the market today."
— Senior Director of Strategy

**[Urgent CTA Button]**:
[Claim Your Copy -> Save 50% (Don't delay. Flash sale ends tomorrow)]

---

## DIVIDER 6: MASSIVE SOCIAL PROOF WALL (Credibility & Action)

**[School Testimonial Wall #3 (LISH)]**:
[Cluster of 20+ everyday practitioner reviews demonstrating diverse wins, screenshots, and 5-star ratings]

**[Urgent CTA Button]**:
[Claim Your Copy -> Save 50% (Don't delay. Flash sale ends tomorrow)]

---

## DIVIDER 7: FINAL CONVERSION & RE-ASSURANCE (Action & Credibility)

**[Final Conversion Form #2]**:
[Full Name] | [Email Address] | [Payment]
[Get Instant Access -> $49 (Flash Discount Active)]

**[Final Reassurance & Guarantee]**:
"Remember: You have nothing to lose. Every order is backed by our unconditional 30-day money-back guarantee."
"""


def main():
    parser = argparse.ArgumentParser(description="Generate a Transformational Landing Page Blueprint")
    parser.add_argument("--product", default="Scientific Copywriting", help="Product / Offer Name")
    parser.add_argument("--audience", default="modern copywriters", help="Target Audience")
    parser.add_argument("--pain", default="imposter syndrome and self-doubt", help="Core Pain Point")
    parser.add_argument("--dream", default="writing high-converting ads", help="Desired Transformation")
    parser.add_argument("--offer", default="50% Off Flash Sale", help="Urgent Incentive")
    parser.add_argument("--output", default="landing_page_draft.md", help="Output file path")
    args = parser.parse_args()

    md = generate_markdown(args.product, args.audience, args.pain, args.dream, args.offer)
    out_path = Path(args.output)
    out_path.write_text(md, encoding="utf-8")
    print(f"Successfully generated Transformational Landing Page blueprint at: {out_path.resolve()}")


if __name__ == "__main__":
    main()
