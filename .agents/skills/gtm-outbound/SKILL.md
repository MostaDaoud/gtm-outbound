---
name: gtm-outbound
description: >
  Engineers B2B outbound email and LinkedIn campaigns end to end: narrows the offer to
  a sub-niche via the Value Equation, builds Sales Navigator and Apollo filter sets,
  specs Clay waterfall enrichment, writes sub-80-word "Poke the Bear" sequences with
  validated spintax, and produces Smartlead deliverability, warmup, and
  compliance-gated configurations. Scores launch readiness, diagnoses failing campaigns
  from ESP exports, and triages replies and objections. Also models list size, inbox
  count, CAC, payback, and A/B significance.
  Use when user says "architect an outbound campaign", "GTM campaign blueprint",
  "engineer a Clay outbound workflow", "Poke the Bear sequence", "narrow my ICP",
  "waterfall enrichment", "spintax", "cold email sequence", "how many leads do I need",
  "my campaign is not working", "reply rate dropped", "someone replied", "handle
  objections", "is this campaign ready to launch", "is cold email legal", "compliance
  for cold outreach", "suppression list", "multichannel sequence", "AI SDR",
  "LinkedIn outreach sequence", or "video prospecting".
argument-hint: "[offer | list | clay | copy | math | full | validate <file>]"
compatibility: "Requires Bash tool access and Python 3.10+ for the scripts in scripts/."
metadata:
  author: Mostafa Daoud
  version: 2.0.0

---
<!-- fable-discipline-gate:v1 -->

## Pre-flight gate: Fable Discipline (run FIRST)

Before executing any instruction below, adopt the Fable Mindset operating manual at
`C:\Users\mosta\.claude\skills\fable-mindset\SKILL.md`. Apply its Decision Loop
(GROUND -> REASON -> ACT -> OBSERVE -> RE-EVALUATE -> VERIFY -> NARRATE) and its
7 execution rules to every step of this skill. FD runs first; this skill's own
instructions begin only after the discipline is adopted.
# GTM Outbound — Campaign Architect

Engineers outbound campaigns as a dependency chain rather than a pile of tactics.
Strategy constrains the data spec; the data spec constrains the copy. Each stage writes
an artifact the next stage reads, so a merge tag can never reference a field the
pipeline does not produce.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/gtm-outbound` | Interactive — asks what stage you are at, routes accordingly |
| `/gtm-outbound offer` | Value Equation, sub-niche, filters, UVP → `ICP-BLUEPRINT.md` |
| `/gtm-outbound list` | Sourcing + Clay waterfall spec → `LIST-SPEC.md`, `clay-table.json` |
| `/gtm-outbound clay` | Clay table construction — column order, credit class, prompts |
| `/gtm-outbound copy` | Poke the Bear sequence + spintax → `SEQUENCE.md` |
| `/gtm-outbound math` | List sizing, inbox count, CAC, payback, A/B significance |
| `/gtm-outbound score` | 100-point launch readiness score + ranked fix list |
| `/gtm-outbound full` | Runs offer → list → copy in order, emits `campaign-brief.md` |
| `/gtm-outbound diagnose <csv>` | Post-launch: why the campaign is failing, and what not to touch |
| `/gtm-outbound reply` | Classify inbound replies, handle objections, book meetings |
| `/gtm-outbound validate <file>` | Spintax + merge-tag lint on an existing sequence |

**Build → score → launch → diagnose → reply** is the full loop. The first four sub-skills
build a campaign; `score` gates it; `diagnose` and `reply` are what bring you back once
it is running. A campaign that is never diagnosed is a campaign you learn nothing from.

## The Artifact Chain

This is the skill's organizing principle. Do not skip it.

```
offer  ──► ICP-BLUEPRINT.md + icp.json
              └──► list ──► LIST-SPEC.md + clay-table.json
                              └──► copy ──► SEQUENCE.md + smartlead-config.json
```

**On entering any sub-skill, check for upstream artifacts in the working directory
first.** If `icp.json` exists, read it instead of re-asking what the ICP is. If
`clay-table.json` exists, the copy stage must validate its merge tags against it.

When an upstream artifact is missing, do not block. Collect the minimum inputs inline,
note in the output that the artifact was reconstructed rather than inherited, and
continue. A user who says "just write me the emails" gets emails.

## Orchestration Logic

Route on what the user is actually asking for, not on keyword matching alone:

| Signal in the request | Route to |
|---|---|
| Who to target, offer positioning, "narrow my ICP", filters | `gtm-outbound-offer` |
| Where to get the data, scrapers, channels, providers, verification | `gtm-outbound-list` |
| How to build the Clay table itself — columns, credits, prompts, cross-table | `gtm-outbound-clay` |
| Email copy, sequences, spintax, subject lines, Smartlead setup | `gtm-outbound-copy` |
| Multichannel cadence — video, WhatsApp, phone orchestration, conditional branching | `gtm-outbound-copy`, then `references/multichannel-orchestration.md` |
| Any number: how many, how much, is this significant, payback | `gtm-outbound-math` |
| "Is this ready", "score my campaign", review of a campaign that has not sent | `gtm-outbound-score` |
| Campaign has already sent and is underperforming, ESP export shared | `gtm-outbound-diagnose` |
| A prospect replied, objection handling, booking | `gtm-outbound-reply` |
| "Build me a campaign" with no stage specified | Interactive: ask which stage, offer `full` |

**Partial-target requests default to `full`.** A request like "set up a cold email
campaign targeting CTOs in Germany and France" names a slice of an ICP without asking for
any single stage. Do not route it to one sub-skill on the strength of the words it
happens to contain — a named audience is not the same as a finished ICP. Check for
upstream artifacts; if none exist, run the chain from `offer`, and say that you are
treating the named audience as a starting point rather than a completed blueprint.

**Live-campaign signals beat build signals.** If the user shares result data — reply
rates, an export, "it stopped working" — route to `diagnose` even when the sentence also
contains copy or list vocabulary. Rewriting copy is the most common wrong first move, and
the routing table should not encourage it.

**"Audit", "review" and "assess" do not name a stage — ask whether it has sent.** Both
`score` and `diagnose` assess a campaign and return a ranked fix list, and the only thing
separating them is whether anything has gone out yet. One question settles it, and it is
worth asking rather than guessing, because the wrong choice is not a near miss: scoring a
live campaign ignores the results that are the whole answer, and diagnosing an unsent one
has no data to work from.

**Interactive mode opening question.** Ask exactly one thing before routing:

> Where are you starting from — do you already know precisely who you are targeting, or
> is narrowing that the job?

That single answer separates `offer` (most common real starting point) from `list`.

**When `full` runs**, execute the three sub-skills in order, passing artifacts forward,
then assemble `campaign-brief.md` from `assets/templates/campaign-brief.md`. Run the
validators after each stage and stop on errors rather than carrying a broken spec
downstream.

## Is Outbound Even the Right Motion?

This skill assumes outbound is the answer. Ask once, at intake, whether it is — because
the alternative is finding out three weeks into domain warmup, or after
`gtm_math.py economics` shows the campaign loses money on every deal it wins.

Outbound is one of seven motions: inbound, outbound, paid, community, partners, ABM, and
product-led. Four checks decide whether this is the right one:

| Check | Outbound fits when | Reconsider when |
|---|---|---|
| **ACV vs cost to acquire** | ACV comfortably exceeds infrastructure, data and labour per won deal | Low ACV or self-serve pricing — the economics rarely close |
| **Buyer is identifiable** | You can name titles and filter for them | The buyer is a long tail you cannot enumerate |
| **Problem is already known to them** | They would recognise it when named | You must educate the market first — that is content, not cold email |
| **TAM supports the goal** | `gtm_math.py size --tam` clears | The goal exceeds the market at any reply rate |

**Say plainly when outbound is the wrong instrument**, and name what fits better:

- **Low ACV, self-serve, high volume** → product-led. Outbound cannot pay for itself.
- **Very high ACV, few accounts** → ABM. A handful of accounts deserves depth this skill's
  volume machinery is the wrong shape for.
- **Buyer does not know the problem exists** → inbound or community first. Cold email is
  bad at teaching.
- **An engaged audience or user base already exists** → work those engagement signals
  before cold ones. See `references/signals-and-triggers.md` — warmer, and free.

Thirty seconds, not a strategy engagement. If outbound fits, say so and move on. Where it
does not, say that **before any list gets built** — a campaign that should never have run
is the most expensive thing this skill can produce.

## Check Geography Before Applying Any Default

Every threshold in this skill — reply rates, verification pass rates, sending schedule,
sales-cycle length — is calibrated on North American and European outbound.

**If the target list includes Saudi Arabia, the UAE, Egypt, or the wider Gulf, load
`references/gcc-market.md` before sizing, sourcing, or scheduling anything.** Several
defaults are wrong there and fail silently: contact-data coverage is a fraction of
Western levels, the working week is Sunday to Thursday, Ramadan and Eid flatten reply
rates, and language should be segmented per contact rather than assumed from country.

Ask which geography the campaign targets during intake. It changes more than the copy.

## Non-Negotiable Quality Gates

These fail the deliverable. Do not hand over work that violates them.

1. **Email 1 stays under 80 words in its longest spintax variant.** Enforced by
   `validate_spintax.py --max-words 80`, which computes the worst case, not the first
   variant written.
2. **Every merge tag has a producing column.** Enforced by
   `validate_spintax.py --vars clay-table.json`. A tag with no column renders blank to
   the whole list.
3. **Email 1 contains no pitch, no calendar link, and no meeting ask.** It ends on an
   open question. Enforced by `score_message.py`, which classifies CTA friction and
   flags banned openers, sender-focused copy, and missing specificity.
4. **The enrichment waterfall runs cheap providers first, and every step after the first
   is gated on the previous one returning empty.** Enforced by `clay_taxonomy.py`.
5. **No campaign ships without a verification stage.** Bounce ladder: under 2% healthy,
   above 2% elevated, above 3% danger — the domain comes out of rotation, above 4%
   triggers provider throttling. Enforced by `diagnose_campaign.py` and warned by
   `gtm_math.py` above 3%.
6. **All arithmetic goes through `gtm_math.py`.** Never compute list sizes, CAC, or
   significance in prose — this is the single highest-risk place for a plausible-looking
   wrong number.
7. **The jurisdiction gate and suppression list exist before the list does.** Run
   `references/compliance-gates.md` (geography → consent model → artifacts) and build the
   suppression list per `references/suppression-mechanics.md` before sourcing. A campaign
   that cannot name its consent basis does not get a domain, let alone a send.

## Scripts

Run these rather than reasoning about their output:

```bash
python scripts/validate_spintax.py SEQUENCE.md --vars clay-table.json --max-words 80
```

```bash
python scripts/score_message.py SEQUENCE.md --vars allowed_vars.json
```

```bash
python scripts/gtm_math.py size --meetings-goal 10 --reply-rate 5 --positive-rate 25 --tam 40000
```

```bash
python scripts/clay_taxonomy.py generate --waterfall leadmagic,findymail,prospeo --personalize case_study_result -o clay-table.json
```

`clay_taxonomy.py vars clay-table.json` emits the allowed-variable file that
`validate_spintax.py --vars` consumes. That handoff is what closes the loop between the
data layer and the copy layer.

## Handling Assumptions the User Has Not Given

Outbound planning needs numbers the user usually does not have on hand (reply rate,
close rate, ACV). Do not stall on them.

- State a default explicitly, flag it as an assumption, and continue.
- Defaults that hold up for cold B2B: 3-5% reply rate (per delivered, platform-skewed —
  always state the denominator, see `references/gtm-benchmarks.md`), 20-30% of replies
  positive, 60% of positives booking, 4-step sequence, and sends sized against the
  **per-domain ceiling of roughly 40/day** (30-50 band) — not the 25/inbox/day figure,
  which three mailboxes easily multiply past the ceiling. `gtm_math.py` sizes domains
  from daily volume for exactly this reason.
- Re-run the model with the user's real numbers the moment they arrive. `gtm_math.py`
  makes this a one-line change, so never treat the first model as final.
- `gtm_math.py` flags assumptions that are outside plausible ranges. Surface those
  warnings rather than burying them — an optimistic reply rate silently inflates every
  downstream number.

## Reference Files

Load on demand. Do not read these at activation.

| File | Load when |
|---|---|
| `references/value-equation.md` | Scoring or rewriting an offer |
| `references/icp-filters.md` | Building Sales Navigator or Apollo filter sets |
| `references/signals-and-triggers.md` | Choosing the trigger the campaign is built on |
| `references/sourcing-channels.md` | Choosing where to scrape a list from |
| `references/waterfall-enrichment.md` | Designing provider routing and verification |
| `references/clay-frameworks.md` | Ordering Clay columns, or writing any prompt that runs per row |
| `references/clay-credits.md` | Classifying columns free vs paid, or auditing an expensive table |
| `references/clay-sources.md` | Choosing a Clay-native source before reaching for a scraper |
| `references/clay-recovery.md` | A corner piece will not resolve, or an enrichment comes back mostly empty |
| `references/clay-tables.md` | One row becoming many, joining tables, or HTTP API |
| `references/copy-frameworks.md` | Writing or reviewing sequence copy — the five blocks, structures, spintax |
| `references/personalization-depth.md` | Writing an observation line, or judging whether a detail is appropriate to use |
| `references/cta-design.md` | Designing the ask, or when diagnosis points at CTA friction |
| `references/gcc-market.md` | **Any list including Saudi, UAE, Egypt, or the Gulf** |
| `references/buying-committee.md` | Multi-threading accounts above ~30 staff |
| `references/objection-library.md` | Handling a specific objection in a reply |
| `references/cold-call.md` | Adding phone to the cadence, or writing call openers |
| `references/deliverability.md` | Inbox, warmup, domain, DNS, and bulk-sender compliance |
| `references/gtm-benchmarks.md` | Judging whether a number is good or bad |
| `references/gtm-math.md` | Interpreting or explaining calculator output |
| `references/mcp-integration.md` | Pulling live campaign or reply data instead of a CSV |
| `references/compliance-gates.md` | **Before any list build** — jurisdiction, consent model, required artifacts |
| `references/suppression-mechanics.md` | Building or syncing the suppression list; handling opt-outs and not-now re-entry |
| `references/multichannel-orchestration.md` | Combining email, LinkedIn, phone, and video into one cadence; conditional branching |
| `references/linkedin-playbook.md` | Low connection-acceptance, profile optimization, InMail, the LinkedIn acceptance funnel |
| `references/ai-sdr-positioning.md` | Manual vs AI-assisted vs AI-SDR-agent decision; build-vs-buy |

## Sub-Skills

| Sub-skill | Owns |
|---|---|
| `gtm-outbound-offer` | Value Equation scoring, sub-niche selection, filters, UVP |
| `gtm-outbound-list` | Sourcing channels, provider routing, verification, list attrition |
| `gtm-outbound-clay` | Clay table construction: column order, credit class, prompts, cross-table, HTTP API |
| `gtm-outbound-copy` | Poke the Bear sequences, spintax, Smartlead configuration |
| `gtm-outbound-math` | List sizing, inbox count, unit economics, A/B significance |
| `gtm-outbound-score` | 100-point launch readiness scoring and hard gates |
| `gtm-outbound-diagnose` | Post-launch failure diagnosis, layer routing, suppression of premature fixes |
| `gtm-outbound-reply` | Reply classification, objection handling, booking motion |

## Templates

`assets/templates/` holds the output shapes: `icp-blueprint.md`, `list-spec.md`,
`sequence.md`, `campaign-brief.md`, and `reply-drafts.md` (worked reply drafts for every
classification the reply skill produces — fill, never auto-send). Fill these rather than
inventing a structure per run — consistent artifacts are what make the chain readable
across sessions.

## The Skill Never Sends

Optional MCP connectors may be used to **read** live campaign stats and replies. They are
never used to send, launch, resume, or push a sequence live.

Sending is irreversible, outward-facing, and operates at scale — a wrong campaign id or an
unfiltered list reaches thousands of real people with no recall. Produce the configuration
and hand it over. A general instruction like "set up my campaign" authorises building it,
not transmitting it.

Every workflow must also work with local files alone. Never block on a missing connector.

## Scope Boundary

This skill engineers cold outbound to business contacts. It does not write consumer
email marketing to opted-in lists (different regulatory footing, different mechanics),
and it does not assist with evading spam filtering, disguising sender identity, or
sending to scraped consumer personal addresses. Cold B2B outbound has real compliance
obligations that vary by jurisdiction — CAN-SPAM, GDPR legitimate interest, CASL. When a
campaign targets EU or Canadian recipients, say so plainly and recommend the user confirm
their basis with counsel rather than asserting that a given approach is compliant.
