# Signals and Triggers — The Organizing Principle

Load when selecting a trigger in `gtm-outbound-offer` or choosing sources in
`gtm-outbound-list`.

Signal-to-source mappings and the sourcing heuristic below are adapted from the
Signal and Trigger Based GTM material in the GTM course transcripts. Framework theirs,
wording and outbound integration ours.

## Why This Sits Above List Building

A trigger is not one filter among many. It is the **cornerstone that determines three
things at once**:

```
the trigger  ──►  who goes on the list
             ──►  what the campaign is about
             ──►  the first line of the email
```

Treating it as a filter attribute produces a list. Treating it as the organizing
principle produces a campaign, because the observation line writes itself from the
trigger rather than being invented afterwards.

If you cannot write the first line of the email from the trigger alone, the trigger is
not strong enough.

## Three Categories, Not One

Most outbound treats "signal" as one thing — public events at the target company. That is
the coldest of three categories, and the one every competitor is also watching.

| Category | What it is | Temperature |
|---|---|---|
| **First-party** | Activity on *your* properties — site visits, pricing-page views, docs reads, repeat returns | Warmest |
| **Engagement** | How they already interacted with *you* — content, events, past replies, community, lapsed trials | Warm |
| **Third-party** | Public change at their company — funding, hiring, tech installs, leadership moves | Coldest |

**First-party outranks everything below it.** Someone reading your pricing page has
self-selected in a way no funding announcement approximates. Visitor de-anonymisation
resolves anonymous traffic to companies, turning site activity into a workable list.

Caveats before building on it:
- Company-level resolution is reliable; person-level is patchier and varies by tool
- It scales with the traffic you already have — a multiplier on existing demand, not a
  substitute for it
- Person-level identification carries heavier privacy obligations in the EU and UK. Check
  the basis before enabling it, not after — see `deliverability.md`

**Engagement signals are the most underused, and they are free.** Webinar registrants who
did not attend, anyone who said "not now" last quarter, newsletter readers, lapsed trials.
These already sit in your own systems. A logged "not now" with a revisit date beats any
cold trigger — and `gtm-outbound-reply` is where those dates should have been captured.

**Rank by category before ranking within it.** A weak first-party signal usually beats a
strong third-party one.

## Signal → Source Map

Third-party signals — the category that needs external sourcing. First-party and
engagement signals come from your own analytics, CRM, and community.

| Signal | Where it is observable |
|---|---|
| **Funding round** (seed, A, B) | Crunchbase, PitchBook, Apollo, Clay, YC and accelerator lists, Forbes / Entrepreneur and similar outlets |
| **Actively hiring a role** | Clay, LinkedIn Jobs (scrape via Apify), job boards |
| **Leadership / job-title change** | Sales Navigator, Apollo, Clay |
| **Headcount growth** (company or department level) | Sales Navigator, LinkedIn, Clay |
| **Technology installed or in use** | BuiltWith, Storeleads, Apollo tech filters, Wappalyzer |
| **Using a competitor's tool** | Apollo and Sales Navigator technology filters, BuiltWith, Clay integrations |
| **Running paid ads** | LinkedIn / Meta / Google Ads libraries, scraped via Apify |
| **Engaged with a post** — commented, liked, shared | LinkedIn search plus PhantomBuster or Apify |

**Post engagement is the highest-intent signal on this list.** Someone who commented on a
post about the problem you solve has publicly self-identified as caring about it, this
month. Volume is low and it does not scale, which is exactly why it converts.

Rank the rest roughly by how recent and how specific the signal is. A funding round from
14 months ago is a firmographic attribute, not a trigger.

## Choosing a Trigger

Two questions, in order:

1. **What condition makes someone need this now?** Not who they are — what changed.
2. **Where is that condition published?** If nowhere, it is not usable, regardless of how
   good a predictor it would be.

Most weak campaigns fail at question 2 and substitute a demographic filter for a trigger.

## The Underused Heuristic: Find Where They Want To Be Found

The default instinct is LinkedIn and Apollo. For many segments that is the *worst*
available source, because everyone else is emailing the same rows.

A better question: **is there a place where these people publish their contact details
because they want inbound?** Directories, listing sites, marketplaces, association
registers, review platforms, speaker rosters. Where a role's business model depends on
being reachable, the data is richer, cleaner, and largely un-emailed — often with email,
phone, and profile all published together.

Worked example from the source material: for US real estate brokers and agents, LinkedIn
and Apollo were the obvious path and the wrong one. Property listing sites carried full
contact details for every agent in the target state, published deliberately, because
those agents want to be contacted about listings.

When the obvious source feels thin, spend ten minutes asking a model to enumerate
non-obvious public data sources for the specific role and geography before defaulting to
Apollo. Describe the segment precisely — a vague prompt returns the obvious answer you
already had.

## Count the Trigger Before You Write to It

**Check how many rows actually carry the signal before building copy around it.** The
failure is ordinary and expensive: a campaign is designed around a trigger — recent
funding, a specific hire, a technology install — the copy is written to it, and the
enrichment then populates it for 60 rows out of 2,000. What ships is a sequence whose
opening line is blank or generic for 97% of the list.

This is why the artifact chain runs list before copy. Concretely, before committing a
trigger:

1. Run the enrichment on a **sample of 100-200 rows**, not the whole table.
2. Read the fill rate. Under ~40% and the trigger cannot carry the campaign's opening line.
3. Either widen the trigger, segment the list so the trigger-carrying rows get their own
   sequence, or fall back to segment relevance and keep the trigger as a bonus line.

A trigger with a thin fill rate is not useless — it is a *segment*, and it should be run as
its own smaller, sharper campaign rather than as a variable in a big one.

## Signal Decay

Every trigger has a shelf life, and using one past it is worse than using none — it
signals that your data is stale.

| Signal | Useful window |
|---|---|
| Post engagement | Days to ~2 weeks |
| Job posting | While the posting is live, plus ~30 days |
| Leadership change | ~90 days |
| Funding | ~3-6 months |
| Technology install | ~3-6 months |
| Competitor tool in use | Ongoing, but not time-bound — treat as a filter, not a trigger |

Record the window in `icp.json` alongside the trigger. A trigger without a window becomes
a static filter within a quarter, and nobody notices until reply rates drift down.

## Speed Is Part of the Signal

The window says how long a trigger stays *valid*. It does not say how much value decays
while you sit inside it — and that decay is steep. Reaching someone within roughly 48
hours of a trigger is a different message from reaching them three weeks later, even
though both are technically in window.

Two structural consequences, neither of which is a copy decision:

**1. Carry signal age as a column.** `clay_taxonomy.py` emits `signal_detected_at` and
`signal_age_days`. Sort the send queue by age and work the freshest first. Without the
column you cannot prioritise, and a queue worked in whatever order the table happens to be
in throws the advantage away.

**2. Set re-scrape cadence from the window, not from convenience.**

| Window | Re-scrape |
|---|---|
| Days to ~2 weeks (post engagement) | Weekly or faster |
| ~30 days (job postings) | Weekly |
| ~90 days (leadership change) | Fortnightly |
| 3-6 months (funding, tech install) | Monthly |

Building a trigger list once and sending from it all quarter is the most common structural
failure in trigger-based outbound. By month three it is a static list wearing a trigger's
name, and the reply rate will say so.

**Suppress stale rows rather than sending to them.** An opener referencing a five-month-old
funding round advertises that your data is old, which is worse than not mentioning it.

## Wiring It Through

| Layer | What the trigger determines |
|---|---|
| `gtm-outbound-offer` | The sub-niche intersection and the exclusion set |
| `gtm-outbound-list` | Which source is authoritative, and the scrape cadence |
| `gtm-outbound-copy` | The observation line, directly |
| `gtm-outbound-diagnose` | Whether a decaying reply rate is really a decayed trigger |

**Re-scrape cadence follows the decay window.** A trigger with a two-week window needs a
weekly refresh, not a one-off list build. This is the most common structural mistake in
trigger-based campaigns: building a trigger list once and then sending from it for a
quarter.
