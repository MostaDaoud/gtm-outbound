from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from source_lib import extract_source, file_hash  # noqa: E402


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="copy-lab-media-test-") as temporary:
        root = Path(temporary)
        media = root / "book.m4b"
        transcript = root / "transcript.vtt"
        manifest = root / "transcription_manifest.json"
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
        source = {
            "id": "test-audiobook",
            "title": "Test Audiobook",
            "author": "Test Author",
            "format": "m4b",
            "source_type": "audiobook",
            "source_path": str(media),
            "text_path": str(transcript),
            "transcript_manifest_path": str(manifest),
        }
        records, status = extract_source(source)
        assert records and records[0]["locator_type"] == "timestamp"
        assert records[0]["source_type"] == "audiobook"
        assert status["status"] == "indexed"
        assert status["extraction_method"] == "faster-whisper-webvtt"
        assert status["transcription_model"] == "local-test-model"

        transcript.write_text(transcript.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        try:
            extract_source(source)
        except ValueError as exc:
            assert "text hash" in str(exc)
        else:
            raise AssertionError("transcript hash drift was not rejected")

    print("Copy Lab media-source tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
