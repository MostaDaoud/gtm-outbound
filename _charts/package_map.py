#!/usr/bin/env python3
"""Regenerate _charts/package-map.txt from the real tree.

Line counts are read from disk, never typed. Descriptions are the only hand-written
part, and a file that gains or loses a description is reported as drift rather than
silently omitted -- the failure mode this replaces was a hand-drawn map listing 15
references when there were 21.
"""
import sys
from pathlib import Path

# The map is box-drawing characters; the Windows console defaults to cp1252 and
# raises on every one of them. The file itself is always written as UTF-8.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "gtm-outbound"
OUT = Path(__file__).parent / "package-map.txt"

NAME_END, NUM_W = 36, 5  # every count right-aligns to one absolute column, not per-prefix
DESC_COL = NAME_END + NUM_W + 3

REFERENCES = [
    ("strategy", [
        ("value-equation.md", "4-lever rubric · weakest-lever diagnosis · UVP form"),
        ("icp-filters.md", "filter taxonomy · exclusions · 3 hard rules"),
        ("signals-and-triggers.md", "signal to source map · decay windows"),
        ("buying-committee.md", "DMU roles · staggered threading above ~30 staff"),
    ]),
    ("sourcing and enrichment", [
        ("sourcing-channels.md", "channel table · trigger sources beat directories"),
        ("waterfall-enrichment.md", "cheap-first order · gating · verification"),
    ]),
    ("clay table construction", [
        ("clay-frameworks.md", "FETE · Jigsaw · SPICE prompt structure"),
        ("clay-credits.md", "free vs paid columns · cost-class ordering"),
        ("clay-sources.md", "Clay-native sources before reaching for a scraper"),
        ("clay-recovery.md", "corner piece won't resolve · empty enrichment"),
        ("clay-tables.md", "write-to-table · lookup · HTTP API · export"),
    ]),
    ("execution", [
        ("copy-frameworks.md", "5 blocks · 5 structures · spintax rules"),
        ("personalization-depth.md", "fact/inference/hypothesis · appropriateness line"),
        ("cta-design.md", "motivation x ability x prompt"),
        ("cold-call.md", "4-move opener · phone as a second signal"),
        ("deliverability.md", "warmup ladder · SPF/DKIM/DMARC · bulk-sender rules"),
        ("objection-library.md", "recurring objections · understand before countering"),
    ]),
    ("measurement and market", [
        ("gtm-benchmarks.md", "email + LinkedIn bands · what not to optimise"),
        ("gtm-math.md", "formulas mirroring the calculator"),
        ("gcc-market.md", "★ MENA: coverage gap · Sun-Thu · Ramadan · Zid/Salla"),
        ("mcp-integration.md", "live-data seam · read-only boundary"),
    ]),
]

SCRIPTS = [
    ("diagnose_campaign.py", "layer-ordered · email + LinkedIn · do-not-yet list"),
    ("validate_spintax.py", "2 dialects · worst-case word count · tag to schema"),
    ("gtm_math.py", "size (fwd/back) · economics · ab · ab-eval"),
    ("clay_taxonomy.py", "generate/validate/vars · ordering + gating rules"),
    ("score_message.py", "banned openers · hedging · CTA friction · specificity"),
    ("reply_classify.py", "deterministic triage · owns the opt-out call"),
]

TEMPLATES = [
    ("sequence.md", "both CTA arms · spintax inline · validator output"),
    ("campaign-score.md", "verdict · hard gates first · ranked fix list"),
    ("clay-build.md", "ordered columns · cost class · run condition"),
    ("reply-triage.md", "counts by type · suppression list · patterns"),
    ("list-spec.md", "channels · pipeline · credit logic · attrition"),
    ("diagnosis.md", "verdict and layer first · evidence · next action"),
    ("campaign-brief.md", "assembled by a full run"),
    ("icp-blueprint.md", "sub-niche · filters · UVP variants"),
]

SUBSKILLS = [
    ("gtm-outbound-offer", "value equation · sub-niche · filters · UVP"),
    ("gtm-outbound-list", "channels · provider routing · verification"),
    ("gtm-outbound-clay", "column order · credit class · prompts"),
    ("gtm-outbound-copy", "poke the bear · spintax · smartlead config"),
    ("gtm-outbound-math", "sizing · unit economics · A/B significance"),
    ("gtm-outbound-score", "100-point gate — has it NOT sent yet"),
    ("gtm-outbound-diagnose", "layer routing — has it ALREADY sent"),
    ("gtm-outbound-reply", "classification · objections · booking · handoff"),
]

drift: list[str] = []


def lines(path: Path) -> int:
    if not path.exists():
        drift.append(f"missing: {path.relative_to(ROOT)}")
        return 0
    return len(path.read_text(encoding="utf-8", errors="replace").splitlines())


def row(prefix: str, name: str, count: int, desc: str) -> str:
    left = f"{prefix}{name}".ljust(NAME_END)
    return f"{left}{count:>{NUM_W},} ─ {desc}".rstrip()


def header(prefix: str, name: str, total: int, desc: str) -> str:
    left = f"{prefix}{name}".ljust(NAME_END)
    return f"{left}{total:>{NUM_W},} ─ {desc}".rstrip()


def band(label: str, total: int) -> str:
    left = f"│   │  ╭─ {label.upper()} ".ljust(NAME_END - 1, "─")
    return f"{left} {total:>{NUM_W},} ─╮"


def audit(directory: Path, described: list[str], glob: str) -> None:
    actual = {p.name for p in directory.glob(glob)}
    for extra in sorted(actual - set(described)):
        drift.append(f"undescribed: {directory.relative_to(ROOT)}/{extra}")


out: list[str] = []
w = out.append

ref_files = [n for _, items in REFERENCES for n, _ in items]
audit(SKILL / "references", ref_files, "*.md")
audit(SKILL / "scripts", [n for n, _ in SCRIPTS], "*.py")
audit(SKILL / "assets/templates", [n for n, _ in TEMPLATES], "*.md")

ref_total = sum(lines(SKILL / "references" / n) for n in ref_files)
script_total = sum(lines(SKILL / "scripts" / n) for n, _ in SCRIPTS)
tpl_total = sum(lines(SKILL / "assets/templates" / n) for n, _ in TEMPLATES)
sub_total = sum(lines(ROOT / d / "SKILL.md") for d, _ in SUBSKILLS)

w("gtm-outbound/".ljust(NAME_END) + "  ★  ORCHESTRATOR — the only file always in context")
w("│")
w(row("├── ", "SKILL.md", lines(SKILL / "SKILL.md"),
      "routing table · artifact chain · 6 hard gates"))
w(" " * DESC_COL + "motion-fit and geography intake · NEVER-SENDS")
w("│")
w("├── agents/")
w(row("│   └── ", "gtm-outbound-researcher.md",
      lines(SKILL / "agents/gtm-outbound-researcher.md"),
      "the one parallel step · can return SUPPRESS"))
w("│")
w(header("├── ", "references/", ref_total,
         f"{len(ref_files)} files, loaded on demand only"))
for group, items in REFERENCES:
    w("│   │")
    w(band(group, sum(lines(SKILL / "references" / n) for n, _ in items)))
    for i, (name, desc) in enumerate(items):
        edge = "│   └── " if i == len(items) - 1 else "│   ├── "
        w(row(edge, name, lines(SKILL / "references" / name), desc))
w("│")
w(header("├── ", "scripts/", script_total, "run these, never reason about their output"))
for i, (name, desc) in enumerate(SCRIPTS):
    edge = "│   └── " if i == len(SCRIPTS) - 1 else "│   ├── "
    w(row(edge, name, lines(SKILL / "scripts" / name), desc))
w("│")
w(header("└── ", "assets/templates/", tpl_total,
         f"{len(TEMPLATES)} files, fill rather than invent a shape"))
for i, (name, desc) in enumerate(TEMPLATES):
    edge = "    └── " if i == len(TEMPLATES) - 1 else "    ├── "
    w(row(edge, name, lines(SKILL / "assets/templates" / name), desc))

w("")
w(header("", "gtm-outbound-*/", sub_total, "SIBLING SKILLS — one loads per route"))
for i, (name, desc) in enumerate(SUBSKILLS):
    edge = "└── " if i == len(SUBSKILLS) - 1 else "├── "
    w(row(edge, name + "/", lines(ROOT / name / "SKILL.md"), desc))

w("")
w("─" * 92)
total = (lines(SKILL / "SKILL.md") + lines(SKILL / "agents/gtm-outbound-researcher.md")
         + ref_total + script_total + tpl_total + sub_total)
w(f"9 skills · 1 agent · {len(ref_files)} references · {len(SCRIPTS)} scripts · "
  f"{len(TEMPLATES)} templates · {total:,} lines")

text = "\n".join(out) + "\n"
print(text)

# Print always, write only when clean. A map that disagrees with the tree is worse
# than no map -- it is the thing being replaced -- so never leave one on disk.
if drift:
    print("DRIFT — map and tree disagree, package-map.txt NOT written:", file=sys.stderr)
    for d in drift:
        print(f"  {d}", file=sys.stderr)
    sys.exit(1)

OUT.write_text(text, encoding="utf-8")
print(f"written to {OUT}")
