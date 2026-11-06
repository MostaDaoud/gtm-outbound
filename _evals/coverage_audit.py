"""Deterministic coverage audit: every assertion added for the merge must have
supporting content in the skill it applies to. Catches a skill claiming a rule
it never actually states - the main failure mode after a content merge.

Exit 1 if any claim is unsupported.
"""
from pathlib import Path
import sys, re

ROOT = Path(r"C:\Users\mosta\gtm-outbound")
SK = ROOT / "skills"
REF = SK / "gtm-outbound" / "references"


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else ""


def gather(paths):
    return "\n".join(read(p) for p in paths).lower()


infra = gather([SK / "gtm-outbound-infra" / "SKILL.md"] + list((REF / "infra").glob("*.md")))
signals = gather([SK / "gtm-outbound-signals" / "SKILL.md"] + list((REF / "signals").glob("*.md")))
ops = gather([SK / "gtm-outbound-ops" / "SKILL.md"] + list((REF / "ops").glob("*.md")))
copyblob = gather([SK / "gtm-outbound-copy" / "SKILL.md", REF / "upload-smartlead.md", REF / "api" / "smartlead.md"])
mathblob = gather([SK / "gtm-outbound-math" / "SKILL.md", REF / "experiments.md"])

CLAIMS = [
    # (eval, assertion, blob, any-of keywords, human description)
    (30, "names-1pct-rule",        infra,   ["1-2%", "1%"],                              "bounce >1-2% is infra not copy"),
    (30, "audits-before-blaming",  infra,   ["audit", "before"],                         "audits before blaming copy"),
    (31, "one-line-contract",      signals, ["one line", "one-line", "one sentence"],    "one signal -> one sentence"),
    (32, "names-one-metric",       ops,     ["positive replies", "total sent"],          "positive replies / total sent"),
    (32, "gives-cadence",          ops,     ["monday", "wednesday", "friday"],           "Mon/Wed/Fri cadence"),
    (33, "per-domain-ceiling",     infra,   ["per domain", "per-domain"],                "per-domain ceiling"),
    (33, "warns-against-concentrating", infra, ["inbox", "domain"],                      "inbox vs domain distinction"),
    (35, "defines-the-field",      signals, ["pipeline", "field"],                       "field produced by pipeline"),
    (38, "refuses-invented-signals", signals, ["hallucinat"],                            "explicit anti-hallucination rule"),
    (38, "requires-pipeline-field", signals, ["pipeline"],                               "pipeline-produced variable"),
    (39, "checks-significance",    mathblob, ["ab-eval"],                                "ab-eval significance check"),
    (40, "upload-is-draft",        copyblob, ["draft"],                                  "DRAFT-only upload"),
    (40, "refuses-auto-start",     copyblob, ["human", "never sends", "start"],          "human presses start"),
    (41, "advises-pause",          infra,   ["pause"],                                   "pause before remedy"),
    (41, "no-reputation-evasion",  infra,   ["evade", "out of scope"],                   "refuses filter evasion"),
]

fails = 0
print(f"{'eval':>5}  {'assertion':<32} {'result':<6} description")
print("-" * 92)
for eid, name, blob, kws, desc in CLAIMS:
    hit = any(k.lower() in blob for k in kws)
    if not hit:
        fails += 1
    print(f"{eid:>5}  {name:<32} {'OK' if hit else 'GAP':<6} {desc}")

# Structural: exactly 19 signal playbooks (excluding clay build companions + index/harness)
signal_dir = REF / "signals"
main = [p for p in signal_dir.glob("*.md")
        if not re.search(r"\.clay-(table|workflow)\.md$", p.name)
        and p.name not in {"index.md", "clay-table-harness.md", "clay-cli-harness.md"}]
print("-" * 92)
print(f"signal playbooks present: {len(main)} (expect 19)")
if len(main) != 19:
    fails += 1

print()
print("COVERAGE: PASS" if fails == 0 else f"COVERAGE: {fails} GAP(S)")
sys.exit(0 if fails == 0 else 1)
