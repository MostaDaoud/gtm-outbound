from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import validate_library as validator  # noqa: E402


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def main() -> int:
    original_find = validator.find_corpus_root
    original_data = validator.resolve_data_dir
    original_catalog = validator.resolve_source_catalog
    original_mining = validator.active_mining_dir
    try:
        with tempfile.TemporaryDirectory(prefix="linkedin-lab-drift-test-") as temporary:
            workspace = Path(temporary)
            corpus = workspace / "_transcripts"
            data = workspace / ".linkedin-lab-data"
            transcript = corpus / "Course" / "lesson.md"
            transcript.parent.mkdir(parents=True)
            transcript.write_text("## Transcript\n\n[00:00] Original lesson text.\n", encoding="utf-8")
            lesson = validator.load_lesson(transcript, corpus)
            write_json(
                data / "corpus_index.json",
                {
                    "lessons": [
                        {
                            "path": str(transcript),
                            "bytes": transcript.stat().st_size,
                            "words": lesson.word_count,
                            "segments": len(lesson.segments),
                        }
                    ]
                },
            )
            catalog = data / "sources" / "catalog.json"
            write_json(catalog, {"sources": []})

            validator.find_corpus_root = lambda: corpus
            validator.resolve_data_dir = lambda **_: data
            validator.resolve_source_catalog = lambda: catalog
            validator.active_mining_dir = lambda: data / "mining"

            findings, status = validator.check_corpus_drift()
            assert findings == [], findings
            assert status["status"] == "current"

            transcript.write_text(
                transcript.read_text(encoding="utf-8") + "[00:05] Newly arrived text.\n",
                encoding="utf-8",
            )
            findings, status = validator.check_corpus_drift()
            assert status["status"] == "drifted"
            assert any("changed since indexing" in item["issue"] for item in findings)

            source = workspace / "new-source.pdf"
            source.write_bytes(b"test")
            findings, status = validator.check_workspace_source_coverage()
            assert status["unregistered"] == 1
            assert any(str(source) == item["file"] for item in findings)

            write_json(catalog, {"sources": [{"source_path": str(source)}]})
            findings, status = validator.check_workspace_source_coverage()
            assert findings == [], findings
            assert status["status"] == "current"

            write_json(
                data / "mining" / "mining_report.json",
                {"generated_utc": "2026-01-02T00:00:00Z"},
            )
            review_manifest = workspace / "library_manifest.json"
            write_json(review_manifest, {"reviewed_utc": "2026-01-01T00:00:00Z"})
            findings = validator.check_freshness(review_manifest)
            assert any("predates" in item["issue"] for item in findings)
            write_json(review_manifest, {"reviewed_utc": "2026-01-03T00:00:00Z"})
            assert validator.check_freshness(review_manifest) == []
    finally:
        validator.find_corpus_root = original_find
        validator.resolve_data_dir = original_data
        validator.resolve_source_catalog = original_catalog
        validator.active_mining_dir = original_mining

    print("LinkedIn Lab drift tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
