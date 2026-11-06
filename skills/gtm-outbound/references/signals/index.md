<!--
  Adapted from coldoutboundskills: playbooks\clay-playbooks
  Source: https://github.com/growthenginenowoslawski/coldoutboundskills
  Author: GrowthEngineX. License: MIT. See NOTICE at the repo root.
  Adapted to gtm-outbound reference format; upstream frontmatter removed.
-->

# Clay Playbooks

Nineteen playbooks. Each one answers a single question:

> A campaign needs signal X on every row. What is the cheapest reliable way to get X, and what exact prompt turns X into copy-ready text?

One playbook produces one field. `new_in_role_line`. `funding_line`. `pricing_page_line`. That
field slots into one sentence of email 1. That is the whole product.

## The three run modes

Every playbook directory ships the same three files. They are three delivery mechanisms for the
same recipe, not three different recipes.

| File | What it is | Use it when |
|---|---|---|
| `SKILL.md` | The playbook itself: source chain, output contract, locked prompt, edge cases | You are running the signal from Claude, ad hoc, on a CSV or a one-off list |
| `clay-table.md` | The Clay **table** build: exact columns, types, formulas, credit gates, AI-column bindings | The signal needs to run continuously on a client table that other people will look at |
| `clay-workflow.md` | The Clay **workflow** build via the `clay` CLI: node graph, real action keys, publish and run | You want the signal version-controlled and buildable from a terminal, no UI clicking |

**Why tables are browser-driven and workflows are CLI-driven.** This is a real constraint, not a
style choice. The `clay` CLI's `tables` command group is read-only (`list`, `get`, `columns`,
`rows`, `query`) — it cannot create a table or add a column. Tables must be built in the UI.
Workflows are the opposite: `clay workflows create` / `nodes create` / `publish` / `runs test`
all exist, so a workflow can be built end to end from a terminal.

Shared procedures, written once so the 19 playbooks do not repeat them:

- **`clay-table-harness.md`** — the generic browser procedure for building any playbook's table.
- **`clay-cli-harness.md`** — the generic `clay` CLI procedure for building any playbook's workflow.

Read the relevant harness once, then read the playbook's own `clay-table.md` / `clay-workflow.md`
for what is specific to that signal.

## Status: recipes, not verified builds

⚠️ **Read this before you tell anyone a playbook "works".**

The `SKILL.md` in each directory carries a verification line saying what was actually run and on
how many rows. Where it says PASS, real rows were graded.

**The `clay-table.md` and `clay-workflow.md` files in every playbook are documented recipes that
have not been built and run in a live Clay workspace.** They are written against the real Clay
action catalog and the real CLI command surface, so the shapes are right, but nobody has clicked
through the table build or published the workflow. Treat them as specifications. Build one, run it
on 5 rows, read the output, and fix the file before you run it on a list.

The one thing most likely to be wrong on first build is the AI column's reasoning-effort
parameter. See `clay-table-harness.md` § "The empty-column trap".

## The 19 playbooks

### Person-level signals (the person did something)

| Playbook | Output field | What it says |
|---|---|---|
| [`signals/new-in-role.md`](../signals/new-in-role.md/) | `new_in_role_line` | they just took this seat |
| [`signals/linkedin-engagement.md`](../signals/linkedin-engagement.md/) | `engagement_line` | they engaged with a relevant post |
| [`signals/social-posts.md`](../signals/social-posts.md/) | `social_post_line` | they posted about something you can speak to |
| [`signals/warm-intros.md`](../signals/warm-intros.md/) | `warm_intro_line` | you share a real connection |

### Company-level signals (the company did something)

| Playbook | Output field | What it says |
|---|---|---|
| [`signals/fundraising.md`](../signals/fundraising.md/) | `funding_line` | they raised, so they are buying |
| [`signals/hiring-surge.md`](../signals/hiring-surge.md/) | `hiring_line` | they are growing the team you sell to |
| [`signals/job-posting-language.md`](../signals/job-posting-language.md/) | `job_language_line` | their own job post names your problem |
| [`signals/ad-library.md`](../signals/ad-library.md/) | `ad_line` | they are spending on ads right now |

### Website-derived signals (their site says something)

| Playbook | Output field | What it says |
|---|---|---|
| [`signals/pricing-page.md`](../signals/pricing-page.md/) | `pricing_page_line` | how they price, read off their own page |
| [`signals/case-study-page.md`](../signals/case-study-page.md/) | `case_study_line` | who they brag about serving |
| [`signals/tech-on-website.md`](../signals/tech-on-website.md/) | `tech_line` | what they run, detected on the page |
| [`signals/google-site-search.md`](../signals/google-site-search.md/) | varies | find any page on their site by keyword |

### List-shaping playbooks (they make other playbooks work)

| Playbook | Output field | What it says |
|---|---|---|
| [`signals/company-name-cleaning.md`](../signals/company-name-cleaning.md/) | `company_name_clean` | "Irby Utilities, LLC" becomes "Irby" |
| [`signals/first-name-cleaning.md`](../signals/first-name-cleaning.md/) | `first_name_clean` | "MARIA-JOSE (MJ)" becomes "MJ" |
| [`signals/social-link-finding.md`](../signals/social-link-finding.md/) | `linkedin_url` etc. | find the profile you are missing |
| [`signals/lookalikes.md`](../signals/lookalikes.md/) | company list | more companies like these |
| [`signals/name-to-other-prospects.md`](../signals/name-to-other-prospects.md/) | contact list | more buyers at the same company |

### Copy-generation playbooks (they turn signals into words)

| Playbook | Output field | What it says |
|---|---|---|
| [`signals/ai-specificity.md`](../signals/ai-specificity.md/) | `specificity_line` | make a generic line concrete |
| [`signals/creative-ideas.md`](../signals/creative-ideas.md/) | campaign angles | what campaign to run at all |

## Cost tags

Every source row in every playbook carries one of these. They are relative to a 1,000-row list.

| Tag | Means |
|---|---|
| **FREE** | no per-row cost, or included in a flat plan |
| **CHEAP** | under $1 per 1,000 rows |
| **METERED** | $1 to $20 per 1,000 rows, scales with volume |
| **EXPENSIVE** | over $20 per 1,000 rows, or per-row LinkedIn reads |

## Rules that apply to all 19

1. **One playbook, one field.** If you need two signals, run two playbooks and let the copy pick.
2. **Abstain is empty string.** Never "N/A", never "unknown", never a guess. A blank is cheap; a
   confident wrong sentence about someone's own job costs you the account.
3. **The model never establishes a fact.** Every fact goes into the prompt already proven by a
   structured source. The model's only job is to turn a fact list into one sentence. If you find
   yourself asking a model "is this true?", you have skipped a source.
4. **Deterministic fields are computed in code, not by the model.** Dates, counts, enums, and
   anything that branches the copy. Models are for prose.
5. **Gate the paid column.** No paid enrichment runs on a row that failed a free upstream check or
   that has no valid email. This is the single biggest cost lever in Clay.
6. **Run 5 rows and read them before you run 5,000.** Every playbook has a smoke test. The failure
   modes are silent: empty columns, unbound variables, and gates that drop every row look
   identical to "still processing".
7. **No em dashes in generated copy.** They read as machine-written. Hyphens in number ranges are
   fine.

## What you need

Playbooks name credentials by environment variable, never by value. Copy `.env.example` to `.env`
and fill in only what the playbooks you actually run require. The common ones:

| Variable | Used by |
|---|---|
| `PROSPEO_API_KEY` | new-in-role, name-to-other-prospects, social-link-finding |
| `OPENAI_API_KEY` | every playbook with a locked prompt |
| `SERPER_API_KEY` (or another SERP provider) | google-site-search, case-study-page, pricing-page |
| `APIFY_API_TOKEN` | ad-library, linkedin-engagement, social-posts |
| `CLAY_API_KEY` | the `clay` CLI, if you are not using browser OAuth |

Never paste a key into a SKILL.md, a Clay column, or a workflow node body. Clay columns read
credentials from the workspace's saved integration auth; the CLI reads them from your shell.

