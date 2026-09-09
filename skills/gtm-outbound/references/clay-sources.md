# Clay-Native Sources

Load when choosing how to get rows into a Clay table.

`sourcing-channels.md` covers **where a list comes from strategically** — scrapers,
directories, trigger sources. This file covers **what Clay can source natively**, which
is often cheaper and always fewer moving parts than routing through an external scraper.

Check here before specifying a third-party scraper. If Clay sources it natively, that is
one less tool, one less API key, and one less failure point in the pipeline.

---

## LinkedIn company import — the free tier

Five filters are free to import against:

- Industry (LinkedIn's own taxonomy, several hundred entries; multi-select, and you can
  exclude industries as well)
- Company size, in LinkedIn's employee bands
- Company type (private, public, and so on)
- Keyword in the company description
- Location — country, state, province, or city

If the ICP is expressible in those five, the base list costs nothing. Enrichment on top
costs credits; the import itself does not.

### Exceeding the 50,000 row cap

One import maxes out at 50,000 rows. To take a larger TAM completely:

1. Import the first 50,000 with your filters.
2. Create a second table with the **same** filters, and add an exclusion pointing at the
   first table.
3. Repeat until the result set is exhausted.

Each pass excludes everything already captured, so the passes do not overlap.

**Preview before importing.** The count appears before you commit — use it to tune filters
rather than importing broadly and trimming afterwards. Every filter tightened before
import is volume you never pay to enrich.

---

## Company lookalikes

Give it a seed set, get similar companies back. Two properties worth knowing:

- Returns a **list per row**, so it needs Write to Table to become usable rows. See
  `clay-tables.md`.
- Produces heavy duplication across seeds. Deduplicate on domain — Clay's dedup will
  report the count it caught. Also consider a lookup against your original list so
  lookalikes that were already in the seed set drop out.

**The strategically interesting use** is not "find more companies." It is: segment your
existing *successful customers* into categories, then find lookalikes per category. You
already know you serve that shape well, and the copy can reference the named customer
that the prospect resembles.

---

## Job signals

Two distinct mechanisms, and picking the wrong one is the usual mistake:

| | Jobs as a **source** | Jobs as an **enrichment** |
|---|---|---|
| Produces | One row per job opening | A job count and list against an existing company row |
| Use when | The opening *is* the entity — recruiting, job seeking | You want hiring as a qualifying signal on companies you already have |

Waterfalls across multiple job data sources, same gating rules as any other waterfall.

**Enumerate title permutations.** Semantic matching is not something to assume — list
"BDR", "SDR", "Business Development Representative", and "Sales Development
Representative" as separate keywords rather than relying on one to catch the rest.

**Filter in stages and watch the count.** A broad job search returns numbers in the tens
of thousands. Add geography, then employment type, then cap the result — checking the
preview count at each step — rather than importing everything and filtering after.

---

## Google Maps

Local and physical businesses, by search term plus location and radius. Returns name,
address, website, phone, star rating, and review count.

Strong for categories that have no meaningful database coverage — trades, retail,
restaurants, clinics, brokerages. The rating and review count are unusually good
personalization material precisely because they are public, verifiable, and rarely used.

Pairs naturally with an owner-discovery step: search the business name plus a role word to
find the individual, then enrich.

---

## Other native sources

| Source | Returns | Notes |
|---|---|---|
| Twitter/X | Followers, followings, thread engagers | Works against any public account, including a competitor's |
| Google search | Search-result rows | The general-purpose escape hatch — see below |
| Yelp | Local businesses and their reviews | Ad results are a decent proxy for still-trading |
| G2 | Ratings, categories, review counts | Sparse outside software |
| BuiltWith | Technology stack | Pair a keyword filter **with** a category, or "WordPress" matches the CMS, the plugins, and the widgets identically. The pairing is also the only way to get first- and last-detected dates, which tell you whether adoption is recent |
| CRM import | Existing contacts | HubSpot, Salesforce, and others, natively |
| CSV | Anything | |

---

## Google search as a source

The escape hatch when no database covers the segment. Build and test the query in Google
itself, then move the finished query into Clay.

Useful operators: `site:` to restrict to a domain, `filetype:` for hosted documents,
quoted phrases for exact matches, `-term` to exclude, and date restrictions for recency.

Two techniques worth knowing:

**Verify the results.** Search results are noisy. Scrape each result and run a free
keyword check against the body text, then filter on the match count being non-empty. This
turns a rough query into a list you can trust.

**Spin the query for volume.** Repeating an identical search returns identical results.
Add a varying term you do not actually care about — a city, a state — to surface a
different result set on each pass, then combine.

---

## Choosing between them

Ask what makes the segment **observable**, then pick the source that observes it:

| The segment is defined by | Source |
|---|---|
| Firmographics alone | LinkedIn free import |
| Physical location | Google Maps |
| Resemblance to known customers | Company lookalikes |
| Hiring activity | Job signals |
| Software they run | BuiltWith |
| Engagement with a topic or competitor | Twitter/X |
| Something published but not indexed anywhere | Google search + verification |

Name at least two sources for any real list. A single-source list inherits that source's
blind spots and you will not know what is missing.

## Ranking the sources by what they are actually best at

No single source wins everywhere. Pick per job:

| Job | Best first | Notes |
|---|---|---|
| **Lookalikes** | Ocean.io, then Clay's own | Apollo and Sales Navigator are usable but weaker for this |
| **Job-posting signals** | Clay | Its job search reads posting *content*, not just titles. Apollo and Sales Navigator are both poor here — this is one of the clearest reasons to run the search inside Clay |
| **E-commerce merchants** | Store Leads | Covers Shopify and WooCommerce, and **Zid and Salla** — which is what makes it non-optional for Saudi (see `gcc-market.md`). Apollo's e-commerce coverage is not competitive |
| **Startups and funding** | Harmonic | Deeper on startup segmentation than Apollo, at a higher credit price |
| **Tech install** | BuiltWith, SimilarWeb | Also surfaces spend signals |
| **Local business** | Google Maps | See above |
| **Competitors of a company** | Owler | Cheap way to expand from one account to its peer set |

**Job-posting searches need a recruitment exclusion.** Searching job *descriptions* for a
technology or function returns staffing and recruitment agencies alongside the companies
actually hiring, because agencies post the same text. Exclude recruitment, staffing and
HR-outsourcing companies in the same filter — otherwise a meaningful slice of the list is
agencies who will never buy.

**A job posting is a two-sided signal.** It can mean a direct need ("hiring a B2B sales
manager" at a historically B2C company), or it can be an indirect read on their stack
("hiring a Shopify developer" means they run Shopify). Both are usable; be clear which one
you are claiming in the copy, because they support different hypotheses.
