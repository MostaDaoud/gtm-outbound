---
name: copy-lab-critique
description: >-
  Score and audit existing copy against a five-category, 100-point rubric backed by a multi-course library plus provenance-aware local sources, covering audience psychology, structure and clarity, evidence and specificity, voice, and offer. Produces severity-ranked findings with the source principle behind each one and a specific rewritten fix. Use when the user says "critique this copy", "score this copy", "audit this page", "review my sales page", "what's wrong with this email", "why isn't this converting", "roast my copy", "copy-lab critique", "audit these fascination bullets", "review this bullet block", "audit this hook", "review my LinkedIn post", "check my hook", "social hook audit", "audit this for AI-sounding patterns", "why does this sound generic", or pastes existing copy for assessment. Not for writing or fully rewriting copy (copy-lab-write) and not for landing page structure (copy-lab-lp).
---

# Copy Lab: Critique

Audit copy against the 100-point rubric. The goal is findings the user can act
on, each traceable to a principle in the library - not opinion dressed as
authority.

**Shared resources.** References and scripts live in the `copy-lab` skill
folder, not this one: `../copy-lab/references/` and `../copy-lab/scripts/`.
Resolve these sibling-relative paths to absolute paths before reading them. Short
names below - `offers.md`, `sales-pages.md` - mean files there.

When a finding needs evidence beyond the distilled references, search both
collections with `copy_lab.py search "topic" --source all`. Cite course material
with timestamps and books with page/chapter locators. Quote only the minimum
needed to support the finding.

## Step 1: Get the brief, or state it

Medhora's rule governs: **specific questions get specific answers**. Scoring a
page against "is this good?" produces nothing usable.

Establish or assume in writing:

- The one action the piece should cause
- Who the reader is and how aware they are
- Where the traffic comes from
- Whether this is standalone or part of a sequence
- What proof actually exists (missing vs. unavailable are different findings)

Never score without naming the segment. Schutz's telco page reduced conversion
for prospects while increasing renewals for existing customers - the same copy,
opposite results. (`sales-pages.md`)

## Step 2: Read the rubric

Load `../copy-lab/references/critique-rubric.md`. It carries the five categories, their
weights, the per-check failure conditions, and the source behind each.

If the copy contains a fascination or teaser-bullet block, also load
`../copy-lab/references/fascination-bullets.md`. Apply its block-level checks
inside the existing five categories; do not add points or create a sixth
category. Treat an unsupported implication as an unsupported claim, including
when the answer itself is withheld.

For a sales letter, direct-mail piece, print-style ad, proof architecture, or
close, load `../copy-lab/references/classic-direct-response.md`. For welcome
sequences, consulting outreach, sales email QA, or formula-driven headlines,
load `../copy-lab/references/lead-and-email-playbooks.md`. Keep their findings
inside the existing rubric and enforce Copy Lab's proof and scarcity rules over
any source template.

If the user asks whether the copy sounds AI-like, generic, over-polished, or
unlike their voice, also load `../copy-lab/references/anti-generic-copy.md`.
Map its findings into Categories 2, 3, and 4 without adding a sixth category or
an “AI score.” Judge reader-facing properties and never infer authorship or
promise a detector result.

For an ad, headline, positioning line, landing-page first screen, newsletter,
or a complaint that the copy is abstract or interchangeable, also load
`../copy-lab/references/harry-dry-copywriting.md`. Use its visual,
falsifiable, and ownable checks inside Categories 2-4; do not add another score.

For Arabic, Saudi, or Gulf market copy, also load `../copy-lab/references/gcc-copywriting.md`
and run `../copy-lab/references/lenses/gcc-lens.md`. Audit dialect consistency,
regional authenticity (Najd vs Hijaz vs Eastern vs UAE), anti-AI Arabic slop, and
local conversion mechanics (WhatsApp / local payments).

For a landing page, opt-in page, or conversion funnel, also load
`../copy-lab/references/landing-pages.md` and run `../copy-lab/references/lenses/lp-lens.md`.
Audit the 7 Dividers, the 4 CDCA pillars, the 6-Element Hero protocol (primer ending
in colon, Eugene Schwartz Clean Window headline, future-pacing subhead, 2-4 sentence
objection buster, urgent parenthetical CTA, concrete artwork deliverable), Transitional
Congruence, Gary Bencivenga Proof First (Divider 2), Whale vs School testimonials,
the 18-filter Fascination Wall in a checkerboard grid, 1 CTA per divider, and the
3-field frictionless form.

For an editorial newsletter, broadcast email, or storytelling sequence, also load
`../copy-lab/references/vgc-principles.md` and `../copy-lab/references/emails.md`.
Audit against the 5-Beat Micro-Lesson Architecture, the Slippery Slide opening, and
Ed Mayer's 40-40-20 rule.

For a social post, LinkedIn post, or short-form feed hook, also load
`../copy-lab/references/social-hooks.md`. Audit the 1-3 lines before the truncation
point: mobile screen budget (<= 50 chars for full lines, <= 45 chars for last
visible line), Cut-Zone Test at characters 42 and 66 for trailing lines, format
compliance (Dense, Punchy+Context, Single-Line Bomb, Stacked), zero em-dashes, and
strict ban on setup language or generic cliches.

For sentence-level craft, pacing, vocabulary, and narrative flow, also load
`../copy-lab/references/vgc-principles.md`. Audit against the 9 Rules of a Compelling
Sentence (strict ban on work words: learn, study, memorize; strict ban on transaction
words: buy, purchase, pay; Anglo-Saxon simplicity), the 3 Rules of Real Writing (no
character mind-reading, no over-description, present tense), Anti-Description (sparse
prose creating cognitive holes for reader imagination), the Fast Feeling, and the
Rule of 26. Strictly flag any em-dashes as an immediate mechanical defect.

For a value proposition, positioning line, brand promise, homepage hero, or
messaging architecture, also load `../copy-lab/references/positioning.md`. Check
whether the target, outcome, meaningful alternative, and credible differentiator
are present; whether functional, emotional, and self-expressive benefits remain
causally connected; and whether the claimed advantage sits in the
customer/brand/competitor "winning zone." Map findings into the existing five
categories without adding another score.

## Step 3: Score

Work category by category. For each check, score 0-2 and note the evidence: the actual line that fails, quoted.

State **context confidence** before the score:

- **High** - segment, action, traffic, offer, and proof are supplied. Report the
  score with a narrow ±3-point sensitivity range.
- **Medium** - one or two inputs are assumed. Mark the score provisional and
  report ±7 points.
- **Low** - the audience, offer, or traffic context is largely unknown. Report
  a ±12-point range and lead with the assumptions; do not imply exactness.

| Category | Weight |
|----------|--------|
| 1. Audience and psychology | 25 |
| 2. Structure and clarity | 20 |
| 3. Evidence and specificity | 20 |
| 4. Voice and distinctiveness | 15 |
| 5. Offer and action | 20 |

**Parallel option.** If the user explicitly asks for parallel agents, delegate
the review lenses in `../copy-lab/references/lenses/` and merge their findings:

| Lens | Covers |
|-------|--------|
| `psych-lens.md` | Category 1 and the evidence side of 3: persuasion, proof, segments, Person (sans "a"), LISH heuristic |
| `dr-lens.md` | The structure side of Category 2, Category 5, and specificity in 3: AIDA, offers, Gary Bencivenga Proof First |
| `lp-lens.md` | Landing pages: 7 Dividers, CDCA engine, 6-Element Hero, 18-filter Fascination Wall, 3-field forms |
| `voice-lens.md` | The clarity side of Category 2 and Category 4: register, authenticity, 3 Rules of Real Writing, 9 sentence rules, anti-slop |
| `gcc-lens.md` | Arabic/GCC copy: dialect integrity, cultural nuance, anti-slop Arabic |

Otherwise run all lenses inline. Do not spawn agents unless asked. When
merging, score each rubric category once; Categories 2 and 3 have observations
from two lenses but retain their original 20-point caps.

## Step 4: Rank and fix

Every finding needs three parts: **what fails**, **why it fails** (with the
source), and **the specific fix** - a rewritten line wherever a rewritten line
is possible. "Be more specific" is not a finding; "'streamline your workflow' →
'cut weekly reporting from 4 hours to 15 minutes'" is.

Severity:

| Level | Meaning |
|-------|---------|
| **Critical** | Blocks conversion, or is dishonest |
| **High** | Materially reduces performance |
| **Medium** | Leaves value on the table |
| **Low** | Preference or polish |

**Always Critical, regardless of score:** fabricated statistics, invented
testimonials or results, and fake scarcity. Flag these first and say plainly
that they are integrity problems, not optimization problems.

For fascination blocks, also flag any bullet whose promised answer is absent or
materially weaker than the implication. Mark regulated or comparative versions
Critical when the unsupported implication triggers the rubric's evidence floor.

## Step 5: Check whether the copy is even the lever

Two findings the rubric cannot produce:

- **The offer is the problem.** Wendt: would you personally pay for this? If
  not, no rewrite helps. (`offers.md`)
- **The content is the problem.** No hook fixes bad content, the same way no
  marketing fixes a bad product. (`headlines.md`)

If either applies, lead with it. Reporting a score alone implies the words are
the lever, which would be misleading.

## Output format

Use the format in `../copy-lab/references/critique-rubric.md`. Two requirements:

**Quote the failing line.** Every finding cites the actual text.

**Include "What is already working."** Two to four items, always. A critique
that only lists faults invites a rewrite that destroys what worked.

## Handling disagreement

The corpus contradicts itself in places - Medhora considers headlines
over-thought while Morrison calls the headline the most important sentence on
the page. When a finding sits on contested ground, say so and give the reason
you are siding with one source for this piece. Do not present a contested
position as settled.

## Failure and recovery

- If audience or traffic context is missing, state assumptions and use the Low
  or Medium confidence range instead of pretending the score is exact.
- If a cited local source has drifted, omit that citation and re-ingest before
  relying on it.
- If the copy is incomplete, score only the supplied sections and name what was
  out of scope.

## Rewriting

Critique does not rewrite the whole piece. If the user wants that after seeing
the findings, hand off to `copy-lab-write` with the findings as input.

## Forward test

For a request such as “audit this cold email for a CFO,” the result must name
the assumed CFO context, quote every failing line, score all five categories
once, rank the fixes, and preserve at least two things that already work.