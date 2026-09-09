# Eval 15 — "set up a cold email campaign targeting CTOs in Germany and France"

No `icp.json` or `clay-table.json` existed in this session, so I reconstructed the ICP
inline rather than blocking, ran the full offer → list → copy chain, and I'm flagging that
reconstruction here rather than presenting it as inherited. I also made a few calls I
didn't have data for — flagged below rather than buried.

## Compliance flag, upfront

Germany and France are both in the EU. Cold B2B outbound there typically runs on **GDPR
legitimate interest**, which requires a documented balancing assessment — it is not
automatically covered by CAN-SPAM-style rules. I'm not asserting this setup is compliant.
Confirm your legitimate-interest basis with counsel before sending, and make sure the
suppression list, opt-out, and physical-address requirements below are non-negotiable in
the build, not a nice-to-have.

## Step 1 — "CTOs in Germany and France" isn't a sub-niche yet

Per `icp-filters.md`'s hard rules: a title string alone (even a real one like "CTO," not a
seniority bucket) plus two entire countries is company-shape-agnostic. It has no headcount
band, no industry, and no trigger — which means the actual result count is very likely
**well over the 50,000-contact ceiling** the skill treats as "too loose to personalize."
I can't pull a live Sales Navigator/Apollo count from here, so I'm not going to invent one
— but the direction is clear enough to act on without it.

I narrowed it using your existing proof point (the Series B fintech case study) as the
signal for where you already have credibility, per the offer skill's rule to start with
the segment where the proof is strongest, even if smaller:

**Sub-niche (assumption, not yours yet — confirm or correct):**
> Series A-C SaaS companies headquartered in Germany or France, 50-500 employees, that have
> posted an engineering or RevOps hiring signal in the last 60 days.

industry/vertical (SaaS) × trigger (recent eng/RevOps hire) × company stage (Series A-C,
50-500 staff) — the three-part compression `gtm-outbound-offer` requires, instead of the
two flat filters in the original ask.

**Value Equation, scored as the prospect would score it:**

| Lever | Score (1-5) | Note |
|---|---|---|
| Dream outcome | 4 | Cheaper, more predictable pipeline is a wanted outcome |
| Perceived likelihood | 2 | **Weakest lever.** One case study, one vertical (fintech), being pitched to a different vertical (SaaS) and a different geography. Likelihood is unproven here. |
| Time delay | 3 | 90-day case study result is a real, citable number |
| Effort & sacrifice | 4 | Low — this is an outsourced infra build, not a process change on their side |

The weakest lever is perceived likelihood, and that's the whole reason Email 1 below leans
on the case study number rather than a generic capability claim — attacking the weak lever
with proof and specificity, not better adjectives.

## Step 2 — Filter sets

**Company level:**
- Headcount: 50-500 (one band — buying process is comparable across it)
- Geography: Germany, France
- Industry: SaaS / software
- Funding stage: Series A-C, funding event within 6 months (decay window per the filter
  rules)
- Trigger: posted an engineering leadership or RevOps role in the last 60 days

**Contact level (exact title strings, not seniority alone):**
`"CTO" OR "Chief Technology Officer" OR "VP Engineering" OR "Head of Engineering" OR "VP RevOps"`

**Exclusions:** agencies/consultancies (not the ICP shape), staffing firms, current
customers, open opportunities, anyone who opted out or replied negatively in the past 12
months, assistant/intern/coordinator/recruiter titles.

## Step 3 — List and enrichment pipeline

Two sources, per the "single-source lists inherit that source's blind spots" rule: Apollo
for the base company/contact list, BuiltWith for tech-stack signals, job boards for the
hiring trigger.

Generated the Clay schema rather than hand-writing it. First attempt caught a real ordering
problem, worth showing:

```bash
python clay_taxonomy.py generate --waterfall leadmagic,dropcontact,findymail \
  --sources apollo,builtwith,job_boards --personalize recent_engineering_signal \
  -o clay-table-task15.json
```

```
Clay table validation: FAIL
  16 columns, 1 errors, 0 warnings
  ERROR    Waterfall runs 'email_dropcontact' (tier 2) before 'email_findymail' (tier 1).
           The cheaper provider should go first so the expensive one only sees leftovers.
```

Reordered so tier-1 providers run first (`leadmagic`, `findymail`), with `dropcontact` —
flagged in the provider registry as "GDPR-friendly, EU-focused" — as the tier-2 fallback,
which is also a reasonable fit given the recipients:

```bash
python clay_taxonomy.py generate --waterfall leadmagic,findymail,dropcontact \
  --sources apollo,builtwith,job_boards --personalize recent_engineering_signal \
  -o clay-table-task15.json
```

```
Wrote clay-table-task15.json (16 columns)
Clay table validation: PASS
  16 columns, 0 errors, 0 warnings
  Exported merge fields: email, first_name, job_title, last_name, recent_engineering_signal
```

```bash
python clay_taxonomy.py vars clay-table-task15.json > allowed_vars-task15.json
```
```
email, first_name, job_title, last_name, recent_engineering_signal
```

Route every found address through MillionVerifier, gate sending on `valid` only, expect
~30% attrition raw-to-verified.

## Step 4 — Sequence

### Arm A — Soft CTA

**Email 1 — Poke the Bear**
Subject: `pipeline infra`
```
{{Hey|Hi|Hello}} {{first_name}},

{{Saw|Noticed}} {{recent_engineering_signal}} — {{that's usually about when the team providing pipeline data can't keep pace with what engineering just shipped|that's normally the point where the data feeding sales stops matching what the product actually does}}.

{{Who owns fixing that gap right now|Is that landing on your team or on revenue ops}}?

{{Best|Thanks|Talk soon}},
Alex
```

**Email 2 — New Angle, Day 3-4**
```
{{One thing worth flagging|Something adjacent}}: most engineering-led scaling stalls not on the product side but on the enrichment and verification feeding outbound — bad data compounds fast once volume goes up.

{{Is that something your team owns, or does it sit with GTM|Curious who owns that on your side}}?
```

**Email 3 — Proof, Day 7-9**
```
For context: we cut cost-per-booked-call 34% for a Series B fintech client in 90 days, mostly by fixing the enrichment layer before touching the messaging. {{Happy to share the breakdown|Can send the specifics}} if it's useful for comparison.
```

**Email 4 — Clean Close, Day 14**
```
{{Will leave it here|Last one from me}} — if the data layer behind outbound becomes a live problem, {{the door's open|feel free to reach back out}}.
```

### Arm B — Hard CTA
```
{{Open to 15 minutes next week|Got time Thursday for a quick call}}?
```

### LinkedIn Track

| Step | Timing | Content |
|---|---|---|
| Connection request | Day 0 | No note |
| Message 1 | On acceptance | Mirrors the engineering-signal observation, not verbatim |
| Message 2 | +4 days | New angle, under 50 words |

### Validator output

```bash
python validate_spintax.py SEQUENCE.md --vars allowed_vars-task15.json --max-words 80
```
```
Spintax validation: PASS  (dialect: smartlead)
  11 spin blocks, 2 merge tags, 0 errors, 0 warnings

  Message                                      Words    Variants
  -------------------------------------- -----------  ----------
  Email 1 — Poke the Bear                      32-37          72
  Email 2 — New Angle — Day 3-4                34-41           4
  Email 3 — Proof — Day 7-9                    34-35           2
  Email 4 — Clean Close — Day 14               17-20           4
  Email 1 CTA (Arm B)                            6-7           2
```

Note `{{first_name}}` is the only Clay-sourced merge tag actually used in Email 1;
`recent_engineering_signal` is real and validated. Company name was deliberately left out
of the observation this time — it wasn't needed for the sentence to read as specific — so
I didn't need to patch the `company_name` export gap the way Eval 10 required.

## Step 5 — Smartlead / deliverability configuration

Assumption flagged: this is being treated as **new sending infrastructure** since none was
specified. That puts the 14-day-minimum warmup on the critical path (see Eval 14 for the
same constraint in more detail).

| Setting | Value |
|---|---|
| Sends per inbox per day | 25 |
| Warmup before first send | 14 days minimum |
| Warmup emails per day | 40 |
| Ramp-up increment | +5/day |
| Warmup reply rate | 30-40% |
| Randomized warmup | On |
| Mailboxes per domain | ~3 |
| Open tracking | Off |
| Link tracking | Custom domain only |

Domain strategy: dedicated sending domains, never the primary company domain — close
variants (`getacme.com`, `acme-hq.com`), each redirecting to the main site, SPF/DKIM/DMARC
(`p=none` → tighten later) on every one.

**Compliance checklist for this build specifically:**
- [ ] Real physical mailing address in the footer
- [ ] Working, immediately-honored opt-out; suppressions shared across every campaign, not
      just this one
- [ ] Documented GDPR legitimate-interest basis, reviewed with counsel — this is the item
      most likely to get skipped, and it's the one I'd least want skipped

## What I didn't fabricate

- **A real TAM.** "CTOs in Germany and France" needs an actual Sales Navigator/Apollo query
  to size — I flagged that it's likely far outside the workable band rather than inventing
  a number.
- **A meetings goal**, which means I didn't run `gtm_math.py size`. Give me either a
  meetings/month target or a list size once the filters above are confirmed or corrected,
  and I'll size inboxes, domains, and first-send date in one line, the way Eval 11 and
  Eval 14 do.
- **Language.** Copy above is in English, which is standard for B2B/technical roles in both
  markets, but it's an assumption — confirm before sending, especially for subject lines.

## Files produced

- `clay-table-task15.json` — validated Clay schema (16 columns)
- `allowed_vars-task15.json` — merge variables the copy above was checked against
