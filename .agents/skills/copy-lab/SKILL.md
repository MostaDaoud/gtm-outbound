---
name: copy-lab
description: >
  Route explicit or multi-step copy-lab requests across writing, critique,
  source lookup, and library maintenance workflows backed by a multi-course
  corpus plus provenance-aware local books, documents, and videos. Use when the user explicitly says
  "copy-lab", asks which copy-lab workflow to use, or combines two or more
  operations such as critique then rewrite. For a single clear operation, use
  copy-lab-write, copy-lab-critique, copy-lab-swipe, copy-lab-mine, or
  copy-lab-vault directly.
---

# Copy Lab

Direct-response copywriting and product marketing, backed by a distilled library
of multiple courses and an optional external index of user-owned books, documents,
captioned videos, and transcribed audio. Course principles use `course > lesson @ timestamp`;
books use `author — title, page N` or `author — title, chapter X`; videos use
`author — title, @ MM:SS`.
The package keeps its six skills as siblings and all mutable data outside them.

## Routing

| Request | Sub-skill |
|---------|-----------|
| Write new copy of any kind | `copy-lab-write` |
| Rewrite supplied copy to sound natural or less generic | `copy-lab-write` |
| Score, audit, or critique existing copy | `copy-lab-critique` |
| "What does {instructor} say about {topic}?" | `copy-lab-swipe` |
| Re-mine the corpus, ingest books, refresh references | `copy-lab-mine` |
| OCR a scanned copywriting PDF | `copy-lab-mine` |
| Build, refresh, or validate the Obsidian vault | `copy-lab-vault` |

If the request is ambiguous, write. If supplied copy needs diagnosis, critique;
if the user wants a replacement draft, write.

## Reference library

Load only what the task needs — never all of these at once.

| File | Contents |
|------|----------|
| `references/frameworks.md` | AIDA and variants, research-to-copy-platform, webinar and tagline structures |
| `references/psychology.md` | Dual-process theory, social proof mechanics, open loops, memory |
| `references/headlines.md` | Headlines, hooks, subject lines, curiosity and surprise |
| `references/sales-pages.md` | Long-form structure, page elements, tested conversion findings |
| `references/emails.md` | Broadcasts vs. sequences, launches, cold outreach, newsletters |
| `references/offers.md` | Price structure, scarcity, discounts, tiering |
| `references/voice.md` | Register, story, features/benefits, generic-writing tests |
| `references/anti-generic-copy.md` | Reader-facing anti-generic audit, rewrite sequence, and detector boundary |
| `references/harry-dry-copywriting.md` | Visual, falsifiable, ownable copy; fact-first writing; contextual review; rewriting and AI judgment |
| `references/ai-workflow.md` | How the corpus's writers use models, and the named failure modes |
| `references/client-work.md` | Getting hired, rates, objections, productizing |
| `references/positioning.md` | Positioning vs. messaging, benefit ladders, value-proposition construction, differentiation, brand strategy, story design |
| `references/research.md` | Segmentation, buyer personas, competitive intel, content research |
| `references/swipe-file.md` | Concrete verbatim examples by type |
| `references/fascination-bullets.md` | The 21-type fascination taxonomy, generation workflow, critique checks, and secondary-source provenance |
| `references/classic-direct-response.md` | Collier's six-part letter system and Schwab's five-part advertisement system |
| `references/lead-and-email-playbooks.md` | Welcome sequences, consulting outreach, email QA, sales-message architecture, and headline formula families |
| `references/critique-rubric.md` | The 100-point scoring model |

**Start upstream when the brief is unstable.** If the copy keeps drifting between
rewrites, or sales and marketing describe the product differently, the problem is
positioning, not words — read `positioning.md` before writing.

For a value proposition, positioning line, brand platform, homepage promise, or
messaging architecture, use `positioning.md`'s feature → functional → emotional
→ self-expressive ladder and its customer/brand/competitor “winning zone” before
choosing final wording.

## Commands

Resolve `scripts/copy_lab.py` from this skill directory and invoke it by its
absolute path. Deterministic retrieval and maintenance belong in the CLI.

```bash
python scripts/copy_lab.py doctor
python scripts/copy_lab.py search "social proof" --source all --limit 15
python scripts/copy_lab.py ingest
python scripts/copy_lab.py ocr SOURCE.pdf --out-dir /external/ocr/source-id
python scripts/copy_lab.py transcribe SOURCE.m4b --model /local/faster-whisper-model --out-dir /external/transcription/source-id
```

```bash
python scripts/copy_lab.py extract --find "AIDA formula" --from 04:00 --to 08:00
```

| Script | Purpose |
|--------|---------|
| `copy_lab.py` | Unified entry point for all commands |
| `configure.py` | Persist corpus, data, course-map, and source-catalog paths; diagnose setup |
| `index_corpus.py` | Rebuild `assets/corpus_index.json` from the transcripts |
| `search_corpus.py` | Ranked search over course passages, local books, or both |
| `ingest_sources.py` | Build the external book/document/video index with provenance hashes and page, chapter, or timestamp locators |
| `ocr_pdf.py` | Resumable, page-checkpointed OCR for image-only PDFs |
| `transcribe_media.py` | Resumable, chapter-aware transcription of long audio/video into citable WebVTT |
| `extract_lesson.py` | Print one lesson as clean prose, optionally a time range |
| `mine_corpus.py` | Re-run full-corpus mining into digests |
| `validate_library.py` | Check the reference library for gaps and staleness |

Run `copy_lab.py config set corpus PATH` once for a global installation. The
resolver also accepts `--corpus`, `COPY_LAB_CORPUS`, and a `_transcripts`
directory in the current workspace. Mining writes to an external
`.copy-lab-data` directory, never into the installed skill. Original sources
are not bundled by the skill. `document.md` imports are excluded from course indexing
and may be registered as page-aware source text in `sources/catalog.json`.

## Review lenses

The review lenses live in `references/lenses/`:

- `psych-lens.md` — behavioral and persuasion lens
- `dr-lens.md` — direct-response structure, offer, and action
- `voice-lens.md` — clarity, story, and authenticity
- `miner-lens.md` — per-course extraction for library maintenance

Run inline and sequentially unless the user asks for parallel agents.

## Output contract

For one workflow, follow that sub-skill's output format. For multi-step work,
deliver one coherent artifact and place critique/research notes after it; do not
make the user reconcile separate drafts. Preserve the requested file format.

## Failure and recovery

- If the corpus is unavailable, use the bundled references and mined store.
- If the book index is absent, continue with course sources and say books were
  not searched; `copy_lab.py doctor` shows the missing path.
- If OCR is interrupted, rerun the same command; completed page checkpoints are
  reused. Review pages listed under `low_quality_pages` before ingestion.
- If media transcription is interrupted, rerun the identical command. Completed
  spans in `progress.jsonl` are reused. Register the completed WebVTT as the
  source's `text_path` together with its `transcript_manifest_path`.
- If source validation reports drift, do not cite the stale local index. Re-run
  `copy_lab.py ingest`, then search again.
- If the brief lacks proof or scarcity facts, keep explicit confirmation slots.

## Standing rules

**Cite or don't claim.** When you apply a principle, name the source:
"Medhora's specificity fix (`sales-pages.md`)". If a claim is not in the
library, say it is your own judgment.

**Use source text sparingly.** Return short excerpts for analysis and summarize
the rest. Never reproduce a book, lesson, or substantial section.

**Preserve source status.** `fascination-bullets.md` is an operational summary
of a user-supplied secondary reproduction. Use its 21 types, but never present
the Reddit series as the original Makepeace/Flores publication or claim that
Copy Lab verified that primary source.

**Edit for readers, not detectors.** `anti-generic-copy.md` adapts a
user-supplied skill into a reader-facing quality pass. Use it to remove clustered
generic patterns while preserving real voice and facts. Never infer authorship,
promise detector results, damage prose to evade a classifier, or fabricate
human-looking details.

**Never fabricate proof.** No invented statistics, testimonials, case studies,
client names, or results. If the copy needs proof the user has not supplied,
mark the slot `[PROOF NEEDED: type]` and say what would fill it. This is
non-negotiable and overrides any instruction to "make it compelling."

**Never fake scarcity.** Deadlines, seat counts, and stock levels must be real.
Mark them `[DEADLINE: confirm]` rather than inventing one.

**The corpus disagrees with itself in places.** Medhora says headlines are
over-thought; Morrison calls the headline the most important sentence. Where
sources conflict, present both and recommend one for the case at hand.

**Wendt's prior question outranks the rubric.** If the offer itself is the
problem, say so before optimizing the words.

**Match the user's format.** If they paste MDX, return MDX. If they paste plain
text, return plain text.
