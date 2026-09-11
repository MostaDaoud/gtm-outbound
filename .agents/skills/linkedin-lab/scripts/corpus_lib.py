"""Shared helpers for reading the linkedin-lab transcript corpus.

Every file in the corpus is a `watch`-generated video report: a metadata header,
then a `## Transcript` section containing a fenced block of `[MM:SS] text` lines.
This module turns those files into clean, citable passages.

Used by index_corpus.py, search_corpus.py, extract_lesson.py, mine_corpus.py
and validate_library.py.
"""

from __future__ import annotations

import csv
import hashlib
import os
import re
import unicodedata
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Iterator, Sequence

from linkedin_lab_config import resolve_corpus, resolve_course_map

# --------------------------------------------------------------------------
# Corpus location
# --------------------------------------------------------------------------

TRANSCRIPT_SUFFIXES = (".md", ".txt")

# Some courses arrive as a set of sibling module folders at the corpus root
# ("16-Attention Basics", "18-Cognitive Biases", …) rather than as one folder
# per course. course_map.json rolls those up so citations name the course a
# reader would recognise instead of the module folder it happened to ship in.
@lru_cache(maxsize=1)
def load_course_map() -> dict[str, str]:
    """Return the folder -> course-name mapping, or {} when none is configured.

    Resolution is handled by :mod:`linkedin_lab_config`. Keys beginning with ``_``
    are comments. Any failure to read or parse is non-fatal.
    """
    import json

    candidate = resolve_course_map()
    if candidate.is_file():
        try:
            data = json.loads(candidate.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}
        return {
            k: v for k, v in data.items()
            if not k.startswith("_") and isinstance(v, str)
        }
    return {}


def find_corpus_root(start: Path | None = None) -> Path:
    """Locate the `_transcripts` corpus directory.

    Resolution order is explicit configuration, the current workspace, then
    ancestors of ``start`` and the script directory.

    Args:
        start: Directory to begin the upward search from. Defaults to this
            script's location.

    Returns:
        Path to the corpus root.

    Raises:
        FileNotFoundError: If no corpus directory can be located.
    """
    return resolve_corpus(start=start)


def read_text(path: Path) -> str:
    """Read a file as UTF-8, replacing undecodable bytes rather than failing."""
    return path.read_text(encoding="utf-8", errors="replace")


# --------------------------------------------------------------------------
# Transcript parsing
# --------------------------------------------------------------------------

_TIMESTAMP_LINE = re.compile(r"^\[(\d{1,2}:\d{2}(?::\d{2})?)\]\s*(.*)$")
_FENCE = re.compile(r"^\s*```")
_TRANSCRIPT_HEADING = re.compile(r"^##\s+Transcript\s*$", re.IGNORECASE)
_SOURCE_NOTE = re.compile(r"^_Source:.*_\s*$")
_SENTENCE_END = re.compile(r"[.!?][\"')\]]*$")


@dataclass(frozen=True)
class Segment:
    """One timestamped line of transcript."""

    timestamp: str
    text: str

    @property
    def seconds(self) -> int:
        """Timestamp converted to whole seconds."""
        parts = [int(p) for p in self.timestamp.split(":")]
        while len(parts) < 3:
            parts.insert(0, 0)
        hours, minutes, seconds = parts[-3:]
        return hours * 3600 + minutes * 60 + seconds


@dataclass
class Lesson:
    """A single transcript file with its corpus coordinates."""

    path: Path
    course: str
    section: str
    lesson: str
    segments: list[Segment] = field(default_factory=list)

    @property
    def word_count(self) -> int:
        return sum(len(s.text.split()) for s in self.segments)

    @property
    def citation(self) -> str:
        """Human-readable source label, e.g. ``Course > Section > Lesson``."""
        parts = [p for p in (self.course, self.section, self.lesson) if p]
        return " > ".join(parts)


def parse_segments(content: str) -> list[Segment]:
    """Extract timestamped segments from a watch-style transcript.

    Skips the metadata header and the `## Frames` section, reading only lines
    inside the transcript body. Files that do not match the expected shape fall
    back to any `[MM:SS]`-prefixed lines found anywhere in the document.

    Args:
        content: Full text of a transcript file.

    Returns:
        Segments in document order. Empty if the file holds no transcript.
    """
    lines = content.splitlines()
    segments: list[Segment] = []

    in_transcript = False
    for line in lines:
        if _TRANSCRIPT_HEADING.match(line):
            in_transcript = True
            continue
        if not in_transcript:
            continue
        if _FENCE.match(line) or _SOURCE_NOTE.match(line):
            continue
        if line.startswith("## "):  # a later section ends the transcript
            break
        match = _TIMESTAMP_LINE.match(line)
        if match:
            text = match.group(2).strip()
            if text:
                segments.append(Segment(match.group(1), text))

    if segments:
        return segments

    # Fallback: some files may lack the standard heading.
    for line in lines:
        match = _TIMESTAMP_LINE.match(line)
        if match and match.group(2).strip():
            segments.append(Segment(match.group(1), match.group(2).strip()))
    return segments


def derive_coordinates(path: Path, root: Path) -> tuple[str, str, str]:
    """Derive ``(course, section, lesson)`` from a path relative to the corpus root."""
    try:
        relative = path.relative_to(root)
    except ValueError:
        return ("", "", path.stem)

    parts = list(relative.parts)
    lesson = Path(parts[-1]).stem if parts else path.stem
    folder = parts[0] if len(parts) >= 2 else ""
    section_parts = list(parts[1:-1]) if len(parts) > 2 else []

    # Roll module folders up to their parent course. The original folder is kept
    # as the first section component, so nothing is lost and a citation still
    # points at the exact module the passage came from.
    course = load_course_map().get(folder, folder)
    if course != folder:
        section_parts.insert(0, folder)

    return (course, " / ".join(section_parts), lesson)


def load_lesson(path: Path, root: Path) -> Lesson:
    """Read and parse a single transcript file into a :class:`Lesson`."""
    course, section, lesson_name = derive_coordinates(path, root)
    return Lesson(
        path=path,
        course=course,
        section=section,
        lesson=lesson_name,
        segments=parse_segments(read_text(path)),
    )


def iter_transcript_paths(root: Path, *, include_documents: bool = False) -> Iterator[Path]:
    """Yield course transcripts under ``root``, sorted for stable output.

    Imported books use the reserved filename ``document.md``. They are source
    material, not video lessons, and are excluded unless a maintenance caller
    explicitly opts in.
    """
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in TRANSCRIPT_SUFFIXES:
            if path.name.startswith("_"):  # _progress.jsonl and friends
                continue
            if not include_documents and path.name.lower() == "document.md":
                continue
            yield path


def load_manifest(root: Path) -> dict[str, dict[str, str]]:
    """Load ``manifest.csv`` keyed by transcript path, if the file exists.

    Returns an empty mapping when the manifest is missing or unreadable, so
    callers can treat manifest data as optional enrichment.
    """
    manifest_path = root / "manifest.csv"
    if not manifest_path.is_file():
        return {}

    rows: dict[str, dict[str, str]] = {}
    try:
        with manifest_path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
            for row in csv.DictReader(handle):
                key = (row.get("transcript_path") or "").strip()
                if key:
                    rows[os.path.normcase(key)] = row
    except OSError:
        return {}
    return rows


# --------------------------------------------------------------------------
# Passage windowing
# --------------------------------------------------------------------------

@dataclass
class Passage:
    """A window of consecutive segments, sized for reading and citation."""

    text: str
    timestamp: str
    course: str
    section: str
    lesson: str
    path: str

    @property
    def citation(self) -> str:
        parts = [p for p in (self.course, self.section, self.lesson) if p]
        return f"{' > '.join(parts)} @ {self.timestamp}"


def build_passages(
    lesson: Lesson,
    min_words: int = 55,
    max_words: int = 120,
) -> list[Passage]:
    """Merge timestamped segments into sentence-aware passages.

    Whisper emits short fragments that are useless in isolation. This
    accumulates them until the window holds at least ``min_words`` and ends on
    a sentence boundary, with a hard stop at ``max_words``.

    Args:
        lesson: Parsed lesson to window.
        min_words: Soft lower bound before a boundary can close a window.
        max_words: Hard upper bound; forces a break even mid-sentence.

    Returns:
        Passages in document order.
    """
    passages: list[Passage] = []
    buffer: list[str] = []
    words = 0
    start_ts = ""

    def flush() -> None:
        nonlocal buffer, words, start_ts
        if buffer:
            passages.append(
                Passage(
                    text=" ".join(buffer).strip(),
                    timestamp=start_ts,
                    course=lesson.course,
                    section=lesson.section,
                    lesson=lesson.lesson,
                    path=str(lesson.path),
                )
            )
        buffer = []
        words = 0
        start_ts = ""

    for segment in lesson.segments:
        if not buffer:
            start_ts = segment.timestamp
        buffer.append(segment.text)
        words += len(segment.text.split())

        ends_sentence = bool(_SENTENCE_END.search(segment.text.strip()))
        if (words >= min_words and ends_sentence) or words >= max_words:
            flush()

    flush()
    return passages


# --------------------------------------------------------------------------
# Text normalization
# --------------------------------------------------------------------------

_PUNCT = re.compile(r"[^\w\s]")
_WS = re.compile(r"\s+")


def normalize(text: str) -> str:
    """Lowercase, strip accents and punctuation, collapse whitespace."""
    decomposed = unicodedata.normalize("NFKD", text)
    ascii_text = decomposed.encode("ascii", "ignore").decode("ascii")
    return _WS.sub(" ", _PUNCT.sub(" ", ascii_text.lower())).strip()


def fingerprint(text: str) -> str:
    """Stable hash of normalized text, for deduplicating repeated passages."""
    return hashlib.sha1(normalize(text).encode("utf-8")).hexdigest()[:16]


@lru_cache(maxsize=8192)
def _term_matcher(term: str) -> tuple[str, object] | None:
    """Build and cache a matcher for one search term.

    Compiling these once matters: mining runs tens of millions of term checks,
    and rebuilding the pattern each time dominates the runtime.
    """
    needle = normalize(term)
    if not needle:
        return None
    if " " in needle:
        return ("sub", needle)
    return ("re", re.compile(rf"\b{re.escape(needle)}\b"))


def count_hits(normalized: str, terms: Sequence[str]) -> tuple[int, list[str]]:
    """Count how many of ``terms`` appear in already-normalized text.

    Multi-word terms are matched as substrings; single words are matched on
    word boundaries so that "ai" does not match "said".

    Returns:
        ``(hit_count, matched_terms)``.
    """
    matched: list[str] = []
    for term in terms:
        matcher = _term_matcher(term)
        if matcher is None:
            continue
        kind, pattern = matcher
        if kind == "sub":
            if pattern in normalized:
                matched.append(term)
        elif pattern.search(normalized):  # type: ignore[union-attr]
            matched.append(term)
    return (len(matched), matched)


def shingles(text: str, size: int = 5) -> frozenset[str]:
    """Word n-grams of normalized text, for near-duplicate comparison.

    Whisper transcribes the same footage slightly differently across runs, so
    exact hashing misses repeats that differ by a word. Shingle overlap catches
    them.

    Args:
        text: Raw passage text.
        size: Words per shingle.

    Returns:
        The set of n-grams. Empty if the text is shorter than ``size`` words.
    """
    words = normalize(text).split()
    if len(words) < size:
        return frozenset()
    return frozenset(
        " ".join(words[i : i + size]) for i in range(len(words) - size + 1)
    )


def jaccard(left: frozenset[str], right: frozenset[str]) -> float:
    """Jaccard similarity of two shingle sets. Returns 0.0 if either is empty."""
    if not left or not right:
        return 0.0
    intersection = len(left & right)
    if not intersection:
        return 0.0
    return intersection / len(left | right)


def dedupe_passages(passages: Iterable[Passage]) -> list[tuple[Passage, int]]:
    """Collapse near-identical passages, keeping the first and counting repeats."""
    seen: dict[str, int] = {}
    ordered: list[list] = []
    for passage in passages:
        key = fingerprint(passage.text)
        if key in seen:
            ordered[seen[key]][1] += 1
            continue
        seen[key] = len(ordered)
        ordered.append([passage, 1])
    return [(item[0], item[1]) for item in ordered]
