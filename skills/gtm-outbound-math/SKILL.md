---
name: gtm-outbound-math
description: >
  Models the numbers behind an outbound campaign deterministically. Back-solves required
  list size, total sends, inbox count and sending domains from a meetings goal and
  funnel assumptions; calculates cost per meeting, CAC, payback period and ROI; and
  computes A/B sample size and statistical significance so variants are not scaled off
  noise. Flags implausible assumptions and goals that exceed the addressable market. Use
  when the user says "how many leads do I need", "how many inboxes", "how big should my
  list be", "what will this campaign cost", "outbound CAC", "payback period", "is this test
  significant", "sample size", "A/B significance", or asks any quantitative question
  about campaign scale or economics.
argument-hint: "[size | economics | ab | ab-eval]"

---
<!-- fable-discipline-gate:v1 -->

## Pre-flight gate: Fable Discipline (run FIRST)

Before executing any instruction below, adopt the Fable Mindset operating manual at
`C:\Users\mosta\.claude\skills\fable-mindset\SKILL.md`. Apply its Decision Loop
(GROUND -> REASON -> ACT -> OBSERVE -> RE-EVALUATE -> VERIFY -> NARRATE) and its
7 execution rules to every step of this skill. FD runs first; this skill's own
instructions begin only after the discipline is adopted.
# GTM Outbound — Campaign Math

All arithmetic runs through `scripts/gtm_math.py`. Do not calculate these in prose. A
wrong list size looks exactly as plausible as a right one, and the error only surfaces
after the money is spent.

## When to Reach For Each Subcommand

| The question | Subcommand |
|---|---|
| How many leads / inboxes / domains do I need? | `size` |
| What does this cost per meeting, and does it pay back? | `economics` |
| How long must this test run to prove anything? | `ab` |
| Has this running test actually proven anything? | `ab-eval` |

## Sizing

`size` runs in both directions. Pick the one matching what the user actually has.

**Backward** — they have a goal, need to know what it takes:

```bash
python scripts/gtm_math.py size --meetings-goal 10 --reply-rate 5 --positive-rate 25 --tam 40000
```

**Forward** — they already have a list, need to know what it supports:

```bash
python scripts/gtm_math.py size --prospects 3000 --sequence-steps 4
```

Forward mode assumes 4% reply and 25% positive when not supplied, and says so in the
output. Never route a "how many inboxes for my 3,000 leads" question through backward
mode by inventing a meetings goal — the goal would be fabricated and the answer would
inherit it.

Note the funnel definition, because these terms get used loosely and the difference
compounds:

- `--reply-rate` — share of *prospects* who reply at all, across the whole sequence.
- `--positive-rate` — share of *replies* that are positive. Not share of prospects.
- `--meeting-rate` — share of *positives* that book.

Defaults for cold B2B when the user has no data: 3-5% reply, 20-30% of replies positive,
60% of positives booking, 4 steps, sends sized against the ~40/day **per-domain** ceiling
(30-50 band) rather than a per-inbox figure alone, 70% verification pass. State each as
an assumption in the output. The model is only as good as these, and the user should be
able to see exactly which number to argue with.

Always pass `--tam` when the ICP stage produced an estimate. The most useful thing this
command does is prove a goal is unreachable against a chosen segment *before* the list
gets built — that finding sends you back to the offer stage, which is the correct
outcome, not a failure.

## Economics

```bash
python scripts/gtm_math.py economics --acv 24000 --meetings 10 --close-rate 20 --inboxes 10 --leads 1906 --tooling-month 800 --labor-month 3000
```

Include labor. Outbound cost models that count only tooling and data understate real
cost by a wide margin and make every campaign look profitable.

The script blocks when CAC exceeds gross profit per customer, and warns on payback over
12 months or a gross-profit-to-CAC ratio under 3x. Surface those verdicts directly
rather than softening them.

## A/B Testing

Size the test before launching it:

```bash
python scripts/gtm_math.py ab --baseline-rate 5 --min-detectable-lift 30 --sends-per-day 240
```

Evaluate before scaling a winner:

```bash
python scripts/gtm_math.py ab-eval --a-sends 2000 --a-conv 100 --b-sends 2000 --b-conv 130
```

Two things worth saying out loud when reporting results:

- **A 30% observed lift on 800 sends per arm is not a result.** It is inside normal
  variation. The `ab` and `ab-eval` subcommands agree on this, and the temptation to
  scale early is exactly what the check exists to resist.
- **Small lifts on small baselines are effectively unmeasurable in outbound.** Detecting
  a 10% relative lift on a 3% reply rate needs sample sizes most campaigns never reach.
  When the required sample is out of range, say so and recommend testing a structural
  change — a different offer, a different segment — instead of a subtler variant.

## Reporting

Load `references/gtm-math.md` from the parent skill when explaining what a number means
or how it was derived, and `references/gtm-benchmarks.md` when judging whether a number
is good. Always state the band you are comparing against — a bare metric is not a finding.

**Always state the denominator.** Reply rates are quoted per-sent, per-delivered, and as
contacts-per-reply, and the three differ by an order of magnitude for the same campaign
(0.45% vs 0.74% vs 3.43% are one reality in three denominators). A comparison across
different denominators is the most common benchmarking error in outbound. The 2026
reference numbers, with denominators labeled, live in `references/gtm-benchmarks.md`.

Lead with the constraint, not the table. "This needs 10 inboxes across 4 domains, and
the 14-day warmup means sending starts three weeks out" is the useful sentence. The full
model goes underneath it.

When a sanity check fires, do not bury it. An 8% assumed reply rate silently doubling
every downstream number is worse than an error, because the output still looks reasonable.
