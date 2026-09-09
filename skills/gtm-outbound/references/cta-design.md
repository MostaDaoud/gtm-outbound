# CTA Design — Friction, Motivation, and the Ask

Load when designing or diagnosing the CTA block in `gtm-outbound-copy`, or when
`diagnose_campaign.py` routes a weak reply rate to CTA friction.

Behavioural framing adapted from the `marketing-psychology` skill and lead-magnet
mechanics from `lead-magnets`, both in
[coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT).
Outbound application ours.

## Why Most CTAs Fail

The CTA is where the whole sequence either converts or does not, and it is the block
teams tune last. The usual failure is not wording — it is **asking for more than the
message has earned.**

## The Behaviour Equation

A reply happens when three things are true at once:

```
Reply  =  Motivation  ×  Ability  ×  Prompt
```

- **Motivation** — do they care about the problem right now?
- **Ability** — how easy is it to act? This is friction, inverted.
- **Prompt** — is there a clear, unmistakable next step?

It is multiplicative. **If any factor is near zero, the reply is near zero**, and no
amount of the other two compensates. A brilliantly motivated prospect facing a
30-minute-demo ask from a stranger still does nothing, because ability is near zero at
first touch.

This is the theory under the friction table: cold email 1 has *low motivation* by
definition, because you have not yet established that the problem is theirs. The only
lever you fully control at that moment is ability. So make the ask trivially easy.

## The Friction Ladder

| CTA | Friction | Ability | Fits |
|---|---|---|---|
| Open question, no ask | Lowest | Highest | Email 1, always |
| "Worth a look?" | Low | High | Email 1 default |
| "Want me to send it over?" | Low | High | When a resource exists |
| Resource or lead magnet offer | Low–med | High | Value is self-evident without a call |
| "Open to 15 minutes Thursday?" | Medium | Medium | Warm thread, after a reply |
| Calendar link | High | Low | Rarely appropriate cold |
| "Book a 30-minute demo" | Highest | Lowest | Almost never cold |

**The governing rule: as friction rises, the value offered must rise with it.** A
high-friction ask attached to a low-value proposition is the most common cause of a
campaign that delivers fine, gets read, and produces nothing.

## Four Checks Before Shipping a CTA

Adapted from the EAST framing — a CTA should be Easy, Attractive, Social, and Timely:

| Check | Question | Fix if no |
|---|---|---|
| **Easy** | Can they act in under 10 seconds, without a decision? | Cut the ask down |
| **Attractive** | Is there something in it for *them*, not you? | Add value or drop the ask |
| **Social** | Does anything show others like them already did this? | Add a named comparable |
| **Timely** | Is there a genuine reason this is relevant now? | Use the trigger — see `signals-and-triggers.md` |

Timely must be **real**. Manufactured urgency and fake deadlines are the fastest way to
lose a B2B buyer, and they are instantly recognisable.

## The Lead Magnet as a CTA

A resource offer is a genuinely low-friction CTA: it asks for a yes rather than a
calendar slot, and it delivers value before asking for anything.

When it works:
- The resource answers a question the hook just raised
- It can be consumed in minutes, not downloaded and forgotten
- It is specific to their segment, not a generic overview

**Match the asset to where they are:**

| Their state | Asset that fits |
|---|---|
| Unaware of the problem | A diagnostic, benchmark, or teardown that reveals it |
| Aware, comparing approaches | A comparison or framework |
| Ready to act | A template, checklist, or calculator |

Cold email 1 almost always lands in the first row. Offering a pricing comparison to
someone who has not conceded they have the problem asks them to skip two steps.

**Do not gate it behind a form in outbound.** They already gave you their address by
replying — asking them to fill in a form is friction re-introduced for no gain. Send it
in the thread.

## Building the Lead Magnet

Most teams have no lead magnet, which is why their CTAs have no value to offer and
default to asking for a meeting. Practitioner claim worth taking seriously: **the majority
of engagements that failed to produce results traced back to a weak offer and weak lead
magnets**, not to poor targeting or copy.

Three steps:

1. **Identify the customer's dream outcome** — the real one, in their words.
2. **Break it into smaller outcomes** and solve exactly one of them for free.
3. **Make delivery cheap for you.** This is the constraint that decides what is viable.

The third step is where most ideas die, and the fix is usually to shift medium rather than
scope. If you build factories you cannot build a free miniature factory — but you can
produce a one-page plan for the factory they want. Same outcome, different medium, near-zero
marginal cost.

Where the asset is something you already own, this is nearly free. A lead-generation firm
sitting on a scraped database can hand over 1,000 contacts at no real cost. A consultancy
with documented SOPs can send the relevant one.

**Give more of it than feels comfortable.** The common mistake is offering the magnet to
three or four prospects and concluding it does not convert. If one in five to ten
converts, a sample of four proves nothing. Volume is part of the mechanism.

**On giving away know-how:** the objection is always "won't they just do it themselves?"
In practice, rarely. Busy buyers lack time, not information — the method is already public
somewhere. What you are actually selling is execution and attention. Withholding the
know-how mainly costs you the credibility that giving it away would have earned.

## Converting a Hard CTA Into a Soft One

The most useful single substitution in cold email:

> ❌ "Let's jump on a call so I can walk you through a demo."
> ✅ "I recorded a video walking through how it works — can I send it over?"

Same content, radically different ability cost. No calendar, no locked time slot, watched
whenever they like. "Yes, send it" is a far cheaper reply than agreeing to a meeting.

The pattern generalises — put the value **before** the request:

> "We helped [comparable] reach [outcome] and wrote up how. Interested to see it?"

A yes here is also a qualification signal: someone who wants the case study has implicitly
conceded the problem is theirs. That is the moment nurture begins, and it is a better
starting point than a meeting agreed out of politeness.

## Soft vs Hard, Revisited

`copy-frameworks.md` frames these as A/B arms. The behaviour equation explains why the
result varies by context rather than being universal:

- **Soft CTA** maximises ability, so it wins where motivation is low — cold lists, senior
  buyers, long cycles.
- **Hard CTA** requires motivation to already exist, so it wins where the trigger is
  strong and recent, or the pain is acute.

That is why the answer depends on ACV, segment, and trigger strength — and why it must be
tested rather than asserted. Size it with `gtm_math.py ab` before running it.

## Diagnosing a CTA Problem

`diagnose_campaign.py` routes here when placement and list are clean but replies are weak.
Work in this order:

1. **Is the ask bigger than the trust earned?** Almost always the answer. Lower it.
2. **Is there value in the message at all,** or does it only ask?
3. **Is the next step ambiguous?** Two asks in one email is zero asks.
4. **Is the timing claim real** or manufactured?

Only after all four are clean is it worth rewriting the sentence itself.
