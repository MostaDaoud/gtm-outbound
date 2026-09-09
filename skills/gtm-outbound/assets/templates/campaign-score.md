# Campaign Readiness Score — [Campaign]

Date: [date]

---

## Verdict

> **[LAUNCH / LAUNCH AFTER FIXES / HOLD]** — **[earned] / [available]**

Report as `earned / available`, not as a percentage. A campaign scoring 71/75 with no
sequence written is not 95% ready; it is incomplete.

**Not assessed:** [categories with no artifact, and why]

---

## Hard Gates

These fail the campaign at any total score. Check these before reading the table.

| Gate | Status |
|---|---|
| `validate_spintax.py` exits clean | |
| `score_message.py` returns no error-severity findings | |
| `clay_taxonomy.py validate` exits clean | |
| Verification stage present in the pipeline | |
| Sending domain is not the primary company domain | |
| One-click unsubscribe headers configured | |
| Opt-out mechanism present and honoured within 2 days | |

**Any unchecked box means HOLD**, and the fix list below leads with it.

---

## Categories

| Category | Score | Max |
|---|---|---|
| ICP & offer specificity | | 25 |
| List & data quality | | 25 |
| Copy quality | | 25 |
| Infrastructure | | 15 |
| Compliance & risk | | 10 |
| **Total** | | **100** |

### ICP & Offer Specificity — /25
| Criterion | Pts | Earned | Note |
|---|---|---|---|
| Sub-niche is vertical × trigger × company shape | 5 | | |
| Trigger has a timestamp and decay window | 5 | | |
| Value Equation scored, weakest lever addressed | 5 | | |
| UVP names measurable outcome + mechanism | 5 | | |
| Exclusion list covers titles, company types, suppressions | 5 | | |

### List & Data Quality — /25
| Criterion | Pts | Earned | Note |
|---|---|---|---|
| Two+ sourcing channels, one carrying the trigger | 5 | | |
| Domain resolution before any paid enrichment | 5 | | |
| ICP filter before contact discovery and research | 5 | | |
| Waterfall ordered cheap→expensive, every later step gated | 5 | | |
| Verification gating on valid only | 5 | | |

### Copy Quality — /25
Score with the scripts, not by reading.
| Criterion | Pts | Earned | Note |
|---|---|---|---|
| Email 1 under 80 words, longest variant | 5 | | |
| Opens on a specific observation, not industry or compliment | 5 | | |
| No pitch, calendar link, or meeting ask in email 1 | 5 | | |
| Spintax clean, every merge tag has a producing column | 5 | | |
| Follow-ups each add a new angle and stand alone | 5 | | |

### Infrastructure — /15
| Criterion | Pts | Earned | Note |
|---|---|---|---|
| Sending domains separate from primary | 5 | | |
| SPF, DKIM, DMARC on every sending domain | 5 | | |
| Warmup set, first-send date respects it, domain load under 40/day | 5 | | |

### Compliance & Risk — /10
| Criterion | Pts | Earned | Note |
|---|---|---|---|
| Physical address and working opt-out | 4 | | |
| Suppression shared across all campaigns and domains | 3 | | |
| Jurisdiction identified and its requirements flagged | 3 | | |

---

## Fix List

Ranked by **points recoverable per unit of effort**, cheapest first. Five points from
exclusion keywords takes ten minutes; five from re-scoping the sub-niche takes a day and
invalidates the list.

| # | Category | Pts | Change | Effort |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |

---

## Bands

| Score | Verdict |
|---|---|
| 90-100 | Launch |
| 75-89 | Launch after the listed fixes |
| 60-74 | Hold — a category is structurally weak |
| Under 60 | Hold — rebuild the weakest category |

Score what is there, not what was intended. Generous scoring produces a campaign that
fails after the money is spent, which is a more expensive way to learn the same thing.
