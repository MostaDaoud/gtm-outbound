---
name: copy-lab-swipe
description: >
  Look up what the copywriting library actually says about a topic, instructor,
  author, or technique, and return brief passages with precise citations.
  Searches the indexed multi-course transcript corpus plus local books, audio, and videos
  — Schutz, Medhora, Morrison, Wendt, Fox, Meng, Rohan and the Drop Dead Copy
  panel, plus the Product Marketing, Digital Psychology & Persuasion, and
  Branding & Brand Strategy curricula covering positioning, messaging,
  segmentation, competitive intel, cognitive biases, and behavioral design. Use
  when the user says "what does Schutz say about", "what does Medhora say
  about", "find where they talk about", "swipe file", "show me examples of",
  "look up in the courses", "search the transcripts", "copy-lab swipe", or asks
  for the "21 fascination bullet types" or the source behind a copywriting
  claim. For writing copy use
  copy-lab-write; for scoring copy use copy-lab-critique.
---

# Copy Lab — Swipe

Answer questions from the sources themselves, with citations precise enough to
open the video at the right moment or find the page/chapter in a book.

**Shared resources.** References and scripts live in the `copy-lab` skill
folder, not this one: `../copy-lab/references/` and `../copy-lab/scripts/`.
Resolve these sibling-relative paths to absolute paths before reading or
executing them.

## Step 1 — Try the reference library first

For well-covered topics the distilled answer already exists and is faster and
cleaner than raw transcript:

| Topic | File |
|-------|------|
| AIDA, research process, webinar structure, taglines | `../copy-lab/references/frameworks.md` |
| System 1/2, biases, social proof, open loops, memory | `../copy-lab/references/psychology.md` |
| Headlines, hooks, subject lines, curiosity | `../copy-lab/references/headlines.md` |
| Page structure, conversion findings | `../copy-lab/references/sales-pages.md` |
| Sequences, launches, cold outreach, newsletters | `../copy-lab/references/emails.md` |
| Pricing, scarcity, discounts, tiering | `../copy-lab/references/offers.md` |
| Register, story, features/benefits | `../copy-lab/references/voice.md` |
| Model workflows and their failure modes | `../copy-lab/references/ai-workflow.md` |
| Reader-facing AI-like patterns and anti-generic editing | `../copy-lab/references/anti-generic-copy.md` |
| Harry Dry's sentence tests, fact-first method, contextual review, rewriting, newsletters, and AI judgment | `../copy-lab/references/harry-dry-copywriting.md` |
| Rates, objections, positioning, productizing | `../copy-lab/references/client-work.md` |
| Concrete examples by type | `../copy-lab/references/swipe-file.md` |
| Fascination bullets and the 21-type taxonomy | `../copy-lab/references/fascination-bullets.md` |
| Collier's letters and Schwab's advertisement system | `../copy-lab/references/classic-direct-response.md` |
| Lead activation, consulting outreach, email QA, message skeletons, headline formulas | `../copy-lab/references/lead-and-email-playbooks.md` |

If the library answers it, quote the library and give its citation. Say the
answer came from the distilled reference, and offer to pull the raw passage.

For the 21 fascination types, report the reference's provenance exactly: the
taxonomy is available through a user-supplied four-part Reddit reproduction
attributed to Clayton Makepeace, while the purported original Makepeace/Flores
issue remains unverified. Do not silently upgrade a secondary reproduction into
a primary citation.

Treat `anti-generic-copy.md` as an operational adaptation of a user-supplied
skill, not as a course-derived authorship test or detector validation.

## Step 2 — Search the sources

When the library does not cover it, or the user wants the source:

```bash
python ../copy-lab/scripts/copy_lab.py search "social proof" --source all --limit 15
```

Options that matter:

- `--course Medhora` — restrict to one instructor (substring match)
- `--course Schwartz` — also filters by a book title or author
- `--source corpus|books|all` — select course transcripts, books, or both
- `--full` — search raw transcripts instead of mined passages, for anything the
  miner scored below threshold
- `--any` — broaden a multi-term query; all terms are required by default
- `--diverse` — round-robin ranked hits by course to surface other viewpoints
- `--min-match-score N` — discard weak query matches
- `--json` — structured output
- `--limit N` — default 15

Quote multi-word phrases. Search terms use whole words or phrases after
normalization, so case and punctuation do not matter. Start with all-term mode;
use `--any` only when recall matters more than precision.

**If the mined course store returns nothing, retry with `--source corpus --full`
before concluding the course corpus is silent.** `--full` affects transcripts;
books are searched from their generated source index.

## Step 3 — Read around the hit

A search result is a window, not the argument. When a hit looks load-bearing,
pull the surrounding context:

```bash
python ../copy-lab/scripts/copy_lab.py extract --find "AIDA formula" --from 04:00 --to 08:00
```

`--find` resolves a lesson by title substring and reports the candidates if the
query is ambiguous. Pass a path directly when you have one. `--timestamps` keeps
the paragraph markers.

## Step 4 — Answer

**Prefer a short quotation plus a summary.** Quote only when wording carries
the point, keep each excerpt brief, and never reproduce a lesson or substantial
section. These are spoken transcripts, so light cleanup of filler is fine—mark
it if you cut anything substantive.

**Cite courses as** `Course, lesson @ timestamp`. **Cite books as**
`Author — Title, page N` or `Author — Title, chapter X`. **Cite videos as**
`Speaker — Title, @ MM:SS`. Never turn the source
index into a substitute for the original: quote briefly and summarize.

**Report disagreement.** Where instructors conflict, show both. Medhora on
headlines being over-thought versus Morrison on the headline as the most
important sentence is a real disagreement, not a retrieval error.

**Report absence honestly.** If the corpus does not cover something, say so —
"nothing in these courses addresses X" — rather than filling the gap with
general knowledge presented as though it came from the library. If you add
outside knowledge, label it as outside the corpus.

**Report source tier honestly.** For `fascination-bullets.md`, cite the Reddit
series as a secondary reproduction and link the relevant part or the four-part
chain. Do not attribute the wording or examples in that reference directly to
the unverified original issue.

## Corpus map

| Course | Lessons | Emphasis |
|--------|---------|----------|
| Bart Schutz — Master of Online Persuasion | 33 | Behavioral science, dual-process theory, pricing psychology |
| Neville Medhora — Copywriting Course | 798 | Direct response, office-hours teardowns, freelancing |
| Jason C Fox — Magnetic Content | 41 | Social content, DMs, offers, community |
| Kathryn Morrison — Words Are Wands | 35 | Messaging, sales pages, voice, cold outreach |
| Drop Dead Copy — AI Copy Secrets Vol 1 | 8 | Eight working copywriters on AI workflow |
| Rohan — Copy Launchpad | 5 | Outreach systems, research, client acquisition |
| Maria Wendt — Words Into Money | 4 | Hooks, landing pages, fundamentals |
| Kevin Meng — Next-Level AI Content | 3 | AI content process, editorial guidelines |

**Multi-instructor curricula** — these ship as numbered module folders that
`assets/course_map.json` rolls up into one course name. The module folder is kept
as the citation's section, so `Product Marketing > 12-Positioning > 08-… @ 10:18`
names both.

| Course | Lessons | Modules include |
|--------|---------|-----------------|
| Product Marketing | 92 | Positioning, Messaging, Segmentation & Persona Research, Storytelling, Competitive Intel, Sales & CS Enablement, Content Marketing Research, Radical Differentiation, Analyst Relations |
| Digital Psychology & Persuasion | 67 | Persuasive design, Attention Basics, Cognitive Biases, Decision Making, Building Trust, Nonconscious Motivation, Habits & Loyalty, Psychological Backfiring |
| Branding & Brand Strategy | 15 | Brand purpose, maturity stages, brand planning, branding |

Medhora is roughly 81% of the corpus by word count, and the curricula are small
beside him. The mining quotas deliberately compress that so smaller courses are
not buried — worth remembering when a search returns mostly Medhora. Use
`--course` to force the other side into view, and note that `--course "Product
Marketing"` now matches the rolled-up name rather than a folder.

**The corpus is live.** Courses and modules have been appearing as the user's
transcription pipeline runs, and the folder-to-course mapping has changed once
already. If a search finds nothing on a topic the curricula should cover, check
whether the library needs re-mining (`copy-lab-mine`) before concluding the
corpus is silent.

## Failure and recovery

- No course hit: retry `--source corpus --full` with fewer terms.
- No book hit: confirm `copy_lab.py doctor` reports a valid source index, then
  broaden with `--any`.
- Drifted source index: re-run `copy_lab.py ingest`; do not cite stale records.
- Ambiguous or conflicting sources: present both positions and their locators.

## Output format

```markdown
## {Question}

**Short answer:** {2-3 sentences}

### {Instructor}
> "{verbatim passage}"
— `{Course} > {lesson} @ {timestamp}`

{One line on what it means in practice}

### Where they disagree
{Only if they do}

### Not in the library
{Anything asked that the configured sources do not address}
```
