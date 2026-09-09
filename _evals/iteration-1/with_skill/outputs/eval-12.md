# Eval 12 — "variant B got 52 positive replies out of 800 sends, variant A got 40 out of 800. B wins right? scaling it now"

## Short answer: no, and I'd hold off on scaling

Ran this through the actual significance test rather than eyeballing the percentages,
per the skill's rule that A/B evaluation is arithmetic and belongs in `gtm_math.py`, not
prose judgment:

```bash
python gtm_math.py ab-eval --a-sends 800 --a-conv 40 --b-sends 800 --b-conv 52
```

```
A/B Significance
================

arms:
  a:
    sends                              800
    conversions                        40
    rate                               0.05
  b:
    sends                              800
    conversions                        52
    rate                               0.065
result:
  observed lift                      0.3
  z score                            1.2887
  p value                            0.1975
  confidence                         0.95
  significant                        no
  verdict                            Inconclusive -- keep running or accept no difference

warning  p = 0.1975 does not clear the 0.05 threshold. The +30.0% difference is within what random variation produces at this sample size. Do not scale the winner yet.
```

**This is exactly the case `gtm-outbound-math`'s reference calls out by name:** "A 30%
observed lift on 800 sends per arm is not a result. It is inside normal variation." The
p-value here is 0.1975 — nowhere near the 0.05 threshold needed to call this significant.
At this sample size, a swing this size is a coin-flip outcome, not evidence B is better.

## Why it looks convincing anyway

52 vs. 40 is a real, visible gap, and a 30% relative lift sounds decisive. But both arms
are working with small numbers — a handful of extra replies in either direction would flip
which one "wins" on the raw count. The test wasn't sized before it ran, so there's no way
to know whether 800/arm was ever enough to detect a real 30% lift with confidence.

Checking that now:

```bash
python gtm_math.py ab --baseline-rate 5 --min-detectable-lift 30 --sends-per-day 240
```

```
A/B Sample Size
===============

test_design:
  baseline rate                      0.05
  target rate                        0.065
  min detectable lift                0.3
  confidence                         0.95
  power                              0.8
requirement:
  sample per arm                     3,132
  total sample                       6,264
  days to conclude                   27
```

**You'd need roughly 3,132 sends per arm — about 4x what you have — before a genuine 30%
lift at a 5% baseline would reliably clear significance.** At 800/arm, this test was
underpowered for the effect size it's now being asked to confirm.

## What I'd do instead of scaling

1. **Keep running both arms**, same allocation, until you're near ~3,100/arm (roughly
   27 days at 240 sends/day combined, per the sizing above) — then re-run `ab-eval` on the
   real numbers.
2. **Don't scale off this result.** If you cut variant A now, you lose the ability to ever
   resolve whether the difference was real, and you've made an infrastructure decision
   (which arm's copy, which CTA, which domains keep sending) on noise.
3. **If the sample requirement itself feels impractical** — 3,100/arm is a lot of volume
   for a niche list — that's a signal to test a bigger structural change (different offer,
   different segment, different CTA type) rather than a subtler copy variant, per the
   math skill's guidance that "small lifts on small baselines are effectively
   unmeasurable in outbound."

Happy to re-run `ab-eval` the moment you have more sends in — it's a one-line change, and
right now is the wrong moment to declare a winner.
