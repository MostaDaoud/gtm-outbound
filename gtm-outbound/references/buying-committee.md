# The Buying Committee — Multi-Threading Outbound

Load when designing contact filters in `gtm-outbound-offer` or sequence tracks in
`gtm-outbound-copy`.

Concepts here draw on the Decision Making Unit framing in the Early Customer Profile
chapter of *Go-to-Market Strategy (GTM)* (the DMU model itself is long-standing B2B
marketing theory). Adapted for cold outbound; the framework is the source's, the
outbound application below is not.

## The Problem With One-Contact Outbound

The default outbound build finds one title per company and sequences it. That works when
the buyer is the user and the price is small. It fails at exactly the deals worth winning,
because as contract value rises the number of people who must agree rises with it — and a
single champion with no internal support stalls at "let me check with the team," which is
where most well-run campaigns quietly die.

Multi-threading is not sending the same email to more people at one company. That reads
as a blast and burns the account. It is sending **different messages to different roles**,
timed so they arrive as a conversation rather than a broadcast.

## The Roles

Six roles. One person often holds several; in a 15-person company the founder may hold
all of them, which is precisely why small-company outbound is easier.

| Role | What they control | What they respond to |
|---|---|---|
| **Initiator** | Notices the problem, starts the search | The problem, named precisely |
| **User** | Lives with the outcome daily | Whether their day gets better or worse |
| **Influencer** | Shapes the criteria and the shortlist | Being consulted; technical credibility |
| **Decider** | Says yes | Business outcome, risk, opportunity cost |
| **Buyer** | Owns the commercial process | Terms, procurement, budget cycle |
| **Gatekeeper** | Controls access | Legitimacy, relevance, not wasting time |

**The Gatekeeper is not always an assistant.** In technical purchases it is often security
review, legal, or an architect with veto power. Discovering the gatekeeper late is what
turns a closed deal into a two-quarter delay.

## Mapping Roles to Filters

This changes `gtm-outbound-offer`. Instead of one title list, build a role map:

```json
{
  "buying_committee": {
    "initiator":  {"titles": ["Head of Growth", "Demand Gen Manager"], "priority": 1},
    "decider":    {"titles": ["VP Marketing", "CMO"], "priority": 2},
    "influencer": {"titles": ["Head of RevOps", "Marketing Ops Manager"], "priority": 3},
    "gatekeeper": {"titles": ["Head of Security", "Data Protection Officer"], "priority": 4}
  }
}
```

**Do not target all four from the start.** Sequence them.

## Threading Order

| Company size | Threading approach |
|---|---|
| Under ~30 staff | Single contact. The founder is the whole committee. |
| ~30-200 | Two threads: initiator first, decider on a delay if the initiator engages |
| ~200-1000 | Three threads, staggered. Initiator, then influencer, then decider |
| Over ~1000 | Full ABM motion. Outbound sequencing alone is the wrong instrument |

**The staggered rule:** start with the person who feels the pain, not the person who signs.
The initiator is cheaper to reach, more likely to reply, and a reply from them gives you
something specific to reference when you approach the decider. Approaching the decider
cold and first wastes your single best shot at the account.

Stagger by 5-8 days. Same week reads as a blast.

## Different Message Per Role

The observation can stay constant. The bridge and the question must not.

| Role | The question is about |
|---|---|
| Initiator | The mechanics of the problem — how are they handling it today |
| User | The daily friction |
| Influencer | How the decision gets made and what the criteria are |
| Decider | The cost of the current approach, in their units |
| Gatekeeper | Whether this is worth routing, and to whom |

Sending the decider's message to the initiator wastes the contact. Sending the
initiator's message to the decider reads as junior and gets deleted.

## Referral Threading

The highest-yield path is a referral inside the account, and the cheapest way to get one
is to be wrong on purpose in a useful direction: approach a plausible-but-adjacent role
and ask who owns it. "Wrong person" replies are a *feature* of this motion, not a failure
— see `gtm-outbound-reply`.

An internal forward outperforms any cold email you could have sent to the same person.

## When Not to Multi-Thread

- Under 30 staff — you are emailing the same person twice
- Deal sizes where the buyer is the user and can expense it
- Where the committee is genuinely one person and you know it
- When your list data is not accurate enough to tell roles apart — a mis-assigned role
  sends the wrong message to the wrong person, which is worse than one clean thread

Multi-threading multiplies both contacts and sends per account. Feed the higher count into
`gtm_math.py size` — the inbox requirement rises with it, and a plan built on
single-threading will be short on sending capacity.
