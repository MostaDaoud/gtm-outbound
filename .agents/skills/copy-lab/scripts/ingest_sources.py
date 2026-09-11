"""Ingest local books/documents into a citable external passage index.

Usage:
    python ingest_sources.py [--catalog PATH] [--out-dir PATH] [--json]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from source_lib import build_source_index


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--catalog", type=Path, default=None, help="Source catalog JSON")
    parser.add_argument("--out-dir", type=Path, default=None, help="Generated source-index directory")
    parser.add_argument("--json", action="store_true", help="Emit full manifest JSON")
    args = parser.parse_args(argv)
    try:
        manifest = build_source_index(args.catalog, args.out_dir)
    except (OSError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(manifest, indent=2, ensure_ascii=False))
    else:
        indexed = sum(1 for source in manifest["sources"] if source["status"] == "indexed")
        needs_ocr = sum(1 for source in manifest["sources"] if source["status"] == "needs_ocr")
        print(
            f"Indexed {manifest['records']} passages from {indexed} source(s)"
            + (f"; {needs_ocr} source(s) need OCR" if needs_ocr else "")
            + f".\nStore: {manifest['store_path']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
