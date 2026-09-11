---
name: gtm-outbound-score
description: >
  Scores an unsent outbound campaign for launch readiness on a 100-point scale across
  five areas — ICP and offer specificity, list and data quality, copy quality, sending
  infrastructure, and compliance and risk. Produces a category breakdown, a prioritized
  fix list ordered by points recoverable per unit of effort, and a launch or hold verdict
  with hard gates that fail the campaign regardless of total score.
  Use when user says "score my campaign", "is this ready to launch", "campaign
  readiness", "review my outbound setup", "audit my campaign before launch", "rate my
  sequence", "grade this campaign", "campaign scorecard", or asks whether a campaign is
  good enough to send. This is the pre-launch gate and nothing has been sent yet; once a
  campaign is live and its results are the question, use gtm-outbound-diagnose instead.
argument-hint: "[campaign directory, or paths to the artifacts]"

---
<!-- fable-discipline-gate:v1 -->

## Pre-flight gate: Fable Discipline (run FIRST)

Before executing any instruction below, adopt the Fable Mindset operating manual at
`C:\Users\mosta\.claude\skills\fable-mindset\SKILL.md`. Apply its Decision Loop
(GROUND -> REASON -> ACT -> OBSERVE -> RE-EVALUATE -> VERIFY -> NARRATE) and its
7 execution rules to every step of this skill. FD runs first; this skill's own
instructions begin only after the discipline is adopted.
# GTM Outbound — Campaign Readiness Score

A pre-launch gate. Scores the artifacts the other sub-skills produce and returns a
verdict with a ranked fix list.

**If the campaign has already sent, this is the wrong skill — use
`gtm-outbound-diagnose`.** "Audit my campaign" and "review my outbound" reach here on
wording alone, and the two skills look similar from outside: both assess a campaign, both
return a ranked fix list. The difference is that once a campaign is live, its results are
the evidence, and scoring the artifacts ignores them. Confirm nothing has gone out before
scoring; if it has, hand over and say why.

## Inputs

Whatever exists in the working directory: `ICP-BLUEPRINT.md`, `icp.json`, `LIST-SPEC.md`,
`clay-table.json`, `SEQUENCE.md`, `smartlead-config.json`.

Missing artifacts are not scored as zero — they are scored as **unknown**, and the
maximum drops accordingly. Report the score as `earned / available` and say which
categories could not be assessed. A campaign that scores 71/75 with no sequence written
is not a 95%; it is an incomplete campaign.

## Scoring

### 1. ICP & Offer Specificity — 25 points

| Points | Criterion |
|---|---|
| 5 | Sub-niche is the intersection of vertical, trigger, and company shape — not one of the three |
| 5 | Trigger event has a timestamp and a recency window |
| 5 | Value Equation scored, weakest lever named and addressed |
| 5 | UVP names a measurable outcome and a mechanism, not just an outcome |
| 5 | Exclusion list exists and covers titles, company types, and suppression lists |

### 2. List & Data Quality — 25 points

| Points | Criterion |
|---|---|
| 5 | At least two sourcing channels, one carrying the trigger |
| 5 | Domain resolution runs before any paid enrichment |
| 5 | ICP filter applied before contact discovery and research columns |
| 5 | Waterfall ordered cheap to expensive with every later step gated |
| 5 | Verification stage present, gating on valid only |

Run `clay_taxonomy.py validate` — its errors map directly onto the last two rows.

### 3. Copy Quality — 25 points

| Points | Criterion |
|---|---|
| 5 | Email 1 under 80 words in its longest variant |
| 5 | Email 1 opens on a specific observation, not an industry or a compliment |
| 5 | No pitch, calendar link, or meeting ask in email 1 |
| 5 | Spintax validates clean, every merge tag has a producing column |
| 5 | Follow-ups each add a new angle rather than bumping |

Score this category with the scripts, not by reading:

```bash
python scripts/validate_spintax.py SEQUENCE.md --vars allowed_vars.json --max-words 80
```

```bash
python scripts/score_message.py SEQUENCE.md --vars allowed_vars.json
```

`score_message.py` returns a per-message score out of 100. Any error-severity
finding fails the message outright, matching the hard-gate rule below.

### 4. Infrastructure — 15 points

| Points | Criterion |
|---|---|
| 5 | Sending domains separate from the primary company domain |
| 5 | SPF, DKIM, and DMARC configured on every sending domain |
| 5 | Warmup duration and volume set, first-send date respects it, **and** the send plan clears the ~40/day per-domain ceiling (mailboxes × per-inbox rate ≤ ceiling) |

The ceiling check is not optional bookkeeping — a plan of 3 mailboxes at 25/day per
inbox puts 75/day on one domain, and no per-inbox number will catch it. If the plan
fails the arithmetic, this row scores 0 and the fix list says "add domains" rather than
"lower quality."

### 5. Compliance & Risk — 10 points

| Points | Criterion |
|---|---|
| 4 | Physical address and working opt-out in the footer |
| 3 | Suppression list exists and is shared across all campaigns and domains (procedure: `references/suppression-mechanics.md`) |
| 3 | Jurisdiction identified, consent model named, and required artifacts present (`references/compliance-gates.md`) — "jurisdiction identified" without a consent basis scores 0 |

## Hard Gates

These fail the campaign at any total score. A 92 with a broken merge tag is not a 92 — it
is a campaign that ships blank personalization to the entire list.

- [ ] `validate_spintax.py` exits clean
- [ ] `clay_taxonomy.py validate` exits clean
- [ ] A verification stage exists
- [ ] Sending domain is not the primary company domain
- [ ] Opt-out mechanism present
- [ ] Suppression list exists and covers every campaign and domain
- [ ] Consent basis documented for every jurisdiction on the list

Any unchecked box means **HOLD**, and the fix list leads with it.

## Bands

| Score | Verdict |
|---|---|
| 90-100 | Launch |
| 75-89 | Launch after the listed fixes |
| 60-74 | Hold — a category is structurally weak |
| Under 60 | Hold — rebuild the weakest category before proceeding |

## The Fix List

Rank by **points recoverable per unit of effort**, not by points alone. Five points from
adding exclusion keywords takes ten minutes; five points from re-scoping the sub-niche
takes a day and invalidates the list. Say which is which, and put the cheap ones first —
a fix list nobody acts on is worth nothing.

For each item: the category, the points at stake, the specific change, and the effort.

## Output

`CAMPAIGN-SCORE.md`, using `assets/templates/campaign-score.md`:

- Verdict and total as `earned / available`
- Hard gate results, first, before the category table
- Category breakdown with per-criterion detail
- Ranked fix list with effort estimates
- Categories that could not be assessed and why

## Honesty Requirement

Score what is there, not what was intended. If the ICP blueprint says "trigger: recently
funded" with no window, that is not 5 points for having a trigger — an unbounded trigger
decays into a static filter within a quarter. Generous scoring here produces a campaign
that fails after the money is spent, which is a far more expensive way to learn the same
thing.

## Next

A score is not a deliverable. Route the top of the fix list to the sub-skill that owns it,
and say which one you are handing to:

| Weakest category | Route to |
|---|---|
| ICP & offer specificity | `gtm-outbound-offer` — re-score the Value Equation, tighten the sub-niche |
| List & data quality | `gtm-outbound-list` for sourcing and routing, `gtm-outbound-clay` for the table itself |
| Copy quality | `gtm-outbound-copy` — start from the failing validator finding, not from a rewrite |
| Infrastructure | `references/deliverability.md` — domains, DNS, warmup schedule |
| Compliance & risk | The consent-basis gap routes to `references/compliance-gates.md`; the footer to `gtm-outbound-copy`; suppression mechanics to `gtm-outbound-reply` |

**On a HOLD verdict, route the failing hard gate first** regardless of which category
scores lowest. A broken merge tag outranks a weak UVP — one ships blank personalization to
the whole list, the other underperforms.

**Re-score after the fixes land.** A score that was never re-run is a to-do list, not a
gate, and the number that mattered was always the second one. Once the verdict is Launch,
the campaign goes live and `gtm-outbound-diagnose` takes over from the first export.
