"""Build a queryable index of the transcript corpus.

Walks every transcript file, parses its coordinates and size, enriches with
`manifest.csv` metadata when available, and writes `corpus_index.json`.

Usage:
    python index_corpus.py [--corpus PATH] [--out PATH] [--quiet]

Output JSON shape:
    {
      "root": "...",
      "generated_utc": "...",
      "totals": {"courses": 8, "lessons": 927, "words": 0, "bytes": 0},
      "courses": [{"name": ..., "lessons": ..., "words": ..., "sections": [...]}],
      "lessons": [{"path", "course", "section", "lesson", "words", "segments",
                   "bytes", "duration", "seconds"}]
    }
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from corpus_lib import (
    find_corpus_root,
    iter_transcript_paths,
    load_lesson,
    load_manifest,
)
from linkedin_lab_config import resolve_data_dir


def build_index(root: Path, quiet: bool = False) -> dict:
    """Index every transcript under ``root``.

    Args:
        root: Corpus directory.
        quiet: Suppress per-course progress on stderr.

    Returns:
        The index dictionary, ready to serialize.
    """
    manifest = load_manifest(root)
    lessons: list[dict] = []
    courses: dict[str, dict] = {}

    for path in iter_transcript_paths(root):
        try:
            lesson = load_lesson(path, root)
        except OSError as exc:  # unreadable file should not abort the run
            print(f"warn: skipping {path}: {exc}", file=sys.stderr)
            continue

        meta = manifest.get(os.path.normcase(str(path)), {})
        record = {
            "path": str(path),
            "course": lesson.course,
            "section": lesson.section,
            "lesson": lesson.lesson,
            "words": lesson.word_count,
            "segments": len(lesson.segments),
            "bytes": path.stat().st_size,
            "duration": meta.get("duration", ""),
            "seconds": float(meta.get("seconds") or 0.0),
        }
        lessons.append(record)

        bucket = courses.setdefault(
            lesson.course,
            {"name": lesson.course, "lessons": 0, "words": 0, "seconds": 0.0, "sections": set()},
        )
        bucket["lessons"] += 1
        bucket["words"] += record["words"]
        bucket["seconds"] += record["seconds"]
        if lesson.section:
            bucket["sections"].add(lesson.section)

    course_list = []
    for name in sorted(courses):
        bucket = courses[name]
        course_list.append(
            {
                "name": bucket["name"],
                "lessons": bucket["lessons"],
                "words": bucket["words"],
                "hours": round(bucket["seconds"] / 3600.0, 2),
                "sections": sorted(bucket["sections"]),
            }
        )
        if not quiet:
            print(
                f"  {bucket['name'][:48]:<48} {bucket['lessons']:>4} lessons  "
                f"{bucket['words']:>8,} words",
                file=sys.stderr,
            )

    return {
        "root": str(root),
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "totals": {
            "courses": len(course_list),
            "lessons": len(lessons),
            "words": sum(item["words"] for item in lessons),
            "bytes": sum(item["bytes"] for item in lessons),
            "hours": round(sum(item["seconds"] for item in lessons) / 3600.0, 2),
        },
        "courses": course_list,
        "lessons": lessons,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--corpus", type=Path, default=None, help="Corpus root directory")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output JSON path (default: external linkedin-lab data directory)",
    )
    parser.add_argument("--quiet", action="store_true", help="Suppress progress output")
    args = parser.parse_args(argv)

    try:
        root = args.corpus.resolve() if args.corpus else find_corpus_root()
        output = (
            args.out.expanduser().resolve()
            if args.out
            else resolve_data_dir(corpus=root, for_write=True) / "corpus_index.json"
        )
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if not args.quiet:
        print(f"Indexing corpus at {root}", file=sys.stderr)

    index = build_index(root, quiet=args.quiet)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")

    totals = index["totals"]
    print(
        json.dumps(
            {
                "status": "ok",
                "index": str(output),
                "courses": totals["courses"],
                "lessons": totals["lessons"],
                "words": totals["words"],
                "hours": totals["hours"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
