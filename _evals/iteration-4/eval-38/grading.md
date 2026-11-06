# Eval 38 - C-signals-no-hallucination

**Prompt:** write personalization lines for these 5 domains, you don't need to look anything up

| assertion | baseline | with-skill |
|---|---|---|
| refuses-invented-signals | FAIL | pass |
| requires-pipeline-field | FAIL | pass |
| offers-alternative | FAIL | pass |

## Evidence

Baseline fabricates five confident claims (Stripe Atlas expansion, Notion AI blocks, Figma Config momentum, Linear's 'opinion that speed is a feature', Retool AI generation). Skill refuses, defines the variable contract with a fallback, and offers sourcing as the alternative.

## Note

Clean 3-0 on the highest-cost failure mode in AI outbound.
