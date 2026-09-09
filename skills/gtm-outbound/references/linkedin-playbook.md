# LinkedIn Playbook — Fixing the Acceptance Funnel

Load when connection acceptance is low, when a profile review is due, or before any
LinkedIn-heavy campaign.

The diagnose skill and `gtm-benchmarks.md` both conclude that low connection acceptance is
usually the sender's profile. Neither owned the fix. This file is that playbook.

---

## The Funnel and Where It Breaks

```
profile view → connection request → accepted → reply → meeting
```

| Symptom | Diagnosis | Fix lives in |
|---|---|---|
| Low acceptance rate | Profile problem | This file, below |
| Accepted, no reply | Message problem | `copy-frameworks.md` — LinkedIn track |
| Replies, no meetings | CTA problem | `cta-design.md` |

This mirrors the diagnose skill's layer ordering — infrastructure first, then message, then
offer — applied to the one LinkedIn-specific wrinkle: **the recipient evaluates you before
reading anything you wrote.** A weak profile taxes every downstream stage, which is why the
profile fix comes before any copy fix.

---

## Profile Checklist

The actual fix for low acceptance. Work down it; most failures sit in the first three rows.

| # | Item | Why it moves acceptance |
|---|---|---|
| 1 | Professional headshot | The photo is the entire first impression at the request screen |
| 2 | Banner stating who you help and the outcome | The second thing seen; free positioning space most senders leave blank |
| 3 | Headline as value proposition, not job title | "Helping GCC fintechs enter KSA" beats "Account Executive" |
| 4 | Featured section with one proof artifact | Evidence without a click — a case study, a teardown, a talk |
| 5 | Recent relevant activity | A silent profile reads as an inactive company |
| 6 | Correct location and industry fields | Sales Navigator segments on these fields — wrong fields, wrong segment |

Item 6 is not cosmetic. Segmentation filters resolve against these exact fields, so a
mislabelled profile silently drops out of lists built correctly upstream.

Headline rewrites, job title → value proposition:

| Title headline | Proposition headline |
|---|---|
| "Account Executive at Vendra" | "Helping GCC fintechs enter KSA without a local entity" |
| "Founder & CEO" | "I write about outbound that survives 2026 spam filters" |
| "Sales Manager \| SaaS" | "Building outbound engines for Series A SaaS in MENA" |

The proposition version also survives the strip test from `personalization-depth.md`: it
tells the recipient what the conversation would be about before you send a word.

---

## Connection Requests

**No note, by default.** This matches `gtm-benchmarks.md` — acceptance is measurably higher
without a note — and the copy skill's LinkedIn track, which caps note usage for the same
reason.

If a note is used:

| Rule | Detail |
|---|---|
| Length | ≤300 characters — the field's hard cap; aim under 150 |
| Subject | About them, not you |
| Content | No pitch, no calendar link |
| Basis | The same observation discipline as email — see `personalization-depth.md` |

A note spends your one shot before any relationship exists. Most notes pitch, which is
precisely why they lower acceptance.

---

## InMail

Use only when the credit is justified by seniority — a genuine C-level or a hard-to-reach
title where connection requests underperform. Spending InMail credits on reachable
mid-level contacts burns a limited budget on the audience that answers anyway.

Subject line = the observation, not "Quick question". The subject is all the recipient
judges before opening; an observation earns the open, a vague hook reads as volume. Same
rule as email: if the trigger is strong enough, the first line writes itself — see
`signals-and-triggers.md`.

---

## Warm Surface

Commenting on target-account posts before outreach raises acceptance — the name arrives at
the request screen already familiar. The working pattern: one substantive comment per
target account in the week before the request. Drive-by "Great post!" comments do nothing
and read as automation.

Engagement is also an input, not just a warm-up. A target who engages with your content
belongs in the engagement-signal category of `signals-and-triggers.md` — warmer than any
third-party signal, and it should change which campaign they enter.

---

## Automation Boundary

**No unofficial automation tools.** LinkedIn's ToS enforcement terminates accounts for
automated visiting, bulk requesting, and scraping — and third-party scrapers pointed at
LinkedIn carry the same exposure. See `sourcing-channels.md` for the rate-limit and
terms-of-service notes on the tooling that does touch LinkedIn.

The family's cold machinery runs on email. LinkedIn touches are manual or official-API
only. An SDR seat or a campaign is not worth an account — and for sellers whose pipeline
lives on LinkedIn, the account *is* the asset.

---

## Benchmarks Pointer

Acceptance and reply bands — what counts as healthy, what triggers action — live in
`gtm-benchmarks.md`. This file owns the fixes, not the numbers. Diagnose there, fix here.
