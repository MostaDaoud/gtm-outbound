# Eval 28 — 2% to 2.3% after a full email rewrite

Two problems before we talk about what to change next.

## 1. Rewriting the whole email taught you nothing

A cold email is five separable, independently testable blocks: subject line, hook,
value proposition, credibility line, and CTA (`copy-blocks.md`). You changed all five at
once. Even if the number had moved a lot, you would not know *which* block did it — and
you can't productize a result you can't attribute. Test one block at a time going
forward, holding the other four constant.

## 2. Before touching copy again — check upstream first

At a 2% baseline, copy is not necessarily the constraint. Rule out the layers above it:

- **Placement**: is the email landing in the primary inbox, or spam/promotions? A
  deliverability problem looks exactly like a bad-copy problem in the reply-rate number.
- **List**: is this the right ICP, verified and warm-enough sending infrastructure? A
  bad or unverified list caps reply rate regardless of what the email says.

Only once both are clean does it become fair to treat copy as the bottleneck. Rewriting
the whole email skipped this check entirely.

## 3. Is 2% → 2.3% even real?

Sized it rather than eyeballing it:

```
python gtm_math.py ab --baseline-rate 2 --min-detectable-lift 15

A/B Sample Size
===============
test design:
  baseline rate                      0.02
  target rate                        0.023
  min detectable lift                0.15
  confidence                         0.95
  power                              0.8
requirement:
  sample per arm                     36,693
  total sample                       73,386

warning  Detecting a 15.0% lift on a 2.0% baseline needs 36,693 per arm. Small lifts on
         small baselines are effectively unmeasurable in outbound -- test bigger
         structural changes.
```

You'd need ~36,700 sends per arm (73,400 total) to reliably detect a 15% relative lift on
a 2% baseline. Unless your send volume is in that range, 2.3% is almost certainly noise,
not signal — you can't conclude the rewrite worked, or even that it didn't.

## What to change next

1. Check placement and list health first — do not touch copy again until both are ruled
   out.
2. If copy really is clean of upstream problems, revert to the original and change **one
   block** (start with the hook — highest leverage, and per `copy-blocks.md` the block
   most likely to move the number on its own).
3. Run each variant to a volume that actually clears significance for the baseline you're
   at — 2% is a small baseline, so plan for a real sample per `gtm_math.py ab`, not a
   week's worth of sends.
