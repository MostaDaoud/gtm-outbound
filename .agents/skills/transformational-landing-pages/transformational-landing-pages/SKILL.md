---
name: transformational-landing-pages
description: >
  Direct-response landing page copywriter and conversion optimization architect
  based on Eddie Shleyner's Very Good Copy masterclass. Crafts high-converting sales
  and opt-in landing pages using the 4 CDCA pillars (Clarity, Desire, Credibility,
  Action), the 7-Divider page sequence, Eugene Schwartz's Clean Window headlines,
  the 6-element Hero, the 18-filter Fascination Vault, Whale and School testimonials,
  and risk-reversal guarantees. Use when user says "landing page", "sales page",
  "write landing page", "fascinations", "hero copy", "convert page", "eddie shleyner",
  "transformational landing page", "improve conversion rate", or "audit landing page".
---

# Transformational Landing Pages (TLP)

A direct-response landing page engine built on the principles of copywriting masters (Eugene Schwartz, Claude Hopkins, Joe Sugarman, Mel Martin, Gary Bencivenga), formulated by Eddie Shleyner (Very Good Copy).

## Quick Reference: The CDCA Engine & 7 Dividers

```
DIVIDER 1: HERO [Clarity + Action]
  -> Primer (ends in colon `:`) + Clean Window Headline + Future Pacing Subhead
  -> Objection-busting Body Copy + Offer Art & Badge + Urgent CTA + Free Downsell
DIVIDER 2: PROOF & RISK REVERSAL [Credibility + Action]
  -> Gary Bencivenga "Show Proof First": Statistics + Logos + Guarantee Seal + CTA
DIVIDER 3: FAST-ACTION CONVERSION [Action + Credibility]
  -> Frictionless 3-Field Form + Whale Testimonial #1 + School Strip #1 + CTA
DIVIDER 4: THE FASCINATION WALL [Desire + Action]
  -> 15-30+ Fascinations across 18 Filters + Checkerboard Grid + Urgent CTA
DIVIDER 5: MID-FUNNEL PROOF [Credibility + Action]
  -> Whale Testimonial #2 + School Testimonials #2 + Urgent CTA
DIVIDER 6: MASSIVE SOCIAL PROOF WALL [Credibility + Action]
  -> School Testimonial Wall #3 (Length Implies Strength Heuristic - LISH) + CTA
DIVIDER 7: FINAL CONVERSION & RE-ASSURANCE [Action + Credibility]
  -> Final Conversion Form #2 + Guarantee Seal + Nothing-to-Lose Reassurance + CTA
```

## Routing & Core Workflows

| User Intent | Primary Action | Reference & Scripts |
|---|---|---|
| **Write New Landing Page** | Plan Person (sans 'a'), generate Hero, draft 7 Dividers, construct Fascination Wall | `references/seven-dividers.md`, `references/hero-anatomy.md`, `scripts/tlp_generate.py` |
| **Audit Existing Page** | Run 100-point CDCA scoring, check 7 dividers, detect guardrail violations | `scripts/tlp_audit.py`, `references/cdca-framework.md` |
| **Write Fascinations** | Extract nuggets, tease value, state benefit, apply 18 filters, format checkerboard | `references/fascination-vault.md` |
| **Hero Optimization** | Craft Primer `:`, Clean Window headline, Future Pacing subhead, Economic CTA | `references/hero-anatomy.md` |
| **Social Proof Architecture** | Deploy Whale endorsements and School walls to trigger LISH | `references/credibility-signals.md` |
| **Testing Strategy** | Test Big Differences first (2x-3x lifts) before single-variable tweaks | `references/testing-methodology.md` |

---

## The 6-Element Hero Protocol (Divider 1)

1. **Primer Copy**: Clarifies category and format; **MUST end with a colon (`:`)** to kickstart Joe Sugarman's *Slippery Slide*.
2. **Hero Headline**: Eugene Schwartz's Clean Window principle. 3 to 7 words. Zero cleverness, zero puns, zero marketese. Look through the words to see the product.
3. **Hero Subhead**: Future pacing the transformation using trigger verbs (`Stop feeling [pain]... Start [desire]...`, `Imagine...`).
4. **Hero Body Copy**: Answers: *"How does this product fulfill this promise?"* Overcomes the primary objection.
5. **Urgent CTA Button**: Economic incentive + parenthetical deadline (`Buy Now -> Save 50% (Don't delay. Flash sale ends tomorrow.)`).
6. **Hero Artwork**: Concrete visual deliverable (mockup, screenshot) + high-contrast flashing discount badge.
- **Transitional Congruence**: The traffic ad must mirror the Hero's copy, layout, and art with 1:1 fidelity. Landing page is always built first.

---

## The 18 Fascination Filters & 9 Guardrails (Divider 4)

### The 9 Guardrails
1. Write 3x-4x what you need, keep top 25%.
2. The more specific the benefit, the better.
3. Prove it (cite page numbers, data, mechanisms).
4. Clarity beats concision.
5. Use simple words.
6. Use the prospect's vocabulary.
7. Avoid "transactional" words (`buy`, `purchase`).
8. Avoid "work" words (`learn`, `study`). Use `discover`, `uncover`.
9. Create variance (checkerboard grid + alternating openings) to defeat LISH fatigue.

### The 18 Filters
- **#1 Mechanism**: The simple "[mechanism]" that [delivers payoff]...
- **#2 Statement+Interest+Benefit**: [Fact]. Did you know [twist]? [Payoff].
- **#3 "What..."**: What you must do immediately before [event] to [gain outcome].
- **#4 "What never..."**: What never to do when [scenario]—and how to avoid [pain].
- **#5 "Right? Wrong..."**: [Common belief], right? Wrong! [Truth].
- **#6 "Why..."**: Why [counterintuitive event happens]—and what it means for you.
- **#7 "When..."**: When [condition] is actually the best time to [act].
- **#8 Specific Question**: [Burning dilemma]? Here is the permanent fix.
- **#9 "If, then..."**: If you are currently [state], discovering this will [payoff].
- **#10 "Quickest, easiest..."**: The easiest way to [goal] without [sacrifice].
- **#11 Number**: [Number] little-known signs of [problem]—and what to do about each.
- **#12 Big Promise**: [VERB] [BIG BENEFIT] without [frustrating chore]!
- **#13 "How..."**: How to [attain dream] using only [ordinary asset]!
- **#14 "Caution..." / "Warning..."**: WARNING: The common [action] that hurts [result].
- **#15 "Truth..."**: THE TRUTH ABOUT [TOPIC]: What insiders will not tell you.
- **#16 "Best..."**: BETTER THAN [STANDARD]: The alternative that delivers [superior result].
- **#17 "Surprising..."**: Can [simple habit] solve [huge problem]? (Surprising answer).
- **#18 "Are you..."**: Are you making these common mistakes with your [topic]?

---

## Deterministic Tool Commands

```bash
# Audit an existing landing page copy against the 100-point CDCA rubric:
python scripts/tlp_audit.py path/to/page.md

# Generate a new 7-divider landing page copy blueprint:
python scripts/tlp_generate.py --product "My Course" --audience "freelancers" --output ./landing_page.md
```

---

## Reference Files

Load on-demand as needed:
- `references/cdca-framework.md` -- The 4 pillars: Clarity, Desire, Credibility, Action
- `references/seven-dividers.md` -- Complete specifications for Dividers 1 through 7
- `references/hero-anatomy.md` -- The 6 Hero elements, clean window, and transitional congruence
- `references/fascination-vault.md` -- 18 filters, 9 guardrails, and master direct-response swipe files
- `references/credibility-signals.md` -- Gary Bencivenga proof-first, statistics, guarantees, Whales & Schools
- `references/action-triggers.md` -- Immediacy drivers: FOMO, ease, risk reversal, 1 CTA per divider
- `references/audience-interview.md` -- Person (sans 'a') vs persona, Andy case study, and Voss mirroring
- `references/testing-methodology.md` -- Eugene Schwartz doctrine: testing big differences vs small tests

---

## Troubleshooting & Quality Gates

- **Low conversions on control**: Do not tweak button colors. Run a **Big Test**: pit a completely transformed 7-divider page against the control.
- **Big Test underperforms**: Revisit the Person (sans 'a'). Did you target the right human? Rewrite the Hero trio (Headline, Subhead, Body) while keeping the fascinations and proof.
- **High bounce rate**: Check **Transitional Congruence**. Does the ad copy and art match the Hero divider 1:1? Eliminate the Curse of Knowledge.
- **Visitor fatigue on bullet points**: Check **Variance**. Ensure fascinations alternate openings across the 18 filters and use a checkerboard UI grid.
