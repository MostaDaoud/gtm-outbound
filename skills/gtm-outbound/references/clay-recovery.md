# Clay Recovery Patterns — When the Direct Route Fails

Load when a corner piece will not resolve, a page will not scrape, or an enrichment
returns empty across most of the table.

Jigsaw (`clay-frameworks.md`) says get the corner pieces first. This file is what to do
when you cannot get them the normal way.

The reflex when an enrichment comes back empty is to reach for a more expensive provider
or a bigger model. That is usually the wrong move — it pays more for the same failure. The
patterns below recover the data by changing the *route*, not the spend.

---

## The escalation ladder

Work down. Each rung costs more than the one above it.

| Rung | Try |
|---|---|
| 1 | A different field you already have — the answer is often already in an enrichment output you did not expand |
| 2 | A different keying strategy — resolve a *different* corner piece and come at it sideways |
| 3 | Someone else's compiled data (Pattern 1) |
| 4 | Infer the entity, then re-search for it (Pattern 2) |
| 5 | Accept partial coverage and gate everything downstream on it |

Rung 1 is skipped more than any other. `enrich person` alone returns over two dozen
fields, several of them nested arrays. Expand the existing output before adding a column.

---

## Pattern 1 — Someone already compiled this

**Use when:** the data point is tedious to gather per company but commercially useful, so
somebody has likely built a directory of it.

Store counts, location counts, franchise numbers, pricing tiers, headcount by site — these
get aggregated by data companies who sell or publish them. The aggregator's page structure
is *uniform by construction*, which is exactly what the original source was not.

**The method:**

1. Search the pattern manually for two or three companies. Note which aggregator keeps
   appearing.
2. Confirm the value sits in the same position on every one of their pages. This is the
   test that decides whether the pattern works.
3. Build a scrape recipe against the aggregator, with the company identifier as a
   **dynamic segment** in the URL rather than a hardcoded one.
4. Automate the lookup: search `{company} {aggregator}`, take the first result, scrape it.

**What you are trading:** their accuracy and their freshness become yours. Fine for
qualification and personalization; not fine for anything you assert as fact in a claim the
prospect will check.

**Check the terms.** Some aggregators prohibit automated collection. `sourcing-channels.md`
covers where that line sits.

---

## Pattern 2 — Infer the entity, then re-search

**Use when:** you have pages that identify a company but share no common structure, so
nothing can be templated.

Documentation sites, help centres, portfolio pages, conference listings — each one built
differently. Scraping yields text but no reliable field.

**The chain:**

```
unusable page
   └─► scrape whatever text exists (title, description, body)
         └─► AI: "which company does this belong to?"
               └─► search that company name
                     └─► resolve domain
                           └─► normal enrichment from here
```

The insight is that the messy page only has to produce **one reliable output** — the
company name. Once you have that, you are back on the paved road and every standard
enrichment applies.

**Constrain the inference step hard.** It returns a name or empty, never prose. And gate
everything downstream on it being non-empty, or you run a full waterfall against a
hallucinated company.

Accuracy here is good but not perfect. Spot-check it like any other AI column — twenty
rows, read by hand.

---

## Pattern 3 — Extract from an inconsistent return

**Use when:** a source returns the field you want, but in an unpredictable position.

Common shape: an enrichment returns four "contact" slots, and any given row might hold a
phone number, a Facebook URL, an Instagram handle, or a Twitter profile in any of them.
Mapping them positionally produces a column that is right perhaps a third of the time —
and silently wrong the rest.

**The fix is a free AI formula**, not a paid column:

> print the value from these columns that contains `instagram.com`

Then a second free formula to reduce it to the key you actually need — the segment after
the last slash, the root domain, the numeric id.

Two free columns turn an unusable source into a keyed one. Reaching for an AI column here
is the exact mistake `clay-credits.md` warns about.

---

## Pattern 4 — Verify a noisy result set

**Use when:** search-based sourcing returned rows that are *plausibly* right.

Search operators get you close; they do not get you clean. A query for a niche category
will return blog posts, directories, aggregators, and unrelated companies alongside real
matches.

**Two free passes fix it:**

1. Scrape each result, then run a keyword check against the body text for the terms that
   define the segment. Filter on the match count being non-empty.
2. Negative-filter the domains that recur as noise — the aggregators and job boards that
   turn up in every search of that shape.

This converts a rough query into a list you can spend enrichment credits on. Doing it in
the other order — enrich first, filter after — pays full price for rows you then discard.

---

## When to stop

Not every segment is reachable, and recognizing that early is worth more than a fifth
attempt.

Stop and rethink the segment when:

- Two rungs of the ladder have failed and coverage is still under ~40%. The definition is
  probably not observable in public data, and no provider will fix that.
- Recovery has grown to four or more chained columns per row. The cost and the compounding
  error rate now exceed the value of the segment.
- The data exists but only behind a login you agreed not to automate against.

The productive move at that point is back at the offer stage, not the table: find a
**proxy** the segment correlates with that *is* observable, and target that instead. A
worse filter you can actually populate beats a perfect one you cannot.
