# Eval 14 — "we need to launch outbound next week, new domains. what's realistic?"

## Leading with the constraint

**Realistic first send date on brand-new domains is roughly three weeks out, not next
week — and that's the binding constraint on this launch, not the copy or the list.**

This comes straight from `references/deliverability.md`, which is the skill's default
warmup playbook (not a platform hard limit, but a working profile that reflects how mailbox
providers actually evaluate new sending history):

| Phase | Days | Warmup/day | Live sends/day |
|---|---|---|---|
| Cold start | 1-7 | Ramp 5 → 40 | 0 |
| Establish | 8-14 | 40 | 0 |
| First sends | 15-21 | 40 | Ramp 5 → 25 |
| Steady state | 22+ | 40 | 25 |

**Sending begins on day 15 at the earliest**, and that's a floor, not a target — the doc
is explicit that shorter warmup "does not establish enough history to look like a real
mailbox." A domain with zero history sending real cold volume in week one is the exact
pattern mailbox providers screen for, and the damage from front-loading isn't visible
immediately — it shows up a week or two later as a placement collapse that's expensive to
recover from (2-4 weeks minimum, per the recovery playbook, and "some domains do not
recover").

## What "next week" can realistically include

Everything that isn't sending itself can start immediately and should, because it's what
makes day 15 actually achievable:

1. **This week:** register the sending domains (close variants of your primary — e.g.
   `getacme.com`, `acme-hq.com` — never the primary domain itself), set up SPF, DKIM, and
   DMARC (`p=none` to start) on each, configure a custom tracking domain, and start warmup
   immediately. Warmup is the thing with the long lead time, so it's the thing to start
   today, not the list or the copy.
2. **In parallel, over the same window:** build the ICP, source and enrich the list, verify
   it (target under 4% bounce), and write the sequence. None of that is on the domain-age
   critical path — the list and copy stages typically finish well inside three weeks.
3. **Day 15-21:** first live sends, ramping 5→25/day per inbox, while warmup keeps running
   at full volume alongside live sending (warmup doesn't stop when sending starts — it's
   what keeps the engagement ratio that holds placement steady).

## Sizing the infrastructure, so "realistic" has a number attached

I don't have a meetings goal or a list size from you yet, so I'm not going to invent one —
the skill is explicit that forcing a sizing model through a fabricated goal produces a
number that looks precise and isn't. Once you give me either:

- a meetings/month goal (I'll run `gtm_math.py size --meetings-goal ...` to back into
  inbox and domain count), or
- a list size you already have (I'll run it forward instead),

I'll return inbox count, domain count, and the exact first-send date this implies, in one
line. As a planning placeholder: `deliverability.md` recommends ~3 mailboxes per domain and
roughly 20% spare domain capacity, since domains do degrade and rebuilding one costs
another two weeks — worth building that buffer in now rather than after a domain gets
burned mid-campaign.

## The honest framing for whoever set the "next week" deadline

If "launch" means "prospect gets an email in their inbox," next week isn't realistic on new
domains without materially higher deliverability risk. If "launch" means "the campaign is
built, the domains are warming, and the team is ready," that's genuinely achievable next
week — it's just not the same milestone, and I'd say that distinction out loud rather than
let "launched" quietly mean two different things to two different people.
