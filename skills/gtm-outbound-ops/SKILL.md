---
name: gtm-outbound-ops
description: >
  The steady-state operating loop that runs after a campaign launches: the Monday /
  Wednesday / Friday rhythm, positive-reply scoring as the one metric that matters,
  inbox-type deliverability comparisons, and the weekly decision of what to change,
  what to leave alone, and what to kill. Covers reply classification into
  positive / neutral / negative / OOO / bounce / unsubscribe, benchmark bands, how long
  to wait before declaring a result, and the discipline of changing one variable at a
  time. Use when the user says "weekly outbound routine", "what do I do every week",
  "is my campaign working", "positive reply rate", "how many positive replies", "should I
  change this yet", "compare inbox types", "Gmail vs Outlook reply rate", "campaign
  plateaued", "when do I scale", or "is it too early to judge".
argument-hint: "[weekly | score | compare]"
metadata:
  author: Mostafa Daoud
  version: 3.0.0

---
<!-- fable-discipline-gate:v1 -->

## Pre-flight gate: Fable Discipline (run FIRST)

Before executing any instruction below, adopt the Fable Mindset operating manual at
`C:\Users\mosta\.claude\skills\fable-mindset\SKILL.md`. Apply its Decision Loop
(GROUND -> REASON -> ACT -> OBSERVE -> RE-EVALUATE -> VERIFY -> NARRATE) and its
7 execution rules to every step of this skill. FD runs first; this skill's own
instructions begin only after the discipline is adopted.
# GTM Outbound — Steady-State Operations

Launching is the easy part. This skill is what separates a program from an experiment:
a fixed weekly loop, one metric, and a bias toward not touching a working campaign.

## Quick Reference

| The question | Subcommand | Reference |
|---|---|---|
| What do I do this week? | `weekly` | `references/ops/weekly-rhythm.md` |
| Is this campaign actually working? | `score` | `references/ops/reply-scoring.md` |
| Which inbox type performs best? | `compare` | `references/ops/deliverability-testing.md` |

## The one metric

**Positive replies divided by total sent.** Not open rate, not total replies, not meetings
booked after a heroic follow-up sequence.

Open rate is unreliable since mail privacy protection pre-fetched pixels; it overstates
opens and cannot distinguish a human from an Apple relay. Total replies inflate with
out-of-office and hostile replies. The ratio that predicts revenue is positive replies
over sends, measured on the same denominator every time.

Classify every reply into exactly one bucket: positive, neutral, negative, out-of-office,
bounce, unsubscribe. `scripts/reply_classify.py` does this deterministically, and
`gtm-outbound-reply` handles what to say back. Do not hand-wave an ambiguous reply into
"positive" to make the week look better — that turns the only honest metric into a mood
ring.

## The waiting rule

Do not judge a campaign before roughly **21 days**, and never change two things between
measurements. A campaign at day 6 with 400 sends has produced noise, not a result. Most
"this isn't working" panics are a sample-size problem wearing a strategy costume.

Before declaring a winner, check significance with `gtm-outbound-math` (`ab-eval`). A 30%
observed lift on 800 sends per arm is inside normal variation.

## The weekly loop

`weekly` is a fixed Mon / Wed / Fri rhythm. It is deliberately boring. The point is that
the same checks happen in the same order so a regression is visible as a deviation rather
than discovered three weeks later:

- **Monday** — read last week's numbers, verify infrastructure is still healthy, decide
  whether anything changes this week.
- **Wednesday** — mid-week inspection: bounce composition, spam placement, reply
  classification, whether the sequence is still on schedule.
- **Friday** — close the week, record the experiment state, plan the next variable.

Full detail in `references/ops/weekly-rhythm.md`.

## Infrastructure is part of the loop

Every week, before interpreting any reply number, confirm the mail was deliverable:
auth intact, no domain past its daily ceiling, bounce rate under the threshold. A reply
rate that halves because a domain started spam-filtering looks identical to a reply rate
that halved because the offer is wrong — and the first is far more common. Route to
`gtm-outbound-infra` when infrastructure is the suspected cause.

## Comparing inbox types

`compare` breaks reply, bounce and positive-reply rates down by inbox type (SMTP, Gmail,
Outlook). Use it to find provider-level problems — one inbox type underperforming the
others is a reputation or auth story, not a copy story.

## What to change, in priority order

When the numbers are genuinely bad, fix in this order and stop at the first real problem:

1. **Infrastructure** — auth, reputation, ceiling, bounce rate
2. **List** — wrong titles, wrong company size, unverified emails
3. **Offer** — the sub-niche is too broad or the problem is not painful
4. **Copy** — only after the three above are clean

Most operators invert this order because copy is the fun part. That is why most operators
plateau.

## Handing off

- Infrastructure suspected -> `gtm-outbound-infra`
- Test sizing or significance -> `gtm-outbound-math`
- Experiment design for the next variable -> `references/experiments.md`
- Replying to what came in -> `gtm-outbound-reply`
- Diagnosing a specific export -> `gtm-outbound-diagnose`
