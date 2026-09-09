# Skill Plan: gtm-outbound

## Overview

- **Domain**: B2B GTM / outbound campaign engineering (email + LinkedIn)
- **Tier**: 3 (multi-skill orchestrator) + scripts layer
- **Sub-skills**: 4
- **Scripts**: 3
- **Reference files**: 7
- **Asset templates**: 4
- **Agents**: 0 (workflows are sequential; no parallel fan-out justified)

**Name rationale**: `gtm-outbound` — kebab-case, no reserved words, no collision with the
68 installed skills. Reads naturally in both `/gtm-outbound` and sub-skill form
(`/gtm-outbound offer`). Avoids `outbound-architect` because "architect" is a verb users
type, not a noun they'd invoke.

---

## The Core Architectural Decision: Artifact Chaining

The three workflows are sequential but must also run standalone. Solution: each sub-skill
**writes a durable artifact** and **reads the previous artifact if present**, otherwise
prompts for the minimum viable inputs.

```
Workflow 1  ──►  ICP-BLUEPRINT.md  +  icp.json
                        │
                        ▼  (read: sub-niche, filters, UVP, case-study angles)
Workflow 2  ──►  LIST-SPEC.md      +  clay-table.json
                        │
                        ▼  (read: enrichment variables available for personalization)
Workflow 3  ──►  SEQUENCE.md       +  smartlead-config.json
```

This is what makes it Tier 3 rather than three unrelated Tier 2 skills. The JSON siblings
are the machine-readable handoff; the `.md` files are the human deliverable.

**Critical constraint enforced by the chain**: Workflow 3 may only write personalization
variables that Workflow 2's `clay-table.json` actually produces. A `{{case_study_result}}`
merge tag in the copy that no Clay column populates is the single most common failure mode
in real outbound builds — the chain makes it structurally detectable, and the spintax
validator enforces it.

---

## Use Cases

### UC1 — Offer & ICP Packaging
- **Trigger**: "build a GTM campaign blueprint", "narrow my ICP", "package my offer",
  "who should I target for [product]"
- **Steps**:
  1. Intake raw offer (what you sell, to whom, proof you have).
  2. Map to Value Equation — Dream Outcome and Perceived Likelihood (numerator),
     Time Delay and Effort/Sacrifice (denominator). Score each 1–5, identify the weakest
     lever, rewrite the offer to attack it.
  3. Decompose broad market → sub-niche (industry × trigger event × company stage).
  4. Build searchable filter sets: **Company Level** (headcount bands, tech stack,
     geo, funding, hiring signals) and **Contact Level** (title strings, seniority,
     tenure, department) — plus **Exclusion Keywords**.
  5. Formulate UVP hypothesis via Steve Blank: "We help [X] achieve [Y] by [Z]".
- **Result**: `ICP-BLUEPRINT.md` + `icp.json`
- **Anti-patterns enforced**: no "all CEOs", no estimated-revenue filters (low accuracy,
  inferred not observed), no filter set that returns >50k or <500 results without a flag.

### UC2 — Technical List & Sourcing Spec
- **Trigger**: "engineer a Clay outbound workflow for [audience]", "how do I build this
  list", "design the enrichment waterfall", "scrape [source]"
- **Steps**:
  1. Select sourcing channels by TAM size and ICP type (Clutch → agencies,
     Storeleads → Shopify brands, PhantomBuster → LinkedIn post commenters/event
     attendees, job boards → hiring-signal plays, G2/Capterra → software buyers).
  2. Design domain resolution + Claygent/Neon web-scrape prompts to extract
     hyper-personalization variables (actual customer case studies, positioning claims,
     recent launches).
  3. Design the waterfall enrichment routing (cheap-and-broad → expensive-and-accurate)
     with credit-preservation ordering and conditional gating.
  4. Define validation criteria via MillionVerifier; target bounce rate <4%.
  5. Emit the Clay table schema as JSON (columns → provider → input mapping → output
     field → Smartlead custom field).
- **Result**: `LIST-SPEC.md` + `clay-table.json`
- **Script**: `clay_taxonomy.py` generates and validates the JSON schema.

### UC3 — Spintax Copy & Deliverability Setup
- **Trigger**: "draft a Poke the Bear copy sequence", "write the outbound emails",
  "set up a Smartlead deliverability spec", "spintax my sequence"
- **Steps**:
  1. Write Email 1 with Poke the Bear: observation → open-ended pain question. No pitch,
     no calendar link, no "quick call" in email 1.
  2. Hard limit: under 80 words. Enforced, not suggested.
  3. Embed spintax across greeting / body / CTA. Generate soft-CTA and hard-CTA arms as
     a testable pair rather than picking one.
  4. Write the follow-up cadence and the LinkedIn parallel track.
  5. Produce the Smartlead spec: sends/inbox/day, warmup duration and volume, ramp-up
     increment, randomization, warmup reply rate, plus SPF/DKIM/DMARC and domain
     strategy.
- **Result**: `SEQUENCE.md` + `smartlead-config.json`
- **Script**: `validate_spintax.py` — hard gate before the artifact is written.

### UC4 — GTM Math & Budget Modeling
- **Trigger**: "how many leads do I need for [N] meetings", "how many inboxes",
  "what's my outbound payback period", "is this A/B test significant"
- **Steps**:
  1. Back-solve required list size and inbox count from a target meeting/positive-reply
     goal and assumed funnel rates.
  2. Compute cost per positive reply, CAC, payback period.
  3. Compute A/B sample size for a target lift at a given confidence and power, and
     evaluate an in-flight test for significance before scaling.
- **Result**: inline model table + optional `campaign-math.json`
- **Script**: `gtm_math.py` — all arithmetic, zero LLM math.

---

## Complexity Tier Assessment

| Signal | Assessment |
|---|---|
| Use cases | 4 distinct → Tier 3 |
| Needs scripts | Yes, 3 → pushes above Tier 3 baseline |
| Sub-skills needed | Yes, 4 |
| Parallel execution | **No** — workflows are strictly sequential and each depends on the prior artifact |
| Reference docs | Yes, 7 |
| Industry templates | Yes, 4 asset templates |

**Verdict: Tier 3 + scripts layer.** Not Tier 4 — Tier 4 is justified by parallel subagent
fan-out (like `seo-audit` delegating to 15 specialists simultaneously). Here the
dependency chain is linear, so agents would add context-handoff cost and buy nothing.

---

## Architecture

```
gtm-outbound/                          # Orchestrator — routing + intake + chain state
  SKILL.md
  references/
    value-equation.md                  # Hormozi scoring rubric, offer rewrite patterns
    icp-filters.md                     # Sales Nav + Apollo filter taxonomy, exclusions
    sourcing-channels.md               # Channel → ICP-type → tool → extraction method
    waterfall-enrichment.md            # Provider routing, credit logic, verification
    copy-frameworks.md                 # Poke the Bear, CTA theory, spintax conventions
    deliverability.md                  # Smartlead config, warmup, DNS, domain strategy
    gtm-math.md                        # Formula definitions the calculator implements
  scripts/
    validate_spintax.py                # Syntax gate: braces, pipes, merge tags, nesting
    gtm_math.py                        # List sizing, CAC/payback, A/B sample size
    clay_taxonomy.py                   # Clay table schema JSON generator + validator
  assets/templates/
    icp-blueprint.md
    list-spec.md
    sequence.md
    campaign-brief.md                  # Combined deliverable across all three

gtm-outbound-offer/SKILL.md            # UC1 — strategy layer
gtm-outbound-list/SKILL.md             # UC2 — data layer
gtm-outbound-copy/SKILL.md             # UC3 — execution layer
gtm-outbound-math/SKILL.md             # UC4 — modeling layer (thin wrapper over script)
```

Flat sibling layout matches the installed convention on this machine (`blog` + `blog-write`,
`seo` + `seo-audit`), so sub-skills are independently invocable via the Skill tool.

---

## Sub-Skill Decomposition

### `gtm-outbound-offer`
- **Responsibility**: Broad offer → specific problem, specific sub-niche, specific mechanism.
- **Inputs**: Raw offer description, existing customers/proof, current targeting (if any).
- **Outputs**: `ICP-BLUEPRINT.md`, `icp.json`
- **References**: `value-equation.md`, `icp-filters.md`
- **Standalone**: Yes — this is the chain head.

### `gtm-outbound-list`
- **Responsibility**: Sourcing + enrichment pipeline design that doesn't burn credits.
- **Inputs**: `icp.json` if present; else sub-niche + filters prompted inline.
- **Outputs**: `LIST-SPEC.md`, `clay-table.json`
- **References**: `sourcing-channels.md`, `waterfall-enrichment.md`
- **Scripts**: `clay_taxonomy.py`
- **Standalone**: Yes, with degraded personalization depth if `icp.json` is absent.

### `gtm-outbound-copy`
- **Responsibility**: Poke the Bear sequences, spintax, deliverability spec.
- **Inputs**: `icp.json` + `clay-table.json` if present; else prompted.
- **Outputs**: `SEQUENCE.md`, `smartlead-config.json`
- **References**: `copy-frameworks.md`, `deliverability.md`
- **Scripts**: `validate_spintax.py` (blocking gate)
- **Standalone**: Yes, but warns that merge tags cannot be verified against a real Clay
  schema and marks them unvalidated.

### `gtm-outbound-math`
- **Responsibility**: All numeric modeling.
- **Inputs**: Goal (meetings/month), assumed funnel rates, ACV, cost inputs.
- **Outputs**: Model table, optional `campaign-math.json`
- **References**: `gtm-math.md`
- **Scripts**: `gtm_math.py`
- **Standalone**: Yes — fully independent, callable mid-campaign.

---

## Routing

| Command | Routes to | Purpose |
|---|---|---|
| `/gtm-outbound` | orchestrator | Interactive full-chain build |
| `/gtm-outbound offer` | `gtm-outbound-offer` | UC1 — ICP + Value Equation |
| `/gtm-outbound list` | `gtm-outbound-list` | UC2 — sourcing + Clay waterfall |
| `/gtm-outbound copy` | `gtm-outbound-copy` | UC3 — spintax + Smartlead |
| `/gtm-outbound math` | `gtm-outbound-math` | UC4 — sizing, CAC, significance |
| `/gtm-outbound validate <file>` | script direct | Spintax lint on an existing sequence |
| `/gtm-outbound full` | orchestrator | Run 1→2→3 end-to-end, emit `campaign-brief.md` |

---

## Description Field (draft — the highest-leverage field in the skill)

```
Engineers B2B outbound email and LinkedIn campaigns end-to-end: narrows a broad offer
into a targeted sub-niche using the Value Equation, designs Sales Navigator and Apollo
filter sets with exclusion keywords, specs Clay and Apollo waterfall enrichment pipelines
with scraper sourcing (Clutch, Storeleads, PhantomBuster, Claygent), writes sub-80-word
"Poke the Bear" email sequences with validated spintax, and produces Smartlead
deliverability and warmup configurations. Also models list sizing, inbox count, CAC,
payback period, and A/B test significance. Use when the user says "architect an outbound
campaign", "build a GTM campaign blueprint", "engineer a Clay outbound workflow", "draft
a Poke the Bear copy sequence", "set up a Smartlead deliverability spec", "narrow my ICP",
"waterfall enrichment", "spintax", "cold email sequence", "how many leads do I need", or
asks about outbound list building, lead sourcing, or email deliverability setup.
```

~870 chars — under the 1024 limit. Contains WHAT + WHEN + tool-name keywords (Clay,
Apollo, Smartlead, Sales Navigator, PhantomBuster, Storeleads, Clutch, Claygent,
MillionVerifier) which are the highest-signal activation tokens in this domain.

---

## Reference File Planning

| File | Contents | Est. lines |
|---|---|---|
| `value-equation.md` | 4-lever scoring rubric, weak-lever diagnosis, offer rewrite patterns, UVP formula + worked examples | ~120 |
| `icp-filters.md` | Company-level and contact-level filter taxonomy, exclusion keyword library, filter anti-patterns, result-count sanity bands | ~150 |
| `sourcing-channels.md` | Channel table (source → ICP fit → tool → extraction method → typical yield), TAM-based selection logic | ~140 |
| `waterfall-enrichment.md` | Provider routing order, conditional gating, credit preservation, verification thresholds, bounce-rate targets | ~130 |
| `copy-frameworks.md` | Poke the Bear anatomy, observation sourcing, question construction, soft vs hard CTA, word budget, spintax conventions and nesting rules | ~160 |
| `deliverability.md` | Smartlead numeric config, warmup schedule, ramp-up, domain/DNS setup, infrastructure sizing | ~120 |
| `gtm-math.md` | Formula definitions mirroring `gtm_math.py`, so outputs are interpreted correctly | ~90 |

---

## Script Contracts

### `validate_spintax.py`
```
Input:  path to sequence file (md/txt/json) or --stdin
Checks: balanced braces; no unclosed pipes; no empty spintax options; no nested
        spintax beyond depth limit; merge tags match allowed variable list
        (--vars from clay-table.json); variant count explosion warning;
        word count per email against --max-words
Output: exit 0 clean / exit 1 with line-anchored error list; --json for machine use
```

### `gtm_math.py`
```
Subcommands:
  size     --meetings-goal --reply-rate --positive-rate --meeting-rate --sends-per-inbox-day
           → required list size, sends/day, inbox count, domain count, days to complete
  economics --acv --gross-margin --cost-inbox --cost-data --cost-tooling --closed-won-rate
           → cost per positive, CAC, payback months, ROI
  ab       --baseline-rate --min-detectable-lift --confidence --power
           → required sample size per arm
  ab-eval  --a-sends --a-conv --b-sends --b-conv --confidence
           → p-value, significant yes/no, do-not-scale warning
Output: human table by default, --json for chaining
```

### `clay_taxonomy.py`
```
Input:  --icp icp.json, --sources <list>, --enrichment-waterfall <ordered providers>
Output: clay-table.json — column name, type, provider, input mapping, output field,
        run condition, Smartlead custom-field target
Validates: no orphan columns, every Smartlead merge field has a producing column,
           waterfall providers ordered cheap→expensive, conditional gates present
```

---

## Two Flags Before Build

1. **Vendor and pricing specifics will age.** Provider coverage, per-credit costs, and
   platform limits shift on a quarterly cadence. The reference files will encode *routing
   logic and decision criteria* as the durable layer, with vendor tables clearly marked as
   user-updatable defaults rather than baked-in truth. Proceeding on that basis.

2. **The Smartlead numbers you specified are treated as configured defaults, not laws.**
   25 sends/inbox/day, 14-day minimum warmup, 40 warmup/day, ramp-up 5, 30–40% warmup
   reply rate — these ship as the default profile in `deliverability.md`, overridable per
   campaign, with the reasoning stated so they can be adjusted as ESP behavior changes.

---

## Next Steps

Run `/skill-forge build gtm-outbound` to scaffold.
