**User:** variant B got 52 positive replies out of 800 sends, variant A got 40 out of 800. B wins right? scaling it now

---

Not yet — that's a raw lift of 30% on a small sample, and "looks better" isn't the same as "proven better." Before scaling anything, this needs to go through `gtm_math.py ab-eval` rather than being eyeballed.

## Running the significance check

```
$ python scripts/gtm_math.py ab-eval --a-sends 800 --a-conv 40 --b-sends 800 --b-conv 52

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

**Verdict: not significant. Do not scale B yet.** A p-value of 0.20 means there's roughly a 1-in-5 chance you'd see a gap this big (or bigger) even if A and B were truly identical. That's nowhere near the 0.05 bar this skill uses, and scaling on it risks doubling down on noise.

## What sample size this would actually need

Sizing the test properly, for a 30% relative lift on a 5% baseline rate:

```
$ python scripts/gtm_math.py ab --baseline-rate 5 --min-detectable-lift 30 --sends-per-day 200

A/B Sample Size
===============

test design:
  baseline rate                      0.05
  target rate                        0.065
  min detectable lift                0.3
  confidence                         0.95
  power                              0.8
requirement:
  sample per arm                     3,780
  total sample                       7,560
  days to conclude                   38
```

**You'd need ~3,780 sends per arm (7,560 total) to detect a 30% lift at 95% confidence / 80% power** — you're at 800 per arm, about 21% of the way there. At 200 sends/day split across both arms, that's roughly 38 days to a readable result.

## What to do instead of scaling now

1. **Keep both arms running** at the current split until you're near the ~3,780-per-arm mark, or
2. **Accept the smaller, faster answer**: if 38 days is too long, you're better off testing a bigger structural change (different hook, different CTA type, different segment) that would produce a lift large enough to resolve at your actual volume, rather than continuing to chase this specific 30% swing.
3. Don't add a third variant while this one is unresolved — testing multiple arms at once inflates false positives and makes this exact calculation unreliable.

Scaling B today means committing budget on the strength of a coin-flip-adjacent result. Let it run, or make a bigger bet that doesn't need this much sample to prove itself.
