"""Unified command-line entry point for copy-lab.

Usage:
    python copy_lab.py doctor
    python copy_lab.py config set corpus PATH
    python copy_lab.py search "social proof" --limit 10
    python copy_lab.py extract --find "AIDA formula"
    python copy_lab.py index
    python copy_lab.py mine --per-theme 75 --min-score 7
    python copy_lab.py ingest
    python copy_lab.py ocr SOURCE.pdf --out-dir OUTPUT
    python copy_lab.py transcribe SOURCE.m4b --model LOCAL_MODEL --out-dir OUTPUT
    python copy_lab.py validate --strict
"""

from __future__ import annotations

import argparse
import sys

import configure
import extract_lesson
import index_corpus
import ingest_sources
import mine_corpus
import ocr_pdf
import search_corpus
import transcribe_media
import validate_library

VERSION = "2.7.3"

COMMANDS = {
    "search": search_corpus.main,
    "extract": extract_lesson.main,
    "index": index_corpus.main,
    "mine": mine_corpus.main,
    "ingest": ingest_sources.main,
    "ocr": ocr_pdf.main,
    "transcribe": transcribe_media.main,
    "validate": validate_library.main,
    "config": configure.main,
}


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments and arguments[0] == "doctor":
        return configure.main(["doctor", *arguments[1:]])
    if arguments and arguments[0] in COMMANDS:
        return COMMANDS[arguments[0]](arguments[1:])

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--version", action="version", version=f"copy-lab {VERSION}")
    parser.add_argument("command", nargs="?", choices=[*COMMANDS, "doctor"])
    args = parser.parse_args(arguments)
    if args.command is None:
        parser.print_help()
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
