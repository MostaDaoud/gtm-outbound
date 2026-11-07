"""Media-source provenance and transcript hash gating.

Previously a standalone script, so pytest collected nothing. Split into
independent tests that each build their own fixture.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from source_lib import extract_source, file_hash  # noqa: E402


@pytest.fixture()
def audiobook(tmp_path: Path) -> dict[str, object]:
    """A media file, a matching WebVTT transcript, and a complete manifest."""
    media = tmp_path / "book.m4b"
    transcript = tmp_path / "transcript.vtt"
    manifest = tmp_path / "transcription_manifest.json"

    media.write_bytes(b"test media provenance")
    transcript.write_text(
        "WEBVTT\n\n1\n00:00:01.000 --> 00:00:05.000\n"
        "System one works automatically and quickly with little effort.\n",
        encoding="utf-8",
    )
    manifest.write_text(
        json.dumps(
            {
                "status": "complete",
                "source_sha256": file_hash(media),
                "transcript_sha256": file_hash(transcript),
                "model": "local-test-model",
            }
        ),
        encoding="utf-8",
    )

    return {
        "transcript": transcript,
        "source": {
            "id": "test-audiobook",
            "title": "Test Audiobook",
            "author": "Test Author",
            "format": "m4b",
            "source_type": "audiobook",
            "source_path": str(media),
            "text_path": str(transcript),
            "transcript_manifest_path": str(manifest),
        },
    }


def test_audiobook_yields_timestamped_records(audiobook: dict[str, object]) -> None:
    records, status = extract_source(audiobook["source"])
    assert records and records[0]["locator_type"] == "timestamp"
    assert records[0]["source_type"] == "audiobook"
    assert status["status"] == "indexed"


def test_extraction_records_model_provenance(audiobook: dict[str, object]) -> None:
    _, status = extract_source(audiobook["source"])
    assert status["extraction_method"] == "faster-whisper-webvtt"
    assert status["transcription_model"] == "local-test-model"


def test_transcript_hash_drift_is_rejected(audiobook: dict[str, object]) -> None:
    transcript = audiobook["transcript"]
    transcript.write_text(transcript.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    with pytest.raises(ValueError) as excinfo:
        extract_source(audiobook["source"])
    assert "text hash" in str(excinfo.value)
