#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "scripts" / "build_vault.py"
VALIDATE = ROOT / "scripts" / "validate_vault.py"
PY = sys.executable


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([PY, *args], text=True, capture_output=True, check=False)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="linkedin-lab-vault-test-") as tmp:
        base = Path(tmp)
        linkedin_lab = base / "linkedin-lab"
        data = base / ".linkedin-lab-data"
        vault = base / "vault"
        transcript = base / "_transcripts" / "Test Course" / "lesson.md"
        transcript.parent.mkdir(parents=True)
        transcript.write_text("## Transcript\n\n[00:00] Original lesson text.\n", encoding="utf-8")
        references = {
            "frameworks.md": "# Frameworks\n\nAIDA is a useful skeleton.\n",
            "critique-rubric.md": "# Critique Rubric\n\nScore the commercial effect.\n",
            "anti-generic-copy.md": "# Anti-generic copy pass\n\nPreserve facts and distinctive voice.\n",
        }
        reference_dir = linkedin_lab / "references"
        reference_dir.mkdir(parents=True)
        manifest_references = {}
        for filename, content in references.items():
            path = reference_dir / filename
            path.write_text(content, encoding="utf-8")
            manifest_references[filename] = {
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "lines": 3,
                "citations": 1,
            }
        lens = reference_dir / "lenses" / "psych-lens.md"
        lens.parent.mkdir(parents=True)
        lens.write_text("# Psychology lens\n\nCheck decision context.\n", encoding="utf-8")
        write_json(
            linkedin_lab / "assets" / "corpus_index.json",
            {
                "totals": {"courses": 1, "lessons": 2, "words": 300, "hours": 1.5},
                "courses": [{"name": "Test Course", "lessons": 2, "words": 300, "hours": 1.5, "sections": ["One"]}],
                "lessons": [],
            },
        )
        write_json(
            linkedin_lab / "assets" / "library_manifest.json",
            {"references": manifest_references},
        )
        write_json(
            linkedin_lab / "assets" / "mining" / "mining_report.json",
            {"passages_kept": 10, "passages_unique": 9, "themes": {"frameworks": {"pool": 20, "selected": 10}}},
        )
        write_json(
            data / "sources" / "catalog.json",
            {"sources": [{"id": "source-1", "title": "Source One", "author": "Writer", "format": "pdf", "source_path": str(base / "one.pdf")}]},
        )
        write_json(
            data / "sources" / "manifest.json",
            {"sources": [{"id": "source-1", "status": "indexed", "records": 5, "locator_type": "page"}]},
        )

        command = [str(BUILD), "--linkedin-lab-dir", str(linkedin_lab), "--data-dir", str(data), "--vault", str(vault)]
        first = run(*command)
        assert first.returncode == 0, first.stderr
        manifest_one = (vault / "_meta" / "build-manifest.json").read_bytes()
        assert (vault / "LinkedIn Lab Dashboard.md").is_file()
        assert (vault / "_generated" / "Topics" / "Frameworks.md").is_file()
        assert (vault / "_generated" / "Courses" / "Test Course.md").is_file()
        assert (vault / "_generated" / "Sources" / "Writer - Source One.md").is_file()

        projects = vault / "Projects" / "Projects.md"
        projects.write_text(projects.read_text(encoding="utf-8") + "\nPersonal project link.\n", encoding="utf-8")
        second = run(*command)
        assert second.returncode == 0, second.stderr
        assert manifest_one == (vault / "_meta" / "build-manifest.json").read_bytes()
        assert "Personal project link" in projects.read_text(encoding="utf-8")

        checked = run(str(VALIDATE), str(vault), "--json")
        assert checked.returncode == 0, checked.stdout + checked.stderr
        result = json.loads(checked.stdout)
        assert result["ok"] is True
        assert result["counts"]["topics"] == 3
        assert result["counts"]["courses"] == 1
        assert result["counts"]["sources"] == 1
        assert result["counts"]["themes"] == 1

        transcript.write_text(
            transcript.read_text(encoding="utf-8") + "[00:05] Newly arrived text.\n",
            encoding="utf-8",
        )
        drifted = run(str(VALIDATE), str(vault), "--json")
        assert drifted.returncode == 1, drifted.stdout + drifted.stderr
        drift_result = json.loads(drifted.stdout)
        assert any("live_transcript_corpus" in item for item in drift_result["errors"])
    print("LinkedIn Lab vault tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
