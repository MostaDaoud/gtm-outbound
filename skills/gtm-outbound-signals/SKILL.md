---
name: gtm-outbound-signals
description: >
  Turns one buying signal into one copy-ready sentence. Nineteen playbooks covering
  person signals (new in role, competitor post engagement, recent social posts, warm
  intros), company signals (fundraising, hiring surge, job-posting language, ad library),
  website signals (public pricing, case-study pages, named tech on site, keyword presence),
  list shaping (company and first-name cleaning, social link resolution, lookalikes,
  name-to-other-prospects) and copy generation (AI specificity, creative ideas). Each
  playbook gives the source chain, the output contract, the locked prompt, the Clay table
  build and the edge cases. Use when the user says "personalization at scale", "what do
  I say in email one", "new in role", "they just raised", "hiring signal", "pricing page
  signal", "found their case study", "what tech do they use", "lookalike list", "clean my
  company names", "clean first names", "is this you or them", "creative ideas per
  company", or "make this offer feel written for them".
argument-hint: "[signal name, or a list of the signals the campaign can support]"
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
# GTM Outbound — Signal Playbooks

A signal is only worth using if it produces a sentence a human would actually write. Every
playbook here obeys the same contract: **one signal, one line, as a pipeline variable** —
never a paragraph of research dumped into an email.

Start at `references/signals/index.md` for the index and the two build harnesses.

## The rule that makes this work

A personalization variable must be **produced by the list pipeline**, not invented by the
copy stage. If the campaign cannot source the signal for a given row, the line falls back
to a defined default rather than hallucinating a fact. That is the whole reason signals
live at the data layer: `gtm-outbound-list` builds the field, this skill defines what the
field means, and `gtm-outbound-copy` may only reference fields that exist.

Hallucinated personalization is worse than none. "I saw you just raised your Series B" to
a company that did not is a permanent credibility loss, and it is the single most common
failure mode in AI-assisted outbound.

## Signals by category

### Person signals

| Signal | Reference | The line it produces |
|---|---|---|
| New in role | `references/signals/new-in-role.md` | "you stepped into the COO seat at Northwind in April" |
| Competitor post engagement | `references/signals/linkedin-engagement.md` | who liked or commented on a source account's posts |
| Recent social posts | `references/signals/social-posts.md` | a hook drawn from their own most recent post |
| Warm intros | `references/signals/warm-intros.md` | "we're both one hop from X" |

### Company signals

| Signal | Reference | The line it produces |
|---|---|---|
| Fundraising | `references/signals/fundraising.md` | "you closed a Series A in March" |
| Hiring surge | `references/signals/hiring-surge.md` | "you've added six people to RevOps since Q1" |
| Job-posting language | `references/signals/job-posting-language.md` | a clause from a live role, filtered by language |
| Ad library | `references/signals/ad-library.md` | what they are currently running on Meta |

### Website signals

| Signal | Reference | The line it produces |
|---|---|---|
| Public pricing | `references/signals/pricing-page.md` | plan tiers, price points, feature boundaries |
| Case-study page | `references/signals/case-study-page.md` | one named customer off their own page |
| Tech on website | `references/signals/tech-on-website.md` | named technologies verified on the live site |
| Google site search | `references/signals/google-site-search.md` | whether their site mentions a specific keyword |

### List shaping

| Signal | Reference | The line it produces |
|---|---|---|
| Company-name cleaning | `references/signals/company-name-cleaning.md` | the short human form a person would say |
| First-name cleaning | `references/signals/first-name-cleaning.md` | the name a person is actually greeted by |
| Social link finding | `references/signals/social-link-finding.md` | verified official profile URLs |
| Lookalikes | `references/signals/lookalikes.md` | companies that would read a case study as themselves |
| Name to other prospects | `references/signals/name-to-other-prospects.md` | "is this you or them?" without naming wrong people |

### Copy generation

| Signal | Reference | The line it produces |
|---|---|---|
| AI specificity | `references/signals/ai-specificity.md` | the one sentence that makes a generic offer specific |
| Creative ideas | `references/signals/creative-ideas.md` | three per-company bullets for a defined slot |

## Each playbook ships three ways

Per signal, expect up to three files:

| File | What it is | Use it when |
|---|---|---|
| `signals/<name>.md` | the playbook: source chain, output contract, locked prompt, edge cases | always — this is the definition |
| `signals/<name>.clay-table.md` | the Clay **table** build: columns, formulas, credit gates | building in the Clay browser app |
| `signals/<name>.clay-workflow.md` | the Clay **workflow** build via the `clay` CLI | driving Clay from a terminal |

The split is a real constraint, not a preference: the `clay` CLI is read-only for tables
but can create, edit and publish workflows. Tables are browser-driven; workflows are
CLI-driven.

**Treat the Clay build files as specifications until proven.** They are written against
the real action catalog, but build one, run five rows, read the output, and fix the file
before trusting it across a list.

## Choosing a signal

Signal choice is a function of the offer, not of what is easy to scrape. Ask in order:

1. **Does the signal actually predict buying?** New-in-role predicts a stack rebuild.
   A website running React predicts nothing anyone will pay for.
2. **Can it be sourced at rate?** A signal available on 4% of the TAM is a small campaign
   with a coverage problem, not a personalization strategy.
3. **Does the resulting line survive being read out loud?** If it sounds like a press
   release, it is not a hook.

Two strong signals beat six weak ones. A campaign that uses one signal honestly and
consistently outperforms one that stacks five shallow variables into a word salad.

## Depth and fan-out

- How deep to personalize, and when depth stops paying -> `references/personalization-depth.md`
- Running per-lead personalization across parallel sub-agents, with an approval loop ->
  `references/personalization-subagent.md`

## Handing off

- The fields do not exist in the pipeline yet -> `gtm-outbound-list`
- Building the Clay table that produces them -> `gtm-outbound-clay`
- Writing the sequence around the line -> `gtm-outbound-copy`
- The copy is written and needs a launch gate -> `gtm-outbound-score`
