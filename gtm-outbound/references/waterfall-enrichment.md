# Waterfall Enrichment — Provider Routing & Verification

Load when designing the enrichment pipeline in `gtm-outbound-list`.

Provider pricing, coverage, and match rates move quarterly. The **routing logic** below
is durable; the specific provider rankings are a starting default. Update
`PROVIDER_REGISTRY` in `scripts/clay_taxonomy.py` to match your contracted rates.

## Why Waterfall At All

Any single email provider finds 40-70% of a B2B list. Running three in sequence reaches
80-90%. The catch is that running three in *parallel* costs three times as much for the
same result, since you pay every provider for every row including the ones the first
already solved.

A waterfall runs them in sequence, each gated on the previous returning empty:

```
Row → LeadMagic ──found?──► done
         │ empty
         ▼
      Findymail ──found?──► done
         │ empty
         ▼
       Prospeo ──found?──► done
         │ empty
         ▼
      unresolved → drop or route to a manual queue
```

## The Two Rules

### 1. Cheap and broad first

Order by cost per successful match, not by headline price per credit. A provider at half
the price with a third of the coverage is more expensive per usable row.

### 2. Every step after the first must be gated

An ungated waterfall is just parallel enrichment with extra latency. This is the single
most expensive mistake in Clay builds, and it is invisible until the invoice arrives —
the table works correctly, it just costs 3x what it should.

`clay_taxonomy.py` treats an ungated later step as an error, not a warning.

## Default Provider Tiers

Relative cost per match, tier 1 cheapest. Verify against your own rates.

| Provider | Tier | Strength |
|---|---|---|
| LeadMagic | 1 | Broad B2B coverage, low cost per hit |
| Findymail | 1 | Strong verified work emails, low bounce |
| Prospeo | 2 | Good LinkedIn-sourced coverage |
| Kaspr | 2 | GDPR-clean EU coverage |
| Datagma | 2 | Useful EU coverage |
| Dropcontact | 2 | GDPR-clean, EU-focused |
| Hunter | 3 | Pattern-based; always verify output separately |
| Apollo | 3 | Wide but staler data |
| BetterContact | 3 | Waterfall-of-waterfalls; simplest setup, highest per-hit cost |
| Clearbit | — | DEPRECATED — acquired by HubSpot, folded into the Breeze stack; no standalone waterfall use (checked 2026-09-09) |

**On pattern-based providers.** Tools that guess `first.last@domain.com` from a known
pattern produce plausible addresses that were never confirmed to exist. They inflate
apparent match rate and then inflate bounce rate. Place them last, and never let their
output skip verification.

**On waterfall-of-waterfalls services.** BetterContact and similar run their own internal
waterfall. Convenient, and reasonable as a final catch-all step — but placing one first
defeats the entire cost structure, since you pay their aggregate rate on every row.

**On Clearbit.** Marked DEPRECATED and kept in the table only as a marker. Acquired by
HubSpot and folded into the Breeze stack, it no longer operates as a standalone waterfall
provider. GDPR-clean EU alternatives for its old role: Dropcontact, Kaspr; Datagma also
covers EU.

**Provider status (checked 2026-09-09).** LeadMagic, Findymail, and Prospeo are verified
alive and actively marketing waterfall integrations. Kaspr and Dropcontact are the EU
GDPR-clean additions. Ocean.io and 6sense were **not verified in this pass** — mark them
unverified and re-check before relying on either.

## Sequencing the Full Pipeline

Order matters for cost as much as correctness. Cheap filters go before expensive lookups.

| # | Stage | Why here |
|---|---|---|
| 1 | Dedupe | Never pay twice for the same row |
| 2 | Domain resolution | Everything downstream keys off a clean root domain |
| 3 | Firmographic enrichment | Cheap, and enables the next step |
| 4 | **Filter on firmographics + ICP classifier** | Drop non-ICP rows *before* paying for contacts |
| 5 | Contact discovery | Find the people |
| 6 | Email waterfall | Gated, cheap to expensive |
| 7 | Verification | Gate on valid |
| 8 | Research / personalization | Most expensive per row — runs last, on verified rows only |

**Step 4 is where budgets are saved.** Filtering out non-ICP companies before contact
discovery and research typically removes 20-40% of rows at near-zero cost. Skipping it
means paying premium research rates on rows you will never send to.

**Step 8 last, always.** Claygent research is usually the most expensive column in the
table. Running it on rows with no deliverable address is pure waste.

## Domain Resolution

Do this before anything else, and do it properly.

Scraped URLs arrive as `https://www.example.com/about?utm_source=clutch`. Normalize to
`example.com`. Strip protocol, `www`, path, query, and trailing slash. Resolve redirects
— acquired companies frequently redirect to a parent domain, and enriching the old one
returns nothing.

Watch for: parked domains, agency portfolio subdomains, regional TLD variants of the same
company, and shared platform domains (`myshopify.com` subdomains are not company domains).

## Verification

Route every discovered address through verification. Non-negotiable.

| Status | Action |
|---|---|
| Valid | Send |
| Catch-all / accept-all | Separate low-volume campaign on a separate domain, or drop |
| Unknown | Drop |
| Invalid | Drop |
| Disposable / role-based | Drop (`info@`, `sales@`, `support@`) |

**The 4% line.** Bounce rate above roughly 4% triggers throttling at major mailbox
providers, and reputation damage extends to every domain in the sending pool — not just
the campaign that caused it. Verification is cheap; a burned domain and a 14-day rewarm
is not.

**Catch-all domains** accept everything and bounce nothing, so they look valid and tell
you nothing. Some are real, some are black holes. They are not free: sending to dead
addresses on a catch-all still damages engagement signals. Isolate them.

**Role-based addresses** rarely reach a decision-maker and disproportionately trigger spam
complaints. Drop them even when they verify clean.

## Phone Enrichment as a Waterfall Output

The cold-call track needs phone numbers; the pipeline above historically produced emails
only. Phone enrichment slots in **after email verification** — as a **parallel branch,
not a serial step**:

```
verified row ──► research / personalization
      └──────► phone enrichment (gated on the same verified-row gate)
```

A row whose email bounced should not spend phone credits; a verified row can be enriched
for phone at the same time it moves to research.

Rules:

- Gate phone spend on the verified-row gate, same as research columns.
- Coverage varies hard by market. GCC phone coverage is as hard as email — see
  gcc-market.md before assuming a hit rate.
- No phone provider is tier-certified here; the provider landscape moves quarterly
  (checked 2026-09-09). Certify against your own contracted rates.
- DNC scrubbing and lawful basis for calling are compliance questions, not data
  questions — route through compliance-gates.md.

## Two Kinds of Research Column

LLM research columns do two different jobs, and conflating them is why people rate them as
unreliable.

| Type | Job | Output shape |
|---|---|---|
| **Classification** | Is this row in the ICP? | One of a fixed set of values |
| **Extraction** | Pull a specific fact for personalization | A short factual string, or empty |

Classification belongs at **step 4 of the pipeline** — the filter before you pay for
contact discovery. Extraction belongs at **step 8**, after verification. Running them at
the same stage wastes money on both ends.

### Classification: Do Not Trust Platform-Native Flags

Data platforms ship their own "is B2B", "is SaaS", "industry" fields. Their classification
logic is frequently poor, and it is poor in a way that is invisible until your campaign is
already targeting the wrong companies.

This is the same principle as never trusting a provider's own "valid email" flag: the
platform's incentive is coverage, yours is accuracy.

An LLM agent reading the company's actual website outperforms these flags substantially,
because it evaluates the same evidence a human would.

**The classification prompt pattern:**

1. **Name the primary source explicitly** — the company's own site: homepage, product,
   pricing, about, FAQs, docs, login page.
2. **Name the signals that decide it.** For SaaS: a pricing page, recurring pricing, public
   API documentation, a login. For B2B: who the pricing and case studies address.
3. **Permit corroboration from named third parties** — LinkedIn company page, Crunchbase,
   G2, Capterra, press coverage. Presence on G2 or Capterra is itself a strong SaaS signal.
4. **Constrain output to enumerated values**, never prose:
   `true` / `false` / `unclear` / `not_found`
5. **Keep the reasoning.** Store why it decided, so misclassifications are auditable rather
   than mysterious.

Point 4 does most of the work. A classifier that can answer in prose will, and prose cannot
be filtered on.

**Save classifiers as reusable agents.** ICP qualification repeats across every campaign —
build the classifier once, save it as a template, and call it by name in each new table
rather than rewriting the prompt. Cheaper, and more importantly consistent: two hand-written
versions of the same classifier will disagree at the margins.

**On model choice:** running the classifier against your own API key is typically cheaper
than the platform's bundled inference. Worth checking at volume, since classification runs
across the entire raw list.

## Extraction Columns

Claygent and similar LLM research columns are powerful and are the easiest place to
generate expensive nonsense.

**Prompt requirements:**

- Constrain the output shape: *"Return only the client name and the metric, under 12
  words. Return empty if not stated on the page."*
- Point at a specific location — their case studies page, not "the web."
- **Always permit an empty return.** A prompt with no exit produces confident
  fabrication, and that fabrication ships to a prospect who knows their own numbers.
- Ask for one fact per column. Multi-fact columns cannot be validated or merged cleanly.

**Validate the output before it reaches copy.** Check for: empty rate (over ~40% means
the prompt or source is wrong), suspiciously uniform answers (the model is pattern-filling
rather than reading), and length outliers (prose where a phrase was requested).

Spot-check 20 rows by hand before running the full table. Every time.

## Clay's Dual-Credit Model

As of the platform's mid-2026 revision, Clay prices across two axes: **Data Credits**
(enrichment lookups) and **Actions** (Claygent runs and per-check signals such as
job-change detection). A job-change signal check, for example, prices as 1 action plus
~0.2 data credits. Source: https://leadmagic.io/guides/complete-guide-to-clay (checked
Jun 2026; pricing detail moves — re-verify before quoting).

The legacy "credits per column" framing undercounts modern tables that mix both axes.
The cost-audit habit in clay-credits.md is unchanged; what changes is the estimation step:
classify every column into **both** axes before computing cost per verified row, because
one column can consume an action and a fractional data credit on the same row.

## Cost Modeling

Model the pipeline cost per *verified sendable row*, not per credit. A rough shape:

```
cost per sendable row =
    (domain resolution + firmographics)          / post-filter survival
  + (contact discovery)                          / contact match rate
  + (weighted waterfall cost)                    / email match rate
  + (verification)                               / verification pass rate
  + (research columns, on verified rows only)
```

When pricing the `research columns` term, classify each column across both credit axes —
see Clay's Dual-Credit Model above.

Feed the result into `gtm_math.py economics --cost-per-lead` so infrastructure and data
costs land in the same CAC model rather than being tracked separately and forgotten.

## Clay Platform Drift

Clay now ships a native Sequencer (sending) and Signals (job-change monitoring) — the
platform is becoming a sending layer, not just an enrichment one (checked 2026-09-09).

This skill family still produces ESP-agnostic configs (Smartlead / Instantly). That
remains the right abstraction: copy, sending, and deliverability stay portable across
ESPs, and the enrichment layer stays swappable. Native Sequencer is a reasonable
alternative for teams fully committed to Clay — accept the lock-in knowingly.
