# Eval 11 — "I want 50 meetings a month. My market is about 4000 companies total and I'm getting a 3% reply rate."

## Leading with the constraint

**This goal is not reachable against this market, in a single month, at these rates.** The
math below runs through `gtm_math.py` per the skill's non-negotiable rule ("all arithmetic
goes through `gtm_math.py` — never compute list sizes... in prose"), not estimated.

You gave reply rate (3%) and a TAM (4,000 companies). You didn't give a positive-reply
share or a booking rate, so I used the stated cold-B2B defaults and flagged them as
assumptions, per the skill's "state a default explicitly, flag it, and continue" rule:

- Positive rate: **25%** of replies (default range 20-30%)
- Booking rate: **60%** of positives (skill default)
- Sequence steps: 4 (default)

## Backward mode — what a 50-meeting goal requires

```bash
python gtm_math.py size --meetings-goal 50 --reply-rate 3 --positive-rate 25 --tam 4000
```

```
Campaign Sizing
===============

mode                               backward (from meetings goal)
goal:
  meetings per month                 50
funnel:
  reply rate                         0.03
  positive share of replies          0.25
  booking rate                       0.6
  prospect to meeting rate           0.0045
list:
  prospects needed                   11,112
  raw leads to scrape                15,875
  expected bounces                   333
sending:
  sequence steps                     4
  total sends                        44,448
  sends per day                      2,021
  inboxes required                   81
  domains required                   27
  working days                       22

BLOCKER  This plan needs 15,875 raw leads but the stated TAM is only 4,000. The goal cannot be reached against this ICP -- widen the segment, raise reply rate, or lower the goal.

warning  81 inboxes is a substantial infrastructure footprint to warm and monitor. Improving reply rate or ACV is usually cheaper than adding sending capacity at this scale.
```

This is a **blocker**, not a warning — the script exits non-zero on it. Hitting 50
meetings/month at a 3% reply rate needs ~15,875 raw leads scraped (after accounting for
~30% verification attrition), against a market of 4,000. That's roughly **4x the entire
market**, in one month, every month. No amount of additional inbox or domain capacity
fixes this — the constraint is the market size and the funnel, not send volume.

## What the market can actually support

To show the real ceiling, I ran it forward — what does the *entire* 4,000-company market
produce, contacted once, at the same funnel rates:

```bash
python gtm_math.py size --prospects 4000 --reply-rate 3 --positive-rate 25
```

```
Campaign Sizing
===============

mode                               forward (from list size)
goal:
  meetings per month                 18
funnel:
  reply rate                         0.03
  positive share of replies          0.25
  booking rate                       0.6
list:
  prospects needed                   4,000
  raw leads to scrape                5,715
sending:
  total sends                        16,000
  sends per day                      728
  inboxes required                   30
  domains required                   10
```

**~18 meetings is the ceiling from this market — once, not per month.** And that ceiling
is a one-time number: if you run through the full 4,000-company TAM in a single push, you
don't have a fresh 4,000 to contact again next month. A recurring monthly goal against a
static, finite market either needs the market to refresh with new triggers (new
funding, new hires, etc.) faster than you exhaust it, or it needs to draw from a
meaningfully larger universe.

## What actually closes the gap

In order of leverage, cheapest fix first:

1. **Raise reply rate.** At 3% you're already near the low end of the cold-B2B band
   (3-5%). Getting to the 8% "healthy" ceiling in `deliverability.md`'s monitoring table
   would roughly triple output from the same list — still nowhere near enough alone, but
   it's the only lever that doesn't require a bigger market.
2. **Widen the ICP.** 4,000 is workable-to-tight per `icp-filters.md`'s sanity bands
   (500-25,000 is the usable range) but is the actual binding constraint here. This is a
   case for going back to the offer/sub-niche stage — a broader trigger or an adjacent
   segment, not tighter filters.
3. **Lower the goal to something the market supports on a recurring basis** — e.g., in the
   high single digits to low teens per month, leaving headroom to re-contact the market as
   new triggers appear rather than burning it once.
4. **Add a second, larger market** run in parallel rather than trying to force 50/month out
   of one 4,000-company segment.

I did not adjust the goal or the TAM on your behalf — that's a decision for you, not
something to bury in the model. Send me either a larger TAM or a lower goal and I'll re-run
this in one line.
