"""Mine the whole transcript corpus into attributed, theme-sorted digests.

Reads every transcript file, windows it into passages, scores each passage for
teaching value, and writes:

  * ``digests/<theme>.md``  -- top passages per theme, grouped by course,
                              each with a course > section > lesson @ timestamp citation
  * ``mined.jsonl``         -- every passage above threshold (the searchable store)
  * ``mining_report.json``  -- coverage and yield statistics

Scoring rewards teaching language ("the key is", "never", "step one"), named
formulas (AIDA, PAS, BAB), enumerated lists, and concrete numbers. Selection
uses a sqrt-weighted per-course quota so a 798-lesson course cannot crowd out a
4-lesson one while still earning the largest share.

Usage:
    python mine_corpus.py [--corpus PATH] [--out DIR] [--per-theme N] [--min-score N]
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from corpus_lib import (
    Passage,
    build_passages,
    count_hits,
    dedupe_passages,
    find_corpus_root,
    fingerprint,
    iter_transcript_paths,
    jaccard,
    load_lesson,
    normalize,
    shingles,
)
from copy_lab_config import resolve_data_dir

# --------------------------------------------------------------------------
# Theme vocabulary
# --------------------------------------------------------------------------

THEMES: dict[str, list[str]] = {
    "frameworks": [
        "formula", "framework", "structure", "template", "blueprint", "process",
        "aida", "pas", "pastor", "quest", "bab", "fab", "acronym", "four steps",
        "attention interest desire", "problem agitate", "before after bridge",
        "features advantages benefits", "hook story offer", "outline", "skeleton",
    ],
    "psychology": [
        "system 1", "system 2", "bias", "heuristic", "cognitive", "subconscious",
        "unconscious", "anchoring", "scarcity", "social proof", "reciprocity",
        "loss aversion", "priming", "nudge", "persuasion", "behavioral",
        "psychology", "emotion", "fear", "motivation", "dopamine", "attention",
        "perception", "memory", "decision making", "autopilot",
    ],
    "headlines": [
        "headline", "hook", "subject line", "opening line", "first sentence",
        "first line", "curiosity", "grab attention", "title", "lead", "big idea",
        "attention grabbing", "scroll stopping", "thumb stopping",
    ],
    "sales_pages": [
        "sales page", "landing page", "vsl", "video sales letter", "long form",
        "sales letter", "above the fold", "close", "closing", "call to action",
        "cta", "bullets", "objection", "guarantee section", "testimonial",
        "proof", "conversion", "funnel", "opt in", "squeeze page",
    ],
    "emails": [
        "email", "newsletter", "sequence", "autoresponder", "broadcast",
        "cold email", "outreach", "follow up", "dm", "direct message",
        "inbox", "open rate", "click rate", "unsubscribe", "welcome sequence",
        "nurture", "drip",
    ],
    "offers": [
        "offer", "price", "pricing", "guarantee", "bonus", "upsell", "downsell",
        "tier", "discount", "risk reversal", "value stack", "package",
        "retainer", "charge", "premium", "anchor price", "payment plan",
    ],
    "voice": [
        "voice", "tone", "authentic", "sound like", "personality", "story",
        "storytelling", "cliche", "jargon", "write like you talk", "conversational",
        "human", "relatable", "vulnerability", "brand voice", "style", "rhythm",
        "boring", "generic", "sound robotic", "stiff", "empathize",
        "design thinking", "narrative arc", "protagonist",
    ],
    "ai_workflow": [
        "chatgpt", "claude", "gpt", "prompt", "llm", "artificial intelligence",
        "ai generated", "ai writing", "model", "automate", "midjourney",
        "training data", "context window", "ai tool", "ai slop", "custom gpt",
    ],
    "examples": [
        "for example", "for instance", "here is an example", "heres an example",
        "let me show you", "case study", "swipe", "real example", "like this",
        "such as", "example of",
    ],
    "client_work": [
        "client", "freelance", "portfolio", "proposal", "pitch", "contract",
        "invoice", "scope", "referral", "cold call", "agency", "retainer",
        "get clients", "first client", "rate", "hourly", "project fee",
        "niche", "business", "enablement", "sales play", "battlecard",
        "buyer journey", "sales process", "coaching", "onboarding",
        "customer success",
    ],
    "positioning": [
        "positioning", "value proposition", "differentiation", "messaging",
        "messaging canvas", "messaging architecture", "brand story",
        "brand strategy", "brand building", "brand plan", "brand maturity",
        "category", "purpose", "point of view", "narrative", "pillars",
        "claim", "proof point", "competitive advantage", "unique mechanism",
        "touch point", "layers and lenses",
    ],
    "research": [
        "segmentation", "segment", "persona", "buyer persona", "icp",
        "ideal customer", "market research", "competitive intelligence",
        "competitor research", "win loss", "battlecard", "audit",
        "customer interview", "survey", "voice of customer", "jobs to be done",
        "firmographic", "demographic", "data source", "insight",
        "content audit", "topic research", "themes and topics",
        "qualitative", "coding", "content marketing", "content strategy",
        "editorial", "distill", "data collection", "theme", "themes",
        "topic", "topics", "buying insights", "closed lost", "closed won",
        "win rate", "abandonment", "respondents",
    ],
}

# Language that marks a passage as instructional rather than filler.
STRONG_SIGNALS: list[str] = [
    "the key is", "the secret", "the trick is", "rule of thumb", "here is how",
    "heres how", "the biggest mistake", "most people", "always", "never",
    "step one", "step 1", "first step", "the formula", "the framework",
    "what you want to do", "make sure you", "the reason why", "this is why",
    "for example", "for instance", "let me show you", "the point is",
    "boils down to", "the whole idea", "pro tip", "best practice",
    "you should", "you need to", "the way to", "instead of", "rather than",
    "the difference between", "works because", "the goal is", "in other words",
    # Structured-lecture register. The conversational courses are full of
    # "always" and "most people"; the curriculum courses teach in this voice
    # instead, and without these they score far below their actual value.
    "the goal here is", "our objectives", "the way that you", "the first step",
    "the process is", "key takeaway", "at a high level", "what we are doing is",
    "let us start with", "the five", "the six", "the three",
]

FORMULA_NAMES: list[str] = [
    "aida", "pas", "pastor", "quest", "bab", "fab", "four ps", "4 ps",
    "attention interest desire action", "problem agitate solution",
    "before after bridge", "features advantages benefits", "hook story offer",
    "awareness levels", "sophistication", "the 1 2 3 4 formula",
]

ENUMERATION = re.compile(
    r"\b(one|two|three|four|five|six|seven|eight|nine|ten|\d{1,2})\s+"
    r"(ways|steps|rules|things|reasons|elements|parts|types|questions|tips|"
    r"mistakes|principles|components|pillars|stages|levels)\b"
)
HAS_DIGIT = re.compile(r"\d")

# Spoken filler. Whisper preserves every "right?" and "you know", which inflates
# the score of rambling passages unless they are penalized.
FILLER = re.compile(
    r"\b(like|you know|right|um+|uh+|kind of|sort of|i mean|basically|"
    r"actually|gonna|wanna|stuff|whatever|okay|so yeah)\b"
)

MIN_PASSAGE_WORDS = 25


# --------------------------------------------------------------------------
# Scoring
# --------------------------------------------------------------------------

def score_passage(passage: Passage) -> tuple[int, dict[str, int], list[str]]:
    """Score one passage for teaching value and assign it to themes.

    Args:
        passage: The passage to score.

    Returns:
        ``(score, theme_hit_counts, matched_signals)``. A passage with no theme
        hits scores zero and should be discarded.
    """
    if len(passage.text.split()) < MIN_PASSAGE_WORDS:
        return (0, {}, [])

    text = normalize(passage.text)

    theme_hits: dict[str, int] = {}
    for theme, terms in THEMES.items():
        hits, _ = count_hits(text, terms)
        if hits:
            theme_hits[theme] = hits

    if not theme_hits:
        return (0, {}, [])

    signal_count, matched_signals = count_hits(text, STRONG_SIGNALS)
    formula_count, matched_formulas = count_hits(text, FORMULA_NAMES)

    score = 2 * sum(theme_hits.values())
    score += 3 * signal_count
    score += 4 * formula_count
    if ENUMERATION.search(text):
        score += 3
    if HAS_DIGIT.search(passage.text):
        score += 1

    # Rambling, filler-dense speech loses points proportional to how much of the
    # passage is filler. Spoken transcripts run 8-15% filler even when the
    # content is excellent, so this stays mild -- it breaks ties, it does not
    # disqualify.
    word_count = max(len(text.split()), 1)
    filler_ratio = len(FILLER.findall(text)) / word_count
    score -= int(filler_ratio * 22)

    return (max(score, 0), theme_hits, matched_signals + matched_formulas)


# --------------------------------------------------------------------------
# Cross-file deduplication
# --------------------------------------------------------------------------

# Shingles this common are boilerplate ("so what you want to do is") and would
# make every passage a candidate for every other. Skip them.
MAX_SHINGLE_BUCKET = 40

# A candidate must share at least this many shingles before Jaccard is computed.
MIN_SHARED_SHINGLES = 3


class _Union:
    """Minimal union-find over passage positions."""

    def __init__(self, size: int) -> None:
        self._parent = list(range(size))

    def find(self, item: int) -> int:
        while self._parent[item] != item:
            self._parent[item] = self._parent[self._parent[item]]
            item = self._parent[item]
        return item

    def union(self, left: int, right: int) -> None:
        root_left, root_right = self.find(left), self.find(right)
        if root_left != root_right:
            self._parent[root_right] = root_left


def _canonical_rank(entry: dict) -> tuple:
    """Sort key deciding which copy of a repeated passage to keep.

    Prefers the shallowest path — a lesson filed directly under a course folder
    beats the same lesson nested inside a sub-course — then falls back to
    alphabetical order so the choice is stable across runs.
    """
    path = Path(entry["passage"].path)
    return (len(path.parts), str(path), entry["passage"].timestamp)


def collapse_across_corpus(
    entries: list[dict],
    near_threshold: float = 0.85,
) -> tuple[list[dict], dict[str, int]]:
    """Collapse passages that repeat across the corpus into one canonical entry.

    Courses republish the same lesson under several folders, so an identical
    passage can appear three or four times. Per-file deduplication cannot see
    that, and the copies crowd distinct material out of the theme digests.

    Exact repeats match on a normalized fingerprint. Near repeats — separate
    whisper runs over the same footage, differing by a word — match on 5-word
    shingle Jaccard similarity, compared only between passages that already
    share several shingles.

    Args:
        entries: Scored passage records, each with a ``passage`` key.
        near_threshold: Jaccard score at or above which two passages are treated
            as the same passage. Pass 1.0 to disable near-duplicate matching.

    Returns:
        ``(collapsed_entries, stats)``. Each collapsed entry gains
        ``occurrences``, ``duplicate_locations``, and ``also_in``.
    """
    if not entries:
        return ([], {"exact_groups": 0, "near_groups": 0, "copies_removed": 0})

    # Stage 1 — exact repeats.
    exact: dict[str, list[int]] = defaultdict(list)
    for index, entry in enumerate(entries):
        exact[fingerprint(entry["passage"].text)].append(index)

    representatives: list[int] = []
    members: list[list[int]] = []
    for group in exact.values():
        group.sort(key=lambda i: _canonical_rank(entries[i]))
        representatives.append(group[0])
        members.append(group)

    exact_groups = sum(1 for group in members if len(group) > 1)

    # Stage 2 — near repeats among the representatives.
    near_groups = 0
    if near_threshold < 1.0 and len(representatives) > 1:
        sets = [shingles(entries[rep]["passage"].text) for rep in representatives]

        by_shingle: dict[str, list[int]] = defaultdict(list)
        for position, shingle_set in enumerate(sets):
            for shingle in shingle_set:
                by_shingle[shingle].append(position)

        union = _Union(len(representatives))
        for position, shingle_set in enumerate(sets):
            shared: Counter[int] = Counter()
            for shingle in shingle_set:
                bucket = by_shingle[shingle]
                if len(bucket) > MAX_SHINGLE_BUCKET:
                    continue
                for other in bucket:
                    if other > position:
                        shared[other] += 1
            for other, count in shared.items():
                if count < MIN_SHARED_SHINGLES:
                    continue
                if jaccard(sets[position], sets[other]) >= near_threshold:
                    union.union(position, other)

        clusters: dict[int, list[int]] = defaultdict(list)
        for position in range(len(representatives)):
            clusters[union.find(position)].append(position)

        merged: list[list[int]] = []
        for positions in clusters.values():
            combined: list[int] = []
            for position in positions:
                combined.extend(members[position])
            merged.append(combined)
            if len(positions) > 1:
                near_groups += 1
        members = merged

    # Build one entry per group, keeping the canonical copy.
    collapsed: list[dict] = []
    copies_removed = 0
    for group in members:
        group.sort(key=lambda i: _canonical_rank(entries[i]))
        canonical = dict(entries[group[0]])
        canonical["score"] = max(entries[i]["score"] for i in group)
        canonical["occurrences"] = sum(
            entries[i].get("local_repeats", 1) for i in group
        )
        canonical["duplicate_locations"] = len(group) - 1
        canonical["also_in"] = [
            {
                "course": entries[i]["passage"].course,
                "section": entries[i]["passage"].section,
                "lesson": entries[i]["passage"].lesson,
                "timestamp": entries[i]["passage"].timestamp,
            }
            for i in group[1:6]
        ]
        collapsed.append(canonical)
        copies_removed += len(group) - 1

    collapsed.sort(key=lambda entry: entry["score"], reverse=True)
    return (
        collapsed,
        {
            "exact_groups": exact_groups,
            "near_groups": near_groups,
            "copies_removed": copies_removed,
        },
    )


# --------------------------------------------------------------------------
# Selection
# --------------------------------------------------------------------------

def course_quotas(
    course_words: dict[str, int],
    total_slots: int,
    minimum: int = 3,
) -> dict[str, int]:
    """Allocate digest slots across courses using sqrt-weighted shares.

    A raw proportional split would give a 798-lesson course ~85% of every
    digest. Square-rooting the share compresses that dominance while still
    letting the largest course contribute the most material.

    Keep ``minimum`` low relative to ``total_slots``. The floor is paid to every
    course present in the theme, so with many courses a generous floor consumes
    the whole digest and the weighting stops doing anything — at 17 courses a
    floor of 4 already claims 68 of 75 slots.

    Args:
        course_words: Word count per course.
        total_slots: Slots to distribute.
        minimum: Floor per course so small courses always appear.

    Returns:
        Slots per course.
    """
    total = sum(course_words.values()) or 1
    weights = {name: math.sqrt(words / total) for name, words in course_words.items()}
    weight_sum = sum(weights.values()) or 1.0
    return {
        name: max(minimum, round(total_slots * weight / weight_sum))
        for name, weight in weights.items()
    }


def select_for_theme(
    scored: list[dict],
    course_words: dict[str, int],
    limit: int,
) -> list[dict]:
    """Pick the top passages for one theme under per-course quotas.

    Args:
        scored: Collapsed passage entries for this theme.
        course_words: Word count per course, for quota weighting.
        limit: Target number of passages.

    Returns:
        Selected entries, highest score first.
    """
    by_course: dict[str, list[dict]] = defaultdict(list)
    for entry in scored:
        by_course[entry["passage"].course].append(entry)
    for items in by_course.values():
        items.sort(key=lambda entry: entry["score"], reverse=True)

    present = {name: course_words.get(name, 1) for name in by_course}
    quotas = course_quotas(present, limit)

    selected: list[dict] = []
    leftovers: list[dict] = []
    for name, items in by_course.items():
        quota = quotas.get(name, 0)
        selected.extend(items[:quota])
        leftovers.extend(items[quota:])

    # Unused capacity (courses with fewer passages than quota) goes to the best remainder.
    if len(selected) < limit:
        leftovers.sort(key=lambda entry: entry["score"], reverse=True)
        selected.extend(leftovers[: limit - len(selected)])

    selected.sort(key=lambda entry: entry["score"], reverse=True)
    return selected[:limit]


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------

def write_digest(
    path: Path,
    theme: str,
    selected: list[dict],
    pool_size: int,
) -> None:
    """Write one theme digest as markdown, grouped by course.

    Entries carry the canonical location. Where the same passage also appears
    elsewhere in the corpus, the alternate lessons are listed beneath it so the
    distillation step can cite the canonical one and know the repeat is not a
    separate teaching.
    """
    grouped: dict[str, list[dict]] = defaultdict(list)
    for entry in selected:
        grouped[entry["passage"].course].append(entry)

    lines = [
        f"# Digest: {theme}",
        "",
        f"Selected {len(selected)} of {pool_size} unique scoring passages. "
        "Each entry is verbatim transcript text with its source citation. "
        "Passages repeated elsewhere in the corpus are collapsed to their "
        "canonical location, with the repeats listed underneath.",
        "",
    ]
    for course in sorted(grouped):
        lines.append(f"## {course}")
        lines.append("")
        for entry in grouped[course]:
            passage = entry["passage"]
            location = " > ".join(p for p in (passage.section, passage.lesson) if p)
            copies = entry.get("duplicate_locations", 0)
            repeat = f" +{copies} repeats" if copies else ""
            lines.append(
                f"- **[{entry['score']}{repeat}] {location} @ {passage.timestamp}**"
            )
            lines.append(f"  {passage.text}")
            for other in entry.get("also_in", []):
                other_location = " > ".join(
                    p for p in (other["section"], other["lesson"]) if p
                )
                lines.append(
                    f"  - _also in: {other['course']} > {other_location} "
                    f"@ {other['timestamp']}_"
                )
            lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--corpus", type=Path, default=None, help="Corpus root directory")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output directory (default: external copy-lab data directory)",
    )
    parser.add_argument("--per-theme", type=int, default=80, help="Passages per digest")
    parser.add_argument("--min-score", type=int, default=8, help="Score threshold to keep")
    parser.add_argument(
        "--near-threshold",
        type=float,
        default=0.85,
        help="Jaccard similarity treated as the same passage (1.0 disables near-dedupe)",
    )
    parser.add_argument("--quiet", action="store_true", help="Suppress progress output")
    args = parser.parse_args(argv)

    try:
        root = args.corpus.resolve() if args.corpus else find_corpus_root()
        output = (
            args.out.expanduser().resolve()
            if args.out
            else resolve_data_dir(corpus=root, for_write=True) / "mining"
        )
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    digests_dir = output / "digests"
    digests_dir.mkdir(parents=True, exist_ok=True)

    course_words: dict[str, int] = defaultdict(int)
    files_read = 0
    files_empty = 0
    passages_total = 0

    # Phase 1 — read, window, and score every file. Deduplication has to wait
    # until the whole corpus is in hand, since repeats span course folders.
    entries: list[dict] = []
    for path in iter_transcript_paths(root):
        try:
            lesson = load_lesson(path, root)
        except OSError as exc:
            print(f"warn: skipping {path}: {exc}", file=sys.stderr)
            continue

        files_read += 1
        if not lesson.segments:
            files_empty += 1
            continue

        course_words[lesson.course] += lesson.word_count
        passages = build_passages(lesson)
        passages_total += len(passages)

        for passage, local_repeats in dedupe_passages(passages):
            score, theme_hits, signals = score_passage(passage)
            if score < args.min_score or not theme_hits:
                continue
            entries.append(
                {
                    "passage": passage,
                    "score": score,
                    "themes": theme_hits,
                    "signals": signals[:6],
                    "local_repeats": local_repeats,
                }
            )

        if not args.quiet and files_read % 100 == 0:
            print(f"  processed {files_read} files, kept {len(entries)} passages",
                  file=sys.stderr)

    kept_total = len(entries)

    # Phase 2 — collapse repeats across the whole corpus.
    if not args.quiet:
        print(f"  collapsing duplicates across {kept_total} passages...",
              file=sys.stderr)
    collapsed, dedupe_stats = collapse_across_corpus(entries, args.near_threshold)

    # Phase 3 — persist and bucket by theme.
    jsonl_path = output / "mined.jsonl"
    theme_pools: dict[str, list[dict]] = defaultdict(list)
    with jsonl_path.open("w", encoding="utf-8") as store:
        for entry in collapsed:
            passage = entry["passage"]
            record = {
                "score": entry["score"],
                "themes": entry["themes"],
                "signals": entry["signals"],
                "course": passage.course,
                "section": passage.section,
                "lesson": passage.lesson,
                "timestamp": passage.timestamp,
                "path": passage.path,
                "text": passage.text,
                "occurrences": entry["occurrences"],
                "duplicate_locations": entry["duplicate_locations"],
                "also_in": entry["also_in"],
            }
            store.write(json.dumps(record, ensure_ascii=False) + "\n")

            # A passage can serve more than one theme; rank it in each.
            for theme in entry["themes"]:
                theme_pools[theme].append(entry)

    theme_stats = {}
    for theme in THEMES:
        pool = theme_pools.get(theme, [])
        selected = select_for_theme(pool, dict(course_words), args.per_theme)
        write_digest(digests_dir / f"{theme}.md", theme, selected, len(pool))
        theme_stats[theme] = {"pool": len(pool), "selected": len(selected)}

    report = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "corpus_root": str(root),
        "files_read": files_read,
        "files_without_transcript": files_empty,
        "passages_windowed": passages_total,
        "passages_kept": kept_total,
        "passages_unique": len(collapsed),
        "deduplication": {
            "near_threshold": args.near_threshold,
            "exact_repeat_groups": dedupe_stats["exact_groups"],
            "near_repeat_groups": dedupe_stats["near_groups"],
            "copies_removed": dedupe_stats["copies_removed"],
        },
        "min_score": args.min_score,
        "per_theme": args.per_theme,
        "courses": dict(sorted(course_words.items())),
        "themes": theme_stats,
        "outputs": {"digests": str(digests_dir), "jsonl": str(jsonl_path)},
    }
    (output / "mining_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(json.dumps({k: report[k] for k in
                      ("files_read", "files_without_transcript", "passages_windowed",
                       "passages_kept", "passages_unique", "deduplication",
                       "themes")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
