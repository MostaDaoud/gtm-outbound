# Eval 39 - C-ops-significance-before-scale

**Prompt:** variant B got 30% more replies than variant A on 800 sends each, scale B

| assertion | baseline | with-skill |
|---|---|---|
| checks-significance | pass | pass |
| calls-it-noise | pass | pass |
| does-not-scale | pass | pass |

## Evidence

Both refuse; baseline computes z ~= 1.4 by hand and estimates 3,000-5,000 per arm, which is close to the skill's 4,783. Skill runs ab-eval.

## Note

Tie on substance; the skill's figure is reproducible, the baseline's is unverifiable arithmetic.
