"""Persistent, cross-platform configuration for linkedin-lab.

Configuration is deliberately stored outside the installed skill so corpus
mining never mutates the skill package. Environment variables remain useful for
one-off overrides and take precedence over the config file.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

CONFIG_ENV_VAR = "linkedin_lab_CONFIG"
CORPUS_ENV_VAR = "linkedin_lab_CORPUS"
DATA_ENV_VAR = "linkedin_lab_DATA"
COURSE_MAP_ENV_VAR = "linkedin_lab_COURSE_MAP"
SOURCE_CATALOG_ENV_VAR = "linkedin_lab_SOURCE_CATALOG"
CORPUS_DIRNAME = "_transcripts"

SKILL_ROOT = Path(__file__).resolve().parent.parent
BUNDLED_ASSETS = SKILL_ROOT / "assets"


def default_config_path() -> Path:
    """Return the per-user linkedin-lab configuration path.

    Codex sandboxes can read the user agent directory while denying ordinary
    AppData access. Keeping configuration next to (but not inside) the global
    skill directory makes persistent resolution work in normal skill runs.
    """
    override = os.environ.get(CONFIG_ENV_VAR)
    if override:
        return Path(override).expanduser().resolve()
    return Path.home() / ".agents" / "linkedin-lab" / "config.json"


def load_config(path: Path | None = None) -> dict[str, Any]:
    """Load configuration, returning an empty mapping when none exists."""
    target = (path or default_config_path()).expanduser()
    if not target.is_file():
        return {}
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def save_config(data: dict[str, Any], path: Path | None = None) -> Path:
    """Write configuration atomically and return its path."""
    target = (path or default_config_path()).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    temporary.replace(target)
    return target


def _configured_path(key: str, env_var: str) -> Path | None:
    value = os.environ.get(env_var) or load_config().get(key)
    if not value:
        return None
    return Path(str(value)).expanduser().resolve()


def _ancestor_candidates(origin: Path) -> list[Path]:
    origin = origin.resolve()
    if origin.is_file():
        origin = origin.parent
    return [origin, *origin.parents]


def resolve_corpus(explicit: Path | None = None, start: Path | None = None) -> Path:
    """Resolve the transcript corpus without depending on install location.

    Resolution order: explicit argument, environment variable, persistent
    config, current working directory ancestors, then ``start`` ancestors.
    """
    candidates: list[tuple[str, Path]] = []
    if explicit:
        candidates.append(("--corpus", explicit.expanduser().resolve()))
    configured = _configured_path("corpus", CORPUS_ENV_VAR)
    if configured:
        candidates.append((CORPUS_ENV_VAR, configured))

    searched: set[Path] = set()
    for label, candidate in candidates:
        if candidate.is_dir():
            return candidate
        raise FileNotFoundError(f"{label} points to {candidate}, which is not a directory.")

    origins = [Path.cwd()]
    if start:
        origins.append(start)
    origins.append(Path(__file__).resolve().parent)
    for origin in origins:
        for parent in _ancestor_candidates(origin):
            if parent in searched:
                continue
            searched.add(parent)
            candidate = parent / CORPUS_DIRNAME
            if candidate.is_dir():
                return candidate

    raise FileNotFoundError(
        f"Could not find '{CORPUS_DIRNAME}'. Run configure.py set corpus PATH, "
        f"pass --corpus, or set {CORPUS_ENV_VAR}."
    )


def resolve_data_dir(
    explicit: Path | None = None,
    corpus: Path | None = None,
    *,
    for_write: bool = False,
) -> Path:
    """Resolve mutable data storage outside the installed skill.

    If no override is configured, a located corpus uses a sibling
    ``.linkedin-lab-data`` directory. Callers that need a generated artifact may
    still fall back to the bundled equivalent when the external artifact does
    not exist.
    """
    if explicit:
        target = explicit.expanduser().resolve()
    else:
        target = _configured_path("data_dir", DATA_ENV_VAR)
        if target is None:
            located = corpus
            if located is None:
                try:
                    located = resolve_corpus()
                except FileNotFoundError:
                    located = None
            target = located.parent / ".linkedin-lab-data" if located else BUNDLED_ASSETS

    if for_write:
        if target == BUNDLED_ASSETS:
            raise FileNotFoundError(
                "No external data directory can be derived. Configure a corpus or data_dir."
            )
        target.mkdir(parents=True, exist_ok=True)
        return target

    return target


def resolve_course_map(explicit: Path | None = None) -> Path:
    """Resolve a user-maintained course map, falling back to the bundled map."""
    if explicit:
        candidate = explicit.expanduser().resolve()
    else:
        candidate = _configured_path("course_map", COURSE_MAP_ENV_VAR)
        if candidate is None:
            try:
                external = resolve_data_dir() / "course_map.json"
            except FileNotFoundError:
                external = Path()
            candidate = external if external.is_file() else BUNDLED_ASSETS / "course_map.json"
    return candidate


def resolve_mined_store(explicit: Path | None = None) -> Path:
    """Prefer a generated external store, then fall back to the bundled store."""
    if explicit:
        return explicit.expanduser().resolve()
    external = resolve_data_dir() / "mining" / "mined.jsonl"
    if external.is_file():
        return external
    return BUNDLED_ASSETS / "mining" / "mined.jsonl"


def resolve_source_dir(explicit: Path | None = None, *, for_write: bool = False) -> Path:
    """Resolve the external, mutable source-index directory."""
    if explicit:
        target = explicit.expanduser().resolve()
        if for_write:
            target.mkdir(parents=True, exist_ok=True)
        return target
    return resolve_data_dir(for_write=for_write) / "sources"


def resolve_source_catalog(explicit: Path | None = None) -> Path:
    """Resolve the local source catalog without bundling copyrighted texts."""
    if explicit:
        return explicit.expanduser().resolve()
    configured = _configured_path("source_catalog", SOURCE_CATALOG_ENV_VAR)
    if configured:
        return configured
    return resolve_source_dir() / "catalog.json"


def resolve_source_store(explicit: Path | None = None) -> Path:
    """Resolve the generated book/document passage store."""
    if explicit:
        return explicit.expanduser().resolve()
    return resolve_source_dir() / "passages.jsonl"


def resolve_source_manifest(explicit: Path | None = None) -> Path:
    """Resolve the generated provenance manifest for local sources."""
    if explicit:
        return explicit.expanduser().resolve()
    return resolve_source_dir() / "manifest.json"
