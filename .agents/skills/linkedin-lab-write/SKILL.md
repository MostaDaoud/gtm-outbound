---
name: linkedin-lab-write
description: >
  Write LinkedIn posts and related drafting using frameworks from a multi-course library and
  provenance-aware local books, documents, audio, and videos. Produces LinkedIn posts, sales pages, VSL scripts,
  email sequences and launches, cold
  outreach, DMs, ads, landing pages, one-pagers, taglines, and offer structures,
  each built on a named framework with source citations and annotated choices.
  Use when the user says "write a LinkedIn post", "write a sales page", "write a VSL", "write an email
  sequence", "write a launch", "cold email", "write a sales letter", "write an
  ad", "write a one pager", "write a tagline", "draft copy", "linkedin-lab write",
  "write fascination bullets", "bullet copy", "humanize this copy", "make this
  sound less AI", "remove AI clichés", or asks for new or rewritten
  direct-response copy grounded in the course library. For
  scoring copy that already exists, use linkedin-lab-critique instead.
---

# LinkedIn Lab — Write

Produce direct-response copy grounded in the mined library. The output should be
usable as written, with the reasoning visible enough that the user can push back
on specific choices.

**Shared resources.** References and scripts live in the `linkedin-lab` skill
folder, not this one: `../linkedin-lab/references/` and `../linkedin-lab/scripts/`.
Resolve these sibling-relative paths to absolute paths before reading or
executing them. Short
names below — `voice.md`, `offers.md` — mean files in that references directory.

## Step 1 — Establish the brief

Ask only for what you genuinely cannot infer. If the user is mid-flow, state
assumptions and write; a draft with explicit assumptions beats an interrogation.

1. **The one action** this piece should cause
2. **The reader** — who they are, and how aware they already are of the problem,
   the solution category, and this specific product
3. **The offer** — what it is, price, what makes it different
4. **Proof available** — real numbers, testimonials, case studies, credentials
5. **Traffic source** — what they already know on arrival
6. **Position in a sequence**, if any
7. **Voice** — an existing sample is worth more than adjectives
8. **For a value proposition** — category, current alternative, target outcome,
   functional differentiator, and any customer language about the feeling or
   identity the result creates

If the user cannot supply proof, proceed and mark the slots. Do not invent it.

## Critical LinkedIn Lab Rules
- **Voice vs. Proof:** Do not use guests, experts, research, or swipes as the target author's voice. Do not use voice samples or swipes as factual proof.
- **Traceability:** Preserve source IDs and locators through planning, writing, and review.
- **Unsupported Claims:** Mark unsupported factual claims with `[SOURCE NEEDED]`.
- **Integrity:** Never fabricate results, testimonials, client names, or deadlines.
- **Provenance:** Every piece of copy must be traceable to a specific source in the library. Use explicit source IDs (e.g., `[Source: {filename}, {location}]`) for all facts, frameworks, and expert advice.

## Step 2 — Check the offer first

Apply Wendt's question before writing a word: *would you personally hand over
money for this?* If the offer looks like the real problem, say so in one or two
sentences, then write the best version anyway under that stated caveat.
(`offers.md`)

## Step 3 — Pick the framework

| Piece | Default | Reference |
|-------|---------|-----------|
| Email, ad, pitch, script, one-pager | AIDA | `frameworks.md` |
| Long-form sales page | Modified AIDA — AIDA with testimonials interleaved | `frameworks.md`, `sales-pages.md` |
| VSL | Problem → solution → recap → offer introduction | `sales-pages.md` |
| Webinar or live | Big promise → new vs. old way → three secrets → CTA | `frameworks.md` |
| Cold outreach set | Value email → case-study email → Crossroads angle | `emails.md` |
| Launch | Sequence timed to an event, never a standalone ask | `emails.md` |
| Tagline | Dump → trim → trim to under a sentence | `frameworks.md` |
| Nothing fits / blank page | Who, What, Where, Why, When — then a framework | `frameworks.md` |

State which framework you chose and why.

## Step 4 — Load only the references you need

Read the framework file plus the format file from
`../linkedin-lab/references/`. Add `psychology.md` when proof or
persuasion mechanics matter, `offers.md` for pricing or scarcity, `voice.md`
before the final pass. Pull concrete patterns from `swipe-file.md`.
When the deliverable includes fascination bullets, bullets for a sales letter,
or a curiosity-led content inventory, also load `fascination-bullets.md`. Use
its 21 types as a choice set, not a requirement to use every type, and preserve
its secondary-source provenance in annotated source notes.

For a classic sales letter, direct-mail piece, print-style ad, proof-heavy
landing page, or close, load `classic-direct-response.md`. For a welcome
sequence, lead activation flow, consulting outreach campaign, email QA pass,
long-form message skeleton, or formula-led headline sprint, load
`lead-and-email-playbooks.md`. Treat those playbooks as attributed guidance,
not independent proof of performance.

When the user asks to humanize supplied copy, remove AI-like phrasing, match a
voice sample, or fix generic model output, also load `anti-generic-copy.md`.
Apply its reader-facing cluster audit after the structural draft. Do not use a
blind banned-word list, infer authorship, promise detector results, or import its
excluded detector-evasion methods.

For ads, headlines, positioning lines, landing-page first screens,
newsletters, or any request for clearer and more ownable copy, also load
`harry-dry-copywriting.md`. Apply its visual/falsifiable/ownable test to the
load-bearing lines, review the work in its delivery context, and ground any new
specific in verified material.

For a value proposition, positioning line, brand promise, homepage hero, or
messaging architecture, also load `positioning.md`. Build the feature →
functional → emotional → self-expressive ladder, filter claims through the
customer/brand/competitor “winning zone,” then assemble only the slots the final
line needs.

To find material the library does not cover:

```bash
python ../linkedin-lab/scripts/linkedin_lab.py search "your topic" --source all --limit 15
```

Course results cite a lesson and timestamp; local sources cite a page, chapter,
or video timestamp. Use source passages as research, quote only brief excerpts,
and never reproduce a substantial section of a source.

## Step 5 — Draft

Write the skeleton first — the framework's sections as literal headers — then
fill each one, then delete the headers. This is Medhora's method and it is the
fastest route out of a blank page.

While drafting, hold these:

- **Specific over vague.** Numbers on claims, narrowed audience.
  (`sales-pages.md`)
- **Destination over mechanism.** Sell the new kitchen, not the loan.
  (`sales-pages.md`)
- **Features and benefits together**, not benefits alone. (`voice.md`)
- **Benefit layers stay causal.** A feeling or identity claim must follow from a
  delivered functional result; do not bolt aspiration onto an unrelated
  feature. (`positioning.md`)
- **Attention and interest carry more weight than desire.** (`frameworks.md`)
- **Teach-a-friend register.** (`voice.md`)
- **Curiosity and surprise early**, especially in the first sentence.
  (`headlines.md`)
- **Fascinations must be written from real product content.** Withhold the
  resolving detail, never the evidence that an answer exists; add
  `[SOURCE NEEDED]` if the payoff cannot be checked.
  (`fascination-bullets.md`)
- **CTAs near the emotional peaks**, and an early one for readers already
  convinced. (`sales-pages.md`)

## Step 6 — Self-check before delivering

Run these against the draft. They are the highest-frequency failures in the
corpus:

- [ ] No invented statistics, testimonials, results, or client names
- [ ] No fabricated deadlines or scarcity
- [ ] No two buzzwords chained together
- [ ] The value proposition names a target, outcome, meaningful alternative,
      and credible differentiator when the format calls for them
- [ ] Emotional and identity benefits trace back to something the product
      demonstrably does
- [ ] Nothing that reads as generic model output — is there something here only
      this author could have written?
- [ ] Load-bearing lines are visual, supported, and ownable where the format permits
- [ ] If the anti-generic pass was requested: no clustered stock constructions,
      repeated recap structure, or fabricated human-looking details
- [ ] A stranger could restate the offer after one read
- [ ] The single intended action is unmistakable
- [ ] Proof is results-shaped, not praise-shaped
- [ ] Every fascination maps to content that delivers its implied answer
- [ ] Length earns itself — brevity is where the value is

## Output format and delivery mode

Match the user's requested format before applying any template:

- **Clean** (default when the user asks for copy): return the usable copy only,
  plus unavoidable `[SOURCE NEEDED]` or `[DEADLINE: confirm]` markers.
- **Annotated** (when the user asks for reasoning): add the framework, choices,
  alternatives, and source notes after the clean copy.
- **Variants** (when the user asks for options): provide controlled headline,
  hook, or CTA alternatives—not several full drafts.
- **Campaign** (when the request spans channels): build the page, email, and
  social adaptations from the same three to five core points.

Use this full template only for Annotated mode:

```markdown
## {Piece} — {Product}

**Framework:** {name} — {one line on why}
**Reader:** {who} · **Awareness:** {level} · **Action:** {the one action}

---

{THE COPY — clean, ready to use, no annotations inline}

---

### Choices worth knowing about
- **{element}** — {why}, applying {principle} (`reference.md`)

### Alternatives
- **Headline B:** {copy} — {when this one is better}
- **CTA B:** {copy} — {when this one is better}

### Needs from you
- `[SOURCE NEEDED: {type}]` at {location} — {what would fill it}
- `[DEADLINE: confirm]` — {what to verify}

### If this underperforms
{The first thing to change, and why that one first}
```

## Failure and recovery

- If retrieval finds nothing, use the distilled references and label any
  additional recommendation as your own judgment.
- If the offer or proof is missing, draft with explicit `[SOURCE NEEDED]` or
  `[DEADLINE: confirm]` slots rather than inventing facts.
- If source validation reports drift, exclude stale local-book results until
  `linkedin_lab.py ingest` succeeds.
- If the user asks for detector-proof copy, improve reader-facing specificity
  and voice but state that detector classification cannot be guaranteed.

## Notes

**Two to three alternatives for headlines and CTAs**, never for the whole
piece. The user should choose between options, not review drafts.

**Write the sequence alongside the page.** Medhora writes email sequences and
sales pages together, then reuses both on social — the three to five core points
become the pillar piece. (`sales-pages.md`)

**Match the user's format exactly** — MDX in, MDX out.
