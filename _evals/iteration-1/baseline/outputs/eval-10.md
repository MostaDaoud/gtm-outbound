# Task 10 Response

I read your clay-table.json. Quick flag before the sequence: your current schema only resolves `company_domain`, `first_name`, `email_leadmagic`, and `verified_email`. There's no column yet that pulls funding data (round, amount, date, investors), so "personalize on their recent funding round" isn't something the table can actually populate today — you'd send blank merge fields.

**Fix needed first:** add an enrichment column, e.g.:

```json
{"name": "recent_funding", "stage": "enrich", "provider": "clearbit" /* or crunchbase/harmonic */,
 "type": "string", "inputs": ["company_domain"], "run_condition": "always",
 "smartlead_field": "recent_funding", "notes": "most recent funding round + amount, e.g. 'Series B, $40M'"}
```

You'll also want a filter/run_condition so the sequence only fires for rows where `recent_funding` is non-null — otherwise you're back to generic copy for anyone without a fresh round on record.

Assuming that column exists and is mapped to Smartlead as `recent_funding`, here's a 4-step sequence built around it:

---

**Step 1 (Day 0) — Congrats + relevance hook**
Subject: congrats on the {{recent_funding}}

Hi {{first_name}},

Saw the {{recent_funding}} news for {{company_name}} — timing like that usually means outbound and pipeline targets get more aggressive fast, and the sales infrastructure has to catch up quickly.

We help mid-market SaaS teams build that infrastructure — data, deliverability, sequencing — so growth in headcount and targets doesn't outrun the systems supporting it.

Worth a quick look at what that could mean for {{company_name}}?

{{sender_name}}

---

**Step 2 (Day 3) — Proof**
Subject: what a fresh raise usually breaks first

{{first_name}} — following up briefly.

Post-raise, the first thing that usually breaks isn't headcount, it's outbound infrastructure not scaling with it. We saw this with a Series B fintech client — rebuilt their targeting and sending setup and cut cost-per-booked-call 34% in 90 days, right as they were scaling the team.

Happy to share exactly what we changed, in case it's relevant post-{{recent_funding}}.

{{sender_name}}

---

**Step 3 (Day 8) — Direct ask, low friction**
Subject: 15 min?

{{first_name}}, keeping this short — with the {{recent_funding}} likely pushing pipeline targets up, is it worth a 15-minute call to see if our setup would save your team time rebuilding outbound infra from scratch?

If now's not right, no worries — just say so and I'll leave it there.

{{sender_name}}

---

**Step 4 (Day 14) — Breakup**
Subject: closing the loop

{{first_name}} — haven't heard back, so I'll assume outbound infrastructure isn't a priority right now post-raise. I'll close this out on my end.

If that changes, happy to reconnect — the case study (34% cost-per-call reduction, fintech, 90 days) is available anytime.

{{sender_name}}

---

Notes on execution:
- Gate the whole sequence on `recent_funding` being populated (empty = skip, don't send generic version through this campaign).
- Consider bucketing by round size/stage (seed vs. Series B+) since urgency and budget differ — Enterprise-tier messaging fits large raises, Starter fits smaller ones.
- Recency matters: funding personalization loses credibility after ~60-90 days, so refresh the enrichment column on a rolling basis rather than a one-time pull.
