# Installing gtm-outbound

A B2B outbound campaign engineering skill set for Claude Code. Nine skills, one agent,
26 reference files, six Python scripts, nine templates.

## Requirements

| | |
|---|---|
| **Claude Code** | Any recent version. Skills also work in Cowork. |
| **Python** | 3.10 or newer, on PATH |
| **Dependencies** | **None.** Standard library only — no pip install, no virtualenv |
| **Network** | Not required. Everything runs locally on files you provide |
| **Disk** | Under 1 MB |

Optional: an MCP connector for your sending platform (Smartlead, Instantly) lets the
diagnose and reply workflows pull live data instead of a CSV export. Everything works
without it.

## Install

### 1. Check the machine can run it

```bash
python preflight.py
```

Verifies the Python version, confirms every file is present, executes all six scripts,
and checks one calculation returns the right answer. It tests rather than assumes — if
this passes, the skill will work.

### 2. Install

**macOS / Linux**

```bash
./install.sh --dry-run
```

```bash
./install.sh
```

**Windows**

```bash
pwsh -File install.ps1 -WhatIf
```

```bash
pwsh -File install.ps1
```

Both install to `~/.claude/skills/`. Both back up any existing directory to
`~/.claude/.skill-backups/<timestamp>/` rather than overwriting, so re-running is safe.

To install elsewhere: `./install.sh --dest /path/to/skills` or
`install.ps1 -DestinationRoot "D:\skills"`.

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
├── gtm-outbound/          orchestrator + references + scripts + templates
├── gtm-outbound-offer/    Value Equation, sub-niche, filters, UVP
├── gtm-outbound-list/     sourcing channels, provider routing, verification
├── gtm-outbound-clay/     Clay table construction, credit class, prompts
├── gtm-outbound-copy/     sequences, spintax, sending config
├── gtm-outbound-math/     list sizing, CAC, payback, A/B significance
├── gtm-outbound-score/    100-point pre-launch readiness gate
├── gtm-outbound-diagnose/ post-launch failure diagnosis
└── gtm-outbound-reply/    reply triage, objections, booking

~/.claude/agents/
└── gtm-outbound-researcher.md   parallel per-account research
```

Nothing outside `~/.claude/skills/` and `~/.claude/agents/` is touched. No global config, no PATH changes, no
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
rm -rf ~/.claude/skills/gtm-outbound ~/.claude/skills/gtm-outbound-* \n   ~/.claude/agents/gtm-outbound-*.md
```

```powershell
Remove-Item -Recurse -Force "$HOME/.claude/skills/gtm-outbound*"
```

Restart Claude Code afterwards.

## Troubleshooting

**The skill does not respond to `/gtm-outbound`**
Skills load at session start — restart Claude Code. If it still does not appear, confirm
the directories landed in `~/.claude/skills/` and that each contains a `SKILL.md`.

**`python: command not found` during install**
The skill files still install correctly; only the scripts need Python. Install Python 3.10+
and re-run `preflight.py`. On some systems the command is `python3`.

**A script fails with a syntax error**
Almost always a Python below 3.10. Check with `python --version`. If you have both, the
scripts run under whichever `python` resolves first on PATH.

**`install.sh: Permission denied`**
```bash
chmod +x install.sh
```

**Windows blocks the PowerShell script**
```bash
pwsh -ExecutionPolicy Bypass -File install.ps1
```

**A skill collides with something already installed**
If the recipient already runs skills with overlapping names or descriptions, activation
becomes ambiguous. `_evals/collision_check.py` measures this:

```bash
python _evals/collision_check.py --installed ~/.claude/skills --candidate .
```

Anything scoring above 0.35 against an existing skill will compete for the same prompts.

## Notes for the Recipient

**All numbers are defaults, not laws.** Reply rates, bounce thresholds, sending volumes,
provider cost tiers — these are calibrated starting points. Replace them with your own
data as it accumulates. The provider tiers in `clay_taxonomy.py` in particular should be
edited to match your contracted rates.

**Targeting the Gulf or wider MENA?** Read `gtm-outbound/references/gcc-market.md` before
anything else. Several defaults in this skill are Western-calibrated and wrong there, and
they fail quietly rather than loudly.

**The skill never sends.** It produces configurations, sequences, and specifications. A
human sends them. That boundary is deliberate and should stay.

## Attribution

Frameworks are re-expressed with sources credited inline. Portions adapt material from
[coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT),
a GTM course, and a GTM strategy book. No source text is reproduced.
