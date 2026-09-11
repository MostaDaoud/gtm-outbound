"""Search the course corpus and optional local book/document index.

Two modes:

  * ``--store`` (default when ``mined.jsonl`` exists) searches the pre-mined
    passages. Fast, and every hit already carries a citation.
  * ``--full`` re-reads every transcript. Slower, but finds anything the miner
    scored below threshold.

All terms must match by default. Results are ranked by term coverage, exact
phrase matches, frequency, proximity, and the miner's teaching-value score.

Usage:
    python search_corpus.py "risk reversal" guarantee [--limit 15] [--course NAME] [--full]
    python search_corpus.py scarcity --json
    python search_corpus.py headline hook --any --diverse
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict, deque
from pathlib import Path

from corpus_lib import (
    build_passages,
    find_corpus_root,
    iter_transcript_paths,
    load_lesson,
    normalize,
)
from copy_lab_config import resolve_corpus, resolve_mined_store, resolve_source_store


def _positions(text_normalized: str, term: str) -> list[int]:
    """Return whole-term positions in normalized text."""
    padded = f" {text_normalized} "
    needle = f" {term} "
    positions: list[int] = []
    start = 0
    while True:
        index = padded.find(needle, start)
        if index < 0:
            return positions
        positions.append(max(index - 1, 0))
        start = index + 1


def score_match(
    text_normalized: str,
    terms: list[str],
    *,
    require_all: bool = True,
) -> tuple[int, list[str]]:
    """Rank a candidate and return ``(score, matched_terms)``.

    Whole-word or whole-phrase matching prevents short terms from matching
    inside unrelated words. Default AND semantics avoids weak one-term hits for
    multi-term research queries.
    """
    first_positions: list[int] = []
    matched_terms: list[str] = []
    frequencies: dict[str, int] = {}
    for term in terms:
        positions = _positions(text_normalized, term)
        if positions:
            matched_terms.append(term)
            first_positions.append(positions[0])
            frequencies[term] = len(positions)

    if not matched_terms or (require_all and len(matched_terms) != len(terms)):
        return (0, matched_terms)

    score = len(matched_terms) * 20
    score += sum(min(frequencies[term], 3) * 2 for term in matched_terms)
    score += sum(10 for term in matched_terms if " " in term)
    if len(matched_terms) == len(terms):
        score += 20
    if len(first_positions) > 1:
        span = max(first_positions) - min(first_positions)
        if span <= 60:
            score += 20
        elif span <= 200:
            score += 10
    return (score, matched_terms)


def search_store(
    store: Path,
    terms: list[str],
    course: str | None,
    *,
    require_all: bool = True,
) -> list[dict]:
    """Search the mined passage store."""
    results: list[dict] = []
    with store.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            filter_text = " ".join(
                str(record.get(key, "")) for key in ("course", "title", "author")
            )
            if course and course.lower() not in filter_text.lower():
                continue
            rank, matched_terms = score_match(
                normalize(record.get("text", "")), terms, require_all=require_all
            )
            if rank:
                results.append(
                    {
                        **record,
                        "source_type": record.get("source_type", "course"),
                        "match_score": rank,
                        "matched_terms": matched_terms,
                    }
                )
    return results


def search_full(
    root: Path,
    terms: list[str],
    course: str | None,
    *,
    require_all: bool = True,
) -> list[dict]:
    """Search every transcript from scratch."""
    results: list[dict] = []
    for path in iter_transcript_paths(root):
        try:
            lesson = load_lesson(path, root)
        except OSError:
            continue
        if course and course.lower() not in lesson.course.lower():
            continue
        for passage in build_passages(lesson):
            rank, matched_terms = score_match(
                normalize(passage.text), terms, require_all=require_all
            )
            if rank:
                results.append(
                    {
                        "course": passage.course,
                        "source_type": "course",
                        "section": passage.section,
                        "lesson": passage.lesson,
                        "timestamp": passage.timestamp,
                        "path": passage.path,
                        "text": passage.text,
                        "match_score": rank,
                        "matched_terms": matched_terms,
                    }
                )
    return results


def diversify_by_course(results: list[dict], limit: int) -> list[dict]:
    """Round-robin ranked results by course to surface minority viewpoints."""
    buckets: dict[str, deque[dict]] = defaultdict(deque)
    order: list[str] = []
    for result in results:
        course = result.get("course", "")
        if course not in buckets:
            order.append(course)
        buckets[course].append(result)

    selected: list[dict] = []
    while len(selected) < limit and order:
        next_order: list[str] = []
        for course in order:
            bucket = buckets[course]
            if bucket and len(selected) < limit:
                selected.append(bucket.popleft())
            if bucket:
                next_order.append(course)
        order = next_order
    return selected


def result_location(item: dict) -> str:
    """Format a course or external-source citation for terminal output."""
    if item.get("source_type") != "course" and item.get("citation"):
        return str(item["citation"])
    path_label = " > ".join(
        p for p in (item.get("course"), item.get("section"), item.get("lesson")) if p
    )
    timestamp = item.get("timestamp", "")
    return f"{path_label} @ {timestamp}" if timestamp else path_label


def main(argv: list[str] | None = None) -> int:
    # Results are verbatim transcript text and can contain characters a cp1252
    # console cannot encode. Without this, printing a hit raises
    # UnicodeEncodeError instead of returning the result.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):  # non-reconfigurable stream
        pass

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("terms", nargs="+", help="Search terms (quote multi-word phrases)")
    parser.add_argument("--limit", type=int, default=15, help="Maximum results")
    parser.add_argument("--course", default=None, help="Restrict to a course (substring match)")
    parser.add_argument("--store", type=Path, default=None, help="Mined course passage store")
    parser.add_argument("--book-store", type=Path, default=None, help="Local book passage store")
    parser.add_argument(
        "--source",
        choices=("corpus", "books", "all"),
        default="all",
        help="Source collection to search (default: all)",
    )
    parser.add_argument("--corpus", type=Path, default=None, help="Corpus root for --full")
    parser.add_argument("--full", action="store_true", help="Search raw transcripts instead")
    parser.add_argument(
        "--any",
        action="store_true",
        help="Match any term instead of requiring all terms",
    )
    parser.add_argument(
        "--diverse",
        action="store_true",
        help="Round-robin results by course after ranking",
    )
    parser.add_argument(
        "--min-match-score",
        type=int,
        default=0,
        help="Discard results below this query-match score",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of markdown")
    args = parser.parse_args(argv)

    terms = [normalize(t) for t in args.terms if normalize(t)]
    if not terms:
        print("error: no usable search terms", file=sys.stderr)
        return 2

    require_all = not args.any
    results: list[dict] = []
    searched: list[str] = []

    if args.source in {"corpus", "all"}:
        store = resolve_mined_store(args.store)
        if args.full or not store.is_file():
            try:
                root = resolve_corpus(args.corpus) if args.corpus else find_corpus_root()
            except FileNotFoundError as exc:
                if args.source == "corpus":
                    print(f"error: {exc}", file=sys.stderr)
                    return 2
            else:
                results.extend(search_full(root, terms, args.course, require_all=require_all))
                searched.append(f"full corpus at {root}")
        else:
            results.extend(search_store(store, terms, args.course, require_all=require_all))
            searched.append(f"mined corpus store at {store}")

    if args.source in {"books", "all"}:
        book_store = resolve_source_store(args.book_store)
        if book_store.is_file():
            results.extend(search_store(book_store, terms, args.course, require_all=require_all))
            searched.append(f"local source store at {book_store}")
        elif args.source == "books":
            print(
                f"error: local source store not found: {book_store}; run copy_lab.py ingest",
                file=sys.stderr,
            )
            return 2

    source = "; ".join(searched) or "no configured sources"

    results = [result for result in results if result["match_score"] >= args.min_match_score]
    results.sort(key=lambda r: (r["match_score"], r.get("score", 0)), reverse=True)
    results = (
        diversify_by_course(results, args.limit)
        if args.diverse
        else results[: args.limit]
    )

    if args.json:
        print(json.dumps({"source": source, "count": len(results), "results": results},
                         indent=2, ensure_ascii=False))
        return 0

    if not results:
        mode = "any" if args.any else "all"
        print(f"No matches for {' + '.join(args.terms)} ({mode}-term mode) in {source}.")
        return 1

    print(f"# Search: {' + '.join(args.terms)}")
    print(f"\n_{len(results)} result(s) from {source}._\n")
    for item in results:
        location = result_location(item)
        print(f"- **{location}**")
        print(f"  {item.get('text', '').strip()}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
