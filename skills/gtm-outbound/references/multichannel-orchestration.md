# Multichannel Orchestration — Email, LinkedIn, Phone, Video as One Sequence

Load when designing a cadence that uses more than email, or deciding which channel a
follow-up belongs on.

**Sources checked 2026-09-09.** URLs appear inline where a claim depends on them. Anything
vendor-claimed is marked as such at the point of use.

---

## The Core Principle

Channels are **branches on triggers and non-response**, not parallel blasts. The sequence
is a decision tree: each next touch depends on what the previous one did — opened, replied,
accepted, ignored — not on the calendar reaching day N.

Every touch needs a reason to exist. Before adding anything to a cadence, answer: what
does this touch add that the last one did not? A new angle, a new channel, a new format, a
new ask. Repeating the same message louder on a second channel is not a reason — the
recipient experiences it as the same message, twice.

Two failure modes this prevents:

| Failure | What it looks like | Why it loses |
|---|---|---|
| Parallel blast | Email, LinkedIn, and phone all fire on day 1 | Buys no familiarity on any channel; reads as volume |
| Calendar zombie | Day-14 email sends regardless of the day-3 reply | Replies should exit the sequence, not share it with more blasts |

---

## Conditional Branching — the 2026 Default

The multichannel sequences now in common use are conditional: a non-response on one channel
routes the prospect to the next channel, and any engagement routes them out of the cold
path.

Default branch rules that hold mid-market:

| Trigger | Branch |
|---|---|
| No opens in 3 days | Switch channel — LinkedIn touch |
| Connection accepted, then silent 7 days | Return to email with a new angle |
| Reply of any kind | Exit the sequence — nothing else sends |
| Opened but no reply in 5 days | Stay on email, change the message not the channel |

Three-branch designs (email → LinkedIn → phone) are the norm. Beyond three branches the
gains flatten and the management cost does not.

Source (vendor template, directionally useful — the branching logic is
platform-independent, the mechanics are Lemlist's):
http://help.lemlist.com/en/articles/13942128-lemcoach-how-to-build-a-multichannel-outreach-sequence-email-linkedin

---

## The Agoge Skeleton — Sam Nelson

The best-known full-cadence template: 15 touches over 27 business days.

| Channel | Touches | Notes |
|---|---|---|
| Email | 7 | The backbone; a new angle each time |
| Call | 6 | 2 are voicemails — scripted, not improvised |
| Social | 2 | Engagement, not pitches |

Source: https://www.sybill.ai/blogs/agoge-sequence-to-nurture-your-prospects (Jun 2026).

**2026 practice trims this.** Fifteen touches is a load for mid-market, where one SDR owns
hundreds of accounts; the common adaptation is 8-12 touches with the same channel mix and
shorter gaps. Treat Agoge as a skeleton to adapt, not a law. What it encodes is an ordering
principle — email establishes, phone follows, social fills — and that principle survives
any trim.

---

## Signal-Triggered Timing

The strongest sequences in this family do not start on a calendar day. They start on a
signal: a job change, a funding round, a hiring push. **The signal is the trigger** — the
campaign enters when the event happens, not when the list happened to be built.

This matches `signals-and-triggers.md`: the trigger determines who is on the list, what the
campaign is about, and the first line. Clay Signals packages job-change, funding, and
hiring signals as campaign entry points for exactly this use.

Source: https://www.clay.com/signals

Two orchestration consequences:

- Signal-triggered entry beats the evergreen blast. A 90-day evergreen sequence with a
  signal wedge is weaker than a 10-touch sequence that starts the week the signal fires.
- Non-response branches still apply *inside* the signal-triggered campaign. The signal
  starts it; non-response routes it.

---

## Video Prospecting

The cold-attached Loom died in 2026. What replaced it is permission-first:

1. **Ask first.** A short email or LinkedIn message offering a 90-second walkthrough.
2. **Record on acceptance.** The video goes to someone who said yes.

Working parameters:

| Parameter | Setting |
|---|---|
| Length | 60-90 seconds |
| Format | Screen-share over talking head — show their site, their data, their problem |
| Placement | Follow-up after engagement, never a first touch |

Sources: https://www.youtube.com/watch?v=ghZtQ4CdGSI (Hoani Taylor, Mar 2026);
https://www.mysalescoach.com/blog/video-prospecting (Jun 2026).

The "216% higher response" figure circulating from Terminus is a vendor press-release
claim, not a controlled study — directional only. Use it to justify testing the channel,
not to forecast pipeline.

---

## WhatsApp for GCC

`gcc-market.md` establishes WhatsApp as a legitimate business channel in the Gulf. This
file adds the orchestration rules, and they are deliberately conservative — WhatsApp is the
least-developed channel in this family. Keep guidance conservative until a verified playbook
exists.

| Rule | Detail |
|---|---|
| Business profile | WhatsApp Business profile, never a personal number |
| Opt-in | Expected to be higher than email; treat an unsolicited first message as a brand risk |
| Timing | Human-timed messages, business hours — never automated blasts |
| Consent | KSA PDPL consent requirements apply to WhatsApp marketing too - see `compliance-gates.md` for the jurisdiction table and `gcc-market.md` for channel norms |

The current boundary: one careful human-sent message after an email thread exists. No
automation on this channel.

---

## Phone in Sequence

Call **after** an email touch establishes context, never cold in parallel. The call's first
sentence can reference the email, which converts a stranger's interruption into a follow-up
— a materially different conversation.

Openers, voicemail scripts, and dial caps live in `cold-call.md`. This file owns only the
placement rule: email first, call second, and silence on one channel is the trigger for the
other.

---

## Channel Budgeting

Adding a channel costs attention and tooling, not money. Adding send volume still costs
domain headroom — a second channel does not relax email's constraints, it adds a second
thing to keep warm.

Before scaling any channel, run the numbers through `scripts/gtm_math.py` (model explained
in `gtm-math.md`). CAC and payback gates apply per channel, not just per campaign — a
channel that adds meetings at triple the cost per meeting is a worse channel, whatever its
reply rate says.

---

## Worked Example — 10-Touch Mid-Market Cadence

Business days. Exit-branch states what happens if the touch lands or does not.

| Day | Channel | Intent | Exit-branch |
|---|---|---|---|
| 0 | Email 1 | Poke the Bear — signal observation, open question | Reply → exit. No open → continue |
| 3 | LinkedIn | Profile view + connection request, no note | Accepted → day-5 path. Ignored → day-6 path |
| 5 | Call 1 | Reference email 1 without demanding they recall it | Conversation → qualify. Voicemail → continue |
| 6 | Email 2 | New angle, hypothesis-linked | Reply → exit. Silent → continue |
| 8 | Call 2 | Direct attempt, second hypothesis | Conversation → qualify. Voicemail → leave one |
| 10 | LinkedIn | Comment on their post or company news | Engagement → day-12 email lands warmer |
| 12 | Email 3 | Different stakeholder angle or use case | Reply → exit. Silent → continue |
| 15 | Call 3 | Last dial — cap reached after this | Voicemail → day-17 |
| 17 | Email 4 | Clean close — permission to close the file | Reply → exit. Silent → nurture list |
| 21 | Email 5 | Break-up, one line, door left open | Reply → re-enter. Silent → recycle in 90 days |

Ten touches, three channels, every branch named. If any touch cannot state what it adds
that the previous one did not, cut it — 8 touches beat 10 hollow ones.
