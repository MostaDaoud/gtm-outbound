# Reply Drafts — [Campaign]

Generated: [date] · Load with `gtm-outbound-reply`
Objection depth: `references/objection-library.md` · Bulk use: `assets/templates/reply-triage.md`

**Fill per campaign.** The connective prose is written; every `[bracket]` is campaign
material. These are starting points — edit per recipient, then hand to the user to send.
**Never auto-sent. Draft only. Nothing here has been sent.** The reply skill classifies and
owns the rules; this file shows the drafts. One worked example per reply type, 40-80 words.
Merge tags shown in Smartlead dialect — convert for Instantly.

---

## Interested

**Respond:** within hours · **Their reply:** [e.g., "makes sense — what would working together look like?"]

```
Hi {{first_name}} — [one-line answer to exactly what they asked, no preamble].

Would [Tuesday 10:00] or [Wednesday 14:00] your time work? Reply with either and I'll send
the calendar hold the same day. If both are awkward, name two that aren't and I'll move.

— [your name]
```

**Words:** ~45 · **Rules honored:** friction-to-zero — two concrete times, never times
*and* a link; no deck, no attachments; same-day confirm promised; answers what they asked,
then stops

---

## Objection — Pricing Too High

**Respond:** same day · **Their reply:** [e.g., "that's more than we budgeted for"]

```
Hi {{first_name}} — fair, and thank you for saying it plainly.

Before anything else: what is it high against — the [in-house] cost of doing it, the
[comparable tool] line, or what you'd expect the return to be? I'd rather size the gap
than argue the price. If the honest answer is "not this quarter's spend," that's useful
too — I'll say so and stop.

— [your name]
```

**Words:** ~64 · **Rules honored:** objection is information, not resistance; asks what
it's high against instead of countering; no discount in the first exchange; no case study
in reply to a pricing objection

---

## Objection — Already Have a Vendor

**Respond:** same day · **Their reply:** [e.g., "we already work with [vendor] on this"]

```
Hi {{first_name}} — that makes sense; [vendor] is good at [what they're good at].

One question, then: what would have to be missing from what you have before you'd look at
anything else? If it's [plausible gap for your niche], that's a short conversation worth
having. If nothing is missing, I'll leave you in peace — genuinely.

— [your name]
```

**Words:** ~57 · **Rules honored:** never criticises the incumbent; differentiation
through the missing-piece question, not a feature fight; respect plus an explicit exit
keeps the thread alive for the renewal window

---

## Objection — Send Me Information

**Respond:** same day · **Their reply:** [e.g., "sure — send me some information"]

```
Hi {{first_name}} — happy to, and I'll keep it to one page rather than a deck.

So I send the right thing: what should it answer — [what it costs against status quo],
[how it fits your existing stack], or something else? Whatever you name, it lands
[Thursday] either way, and if it misses the mark, tell me what to fix.

— [your name]
```

**Words:** ~61 · **Rules honored:** diagnoses brush-off versus real request by demanding
specificity; one page answering their question, not twenty pages of overview; a reason to
reconnect built in

---

## Referral

**Respond:** fast — highest value · **Their reply:** [e.g., "this is [colleague]'s area — try [email]"]

```
Hi {{first_name}} — thanks for the pointer; that's genuinely helpful.

Could you forward this thread with a line on why it's worth [colleague]'s time? A forward
from you will land where a cold email from me won't. I won't write to [colleague] directly
unless you say go — and either way, I owe you one for the steer.

— [your name]
```

**Words:** ~58 · **Rules honored:** warm intro over a bare name; never cold-emails the
referral without naming the referrer; explicit permission before any contact

---

## Not Now

**Respond:** same day · **Their reply:** [e.g., "not a priority right now"]

```
Understood, {{first_name}} — I'll stop the sequence here, no more emails from me.

One question so I know when to come back: what would need to be true for this to move up
the list — [a second SDR hired], [the incumbent renewal], [next budget cycle]? I'll watch
for that rather than the calendar. Good luck with [their current priority].

— [your name]
```

**Words:** ~60 · **Rules honored:** taken at face value; one diagnostic question — the
trigger gets logged, not just a date; sequence stopped, because continuing converts a
future opportunity into an opt-out

---

## Wrong Person

**Respond:** same day · **Their reply:** [e.g., "you'll want [team], not me"]

```
Hi {{first_name}} — my mistake, and thank you for the steer instead of a silence.

Who owns [the area] day to day? If you'd forward this with a one-line "worth a look,"
that's the version that lands — but even just a name helps. I'll keep it short with them,
and I won't quote you.

— [your name]
```

**Words:** ~55 · **Rules honored:** no pitch to the wrong person; the cheapest possible
referral ask — a forward if they'll give it, a name if they won't

---

## Unsubscribe

**Respond:** immediate — suppress · **No draft.** The rule is silence.

- [ ] Reply suppressed: nothing sent, nothing pending
- [ ] Opt-out processed across every campaign and domain, within 2 days
- [ ] Shared suppression list updated (`sequence.md` compliance block)
- [ ] No confirmation email, no save attempt

**Rules honored:** suppression is a legal obligation, not a negotiation — no reply, no
confirmation, no attempt to change their mind

---

## Out of Office

**Respond:** nothing to the auto-reply itself. The draft below is the resume touch - it goes on the return date, not before. **Their reply:** [auto-reply, "back [date]"]

```
Hi {{first_name}} — enjoy the time off; everything holds until you're back.

When you return, one question is still standing: [the sequence's open question]? A
one-line answer tells us both whether this is worth a call. I'll follow up
[return date + 1 business day] if I haven't heard from you before then.

— [your name]
```

**Words:** ~42 · **Rules honored:** pause, resume after the stated return date; light
touch — acknowledge, restate the one open question, no re-pitch

---

## Before Sending Any Draft

- [ ] Classified per `gtm-outbound-reply` Step 1 — opt-outs decided by `reply_classify.py`, never by tone
- [ ] Objection drafts load `references/objection-library.md` before the reply goes out
- [ ] Every draft is under 80 words in its longest form
- [ ] Handoff fields captured for anything that books (trigger, hypothesis, their words)
- [ ] Outcome recorded against the account — held, not qualified, or no-show
