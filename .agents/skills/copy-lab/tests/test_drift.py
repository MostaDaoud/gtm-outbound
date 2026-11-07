"""Drift, coverage and freshness gates for the copy-lab library.

These were previously written as standalone scripts with a ``main()``, so pytest
collected nothing and a broken gate could pass unnoticed. Each assertion is now
an independent test.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import validate_library as validator  # noqa: E402


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


@pytest.fixture()
def workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Path]:
    """Isolated corpus, data dir and source catalog with the resolvers patched."""
    corpus = tmp_path / "_transcripts"
    data = tmp_path / ".copy-lab-data"
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

    monkeypatch.setattr(validator, "find_corpus_root", lambda: corpus)
    monkeypatch.setattr(validator, "resolve_data_dir", lambda **_: data)
    monkeypatch.setattr(validator, "resolve_source_catalog", lambda: catalog)
    monkeypatch.setattr(validator, "active_mining_dir", lambda: data / "mining")

    return {"root": tmp_path, "corpus": corpus, "data": data, "transcript": transcript, "catalog": catalog}


def test_clean_corpus_is_current(workspace: dict[str, Path]) -> None:
    findings, status = validator.check_corpus_drift()
    assert findings == [], findings
    assert status["status"] == "current"


def test_edited_transcript_reports_drift(workspace: dict[str, Path]) -> None:
    transcript = workspace["transcript"]
    transcript.write_text(
        transcript.read_text(encoding="utf-8") + "[00:05] Newly arrived text.\n",
        encoding="utf-8",
    )
    findings, status = validator.check_corpus_drift()
    assert status["status"] == "drifted"
    assert any("changed since indexing" in item["issue"] for item in findings)


def test_unregistered_workspace_source_is_flagged(workspace: dict[str, Path]) -> None:
    source = workspace["root"] / "new-source.pdf"
    source.write_bytes(b"test")
    findings, status = validator.check_workspace_source_coverage()
    assert status["unregistered"] == 1
    assert any(str(source) == item["file"] for item in findings)


def test_registered_workspace_source_is_current(workspace: dict[str, Path]) -> None:
    source = workspace["root"] / "new-source.pdf"
    source.write_bytes(b"test")
    write_json(workspace["catalog"], {"sources": [{"source_path": str(source)}]})
    findings, status = validator.check_workspace_source_coverage()
    assert findings == [], findings
    assert status["status"] == "current"


def test_stale_review_manifest_predates_mining(workspace: dict[str, Path]) -> None:
    write_json(
        workspace["data"] / "mining" / "mining_report.json",
        {"generated_utc": "2026-01-02T00:00:00Z"},
    )
    review = workspace["root"] / "library_manifest.json"
    write_json(review, {"reviewed_utc": "2026-01-01T00:00:00Z"})
    findings = validator.check_freshness(review)
    assert any("predates" in item["issue"] for item in findings)


def test_fresh_review_manifest_passes(workspace: dict[str, Path]) -> None:
    write_json(
        workspace["data"] / "mining" / "mining_report.json",
        {"generated_utc": "2026-01-02T00:00:00Z"},
    )
    review = workspace["root"] / "library_manifest.json"
    write_json(review, {"reviewed_utc": "2026-01-03T00:00:00Z"})
    assert validator.check_freshness(review) == []
