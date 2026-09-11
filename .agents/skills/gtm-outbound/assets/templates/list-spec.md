# List & Enrichment Spec — [Campaign]

Generated: [date] · Stage 2 of 3 · Next: `/gtm-outbound copy`
Source ICP: [inherited from icp.json / reconstructed inline]

## Sourcing Channels

| # | Source | Why this one | Extraction method | Expected rows |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |

**Trigger source:** [which channel carries the timestamped trigger]

## Pipeline

Ordered. Cheap filters run before expensive lookups.

| # | Stage | Column(s) | Provider | Run condition |
|---|---|---|---|---|
| 1 | Dedupe | | — | always |
| 2 | Domain resolution | `company_domain` | | always |
| 3 | Firmographics | | | domain not empty |
| 4 | **ICP filter** | — | — | drop non-matching before paid stages |
| 5 | Contact discovery | | | |
| 6 | Email waterfall | | | gated, see below |
| 7 | Verification | `email_status` | MillionVerifier | email not empty |
| 8 | Research | | Claygent | verified email not empty |

## Email Waterfall

| Order | Provider | Tier | Runs when |
|---|---|---|---|
| 1 | | | always |
| 2 | | | step 1 empty |
| 3 | | | step 2 empty |

Unresolved rows: [drop / manual queue]

## Research Column Prompts

### `[variable_name]`
- **Look at:** [specific location, not "the web"]
- **Return:** [exact output shape and length limit]
- **Empty when:** [the explicit exit condition]

## Verification Criteria

| Status | Action |
|---|---|
| Valid | Send |
| Catch-all | [separate campaign / drop] |
| Unknown / Invalid | Drop |
| Role-based | Drop |

**Bounce rate target:** under 2% (2-3% investigate; above 3% pulls the domain from rotation; 4% throttles)

## Expected Funnel

| Stage | Rows | Survival |
|---|---|---|
| Raw scrape | | — |
| Deduplicated | | |
| Domain resolved | | |
| Contacts found | | |
| Emails found | | |
| **Verified sendable** | | |

## Sender Field Mapping

| Clay column | Smartlead field |
|---|---|
| `verified_email` | `email` |
| | |

Any column without a mapping is invisible to the copy stage.

## Cost Model

| Component | Unit cost | Volume | Total |
|---|---|---|---|
| | | | |

**Cost per verified sendable row:** [figure] → feeds `gtm_math.py economics --cost-per-lead`

## Validation

```
[paste clay_taxonomy.py validate output]
```

## Handoff

`clay-table.json` and `allowed_vars.json` written. The copy stage validates every merge
tag against them.
