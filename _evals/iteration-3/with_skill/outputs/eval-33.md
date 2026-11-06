# Eval 33 — B-infra-vs-math-inbox-count

**Prompt:** how many inboxes and domains do I need to send 2000 emails a day

**Arm:** with_skill (fresh context)  
**Verdict:** pass

## Assertion results

- [x] **splits-the-question** — Sends the arithmetic to gtm-outbound-math and the provisioning decision to gtm-outbound-infra, or does both explicitly
- [x] **per-domain-ceiling** — Uses the per-DOMAIN ceiling (~40/day, 30-50 band), not a per-inbox figure alone
- [x] **warns-against-concentrating** — Warns that spreading one domain across many inboxes concentrates risk rather than multiplying safe volume

## Evidence

- Answered the arithmetic and the provisioning decision explicitly together: 2,000/day -> 50 domains -> 100 inboxes at 20/day each.
- Led with the per-domain figure: 'The number that decides this is the per-domain ceiling of ~40 sends/day, not a per-inbox rate.'
- Made the concentration risk explicit: 'Splitting a domain across mailboxes divides its reputation budget, it does not multiply it.'

## Note

Recommended provisioning 55-60 rather than the 50 floor, citing warmup lead time for replacements.
