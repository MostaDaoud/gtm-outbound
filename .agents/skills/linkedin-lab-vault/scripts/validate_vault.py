#!/usr/bin/env python3
"""Validate a built LinkedIn Lab Obsidian vault."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
REQUIRED = [
    "LinkedIn Lab Dashboard.md",
    "Start Here.md",
    "Dashboards/Course Library.md",
    "Dashboards/Topic Library.md",
    "Dashboards/Source Library.md",
    "Dashboards/Theme Coverage.md",
    "Dashboards/Library Health.md",
    "Dashboards/LinkedIn Lab Workflow.canvas",
    "Projects/Projects.md",
    "Templates/Copy Brief.md",
    "Workflows/Write Copy.md",
    ".obsidian/app.json",
    ".obsidian/core-plugins.json",
    "_meta/build-manifest.json",
    "_meta/vault-config.json",
]


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object: {path}")
    return data


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_input(path: Path) -> str:
    if path.is_file():
        return sha256(path)
    digest = hashlib.sha256()
    children = (
        child for child in path.rglob("*")
        if child.is_file()
        and child.suffix.lower() in {".md", ".txt"}
        and not child.name.startswith("_")
        and (path.name.casefold() != "_transcripts" or child.name.casefold() != "document.md")
    )
    for child in sorted(children, key=lambda item: item.relative_to(path).as_posix().casefold()):
        digest.update(child.relative_to(path).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(child.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def note_index(vault: Path) -> tuple[dict[str, list[Path]], dict[str, Path]]:
    by_stem: dict[str, list[Path]] = {}
    by_path: dict[str, Path] = {}
    paths = [*vault.rglob("*.md"), *vault.rglob("*.canvas")]
    for path in paths:
        relative = path.relative_to(vault)
        stem_path = relative.with_suffix("").as_posix()
        by_path[stem_path.casefold()] = path
        by_path[relative.as_posix().casefold()] = path
        by_stem.setdefault(path.stem.casefold(), []).append(path)
        by_stem.setdefault(path.name.casefold(), []).append(path)
    return by_stem, by_path


def validate(vault: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if not vault.is_dir():
        return {"ok": False, "errors": [f"vault does not exist: {vault}"], "warnings": [], "counts": {}}
    for relative in REQUIRED:
        if not (vault / relative).is_file():
            errors.append(f"missing required file: {relative}")

    manifest_path = vault / "_meta" / "build-manifest.json"
    manifest: dict[str, Any] = {}
    if manifest_path.is_file():
        try:
            manifest = load_json(manifest_path)
        except (ValueError, json.JSONDecodeError) as exc:
            errors.append(f"invalid build manifest: {exc}")

    generated = manifest.get("generated_files", {})
    if generated and not isinstance(generated, dict):
        errors.append("build manifest generated_files must be an object")
        generated = {}
    for relative, expected in generated.items():
        path = vault / relative
        if not path.is_file():
            errors.append(f"generated file missing: {relative}")
        elif sha256(path) != expected:
            errors.append(f"generated file changed since build: {relative}")

    inputs = manifest.get("inputs", {})
    if isinstance(inputs, dict):
        for name, record in inputs.items():
            if not isinstance(record, dict) or not record.get("path") or not record.get("sha256"):
                errors.append(f"invalid input record: {name}")
                continue
            source = Path(str(record["path"]))
            if not source.exists():
                errors.append(f"build input missing: {name} -> {source}")
            elif sha256_input(source) != record["sha256"]:
                errors.append(f"build input changed; refresh vault: {name}")

    json_files = [
        ".obsidian/app.json",
        ".obsidian/appearance.json",
        ".obsidian/core-plugins.json",
        ".obsidian/templates.json",
        ".obsidian/graph.json",
        "Dashboards/LinkedIn Lab Workflow.canvas",
        "_meta/build-manifest.json",
        "_meta/vault-config.json",
    ]
    for relative in json_files:
        path = vault / relative
        if not path.is_file():
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON: {relative}: {exc}")

    by_stem, by_path = note_index(vault)
    unresolved: list[str] = []
    ambiguous: list[str] = []
    for note in vault.rglob("*.md"):
        text = note.read_text(encoding="utf-8", errors="replace")
        for target in WIKILINK.findall(text):
            normalized = target.strip().rstrip("\\").replace("\\", "/").removesuffix(".md")
            if not normalized:
                continue
            if "/" in normalized:
                if normalized.casefold() not in by_path:
                    unresolved.append(f"{note.relative_to(vault).as_posix()} -> {target}")
            else:
                matches = by_stem.get(normalized.casefold(), [])
                if not matches:
                    unresolved.append(f"{note.relative_to(vault).as_posix()} -> {target}")
                elif len(matches) > 1:
                    ambiguous.append(f"{note.relative_to(vault).as_posix()} -> {target}")
    errors.extend(f"unresolved wikilink: {item}" for item in sorted(set(unresolved)))
    warnings.extend(f"ambiguous wikilink: {item}" for item in sorted(set(ambiguous)))

    counts = manifest.get("counts", {}) if isinstance(manifest.get("counts", {}), dict) else {}
    actual = {
        "topics": len(list((vault / "_generated" / "Topics").glob("*.md"))),
        "courses": len(list((vault / "_generated" / "Courses").glob("*.md"))),
        "sources": len(list((vault / "_generated" / "Sources").glob("*.md"))),
        "themes": len(list((vault / "_generated" / "Themes").glob("*.md"))),
    }
    for key, value in actual.items():
        if key in counts and int(counts[key]) != value:
            errors.append(f"{key} count mismatch: manifest={counts[key]} actual={value}")

    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "counts": {**counts, "markdown_notes": len(list(vault.rglob("*.md")))},
        "generated_files_checked": len(generated),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vault", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = validate(args.vault)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print("OK: LinkedIn Lab vault is valid" if result["ok"] else "FAIL: LinkedIn Lab vault is invalid")
        for item in result["errors"]:
            print(f"ERROR: {item}")
        for item in result["warnings"]:
            print(f"WARNING: {item}")
        print("Counts: " + json.dumps(result["counts"], ensure_ascii=False, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
