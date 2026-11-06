#!/usr/bin/env python3
"""Regenerate _charts/package-map.txt from the real tree.

Line counts are read from disk, never typed. Descriptions are the only hand-written
part, and a file that gains or loses a description is reported as drift rather than
silently omitted -- the failure mode this replaces was a hand-drawn map listing 15
references when there were 21.

v3.0.0: the tree moved under skills/, and the reference set split into subdirectories
(infra/, signals/, ops/, api/). Both are handled here; the audit is now recursive so a
new subdirectory cannot slip past it. Repetitive signal build files are aggregated into
explicit counted rows rather than enumerated 38 times, and the audit still checks them
file by file against the playbook list.
"""
import sys
from pathlib import Path

# The map is box-drawing characters; the Windows console defaults to cp1252 and
# raises on every one of them. The file itself is always written as UTF-8.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"          # sibling skills live here
SKILL = SKILLS / "gtm-outbound"   # the orchestrator package
OUT = Path(__file__).parent / "package-map.txt"

NAME_END, NUM_W = 36, 5  # every count right-aligns to one absolute column, not per-prefix
DESC_COL = NAME_END + NUM_W + 3

# ---------------------------------------------------------------------------
# Signal playbooks. The 19 names drive three files each: the playbook itself,
# a Clay table build and a Clay CLI workflow build. Those two build sets are
# aggregated in the map but audited file by file.
# ---------------------------------------------------------------------------
SIGNALS = [
    ("new-in-role", "start date · title change · rebuild window"),
    ("linkedin-engagement", "likers and commenters on a source account"),
    ("social-posts", "hook from their own most recent post"),
    ("warm-intros", "one hop from the client · say so"),
    ("fundraising", "round, date, investor · buying window"),
    ("hiring-surge", "department headcount growth in 6 months"),
    ("job-posting-language", "a clause from a live role"),
    ("ad-library", "what they run on Meta right now"),
    ("pricing-page", "public tiers · price points · feature edges"),
    ("case-study-page", "one named customer off their own page"),
    ("tech-on-website", "named tech verified on the live site"),
    ("google-site-search", "does their site mention this keyword"),
    ("company-name-cleaning", "the short form a person says aloud"),
    ("first-name-cleaning", "the greeting form, not the raw field"),
    ("social-link-finding", "verified official profile URLs"),
    ("lookalikes", "case study to companies that see themselves"),
    ("name-to-other-prospects", "right-fit colleague · no wrong-name risk"),
    ("ai-specificity", "the sentence that makes a generic offer specific"),
    ("creative-ideas", "three per-company bullets for a slot"),
]

REFERENCES = [
    ("strategy", [
        ("value-equation.md", "4-lever rubric · weakest-lever diagnosis · UVP form"),
        ("icp-filters.md", "filter taxonomy · exclusions · 3 hard rules"),
        ("signals-and-triggers.md", "signal to source map · decay windows"),
        ("buying-committee.md", "DMU roles · staggered threading above ~30 staff"),
        ("compliance-gates.md", "jurisdiction to consent model to required artifacts"),
        ("icp-intake.md", "long-form interview · when the ICP has no words yet"),
        ("campaign-ideas.md", "15-25 angles · raw material, not a substitute for narrowing"),
        ("lead-magnets.md", "free hook selection · what to give away"),
    ]),
    ("sourcing and enrichment", [
        ("sourcing-channels.md", "channel table · trigger sources beat directories"),
        ("waterfall-enrichment.md", "cheap-first order · gating · verification"),
        ("list-lanes.md", "one-command lanes · snowball until the market is dry"),
        ("list-expansion.md", "~10 seeds to a qualified TAM · fingerprint to verify"),
        ("list-sculpt.md", "SCULPT · learn the customer's own labels"),
        ("list-ai-qualification.md", "AI qualification prompt · tune before contact pull"),
        ("list-qa.md", "8 dimensions · grade before upload"),
        ("sourcing-blitz.md", "domain to contacts"),
        ("sourcing-google-maps.md", "local SMB lists · category x place"),
        ("sourcing-discolike.md", "lookalikes from seed domains"),
        ("sourcing-competitor-engagers.md", "who engages with competitor posts"),
        ("sourcing-prospeo-export.md", "paginated people export"),
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
        ("copy-stepwise.md", "direction to subject to body to YAML · confirm each step"),
        ("copy-spintax.md", "Smartlead spintax · variation budgets"),
        ("spam-rules.md", "phrases that trip filters · scan before send"),
        ("personalization-depth.md", "fact/inference/hypothesis · appropriateness line"),
        ("personalization-subagent.md", "per-lead fan-out · approval loop"),
        ("cta-design.md", "motivation x ability x prompt"),
        ("cold-call.md", "4-move opener · phone as a second signal"),
        ("linkedin-playbook.md", "connection notes · sequencing · reply handling"),
        ("multichannel-orchestration.md", "video · WhatsApp · phone · conditional branches"),
        ("deliverability.md", "warmup ladder · SPF/DKIM/DMARC · bulk-sender rules"),
        ("suppression-mechanics.md", "global suppression · cross-domain removal"),
        ("upload-smartlead.md", "DRAFT upload · human presses start"),
        ("objection-library.md", "recurring objections · understand before countering"),
    ]),
    ("measurement and market", [
        ("gtm-benchmarks.md", "email + LinkedIn bands · what not to optimise"),
        ("gtm-math.md", "formulas mirroring the calculator"),
        ("experiments.md", "single-variable design · avoid confounded arms"),
        ("ai-sdr-positioning.md", "what to automate · where AI SDR stops paying"),
        ("gcc-market.md", "★ MENA: coverage gap · Sun-Thu · Ramadan · Zid/Salla"),
        ("mcp-integration.md", "live-data seam · read-only boundary"),
    ]),
    ("infrastructure", [
        ("infra/domains.md", "domain generation · purchase · nameservers"),
        ("infra/inbox-warmup.md", "warmup ramps · signatures · tagging"),
        ("infra/deliverability-audit.md", "SPF/DKIM/DMARC · placement · bounce mix"),
        ("infra/deliverability-incident.md", "failure-mode triage tree"),
        ("infra/inbox-lifecycle.md", "keep/cancel/promote/buy · replacement lead time"),
    ]),
    ("operations", [
        ("ops/weekly-rhythm.md", "Mon/Wed/Fri · fixed order so drift is visible"),
        ("ops/reply-scoring.md", "positive replies / sends · the one metric"),
        ("ops/deliverability-testing.md", "compare reply and bounce by inbox type"),
    ]),
    ("APIs", [
        ("api/smartlead.md", "campaigns · leads · inboxes · analytics endpoints"),
        ("api/prospeo.md", "Search Person filters · pagination"),
    ]),
    ("signal playbooks", [
        ("signals/index.md", "playbook index · the two build harnesses"),
        *[(f"signals/{k}.md", d) for k, d in SIGNALS],
    ]),
    # Aggregated below: 19 clay-table builds + 19 CLI workflows, counted and audited.
    ("signal builds (aggregated)", [
        ("signals/clay-table-harness.md", "shared harness for every clay table build"),
        ("signals/clay-cli-harness.md", "shared harness for every CLI workflow build"),
        ("signals/*.clay-table.md", "Clay table build · columns · credit gates"),
        ("signals/*.clay-workflow.md", "Clay CLI workflow build"),
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
    ("reply-drafts.md", "draft per reply class · never sends"),
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
    ("gtm-outbound-infra", "domains · warmup · auth · incidents · fleet lifecycle"),
    ("gtm-outbound-signals", "19 signal playbooks · one line each"),
    ("gtm-outbound-ops", "weekly rhythm · reply scoring · inbox-type tests"),
]

drift: list[str] = []


def count_lines(path: Path) -> int:
    if not path.exists():
        drift.append(f"missing: {path.relative_to(ROOT)}")
        return 0
    return len(path.read_text(encoding="utf-8", errors="replace").splitlines())


def item_stats(name: str) -> tuple[int, int]:
    """(file count, total lines) for a reference entry; supports a glob aggregate."""
    refdir = SKILL / "references"
    if "*" in name:
        matches = sorted(refdir.glob(name))
        return len(matches), sum(count_lines(p) for p in matches)
    return 1, count_lines(refdir / name)


def audit(directory: Path, described: list[str], pattern: str) -> None:
    """Every file on disk must be described, and every description must resolve."""
    actual = {
        str(p.relative_to(directory)).replace("\\", "/")
        for p in directory.rglob(pattern)
    }
    expected: set[str] = set()
    for name in described:
        if "*" in name:
            expected |= {
                str(p.relative_to(directory)).replace("\\", "/")
                for p in directory.glob(name)
            }
        else:
            expected.add(name)
    for extra in sorted(actual - expected):
        drift.append(f"undescribed: {directory.name}/{extra}")
    for gone in sorted(expected - actual):
        drift.append(f"described but absent: {directory.name}/{gone}")


def row(prefix: str, name: str, count: int, desc: str) -> str:
    left = f"{prefix}{name}".ljust(NAME_END)
    return f"{left}{count:>{NUM_W},} ─ {desc}".rstrip()


def header(prefix: str, name: str, total: int, desc: str) -> str:
    left = f"{prefix}{name}".ljust(NAME_END)
    return f"{left}{total:>{NUM_W},} ─ {desc}".rstrip()


def band(label: str, total: int) -> str:
    left = f"│   │  ╭─ {label.upper()} ".ljust(NAME_END - 1, "─")
    return f"{left} {total:>{NUM_W},} ─╮"


ref_files = [n for _, items in REFERENCES for n, _ in items]
audit(SKILL / "references", ref_files, "*.md")
audit(SKILL / "scripts", [n for n, _ in SCRIPTS], "*.py")
audit(SKILL / "assets/templates", [n for n, _ in TEMPLATES], "*.md")

out: list[str] = []
w = out.append


def band_total(items) -> int:
    return sum(item_stats(n)[1] for n, _ in items)


ref_total = band_total([(n, d) for _, items in REFERENCES for n, d in items])
ref_count = len(list((SKILL / "references").rglob("*.md")))
script_total = sum(count_lines(SKILL / "scripts" / n) for n, _ in SCRIPTS)
tpl_total = sum(count_lines(SKILL / "assets/templates" / n) for n, _ in TEMPLATES)
sub_total = sum(count_lines(SKILLS / d / "SKILL.md") for d, _ in SUBSKILLS)
opt_files = sorted((SKILL / "optional" / "scripts").rglob("*.ts"))
opt_count = len(opt_files)
opt_total = sum(count_lines(p) for p in opt_files)

w("gtm-outbound/".ljust(NAME_END) + "  ★  ORCHESTRATOR — the only file always in context")
w("│")
w(row("├── ", "SKILL.md", count_lines(SKILL / "SKILL.md"),
      "routing table · artifact chain · hard gates"))
w(" " * DESC_COL + "motion-fit and geography intake · NEVER-SENDS")
w("│")
w("├── agents/")
w(row("│   └── ", "gtm-outbound-researcher.md",
      count_lines(SKILL / "agents/gtm-outbound-researcher.md"),
      "the one parallel step · can return SUPPRESS"))
w("│")
w(header("├── ", "references/", ref_total, f"{ref_count} files, loaded on demand only"))
for group, items in REFERENCES:
    w("│   │")
    w(band(group, band_total(items)))
    for i, (name, desc) in enumerate(items):
        edge = "│   └── " if i == len(items) - 1 else "│   ├── "
        nfiles, nlines = item_stats(name)
        label = name if "*" not in name else name.replace("*", f"{nfiles}")
        w(row(edge, label, nlines, desc))
w("│")
w(header("├── ", "scripts/", script_total, "run these, never reason about their output"))
for i, (name, desc) in enumerate(SCRIPTS):
    edge = "│   └── " if i == len(SCRIPTS) - 1 else "│   ├── "
    w(row(edge, name, count_lines(SKILL / "scripts" / name), desc))
w("│")
w(header("├── ", "optional/", opt_total,
         f"{opt_count} TypeScript files — OUTSIDE the zero-dependency core"))
w(row("│   ├── ", "README.md", count_lines(SKILL / "optional" / "README.md"),
      "what breaks if you move this into the core"))
w(row("│   └── ", "scripts/<skill>/*.ts", opt_total,
      "need Node 18+, tsx and API keys · not covered by preflight"))
w("│")
w(header("└── ", "assets/templates/", tpl_total,
         f"{len(TEMPLATES)} files, fill rather than invent a shape"))
for i, (name, desc) in enumerate(TEMPLATES):
    edge = "    └── " if i == len(TEMPLATES) - 1 else "    ├── "
    w(row(edge, name, count_lines(SKILL / "assets/templates" / name), desc))

w("")
w(header("", "gtm-outbound-*/", sub_total, "SIBLING SKILLS — one loads per route"))
for i, (name, desc) in enumerate(SUBSKILLS):
    edge = "└── " if i == len(SUBSKILLS) - 1 else "├── "
    w(row(edge, name + "/", count_lines(SKILLS / name / "SKILL.md"), desc))

w("")
w("─" * 92)
total = (count_lines(SKILL / "SKILL.md")
         + count_lines(SKILL / "agents/gtm-outbound-researcher.md")
         + ref_total + script_total + tpl_total + sub_total)
w(f"{len(SUBSKILLS) + 1} skills · 1 agent · {ref_count} references · "
  f"{len(SCRIPTS)} scripts · {len(TEMPLATES)} templates · {total:,} lines")

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
