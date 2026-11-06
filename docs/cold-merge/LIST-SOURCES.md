# Bundled list sources (not shipped in this repo)

coldoutboundskills ships roughly **525 MB** of pre-built lead CSVs. They are genuinely
useful and genuinely too heavy to vendor into a skill repository that installs in seconds
via `npx skills add`. They are therefore **excluded** here and documented instead.

Get them from upstream:
https://github.com/growthenginenowoslawski/coldoutboundskills/tree/main/Common%20Outbound%20Lists

## What is there

| List | Rows | Size | Notes |
|---|---|---|---|
| Google Maps Scrape — 12M US Businesses | ~12.3M | ~426 MB | Split across 13 zip parts. Grep `category_titles` first; the full pull is large and most of it will not match any ICP. |
| Shopify Stores — 259K Active | 259,293 | 24 MB | Stores with ≈$1k+ estimated monthly visits. Columns: `domain`, `merchant_name`, `description`, `company_linkedin` (≈65% fill). |
| US Software / SaaS companies (cleaned) | ~173K | 74 MB | Cleaned company list, domain-first. |
| US zip codes | 42,734 | 3 MB | Zip / city / state / lat-lng / population. Used by the Google Maps lane. |

## How to use them with this skill set

These are **companies, not people**. They are candidate supply, not a sendable list.

1. Treat them as `extra_candidates` input to the list stage — see
   `skills/gtm-outbound/references/list-lanes.md` and `list-expansion.md`.
2. Qualify against the ICP **before** pulling contacts:
   `skills/gtm-outbound/references/list-ai-qualification.md`.
3. Score the result before upload: `skills/gtm-outbound/references/list-qa.md`.
4. Then hand the qualified company set to `gtm-outbound-list` for the proper pipeline,
   and `gtm-outbound-clay` to build the enrichment table.

## Why not just commit them

- A 426 MB folder is beyond what a skill repo should carry; clones and installs become
  slow enough that people stop installing.
- The data ages. Committing a scrape freezes a snapshot that silently rots in the repo,
  whereas a pointer to upstream inherits upstream's refresh cadence.
- The repository's promise is a sub-1 MB, zero-dependency install that runs offline. Bulk
  data is a different product with a different lifecycle.

If you want a local copy, download upstream and keep it outside version control, e.g.
`~/outbound-lists/`, and point the list stage at that path.
