# Eval 23 — Outbound campaign for Saudi ecommerce brands, 1-10M SAR

Target list includes Saudi Arabia, so `references/gcc-market.md` is loaded before any
sizing or sourcing decision — several Western defaults in this skill are wrong here and
fail silently.

Also on routing: "Saudi ecommerce brands doing 1-10M SAR" names an audience slice, not a
completed ICP blueprint. Treating it as a starting point and running the full chain
(offer → list → copy) rather than jumping straight to list-building, since revenue band
alone doesn't tell us the sub-niche, the trigger, or the offer fit yet. Below is the
list-stage view since that's where the GCC-specific facts bite hardest; happy to run
`offer` first properly if you want the Value Equation pass.

## Platform reality — do not default to Shopify

Western ecommerce sourcing assumes Shopify/WooCommerce. In Saudi, **Zid and Salla** hold
the larger share of the market at this revenue band. Neither is well covered by Apollo or
Sales Navigator — **Storeleads does carry them**, so the scraper spec routes through
Storeleads rather than a Shopify app-store scrape. Building this list on Western sourcing
assumptions returns a small, unrepresentative slice of the real 1-10M SAR segment.

## Data coverage is the binding constraint, not copy or targeting

Apollo/Sales Navigator coverage in Saudi is roughly:

| Layer | Approximate |
|---|---|
| LinkedIn users in market | ~10,000,000 |
| Profiles in Apollo | ~1,700,000 (under 20%) |
| Verified emails available | ~443,000 (~4% of the market) |

That means:
- Single-source list building is not viable — multi-source plus heavy waterfall
  enrichment is mandatory, not an optimization.
- Expect a materially lower verification pass rate than the 70% Western default in
  `gtm_math.py size` — size the raw scrape well above what the same TAM would need in the
  US or EU.
- Phone numbers are as hard to get as emails.
- Flag to you now, before the list build starts: a goal that's easily reachable against a
  comparable Western TAM may simply not be reachable here on data availability alone. That
  belongs in scoping, not discovered after the build fails.

## Calendar

Working week is **Sunday–Thursday**, not Monday–Friday — a Western send schedule wastes
two send days and lands two sends on the weekend. The **last 10 days of Ramadan and Eid**
flatten reply rates sharply (Eid effectively to zero); build the sending calendar around
both rather than a fixed weekly cadence.

## Other GCC-specific calls worth making now

- **Language is a property of the contact, not the country.** IT/software roles at these
  brands often skew English-speaking (expatriate staff); Saudized commercial/HR roles skew
  Arabic. Split the list by Sales Navigator's Profile Language filter rather than assuming
  Arabic across the board — Arabic copy to Arabic-speaking recipients can roughly double
  reply rate, so this split is worth the extra list step.
- **Sales cycle is longer** — plan for 3-5 months, not the Western default, when this
  feeds `gtm_math.py economics`.
- **WhatsApp is a legitimate channel here**, unlike in most Western markets — worth
  including in the multi-channel plan for this segment rather than treating it as
  off-limits.

Want me to run the `offer` stage next to narrow the sub-niche (e.g., which vertical within
ecommerce, what's driving 1-10M SAR as the band) before locking the Storeleads spec?
