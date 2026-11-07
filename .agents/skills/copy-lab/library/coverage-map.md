# Corpus Coverage Map

Source files:
- `assets/corpus_index.json` (generated 2026-08-15T13:41:11+00:00, root `E:\Copywriting\_transcripts`)
- `assets/mining/mined.jsonl` (4,210 JSONL records, 4,243,510 bytes)
- `assets/mining/digests/*.md` (12 files, 766,571 bytes total)

Every figure below is computed from those three files. Ratios are shown so they can be re-derived.

## Budget

| Measure | Value | How computed |
|---|---|---|
| Courses | 12 | `totals.courses` |
| Lessons | 1,116 | `totals.lessons`, equals `len(lessons)` |
| Words in corpus | 4,096,760 | `totals.words`, equals sum of per-lesson `words` (delta 0) |
| Hours | 372.1 | `totals.hours`, equals sum of per-lesson `seconds` / 3600 (delta 0.00) |
| Mined records | 4,210 | line count of `mined.jsonl` |
| Words that survived into the mined store | 436,705 | sum of `len(text.split())` over all 4,210 records |
| Survival rate | 10.66% | 436,705 / 4,096,760 = 0.10660 |
| Compression ratio | 9.4 : 1 | 4,096,760 / 436,705 = 9.381 |
| Digest corpus (derived summary) | 139,648 words (3.41%) | sum of word counts of the 12 digest files |
| Records per lesson | 3.77 | 4,210 / 1,116 |
| Words per record | 103.7 | 436,705 / 4,210 |
| Corpus words per lesson | 3,670.9 | 4,096,760 / 1,116 |
| Mined words per lesson | 391.3 | 436,705 / 1,116 |

Plainly: for every 10 words in the source transcripts, roughly 1 word reached the mined store. Each lesson of about 3,671 words yielded about 391 words, in about 3.8 records averaging 104 words.

## Per-course coverage

Sorted by share of the course's own words that reached the mined store, worst first.

Verdict rule used:
- **effectively absent**: less than 8% of the course's words are in the store.
- **thin**: 8% to 18% of words, or fewer than 80% of lessons contribute at least one record.
- **well covered**: at least 18% of words and at least 80% lesson coverage.

| Course | Lessons | Words | Mined records | Records per 1,000 words | Mined words | % of course mined | Lessons with records | Verdict |
|---|---|---|---|---|---|---|---|---|
| Martin Lindstrom - Buyology | 2 | 28,147 | 16 | 0.57 | 1,453 | 5.2% | 2/2 (100%) | effectively absent |
| Kathryn Morrison (Words Are Wands) | 35 | 90,574 | 64 | 0.71 | 6,792 | 7.5% | 26/35 (74.3%) | effectively absent |
| Neville Medhora (Copywriting Course) | 798 | 3,189,353 | 2,651 | 0.83 | 274,638 | 8.6% | 602/798 (75.4%) | thin |
| Digital Psychology & Persuasion | 67 | 66,710 | 92 | 1.38 | 8,089 | 12.1% | 36/67 (53.7%) | thin |
| Maria Wendt (Words Into Money) | 4 | 3,729 | 6 | 1.61 | 608 | 16.3% | 3/4 (75.0%) | thin |
| Product Marketing | 105 | 341,556 | 646 | 1.89 | 62,087 | 18.2% | 92/105 (87.6%) | well covered |
| Bart Schutz (Master of Online Persuasion) | 33 | 156,686 | 261 | 1.67 | 30,475 | 19.4% | 33/33 (100%) | well covered |
| Kevin Meng - Next-Level AI Content | 3 | 7,084 | 13 | 1.84 | 1,434 | 20.2% | 3/3 (100%) | well covered |
| Jason C Fox - Magnetic Content | 41 | 95,659 | 173 | 1.81 | 20,062 | 21.0% | 34/41 (82.9%) | well covered |
| Drop Dead Copy (AI Copywriting Secrets Vol 1) | 8 | 63,420 | 129 | 2.03 | 13,971 | 22.0% | 8/8 (100%) | well covered |
| Branding & Brand Strategy | 15 | 38,124 | 96 | 2.52 | 9,255 | 24.3% | 15/15 (100%) | well covered |
| Rohan - Copy Launchpad | 5 | 15,718 | 63 | 4.01 | 7,841 | 49.9% | 5/5 (100%) | well covered |

Reading the table: the two worst-served courses are not the smallest in absolute terms. Lindstrom is 7.4 hours of audio and 28,147 words reduced to 16 records. Kathryn Morrison is 90,574 words reduced to 64 records, one per 1,415 words.

## Skew analysis

Record share of the whole store:

| Course | Records | Share of 4,210 |
|---|---|---|
| Neville Medhora (Copywriting Course) | 2,651 | 63.0% |
| Product Marketing | 646 | 15.3% |
| Bart Schutz (Master of Online Persuasion) | 261 | 6.2% |
| Jason C Fox - Magnetic Content | 173 | 4.1% |
| Top four combined | 3,731 | 88.6% |

A single folder is the true centre of gravity: Neville's `01-Videos` section holds 2,402 records, **57.1% of the entire mined store**, and 247,617 of the 436,705 mined words. That folder is his Office Hours series: unscripted live coaching, 684 lessons, 2,932,201 words.

Two corrections to the obvious reading, both worth carrying into the rebuild:

1. Neville is not over-sampled relative to its size. It is 77.9% of corpus words (3,189,353 / 4,096,760) and 76.2% of hours, but only 63.0% of records and 62.9% of mined words. It is the most under-mined course of the large ones. The store looks Neville-heavy because the corpus is Neville-heavy.
2. Sampling density runs backwards against size. Records per 1,000 words range from 0.57 (Lindstrom) to 4.01 (Rohan), a 7.0x spread; among larger courses, Rohan at 4.01 vs Neville at 0.83 is 4.8x. Small courses were mined 4 to 7 times more densely than the largest one. Whatever produced the store sampled by count, not by value.

Effectively absent, in practice:
- Martin Lindstrom - Buyology: 16 records, 0.4% of store, 5.2% of the course.
- Maria Wendt - Words Into Money: 6 records, 0.1% of store.
- Kevin Meng - Next-Level AI Content: 13 records, 0.3% of store.

Together those three are 35 records, 0.83% of the store.

What this means for a copywriter using the skill: the library's knowledge of persuasion theory, consumer psychology and live copy critique rests on a handful of fragments. Lindstrom's Buyology (7.4 hours on why people buy) is 16 snippets. Kathryn Morrison's `07-Behind the Wand: Live Messaging Audits` section (20,925 words) has 2 records, and it is the only live copy-audit material anywhere in the corpus, so the skill has almost no evidence base for reviewing someone's copy. Meanwhile 57% of the store is improvised Q&A, which is anecdotal and episodic: useful for tactics and pricing chatter, weak for frameworks, and non-repeatable. In inference terms, the library is strong on what Neville said on a given Thursday and weak on the structured curricula that the other 11 courses exist to teach.

## Topic digest coverage

All 12 digests exist and all 12 match the theme keys in the store exactly (no theme key lacks a digest, no digest lacks a theme). Each digest is a cross-course extraction with 10 to 12 course blocks, about 11,500 words, and all 12 together are 139,648 words, 3.41% of the corpus.

| File | Bytes | Words | Course blocks | What it appears to cover |
|---|---|---|---|---|
| ai_workflow.md | 62,114 | 11,555 | 11 | Automating copy production, AI tooling and prompting. Distinctive terms: automate, trained, metrics. |
| client_work.md | 63,661 | 11,559 | 11 | Agency and client engagements, service pricing, scope and value framing. Distinctive: triple, values, groupon. |
| emails.md | 63,998 | 11,671 | 10 | Email structure, broadcasts, preview text, sequencing. Distinctive: broadcasts, preview, partitioning. |
| examples.md | 64,398 | 11,745 | 12 | Worked copy examples and swipe lines. Largest theme by record count (1,713 records, 40.7%). |
| frameworks.md | 65,054 | 11,830 | 11 | Named models and acronyms (AIDA, OODA and similar). Distinctive: acronym, blueprint, momentum. |
| headlines.md | 64,757 | 11,942 | 10 | Headlines, hooks, scroll-stopping openings. Distinctive: scrolling, threat, humans. |
| offers.md | 63,532 | 11,480 | 12 | Offer construction, bonuses, guarantees, product description. Distinctive: toblerone, chocolate, tactics. |
| positioning.md | 63,566 | 11,460 | 11 | Positioning statements, differentiation, category framing. Distinctive: therapist, subjects, creator. |
| psychology.md | 63,763 | 11,442 | 12 | Biases, persuasion, demographics and segmentation. Distinctive: demographic, empathy, validating. |
| research.md | 62,051 | 11,232 | 11 | Market and customer research, awareness sophistication. Distinctive: sophistication, requirements, studying. |
| sales_pages.md | 63,445 | 11,612 | 12 | Long-form page structure and modular sections. Distinctive: modular, visuals, adidas. |
| voice.md | 66,232 | 12,120 | 11 | Brand voice, tone, rewriting and style transfer. Distinctive: storyteller, rewrote, essence. |

Coverage gaps at topic level (evidence, not preference):
- **Pricing psychology has no digest.** Bart Schutz's `8. Pricing Psychology` is the densest section in the corpus at 2.60 records per 1,000 words (67 records, 25,747 words), and 153 records contain "pricing", yet the material is scattered through `offers.md` and `psychology.md` rather than named.
- **Differentiation has no digest.** `13-Radical Differentiation` alone holds 220 records across 180,983 words (1.22 per 1,000). Only 61 of 4,210 records contain the stem "differentiat", and no digest is named for it. Inference: the largest structured topic in Product Marketing is under-labelled by the theme schema, so it is invisible as a topic.
- **Copy audit and critique has no digest.** The only audit material (`07-Behind the Wand`) produced 2 records, too few to seed a digest.
- **Thin themes despite real source volume:** "urgency" appears in 14 records, "guarantee" in 35, "objection" in 30, "proposal" in 15, "negotiat" in 2. These are standard copywriting topics with almost no representation.
- **Theme weight is itself skewed:** `examples` touches 1,713 records (40.7%), `client_work` 1,310 (31.1%), `emails` 1,294 (30.7%), against `ai_workflow` 317 (7.5%) and `headlines` 423 (10.0%).
- The digests inherit the mining holes: Maria Wendt appears in only 7 of 12 digests, Martin Lindstrom in 9, Kevin Meng in 10, because those courses produced too few records per theme to earn a block.

No course is entirely missing from the digest set (the union of blocks covers all 12). The gaps are at topic level, and in block size: Neville's block is 40.2% of digest characters on average, and 46.6% in `headlines.md`.

## Structural defects found

1. **257 of 1,116 lessons (23.0%) contribute zero records.** Worst holes: 154 of Neville's 684 `01-Videos` lessons, 20 of Digital Psychology's 33 `18-Cognitive Biases` lessons, 16 of Neville's `03-Copywriting Guides`. Largest single omission is Neville `84-Office Hours- September 11 2025` at 10,830 words.
2. **The store is mechanically chunked, not semantically segmented.** 2,415 of 4,210 records (57.4%) are between 100 and 140 words; median 120, minimum 33, maximum 340, only 6 records above 200. Text starts and ends mid-sentence (frequent records beginning with "Um, but, but I'm just" or ending in "And"). Inference: a fixed window of about 120 words was applied, so sentence and idea boundaries were cut.
3. **A hard score floor decided what survived.** `score` ranges 7 to 26, median 8, and 1,387 records sit at exactly 7 with none below. 2,976 records (70.7%) score under 10. Inference: records were filtered at `score >= 7`, so the threshold, not topical relevance, gated the store.
4. **Two courses have no section metadata.** Drop Dead Copy: `sections: []`, 8 lessons all with `section: ""`, and all 129 of its records carry an empty section. Martin Lindstrom: same shape, 2 lessons, 16 records, empty section. Section-level navigation is impossible for 63,420 + 28,147 words.
5. **Three courses are synthetic buckets, not directories.** Product Marketing spans 10 top-level folders, Digital Psychology 7, Branding 2. The course name appears in zero paths for Branding and Digital Psychology, and 832 records have a path that does not contain their course string (644 Product Marketing, 96 Branding, 92 Digital Psychology). Course attribution exists only in the index and cannot be re-derived from the filesystem.
6. **Three duplicate lessons.** Pairs identical in words, seconds and bytes under different filenames: The AIDA Formula For Easy Writing Demo (1,371 words), 9 Copywriting Exercises (2,662), Three Tiered Pricing Structure (2,040). Extra 6,073 duplicated words, 0.15% of the corpus.
7. **One corrupted record.** 2 replacement characters (U+FFFD) inside the text of Product Marketing `09-Radical differentiation  becoming the -only-` at 02:02. The only encoding damage found in either file.
8. **Dash variants are a matching hazard.** The index contains 1,761 en dashes (U+2013), and 5 of 12 course names contain one. Any string join on course name will fail across encoders, which is the likely origin of the 832 path mismatches in item 5.
9. **Recurring text is flagged but not removed.** 147 records have `occurrences > 1` with populated `also_in` (110 at 2 locations, 24 at 3, 10 at 4, 3 at 5). Exact duplicate text across records is 0, so deduplication happened, but the 147 are the same passage offered at multiple timestamps.
10. **Checks that came back clean.** 4,210 of 4,210 record paths resolve to lessons in the index. 0 section mismatches against the index. 0 unparsable timestamps. 0 timestamps beyond the lesson's duration. 0 records with empty text. Per-course words and hours reconcile exactly to declared totals (delta 0 on all 12). Duplicate lesson names: 0. Digest block duplication across files: 3 identical block pairs of 696 (0.4%), so the digests are genuinely theme-specific rather than copies.

## Recommended re-mining targets

Ordered by value recovered per word, not by size.

1. **Kathryn Morrison - Words Are Wands (35 lessons, 90,574 words).** Only 7.5% mined, 9 lessons and 18,638 words never touched, and `07-Behind the Wand: Live Messaging Audits` (20,925 words, 2 records) is the only live copy-critique material in the entire corpus. This is the single biggest capability hole: the skill cannot show how a professional rewrites weak copy because almost none of it was mined.
2. **Martin Lindstrom - Buyology (2 lessons, 28,147 words, 7.4 hours).** 5.2% mined, 26,694 words unmined, 16 records total. It is the corpus's only dedicated consumer-psychology source and currently functions as a stub. Lesson-level coverage reads 100%, which is exactly why the shortfall has stayed invisible.
3. **Digital Psychology & Persuasion (67 lessons, 66,710 words).** 24.8% of the course absent, 31 of 67 lessons with zero records, including 20 of 33 `18-Cognitive Biases` lessons and 5 of `20-Building Trust`. It is a structured curriculum that duplicates Bart's territory at higher practical density, and it is half missing.
4. **Neville `02-Courses` (the sequenced curriculum, 9 subsections).** This is the teaching path, as distinct from Office Hours, and its density is poor: SEO 0.12 per 1,000 (2 records, 16,404 words), Website Pages 0.37, Build Digital Products 0.63, Freelancing 0.65. Mining the full curriculum would buy more usable instruction than adding further Office Hours volume.
5. **Product Marketing `13-Radical Differentiation` and `15-Analyst Relations`.** Differentiation holds 220 records over 180,983 words (1.22 per 1,000) and has no digest; Analyst Relations is 8 records over 11,723 words (0.68). 13 lessons and 15,714 words of the course are unmined.
6. **Jason C Fox - Magnetic Content (41 lessons, 95,659 words).** 7 lessons and 7,125 words unmined; `06-Daily Sales Challenge` is at 0.67 per 1,000. It is the strongest remaining source on direct-response sales language.
7. **Maria Wendt - Words Into Money (4 lessons, 3,729 words).** Only 6 records, and `04-Formatting-For-Conversions` is the one section in the corpus with zero records (552 words). Cheapest complete fix available.
8. **Neville `01-Videos`, selective only.** 154 lessons have zero records, but this folder is already 57.1% of the store. Re-mine only named-topic episodes (for example `94-Copy for an event was very bland`, `310-Doing a B2B webinar for divorce professionals`), and cap its share so it cannot re-exercise the same dominance.

Process fixes to carry into the rebuild, each tied to a defect above: segment on sentence and section boundaries rather than a fixed 120-word window (defect 2); set a per-course record quota instead of a global score floor (defect 3); backfill section metadata for Drop Dead Copy and Lindstrom (defect 4); dedupe on (words, seconds, bytes) before counting lessons (defect 6); and add topic keys for pricing, differentiation, urgency, guarantees, objections and copy audit, all of which have source volume but no home in the current schema.
