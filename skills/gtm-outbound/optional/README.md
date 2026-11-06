# Optional tooling

**Nothing in this folder is required. The core skill set remains zero-dependency:
standard-library Python only, no `pip install`, no network.**

This directory holds Node/TypeScript helpers adapted from
[coldoutboundskills](https://github.com/growthenginenowoslawski/coldoutboundskills)
(MIT — see `NOTICE` at the repo root). They automate the parts of outbound that genuinely
require talking to an API: buying domains, provisioning inboxes, setting warmup, checking
authentication, running spam tests, exporting leads, uploading DRAFT campaigns.

They are quarantined here for one reason: they break the dependency promise if they leak
into the core.

## Requirements

| | |
|---|---|
| Node | 18 or newer |
| Runner | `npx tsx` (or install `tsx` globally) |
| API keys | Per script — see `.env.example` at the repo root |
| Network | Required |

## Why they are separate

`preflight.py` smoke-tests the six core Python scripts and asserts a stdlib-only
environment. It deliberately **does not** cover this folder. Including TypeScript here
would make a clean install fail for everyone who only wants the reasoning layer, so the
scripts live behind an explicit opt-in.

## Layout

```
optional/scripts/<upstream-skill-name>/*.ts
```

Each subdirectory mirrors the upstream skill it came from, which keeps the provenance
obvious and avoids the filename collisions that a flat copy produces (three upstream
skills each ship a different `_lib.ts`).

## Using them without them

Every script here automates a decision that is documented in plain language in
`skills/gtm-outbound/references/`:

| Script area | Decision logic lives in |
|---|---|
| Domain purchase, inbox provisioning | `references/infra/domains.md` |
| Warmup, signatures, tagging | `references/infra/inbox-warmup.md` |
| Auth checks, spam tests, audits | `references/infra/deliverability-audit.md` |
| Lifecycle keep/cancel/promote/buy | `references/infra/inbox-lifecycle.md` |
| Lead export, list scoring | `references/list-lanes.md`, `references/list-qa.md` |
| Reply fetching and classification | `references/ops/reply-scoring.md` |

Read the reference, do it in the vendor UI, and skip the script. That is a supported path,
not a degraded one.

## Safety

Several of these scripts spend money (domain purchase) or touch live sending state
(warmup, campaign upload). Read a script before running it, and assume anything that
allocates real infrastructure is irreversible.
