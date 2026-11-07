---
name: copy-lab-lp
description: >-
  Build, structure, or audit long-form landing pages using Eddie Shleyner's Transformational Landing Pages system: the CDCA engine, the 7-Divider sequence, the 6-element hero protocol, the fascination wall, and the Length-Implies-Strength social proof heuristic. Use when the user says "landing page", "sales page structure", "page audit", "hero rewrite", "above-the-fold copy", "opt-in page", "VSL page", "why isn't this page converting", or asks why a page converts poorly. Also use for VSL page skeletons and opt-in pages. Not for standalone ad copy (copy-lab-write), emails (copy-lab-write), or short-form posts (copy-lab-write).
---

# Copy Lab: Landing Pages

Landing page architecture and conversion review, grounded in Eddie Shleyner's
Transformational Landing Pages and Eugene Schwartz's direct-response doctrine.

This skill is the builder and structural reviewer. For scoring an arbitrary piece
of copy, use `copy-lab-critique`. For the persuasion psychology underneath a page,
the lens in `references/lenses/lp-lens.md` is the detailed pass.

## When this applies

- Building a landing page from an offer, a product, or a brief.
- Restructuring an existing page that underperforms.
- Reviewing the hero, the proof sequence, or the CTA cadence.
- Writing a VSL page skeleton or an opt-in page.

Not for: ad copy, email sequences, social posts, or Arabic Gulf localisation
(`copy-lab-gcc` handles that).

## Read before working

Load only what the task needs.

| File | Use it for |
|------|------------|
| `../copy-lab/references/landing-pages.md` | The core system: CDCA, 7 Dividers, hero protocol, fascination wall, LISH |
| `../copy-lab/references/lenses/lp-lens.md` | The 10-step audit pass and the scoring output contract |
| `../copy-lab/references/fascination-bullets.md` | The 21 fascination types and the generation workflow |
| `../copy-lab/references/offers.md` | Price framing, stacking, guarantees, risk reversal |
| `../copy-lab/references/vgc-principles.md` | Anti-Description, Mind Movie, the sentence rules |
| `../copy-lab/references/critique-rubric.md` | The 100-point model if a scored verdict is requested |

To check a claim against the course corpus:

```bash
python /absolute/path/to/copy-lab/scripts/copy_lab.py search "landing page hero" --source all --limit 10
```

## The CDCA engine

Every page balances four pillars. When one is weak, name it before rewriting.

- **Clarity**: the reader understands what this is and who it is for within seconds.
- **Desire**: the reader wants the outcome more than they want the money or the effort.
- **Credibility**: the reader believes the promise is real for someone like them.
- **Action**: the reader knows the next step and sees no friction in taking it.

## Build workflow

1. **Establish transitional congruence.** The hero must mirror the traffic source
   in copy, tone, and promised deliverable. A page that contradicts the ad that
   sent the reader there wastes the click.
2. **Write Divider 1, the hero.** Six elements: primer copy ending in a colon,
   a 3 to 7 word headline with zero cleverness, a subhead that future-paces with
   active verbs, body copy that kills the single biggest friction point, an urgent
   CTA pairing the economic incentive with a parenthetical deadline, and artwork
   showing the concrete deliverable plus a guarantee or discount badge.
3. **Divider 2, proof before pitch.** Hard proof appears before the offer is
   restated: statistics, authority logos, named results, guarantee seal.
4. **Divider 3, fast action.** A form of no more than three fields, plus the first
   whale testimonial: full name, title, headshot, quantifiable result.
5. **Divider 4, the fascination wall.** 15 to 30 curiosity-driven bullets across
   the 18 filters, alternating syntax, concrete benefits, proof locators.
6. **Divider 5, mid-funnel proof.** A second whale, a strip of peer testimonials,
   and a micro-FAQ answering the top friction objections.
7. **Divider 6, the social proof wall.** Dense peer testimonials, long enough that
   the length itself implies strength.
8. **Divider 7, final conversion.** Second form, prominent risk-reversal badge,
   nothing-to-lose reassurance, urgent CTA.
9. **Place one CTA per divider.** Every divider must anchor back to conversion.

## Audit workflow

Follow `lenses/lp-lens.md` step by step: transitional congruence, then the seven
dividers in order, then conversion mechanics, then scoring. Quote the failing line
and supply the replacement.

## Output contract

For a build: deliver the page in the requested format, with `[PROOF NEEDED: type]`
and `[DEADLINE: confirm]` markers where facts are missing. Do not invent them.

For an audit: use the lens output format, with the CDCA scores, the seven-divider
map, a severity-ranked findings table, and a short list of what is already working.

## Hard rules

**Never invent proof.** No statistics, testimonials, client names, or results the
user did not supply. Mark the slot and say what would fill it.

**Never fake scarcity.** Deadlines and seat counts must be real.

**No em dashes.** Not in copy, not in findings. Use commas, colons, parentheses,
or separate sentences.

**Cite the principle.** Name the divider and the file, for example
"Bencivenga Proof First (`landing-pages.md`)".

**Match the requested format.** If they paste MDX, return MDX.