# Eval run sheet — 12 evals, 28 assertions

Run these in a **fresh session**. A session that already has the skill in
context routes differently, which is exactly what these are testing.

## 0 · A-route-math-natural
`activation` — should trigger

> how many inboxes do I need if I want 15 meetings a month

- [ ] **routes-to-math** — Routes to gtm-outbound-math, not the orchestrator or copy
- [ ] **runs-script** — Invokes gtm_math.py size rather than computing in prose
- [ ] **states-assumptions** — Explicitly flags the reply/positive/meeting rates it assumed

**Result:** pass / fail — 

## 1 · A-route-list-natural
`activation` — should trigger

> engineer a Clay outbound workflow for Shopify brands doing 1-10M

- [ ] **routes-to-list** — Routes to gtm-outbound-list
- [ ] **picks-storeleads** — Selects Storeleads or BuiltWith for the Shopify segment
- [ ] **gated-waterfall** — Waterfall steps after the first are gated on the previous returning empty
- [ ] **runs-clay-script** — Generates clay-table.json via clay_taxonomy.py rather than hand-writing JSON

**Result:** pass / fail — 

## 2 · A-route-offer-implicit
`activation` — should trigger

> my reply rate is 2% and I'm not sure my targeting is right

- [ ] **diagnoses-upstream** — Treats this as an ICP/offer problem rather than jumping to copy edits
- [ ] **checks-deliverability-first** — Considers that a sub-1% or collapsed reply rate can be a placement problem, not a copy problem

**Result:** pass / fail — 

## 3 · A-route-copy-direct
`activation` — should trigger

> draft a Poke the Bear sequence for agency owners

- [ ] **routes-to-copy** — Routes to gtm-outbound-copy
- [ ] **observation-bridge-question** — Email 1 follows observation then bridge then open question
- [ ] **no-pitch-in-email-1** — Email 1 contains no pitch, calendar link, or meeting ask
- [ ] **under-80-words** — Email 1 is under 80 words in its longest spintax variant
- [ ] **validator-run** — validate_spintax.py is actually run and its output shown

**Result:** pass / fail — 

## 4 · A-route-full-chain
`activation` — should trigger

> build me a full outbound campaign for a B2B data consultancy targeting mid-market ecommerce

- [ ] **runs-three-stages** — Executes offer then list then copy in order
- [ ] **artifacts-chained** — Later stages read the artifacts earlier stages wrote
- [ ] **emits-brief** — Produces campaign-brief.md

**Result:** pass / fail — 

## 5 · B-collision-blog-repurpose
`collision` — must NOT trigger

> turn this blog post into a LinkedIn post

- [ ] **does-not-trigger** — gtm-outbound does NOT activate; blog-repurpose is the correct target

**Result:** pass / fail — 

## 6 · B-collision-blog-write-topic
`collision` — must NOT trigger

> write a blog post about cold email deliverability best practices

- [ ] **does-not-trigger** — gtm-outbound does NOT activate; this is blog-write with an outbound topic
- [ ] **topic-vs-task** — Correctly distinguishes writing ABOUT outbound from DOING outbound

**Result:** pass / fail — 

## 7 · B-collision-seo-linkedin
`collision` — must NOT trigger

> audit my site and tell me how to rank for cold email software

- [ ] **does-not-trigger** — gtm-outbound does NOT activate; seo-audit is correct

**Result:** pass / fail — 

## 8 · B-collision-linkedin-organic
`collision` — must NOT trigger

> write me a LinkedIn post about our new product launch

- [ ] **does-not-trigger** — gtm-outbound does NOT activate; organic social is not outbound sequencing

**Result:** pass / fail — 

## 23 · A-route-gcc
`activation` — should trigger

> Building an outbound campaign for Saudi ecommerce brands doing 1-10M SAR

- [ ] **loads-gcc** — Loads gcc-market.md before sizing or sourcing
- [ ] **zid-salla** — Names Zid and Salla rather than defaulting to Shopify
- [ ] **data-coverage** — Flags that MENA contact-data coverage is a fraction of Western levels
- [ ] **working-week** — Notes the Sunday-Thursday working week or Ramadan/Eid timing

**Result:** pass / fail — 

## 26 · B-collision-pricing-strategy
`collision` — must NOT trigger

> help me decide between usage-based and seat-based pricing

- [ ] **does-not-trigger** — gtm-outbound does NOT activate; pricing strategy is out of scope

**Result:** pass / fail — 

## 27 · B-collision-board-deck
`collision` — must NOT trigger

> I need to prepare my board deck for next quarter

- [ ] **does-not-trigger** — gtm-outbound does NOT activate

**Result:** pass / fail — 

