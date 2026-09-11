# Sourcing Channels — Where Lists Actually Come From

Load when selecting sourcing channels in `gtm-outbound-list`.

Tool capabilities and access terms change. Verify a source still exposes what you need,
and that your use is within its terms, before building a pipeline on it.

## Selection Logic

Choose the source that makes your **trigger** observable, not the one with the most rows.

```
Is the sub-niche defined by a trigger event?
  ├─ Yes → use a trigger source (job boards, funding, PhantomBuster, review activity)
  └─ No  → is it defined by an observable attribute?
             ├─ Yes → use a directory or tech-detection source
             └─ No  → the sub-niche is underspecified; return to gtm-outbound-offer
```

The third branch is common and worth catching early. "Companies that need better data
hygiene" is not sourceable, and no amount of Clay will fix that.

## Channel Table

| Source | Best for | Yields | Notes |
|---|---|---|---|
| **Clutch** | Agencies, dev shops, consultancies | Company, services, client list, reviews, size | Client rosters are excellent personalization fuel |
| **Storeleads** | Ecommerce brands | Platform, traffic band, apps, revenue estimate | Best single source for Shopify segments |
| **BuiltWith / Wappalyzer** | Tech-stack segments | Detected tech, install date | Install date is a strong recency trigger |
| **PhantomBuster** | Engagement-based segments | Post commenters, likers, event attendees, group members | Highest-intent source available; low volume |
| **Job boards / LinkedIn Jobs** | Hiring-trigger segments | Role, dept, posted date, JD text | JD text often states the pain in their own words |
| **G2 / Capterra** | Software buyers, competitor users | Reviews, categories, sentiment | Reviewers are identifiable and already vocal |
| **Crunchbase** | Funding-trigger segments | Round, amount, date, investors | Window closes fast; keep under 6 months |
| **Apollo / Sales Navigator** | General B2B | Contacts and firmographics | Broad but everyone else is emailing the same rows |
| **Industry associations** | Regulated and niche verticals | Member directories | Underused; often unscraped by competitors |
| **Podcast / conference rosters** | Thought-leader segments | Speakers, guests, sponsors | Small, very high relevance |

## Trigger Sources Beat Static Directories

A static directory gives you a company that *matches*. A trigger source gives you a
company that matches **and has a reason to care this month**.

Ranked by typical strength:

1. **Job posting for the role that owns your problem** — budgeted, timestamped, public.
2. **Recent funding** — money to spend and pressure to deploy it.
3. **New tech install / removal** — actively rebuilding that part of the stack.
4. **Engagement with a competitor or topic** — self-identified interest.
5. **Leadership change in the buying role** — new mandate, no vendor loyalty.
6. **Review or complaint about an incumbent** — stated dissatisfaction.

Static attributes still matter, but they belong in the filter, not the trigger.

## Multi-Source Strategy

Use at least two sources per campaign.

- Every source has coverage bias you cannot see from inside it. Clutch only has agencies
  that chose to list. Storeleads misses headless builds.
- Two sources let you compare reply rate by origin, which is often a bigger performance
  difference than any copy test.
- Overlap between two independent sources is a quality signal worth tagging.

Record source per row in the Clay table. Segmenting results by origin later is
impossible if you did not.

## Extraction Notes

**Directories** — paginate carefully and capture the profile URL as the join key.

**PhantomBuster** — respect rate limits. Aggressive scraping risks the LinkedIn account,
not just the run. Use a secondary account, never the one running the campaign.

**Job boards** — capture posting date and the JD body. The JD frequently contains the
exact pain language to mirror in the observation line.

**Review sites** — capture review text and date. A specific complaint about an incumbent
is among the strongest observations available for a first line.

## What Not to Source

- Purchased lists with no provenance. Bounce rates and spam-trap risk are unacceptable,
  and a single trap hit can burn a domain.
- Consumer personal addresses. Different legal footing entirely; out of scope here.
- Anything behind a login you agreed not to scrape. The account loss is not worth it,
  and it is a contract violation regardless of whether it is detected.
- Rows older than ~12 months without re-verification. B2B contact data decays fast —
  people change jobs constantly.

## Yield Expectations

Rough planning figures. Measure your own; these vary enormously by segment.

| Stage | Typical survival |
|---|---|
| Raw scrape → deduplicated companies | 80-90% |
| Companies → domain resolved | 85-95% |
| Companies → at least one matching contact | 50-70% |
| Contacts → email found (good waterfall) | 60-80% |
| Emails found → verified valid | 70-85% |

Compounded, roughly 25-45% of a raw scrape becomes a sendable row. Size the scrape from
the verified target backwards, using `gtm_math.py size --verify-pass-rate`, rather than
sizing forward and discovering the shortfall at send time.

## Audience-Borrowing Plays

The strongest lists are usually assembled from an audience someone else has already
qualified. These are the plays that produce a segment no directory filter can express.

| Play | Mechanism | Best for |
|---|---|---|
| **Post engagers** | Scrape likers and commenters on a relevant post — yours, a competitor's, or a creator's in the space — then filter to ICP | Warm-ish intent, dated, and still underused outside the US |
| **Competitor followers** | A competitor's LinkedIn company-page followers, filtered to ICP | People who have already self-identified as interested in the category |
| **A competitor's connections** | Sales Navigator's connections-of filter against a competing founder or sales lead in your network | Their network is disproportionately their market |
| **Niche groups and events** | LinkedIn or Facebook groups organised around a topic, certification, or conference; event networking groups | The topic *is* the qualifier — a PMI group is a project-management list |
| **Ads libraries** | Meta and LinkedIn ad libraries list who is actively running ads | Advertising spend is a growth-and-budget signal, and "saw your campaign" is a genuine, dated opener |
| **Tech install** | BuiltWith, SimilarWeb, or a Clay column for the stack they run | Selling into or against a specific tool |
| **Job openings** | See `signals-and-triggers.md` | Both a direct need and an indirect read on their stack |
| **Local business** | Google Maps, D7, and `maroof.sa` in Saudi | Anything without a meaningful LinkedIn presence — clinics, restaurants, trades |

**Funding data: check Apollo before paying for Crunchbase.** Apollo's funding filter is
sourced from the same underlying data at a fraction of the per-row cost. Reach for a
premium funding provider only when Apollo's coverage demonstrably fails your segment.

### One of these crosses the line

A play circulates in which you add a fake job entry to your own LinkedIn profile claiming
to work at a competitor, so that Sales Navigator's "following your company" filter exposes
that competitor's follower list.

**Do not run it.** It is misrepresentation to LinkedIn and to every person who views the
profile, and this skill does not assist with disguising sender identity — the same boundary
that rules out spoofed sending domains. The list it produces is not worth a sales profile
that says something false about where you work.

The legitimate versions of the same idea are already in the table above: followers, post
engagers, and connections-of are all reachable without claiming to be someone you are not.
