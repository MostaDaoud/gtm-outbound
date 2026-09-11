"""Configure and diagnose a linkedin-lab installation.

Usage:
    python configure.py show
    python configure.py set corpus E:\\Copywriting\\_transcripts
    python configure.py set data_dir E:\\Copywriting\\.linkedin-lab-data
    python configure.py unset corpus
    python configure.py doctor
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from linkedin_lab_config import (
    BUNDLED_ASSETS,
    default_config_path,
    load_config,
    resolve_corpus,
    resolve_data_dir,
    resolve_mined_store,
    resolve_source_catalog,
    resolve_source_manifest,
    resolve_source_store,
    save_config,
)
from source_lib import validate_source_index

ALLOWED_KEYS = {"corpus", "data_dir", "course_map", "source_catalog"}


def _show() -> dict:
    config = load_config()
    result: dict[str, object] = {
        "config_file": str(default_config_path()),
        "config": config,
        "bundled_assets": str(BUNDLED_ASSETS),
    }
    try:
        result["resolved_corpus"] = str(resolve_corpus())
    except FileNotFoundError as exc:
        result["corpus_error"] = str(exc)
    try:
        result["resolved_data_dir"] = str(resolve_data_dir())
        result["resolved_store"] = str(resolve_mined_store())
        result["resolved_source_catalog"] = str(resolve_source_catalog())
        result["resolved_source_store"] = str(resolve_source_store())
        result["resolved_source_manifest"] = str(resolve_source_manifest())
        _, result["source_index"] = validate_source_index()
    except FileNotFoundError as exc:
        result["data_error"] = str(exc)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("show", help="Show configured and resolved paths")
    subparsers.add_parser("doctor", help="Validate corpus and data paths")

    setter = subparsers.add_parser("set", help="Persist a path")
    setter.add_argument("key", choices=sorted(ALLOWED_KEYS))
    setter.add_argument("path", type=Path)

    unsetter = subparsers.add_parser("unset", help="Remove a configured path")
    unsetter.add_argument("key", choices=sorted(ALLOWED_KEYS))
    args = parser.parse_args(argv)

    if args.command == "set":
        path = args.path.expanduser().resolve()
        if args.key == "corpus" and not path.is_dir():
            print(f"error: corpus is not a directory: {path}", file=sys.stderr)
            return 2
        if args.key in {"course_map", "source_catalog"} and not path.is_file():
            print(f"error: {args.key} is not a file: {path}", file=sys.stderr)
            return 2
        config = load_config()
        config[args.key] = str(path)
        target = save_config(config)
        print(json.dumps({"status": "ok", "config": str(target), args.key: str(path)}, indent=2))
        return 0

    if args.command == "unset":
        config = load_config()
        config.pop(args.key, None)
        target = save_config(config)
        print(json.dumps({"status": "ok", "config": str(target), "removed": args.key}, indent=2))
        return 0

    result = _show()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if args.command == "doctor" and "data_error" in result:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
