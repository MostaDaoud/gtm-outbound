# Reply Triage — [Campaign]

Date: [date] · Replies processed: [n] · Source: [live via MCP / CSV export]

---

## Counts

```
[paste reply_classify.py output]
```

| Type | Count | Action |
|---|---|---|
| Interested | | Respond within hours |
| Objection | | Respond same day |
| Referral | | Respond fast — highest value |
| Not now | | Log revisit date, stop sequence |
| Wrong person | | Ask who owns it |
| Unsubscribe | | Suppress immediately, no reply |
| Out of office | | Pause, resume after return date |
| Bounce / auto-reply | | Suppress or re-verify |
| **Needs review** | | Tone decides — read these yourself |

---

## Suppress Immediately

Opt-outs, data requests, and hard bounces. Process within 2 days, permanently, across
every campaign and domain.

```
[addresses]
```

**Confirmed applied:** [yes/no] · **Shared across all campaigns:** [yes/no]

The deterministic classifier owns this list. Never let a conversational read of the
inbox decide whether someone opted out.

---

## Drafted Responses

Draft only. Nothing here has been sent.

### [address] — [classification]
> [their reply, verbatim]

**Draft:**
```
[response]
```
**Reasoning:** [why this response, which objection pattern if any]

---

## Needs Your Judgment

Rows the classifier deliberately did not decide — tone carries the meaning.

| Row | From | Excerpt | Your call |
|---|---|---|---|
| | | | |

---

## Booking

| Prospect | Replied | Times offered | Confirmed | Reminder sent | Held |
|---|---|---|---|---|---|
| | | | | | |

Every step after "yes" is a place to lose them. The meeting is booked when they attend.

**Artifact promised in the CTA:** [what] · **Sent:** [yes/no]
An unfulfilled offer is worse than never making one — it was the reason they replied.

---

## Patterns Worth Routing Upstream

One objection is a conversation. The same objection across twenty replies is a defect in
the offer or the targeting.

| Pattern | Count | Route to |
|---|---|---|
| Same objection repeating | | `gtm-outbound-offer` — the offer is not answering it |
| "Wrong person" repeating | | `gtm-outbound-offer` — contact filters are wrong |
| "How did you get this" | | `gtm-outbound-diagnose` — list source or jurisdiction |
| Positive but never books | | The booking motion, not the copy |
| Replies but no interest | | `gtm-outbound-diagnose` — offer layer |

**Answer recurring objections in the sequence**, not one at a time in replies.

---

## Engagement Signals Captured

Feed these back — they are warmer than any cold trigger and cost nothing.

| Contact | Signal | Revisit date |
|---|---|---|
| | "not now" — [stated reason] | |
