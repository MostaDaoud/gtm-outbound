---
name: gtm-outbound-list
description: >
  Designs the technical pipeline that turns an ICP into a clean, enriched, verified
  outbound list without burning platform credits. Selects sourcing channels by TAM and
  ICP shape (Clutch, Storeleads, PhantomBuster, BuiltWith, job boards, G2), specs domain
  resolution and Claygent web research for hyper-personalization variables, designs
  waterfall email enrichment routing across LeadMagic, Findymail, Prospeo and others,
  and defines MillionVerifier validation to hold bounce rate under 2% (3% pulls the
  domain from rotation). Emits
  LIST-SPEC.md and a validated clay-table.json. Use when the user says "engineer a Clay
  outbound workflow", "how do I build this list", "design the enrichment waterfall",
  "waterfall enrichment", "scrape leads", "which email finder should I use", "lead
  sourcing", "find emails", or "verify my list". For building the Clay table itself —
  columns, credits, prompts — see gtm-outbound-clay.
argument-hint: "[path to icp.json or a target audience description]"

---
<!-- fable-discipline-gate:v1 -->

## Pre-flight gate: Fable Discipline (run FIRST)

Before executing any instruction below, adopt the Fable Mindset operating manual at
`C:\Users\mosta\.claude\skills\fable-mindset\SKILL.md`. Apply its Decision Loop
(GROUND -> REASON -> ACT -> OBSERVE -> RE-EVALUATE -> VERIFY -> NARRATE) and its
7 execution rules to every step of this skill. FD runs first; this skill's own
instructions begin only after the discipline is adopted.
# GTM Outbound — Technical List & Sourcing Spec

The data layer. This stage decides what the copy can say, because copy can only
reference variables this pipeline actually produces.

## Inputs

Read `icp.json` from the working directory if it exists — sub-niche, filters,
`personalization_vars`, and `estimated_tam` all come from it. If absent, collect the
sub-niche and the target variables inline and note in the output that the ICP was
reconstructed rather than inherited.

## Step 0 — Check Geography First

**Run the jurisdiction gate before sourcing anything** — `references/compliance-gates.md`:
geography → consent model → required artifacts. Saudi Arabia in particular now requires
consent for marketing email under the PDPL (enforced since September 2024); a scraped KSA
list without a documented basis is a legal exposure, not a list.

If the list includes Saudi Arabia, the UAE, Egypt, or the Gulf, also load
`references/gcc-market.md` before choosing anything. Contact-data coverage there is a
fraction of Western levels — a single-source list is not viable, the raw scrape must be
sized well above the defaults, and Saudi ecommerce runs on Zid and Salla rather than
Shopify, which neither Apollo nor Sales Navigator covers well.

## Step 1 — Select Sourcing Channels

Load `references/sourcing-channels.md` from the parent skill.

Pick channels by what makes the sub-niche *observable*, not by what is convenient:

| If the sub-niche is defined by | Source from |
|---|---|
| Service category and client roster | Clutch, agency directories |
| Ecommerce platform and revenue band | Storeleads, BuiltWith |
| Engagement with a topic or competitor | PhantomBuster on post commenters, event attendees |
| Hiring a specific role (trigger) | Job boards, LinkedIn Jobs |
| Software they already run | BuiltWith, Wappalyzer, G2 reviews |
| Recent funding | Crunchbase, funding newsletters |

**Prefer trigger-based sources over static directories.** A static directory gives you a
company that matches; a trigger source gives you a company that matches *and* has a
reason to care this month. That difference shows up in reply rate more than any copy
change. `references/signals-and-triggers.md` maps each signal to where it is observable.

**Before defaulting to Apollo or LinkedIn, ask where these people publish contact details
because they want inbound.** Directories, marketplaces, listing sites, association
registers, speaker rosters. Where a role's business model depends on being reachable, the
data is richer, cleaner, and largely un-emailed — while Apollo rows are being worked by
everyone else in your category.

**Set the re-scrape cadence from the trigger's decay window,** not from convenience. A
two-week trigger needs a weekly refresh; building that list once and sending from it for
a quarter is the most common structural failure in trigger-based campaigns.

Name at least two sources. Single-source lists inherit that source's blind spots, and
you will not know what you are missing.

## Step 2 — Resolve and Enrich the Company

1. **Domain resolution first.** Every downstream lookup keys off a clean root domain.
   Scraped URLs carry tracking parameters, subdomains, and redirects — normalize before
   enriching or you pay for lookups against garbage.
2. **Firmographics** — headcount, industry, location. Use these to filter *before* the
   expensive stages, not after.
3. **Research columns via Claygent** — one column per `personalization_var` from the
   ICP. Write the prompt to return a short factual string or an empty value, never
   prose. A research column that returns a paragraph cannot be dropped into an email.

**Claygent prompt requirements**, since this is where cost and quality both concentrate:

- Constrain the output shape explicitly: "Return only the metric and client name, under
  12 words. Return empty if not found on the site."
- Give it a specific place to look, not the whole web.
- Always allow an empty return. A prompt that cannot fail returns confident fabrication,
  which then ships to a prospect who knows it is wrong.

## Step 3 — Design the Waterfall

Load `references/waterfall-enrichment.md` from the parent skill.

The rule is cheap-and-broad first, expensive-and-accurate last, with every step after
the first gated on the previous returning empty. Ungated waterfalls charge every
provider for every row — the most common way outbound budgets disappear.

Generate the schema rather than hand-writing it:

```bash
python scripts/clay_taxonomy.py generate --waterfall leadmagic,findymail,prospeo --sources clutch,storeleads --personalize case_study_result,recent_launch -o clay-table.json
```

The script validates ordering, gating, and credit classification on write. Fix what it
reports before moving on.

**For table construction depth, hand off to `gtm-outbound-clay`.** This stage decides
*which providers and sources* the table uses. That one decides *how the table is built* —
column ordering by corner-piece dependency, classifying each column free vs paid so
zero-credit formulas do the work paid AI columns are usually wasted on, SPICE-structured
prompts, and cross-table mechanics when one row has to become many.

## Step 4 — Verification

Route every found address through MillionVerifier and gate sending on `valid` only.

- Bounce ladder: target **under 2%** (the 2026 median for verified lists is ~1.5%).
  Above 2% is elevated — investigate before scaling. Above 3% is danger — pull the
  domain from rotation. At 4% mailbox providers throttle and deliverability degrades for
  every campaign sharing the domain.
- Discard `catch-all` and `unknown` for cold sending, or route them to a separate,
  lower-volume campaign on a separate domain. They are not free — they are a shared
  reputation cost.
- Expect roughly 30% attrition from raw scrape to verified. Size the scrape accordingly;
  `gtm_math.py size` accounts for this via `--verify-pass-rate`.

## Step 5 — Map to the Sender

Every variable the copy will use needs an explicit `smartlead_field` mapping. A column
that exists in Clay but is not exported renders blank in the email — the data is there,
the send is still broken, and nothing in either tool flags it.

Worked example of a mapping row (the shape every column needs):

```json
{"column": "case_study_result", "smartlead_field": "case_study",
 "used_in": "email_1.observation", "empty_fallback": "omit sentence"}
```

Three things per mapping: the Clay column name, the Smartlead custom field it feeds, and
where in the sequence it is used. Check the sending platform's custom-field limit before
designing the column set — Smartlead historically allows a bounded number of custom
fields per campaign (verify the current figure in its UI; it moves), and a spec that
needs twelve fields on a platform that renders six is a blank render waiting to happen.

**If the campaign includes a phone track**, phone numbers are a waterfall output too —
a parallel branch gated on verified rows, not a free by-product. See the phone-enrichment
section in `references/waterfall-enrichment.md`, and run the result past
`references/compliance-gates.md` before dialing (DNC obligations are jurisdiction-specific).

**Dedupe against the suppression list before verification.** Never pay to verify a
known-suppressed contact — the procedure and the artifact live in
`references/suppression-mechanics.md`.

Emit the allowed-variable file the copy stage validates against:

```bash
python scripts/clay_taxonomy.py vars clay-table.json > allowed_vars.json
```

## Outputs

- `LIST-SPEC.md` from `assets/templates/list-spec.md` — channels, extraction method per
  source, column-by-column pipeline, credit logic, verification criteria.
- `clay-table.json` — validated schema.
- `allowed_vars.json` — merge variables available to the copy stage.

Report the expected funnel explicitly: raw scraped → domain resolved → contacts found →
emails found → verified. Each stage loses rows, and a spec that does not state the
attrition will undershoot the list by the time it reaches sending.

## Next

Hand off to `gtm-outbound-copy`. It will validate every merge tag against
`allowed_vars.json`, so any variable not produced here cannot silently reach a send.
