# GTM Math — Reading the Output

Load when interpreting `scripts/gtm_math.py` output or explaining a number to someone.

**The script is authoritative.** This file does not restate its formulas — read the source
if you need them. What follows is the part the script cannot carry: what the terms mean,
what the defaults assume, and which two results should stop work rather than inform it.

## Funnel Definitions

These terms get used loosely, and the ambiguity compounds through the model. The script
uses:

| Term | Denominator |
|---|---|
| Reply rate | Prospects contacted |
| Positive rate | **Replies**, not prospects |
| Meeting rate | **Positive replies** |
| Prospect-to-meeting | The three multiplied |

**The common error is treating positive rate as a share of prospects.** That inflates the
funnel roughly 20× and produces a list too small to hit the goal — a mistake that only
surfaces after the list is built.

## Defaults, and What They Assume

| Input | Default | Assumes |
|---|---|---|
| Reply rate | 3-5% | Genuinely cold. Above 15% the script flags it as implausible |
| Positive rate | 20-30% | Of replies. Above 50% flagged |
| Meeting rate | 60% | Of positives |
| Sequence steps | 4 | |
| Sends per inbox/day | 15-25 | See `deliverability.md` |
| **Sends per domain/day** | **40** | The binding constraint, not the inbox figure |
| Working days | 22 | Per month. Not true for MENA — see `gcc-market.md` |
| Verify pass rate | 70% | Western data coverage. Far lower for MENA |

Every default is an assumption that should be stated in the output and replaced when real
data arrives. Say which one the user should argue with.

## Interpreting Results

**`size` runs both directions.** Backward from a goal, or forward from a list you already
have. Never route a "how many inboxes for my 3,000 leads" question through backward mode
by inventing a goal — the goal would be fabricated and the answer inherits it.

**Domains are sized from daily volume, not mailbox count.** Dividing inboxes by
mailboxes-per-domain silently permits several times the domain ceiling.

**`economics` must include labour.** Models counting only tooling and data understate real
cost enough to make every campaign look profitable.

**`ab` lift is relative.** A 30% lift on a 5% baseline means 6.5%, not 35%.

**`ab-eval` is unreliable below ~5 conversions per arm.** The normal approximation stops
holding; repeat the script's warning rather than quoting a clean p-value.

## Thresholds the Script Enforces

| Condition | Severity | Meaning |
|---|---|---|
| CAC > gross profit per customer | Blocker | Loses money on every won deal |
| Payback > 12 months | Warning | Needs financing, not a bigger list |
| Gross-profit-to-CAC < 3× | Warning | Not worth scaling before fixing conversion or price |
| Customers/month < 1 | Warning | Monthly averages mislead; judge over a quarter |

## The Two Results That Should Stop Work

Most output is descriptive. These two send the problem upstream:

**1. The goal exceeds the addressable market.** When `raw_leads_to_scrape > TAM`, no
sending capacity reaches the goal against this ICP. Fix the segment, the offer, or the
goal. Building the list anyway wastes the entire build.

**2. The required sample is unreachable.** When detecting the lift needs more sends than
the campaign will ever produce, the test cannot conclude — ever. Test a structural change
instead of a subtler variant.

Both prevent spend rather than describing it, which makes them more valuable than any
number in the table.

**Do not estimate sample size by intuition.** In testing, a strong unaided estimate of
"how much sample do I need" came out at roughly 1,000 per arm where the real answer was
36,693 — wrong by more than 36×. Run `ab` and paste the output.
