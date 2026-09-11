# Clay Credit Economics — Free vs Paid Columns

Load when building or auditing a Clay table, or when a table costs more than expected.

Waterfall gating (`waterfall-enrichment.md`) is the well-known cost lever. This file
covers the second one, which is less known and often larger: **most transform work in a
Clay table is free, and people pay for it anyway.**

---

## The three cost classes

| Class | Cost | What it covers |
|---|---|---|
| `free` | Zero credits, to create **and** to run | AI formulas, native tool functions, filters, conditional-run gates, lookups within the workspace |
| `credit` | Clay credits per row | Native sources, enrichment integrations, provider lookups |
| `ai` | Credits scaling with model and prompt length | AI columns, Claygent web research |

**Default every column to `free` and justify each exception.** If a column only rearranges
data already in the table, it should almost never cost anything.

---

## What is genuinely free

### AI formulas

Zero credits to create, zero to run. They generate code from a plain-language instruction
and then execute deterministically. Use for:

- Extraction — pull the city out of "Plano, TX"; pull the username after the last slash
- Counting — how many roles, how many past employers
- Concatenation — string together every company someone has worked at
- Case and punctuation — lowercase a generated phrase so it reads mid-sentence
- Conditional logic — checkbox columns for filtering
- **Run conditions** — the gate expressions on every paid column

If the generated code is wrong, adjust the instruction, read the code and correct it, or
simply regenerate — the model often produces a different approach on a second pass.

### Native tool functions

Clay ships prebuilt functions that also cost nothing, grouped by category: **normalization,
extraction, counting, scoring, ordering, mapping, grouping**, and formulas.

Reach for these before writing a formula. The clearest case is **company-name
normalization**: turning a legal name like "Clay Labs Inc" into "Clay". Hand-building this
as an AI formula means accumulating edge cases forever — Inc, LLC, Ltd, GmbH, Holdings,
Agency, Group. The native function already handles them.

Worth explicitly browsing the tool section before building anything custom. A meaningful
share of bespoke AI columns in real tables duplicate a native function.

---

## What actually needs to be paid

Reserve `ai` class columns for work that requires **judgment or information not in the
table**:

- Web research for a data point no provider carries (Claygent)
- Classification requiring semantic understanding — B2B vs B2C from a description,
  seniority bucketing from a messy job title
- Copy generation
- Summarization of long unstructured text into something usable

Seniority bucketing is the canonical legitimate case: no data provider returns the
definition of seniority you actually want, so you derive it from job titles with AI.

---

## Conditional runs — gate everything paid

Any column can carry a run condition. Build it free through the formula box:

> only run if `{column}` is blank

### The coverage pattern

This is the highest-value application, and it generalizes well beyond email waterfalls:

```
cheap broad method  ──► fills most rows
        │
        │ rows still empty
        ▼
expensive precise method  ──► fills the remainder
```

Applied to LinkedIn URL discovery: run the waterfall, then Claygent gated on the rows
that came back empty. Applied to any enrichment: run the integration, then Claygent on the
misses. Coverage climbs toward complete while cost stays proportional to the gaps rather
than to the table.

### Gating rules

1. **Every waterfall step after the first** is gated on the previous returning empty.
   Enforced as an error by `clay_taxonomy.py`.
2. **Every research column** is gated on a corner piece existing, and — for email
   campaigns — on a deliverable address existing. Researching a row you cannot contact is
   pure waste.
3. **Every column downstream of a resolution step** is gated on that resolution
   succeeding. A domain that never resolved will otherwise burn a full waterfall
   returning nothing.

---

## Claygent model selection

Claygent cost scales with the model. The ladder:

1. **Start on the cheapest model, always.** Run it on a handful of rows first.
2. Escalate to a mid-tier model only on measured failure.
3. Escalate to a frontier model only after that.
4. **Re-check the prompt before every escalation.** A weak prompt fails on every model and
   simply costs more on the expensive ones. Most escalations are prompt problems.

Iterate on a few rows, refine, *then* scale. Never debug a prompt at full table width.

Preset templates exist for common research tasks and are worth checking before writing a
prompt from scratch.

---

## Auditing an expensive table

Work this order:

1. **Ungated waterfall steps** — every provider charging for every row. Largest and most
   common.
2. **Ungated research columns** — the most expensive per-row column running on rows that
   were never contactable.
3. **Paid columns doing free work** — AI columns extracting, counting, formatting,
   concatenating, or normalizing. Reclassify to formulas or native functions.
4. **Enrichment duplicating enrichment** — a custom research column retrieving something
   `enrich company` or `enrich person` already returned. Check the existing enrichment
   output before adding any research column.
5. **Unfiltered volume** — the cheapest fix of all. Filter on free firmographic data
   *before* the paid stages, never after. Preview counts at every filter step and stop
   when the number is sane rather than importing and trimming later.

---

## Reporting cost in a spec

State three things:

- How many columns are `free` versus `credit` versus `ai`
- Which single column is most expensive per row
- What each paid column is gated on

That third line is what makes the spec auditable. A paid column with `run_condition:
always` should be visible at a glance.

## Bring your own API keys

Clay's own credits are priced above buying the same capability direct. Anything you already
hold an account with — Apollo, OpenAI, LeadMagic, Findymail — should be connected under
**Settings → Connections** and billed to that account, not consumed as Clay credits.

The free tier cannot do this. It ships ~100 credits and blocks external connections and
sequencer integrations, which makes it a demo rather than a starting point: you cannot
build the cheap version of a table on it.

**Enrichment providers only charge on a hit.** A waterfall step that returns nothing costs
nothing, which is what makes deep waterfalls affordable — the cost is bounded by matches,
not attempts. This is the opposite of the AI columns, which charge per row regardless.

**Check the per-request price before adding a data source, not after.** Funding data is the
usual trap: a Crunchbase-style lookup can run ~8 credits per row, so a 2,000-row table
spends 16,000 credits on one column. A Claygent web-search column answering the same
question — *did this company raise recently, and how much* — costs a fraction of that and
is usually good enough for a trigger you are going to hedge in the copy anyway.

Ordering rule: **free formula → cheap provider → Claygent → premium data source.** Most
tables never need the fourth tier.
