# Eval 33 - B-infra-vs-math-inbox-count

**Prompt:** how many inboxes and domains do I need to send 2000 emails a day

| assertion | baseline | with-skill |
|---|---|---|
| splits-the-question | pass | pass |
| per-domain-ceiling | FAIL | pass |
| warns-against-concentrating | FAIL | pass |

## Evidence

Baseline: '20-30 sends per inbox/day' and '3-5 inboxes per domain' -> 20-35 domains, i.e. 75-150 sends per domain per day. Skill: 50 domains at the ~40/domain ceiling, and explicit warning that mailboxes divide a domain's reputation budget rather than multiplying it.

## Note

The most consequential difference. Baseline's answer is the pattern the skill names as the classic silent burn.
