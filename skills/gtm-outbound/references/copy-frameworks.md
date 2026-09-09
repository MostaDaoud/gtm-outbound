# Copy — Blocks, Structure, and Spintax

Load when writing or reviewing sequence copy in `gtm-outbound-copy`.

Block decomposition and hook taxonomy adapted from the copywriting lessons in the GTM
course transcripts. The alternative structures and the load-bearing test adapt the
`cold-email` skill in
[coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT).
**Poke the Bear is Josh Braun's** — the course credits him for it, and so must we; the
template swipe file it draws on also credits Eric Nowoslawski, Cold IQ, the Lemlist team
and Jordan Crawford. The sub-80-word gate and the no-ask variant of Poke the Bear are ours.

Benchmark claims checked 2026-09-09; sources live in `gtm-benchmarks.md`.

## The Five Blocks

A cold email is not one thing. It is five components, each with its own job, each
independently testable:

```
1. Subject line       →  gets it opened
2. Hook / intro line  →  earns the second sentence
3. Value proposition  →  says what is in it for them
4. Credibility line   →  makes it believable
5. CTA                →  defines the next step
```

**Test one block at a time.** A rewritten email tells you nothing about *why* the number
moved. A rewritten hook, holding the other four constant, tells you exactly what happened.
Most teams change all five at once and then cannot read the result — size the test with
`gtm_math.py ab` before running it.

Each block maps onto the Value Equation (`value-equation.md`). Ask of every block: which
lever is this moving? A block that moves none is decoration and should be cut.

## Choosing the Shape

**The entry point decides the structure** — what you can credibly lead with determines
which shape fits. Picking a framework that needs a signal you do not have produces a
forced opening line, which is worse than a plainer one.

| You can lead with | Use | Shape |
|---|---|---|
| A specific observation about them | **Poke the Bear** (default) | Observation → bridge → open question |
| An observation plus real proof | Observation → Problem → Proof → Ask | Adds a named result before the ask |
| No signal, but a well-known pain | Question → Value → Ask | Opens on the pain, not on them |
| A recent, dated event | Trigger → Insight → Ask | Names the event, then what it usually implies |
| A close comparable customer | Story → Bridge → Ask | Their peer's situation, then the connection |

**Poke the Bear is Josh Braun's**, and the name is his. The move it describes is the
transition: do not pitch off the hook, bridge from your observation into a question about
the problem your solution addresses. Braun's own version continues into a value
proposition and an ask. **This skill uses a stricter variant** — email 1 stops at the
question — because a first touch to a stranger cannot afford the ask. Know the difference
when you cite it.

**Poke the Bear is the default for email 1** because it is the only one of the five that
does not ask for anything. The others end in an ask — right for a warmed thread, expensive
for a first touch. The mechanism: you are not presenting a solution, you are prodding a
problem the prospect already half-knows they have and letting them react. A question about
a real problem is cheap to answer; a pitch is expensive to refuse, and the cheapest way to
avoid a decision is to not reply. Gong's 85M-email analysis puts a number on it: a pitch in
email 1 cuts reply rate by up to 57% (vendor data,
https://www.gong.io/blog/does-cold-email-even-work-any-more-heres-what-the-data-says,
checked 2026-09-09).

**The goal of email 1 is a reply, not a meeting.** The meeting is negotiated in the thread,
once a conversation exists.

**Selection rule:** if there is no observable signal for this prospect, do not fake one.
Drop to Question → Value → Ask and carry the message on segment relevance instead. A
generic observation is the single most recognisable tell in cold email.

### What Must Not Appear in Email 1

| Forbidden | Why |
|---|---|
| Any pitch or feature list | Converts a cheap reply into an expensive refusal |
| Calendar link | Asks for the biggest commitment at the point of least trust |
| "Quick 15 minutes?" | Same, in disguise |
| "I help X do Y" opener | Signals template immediately |
| Compliment opener | Reads as manipulation; everyone recognises it |
| Company boilerplate | They did not ask who you are yet |

## Relevance Before Personalization

The most commonly inverted priority in outbound. Teams pour effort into per-prospect
personalization and neglect whether the message speaks the recipient's language at all.

**Personalization** is prospect-specific: a podcast quote, a named case study on their site.
**Relevance** is segment-specific: the vocabulary, metrics, and concerns of their function.

If you can do both, do both. If personalization is going to be shallow — and at volume it
usually is — **relevance wins, and it is not close.**

### Two Tests

**Breadth test.** If this exact message went to a thousand other people, would it carry the
same meaning? If yes it is not personalized, whatever the merge tags say. `{{first_name}}`
was personalization a decade ago; nobody reads it as effort now.

**Load-bearing test.** Remove the personalized opening. Does the email still make sense? If
it does, the personalization was decoration. It has to connect to the problem, not sit
beside it.

The two catch different failures — generic copy wearing a merge tag, versus a genuinely
specific observation that never connects to why you are writing. Run both.

### Shallow Personalization Is Worse Than None

"I was on your website and it looks great." "Love what you're building." These actively
signal that a line was generated to claim personalization. Delete them and the email
improves.

This applies to LLM research columns: a Claygent column returning a generic compliment is
worse than an empty one, because empty falls back to a clean segment sentence while the
generic one broadcasts that a machine wrote it. See the empty-return requirement in
`waterfall-enrichment.md`.

### Speak Their Function

Build the sequence around a **segmented list with a narrative per segment**, rather than
one sequence with a personalization slot.

| Segment | Speak in |
|---|---|
| Marketing | CPC, CPL, funnel stages, attribution, pipeline contribution |
| Sales | Quota, ramp time, pipeline coverage, win rate, cycle length |
| RevOps | Data hygiene, routing, stack consolidation, reporting accuracy |
| HR | Time-to-hire, retention, cost per hire, headcount plan |
| Finance | Payback, burn, unit economics, forecast accuracy |

A message using a marketer's actual vocabulary, with no personalization at all, outperforms
a personalized line bolted onto generic copy. The vocabulary is itself the proof.

**This matters more where email is not the dominant business channel** — parts of the
Middle East among them. Where copywriting norms are less established, attempts at
personalization read as awkward more often than thoughtful. Lead with segment relevance.

### What Counts As Value

The email must give something before it asks:

- A specific observation implying a problem you can solve
- A named result for a comparable company, with the number
- Something useful they can act on whether or not they reply

These do not: describing who you are, listing what you sell, asking for time.

---

## Block 1 — Subject Line

**Write it last.** Draft the body, then write a subject expressing what the body actually
says. A subject written first commits you to an email you have not written.

Two to four words. Lowercase. No punctuation, no emoji, **no merge tag** — `{{first_name}}`
in a subject is one of the most recognisable cold-email signatures there is.

**Never look like marketing.** "Don't miss our new plan", "Q4 offer" — filtered by the
reader before the provider gets to it. Write as though from a colleague.

The same Gong analysis adds a specific trap: buzzwords and numbers in subject lines cut
open rates by 17.9% (vendor data), and "AI" itself is called out as a buzzword to avoid —
in 2026 it reads as a claim, not a capability.

| Pattern | Example |
|---|---|
| Relevant KPI | `5x ROAS` · `time to hire` · `logistics efficiency` |
| Domain-expert hook | `smartlead question` |
| Pattern interrupt | `this is a cold email` |
| Intriguing, no context | `are you the right contact?` · `shall I send over?` |
| Personalized | `saw your linkedin post` |

**Deliberate imperfection outperforms polish.** Lowercase openers, no final punctuation —
these read as human. A polished, capitalised, emoji-bearing subject reads as generated,
because it usually is. Some brands refuse this on image grounds; that is a legitimate trade
between reply rate and register.

**The preview-pane consequence.** Gmail renders the first body line under the subject, so
the intro line is part of the *open* decision, not just the read decision. Another reason
the hook carries so much weight.

Generation prompt: draft the body, then ask for **at least five** short subject lines that
read as though sent by a colleague (ten for a new market). Pick one. Asking for a single
option produces the dullest.

## Block 2 — Hook

The first line, and the highest-leverage sentence in the sequence. Three approaches.

**2a. Pain / KPI.** Open on a problem the role actually owns, in their vocabulary. Needs no
per-prospect research, which makes it the fallback when no signal exists. Pattern: *"What
[title]s hate about their job is [specific problem]…"* — naming a real grievance in their
terms proves you understand the role. Vocabulary per function in the table above.

**2b. Recent signal or trigger.** Strongest when available; see `signals-and-triggers.md`.
Usable: promotion or role change in the last 1–3 months, a new joiner, recent funding,
first-time founder, a LinkedIn post, a podcast appearance. New-in-role is among the best —
a fresh mandate and no loyalty to the incumbent.

**2c. Observation.** Something you noticed — **not a compliment**. "Congrats on the growth"
is flattery; "your headcount grew 25% last quarter and that usually breaks X" is an
observation with a thesis attached. Observable and useful: headcount growth, a newly
installed tracking pixel, poor Glassdoor reviews implying an engagement problem, a
published customer result. Open with *I saw* / *I noticed*.

The observation must be something that could only be said to this company:

- Weak: "I see you're in ecommerce." · "Love what you're building at Acme."
- Strong: "Saw the Peloton case study on your site — 3.2x ROAS in 90 days."

Then **one bridge clause** connecting it to a plausible problem — speculative, not
asserted, because you do not know their situation and pretending you do reads as template:
*"Usually when agencies publish numbers like that, the bottleneck moves to lead volume."*

### Two Hooks That Need No Research

**Path-to-you.** Tell them how you found them — not a compliment, just the honest trail.
*"Saw your ad on Facebook, went to the site, then found your profile, and thought I'd reach
out about X."* Stating where you found them is itself evidence of effort at zero research
cost, and it disarms the "how did you get my details" objection before it forms.

**Comparable-client.** *"We just wrapped a project with [comparable] and delivered
[result]. Looking for one more partner like them — searched, found you. Worth a look?"*
Carries on credibility rather than research, which makes it viable at volume when
enrichment is thin.

### Patterns Worth Testing

- *"[Data source] told me you're using [tool] — thought this might be relevant."*
- *"What [title]s hate about their job is [problem], so I wanted to reach out."*
- *"I saw your LinkedIn post about [3–5 word summary] and wanted to reach out."*
- *"Are there internal discussions about [problem] and plans to fix it in [year]?"*

The last one performs oddly well because it reads like an internal question, not a pitch.

### Automating Post-Based Hooks

The wrong prompt is *"find something to personalize on"* — that returns generic flattery.
The right pipeline: filter for people who posted in the last 3 months → enrich the post
text → have the model summarise each in **3–5 words, nothing more** → drop that into a
fixed sentence frame. The constraint is what prevents AI filler.

## Block 3 — Value Proposition

Arguably more important than the hook. The hook earns the second sentence; this is the
first moment they understand what they get.

```
[specific niche]  +  [dream outcome]  +  [risk or effort removed]
```

Every B2B offer resolves to one of five: **earn money · save money · save time · save
effort · reduce risk.** Name which one you are in.

**One niche. One problem. One dream outcome.** Not everything you do — the instinct to list
capabilities is what kills this line.

| Niche | Dream outcome | Risk/effort removed |
|---|---|---|
| B2B HR SaaS — ATS and HR AI tools | 30–50 interested leads | 100% automated, without lifting a finger |
| Saudi real-estate developers | Better ROAS | Without investing in new tools |

Note how narrow the niche is. "HR companies" is not a niche; "B2B applicant tracking
systems" is.

Maps onto the Value Equation: dream outcome is the numerator, removed risk the
denominator. If the line does not visibly reduce a denominator, it is a feature list.

**The most common failure in cold outbound is this line, not the hook.** It gets written as
features rather than end results, or overloaded with everything the business does. It is
also the first place you talk about yourself — if it does not land, nothing downstream
recovers.

## Block 4 — Credibility

The Value Equation's **perceived likelihood of achievement** — the lever that fails most
often in B2B, because a stranger's claim about themselves carries near-zero weight.

| Source | Form |
|---|---|
| Named comparable clients | "We worked with [brand] in your sector" |
| Category + count, under NDA | "Five of the ten largest banks in this market" |
| Average result across clients | "Clients typically see 50–75% ROAS" |
| Relevant anonymised case study | "A ride-hailing company in Saudi — same model as yours" |
| Awards, accreditation | Only where the audience recognises the issuer |

**Relevance beats size.** A smaller logo from their own sector outperforms a larger one from
outside it. Segment the credibility line per campaign. Sending your most impressive name to
a segment that does not recognise it wastes your strongest asset.

The corollary: **credibility the audience cannot evaluate is worth nothing.** Certification
by a platform is powerful inside that platform's community and meaningless outside it.

**The anonymised-relevant play.** You do not need permission to be persuasive. "We worked
with a ride-hailing business in Saudi and delivered [result] — want to see how?" names no
one, breaks no NDA, and lands harder than logos from the wrong industry, because it is
*their* situation.

**No case studies yet?** Credibility comes from risk reversal: a guarantee ("if we do not
reach [outcome] in 90 days, full refund") or performance-based entry ("no fees until your
first 10 qualified leads"). Both transfer risk from them to you. Note the strategic trade —
a first engagement at or below cost buys the logo that makes the next ten easier.

## Block 5 — CTA

Full treatment in `cta-design.md`. In brief: keep friction low in email 1, and as the ask
grows the value offered must grow with it.

In Poke the Bear the CTA **is** the open question. A good one passes all four:

1. Can they answer in one sentence?
2. Do they know the answer without looking anything up?
3. Is it about *their* situation, not your product?
4. Would a peer plausibly ask it in a hallway?

Fails: "Are you looking to improve your outbound?" — yes/no, obviously self-serving.
Passes: "Who's picking up pipeline while you're heads-down on delivery?"

**Soft vs hard is not doctrine.** Soft is the safe default; hard is correct when the value
proposition is strong enough that replying costs no thought. Resolve it empirically — size
the soft/hard arms with `gtm_math.py ab`. ~500 sends per arm resolves only enormous
differences; most realistic lifts need thousands per arm, so a small list tests structural
changes, not word choices. If soft wins clearly, stay soft. If the gap is small take the
hard CTA, because it is a shorter path to the meeting.

| | Soft | Hard |
|---|---|---|
| Form | Open question, no ask | Direct, specific, time-bound |
| Example | "Worth a look?" | "Open to 15 minutes Thursday?" |
| Typical effect | Higher raw reply rate | Lower reply rate, higher meeting rate per reply |
| Suits | High ACV, long cycles, senior buyers | Lower ACV, transactional, high sales capacity |

---

## Word Budget

**80 words maximum, in the longest spintax variant.** Enforced by
`validate_spintax.py --max-words 80` and `score_message.py`.

Not a stylistic preference. Cold email is read on a phone in a preview pane and the reply
decision is made in the first two lines. Length past that adds only reasons to defer.

The same Gong analysis lands near this number — roughly 100 words and 3-4 sentences as the
reply-rate optimum (vendor data). It corroborates the ceiling; it does not move it. Eighty
words stays the worst-case gate enforced here.

Rough allocation: observation 20-30, bridge 15-25, question 10-20, greeting and sign-off
10-15.

**The brevity test:** a finished cold email should read as though it could have been
shorter, never as though it should have been longer.

## Follow-Up Cadence

| Step | Timing | Thread | Content |
|---|---|---|---|
| 1 | Day 0 | new | Poke the Bear |
| 2 | Day 3-4 | same | New angle — a different pain, not a restatement |
| 3 | Day 7-9 | **new thread, new subject** | A different email-1 angle, plus proof: a named result for a comparable company |
| 4 | Day 14 | same as 3 | Clean close |

**Every follow-up must add something** — a new angle, fresh proof, a useful resource. "Just
bumping this" teaches the recipient the thread contains nothing, a lesson they only need
once.

**Each email must stand alone.** Assume they never read the previous one, because most did
not. A follow-up that only makes sense as a reply to your own earlier message is wasted on
most of the list.

The final message closes cleanly and stops. No guilt, no "I'll assume you're not
interested," no breakup framing that is really another ask.

**Step 3 opens a new thread with a fresh subject line.** Steps 1 and 2 belong on one
thread; by the third touch that thread has been ignored twice and is carrying that history
in the reader's inbox. A new subject gets a second first impression — reuse a different
angle from your email-1 variants rather than continuing the conversation they never joined.

**A useful step-3 ask: "would <colleague> be a better person to speak to about this?"**
It is answerable by someone who is not the buyer, which is the point — at this stage any
reply is worth more than the right reply.

### Where to spend your testing budget

**Email 1 carries roughly 80% of the positive replies a sequence will ever produce.** The
follow-ups matter, but they are not where the campaign is won or lost, and testing effort
should be weighted accordingly.

Within email 1, vary in this order:

1. **Value proposition** — the highest-leverage block by a distance
2. **Intro line** — the hook and its observation
3. **CTA** — soft versus hard, per `cta-design.md`
4. **Credibility** — real, but the least movement per test

Hold four constant, vary one. See `Block Testing Is Geography-Dependent` below before
porting a winner into a new market.

**Public templates decay.** Every swipe file worth having is online, which means a template
that works today is being sent by everyone in your category, and it burns per market rather
than globally. A template that performs against one audience can produce nothing against a
near-identical audience elsewhere. Treat any template — including the ones here — as a
starting shape to test, not a formula.

## Follow-Up Emails 2-4

The cadence rules above already require each follow-up to add something and to stand alone.
What has been missing is the arithmetic. Step 1 takes 58% of replies, so the follow-ups
fight for the other 42% — and 84% of positive replies arrive within the first four emails
(Instantly/Woodpecker 2026 telemetry, via `gtm-benchmarks.md`, checked 2026-09-09). The
testing-budget note above counts a different number — roughly 80% of *positive* replies on
email 1. The two agree on priority and disagree on payoff: the follow-ups are the minority
channel, but 42% of replies is too much to spend on bumps. Write them properly; test them
lightly.

Three named follow-up patterns, from Josh Braun's cold-email material:

| Pattern | Shape | What it does |
|---|---|---|
| **The Surrender** | "Should I close your file?" | Hands the exit to them. Answers well, because confirming a door's closure is easier than leaving it ajar |
| **The Presumptive Negative** | "Assuming this isn't a priority this quarter…" | Assumes a benign external cause, not disinterest — correcting you is then the cheapest reply available |
| **The last-email close** | States plainly this is the last one, restates the one question, stops | Scarcity as fact — the sequence genuinely ends — never manufactured urgency |

Braun reports ~70% of a sequence's responses coming from the follow-ups (practitioner
claim, checked 2026-09-09) — a directional argument for writing steps 2-4 properly, not a
benchmark to plan against. Sources: https://joshbraun.com/goingcold ·
https://joshbraun.com/cold-email-ctas

**Reconciling with the no-breakup rule.** The direct-response table at the end of this file
forbids guilt closes, and the cadence rules above forbid "I'll assume you're not
interested." The distinction is who carries the exit. The forbidden close manufactures
guilt to extract one more reply; these patterns state an assumption, make it trivially easy
to correct, and stop when nothing comes back. A surrender that is really another ask is
exactly what the table is for.

## LinkedIn Track

Connection request with **no note** — noteless requests are accepted more often, and a note
spends your one shot before any relationship exists.

After acceptance, a message mirroring the email observation without repeating it verbatim.
Identical text across both channels reads as automation, because it is. Keep LinkedIn under
50 words.

For a phone track, see `cold-call.md`.

## Spintax

### The 2026 Reframe

The default has moved. ESPs and buyers now pattern-match template-family text, and
AI-generated statistically-similar copy is the named cause of the 2026 reply-rate dip —
SmartReach's State of Cold Email 2026 makes the case directly
(https://smartreach.io/reports/state-of-cold-email/the-state-of-cold-email-2026.pdf), with
the same mechanism argued at https://yalc.ai/blog/cold-email-deliverability (checked
2026-09-09). Mechanical spintax spun from a single draft is a footprint now, not
camouflage.

The position:

- Prefer **N genuinely distinct human-written variants** over one draft mechanically spun.
- Rotate at least **5 distinct subject-line variants**.
- `validate_spintax.py` stays as the guard — its worst-case word-count check is the part
  that still matters. Heavy mechanical spintax is no longer the recommended default.

Everything below still governs when spintax **is** used — the platforms collide and the
validator needs the right dialect. What changed is the default, not the mechanics.

Confirm the platform before writing — the conventions collide:

| Platform | Merge tag | Spintax |
|---|---|---|
| Smartlead | `{{first_name}}` | `{{Hey\|Hi\|Hello}}` |
| Instantly | `{{firstName}}` | `{Hey\|Hi\|Hello}` |

Smartlead overloads one delimiter for both; a pipe is the only thing distinguishing them.
Pass `--dialect` to the validator to match.

| Element | Options | Value |
|---|---|---|
| Greeting | 3-4 | Low risk, high volume of variation |
| Observation phrasing | 2-3 | Highest value — the bulk of the text |
| Bridge clause | 2-3 | Good structural variation |
| CTA | 2 | Also serves as the test arm |
| Sign-off | 2-3 | Free variation |

- **Vary structure, not synonyms.** "great" → "awesome" changes nothing and makes review
  harder. Vary sentence shape.
- **Never nest.** Both platforms flatten nested blocks unpredictably; the validator rejects it.
- **Every option must be independently grammatical** in the surrounding sentence.
- **Keep variants under a few thousand per message**, or you cannot read what ships.
- **Watch whitespace inside options** — a leading space produces double spaces in a share of
  sends, which is a visible tell.

Uniqueness also helps placement: identical bodies across hundreds of recipients look like
exactly what they are. See `deliverability.md`.

## Block Testing Is Geography-Dependent

A hook that performs with CEOs in one country can fail with the same title in another. **Do
not port a block library between markets and assume it holds.** Re-test the hook block first
when entering a new geography — it is the block most sensitive to local norms. See
`gcc-market.md` for the Gulf and wider MENA.

## What Direct Response Teaches, and Where It Inverts

Cold B2B outbound borrows its vocabulary from direct response — hooks, headlines, CTAs,
sequences. The debt is real and the classics are worth reading: Schwab on specificity and
self-interest, and the mail-order headline formula sheets that still circulate as swipe
files. Take the discipline of writing to one person about one thing.

**Then stop, because the economics are different.** Direct response optimises a warm,
opted-in list that chose to hear from you. Cold outbound has no such permission, and the
techniques that pay there invert here:

| Direct-response move | Why it fails cold |
|---|---|
| Manufactured deadline — "12 more hours", "last chance" | The deadline is yours, not theirs. A stranger inventing urgency is the clearest bulk-mail signal there is |
| Breakup and guilt closes — "this will be my last email" | Silence is not a debt. There was no relationship to end |
| Headline formulas — "the secret to", "who else wants" | Proven in mail order, instantly recognisable as broadcast in a work inbox |
| Title Case subject lines | Companies capitalise that way; people writing to one person do not |
| Emphasis by CAPS | A promotional-tab signal. Carry emphasis in the sentence |
| Stacked asks — reply *and* book *and* download | One email, one job. A choice splits the response rather than doubling it |
| AIDA / PASOP agitation — "twist the knife" | Requires a pain the reader already told you about. Cold, it asserts knowledge you do not have — see `personalization-depth.md` |

The first six are enforced by `score_message.py`, and the first two fail the message
outright. **Agitation is the exception and stays a human judgement** — "twist the knife"
has no reliable textual signature, and a check that guessed at it would fire on legitimate
problem-framing. Read for it yourself.

The scope boundary in the orchestrator says this skill does not write consumer email
marketing to opted-in lists, and this table is where that boundary becomes concrete.
