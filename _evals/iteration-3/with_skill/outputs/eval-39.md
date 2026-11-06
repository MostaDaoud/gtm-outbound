# Eval 39 — C-ops-significance-before-scale

**Prompt:** variant B got 30% more replies than variant A on 800 sends each, scale B

**Arm:** with_skill (fresh context)  
**Verdict:** pass

## Assertion results

- [x] **checks-significance** — Requires a significance check (gtm-outbound-math ab-eval) before scaling
- [x] **calls-it-noise** — Identifies that this lift on this sample is inside normal variation
- [x] **does-not-scale** — Does not recommend scaling on this evidence

## Evidence

- Ran gtm_math.py ab-eval across the plausible baseline band rather than eyeballing the lift.
- 'Don't scale B. On 800 sends per arm, that lift is noise.' and 'not significant at 95%' in every scenario.
- Refused the scale decision and gave the required sample instead: ~4,783 sends per arm at a 4% baseline.

## Note

Also redirected from total replies to positive replies / sends, which is the metric the ops skill specifies.
