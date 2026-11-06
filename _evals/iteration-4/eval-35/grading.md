# Eval 35 - B-signals-vs-copy

**Prompt:** write me a cold email opener that mentions their recent funding round

| assertion | baseline | with-skill |
|---|---|---|
| defines-the-field | FAIL | pass |
| stays-one-line | FAIL | pass |
| no-invented-facts | FAIL | pass |

## Evidence

Baseline asserts 'Saw you closed your Series B last month' for an unnamed company and writes a full email with a pitch and CTA. Skill emits a ~55-word opener using {{funding_round}}/{{funding_month}} placeholders and states the tags must come from a sourced column.

## Note

Clean 3-0. This is the failure mode the merge was meant to close.
