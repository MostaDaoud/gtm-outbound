---
name: linkedin-lab-plan
description: >
  Generate strategic LinkedIn content pillars, ideas, post briefs, and editorial calendars
  grounded in the user's specific brand, voice, knowledge, and proof sources.
  Use when the user asks to "plan my linkedin content", "brainstorm post ideas",
  "write a brief for a post about X", "create a content calendar", "plan my content pillars",
  or use the "linkedin-lab-plan" skill. For writing the actual posts use linkedin-lab-write;
  for searching the reference library use linkedin-lab-swipe.
---

# LinkedIn Lab — Plan

Develop LinkedIn strategy, content pillars, post ideas, briefs, and editorial calendars using the user's ingested source material.

**Shared resources.** References and scripts live in the `linkedin-lab` skill
folder, not this one: `../linkedin-lab/references/` and `../linkedin-lab/scripts/`.
Resolve these sibling-relative paths to absolute paths before reading or
executing them.

## Step 1 — Gather context

Planning requires understanding the user's strategic positioning and available material.

1. **Check brand materials**:
```bash
python ../linkedin-lab/scripts/linkedin_lab.py search "" --role brand --limit 50
```
Review the results to understand positioning, audience, offers, beliefs, and boundaries.

2. **Discover available themes**:
```bash
python ../linkedin-lab/scripts/linkedin_lab.py search "" --role knowledge --limit 20
```
Sample the knowledge base to see what topics the user is equipped to talk about.

## Step 2 — Develop Pillars and Ideas

When the user asks for content pillars or ideas:
- Group available `knowledge` and `brand` material into 3-5 core strategic pillars.
- Brainstorm post ideas that align with these pillars.
- For each idea, briefly identify which source material (knowledge/proof) supports it.
- **Do not invent ideas that have no grounding in the user's source material.**

## Step 3 — Write Content Briefs

When the user asks for a brief (or after an idea is selected):
- Determine the post's goal, target audience, and primary hook angle.
- Identify the core argument or story.
- Find specific factual support:
```bash
python ../linkedin-lab/scripts/linkedin_lab.py search "relevant topic" --role proof --limit 5
```
- Outline the structure (e.g., Hook, Body, Proof, Takeaway/CTA).
- Note which sources should be cited in the draft.

## Step 4 — Build Editorial Calendars

When the user asks for a calendar:
- Propose a publishing schedule (e.g., 3x a week).
- Mix different content types (e.g., actionable advice, contrarian takes, personal stories, social proof).
- Assign specific approved ideas to specific days.
- Ensure a balance across the strategic pillars.

## Critical Rules

1. **Role strictness:** Only use `brand` sources for strategic context, `knowledge` for concepts/explanations, `proof` for factual claims, and `swipe` for structural patterns.
2. **Do not write the post:** This skill is for planning. Stop at the brief or calendar stage. If the user wants to draft the post, instruct them to use `linkedin-lab-write` and hand over the brief you created.
3. **Traceability:** Always include the source locators (e.g., `Author — Title @ MM:SS` or file paths) in your ideas and briefs so that `linkedin-lab-write` can reference them directly.
4. **No hallucination:** If the user asks for ideas on a topic not covered by their `knowledge` or `brand` sources, inform them of the gap instead of making things up. Suggest they add new material to `Sources/Research` or `Sources/Podcasts` and ingest it first.
