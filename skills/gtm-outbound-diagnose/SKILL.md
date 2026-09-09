---
name: gtm-outbound-diagnose
description: >
  Diagnoses a live or underperforming outbound campaign from a Smartlead, Instantly, or
  other ESP CSV export, and routes the fix to the correct layer in order:
  infrastructure, then list, then offer, then copy. Detects bounce and spam-complaint
  breaches, individual inboxes landing in spam, segment-level reply variance, and offers
  that generate replies but no interest. Explicitly blocks downstream work while an
  upstream cause is unresolved. Use when the user says "my campaign is not working",
  "reply rate dropped", "why is my outbound failing", "diagnose my campaign", "analyze
  my Smartlead export", "campaign performance", "no one is replying", "my open rate
  fell", "should I rewrite my copy", "audit my live campaign", or shares campaign result
  data. This is the post-launch layer and the campaign has already sent; to gate one that
  has not sent yet, use gtm-outbound-score instead.
argument-hint: "[path to ESP export CSV]"

---
<!-- fable-discipline-gate:v1 -->

## Pre-flight gate: Fable Discipline (run FIRST)

Before executing any instruction below, adopt the Fable Mindset operating manual at
`C:\Users\mosta\.claude\skills\fable-mindset\SKILL.md`. Apply its Decision Loop
(GROUND -> REASON -> ACT -> OBSERVE -> RE-EVALUATE -> VERIFY -> NARRATE) and its
7 execution rules to every step of this skill. FD runs first; this skill's own
instructions begin only after the discipline is adopted.
# GTM Outbound — Campaign Diagnosis

The post-launch layer. Everything else in this skill builds campaigns; this one explains
why a running campaign is failing and, more importantly, what not to touch yet.

**If nothing has sent yet, this is the wrong skill — use `gtm-outbound-score`.** There is
no result data to diagnose, and every threshold below is meaningless without it. A
campaign that has not launched gets gated, not diagnosed.

## The Core Problem This Solves

Every layer failing produces the same visible symptom: replies stopped. Copy is the most
visible layer, so it gets rewritten first. It is usually not the cause.

Diagnose in the order the causes stack:

```
infrastructure  →  list  →  offer  →  copy
```

**A broken upstream layer masks everything downstream.** Testing new copy while one inbox
is in spam produces a meaningless result and burns the test budget. Refuse to advance
until the upstream layer is clean, and say so plainly.

## Inputs

**Check for a live connector first.** If an MCP server for the sending platform is
available, pull per-inbox and per-campaign stats, write them to a local CSV in the shape
the script expects, and run the script unchanged. If no connector is present, fall back to
a manual export without comment. Load `references/mcp-integration.md` for the
availability-check pattern and the read/write boundary — this skill never sends.

State which path was used and when the data was pulled. A diagnosis on a three-week-old
export deserves different confidence than one on live data, and the reader cannot tell
otherwise.

An export with, at minimum, a sends column. Bounces, replies, positive replies,
unsubscribes, and complaints all improve the diagnosis. Per-inbox or per-segment rows are
substantially better than a single aggregate row — most real causes are visible only in
the variance between rows.

If the user has only aggregate numbers, run the diagnosis anyway and tell them what the
missing breakdown would have revealed.

## Step 1 — Run the Diagnostic

```bash
python scripts/diagnose_campaign.py export.csv --group-by inbox --baseline-reply-rate 5
```

For a LinkedIn campaign, pass `--channel linkedin`. That funnel has a layer email does
not: **acceptance**. A low connection-acceptance rate is usually the sender's profile
rather than the targeting, and no message rewrite can reach it — the recipient judges you
before reading a word. Diagnose profile, then list, then offer, then copy. The profile
fixes live in `references/linkedin-playbook.md` — route there, do not hand-wave
"improve the profile."

```bash
python scripts/diagnose_campaign.py linkedin-export.csv --channel linkedin
```

Load `references/gtm-benchmarks.md` to judge whether a number is actually bad. Reporting
"3% reply rate" is not a finding; "3% against a 3-8% healthy band" is.

Group by `inbox` first. It is the single highest-yield breakdown, because one dead
mailbox drags the aggregate into a range that looks exactly like weak copy.

Then re-run with `--group-by domain` — the script supports it and the domain is where
reputation actually scores. A campaign with six healthy mailboxes and one over-driven
domain fails at the domain level while every inbox-level row looks fine. The ceiling is
~40 sends/day per domain; `diagnose_campaign.py` flags violations automatically.

Then re-run with `--group-by segment` if the export has segment data, to find targeting
gains available without touching messaging.

**Treat open rate as a trend signal, never a diagnostic.** Apple MPP inflates opens
15-20+ points and AI bot clicks pollute the rest — an "open rate fell" report cannot
distinguish a placement problem from a pixel problem. Diagnose placement from bounce
rate, complaint rate, and reply-rate-per-inbox instead; the full demotion rationale lives
in `references/deliverability.md`.

Do not compute these rates by hand. The thresholds are shared with
`references/deliverability.md` and drift if restated.

## Step 2 — Report the Verdict First

Lead with the layer, not the metrics table:

> Fix the infrastructure layer first. One inbox is at 0.3% reply against a 4.9% median —
> it is landing in spam and dragging the aggregate. The copy is not the problem yet.

Then the evidence, then the action. The metrics table goes last, or in a fold. An
operator reading this wants to know what to do on Monday.

## Step 3 — Honor the Suppression

The script emits a `do_not_yet` list. Reproduce it. This is the most valuable output and
the easiest to soften into uselessness.

If the user pushes back — "I still think it's the copy" — restate the reasoning once,
concretely: a copy test run while an inbox is in spam cannot produce a readable result,
because the variance from placement swamps the variance from wording. Then, if they still
want to proceed, help them do it and note the caveat in the output. It is their campaign.

## Step 4 — Route the Fix

| Primary layer | Route to |
|---|---|
| infrastructure | `references/deliverability.md` — placement, warmup, DNS, recovery. After a domain-recovery pause, re-enter through `gtm-outbound-score` before resuming volume — a re-warmed domain restarting at full rate is a second burn waiting to happen |
| list | `gtm-outbound-list` for sourcing and verification, `gtm-outbound-offer` for filters |
| offer | `gtm-outbound-offer` — re-score the Value Equation, find the weak lever |
| copy | `gtm-outbound-copy` — start with the observation line, not the CTA |

**When the layer is copy, size the test before running it.** `gtm_math.py ab` tells you
whether the change you want to test can be detected at your volume. Most cannot.

## Interpreting the Awkward Cases

**Healthy reply rate, low positive share.** The most misread pattern in outbound. A 5%
reply rate feels like success, but if 6% of those replies are positive, delivery and copy
are both working and people are saying no. That is an offer or segment failure. More
volume makes it worse, not better.

**Sudden collapse versus gradual decline.** Copy fatigue degrades gradually. Placement
collapses. If replies fell off a cliff with no copy change, check placement before
anything else — the timing itself is the evidence.

**Check the calendar before the infrastructure on MENA campaigns.** A reply-rate collapse
during the last ten days of Ramadan or over Eid looks identical to a deliverability event
and is not one. The script cannot see this. Load `references/gcc-market.md` and rule out
seasonality before pausing domains or re-verifying a list that is fine.

**Small samples.** Under a few hundred delivered, most of these rates are noise. Say so
rather than diagnosing confidently off 80 sends.

## Outputs

Write `DIAGNOSIS.md` using `assets/templates/diagnosis.md`:

- The verdict and the responsible layer, first
- Evidence with real numbers
- The do-not-yet list
- The specific next action, routed to the right sub-skill
- What additional data would sharpen the diagnosis next time

## Next

After the fix lands, re-run against a fresh export to confirm the layer actually cleared
before moving down the stack. A fix that was never verified is an assumption.
