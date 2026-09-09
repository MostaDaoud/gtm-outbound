# Sequence — [Campaign]

Generated: [date] · Stage 3 of 3
Platform: [Smartlead / Instantly] · Merge tags validated against: [allowed_vars.json / UNVALIDATED]
Geography: [market] · [load gcc-market.md if Gulf/MENA]

---

## Evidence Behind the Opener

Fill this before writing a word. If you cannot complete it, the observation is not ready.

```
OBSERVATION      [verifiable fact]
SOURCE           [URL]
DATED            [when published/observed, or UNDATED]
SIGNAL AGE       [days]  ·  decay window: [days]  ·  [in window / STALE]

INFERENCE        [what this may indicate operationally]
HYPOTHESIS       [problem or opportunity that may follow]

CONFIDENCE       high / medium / low
BECAUSE          [why that level]
ALTERNATIVE      [the innocent explanation that would make this wrong]

ROLE RELEVANCE   [why this role specifically would care]
VOCABULARY       [2-4 terms they actually use]
```

**Personalization level achieved:** [1-5] — see `personalization-depth.md`
**Route to relevance:** [segment narrative / recent signal]

---

## Arm A — Soft CTA

### Email 1

**Structure used:** [Poke the Bear / Observation-Problem-Proof-Ask / Question-Value-Ask / Trigger-Insight-Ask / Story-Bridge-Ask]
**Why this one:** [what you could credibly lead with]

**Subject:** [2-4 words, lowercase, no merge tag, written last]

```
[greeting spintax] {{first_name}},

[BLOCK 2 — hook: observation, from the evidence above]

[BLOCK 3 — value prop: niche + dream outcome + risk removed, one sentence]

[BLOCK 4 — credibility: named comparable result, if it belongs here]

[BLOCK 5 — CTA: open question]
```

| Block | Present | Notes |
|---|---|---|
| 1 Subject | | |
| 2 Hook | | |
| 3 Value prop | | |
| 4 Credibility | | |
| 5 CTA | | |

**Words:** [min-max] · **Variants:** [n] · **Hedges:** [n, target 1] · **you:we ratio:** [n:n]
**CTA friction:** [soft / hard] · **Ends on a question:** [yes/no]

### Email 2 — New Angle · Day 3-4
```
[body]
```
**Adds:** [what is new — not a restatement] · **Stands alone:** [yes/no]

### Email 3 — Proof · Day 7-9
```
[body]
```
**Proof point:** [named result, comparable company]

### Email 4 — Clean Close · Day 14
```
[body]
```

---

## Arm B — Hard CTA

Identical to Arm A except the CTA. Only the changed lines shown.

**Email 1 CTA:**
```
[direct, specific, time-bound ask]
```

**Why hard is defensible here:** [value prop strong enough that the reply costs no thought — or mark as the test arm]

---

## LinkedIn Track

| Step | Timing | Content |
|---|---|---|
| Connection request | Day 0 | No note |
| Message 1 | On acceptance | [mirrors the email observation, does not repeat it] |
| Message 2 | +4 days | [new angle, under 50 words] |

## Phone Track (if used)

See `cold-call.md`. Place Call 1 around day 3, after email 1 has landed.

```
[opener: name yourself → reason for call → qualified hypothesis → ask for 30 seconds]
```

---

## Merge Variables Used

| Variable | Produced by (Clay column) | Exported as | Fallback if empty |
|---|---|---|---|
| | | | |

Every row must trace to a column in `clay-table.json` **with a `smartlead_field` mapping**.
A column that exists but is not exported renders blank on every send.

---

## Validator Output

Both are gates. Paste real output.

```
[validate_spintax.py --vars allowed_vars.json --max-words 80]
```

```
[score_message.py --vars allowed_vars.json]
```

**Any error-severity finding fails the sequence regardless of score.**

---

## Test Design

| | Arm A | Arm B |
|---|---|---|
| CTA | Soft | Hard |
| Sample needed per arm | [from `gtm_math.py ab`] | |
| Days to conclude | | |

Do not scale a winner before `gtm_math.py ab-eval` confirms significance.

---

## Sending Configuration

| Setting | Value |
|---|---|
| Sends per inbox per day | 15-25 |
| **Sends per DOMAIN per day** | **[≤ 40 — the binding constraint]** |
| Mailboxes per domain | 2-3 |
| Inboxes / domains | [n] / [n] |
| Warmup before first send | 14 days |
| Warmup per day · ramp | 40 · 10→15→20→25 |
| Randomized warmup | On |
| Open tracking | Off |
| Link tracking | Custom domain |

**First send date:** [date] — accounts for warmup

### Compliance
- [ ] SPF, DKIM, DMARC on every sending domain
- [ ] **One-click unsubscribe headers** (`List-Unsubscribe` + `List-Unsubscribe-Post`)
- [ ] Opt-outs processed within 2 days, suppression shared across all campaigns
- [ ] Physical address in footer
- [ ] Sending domain separate from primary
- [ ] Jurisdiction checked — [US / EU per member state / UK / Canada / GCC]

---

## Assumptions

[Anything stated without client data, so it can be replaced when real numbers arrive.]
