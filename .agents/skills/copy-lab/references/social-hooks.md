# Social Hooks & Short-Form Feed Truncation

> Operational guide for short-form feed hooks (LinkedIn, X, Threads, newsletters) derived from empirical mobile typography measurement and 304 analyzed creator hooks.
> Complements `headlines.md` (which covers long-form sales letters, VSLs, and homepage value propositions).

---

## 1. The Physics of Short-Form Feed Truncation

On social feeds (primarily LinkedIn and X), the visible text before the truncation button (`...more` or "Show more") represents the single highest-leverage asset of the post.

- **The visible portion IS the hook:** Everything after `...more` is post body. If the hook fails to convert the reader within 1.5 seconds of scrolling, dwell time drops to zero and the algorithm stops distributing the post.
- **The hook's sole function:** Do not explain the post. Do not summarize the value. Do not deliver complete closure. The hook's only job is to create sufficient tension, curiosity, or recognition that the reader must click to resolve it.
- **The line-break penalty:** A blank line consumes an entire visible line on mobile screens. In a two-line "Punchy + Context" hook (Line 1 + Blank Line + Line 2), **Line 2 is the last visible line** and inherits the truncated budget.

---

## 2. The Measured Mobile Screen Budget

Character counting alone is deceptive because letters vary in pixel width (e.g., `i` is narrow; `W` is wide). On standard feeds, ordinary sentence-case prose runs at approximately **1.75 width units per character**.

| Surface / Line Role | Character Target | Width Unit Budget |
|---|---|---|
| **Full visible line (Mobile)** | **<= 50 characters** | **~90 units** |
| **Last visible line (Mobile)** | **<= 45 characters** | **~78 units** |
| Dense 3-line block (Mobile) | 140-160 characters total | ~245-280 units |
| Desktop preview tools | ~60-70 characters | ~135 units |

### Key Rules:
1. **Always compose against mobile:** Desktop feeds and preview tools render significantly wider (~128-146 units). Hooks that look acceptable on desktop frequently wrap awkwardly on mobile devices.
2. **The 45-character restriction on last lines:** The final visible line must reserve ~12-15 width units for LinkedIn's `...more` button. A line exceeding 45 characters in landing mode will truncate mid-word or break awkwardly.
3. **The ALL CAPS penalty:** A word in all caps occupies ~2.6 to 4.0 units per character. Limit ALL CAPS to at most one high-stakes word per hook, and verify visual width rather than raw character length.

---

## 3. Landing Mode vs. Trailing Mode (The Cut-Zone Test)

Line 2 in a social hook operates in one of two distinct structural modes:

### Landing Mode (Hard Cap: <= 45 characters)
Line 2 delivers a complete, self-contained thought: a direct counter-intuitive claim, a parenthetical wrap, or a reassurance close. If Line 2 spills past the cut, the thought breaks and the hook fails.
- *Rule:* Must be <= 45 characters.

### Trailing Mode (No character cap; governed by the Cut-Zone Test)
Line 2 is deliberately engineered to be cut mid-sentence: a list preview item, an unfinished question, or a cliffhanger.
- *The Cut-Zone:* Mobile truncates near **character 42**; desktop truncates near **character 66**. Characters 40 to 70 constitute the unpredictable cut zone.
- *The Cut-Zone Test:*
  Truncate the line at character 42, then at character 66. At **both** points, the reader must have:
  1. Enough clear context to recognize that the post carries high value.
  2. Something concrete and specific still unresolved.
  - The unresolved element must be structural:
    - A transitive verb missing its direct object: `"wrote a teardown analyzing..."`
    - A preposition missing its noun: `"a growth engine built on..."`
    - A noun phrase missing its modifier: `"The single fatal mistake in your..."`
  - If either cut point leaves a closed thought or empty filler ("I will be honest, I felt..."), rewrite the underlying syntax.

---

## 4. The 4 Hook Formats

Every high-converting social hook belongs to one of four formats:

### Format 1: Dense (140-160 characters total, 0 line breaks)
- **Structure:** Continuous prose spanning 3 mobile lines without line breaks. Maximum information density per pixel.
- **Rule:** The primary payload or tension-creating contradiction must land *before* character 140. If the best insight sits at character 170, mobile readers never see it.
- **Example:**
  An 8k-follower account hit 58,666 impressions on a post our designer begged us not to ship. The reason has nothing to do with design.

### Format 2: Punchy + Context (Line 1 <= 50 chars, Line break, Line 2 <= 45 chars)
- **Structure:** Line 1 is a bold claim, metric, or pattern interrupt. Line break. Line 2 is the rehook.
- **Sub-Variants (Rotate across options):**
  - **A. Plain:** Line 2 is a direct counter-intuitive teaser or claim.
  - **B. Parenthesis Wrap:** Line 2 is entirely a parenthetical muttered aside.
  - **C. Strategic ALL CAPS:** Exactly one high-stakes word capitalized in Line 1.
  - **D. List Preview:** Line 1 frames a list and ends in a colon `:`. Line 2 IS the first list item (`- ` or `1. `) and serves as the free sample. The first item must be the most concrete or surprising item of the list, never the most generic.
  - **E. Negation into Prescription:** Line 1 removes a common belief or expensive tool; Line 2 replaces it with the faster/cheaper method.
  - **F. Quoted Opener:** Direct quote from a reader objection, an antagonist critique, or a civilian question.
  - **G. After-Stack Setup:** Both lines begin with "After [cost/obstacle]..." and end with trailing dots.
- **Example:**
  We deliberately made a client post look ugly.

  58,666 impressions. (Our designer was pissed.)

### Format 3: Single-Line Bomb (<= 45 characters, 0 line breaks)
- **Structure:** One short, charged sentence immediately preceding the `...more` cut. Maximum curiosity gap.
- **Rule:** Fails completely if the statement is generic. Must express a polarizing, contrarian, or surprising thesis.
- **Example:**
  SEO has been dying since 1997.

### Format 4: Stacked (Tight or Spaced, Lines <= 50 chars, Final Line <= 45 chars)
- **Structure:** 2-3 short lines establishing a pattern that demands resolution (completion bias).
- **Styling:**
  - *Spaced (blank line between):* Blank lines create emotional pauses. Best for before/after contrast.
  - *Tight (no blank lines):* 2-3 lines read as a single compact block. Line widths must be tightly matched (within 10 width units).
- **Sub-Variants:**
  - **A. Before/After Timeline (spaced):** Two lines contrasting the starting state with the present outcome.
    `2023: 0 followers. $0 revenue. Felt invisible.`
    `2026: 317k followers. $2M+ ARR. Forbes feature.`
  - **B. Countdown Stack (tight):** Three lines using shrinking time intervals (365 days ago / 30 days ago / 2 hours ago). The acceleration builds momentum.
  - **C. Anaphora Stack (tight):** The identical opening phrase repeated across 2-3 consecutive lines.
  - **D. Parallel Regret Stack (tight):** 2-3 lines with identical grammatical structure naming specific avoidance behaviors and emotional costs.
  - **E. Tight Two-Line:** Line 1 frames the authority/context; Line 2 completes the thought with an unresolved hook.
    `As an ex-Google engineer, I reviewed hundreds of sites.`
    `Here is the #1 architecture flaw killing your rankings:`

---

## 5. The Parenthetical Technique

Parentheses perform three distinct direct-response functions in social hooks:

1. **Type A: Mid-Sentence Qualifier (1-2 words):**
   - Injected directly before a noun or claim: `(very)`, `(literally)`, `(ugly)`, `(still)`, `(yet)`, `(fresh)`, `(obvious)`.
   - Sharpens the claim and signals genuine human reflection. "Do not upgrade to the enterprise tier (yet)" sounds like considered advice; without "(yet)" it is merely an imperative.
2. **Type B: Reassurance Closing Line 2 (3-6 words):**
   - Placed at the end of Line 2 to address price, time, effort, or format friction: `(for free)`, `(takes 2 mins)`, `(in one diagram)`, `(with zero code)`, `(fix in 60 secs)`.
   - Lowers the cognitive cost of clicking before the reader commits.
3. **Type C: Full Muttered Aside on Line 2:**
   - The entire second line is enclosed in parentheses, delivered like an informal whisper: `(And it is worse than you think)`, `(normies, keep scrolling)`.

---

## 6. Core Hook Writing Principles

1. **Write the post body FIRST:** The strongest hook is almost never the opening thought. It sits buried in the middle or conclusion as an unexpected metric, a counter-intuitive failure, or a painful realization.
2. **Lead with the payload, not the setup:** Banish warm-up phrasing. Never open with:
   - "I want to share..."
   - "Here is what I learned..."
   - "Let me tell you about..."
   - "In this post..."
   - "I have been thinking about..."
3. **Reader-first framing:** The reader must feel "that is my problem" before discovering the post is a personal case study or client breakdown.
4. **Concrete numbers beat adjectives:** "$4.8M in 2 years (200% quota)" outperforms "crushed our revenue targets."
5. **Zero em-dashes:** Do not use em-dashes (no long dashes). Use colons, commas, periods, or parentheses to control pacing.
6. **Banned cliches:** Disallow AI/LinkedIn cliches:
   - "game-changer"
   - "let that sink in"
   - "read that again"
   - "this changed everything"
   - "they called me crazy"
   - "here is the thing"
   - "the truth is"
   - "I am excited to share"
7. **No emojis or arrows by default:** In top recommendations, omit emojis and unicode arrows. Add them only when explicitly requested by the user.

---

## 7. The Hook Sprint Protocol

When generating social hooks for any post, article, or announcement, execute this 4-step sequence:

1. **Mine the Draft:** Identify the most surprising metric, contrarian take, or sharpest before/after delta in the source material.
2. **Draft 8-10 Options:** Span all 4 formats (Dense, Punchy+Context, Single-Line Bomb, Stacked) and rotate sub-variants.
3. **Pre-Output Validation Pass:**
   - Verify character budgets by role (Full lines <= 50, Last line <= 45 in landing mode).
   - Apply the Cut-Zone Test at characters 42 and 66 for trailing lines.
   - Audit for zero em-dashes and zero banned cliches.
4. **Deliver Output with Top 3 Picks:**
   Present the valid hook options with format, character count, and angle rationale, followed by the **Top 3 Picks** recommended for immediate publication.
