# Campaign Diagnosis — [Campaign]

Date: [date] · Channel: [email / linkedin]
Data source: [live via MCP, pulled {timestamp} / manual export, file dated {date}]
Period covered: [n] sending days

---

## Verdict

> **Fix the [LAYER] layer first.**
>
> [One sentence: what is broken and what it is costing.]

**Do NOT do these yet:**
- [ ] [downstream layer] — changes there will be masked by the above
- [ ] [downstream layer]

---

## Evidence

```
[paste diagnose_campaign.py output verbatim]
```

| Metric | Observed | Healthy band | Reading |
|---|---|---|---|
| Bounce rate | | under 2% healthy, 2-3% investigate, over 3% pull domain, over 4% pause | |
| Reply rate | | 3-8% | |
| Positive share | | 20-30% | |
| Complaint rate | | under 0.1%, enforce at 0.3% | |
| Sends per domain per day | | under 40 | |

State the band alongside every number. "3% reply" is not a finding; "3% against a 3-8%
band" is.

---

## Ruled Out

What was checked and found clean, in layer order. This matters as much as the finding —
it is what justifies skipping ahead.

| Layer | Checked | Clean? |
|---|---|---|
| Infrastructure — placement, domain load, bounce, complaints | | |
| List — targeting, verification, segment variance | | |
| Offer — positive share, unsubscribe rate | | |
| Copy — only reached if all above are clean | | |

**Seasonality checked:** [yes/no] — [Ramadan, Eid, holidays, quarter-end. Required for
MENA campaigns; a calendar collapse is indistinguishable from a deliverability event.]

---

## The Fix

**Owner layer:** [infrastructure / list / offer / copy / profile]

| # | Action | Effort | Expected effect |
|---|---|---|---|
| 1 | | | |
| 2 | | | |

**Routed to:** [`gtm-outbound-offer` / `gtm-outbound-list` / `gtm-outbound-copy` / `deliverability.md`]

---

## Confidence

**Sample size:** [n] delivered — [sufficient / too small to conclude]

Under a few hundred delivered, most of these rates are noise. Say so rather than
diagnosing confidently off a thin sample.

**Sudden or gradual:** [collapse suggests placement; gradual decline suggests fatigue]

---

## What Would Sharpen This

[What data was missing — per-inbox rows, complaint counts, segment labels, dates. Ask for
it in the next export.]

---

## Re-check

After the fix lands, re-run against a fresh export and confirm the layer cleared before
moving down the stack. A fix that was never verified is an assumption.

```bash
python scripts/diagnose_campaign.py [export] --group-by inbox --days [n]
```
