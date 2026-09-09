---
name: gtm-outbound-clay
description: >
  Builds the Clay table itself — column order, credit class per column, run conditions,
  Claygent prompts, Clay-native sources, and cross-table moves. Covers the FETE, Jigsaw
  and SPICE frameworks, free versus paid column classification, conditional gating to
  control spend, Write to Table and Lookup for one-row-becomes-many, and the HTTP API for
  tools Clay does not integrate natively. Use when user says "build my Clay table", "Clay
  columns", "Claygent prompt", "Clay credits", "my Clay table is expensive", "Clay
  lookalikes", "write to table", "Clay HTTP API", "how do I structure this table", or is
  working inside Clay rather than planning the pipeline. For choosing sources and
  providers strategically first, see gtm-outbound-list.
argument-hint: "[path to clay-table.json or icp.json]"

---
<!-- fable-discipline-gate:v1 -->

## Pre-flight gate: Fable Discipline (run FIRST)

Before executing any instruction below, adopt the Fable Mindset operating manual at
`C:\Users\mosta\.claude\skills\fable-mindset\SKILL.md`. Apply its Decision Loop
(GROUND -> REASON -> ACT -> OBSERVE -> RE-EVALUATE -> VERIFY -> NARRATE) and its
7 execution rules to every step of this skill. FD runs first; this skill's own
instructions begin only after the discipline is adopted.
# GTM Outbound — Clay Table Construction

`gtm-outbound-list` decides *what* the pipeline does and which providers run.
This decides *how the table is actually built*.

## Inputs

`clay-table.json` if it exists — `clay_taxonomy.py generate` produces the schema and this
skill turns it into a working table. Otherwise `icp.json` for the personalization
variables, or the target description inline.

## References — Load By Task

Each covers a distinct failure mode. Load only what the task needs.

| Task in front of you | Load |
|---|---|
| Ordering columns, or writing any prompt that runs per row | `references/clay-frameworks.md` — FETE, Jigsaw, SPICE |
| Deciding what a column costs, or auditing an expensive table | `references/clay-credits.md`, plus the dual-credit model section in `references/waterfall-enrichment.md` — Clay now prices Data Credits and Actions separately |
| Getting rows in without a scraper | `references/clay-sources.md` |
| A corner piece will not resolve, or a page will not scrape | `references/clay-recovery.md` |
| One row becoming many, joining tables, HTTP API, export | `references/clay-tables.md` |
| Provider routing and waterfall order | `references/waterfall-enrichment.md` |
| Carrying trigger freshness into the table | `references/signals-and-triggers.md` |

## The Two Rules That Survive Every Table

Everything else is situational. These are not.

**1. Order by cost class, cheapest first.** A row that fails the ICP filter must never
reach a metered or expensive column. Filtering after enrichment produces identical output
at several times the cost, and nothing in Clay warns you. Detail in `clay-credits.md`.

**2. Gate everything paid.** Every waterfall step after the first runs only when the
previous returned empty; research columns run only on rows with a verified address. An
ungated table pays every provider for every row.

`clay_taxonomy.py validate` enforces both and fails the schema if either is violated.

## The ICP Classifier Exception

One expensive column deliberately runs *before* the filter — the ICP classifier, because
it **is** the filter. It removes rows that would otherwise hit three metered columns and a
second expensive one.

Shrink what it sees first: run the cheap firmographic filter ahead of it, so the
classifier reads a smaller table.

Do not trust a platform's native "is B2B" or "is SaaS" flag in its place. Their incentive
is coverage; yours is accuracy — the same reason you never trust a provider's own "valid
email" flag.

## Two Column Types, Two Output Contracts

| Type | Answers | Output must be |
|---|---|---|
| **Classification** | Is this row in the ICP? | One of a fixed set — `true` / `false` / `unclear` / `not_found` |
| **Extraction** | What fact personalizes this row? | A short factual string, or empty |

A classifier that *can* answer in prose will, and prose cannot be filtered on. An
extraction column returning a paragraph cannot be dropped into an email. The output
contract is the column's most important property — see SPICE in `clay-frameworks.md`.

**Always permit an empty return.** A prompt with no exit produces confident fabrication,
and that ships to a prospect who knows their own numbers.

## Carry the Signal Date

`clay_taxonomy.py` emits `signal_detected_at` and `signal_age_days` as source columns.
Keep them. Without the age column you cannot sort the send queue by freshness or suppress
stale rows, and a trigger list worked in arbitrary order throws away most of its advantage.

## Spot-Check Before Running Full

**Run 20 rows. Read every one by hand.** Every new prompt, every time.

| What you see | What it means |
|---|---|
| Empty rate above ~40% | The prompt or the source is wrong, not the data |
| Suspiciously uniform answers | Pattern-filling rather than reading |
| Length outliers | The output constraint is not binding |
| Confident but wrong | The expensive one. Check against companies you know. |

Twenty rows costs almost nothing. Five thousand rows of confident fabrication costs the
campaign, and you learn about it when a prospect writes back to correct you.

## Validate Before Handing Off

```bash
python scripts/clay_taxonomy.py validate clay-table.json
```

```bash
python scripts/clay_taxonomy.py vars clay-table.json > allowed_vars.json
```

The first catches ordering and gating errors. The second produces the merge-variable file
the copy stage checks against — **a column that exists in Clay but is not exported renders
blank in the email**, and neither tool catches that alone.

## Output

`CLAY-BUILD.md`, using `assets/templates/clay-build.md`: the ordered column list with cost class and run condition per column, the
exact prompts, spot-check results, and estimated cost per verified row. That cost
estimate is computed, not guessed — the formula is in `references/waterfall-enrichment.md`
(cost model section), and under Clay's dual-credit model each column carries both a Data
Credit cost and an Action cost. When a table is expensive, run the free-work audit and
the model-choice ladder in `references/clay-credits.md` before cutting columns — paid AI
columns doing free native functions are the most common finding, not provider price.

## Next

`gtm-outbound-copy` — it validates every merge tag against `allowed_vars.json`.
