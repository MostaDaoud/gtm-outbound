# Eval 34 - B-infra-vs-diagnose-spam

**Prompt:** open rate dropped from 60% to 20%, is my subject line bad

| assertion | baseline | with-skill |
|---|---|---|
| not-copy-first | pass | pass |
| treats-open-rate-as-unreliable | pass | pass |
| asks-for-hard-signals | pass | pass |

## Evidence

Both refuse the copy premise and name Apple MPP. Skill adds the cliff-vs-decline heuristic and points at the existing diagnose script.

## Note

Tie.
