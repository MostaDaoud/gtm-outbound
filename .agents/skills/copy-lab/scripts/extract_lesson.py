"""Print one lesson's transcript as clean, readable prose.

Strips the watch-report header and the `[MM:SS]` prefixes, then reflows the
segments into paragraphs. Use this when a digest citation looks promising and
you need the surrounding context before quoting it.

Usage:
    python extract_lesson.py "path/to/lesson.md"
    python extract_lesson.py --find "AIDA formula"          # resolve by title
    python extract_lesson.py "path.md" --from 05:00 --to 09:30
    python extract_lesson.py "path.md" --timestamps
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from corpus_lib import (
    build_passages,
    find_corpus_root,
    iter_transcript_paths,
    load_lesson,
)


def to_seconds(stamp: str) -> int:
    """Convert ``MM:SS`` or ``HH:MM:SS`` to whole seconds."""
    parts = [int(p) for p in stamp.strip().split(":")]
    while len(parts) < 3:
        parts.insert(0, 0)
    return parts[-3] * 3600 + parts[-2] * 60 + parts[-1]


def resolve_by_title(root: Path, query: str) -> list[Path]:
    """Find transcripts whose lesson name contains ``query`` (case-insensitive)."""
    needle = query.lower()
    return [p for p in iter_transcript_paths(root) if needle in p.stem.lower()]


def main(argv: list[str] | None = None) -> int:
    # Transcripts contain em dashes, curly quotes and the occasional non-Latin
    # character. Windows consoles default to cp1252, which cannot encode them —
    # printing would raise UnicodeEncodeError mid-lesson.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):  # non-reconfigurable stream
        pass

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("path", nargs="?", type=Path, help="Transcript file path")
    parser.add_argument("--corpus", type=Path, default=None, help="Corpus root directory")
    parser.add_argument("--find", default=None, help="Resolve the lesson by title substring")
    parser.add_argument("--from", dest="start", default=None, help="Start timestamp (MM:SS)")
    parser.add_argument("--to", dest="end", default=None, help="End timestamp (MM:SS)")
    parser.add_argument("--timestamps", action="store_true", help="Keep paragraph timestamps")
    args = parser.parse_args(argv)

    try:
        root = args.corpus.expanduser().resolve() if args.corpus else find_corpus_root()
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.find:
        matches = resolve_by_title(root, args.find)
        if not matches:
            print(f"error: no lesson title contains {args.find!r}", file=sys.stderr)
            return 1
        if len(matches) > 1:
            print(f"{len(matches)} matches -- narrow the query or pass a path:", file=sys.stderr)
            for match in matches[:20]:
                print(f"  {match}", file=sys.stderr)
            return 1
        target = matches[0]
    elif args.path:
        target = args.path
    else:
        parser.error("provide a path or --find")

    if not target.is_file():
        print(f"error: not a file: {target}", file=sys.stderr)
        return 1

    lesson = load_lesson(target, root)
    if not lesson.segments:
        print(f"error: no transcript found in {target}", file=sys.stderr)
        return 1

    start = to_seconds(args.start) if args.start else None
    end = to_seconds(args.end) if args.end else None

    print(f"# {lesson.lesson}")
    print()
    print(f"_{lesson.citation} -- {lesson.word_count:,} words, "
          f"{len(lesson.segments)} segments_")
    print()

    for passage in build_passages(lesson):
        moment = to_seconds(passage.timestamp) if passage.timestamp else 0
        if start is not None and moment < start:
            continue
        if end is not None and moment > end:
            break
        if args.timestamps:
            print(f"**[{passage.timestamp}]** {passage.text}")
        else:
            print(passage.text)
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
