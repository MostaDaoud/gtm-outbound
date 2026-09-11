# ICP Filter Taxonomy — Sales Navigator & Apollo

Load when building filter sets in `gtm-outbound-offer`.

## The Governing Principle

**Filter on what is observed, not on what is inferred.** Platforms expose both, and they
look identical in the UI. Observed fields come from something the company published;
inferred fields come from a model. Inferred fields corrupt segments quietly, because the
rows still look plausible.

| Observed (trust) | Inferred (avoid) |
|---|---|
| Headcount on the company page | Estimated revenue |
| Job postings | "Company growth" scores |
| Tech detected on the site | Predicted intent |
| Funding announcements | Inferred department budget |
| Named title strings | Seniority-only buckets |

## Company-Level Filters

| Filter | Use | Notes |
|---|---|---|
| Headcount | Always | Use narrow bands. "11-50" spans a solo-founder shop and a real org. |
| Geography | Always | Filter to where you can actually serve and legally send. |
| Industry / SIC | With care | Self-reported and often stale. Pair with a second signal. |
| Tech stack | High value | Strongest observable proxy for how they operate. |
| Funding stage / recency | High value when it is the trigger | Decays fast; keep the window under 6 months. |
| Job postings | Highest value | A live posting is a budgeted, timestamped problem. |
| Company type | Always | Excludes staffing, nonprofits, government where irrelevant. |

**Headcount banding.** Pick a band where the buying process is the same across the range.
15-60 staff is one band because the founder still decides. 15-500 is not a band, because
somewhere in there procurement appears and the entire sale changes.

## Contact-Level Filters

| Filter | Use | Notes |
|---|---|---|
| Exact title strings | Always | The single highest-precision filter available. |
| Seniority | Only alongside titles | Never alone. |
| Department | Supporting | Broad and inconsistently populated. |
| Tenure in role | High value | Under 6 months = mandate to change; over 5 years = ownership of the status quo. |
| Years of experience | Rarely | Weak signal, poorly populated. |

**Title strings beat seniority.** "VP" returns VP of Facilities. `"VP Demand Generation"
OR "VP Growth" OR "Head of Demand Gen"` returns the person who owns the problem. Write
6-12 exact strings, including the informal variants people actually use.

**Tenure as a trigger.** Someone 0-6 months into a role has a mandate and no loyalty to
the incumbent vendor. This is one of the most reliable, least-used filters in outbound.

## Exclusion Keywords

The most underbuilt part of most specs, and the cheapest to fix.

**Title exclusions** — assistant, intern, coordinator, recruiter, student, retired,
"seeking", "open to work", freelance, consultant (when targeting operators), founder
(when targeting functional owners at scale).

**Company exclusions** — staffing and recruiting firms, agencies (when targeting brands),
brands (when targeting agencies), competitors, your existing customers, your existing
pipeline, education, government, nonprofit — unless any of these *is* the segment.

**Self-exclusions people forget** — current customers, open opportunities, anyone who has
opted out or replied negatively in the past 12 months. Emailing a live opportunity with a
cold sequence is a reliable way to lose it.

Build exclusions as a reusable list per ICP, not per campaign. It compounds.

## Three Hard Rules

### 1. Never "all CEOs"

Seniority without title strings returns every founder of every two-person shop in the
geography. The list looks large and converts at nothing. If the buyer genuinely is the
CEO, constrain hard on company shape instead — headcount band, industry, trigger event.

### 2. Never filter on estimated revenue

It is modeled from headcount and industry, so it adds no information beyond filters you
already have, while introducing model error. Where revenue genuinely matters, use an
observable proxy: funding raised, headcount in revenue roles, store count, review volume,
number of locations.

### 3. Sanity-check the result count

| Result count | Reading |
|---|---|
| Under 500 | Too tight to test. You cannot learn from a list this size. |
| 500 - 5,000 | Ideal for a first campaign. Personalization stays feasible. |
| 5,000 - 25,000 | Workable with strong automation. |
| Over 50,000 | Too loose. The message cannot be specific enough to land. |

If the count is far outside these bands, the sub-niche is wrong — not the filters.
Return to sub-niche selection rather than adding arbitrary constraints to hit a number.

## Boolean Construction

Sales Navigator title search supports boolean. Structure it as:

```
("VP Demand Generation" OR "VP Growth" OR "Head of Demand Generation" OR "Director of Demand Gen")
NOT (Assistant OR Intern OR Coordinator OR Recruiter)
```

Quote multi-word titles. Unquoted terms match on any word and will return everyone whose
title contains "Growth."

## Recording the Spec

Record filters as structured data in `icp.json`, not prose. The list stage consumes it,
and prose filters get reinterpreted differently every time someone rebuilds the list:

```json
{
  "company_filters": {
    "headcount": "15-60",
    "geo": ["United States", "Canada"],
    "tech": ["Shopify Plus"],
    "trigger": "posted a paid media role in the last 60 days"
  },
  "contact_filters": {
    "titles": ["Head of Growth", "VP Marketing", "Director of Ecommerce"],
    "tenure_months_max": 24
  },
  "exclusions": {
    "titles": ["Assistant", "Intern", "Recruiter"],
    "company_types": ["Staffing", "Agency"],
    "lists": ["existing_customers", "open_opportunities", "prior_optouts"]
  }
}
```
