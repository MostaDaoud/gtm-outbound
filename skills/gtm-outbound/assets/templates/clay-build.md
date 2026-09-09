# Clay Build — [Campaign]

Date: [date] · Source ICP: [icp.json / reconstructed inline]

---

## Column Order

Ordered by cost class, cheapest first. A row that fails the ICP filter must never reach a
metered or expensive column.

| # | Column | Stage | Class | Provider | Runs when |
|---|---|---|---|---|---|
| 1 | dedupe | source | free | — | always |
| 2 | `signal_detected_at` | source | free | — | always |
| 3 | `signal_age_days` | source | free | — | always |
| 4 | `company_domain` | resolve | cheap | | always |
| 5 | firmographics | enrich | cheap | | domain not empty |
| 6 | **ICP classifier** | filter | expensive | | passes firmographic filter |
| — | **── FILTER ──** | | | | drop non-ICP rows |
| 7 | contact discovery | people | metered | | in ICP |
| 8 | email waterfall step 1 | email | metered | | always (of survivors) |
| 9 | email waterfall step 2 | email | metered | | step 1 empty |
| 10 | verification | verify | metered | | email not empty |
| — | **── GATE on valid ──** | | | | |
| 11 | research columns | personalize | expensive | claygent | verified email present |
| 12 | export mapping | export | free | — | — |

**Why the classifier sits at step 6:** it is an expensive column running before the
filter, deliberately — because it *is* the filter. One expensive call removes rows that
would otherwise hit three metered columns and a second expensive one.

---

## Prompts

### `[column_name]` — [classification / extraction]

**Source named:** [their site: homepage, pricing, docs — not "the web"]
**Deciding signals:** [what counts as yes]
**Corroboration allowed:** [named third parties, or none]
**Output contract:** [enumerated values, or short string + length limit]
**Empty return permitted:** [the exact exit condition]

```
[exact prompt as entered in Clay]
```

**Reasoning column kept:** [yes/no] — makes misclassification auditable

---

## Saved Agents Used

| Agent | Reused from | Why saved |
|---|---|---|
| | | Consistency — two hand-written versions disagree at the margins |

---

## Spot-Check — 20 Rows

Run before the full table. Every new prompt, every time.

| Check | Result | Verdict |
|---|---|---|
| Empty rate | [n]% | [under 40% ok] |
| Uniform answers | | [pattern-filling?] |
| Length outliers | | [constraint binding?] |
| Confident but wrong | | [checked against known companies] |

**Rows read by hand:** [n] · **Prompt revised after check:** [yes/no]

---

## Export Mapping

| Clay column | Sender field |
|---|---|
| `verified_email` | `email` |
| | |

**Unmapped columns:** [list] — these exist in Clay but are invisible to the copy stage.

---

## Cost

| Component | Unit | Volume | Total |
|---|---|---|---|
| | | | |

**Cost per verified sendable row:** [figure] → feeds `gtm_math.py economics --cost-per-lead`

---

## Validation

```
[paste clay_taxonomy.py validate output]
```

```bash
python scripts/clay_taxonomy.py vars clay-table.json > allowed_vars.json
```

**`allowed_vars.json` written:** [yes/no] — the copy stage validates every merge tag
against it.
