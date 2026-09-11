# Cold Calling — The Third Channel

Load when building a multi-channel cadence or writing call openers in `gtm-outbound-copy`.

Email and LinkedIn are asynchronous: the recipient decides when to engage, and silence is
ambiguous. The phone is synchronous, which makes it both higher-yield and higher-risk —
you get a real answer, including a real no, in under two minutes.

## Where It Fits

Calling is not a replacement for the sequence. It is a **second signal on the same
account**, and it works best after an email has already introduced the name.

A workable two-week cadence:

| Day | Channel | Purpose |
|---|---|---|
| 0 | Research + LinkedIn profile view | Register the name |
| 0 | Email 1 | Poke the Bear |
| 3 | **Call 1** | Reference email 1 without demanding they recall it |
| 5 | LinkedIn engagement | Familiarity, not a pitch |
| 7 | Email 2 | New angle |
| 10 | **Call 2** | Direct conversation attempt |
| 14 | Email 3 | Clean close |

The profile view before the first email is deliberate — a name that has appeared once is
not quite cold by the time you call.

The numbers themselves are plumbing: phone-number enrichment is a waterfall output — see
the phone section in `waterfall-enrichment.md`.

## The Opener

Four moves, in this order. It runs about 20 seconds.

1. **Name yourself and your company.** Plainly. Attempting to disguise a cold call fails
   immediately and costs the credibility you needed.
2. **State the reason for the call.** Specifically, and within the first sentence or two.
   This is the single highest-leverage part of the call.
3. **Offer the hypothesis**, qualified — the same observation → inference → hypothesis
   discipline as email. See `personalization-depth.md`.
4. **Ask for a small, bounded permission.** Thirty seconds, not a meeting.

```
"Hi [name], it's [you] from [company]. The reason I called is I saw
[specific observation]. In similar situations, [pattern] usually becomes
the problem before [obvious thing] does. I might be off — can I take
thirty seconds to explain, and you tell me whether it's worth continuing?"
```

Asking permission for thirty seconds rather than fifteen minutes is the same friction
logic as `cta-design.md`: at first contact, ability is the only lever you control.

Gong's cold-call research quantifies the two most-debated openers (vendor data,
https://www.gong.io/blog/cold-call-objections, checked 2026-09-09): "How have you been?"
books at 6.6x baseline (10.01% of calls), and "Did I catch you at a bad time?" is 40% less
likely to book. The numbers confirm the pattern this skill already works from — an opener
that manufactures familiarity and an opener that invites the exit both trade away the
honesty of the first five seconds. Handling the objection once it lands is its own
discipline: see `objection-library.md` → "On the Phone".

## What Not To Open With

**"Did I catch you at a bad time?"** invites the exit — Gong measures it 40% less likely
to book (above). You called unannounced — of course it is a bad time.

**"How have you been?"** books at 6.6x baseline (10.01% — above). It works as a pattern
interrupt precisely because it implies a relationship that does not exist. That is
manufactured familiarity, and it sits against everything else in this skill. A statistical
correlation is not a reason to open with a small deception — do not use it.

**Launching into a pitch** before stating why you called. The reason for the call is what
buys the next fifteen seconds.

## The Mic Drop Method

Belal Batrawy's architecture for the call itself
(https://jed.substack.com/p/85-the-mic-drop-cold-call-method, checked 2026-09-09). Four
stages, in order:

| Stage | Job |
|---|---|
| **Permission** | Earn the next thirty seconds — the same friction logic as the opener above |
| **Problem** | Name the problem, never the product — the call-side mirror of no-pitch-in-email-1 |
| **Provoke** | Make the problem cost something — what it is doing to them while nobody owns it |
| **Promise** | One sentence on what a conversation would give them, then the small ask |

The habit worth keeping regardless of architecture: **map every call in stages and note
where prospects drop off.** A call is a funnel in miniature, and the stage it dies at is
the stage to fix — the same layer-thinking `gtm-outbound-diagnose` applies to a campaign,
applied at call scale. Read that way, exits localize: dying at Permission points at the
list or the dial timing; at Problem, the observation or the segment; at Provoke, an
interesting offer that costs them nothing; at Promise, an ask that outran the value. Ten
calls with stage notes turn scattered exits into one fixable stage.

## Connection Discipline

The phone rewards precision far more than volume, and volume is the default failure.

- **People who answer unknown numbers usually do so on the first or second attempt.**
  Beyond about three unproductive dials, the marginal value collapses — retire the number
  and put the effort into another account.
- **Cap dials per contact**, then move to another channel. Repeated calling with no
  connection is not persistence; it reads as harassment and it is time you are not
  spending on a reachable account.
- Time-of-day patterns are real but local. Test your own windows rather than importing
  someone else's — and note that for MENA the working week itself differs
  (`gcc-market.md`).

## Voicemail

Twenty seconds. Name, reason for call, one sentence of context, and that you will follow
up by email. **No pitch, no callback request** — they will not call back, and asking makes
the message longer for no gain.

Its job is name recognition for the email that follows, nothing more.

## After the Call

Log the outcome against the account regardless of result. A "not now" with a stated reason
is a genuine engagement signal — feed it back per `signals-and-triggers.md`, and the
revisit date belongs in the same place `gtm-outbound-reply` records them.

**A phone no is worth more than email silence.** It closes the loop, frees the capacity,
and often tells you why — which is information the rest of the campaign can use.

## Call Logging

Log every call outcome into the same feedback loop as email replies — outcome recording is
owned by `gtm-outbound-reply`, so outcomes, stated reasons, and revisit dates belong in the
same place whether the contact replied or answered. Call-stage drop-off is a diagnosis
input, not a one-off anecdote: route it alongside reply patterns per `gtm-outbound-diagnose`.

## Compliance

Cold calling is regulated separately from email, and often more strictly.

- **Do-not-call registries** apply in many jurisdictions and can carry per-call penalties
- **Consent rules differ from email** — an email basis does not transfer to phone
- **Call recording** frequently requires disclosure or two-party consent
- Mobile numbers may carry restrictions that landlines do not

Flag jurisdiction before building a calling motion, and recommend the user confirm their
position rather than asserting it is fine. The same discipline as the email jurisdiction
table in `deliverability.md`.
