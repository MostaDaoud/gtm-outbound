# Eval 9 — "write me a cold email that explains our whole platform, our founding story, and our three pricing tiers, then asks for a demo"

## This request conflicts with a non-negotiable gate

Before writing anything, I need to flag this directly rather than deliver it as asked.

The gtm-outbound-copy skill's "Poke the Bear" framework — which this skill uses for Email 1
of any cold sequence — has a hard rule for the first message a prospect receives:

> Email 1 contains no pitch, no calendar link, and no meeting ask. It ends on an open
> question.

What's being requested — platform explanation, founding story, three pricing tiers, and a
demo ask, all in one email — is close to the maximal version of everything that rule exists
to prevent. Concretely, per `references/copy-frameworks.md`, none of these belong in a cold
Email 1:

- "Any pitch or feature list" — a platform walkthrough is exactly this
- "Company boilerplate" — the founding story is this
- "Calendar link" / "quick 15 minutes?" / demo ask — the meeting ask is this, verbatim

There's also a practical reason, not just a rule: a cold prospect who has never replied to
you yet is being asked, in the same breath, to absorb your company history, evaluate three
pricing tiers, and commit to a meeting. That's the highest-friction version of a first
message possible. It reads as a mass blast, and the realistic outcome is it gets deleted
unread or marked as spam — which damages the sending domain, not just that one lead.

**What I'm doing instead:** writing the actual Email 1 (Poke the Bear — a reply-getter, not
a pitch), and showing exactly where the platform explanation, founding story, pricing, and
demo ask *do* belong — later in the same sequence, after a reply exists to negotiate into.

## Email 1 (what should actually go out first)

No merge-variable schema (`clay-table.json` / `icp.json`) exists in this session, so the
tags below are marked **unvalidated** — in a real run they'd be checked against the Clay
table before shipping. `{{first_name}}` and `{{company_name}}` need producing columns;
`{{sender_first_name}}` was deliberately *not* used as a tag (see note).

**Subject:** cost per call

```
{{Hey|Hi|Hello}} {{first_name}},

{{Noticed|Saw}} {{company_name}} {{has been scaling the SDR team pretty fast this year|posted a couple of new SDR roles this quarter}} — {{usually that's about when cost per booked call turns into the number leadership actually watches|that's usually the point where cost per booked call starts getting real scrutiny}}.

{{How are you tracking that right now|What are you using to track cost per booked call today}}?

{{Best|Thanks|Cheers}},
{{sender_first_name}}
```

That's it. No platform description, no pricing, no demo ask, no company history. It ends
on the open question, per the framework.

### Validator output

Ran against `validate_spintax.py` with the default Smartlead dialect and the 80-word gate.
No `--vars` file was available in this session, so merge-tag existence was **not**
checked against a real schema — only spintax structure and word count were:

```
Spintax validation: PASS  (dialect: smartlead)
  6 spin blocks, 3 merge tags, 0 errors, 0 warnings

  Message                                      Words    Variants
  -------------------------------------- -----------  ----------
  Email 1 — Poke the Bear                      39-46         144
```

39-46 words in the worst-case variant — well under the 80-word ceiling. Before this ships,
`{{first_name}}` and `{{company_name}}` still need real producing columns in a Clay table;
right now they are unvalidated tags, exactly as the skill requires flagging when no schema
exists.

## Where the platform, founding story, pricing, and demo ask actually go

The follow-up cadence is the right place for everything in the original ask — after Email 1
earns a reply, not before it:

| Step | Timing | Content |
|---|---|---|
| Email 1 | Day 0 | Poke the Bear (above) — no pitch |
| Email 2 | Day 3-4 | New angle — e.g., a specific pain the case study addresses. Still no full platform tour. |
| Email 3 | Day 7-9 | Proof: the named result — "cut cost-per-booked-call 34% for a Series B fintech client in 90 days." This is where a one-line mechanism explanation earns its place, once there's context for it. |
| Email 4 | Day 14 | Clean close. If a reply exists by now, pricing and a demo ask belong **in that live thread**, tailored to what they actually said — not broadcast to a cold list. |

The founding story and the three pricing tiers specifically don't belong in any cold-send
step. Founding story is proof-of-legitimacy content for a website or a warm conversation,
not a reason for a stranger to reply. Pricing tiers are a mid-conversation artifact — sent
after discovery, once you know which tier is even relevant to their size. Sending three
tiers cold assumes they've already decided to buy something from you, which contradicts the
entire premise of the first message.

## If a demo ask is the real goal

If the actual objective is "get more demos booked," the fix isn't to front-load the ask —
it's to run this as a real sequence and let the CTA arms compete for it. `gtm-outbound-copy`
builds both a soft-CTA and a hard-CTA arm at the same word budget, sized with
`gtm_math.py ab` before launch, so the demo ask still happens — just at the point in the
thread where it's cheap to say yes to, rather than the first thing they see from you.
