# GTM Benchmarks — What Good Looks Like

Load when interpreting campaign results in `gtm-outbound-diagnose` or setting assumptions
in `gtm-outbound-math`.

Benchmarks adapted from the GTM Metrics and KPIs material in the GTM course transcripts.
These are practitioner figures for B2B cold email and LinkedIn, not universal constants —
treat them as calibration, and replace each one with your own data as it accumulates.

*2026 additions checked 2026-09-09 against the sources cited with each figure.*

## Denominators First

The single most common benchmark error is quoting a reply rate without its denominator.
Replies divided by *sent*, replies divided by *delivered*, and replies per *contact* are
three different numbers describing one reality — and they differ by several multiples in
size.

Belkins' 0.45% is of sent. Smartlead's 0.74% median is contacts-per-reply. Instantly's
3.43% is of delivered. These are not conflicting benchmarks; they are the same market
counted three ways (checked 2026-09-09:
https://caliberoutbound.com/blog/cold-email-benchmarks-2026-reply-rates-by-industry).

**Rule: state the denominator whenever quoting a rate.** A rate without one is not
calibration — it is noise.

## Metrics That Are Not KPIs

Two numbers that look like signal and are not. Both are worse than useless, because
collecting them actively costs you placement.

| Metric | Why not |
|---|---|
| **Open rate** | Requires a tracking pixel, which damages domain reputation. Since Apple Mail Privacy Protection began pre-fetching images, the number is not even accurate. Do not track it. |
| **Click-through rate** | Same pixel problem. Link and open tracking are recognisable marketing-tool behaviour, and mailbox providers use that to route messages to Promotions or Spam. |

If someone reports a campaign by open rate, the first useful thing to say is that the
number is not measuring what they think, and that collecting it made placement worse.

## 2026 Benchmarks

*Every figure in this section checked 2026-09-09 against the source cited with it.*

| Source | Figure | Denominator |
|---|---|---|
| **Smartlead State of Cold Email 2026** (850M emails, Jan-Jun 2026) | 0.74% median reply; top 10% at 2.63%+; bottom quartile under 0.37% | contacts-per-reply |
| **Instantly Cold Email Benchmark 2026** | 3.43% average; top quartile 5.5%; elite 10.7%+ | of delivered |
| **SmartReach State of Cold Email 2026** (agency funnel) | ~10% reply → ~2.2% positive → ~1.2% meeting → ~0.6% opportunity; agencies roughly 2x in-house across verticals | agency funnel stages, of sent |
| **Belkins** (all industries) | 0.45% | of sent |

Sources: https://www.smartlead.ai/benchmarks/average-cold-email-reply-rate ·
https://instantly.ai/cold-email-benchmark-report-2026 ·
https://smartreach.io/reports/state-of-cold-email/the-state-of-cold-email-2026.pdf

**Reconciliation**
(https://caliberoutbound.com/blog/cold-email-benchmarks-2026-reply-rates-by-industry):
positive replies run 0.3-0.8% of sent, with 1%+ marking a strong campaign; a healthy
campaign sees 20-40% of replies positive; total reply below 2% of sent indicates a list or
deliverability problem, not a copy problem.

**Platform-data skew.** These datasets over-represent engaged, optimized senders — the
platforms count their own most-active users. That is why the same underlying reality reads
0.45% and 3.43% depending on who is counting. The 3-8% band in the table below is
*average-to-good, per-delivered, platform-skewed* — quote it only with that denominator
attached.

**Bounce.** Median 1.54% (Smartlead:
https://www.smartlead.ai/benchmarks/cold-email-bounce-rate). Verification moves most
senders toward the median; a rate far from it usually means verification was skipped or is
broken.

### Sequence Structure

58% of replies land on step 1 (Instantly 2026), 84% of positive replies arrive within the
first four emails, and the reply curve goes flat after roughly five follow-ups (Woodpecker
data via https://searchlab.nl/en/statistics/cold-email-statistics-2026). Additional steps
buy little; sequence length is a diminishing-returns decision.

### Copy Effect Sizes

Gong's 85M-email study with Outbound Squad / 30MPC (2025)
(https://www.gong.io/blog/does-cold-email-even-work-any-more-heres-what-the-data-says):

- Pitching in the email cuts reply rate by up to 57%.
- Buzzwords or numbers in subject lines cut opens 17.9% — measured in opens, a degraded
  metric (see *Metrics That Are Not KPIs*), but the direction is unambiguous.
- Ideal length is 100 words or fewer, 3-4 sentences.
- Top performers get 4.2x the replies and book 8.1x more meetings.

### Timing

Tuesday-Wednesday is the peak — Tuesday the single best day at 3.8% reply — with Friday
and weekends the worst. January and September run 18-22% above the monthly average
(compilation at https://searchlab.nl/en/statistics/cold-email-statistics-2026).

### Personalization

Trigger-based personalization — anchored to a real event — draws 5.3% reply against a
generic opener, a +71% lift (Woodpecker, via the searchlab compilation above).

### Scale

Senders under 10k messages/month report 5-10% replies; above 100k/month, 1-3%
(https://levelupleads.io/cold-email-benchmarks-2025-key-stats-every-marketer-should-know).
Personalization scales down, not up: the smaller the volume, the more each email can be
researched. Do not calibrate a small sender against platform medians built on large ones.

## Email Benchmarks

| Metric | Healthy | Action threshold |
|---|---|---|
| **Bounce rate** | Under 2% (median 1.54%) | Ladder: above 2% elevated; above 3% danger — pull the domain; above 4% — pause |
| **Reply rate** | 3-8% — average-to-good, per-delivered, platform-skewed (see 2026 Benchmarks) | Under 1% — this is targeting or deliverability, never copy |
| **Positive share of replies** | 20-30% | Under 20% — the offer or the CTA is wrong |
| **Inbox placement** | Over 80% primary | Under 60% — pause and extend warmup |
| **Spam complaints** | Under 0.1% | Over 0.3% — pause immediately |

**The sub-1% reply rate protocol**, in order — this is the same layer ordering
`diagnose_campaign.py` enforces:

1. Run a placement test. Deliverability is the most common cause and the cheapest to check.
2. Check the list. Wrong targeting produces the same symptom.
3. Only then look at the CTA — specifically its friction level.

## CTA Friction

A distinct diagnostic lever, easy to miss because the copy reads fine. When reply rate is
weak but placement and list both check out, the ask is the next suspect — lower the
friction or raise the value before rewriting sentences.

Full friction ladder and the behaviour model behind it: `cta-design.md`.

## LinkedIn Benchmarks

| Metric | Healthy | Action threshold |
|---|---|---|
| **Connection acceptance** | Over 20%; 30% good, 40% excellent | 10% or below — targeting is wrong or the profile is not optimised |
| **Reply rate after acceptance** | 10-20% | Under 10% — message too long, wrong targeting, or weak offer |
| **Positive share of replies** | 20-30% | Under 20% — offer or CTA, change the campaign narrative |

**Send connection requests without a note.** Acceptance is measurably higher, and a note
spends your one shot before any relationship exists — most people use it to pitch, which
is precisely why it lowers acceptance.

A low acceptance rate is often the *sender's profile*, not the targeting. This is the one
LinkedIn failure with no email equivalent: the recipient evaluates you before reading
anything you wrote.

## Funnel Benchmarks

| Metric | Healthy | Reading |
|---|---|---|
| **Lead to deal conversion** | 20-30% | Under 10% means the offer is weak or the sales motion is, not the top of funnel |
| **Cost per lead** | Compare across channels, not against an absolute | The channel with the lowest CPL and highest conversion gets more budget |

Cost per lead is only meaningful comparatively. Run it per channel and let the comparison
allocate spend — an absolute CPL number tells you almost nothing on its own.

## Verification Providers

| Provider | Note |
|---|---|
| MillionVerifier | Affordable, solid default |
| LeadMagic | Affordable, also does email finding |
| Bounceban | Higher quality, higher price — worth it when bounce rate is the binding constraint |

If bounce rate is above 3% *after* verification — past the danger tier of the ladder —
the verification tool itself is the problem. Change it rather than tightening filters
around it.

## Quality and Cost Metrics

Reply rate cannot tell you whether personalization is working, or whether it is
economically sustainable. Four measures it hides:

| Metric | Formula | What it catches |
|---|---|---|
| **Pipeline per research hour** | qualified pipeline ÷ research hours | Whether depth actually pays. A message that doubles reply rate and takes ten times longer is a loss. |
| **Offer acceptance rate** | accepted offers ÷ messages containing that offer | Whether the lead magnet is genuinely wanted, separately from meeting conversion |
| **Factual defect rate** | audited messages with a wrong claim ÷ audited | The risk personalization introduces. A confident wrong claim is worse than no claim. |
| **Boundary violation rate** | messages judged invasive ÷ audited | Whether research is drifting into detail that damages the sender |

The last two require someone actually reading a sample of what went out. Without that
audit both read as zero, and neither is.

**Segment before trusting any of these.** An aggregate reply rate conceals a tactic that
works on managers and fails on executives, or works in one geography and not another. The
useful question is never "did personalization help" but "which kind produced commercially
useful conversations at a research cost we can sustain."

## Testing Discipline

Change one variable at a time. Signal type, subject line, length, proof, and CTA moved
together produce a winner that teaches you nothing about why it won.

Assign comparable prospects within the same segment to baseline and one treatment. Size it
with `gtm_math.py ab` first — most proposed tests cannot resolve at the available volume,
and learning that beforehand saves the send budget.

## Observed Campaigns — MENA B2B SaaS

Reported results from three campaigns run by the practitioner behind the GTM course, into
Gulf and Egyptian B2B SaaS buyers. Small sample, one operator, self-reported — **use them
to sanity-check a band, never as a target to promise a client.**

| Campaign | Reply rate | Positive share | Outcome |
|---|---|---|---|
| Fintech SaaS | 3.2% | 43% | ~200 positive replies over 2 months |
| Corporate wellness SaaS | 7.0% | 35% | 170 leads, 45 meetings over 3 months |
| Corporate mobility SaaS | 4.3% | 45% | ~120 leads over 4 months |
| Agency campaign (single) | — | — | 10,000 sends → 106 positive replies (~1.1% of sends) |

**Reply rates sit inside the standard 3-8% band. The positive share does not.** These run
35-45% where the cold-B2B default used elsewhere in this skill is 20-30%. Two readings, and
you cannot tell them apart from this data alone:

- **Segment and offer fit were unusually good**, which is what a tight sub-niche plus a
  concrete offer is supposed to produce — in which case 20-30% is a floor for lazy targeting
  rather than a ceiling.
- **"Positive" was scored generously.** Positive-reply definitions vary enormously between
  operators, and nothing here pins down whether a soft "send me info" counted.

**The second reading is now confirmed, and it matters.** In Smartlead the positive-reply
number is not a fixed definition — it is a *configurable mapping*. A Category Manager lets
the operator declare which reply categories count as positive, and the campaign analytics
follow that declaration. The setup behind these campaigns marks **"Information Request",
"Meeting Request" and "Interested" all as positive.**

So a reply saying "send me more info" scores identically to one asking for a meeting. That
is a defensible operational choice — both are live conversations — but it is a **wider
definition than the 20-30% band assumes**, and it explains most of the gap without needing
to believe the targeting was three times better than normal.

**Two consequences.** First, never compare a positive-reply rate across operators without
asking how the categories are mapped; the number is not standardised and the tool does not
make the mapping visible in the headline figure. Second, when reporting your own, say which
categories you counted — otherwise you are quoting a number nobody can interpret, including
yourself in three months.

**Practical use:** keep 20-30% as the planning default in `gtm_math.py`, because planning
against the optimistic end of a self-reported range is how campaigns miss. But treat a
positive share below 20% as a real signal that the offer or segment is wrong — these
numbers show the ceiling is well above that when both are right.

**The last row is the one to internalise.** 10,000 sends produced 106 positive replies —
roughly 1%. That is what a functioning campaign looks like from the top of the funnel, and
it is why `gtm_math.py size` exists: the intuition that 10,000 emails is a lot of emails
does not survive contact with the arithmetic.

## Using These

- State which benchmark you are comparing against when you report a number. "3% reply" is
  not a finding; "3% reply against a 3-8% healthy band, so mid-range" is.
- Replace these with the user's own historical figures the moment those exist. A house
  benchmark beats an industry one every time.
- When a metric is outside the band, name the layer before naming the fix. See
  `gtm-outbound-diagnose`.
