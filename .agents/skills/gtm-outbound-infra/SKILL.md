---
name: gtm-outbound-infra
description: >
  Builds and maintains the sending infrastructure a cold outbound program runs on:
  domain generation and purchase, mailbox provisioning, warmup ramps, SPF/DKIM/DMARC
  authentication, spam-placement testing, incident triage when deliverability breaks,
  and the weekly keep/cancel/promote/buy decision for a sending fleet. Diagnoses why
  mail lands in spam, why bounce rates spike, and how many inboxes a send goal actually
  requires. Use when the user says "set up domains for cold email", "buy domains",
  "provision inboxes", "warmup settings", "is my domain burned", "I landed in spam",
  "bounce rate is too high", "blacklisted", "SPF DKIM DMARC", "spam test", "how many
  inboxes do I need", "cancel domains", "sending reputation", or "my open rate dropped".
argument-hint: "[audit | domains | warmup | incident | lifecycle]"
metadata:
  author: Mostafa Daoud
  version: 3.0.0

---
<!-- fable-discipline-gate:v1 -->

## Pre-flight gate: Fable Discipline (run FIRST)

Before executing any instruction below, adopt the Fable Mindset operating manual at
`C:\Users\mosta\.claude\skills\fable-mindset\SKILL.md`. Apply its Decision Loop
(GROUND -> REASON -> ACT -> OBSERVE -> RE-EVALUATE -> VERIFY -> NARRATE) and its
7 execution rules to every step of this skill. FD runs first; this skill's own
instructions begin only after the discipline is adopted.
# GTM Outbound — Sending Infrastructure

Infrastructure is the part of outbound that fails silently. Copy that never arrives
looks exactly like copy that nobody answered. Before any diagnosis of a reply rate, rule
out that the mail was never delivered — in that order, every time.

## Quick Reference

| The question | Subcommand | Reference |
|---|---|---|
| Is this program even healthy? | `audit` | `references/infra/deliverability-audit.md` |
| What domains and inboxes do I need, and how do I buy them? | `domains` | `references/infra/domains.md` |
| How do I warm these up without burning them? | `warmup` | `references/infra/inbox-warmup.md` |
| I am in spam / bouncing / blacklisted, right now | `incident` | `references/infra/deliverability-incident.md` |
| Which domains do I keep, promote, cancel, or replace? | `lifecycle` | `references/infra/inbox-lifecycle.md` |

## The order of operations

Never start at `domains`. Starting there is how people buy 20 domains to fix a problem
that was, in fact, a missing DMARC record on the one domain they already owned.

1. **Audit what exists.** Authentication, inbox reputation, spam placement, bounce
   composition, per-domain send volume. Most "deliverability problems" are one of four
   things: missing or broken auth, a domain sent past its ceiling, a list with a
   catch-all problem, or content that trips filters.
2. **Only then** decide whether the fix is provisioning, warmup, list hygiene, or copy.
3. **Only then** spend money.

## The ceiling that governs everything

The single number that constrains fleet size: **roughly 40 sends per domain per day**,
and the usable band is 30-50. That is a per-domain figure, not per-inbox. Splitting one
domain across four inboxes does not quadruple safe volume — it concentrates risk on one
domain and can burn all four mailboxes together.

So fleet size is a division problem with a warmup lead time attached:

```
domains needed = ceil(daily sends / 40)
inboxes        = domains x inboxes-per-domain (2-3 typical)
lead time      = 14 days warmup + buffer before the first campaign send
```

Run `gtm-outbound-math` for the fleet arithmetic and this skill for what to actually
provision. If someone asks "how many inboxes", answer with domains first — the inbox
count is downstream of the domain count, and quoting inboxes alone is how people end up
with 40 mailboxes on 3 domains and a burned reputation.

## Audit before you blame copy

`audit` checks, in this order: SPF, DKIM, DMARC alignment, then inbox-level warmup state
and reputation, then a spam-placement test, then bounce composition, then per-domain
volume against the ceiling.

The 1% rule: **bounce rate above roughly 1-2% is an infrastructure and list problem, not
a copy problem.** At 3% many senders pull the domain from rotation automatically. Do not
optimize subject lines while the list is bouncing.

## Incident triage

When deliverability breaks, the instinct is to change the copy. Resist it. Work the
decision tree in `references/infra/deliverability-incident.md`: identify the failure mode
first (spam placement, hard bounces, blacklisting, warmup block, or reputation hit), because
each has a different remedy and the wrong remedy makes it worse. Pausing a warm domain is
often the correct first move and costs nothing.

## Fleet lifecycle

Domains are consumables, not assets. `lifecycle` runs the weekly loop: which domains are
healthy and can take more volume, which are burned and must be cancelled, which to buy as
replacements, and how far ahead to buy them. Replacements need roughly a month of lead
time, so the buy decision is always made before the need is urgent.

## Optional tooling

`optional/scripts/` contains Node/TypeScript helpers for the API-driven parts of this
work (domain purchase, inbox provisioning, auth checks, spam tests). They require Node 18+,
`npx tsx`, and the relevant API keys, and they are deliberately **outside** the
zero-dependency core — `preflight.py` does not cover them. See `optional/README.md`.

Everything above works without them. The scripts automate; the decision logic lives in
the references and does not depend on any API.

## Handing off

- Fleet size unknown -> `gtm-outbound-math`
- Auth and warmup healthy, replies still low -> `gtm-outbound-diagnose`
- Copy is the suspected cause -> `gtm-outbound-copy` (and check `references/spam-rules.md`)
- Live campaign needs ongoing inspection -> `gtm-outbound-ops`
