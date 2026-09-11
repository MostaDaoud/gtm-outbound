# AI SDR Positioning — Manual, Hybrid, or Agent

Load when a client asks whether to hire, hybridise, or subscribe — or when the
orchestrator's motion-fit check reaches the operating-model question.

**Sources checked 2026-09-09.** Pricing in particular moves often; re-verify before
quoting anything to a client.

---

## Three Operating Models

| Model | What AI does | What humans do | Where it fits |
|---|---|---|---|
| **Manual** | Nothing worth naming | Everything | High ACV, tiny volume, founder-led sales |
| **AI-assisted hybrid** | Research, drafting, reply classification | Strategy, targeting, every reply that ships | The default for most B2B outbound |
| **AI SDR agent** | Vendor autopilot: sourcing, sending, replying | Oversight | Low ACV, high volume, tolerant buyers |

The named autopilot vendors as of 2026: 11x (Alice), Artisan (Ava), AiSDR. The category
sells a full SDR seat as a subscription.

---

## The Evidence

The core dataset is a paired study: 100,000 emails, split between AI-run and human-run
sending on the same segments.

| Metric | AI | Human | Reading |
|---|---|---|---|
| Reply rate | 4.1% | 5.2% | Humans still win on quality of conversation |
| Meetings per send | 0.7% | 1.1% | The gap that matters — bookings, not replies |
| Spam flags | 8% | 3% | The real cost: deliverability, not copy |

Source: https://digitalapplied.com/blog/ai-sdr-real-performance-100k-email-analysis-2026
(Apr 2026). Single-source study — treat the magnitudes as one data point and the direction
as the finding.

Against 2024's version of this comparison, the reply-rate gap narrowed. What did not narrow
is the deliverability penalty: AI-sent volume still flags spam at roughly 2.5x the human
rate, and a flagged domain degrades everything else sending from it. See `deliverability.md`
for what a burned domain costs to recover.

Vendor admission worth quoting to clients: Artisan's own CEO conceded that gen-1 AI SDRs
had low response rates, high churn, and hallucination problems — via
https://www.11x.ai/guides/artisan-vs-aisdr-vs-11x (May 2026). The category's own operators
agree autopilot was oversold.

---

## Pricing Anchors

Checked Sep 2026. These move often — re-verify before quoting.

| Vendor | Entry price | Basis |
|---|---|---|
| 11x | $3,750/mo | Annual commitment |
| Artisan | ~$280/mo | Single-source, vendor-adjacent list |
| AiSDR | ~$250/mo | Single-source, vendor-adjacent list |

Source: https://instantly.ai/blog/artisan-vs-other-ai-sdr-tools — a competitor's roundup,
so treat the Artisan and AiSDR figures as approximate.

Two notes on the numbers. First, the spread between the leader and the rest is an order of
magnitude, which means "AI SDR" is not one product category yet. Second, at 11x's entry
point the subscription costs more than a junior human SDR in most markets — the buy
decision at that tier is about volume and consistency, not cost per seat.

---

## The 2026 Consensus

Hybrid wins. AI handles volume and qualification — list building, research, drafting,
classification. Humans handle negotiation and anything that touches a real relationship.

Full autopilot is a segment-fit question, not a default. It can work where ACV is low,
volume is high, and the buyer tolerates a rough first touch. Where ACV funds a human
conversation, autopilot forfeits the meetings that matter — the 0.7% vs 1.1% above is the
whole argument in one row.

---

## Build-vs-Buy Heuristic

Two questions, in order:

1. **Does the ACV support a human SDR?** If yes, hybrid-in-house beats agent
   subscriptions. The human owns replies and strategy; AI owns research and drafting; the
   stack this family builds is the cheapest version of that.
2. **Is volume high and ACV low?** Then agents deserve a test — under the same measurement
   discipline as any campaign. The math skill applies unchanged: same CAC and payback
   gates, same break-even analysis (`gtm-math.md`, `scripts/gtm_math.py`). An agent
   subscription is a channel with a cost per meeting; measure it as one.

---

## Where This Skill Family Sits

This family **is** the hybrid stack. Clay research, ESP infrastructure, deliverability
discipline, human-owned replies. The reply skill's deterministic-first-pass rule
(`scripts/reply_classify.py`) exists precisely because reply handling must not be
autopiloted — an opt-out decided by a language model is a compliance risk, and a
meeting-interest reply mis-sorted by one is a lost meeting.

Positioning against agent vendors is therefore not defensive. The pitch: same
infrastructure, human judgment where it pays.

---

## Orchestrator Integration

The motion-fit check covers outbound vs PLG/ABM but stops there. After "outbound at all?"
and before any build, ask:

> Manual, hybrid, or agent?

Route accordingly. Manual and hybrid run this family as designed. Agent-first clients get
the segment-fit test above first — the family's research and infrastructure still apply,
but the send layer is the vendor's, and the deliverability risk sits with the vendor's
sending practices, not the client's domain.
