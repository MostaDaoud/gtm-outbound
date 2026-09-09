# Re: "write me a cold email that explains our whole platform, our founding story, and our three pricing tiers, then asks for a demo"

I'm not going to write that one as specified — it breaks two non-negotiable rules for
email 1, and it would underperform even if I did.

**Why not:**

- **80-word hard cap.** Platform overview + founding story + three pricing tiers doesn't
  fit in 80 words even badly compressed — you'd end up with a wall of text read in a
  phone preview pane, which is the fastest way to get deleted unread.
- **No pitch in email 1.** This isn't a style preference, it's the whole mechanism: a
  question about a real problem is cheap for a stranger to answer; a pitch (what you do,
  who you are, what it costs) is expensive to refuse, and the cheapest way to avoid a
  decision is to not reply. Company boilerplate, feature lists, and pricing are all things
  "they haven't asked who you are yet" — putting them in message 1 converts a cheap reply
  into an expensive one, before you've earned any trust.

**Where that content actually belongs:** spread across the cadence, once a conversation
exists — not compressed into message 1.

| Step | Content |
|---|---|
| 1 (Day 0) | Poke the Bear: observation → bridge → open question. No pitch. |
| 2 (Day 3-4) | A new angle on the problem — still no full pitch. |
| 3 (Day 7-9) | A named, specific proof point — this is where your one case study earns its keep. |
| 4 (Day 14) | Clean close. |

Founding story and a full pricing breakdown don't really belong in the outbound cadence
at all, even in step 3-4 — that's material for the call itself or a landing page you send
once someone's replied, not something a cold recipient has asked for yet. The demo ask
also doesn't belong in message 1 for the same reason a calendar link doesn't: it's the
biggest ask at the point of lowest trust.

**Here's message 1**, using what you've told me about the business (B2B data
consultancy, outbound infrastructure for mid-market SaaS, $24k ACV, one case study — 34%
cost-per-booked-call reduction for a Series B fintech in 90 days). No prospect-specific
observation was given, so this uses the case-study result as the value driver rather than
faking a personalization:

```
Subject: cost per booked call

{{Hi|Hey}} {{first_name}},

{{Curious how|Wondering how}} you're {{tracking|thinking about}} cost per booked call
right now — for a Series B fintech we worked with, that number was usually the real
bottleneck, not lead volume, and it dropped 34% in 90 days once the outbound data
pipeline stopped feeding reps stale lists.

Is cost per booked call something that's on your radar, or is the team optimizing
something else at the moment?

{{Best|Cheers}},
[name]
```

Ran it through the actual gates rather than eyeballing it:

- `validate_spintax.py --max-words 80`: **0 errors, 0 warnings**, longest variant **75
  words** (16 variants total) — inside the cap.
- `score_message.py --max-words 80`: **100/100**, 0 findings — soft CTA, one hedge
  ("usually"), no first-person opener, ends on an open question.

If you want, I can build out steps 2-4 (new angle, then the full case study detail, then
the close) so the platform overview and pricing land where a reader will actually
engage with them — after they've replied, not before.
