---
name: gtm-outbound-reply
description: >
  Handles what happens after a prospect replies to a cold campaign. Classifies inbound
  replies (interested, objection, referral, not now, wrong person, unsubscribe,
  out-of-office, auto-reply), drafts the response for each type, works a reusable
  objection library (too expensive, already have a vendor, no budget, send me
  information, not a priority), and runs the booking motion from positive reply to held
  meeting. Also maintains suppression hygiene. Use when the user says "how do I respond
  to this reply", "handle objections", "someone replied", "reply handling", "they said
  they already have a vendor", "book the meeting", "triage my inbox", "what do I say
  back", or pastes a prospect reply.
argument-hint: "[pasted reply, or path to a replies CSV]"

---
<!-- fable-discipline-gate:v1 -->

## Pre-flight gate: Fable Discipline (run FIRST)

Before executing any instruction below, adopt the Fable Mindset operating manual at
`C:\Users\mosta\.claude\skills\fable-mindset\SKILL.md`. Apply its Decision Loop
(GROUND -> REASON -> ACT -> OBSERVE -> RE-EVALUATE -> VERIFY -> NARRATE) and its
7 execution rules to every step of this skill. FD runs first; this skill's own
instructions begin only after the discipline is adopted.
# GTM Outbound — Reply Handling

The campaign exists to produce this moment. Everything upstream is wasted if the reply is
answered badly, and most cold sequences are built by people who stop thinking at the
send button.

## Step 1 — Classify

Every inbound falls into one of these. Classification determines everything after it.

| Type | Signal | Priority |
|---|---|---|
| **Interested** | Asks a question, wants detail, proposes time | Respond within hours |
| **Objection** | Engages but pushes back | Respond same day |
| **Referral** | Points to someone else | High value, respond fast |
| **Not now** | Timing, not fit | Log a date, stop sequencing |
| **Wrong person** | Not their remit | Ask for the right one |
| **Unsubscribe** | Any opt-out signal | Suppress immediately, no reply |
| **Out of office** | Auto-generated, dated | Pause, resume after return date |
| **Auto-reply / bounce** | System-generated | Suppress or re-verify |

For a bulk CSV:

```bash
python scripts/reply_classify.py replies.csv --json
```

The script does a deterministic first pass on the unambiguous cases — opt-outs,
out-of-office, auto-replies — which are the ones where a misread is expensive. Read the
remainder yourself; a model reads tone better than a keyword list, but it should never be
the thing that decides whether someone opted out.

**If an MCP connector for the inbox is available**, pull recent replies into that same CSV
shape and classify as normal — see `references/mcp-integration.md`. Two constraints hold
regardless of where the data came from:

1. **Opt-out detection stays in the script.** Never let a conversational read of connector
   output decide whether someone unsubscribed. A missed opt-out is a compliance failure,
   not a bug.
2. **Drafting only.** This skill never sends a reply, with or without a connector.

## Step 2 — Respond by Type

### Interested
Match their energy and reduce friction to near zero. Do not send a deck. Do not send a
questionnaire. Offer two concrete times or a single link, answer what they asked, stop.

### Referral
Thank them, ask for a warm intro rather than just a name. A forwarded email from a
colleague outperforms a fresh cold email to the referred person by a wide margin. Do not
cold-email the referral without mentioning the referrer.

### Not now
Ask one question: what would need to be true for this to be worth revisiting? The answer
tells you whether it is a real timing objection or a soft no. Log the date and stop the
sequence — continuing to send after "not now" converts a future opportunity into an
opt-out.

**Close the loop when the date arrives.** A logged revisit date that never resurfaces is
a list decaying silently. When it arrives, the contact leaves suppression only by
explicit review and re-enters as a **warm trigger** — the date itself is the opener
("when we spoke in March you said Q4"). The re-entry mechanics live in
`references/suppression-mechanics.md`.

### Wrong person
Ask who owns it. Do not pitch. This is the cheapest referral you will ever get.

### Unsubscribe
Suppress immediately and permanently, across every campaign and domain. Do not reply. Do
not send a confirmation. Do not attempt to save it — this is a legal obligation, not a
negotiation. The mechanism — the canonical list artifact, ESP wiring, and the sync
procedure three skills gate on — is `references/suppression-mechanics.md`.

## Step 3 — Objections

Load `references/objection-library.md` from the parent skill.

The governing rule: **an objection is information, not resistance.** The reflex is to
counter it. The better move is almost always to understand it first, because a good share
of what sounds like an objection is a real constraint you cannot argue with, and treating
it as resistance destroys the relationship.

The library also carries a three-family taxonomy (dismissive / situational /
existing-solution, with the 300M-call distribution) and a phone-specific handling
section — use the phone section whenever the objection arrived on a call rather than in
email, because the right moves invert on a live line.

Never:
- Counter before acknowledging
- Discount within the first exchange
- Send a case study in reply to a pricing objection
- Argue with a stated budget

## Step 4 — The Booking Motion

Positive reply to held meeting is where most outbound leaks.

1. Propose two specific times, or send one link. Never both.
2. Confirm the same day.
3. Send a one-line reminder 24 hours out that restates why they said yes.
4. If they no-show, one message assuming good faith and re-offering.

**Every step after "yes" is a place to lose them.** The meeting is not booked when they
say yes; it is booked when they attend.

## Step 4b — The Handoff

The meeting is booked. Outbound's job is nearly done, and this is where its work most
often gets wasted.

**Write the handoff before the meeting happens.** Whoever runs it — the same person or a
closer — needs what outbound already knows, and reconstructing it from a calendar invite
loses the thread that earned the reply:

| Field | Why it carries |
|---|---|
| The trigger that opened the conversation | The meeting should continue that thread, not restart |
| The exact hypothesis put to them | If it was wrong, that is the first thing to establish |
| What they actually replied | Their words, not a summary — vocabulary matters |
| Objections already raised | Re-litigating a handled objection reads as not listening |
| The offer they accepted | If they said yes to a case study, lead with it |
| Segment and role | Which committee seat they occupy — see `references/buying-committee.md` |

A meeting that opens by asking questions outbound already answered tells the prospect
nobody read the thread.

**Confirm the artifact exists.** If the CTA promised a checklist, teardown, or comparison,
it must be real and sent before the meeting. An unfulfilled offer is worse than never
having made one — it was the reason they said yes.

**Record the outcome against the account**, held or not:

- **Held and qualified** → the trigger and hypothesis are validated. That combination is
  now a proven play; note it for the next campaign.
- **Held, not qualified** → the ICP filters let through someone who should not have been
  there. Route to `gtm-outbound-offer`.
- **No-show** → one message assuming good faith and re-offering. If a segment no-shows
  repeatedly, the yes was politeness rather than interest, which is a CTA problem.

**No-show rate is an outbound metric, not a calendar metric.** Sustained no-shows mean the
CTA is extracting agreement the message did not earn — see `references/cta-design.md`.

## Step 5 — Feed It Back

Reply data is the highest-quality signal the campaign produces. Route it:

| Pattern in replies | Feed to |
|---|---|
| Same objection repeatedly | `gtm-outbound-offer` — the offer is not answering it |
| "Wrong person" repeatedly | `gtm-outbound-offer` — contact filters are wrong |
| "How did you get my information" | `gtm-outbound-diagnose` — list source or compliance |
| Positive but never books | The booking motion, not the copy |
| Replies but no interest | `gtm-outbound-diagnose` — offer layer |

A recurring objection is a specification for the next campaign. Objections that repeat
across 20 replies should be answered *in the sequence* rather than handled one at a time.

## Outputs

For a single reply: the classification, the drafted response, and the reasoning. Worked
drafts for every type live in `assets/templates/reply-drafts.md` — fill one rather than
starting from a blank page, and annotate which rules the draft honors.

For a batch: `REPLY-TRIAGE.md` from `assets/templates/reply-triage.md`, with counts by type, drafted responses for anything needing
one, the suppression list, and the patterns worth routing upstream.

## Working the Unified Inbox

At any real volume replies arrive across dozens or hundreds of mailboxes, and logging into
each is not a workflow. Sending platforms consolidate them into one inbox. Three controls
there matter more than the rest:

**The suppression list is a control, not a report.** Marking a lead "do not contact" adds
them to a global block list that blocks *every* campaign and domain on the account, not
just the current one. This is the mechanism behind the permanent-suppression rule above —
use it rather than deleting a row, which suppresses nothing.

**Build the block list before launch, not after.** Upload existing customers, live
opportunities, current suppressions, and anyone the client has asked you not to touch.
The most damaging cold email you can send is one to an account your colleague is already
closing, and it is entirely preventable with an upload that takes two minutes.

**Out-of-office has a resume date, and the tool holds it.** An auto-reply pauses that
lead's sequence. Set it to resume a few days after their stated return rather than
cancelling — the sequence continues from where it stopped, which is exactly the handling
the classification table above prescribes.

**Reply categories drive the analytics number.** The platform lets you declare which
categories count as "positive", and campaign reporting follows that declaration. Decide the
mapping deliberately and write it down, because a positive-reply rate is uninterpretable
without it — see `references/gtm-benchmarks.md`.

## Reply Agents: Draft, Never Auto-Send

Sending platforms now ship AI agents that can answer inbound replies unattended, scoped to
an account, a client, a campaign, or a single reply category, with a choice between
auto-send and generate-a-draft-for-approval.

**Configure the draft mode. Never the auto-send mode.** This is the same standing rule as
the rest of the skill: a reply is outward-facing, irreversible, and goes to a real person
who has just engaged — which makes it the *worst* place to remove the human, not the most
convenient. An agent that mishandles an objection or answers a pricing question wrongly does
so in the one conversation the entire campaign existed to produce.

Draft mode is genuinely useful and worth setting up: it drafts against your context and
waits for approval, which is the same shape as this skill's own output.

If the user decides to run auto-send anyway, that is their call on their account. Say
plainly what the exposure is, and do not configure it for them.

## Boundary

Draft responses for the user to review and send. Do not send email on the user's behalf,
and do not describe a drafted reply as though it has already gone out.
