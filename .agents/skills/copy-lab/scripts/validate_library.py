"""Check that the copy-lab reference library is present, sized, and current.

Verifies that every expected reference file exists, is non-trivial, carries
source citations, and is no older than the corpus it was distilled from.
Exits non-zero when a Critical issue is found, so it can gate a build.

Usage:
    python validate_library.py [--json] [--strict]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from copy_lab_config import BUNDLED_ASSETS, resolve_data_dir, resolve_source_catalog
from corpus_lib import find_corpus_root, iter_transcript_paths, load_lesson
from source_lib import validate_source_index

SKILL_ROOT = Path(__file__).resolve().parent.parent
REFERENCES = SKILL_ROOT / "references"
MANIFEST = BUNDLED_ASSETS / "library_manifest.json"

EXPECTED_REFERENCES: dict[str, int] = {
    "frameworks.md": 60,
    "psychology.md": 60,
    "headlines.md": 50,
    "sales-pages.md": 60,
    "emails.md": 50,
    "offers.md": 50,
    "voice.md": 50,
    "anti-generic-copy.md": 100,
    "harry-dry-copywriting.md": 180,
    "ai-workflow.md": 40,
    "client-work.md": 40,
    "positioning.md": 50,
    "research.md": 50,
    "swipe-file.md": 40,
    "critique-rubric.md": 40,
    "fascination-bullets.md": 80,
    "classic-direct-response.md": 80,
    "lead-and-email-playbooks.md": 80,
}

# A citation looks like "(Schutz, 2.3 Anchoring @ 12:04)" or a bare "@ 12:04".
CITATION = re.compile(r"@\s*\d{1,2}:\d{2}")
DISCOVERABLE_SOURCE_SUFFIXES = {".epub", ".m4a", ".m4b", ".mp3", ".mp4", ".pdf", ".wav"}


def file_hash(path: Path) -> str:
    """Return a stable SHA-256 hash for a library artifact."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def active_mining_dir() -> Path:
    """Use generated external mining data when complete, otherwise bundled data."""
    external = resolve_data_dir() / "mining"
    if (external / "mining_report.json").is_file():
        return external
    return BUNDLED_ASSETS / "mining"


def build_manifest() -> dict:
    """Build an integrity manifest for references and their mined source store."""
    mining = BUNDLED_ASSETS / "mining"
    report_path = mining / "mining_report.json"
    store_path = mining / "mined.jsonl"
    generated_utc = ""
    if report_path.is_file():
        try:
            generated_utc = json.loads(report_path.read_text(encoding="utf-8")).get(
                "generated_utc", ""
            )
        except (OSError, ValueError):
            pass
    references = {}
    for name in EXPECTED_REFERENCES:
        path = REFERENCES / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        references[name] = {
            "sha256": file_hash(path),
            "lines": len(text.splitlines()),
            "citations": len(CITATION.findall(text)),
        }
    return {
        "schema_version": 2,
        "reviewed_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "mined_utc": generated_utc,
        "mined_store_sha256": file_hash(store_path) if store_path.is_file() else "",
        "references": references,
    }


def check_manifest(path: Path = MANIFEST) -> list[dict]:
    """Detect reference drift from the reviewed, mined library snapshot."""
    if not path.is_file():
        return [{"severity": "High", "file": str(path), "issue": "Missing provenance manifest"}]
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [{"severity": "Critical", "file": str(path), "issue": f"Invalid manifest: {exc}"}]

    findings: list[dict] = []
    expected = manifest.get("references", {})
    for name in EXPECTED_REFERENCES:
        reference = REFERENCES / name
        recorded = expected.get(name)
        if not isinstance(recorded, dict):
            findings.append({"severity": "High", "file": name, "issue": "Absent from provenance manifest"})
            continue
        if reference.is_file() and file_hash(reference) != recorded.get("sha256"):
            findings.append({"severity": "High", "file": name, "issue": "Changed since provenance review"})

    store = BUNDLED_ASSETS / "mining" / "mined.jsonl"
    recorded_store = manifest.get("mined_store_sha256")
    if store.is_file() and recorded_store and file_hash(store) != recorded_store:
        findings.append(
            {
                "severity": "High",
                "file": "assets/mining/mined.jsonl",
                "issue": "Mined store changed without rebuilding provenance manifest",
            }
        )
    return findings


def check_references() -> list[dict]:
    """Validate each expected reference file."""
    findings: list[dict] = []
    for name, min_lines in EXPECTED_REFERENCES.items():
        path = REFERENCES / name
        if not path.is_file():
            findings.append(
                {"severity": "Critical", "file": name, "issue": "Missing reference file"}
            )
            continue

        text = path.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        if len(lines) < min_lines:
            findings.append(
                {
                    "severity": "High",
                    "file": name,
                    "issue": f"Thin: {len(lines)} lines, expected at least {min_lines}",
                }
            )
        if name not in {
            "critique-rubric.md",
            "fascination-bullets.md",
            "classic-direct-response.md",
            "lead-and-email-playbooks.md",
            "anti-generic-copy.md",
        } and not CITATION.search(text):
            findings.append(
                {
                    "severity": "High",
                    "file": name,
                    "issue": "No timestamped source citations found",
                }
            )
        if not text.lstrip().startswith("#"):
            findings.append(
                {"severity": "Medium", "file": name, "issue": "Missing top-level heading"}
            )
    return findings


def check_freshness(path: Path = MANIFEST) -> list[dict]:
    """Warn when the reviewed library snapshot predates the latest mining run.

    Reference mtimes are not reliable review evidence: a file may be reviewed
    and intentionally left unchanged. The provenance snapshot is the explicit
    review boundary, so compare its timestamp with the mining report instead.
    """
    report = active_mining_dir() / "mining_report.json"
    if not report.is_file():
        return [
            {
                "severity": "Medium",
                "file": "assets/mining/mining_report.json",
                "issue": "No mining report; run mine_corpus.py",
            }
        ]

    mined_at = report.stat().st_mtime
    try:
        generated = json.loads(report.read_text(encoding="utf-8")).get("generated_utc")
        if generated:
            mined_at = datetime.fromisoformat(generated.replace("Z", "+00:00")).timestamp()
    except (OSError, ValueError, TypeError):
        pass
    if not path.is_file():
        return []
    try:
        reviewed = json.loads(path.read_text(encoding="utf-8")).get("reviewed_utc")
        if not reviewed:
            return [{
                "severity": "Low",
                "file": str(path),
                "issue": "Provenance snapshot lacks a review timestamp; rebuild it after review",
            }]
        reviewed_at = datetime.fromisoformat(reviewed.replace("Z", "+00:00")).timestamp()
    except (OSError, ValueError, TypeError):
        return [{
            "severity": "Low",
            "file": str(path),
            "issue": "Provenance review timestamp is invalid",
        }]
    if reviewed_at < mined_at:
        return [{
            "severity": "Low",
            "file": str(path),
            "issue": "Reviewed library snapshot predates the latest mining run",
        }]
    return []


def check_corpus_drift() -> tuple[list[dict], dict]:
    """Compare the live transcript tree with the most recent corpus index.

    The former validator only checked the recorded artifact hashes. New lesson
    files could therefore arrive after indexing while the library still scored
    100. This check parses the live files and compares paths, sizes, word counts,
    and segment counts with the active index.
    """
    try:
        root = find_corpus_root()
    except FileNotFoundError as exc:
        return ([{"severity": "High", "file": "_transcripts", "issue": str(exc)}],
                {"status": "missing", "live_lessons": 0, "indexed_lessons": 0})

    external_index = resolve_data_dir(corpus=root) / "corpus_index.json"
    index_path = external_index if external_index.is_file() else BUNDLED_ASSETS / "corpus_index.json"
    if not index_path.is_file():
        return ([{"severity": "High", "file": str(index_path), "issue": "Missing corpus index"}],
                {"status": "unindexed", "live_lessons": 0, "indexed_lessons": 0})
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return ([{"severity": "Critical", "file": str(index_path), "issue": f"Invalid corpus index: {exc}"}],
                {"status": "invalid", "live_lessons": 0, "indexed_lessons": 0})

    def key(path: Path | str) -> str:
        candidate = Path(path)
        try:
            relative = candidate.resolve().relative_to(root.resolve())
        except (OSError, ValueError):
            relative = candidate
        return str(relative).replace("\\", "/").casefold()

    indexed = {key(item.get("path", "")): item for item in index.get("lessons", [])}
    live: dict[str, dict] = {}
    findings: list[dict] = []
    for path in iter_transcript_paths(root):
        lesson = load_lesson(path, root)
        item = {
            "path": str(path),
            "bytes": path.stat().st_size,
            "words": lesson.word_count,
            "segments": len(lesson.segments),
        }
        live[key(path)] = item
        if not item["segments"] or not item["words"]:
            findings.append(
                {"severity": "High", "file": str(path), "issue": "Transcript has no indexed text segments"}
            )

    for relative in sorted(live.keys() - indexed.keys()):
        findings.append({"severity": "High", "file": live[relative]["path"], "issue": "New transcript is not indexed"})
    for relative in sorted(indexed.keys() - live.keys()):
        findings.append({"severity": "High", "file": indexed[relative].get("path", relative), "issue": "Indexed transcript is missing"})
    for relative in sorted(live.keys() & indexed.keys()):
        current = live[relative]
        recorded = indexed[relative]
        changed = [
            field for field in ("bytes", "words", "segments")
            if int(current[field]) != int(recorded.get(field) or 0)
        ]
        if changed:
            findings.append(
                {
                    "severity": "High",
                    "file": current["path"],
                    "issue": f"Transcript changed since indexing ({', '.join(changed)})",
                }
            )

    summary = {
        "status": "current" if not findings else "drifted",
        "root": str(root),
        "index": str(index_path),
        "live_lessons": len(live),
        "indexed_lessons": len(indexed),
    }
    return findings, summary


def check_workspace_source_coverage() -> tuple[list[dict], dict]:
    """Report top-level books and media that are absent from the source catalog."""
    try:
        workspace = find_corpus_root().parent
        catalog_path = resolve_source_catalog()
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, ValueError) as exc:
        return ([{"severity": "Medium", "file": "source catalog", "issue": f"Cannot check unregistered sources: {exc}"}],
                {"status": "unavailable", "candidates": 0, "registered": 0})

    registered = set()
    for source in catalog.get("sources", []):
        if not isinstance(source, dict) or not source.get("source_path"):
            continue
        try:
            registered.add(str(Path(source["source_path"]).expanduser().resolve()).casefold())
        except OSError:
            continue
    candidates = sorted(
        path.resolve() for path in workspace.iterdir()
        if path.is_file() and path.suffix.casefold() in DISCOVERABLE_SOURCE_SUFFIXES
    )
    unregistered = [path for path in candidates if str(path).casefold() not in registered]
    findings = [
        {"severity": "High", "file": str(path), "issue": "Top-level source is not registered in the source catalog"}
        for path in unregistered
    ]
    return findings, {
        "status": "current" if not findings else "drifted",
        "workspace": str(workspace),
        "candidates": len(candidates),
        "registered": len(candidates) - len(unregistered),
        "unregistered": len(unregistered),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--strict", action="store_true", help="Fail on High as well as Critical")
    parser.add_argument("--manifest", type=Path, default=MANIFEST, help="Provenance manifest")
    parser.add_argument(
        "--write-manifest",
        action="store_true",
        help="Write a provenance manifest for the current bundled library",
    )
    args = parser.parse_args(argv)

    if args.write_manifest:
        manifest = build_manifest()
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(json.dumps({"status": "ok", "manifest": str(args.manifest)}, indent=2))
        return 0

    source_findings, source_status = validate_source_index()
    corpus_findings, corpus_status = check_corpus_drift()
    coverage_findings, coverage_status = check_workspace_source_coverage()
    findings = (check_references() + check_manifest(args.manifest) + check_freshness(args.manifest)
                + source_findings + corpus_findings + coverage_findings)
    order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    findings.sort(key=lambda f: order.get(f["severity"], 9))

    counts = {level: sum(1 for f in findings if f["severity"] == level) for level in order}
    present = sum(1 for name in EXPECTED_REFERENCES if (REFERENCES / name).is_file())
    healthy = max(0, 100 - counts["Critical"] * 25 - counts["High"] * 10 - counts["Medium"] * 4
                  - counts["Low"] * 1)

    result = {
        "references_expected": len(EXPECTED_REFERENCES),
        "references_present": present,
        "health_score": healthy,
        "counts": counts,
        "findings": findings,
        "source_index": source_status,
        "corpus_index": corpus_status,
        "workspace_sources": coverage_status,
    }

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"copy-lab library health: {healthy}/100 "
              f"({present}/{len(EXPECTED_REFERENCES)} references present)")
        if not findings:
            print("No issues found.")
        for finding in findings:
            print(f"  [{finding['severity']:<8}] {finding['file']}: {finding['issue']}")

    failing = counts["Critical"] > 0 or (args.strict and counts["High"] > 0)
    return 1 if failing else 0


if __name__ == "__main__":
    raise SystemExit(main())
