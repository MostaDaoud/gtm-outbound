# Objection Library

Load when handling replies in `gtm-outbound-reply`.

## The Governing Rule

**An objection is information, not resistance.** The reflex is to counter. The better move
is almost always to understand first, because a large share of what sounds like an
objection is a real constraint you cannot argue with — and treating a real constraint as
resistance is how you turn a future customer into someone who blocks your domain.

A second rule that saves more deals than any script: **the first objection is often not
the real one.** "Too expensive" frequently means "I do not yet believe this works." Answer
the stated objection and you lose; find the real one and you have a conversation.

## Structure That Works

1. **Acknowledge** the objection as legitimate, without agreeing it is fatal
2. **Ask one question** that surfaces what sits underneath it
3. **Respond** to what they actually said
4. **Return the ball** with a low-cost next step

Never skip step 2. Answering an objection you have not diagnosed is guessing in public.

## The Five

### "Too expensive" / "No budget"

Distinguish the two — they are different objections wearing the same words. *Too
expensive* is a value problem: they do not believe the return. *No budget* is a timing
and authority problem: they may believe you and still be unable to act this quarter.

Ask: what would the return need to look like for this to be worth finding budget for?

- Do not discount. A discount in the first exchange confirms the original price was
  invented, and it re-prices every future deal in that segment.
- Do not send a case study as the reply. That answers a value objection they may not have.
- Budget cycles are real. "Not this quarter" from someone who believes you is a better
  outcome than a discount from someone who does not.

### "We already have a vendor"

The most common and most misread. Usually true, and usually not a no.

Ask: what would have to be missing from what you have for you to look at something else?

- Never criticise the incumbent. It insults the decision and the person who made it.
- The useful outcome is often not displacement but position — being the obvious call when
  the incumbent renews or fails.
- If they are genuinely happy, ask who else in their network is not. This is where
  referrals come from.

### "Send me some information"

Ambiguous. It is either a polite brush-off or a real request, and the two look identical.

Diagnose by making the information specific: what would you want it to answer? A real
request produces a specific answer. A brush-off produces silence or vagueness.

- Do not send a generic deck. It confirms the brush-off and ends the thread.
- One page answering their specific question outperforms twenty pages of overview.

### "Not a priority right now"

Take at face value and ask what would change it.

Ask: what would need to happen for this to move up the list?

- The answer tells you whether it is timing or a soft no. Both are useful.
- Log the trigger, not just a date. "When we hire a second SDR" is more actionable than
  "Q3", because you can watch for it.
- Stop the sequence. Continuing after this converts a future opportunity into an opt-out.

### "How did you get my information?"

Answer plainly and immediately. This is a compliance moment, not a sales one.

- Say exactly where the data came from. Vagueness here is what escalates it.
- Offer immediate suppression and honor it whether or not they ask.
- Do not pitch in the same message. Nothing you say after evasion will land.
- If it recurs across a campaign, route it to `gtm-outbound-diagnose` — it is a list
  sourcing or jurisdiction problem, not a copy problem.

## The Taxonomy Layer

A 300M-call study (Outbound Sales Pro, Aug 2026 —
https://outboundsalespro.com/cold-call-objections, checked 2026-09-09) sorts objections
into three families, and the distribution is the finding:

| Family | Share | What it sounds like |
|---|---|---|
| Dismissive | 49.5% | "Not interested" · "send me an email" |
| Situational | 42.6% | Budget, bandwidth, timing |
| Existing solution | 7.9% | "We already use X" |

Nearly half of what you hear is a brush-off, not an objection — and the incumbent
objection most teams build their playbooks around is under 8%.

This file's five, mapped:

| The Five | Family |
|---|---|
| "Too expensive" / "No budget" | Situational |
| "We already have a vendor" | Existing solution |
| "Send me some information" | Dismissive |
| "Not a priority right now" | Situational |
| "How did you get my information?" | None — a compliance moment, not an objection; handled per its own rules above |

### Per-Family Response Patterns

Family names per Outbound Sales Pro (practitioner naming, checked 2026-09-09):

| Family | Pattern | What it does |
|---|---|---|
| Dismissive | **Disarmingly Blunt** | Drops the script and meets the pattern-matched dismissal with unexpected directness — the one thing the brush-off reflex has no counter for |
| Situational | **Remove the Pressure** | Takes the decision off the spot so the real constraint surfaces — the same acknowledge-then-ask move as the structure above |
| Existing solution | **Miyagi Method** | Demonstrates rather than argues — shows what the incumbent leaves uncovered instead of contesting the decision to have bought it |

## Recurring Objections Are a Specification

One objection is a conversation. The same objection across twenty replies is a defect in
the offer or the targeting.

| Recurring objection | What it actually means |
|---|---|
| "Too expensive" repeatedly | Perceived likelihood is the weak lever — proof is missing, not price |
| "Already have a vendor" repeatedly | Segment is saturated, or the trigger is wrong |
| "Not a priority" repeatedly | The problem is real but not urgent — wrong trigger event |
| "Wrong person" repeatedly | Contact filters are wrong — fix in `gtm-outbound-offer` |
| "How did you get this" repeatedly | List source or jurisdiction problem |

Answer these **in the sequence** rather than one at a time in replies. An objection that
appears in twenty threads should have been pre-empted in email two.

## On the Phone

The library above is email-shaped: time to think, structure visible, tone repairable on
rewrite. Live, the prospect decides in seconds, and parts of this invert. Gong's cold-call
objection research (https://www.gong.io/blog/cold-call-objections, updated Mar 2026,
checked 2026-09-09) gives a three-point sequence:

1. **Validate** — the objection is legitimate; say so
2. **Label the emotion** — "sounds like timing is brutal right now"
3. **Ask a keep-alive question** — anything that keeps them talking

Two effect sizes from the same source (vendor data): "How have you been?" books at 6.6x
baseline (10.01% of calls) — see `cold-call.md` for why this family still declines to open
with it — and "Did I catch you at a bad time?" is 40% **less** likely to book. The opener
that invites the exit receives it.

For the universal case, LAER — **Listen, Acknowledge, Explore, Respond** — is the 30-45
second handling sequence (https://skipcall.io/en/blog/cold-call-objections, checked
2026-09-09). Cap handling attempts at two or three per call: past that, the objection is
the answer, and the graceful move is to ask for the revisit condition and end well.

## What Never Works

- Countering before acknowledging
- Discounting in the first exchange
- "I completely understand, but..."
- Arguing with a stated budget
- Manufactured urgency and fake deadlines
- Following up more aggressively after a soft no
