# Installing gtm-outbound

A B2B outbound campaign engineering skill set for Claude Code. Nine skills, one agent,
26 reference files, six Python scripts, nine templates.

## Requirements

| | |
|---|---|
| **Claude Code** | Any recent version. Also works with Codex, Cursor, OpenCode, and 60+ other agents via the same installer |
| **Node 18+** | For `npx` — the installer runs through it |
| **Python** | 3.10 or newer, on PATH — needed by the six scripts inside the skills |
| **Dependencies** | **None.** Standard library only — no pip install, no virtualenv |
| **Network** | Not required after install. Everything runs locally on files you provide |
| **Disk** | Under 1 MB |

Optional: an MCP connector for your sending platform (Smartlead, Instantly) lets the
diagnose and reply workflows pull live data instead of a CSV export. Everything works
without it.

## Install

One command — no clone needed:

```bash
npx skills add MostaDaoud/gtm-outbound
```

This is the [open agent skills](https://agentskills.io) installer. It discovers the nine
skills and asks where to put them. To install globally (available in every project):

```bash
npx skills add MostaDaoud/gtm-outbound -g
```

Useful variants:

```bash
npx skills add MostaDaoud/gtm-outbound --list          # see the skills without installing
npx skills add MostaDaoud/gtm-outbound --skill gtm-outbound-math   # install one only
npx skills add MostaDaoud/gtm-outbound --agent claude-code -g      # skip the prompts
```

### 1. Check the machine can run it

```bash
python preflight.py
```

Verifies the Python version, confirms every file is present, executes all six scripts,
and checks one calculation returns the right answer. It tests rather than assumes — if
this passes, the skill will work.

### 2. The researcher agent

The offer skill can delegate per-account research to a bundled agent. The skills
installer copies it inside the skill folder; to register it with Claude Code's agent
runner, copy it in:

```bash
cp ~/.claude/skills/gtm-outbound/agents/gtm-outbound-researcher.md ~/.claude/agents/
```

Optional — everything else works without this step.

### 3. Restart Claude Code

Skills are loaded at session start. A running session will not see them.

### 4. Confirm

Start a new session and type:

```
/gtm-outbound math
```

If it responds, you are done. If nothing happens, see Troubleshooting.

## What Gets Installed

```
~/.claude/skills/
├── gtm-outbound/          orchestrator + references + scripts + templates + agent
├── gtm-outbound-offer/    Value Equation, sub-niche, filters, UVP
├── gtm-outbound-list/     sourcing channels, provider routing, verification
├── gtm-outbound-clay/     Clay table construction, credit class, prompts
├── gtm-outbound-copy/     sequences, spintax, sending config
├── gtm-outbound-math/     list sizing, CAC, payback, A/B significance
├── gtm-outbound-score/    100-point pre-launch readiness gate
├── gtm-outbound-diagnose/ post-launch failure diagnosis
└── gtm-outbound-reply/    reply triage, objections, booking
```

The installer backs up any existing install (`npx skills remove` undoes it cleanly).
Nothing else on your machine is touched — no global config, no PATH changes, no
services.

## First Run

Three entry points depending on where you are:

| Situation | Command |
|---|---|
| Starting from nothing | `/gtm-outbound` — it asks one question and routes |
| Have a campaign running badly | `/gtm-outbound diagnose export.csv` |
| Just want a number | `/gtm-outbound math` |

The full chain is `offer → list → copy`, and each stage writes a file the next one reads.

## Uninstall

```bash
npx skills remove
```

Restart Claude Code afterwards.

## Troubleshooting

**The skill does not respond to `/gtm-outbound`**
Skills load at session start — restart Claude Code. If it still does not appear, confirm
the directories landed in `~/.claude/skills/` and that each contains a `SKILL.md`.

**`python: command not found` during preflight**
The skill files still install correctly; only the scripts need Python. Install Python 3.10+
and re-run `preflight.py`. On some systems the command is `python3`.

**A script fails with a syntax error**
Almost always a Python below 3.10. Check with `python --version`. If you have both, the
scripts run under whichever `python` resolves first on PATH.

**A skill collides with something already installed**
If the recipient already runs skills with overlapping names or descriptions, activation
becomes ambiguous. `_evals/collision_check.py` measures this:

```bash
python _evals/collision_check.py --installed ~/.claude/skills --candidate skills
```

Anything scoring above 0.35 against an existing skill will compete for the same prompts.

## Notes for the Recipient

**All numbers are defaults, not laws.** Reply rates, bounce thresholds, sending volumes,
provider cost tiers — these are calibrated starting points. Replace them with your own
data as it accumulates. The provider tiers in `clay_taxonomy.py` in particular should be
edited to match your contracted rates.

**Targeting the Gulf or wider MENA?** Read `skills/gtm-outbound/references/gcc-market.md`
before anything else. Several defaults in this skill are Western-calibrated and wrong
there, and they fail quietly rather than loudly.

**The skill never sends.** It produces configurations, sequences, and specifications. A
human sends them. That boundary is deliberate and should stay.

## Attribution

Frameworks are re-expressed with sources credited inline. Portions adapt material from
[coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT),
a GTM course, and a GTM strategy book. No source text is reproduced.
