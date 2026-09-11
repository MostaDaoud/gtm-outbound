---
name: copy-lab-mine
description: >
  Re-mine the copywriting transcript corpus, OCR scanned PDFs, transcribe long-form audio,
  ingest local books and captioned media, and refresh the copy-lab reference library. Rebuilds course indexes,
  creates page/chapter-aware source indexes, and updates distilled references.
  Use when the user adds a new course to the transcripts, says "re-mine the
  corpus", "refresh the library", "add a course to copy-lab", "rebuild the
  index", "update the references", "OCR this PDF", "process these scanned
  letters", "copy-lab mine", or when validate_library reports the references
  are stale or thin. This is the maintenance path for copy-lab, not a writing
  or critique workflow.
---

# Copy Lab — Mine

Rebuild the reference library from the transcript corpus. Run this when courses
are added, when the scoring vocabulary changes, or when the library drifts out
of date.

**Shared resources.** Resolve the sibling `../copy-lab/` directory from this
`SKILL.md` directory, then use the absolute path to
`scripts/copy_lab.py`. Mutable indexes, mining output, and configuration live
outside the installed skill. Never write maintenance output into a Claude skill
directory or into the transcript corpus.

## When to run

| Trigger | Scope |
|---------|-------|
| New course added to `_transcripts/` | Full re-mine, then update affected references |
| New book, document, captioned video, or audio added | Transcribe when needed, add it to the external source catalog, then ingest |
| `validate_library.py` reports stale or thin files | Targeted — re-mine, rewrite only what it flagged |
| Theme vocabulary needs changing | Edit `THEMES` in `mine_corpus.py`, full re-mine |
| Digests look noisy or thin | Retune scoring, full re-mine |

## Course names come from a map, not the folder

Some courses ship as a set of sibling **module folders** at the corpus root
(`16-Attention Basics`, `18-Cognitive Biases`, …) rather than one folder per
course. The bundled `assets/course_map.json` is the default map and rolls those
up:

```json
"18-Cognitive Biases": "Digital Psychology & Persuasion"
```

`derive_coordinates` applies the map and **keeps the original folder as the first
section component**, so nothing is lost — a citation still names the exact module
the passage came from. Folders absent from the map keep their own name as the
course.

**When a new module folder arrives, copy the bundled map into the external data
directory and edit that copy before mining.** Register it with:

```bash
python /absolute/path/to/copy-lab/scripts/copy_lab.py config set course_map /absolute/path/to/course_map.json
```

Otherwise the folder becomes its own single-module "course", which distorts the
per-course quotas and scatters one curriculum across several digest sections.

---

## Step 1 — Index

```bash
python /absolute/path/to/copy-lab/scripts/copy_lab.py index
```

Writes `corpus_index.json` in the configured external data directory. Check the
per-course lesson and word counts in the output against what you expect. A
course showing 0 words means its files did not parse — see Troubleshooting.
Files named `document.md` are deliberately excluded: they are document imports,
not course lessons, and belong in the source catalog below.

### Ingest books, documents, captioned videos, and audio

Keep the catalog outside the skill at `.copy-lab-data/sources/catalog.json`.
Each source needs `id`, `title`, `source_path`, and usually `author` and
`format`. A PDF may also name a `text_path` whose `[HH:MM]` markers encode page
numbers (`[01:16]` becomes page 76).

WebVTT captions use `format: "vtt"`, may set `source_type: "video"` and
`source_url`, and are indexed by timestamp. The ingester removes rolling
YouTube caption overlap before building 30-second citable passages. If edited
and original caption files are byte-identical, register only one source.

```bash
python /absolute/path/to/copy-lab/scripts/copy_lab.py ingest
```

This rebuilds `sources/passages.jsonl` and `sources/manifest.json`. The manifest
records source and extracted-text hashes, extraction method, locator type,
record counts, and OCR status. It never changes or copies the originals. EPUBs
are indexed by chapter; PDFs by page. Image-only PDFs remain `needs_ocr` until
a trusted OCR text source is supplied.

For image-only PDFs, generate that source outside `_transcripts/`:

```bash
python /absolute/path/to/copy-lab/scripts/copy_lab.py ocr /absolute/source.pdf \
  --out-dir /absolute/.copy-lab-data/ocr/source-id --jobs 4
```

The OCR command checkpoints every page as text plus confidence metadata. Rerun
the same command to resume. Only a complete run creates `document.md`; partial
runs create `document.partial.md`. Visually inspect representative pages and
every page reported under `low_quality_pages`. Then register `document.md` as
`text_path` and `ocr_manifest.json` as `ocr_manifest_path` in the catalog. The
ingester refuses partial OCR manifests or source-hash mismatches.

For audio or video without captions, run the resumable transcriber from a
project-local Python environment containing `faster-whisper`:

```bash
python -m pip install -r /absolute/path/to/copy-lab/requirements-transcription.txt
python /absolute/path/to/copy-lab/scripts/copy_lab.py transcribe /absolute/source.m4b \
  --model /absolute/local-faster-whisper-model \
  --out-dir /absolute/.copy-lab-data/transcription/source-id
```

The transcriber uses embedded chapters when available and divides long chapters
into bounded spans. It writes `progress.jsonl`, `transcript.vtt`, and a
hash-bound `transcription_manifest.json`. Rerun the identical command to resume.
Register the original media as `source_path`, the WebVTT as `text_path`, the
media extension as `format`, and the manifest as `transcript_manifest_path`.
The ingester rejects incomplete transcripts and source or transcript hash drift.

## Step 2 — Mine

```bash
python /absolute/path/to/copy-lab/scripts/copy_lab.py mine --per-theme 75 --min-score 7
```

## Output artifacts

Produces the following under the configured external data directory:

- `mining/digests/{theme}.md` — top passages per theme, grouped by
  course, each carrying `course > lesson @ timestamp`
- `mining/mined.jsonl` — every unique passage above threshold; this is
  what `search_corpus.py` searches
- `mining/mining_report.json` — coverage, yield, and dedupe statistics

**Deduplication runs corpus-wide, after scoring.** Courses republish the same
lesson under several folders, so an identical passage can appear three or four
times and crowd distinct material out of the digests. Exact repeats match on a
normalized fingerprint; near repeats — separate whisper runs over the same
footage — match on 5-word shingle overlap at `--near-threshold` (default 0.85,
set to 1.0 to disable). The canonical copy is the one at the shallowest path,
chosen deterministically; the rest appear as `also in:` lines beneath it.

**Verify coverage before going further.** In `mining_report.json`:

- `files_read` should equal the file count from the index
- `files_without_transcript` should be 0
- Each theme's `pool` should comfortably exceed `per_theme`, so the selector is
  actually selecting rather than taking everything available

## Step 3 — Calibrate if the yield is wrong

The threshold is the main lever, and the right value depends on the corpus.

| Symptom | Fix |
|---------|-----|
| Pools ≈ selected count | Threshold too high — lower `--min-score` |
| Digests full of rambling | Threshold too low, or raise the filler penalty in `mine_corpus.py` |
| One course dominates every theme | Quotas are sqrt-weighted in `course_quotas()`; lower the exponent effect or raise the floor |
| A theme is empty | Its vocabulary in `THEMES` does not match how the corpus talks |
| One course yields far fewer passages per word than its peers | Its **register** differs, not its quality — see below |
| Near-identical passages still reaching digests | Lower `--near-threshold` toward 0.75 |
| Distinct passages wrongly merged | Raise `--near-threshold` toward 0.95, or 1.0 for exact-only |

### Register, not quality

The scorer rewards teaching language, and different courses teach in different
voices. Conversational courses are full of "always", "most people", "here's how".
Structured curricula teach in a flatter register — "the goal here is", "our
objectives", "the first step" — and without those phrases in `STRONG_SIGNALS`
they score far below their actual value.

This is a real failure that has already happened once: a six-lesson, 15k-word
course yielded **3 passages** until lecture-register signals were added, then
yielded 16. Diagnose it by comparing passages-per-1,000-words across courses in
`mining_report.json`. An outlier low course usually needs vocabulary, not a lower
threshold — lowering the threshold globally lets noise in everywhere else.

Check `deduplication.copies_removed` in the report. Zero across a corpus with
republished lessons means the threshold is too strict; a number approaching
`passages_kept` means it is far too loose and distinct material is being merged.

To choose a threshold rather than guess it, score the whole corpus and read the
distribution before committing — target keeping roughly 8–15% of themed
passages.

## Step 4 — Distill in a staging package

Digests are raw material, not references. For each theme, read the digest and
write or update the corresponding file in a staged copy of `references/`.
Review and validate that staged package before promoting it. Never edit the
global Claude skill or `_transcripts/` during distillation.

| Digest | Reference |
|--------|-----------|
| `frameworks.md` | `references/frameworks.md` |
| `psychology.md` | `references/psychology.md` |
| `headlines.md` | `references/headlines.md` |
| `sales_pages.md` | `references/sales-pages.md` |
| `emails.md` | `references/emails.md` |
| `offers.md` | `references/offers.md` |
| `voice.md` | `references/voice.md` |
| `ai_workflow.md` | `references/ai-workflow.md` |
| `client_work.md` | `references/client-work.md` |
| `positioning.md` | `references/positioning.md` |
| `research.md` | `references/research.md` |
| `examples.md` | `references/swipe-file.md` |
| — | `references/critique-rubric.md` is synthesized from the others |
| — | `references/anti-generic-copy.md` is a reviewed operational adaptation, not a mined digest |
| — | `references/harry-dry-copywriting.md` is a reviewed video distillation with timestamp citations |

Read one digest, write its reference, move on. Reading them all first wastes
context and blurs the material.

### Distillation standards

- **Every claim carries a citation** — `(Instructor, lesson @ timestamp)`
- **Organize by what a writer needs**, not by the order the digest presents
- **Preserve disagreement.** Where instructors conflict, record both positions
  and say which lesson each came from
- **Preserve the caveats the instructor gave.** Schutz's warning that drip
  pricing degrades for repeat-purchase businesses is as important as the tactic
- **Keep worked examples verbatim.** The concrete line is the value
- **Do not smooth speculation into fact.** If an instructor is reasoning aloud
  or making a dated claim, mark it as theirs

### Adding a course

If a new course introduces a theme the current vocabulary misses, add it to
`THEMES` in `mine_corpus.py`, add the matching entry to `EXPECTED_REFERENCES` in
`validate_library.py`, add a row to the orchestrator's reference table, and
re-mine.

## Step 5 — Validate

```bash
python /absolute/path/to/copy-lab/scripts/copy_lab.py validate
```

Checks that every expected reference exists, is substantial, carries timestamped
citations, and is newer than the last mining run. It also verifies local source
hashes, detects live transcript drift, and reports top-level books or media that
have not been registered in the source catalog. Exits non-zero on Critical
findings. Use `--strict` to fail on High as well, and `--json` for structured
output.

## Troubleshooting

**A course indexes with 0 words.** Its files do not match the expected watch
report shape. `parse_segments()` falls back to scanning for `[MM:SS]`-prefixed
lines anywhere in the file; if the transcript has no timestamps at all, it needs
a new parser branch.

**Corpus not found.** Run `copy_lab.py config set corpus /absolute/path/to/_transcripts`,
set `COPY_LAB_CORPUS` for a one-off override, or run from a workspace whose
ancestor contains `_transcripts/`. Use `copy_lab.py doctor` to see the active
configuration.

**Duplicate passages across courses.** Handled by the pipeline. Repeats are
collapsed corpus-wide to a canonical location, with the other locations listed
under the entry as `also in:` lines. Cite the canonical one. If duplicates still
reach a digest, they differ by more than the near-duplicate threshold — lower
`--near-threshold` (0.85 default) and re-run.

**Search returns nothing after re-mining.** `copy_lab.py search` reads the
configured external `mining/mined.jsonl`, then falls back to the bundled store.
Use `--store` to select a specific file, or `--full` to search raw transcripts.
Use `--source books` to isolate the local source index or `--source all` to merge
course and book results.

**OCR reports low-confidence pages.** Inspect the matching source pages. If the
layout is multi-column or unusually sparse, rerun only those pages with
`--pages 10,25-28 --force` and a different `--psm` or higher `--dpi`, then run
the full command again to recompose and validate `document.md`.

**A text-native PDF is reported as `needs_ocr`.** The ingesting Python runtime
cannot import `pypdf` and no `pdftotext` executable is available. Confirm that
text can be selected or extracted, then rerun `copy_lab.py ingest` with a Python
environment containing `pypdf`. Do not OCR clean embedded text merely to work
around a missing dependency.
