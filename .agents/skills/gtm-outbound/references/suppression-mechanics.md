# Suppression Mechanics

Suppression is a hard gate in two skills (score category 2 and the reply skill's
unsubscribe mandate) and a 2-day SLA in `deliverability.md`. None of them owned the
procedure. This file does, because "suppress immediately and permanently across every
campaign and domain" is a requirement, not a mechanism.

One recipient who opted out and gets mailed anyway is a complaint generator. Complaints
throttle domains — the failure arrives at the infrastructure layer and looks like
deliverability, which is why it must be impossible by construction rather than avoided
by memory.

## The Canonical Artifact

One suppression list per workspace. Local file, not an ESP feature — ESP-native
suppression is per-workspace, and this list must be **cross-campaign and cross-domain**
by default. The local list is what makes it cross-ESP.

```
email,suppressed_at,reason,source_campaign,re_eligible_date
jane@acme.com,2026-09-09,unsubscribe,q3-saas-ctas,
bob@gulfcorp.sa,2026-09-01,not_now,q3-gcc-pilot,2026-12-01
```

Rules:

- **One row per email address**, never per campaign. Re-suppression updates the row; it
  never duplicates it.
- **reason** is one of: `unsubscribe`, `gdpr_request`, `bounce`, `complaint`,
  `not_now`, `hard_bounce`.
- **re_eligible_date** is populated ONLY for `not_now`. Every other reason suppresses
  permanently — a re-eligible unsubscribe is a compliance incident, not a campaign
  decision.
- Cross-domain is the default. A per-campaign exception must be explicit, documented,
  and rare (transactional vs cold separation is the only routine one).

## Intake Paths

| Source | Procedure | SLA |
|---|---|---|
| `reply_classify.py --suppression-out` | Append the output to the canonical list, same session | Same day |
| Manual unsubscribe in any inbox | Append by hand (reason `unsubscribe`) | 2 days |
| GDPR erasure / objection request | Append (reason `gdpr_request`); also note the request date in `source_campaign` | 2 days |
| Bounce past the danger threshold | Append the domain's hard bounces at domain-pull time (reason `bounce`) | At pull |
| Customer / live-opportunity list | Build the do-not-contact list from these **before launch**, not after | Pre-launch |

## ESP Wiring

- Smartlead and Instantly both support exclusion/suppression lists. Upload the merged
  list at campaign creation **and** before every send batch that adds new contacts.
- Verify the header names in the current UI — feature names move. (Checked 2026-09-09.)
- The ESP copy of the list is a projection of the canonical file. The canonical file is
  the source of truth; when they disagree, the canonical file wins and the ESP gets
  re-uploaded.

## List-Build Check

Dedupe new scrapes against the suppression list **before verification** — never pay to
verify a known-suppressed contact. This check belongs to the list skill's build order;
the list skill references this file, this file does not describe the scrape.

## Not-Now Re-Eligibility

When a `re_eligible_date` arrives, the contact does not silently re-enter a cold
sequence. It leaves suppression only by explicit review, and it re-enters as a **warm
trigger** — the revisit date itself is the opener ("when we spoke in March you said Q4").

This closes the loop the reply skill opens when it logs a revisit date. A logged date
that never resurfaces is a list that decays silently.

## Verification Checklist

Run before the first send of any new campaign:

- [ ] Canonical list row count matches the sum of ESP exclusion lists
- [ ] No suppressed email address appears in the campaign list (automated diff, not spot check)
- [ ] Opt-out webhook / reply monitoring confirmed pointing at the append path
- [ ] Test unsubscribe processed within SLA on a seed address
