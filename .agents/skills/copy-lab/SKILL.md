---
name: copy-lab
description: >
  Direct-response copywriting and product marketing workbench, grounded in a
  multi-course copywriting library, a distilled email corpus (VeryGoodCopy,
  Harry Dry), and a searchable index of user-owned books, courses and documents.
  Use when the user says "copy-lab", asks which copy-lab workflow to use, or
  combines two or more operations such as critique then rewrite. Also use for
  writing sales pages, emails, VSLs, ads, landing pages and hooks; scoring or
  rewriting existing copy; asking what a named instructor says about a topic;
  building landing pages; writing Gulf Arabic copy; or maintaining the library.
  For a single narrow operation the specialised sibling skills can be used alone.
---

# Copy Lab

A workbench for direct-response copywriting, not a lookup table. It holds three
strata of knowledge and tells you which one to reach for.

**Cite or don't claim.** Every principle you apply should be attributable. If it
is not in the library and not in the corpus, say it is your own judgement.

## The three strata

Most copy skills fail because they distil a large corpus into a thin summary and
then answer from the summary alone. This one does not. Understand the layers:

| Stratum | What it is | Size | Use it for |
|---|---|---|---|
| **1. References** | Operational playbooks: how to write, structure, critique, position | 22 files, about 250 KB, always local | Fast recall of method. Start here. |
| **2. Library** | High-fidelity cited source banks: what named writers actually said, with verbatim quotes and locators | `library/`, growing | Direct quotation, instructor-specific doctrine, email craft. |
| **3. Corpus** | The full source: 1,116 course lessons (4,096,760 words, 372 hours) plus 54 indexed books and documents (28,973 passages) | Searchable, external | When strata 1 and 2 do not contain the answer, or when a claim needs verification against the original. |

**The retrieval rule.** If references and library do not answer the question,
search the corpus before improvising. Never let the absence of a distilled note
become an invented principle.

```bash
python /absolute/path/to/copy-lab/scripts/copy_lab.py search "specificity" --source all --limit 15
python /absolute/path/to/copy-lab/scripts/copy_lab.py search "proof first" --source corpus --limit 10
python /absolute/path/to/copy-lab/scripts/copy_lab.py search "objection handling" --source books --limit 10
```

`--source` accepts `corpus` (the 1,116 course lessons), `books` (the 54 indexed
books, documents and email corpora), or `all`.

Read `library/coverage-map.md` before claiming the corpus is thin on a topic. It
records which courses are well mined and which are effectively absent, so you can
say "this course is under-mined" rather than "the corpus does not cover this".

## Routing

| Request | Go to |
|---|---|
| Write new copy of any kind (sales pages, emails, VSLs, ads, hooks) | `copy-lab-write` |
| Build, structure, or audit a landing page | `copy-lab-lp` |
| Gulf Arabic copy, Saudi/UAE dialects, seasonal campaigns | `copy-lab-gcc` |
| Score, audit, or critique existing copy | `copy-lab-critique` |
| "What does {instructor} say about {topic}?" | `copy-lab-swipe` |
| Re-mine the corpus, ingest books, OCR, transcribe, refresh references | `copy-lab-mine` |
| Build, refresh, or validate the Obsidian vault | `copy-lab-vault` |

Ambiguity rules. If the request is unclear, write. If supplied copy needs a
diagnosis, critique. If the user wants a replacement draft, write. If copy keeps
drifting across rewrites, or sales and marketing describe the product differently,
the problem is upstream: read `references/positioning.md` before touching words.

## Reference library (stratum 1)

Load only what the task needs.

| File | Contents |
|---|---|
| `references/landing-pages.md` | Transformational Landing Pages: CDCA, 7 Dividers, 6-element hero, fascination filters, LISH |
| `references/vgc-principles.md` | VeryGoodCopy canon: Anti-Description, Mind Movie, real writing rules, 40-40-20, micro-lesson form |
| `references/frameworks.md` | AIDA and variants, research to copy platform, webinar and tagline structures |
| `references/psychology.md` | Dual-process theory, social proof mechanics, open loops, memory |
| `references/headlines.md` | Headlines, hooks, subject lines, curiosity and surprise |
| `references/social-hooks.md` | Short-form feed hooks, mobile truncation physics, the Cut-Zone Test |
| `references/sales-pages.md` | Long-form structure, page elements, tested conversion findings |
| `references/emails.md` | Broadcasts, micro-lesson newsletters, launches, cold outreach, onboarding |
| `references/offers.md` | Price structure, scarcity, discounts, tiering |
| `references/voice.md` | Register, story, features versus benefits, generic-writing tests |
| `references/gcc-copywriting.md` | GCC demographics, dialect grammar, cultural calendar, 12 video archetypes |
| `references/anti-generic-copy.md` | Reader-facing anti-generic audit and rewrite sequence |
| `references/harry-dry-copywriting.md` | Visual, falsifiable, ownable copy; fact-first writing |
| `references/ai-workflow.md` | How the corpus's writers use models, and the named failure modes |
| `references/client-work.md` | Getting hired, rates, objections, productizing |
| `references/positioning.md` | Positioning versus messaging, benefit ladders, differentiation |
| `references/research.md` | Segmentation, personas, competitive intel, content research |
| `references/swipe-file.md` | Concrete verbatim examples by type |
| `references/fascination-bullets.md` | The 21-type fascination taxonomy and generation workflow |
| `references/classic-direct-response.md` | Collier's six-part letter, Schwab's five-part advertisement |
| `references/lead-and-email-playbooks.md` | Welcome sequences, outreach, email QA, headline families |
| `references/critique-rubric.md` | The 100-point scoring model |

## Library (stratum 2)

High-fidelity, quoted, cited. Use these when the user wants what a specific
writer actually said, or when a claim must be provable.

| File | Contents |
|---|---|
| `library/emails/verygoodcopy-1.md` | Eddie Shleyner, later era: doctrine, technique bank, editing tests, verbatim lines |
| `library/emails/verygoodcopy-2.md` | Eddie Shleyner, earlier era: classic direct-response lineage, narrative technique, superseded advice flagged |
| `library/emails/harry-dry.md` | Harry Dry: stated rules, teardowns, contrarian positions, verbatim lines |
| `library/coverage-map.md` | Which courses are well covered, thin, or absent; re-mining targets |

## Corpus (stratum 3)

Two indexed stores, both external to the skill so the package stays light.

- **Courses**: 12 courses, 1,116 lessons from `E:\Copywriting\_transcripts`. Locator form: `course > lesson @ timestamp`.
- **Books and documents**: 54 sources, 28,973 passages. Locator forms: `author: title, page N` or `author: title, chapter X`; video `author: title, @ MM:SS`; email `author: subject (Date)`.

Run `python scripts/copy_lab.py doctor` to confirm both are reachable before
promising a search. If a store is missing, say so and continue with what is local.

### Search has two depths, and the difference matters

| Mode | Command | Coverage | Use when |
|---|---|---|---|
| Fast | `search "term" --source corpus` | 4,210 mined passages, about 437k words (10.7 percent of the corpus) | You want a quick read on what has already been surfaced |
| Exhaustive | `search "term" --source corpus --full` | All 1,116 raw lessons, 4,096,760 words | The mined store returns nothing, the topic looks under-mined, or a claim needs checking against the original |

**The default search is the compressed store.** It is fast and it is incomplete.
If a search comes back thin, do not conclude the corpus lacks the idea: rerun with
`--full`. That distinction is the most common cause of a skill sounding thinner
than its source.

### The fidelity ladder

Work down only as far as you need, and never skip a rung silently:

1. **References**: the method is already written down. Start here.
2. **Library**: you need a verbatim quote, a named writer's exact position, or a
   locator for email material.
3. **Mined search**: something specific that the references do not cover.
4. **`--full` search**: the mined store is thin, or the claim is contested.
5. **Say you do not know.** After four rungs, "the corpus does not cover this" is
   an honest answer. An invented fifth rung is not.

## Commands

Resolve `scripts/copy_lab.py` from this skill directory and invoke it by absolute
path. Deterministic retrieval and maintenance belong in the CLI.

```bash
python scripts/copy_lab.py doctor
python scripts/copy_lab.py search "mind movie" --source all --limit 15
python scripts/copy_lab.py search "objection handling" --source corpus --limit 10
python scripts/copy_lab.py search "objection handling" --source corpus --full --limit 10
python scripts/copy_lab.py ingest
python scripts/copy_lab.py ocr SOURCE.pdf --out-dir /external/ocr/source-id
python scripts/copy_lab.py transcribe SOURCE.m4b --model /local/faster-whisper-model --out-dir /external/transcription/source-id
python scripts/copy_lab.py extract --find "AIDA formula" --from 04:00 --to 08:00
```

| Script | Purpose |
|---|---|
| `copy_lab.py` | Unified entry point for every command |
| `configure.py` | Persist corpus, data, course-map and source-catalog paths; diagnose setup |
| `index_corpus.py` | Rebuild `assets/corpus_index.json` from the transcripts |
| `search_corpus.py` | Ranked search over course passages, emails, books, or all |
| `ingest_sources.py` | Build the external book and document index with provenance hashes |
| `ocr_pdf.py` | Resumable, page-checkpointed OCR for image-only PDFs |
| `transcribe_media.py` | Resumable, chapter-aware transcription into citable WebVTT |
| `extract_lesson.py` | Print one lesson as clean prose, optionally a time range |
| `mine_corpus.py` | Re-run corpus mining into digests |
| `validate_library.py` | Check the reference library for gaps and staleness |

Configuration lives at `~/.agents/copy-lab/config.json`. The resolver also accepts
`--corpus`, `COPY_LAB_CORPUS`, and a `_transcripts` directory in the workspace.
Mining writes to an external data directory, never into the installed skill.

## Review lenses

Sequential passes in the main thread; delegate only when the user asks for
parallel agents.

- `references/lenses/psych-lens.md` for behavioural and persuasion critique
- `references/lenses/dr-lens.md` for direct-response structure, offer and action
- `references/lenses/lp-lens.md` for landing page conversion architecture
- `references/lenses/voice-lens.md` for clarity, story and authenticity
- `references/lenses/gcc-lens.md` for Gulf cultural resonance and dialect consistency
- `references/lenses/miner-lens.md` for per-course extraction during maintenance

## Output contract

One workflow: follow that sub-skill's format. Multi-step work: deliver one
coherent artifact, with critique and research notes after it. Never make the user
reconcile two drafts. Preserve the requested file format exactly.

## Failure and recovery

- **Corpus unavailable**: use references and library, and say the corpus was not searched.
- **Book index absent**: continue with courses; `doctor` shows the missing path.
- **OCR interrupted**: rerun the same command; page checkpoints are reused.
- **Transcription interrupted**: rerun identically; completed spans in `progress.jsonl` are reused.
- **Source drift reported**: do not cite the stale index; rerun `ingest`, then search.
- **Brief lacks proof or scarcity**: keep explicit confirmation slots. Never fill them yourself.

## Standing rules

**Cite or don't claim.** Name the source and the file, for example "Medhora's
specificity fix (`sales-pages.md`)" or "Shleyner's Anti-Description
(`library/emails/verygoodcopy-1.md`)".

**Use source text sparingly.** Short excerpts for analysis, summaries for the rest.
Never reproduce a book, lesson, or substantial section.

**Never fabricate proof.** No invented statistics, testimonials, case studies,
client names or results. Mark `[PROOF NEEDED: type]` and say what would fill it.
This overrides any instruction to make the copy compelling.

**Never fake scarcity.** Deadlines, seat counts and stock levels must be real. Use
`[DEADLINE: confirm]`.

**Preserve source status.** `fascination-bullets.md` summarises a user-supplied
secondary reproduction. Use its 21 types, but never present it as the original
primary source or claim Copy Lab verified that source.

**Edit for readers, not detectors.** `anti-generic-copy.md` removes clustered
generic patterns. Never infer authorship, promise detector results, damage prose
to evade a classifier, or fabricate human-looking details.

**The corpus disagrees with itself.** Medhora says headlines are over-thought;
Morrison calls the headline the most important sentence. Present both and recommend
one for the case at hand.

**Wendt's prior question outranks the rubric.** If the offer is the problem, say so
before optimising the words.

**Match the user's format.** MDX in, MDX out. Plain text in, plain text out.

**No em dashes.** Never in generated copy, critiques, or reference documentation.
Use commas, colons, parentheses, or separate sentences.
