# Cold Outbound Skills -> gtm-outbound: curated merge design

Status: in progress
Branch: `feat/cold-outbound-merge`
Source: https://github.com/growthenginenowoslawski/coldoutboundskills (MIT)
Target: https://github.com/MostaDaoud/gtm-outbound

## What each side actually is

**gtm-outbound** is a gated dependency chain: an always-loaded orchestrator routes to
eight thin sub-skills, and every piece of depth lives as an on-demand reference under
`skills/gtm-outbound/references/`. Stages write artifacts (`icp.json`,
`clay-table.json`) that the next stage validates against. It refuses to send anything.
It has zero runtime dependencies.

**coldoutboundskills** is 51 flat, task-scoped skills across six tracks. It is strong
exactly where gtm-outbound is empty: sending infrastructure, deliverability operations,
and 19 per-signal personalization playbooks. It is weaker where gtm-outbound is strong:
no artifact contract, no scoring gate, no campaign math.

## Architecture decision

Do **not** vendor 51 skill folders in. That would produce two competing orchestrators,
~60 skills, and duplicated ICP/list/copy logic.

Instead, follow the target's existing shape: **thin sub-skills route; references carry
depth.** Cold content is transformed into reference files, and only genuinely new
capability gets a new sub-skill.

### New sub-skills (3)

| Skill | Covers | Why it cannot fold into an existing one |
|---|---|---|
| `gtm-outbound-infra` | Domain purchase, inbox provisioning, warmup, auth audit, incident triage, fleet lifecycle | gtm-outbound has no sending-infrastructure coverage at all |
| `gtm-outbound-signals` | 19 buying-signal playbooks, one copy-ready sentence each | gtm has `personalization-depth.md` (how deep) but no per-signal recipes (what to say) |
| `gtm-outbound-ops` | Weekly Mon/Wed/Fri rhythm, positive-reply scoring, inbox-type testing | gtm is launch-shaped; this is the steady-state operating loop |

### Folds into existing skills (no new skill, depth added to references)

| Cold skill | Folds into |
|---|---|
| `icp-onboarding`, `campaign-strategy`, `lead-magnet-brainstorm` | `gtm-outbound-offer` |
| `list-builder`, `list-expander`, `perfect-company-list`, `list-quality-scorecard`, `icp-prompt-builder`, `blitz-list-builder`, `google-maps-list-builder`, `disco-like`, `competitor-engagers`, `prospeo-full-export` | `gtm-outbound-list` |
| `campaign-copywriting`, `spam-word-checker`, `smartlead-spintax`, `smartlead-campaign-upload` | `gtm-outbound-copy` |
| `experiment-design` | `gtm-outbound-math` |
| `personalization-subagent-pattern` | `gtm-outbound-signals` + orchestrator agent |
| `positive-reply-scoring`, `deliverability-test-public` | `gtm-outbound-ops` |
| `cold-email-kickoff` routing | orchestrator routing table |
| `smartlead-api`, `prospeo-search-api` | `references/api/` |

### Deliberately excluded

- **`auto-research-public`** — it launches campaigns autonomously. That contradicts
  gtm-outbound's stated rule that the skill never sends anything itself. Excluded by
  design, documented so the decision is visible.
- **All 525 MB of bundled lead CSVs** (426 MB Google Maps, 74 MB SaaS, 24 MB Shopify).
  Excluded from the repo; documented with upstream download pointers instead.
- **TypeScript scripts** stay out of the zero-dependency core. They move to
  `skills/gtm-outbound/optional/` with their own README, explicitly outside
  `preflight.py` and the no-dependency promise.

## The dependency promise is preserved

gtm-outbound's contract is: stdlib-only Python, no pip install, no network, under 1 MB.
The merge must not break it. Therefore:

- Core references stay Markdown.
- Core scripts stay stdlib Python.
- Any Node/TypeScript + API-key tooling lives under `optional/`, is never imported by a
  core skill, and is excluded from `preflight.py`.

## Directory changes

```
skills/gtm-outbound/
  references/
    infra/            domains.md inbox-warmup.md deliverability-audit.md
                      deliverability-incident.md inbox-lifecycle.md
    signals/          index.md + 19 playbook refs (+ their clay-table/clay-workflow)
    ops/              weekly-rhythm.md reply-scoring.md deliverability-testing.md
    api/              smartlead.md prospeo.md
    experiments.md  list-lanes.md  list-expansion.md  list-qa.md
    campaign-ideas.md  lead-magnets.md  spam-rules.md  personalization-subagent.md
  optional/           README.md scripts/*.ts
skills/gtm-outbound-infra/SKILL.md
skills/gtm-outbound-signals/SKILL.md
skills/gtm-outbound-ops/SKILL.md
docs/cold-merge/DESIGN.md
docs/cold-merge/LIST-SOURCES.md      (where the 525 MB of CSVs lives)
NOTICE                               (MIT attribution for the merged source)
```

Every merged skill is also mirrored to `.agents/skills/` to match the existing pattern.

## Verification gates

1. `python preflight.py` — all six core scripts still execute.
2. Frontmatter lint — every new `SKILL.md` has name, description, argument-hint.
3. Reference resolution — every reference path named in a SKILL.md exists on disk.
4. Mirror check — `skills/` and `.agents/skills/` hashes match.
5. skill-forge review -> evals -> benchmark -> evolve on the merged set.
