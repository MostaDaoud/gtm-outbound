# 4 inboxes, 1 domain, 25/day each — is that safe?

No. That setup puts you at real risk, and the "25 per inbox" framing is hiding the actual number that matters.

## The number that matters

4 inboxes × 25/day = **100 emails/day sent from one domain**. Mailbox providers (Gmail, Microsoft, Yahoo) don't score your reputation per-inbox — they score it **per domain** (and to a lesser extent per sending IP/subnet). All four of your inboxes are drawing down the same shared reputation pool.

A single domain doing cold outreach is generally considered safe in the **30-50 emails/day aggregate** range, especially while a domain is still relatively young or lightly-warmed. At 100/day, you're 2-3x over that ceiling — spread across four inboxes doesn't change the total load the domain is putting on recipient mail servers and spam filters. From the receiving side, it looks the same as one inbox sending 100/day.

## Why this feels safe but isn't

It's an intuitive but incorrect mental model to think "each inbox is under a per-mailbox limit, so I'm fine." Splitting volume across mailboxes on the *same domain* doesn't reduce domain-level signal like:

- Aggregate complaint rate across all sending from that domain
- Aggregate bounce rate
- Overall engagement/spam-report patterns tied to the domain's DNS records (SPF/DKIM/DMARC all reference the domain)
- Domain age and sending history

If complaints or bounces climb because of volume, the whole domain's reputation degrades — and that drags down deliverability for all four inboxes simultaneously, not just the one that "caused" it.

## The fix: add domains, not mailboxes

If you need to send 100/day of real volume, the right move is to **spread that volume across more domains**, not to add more mailboxes to the domain you already have. A common, safer structure:

- 4 domains (ideally variations of your brand, purchased for sending only — not your primary corporate domain)
- 1-2 inboxes per domain
- 25-30/day per inbox, keeping each domain's aggregate at or under ~30-50/day

That gets you to the same 100/day total output while keeping each domain's individual load inside the safe ceiling, so no single domain's reputation is doing all the work.

## Also worth checking

- Are all 4 inboxes actually warmed (ramped gradually over 2-4 weeks), or did they go straight to 25/day?
- Is SPF/DKIM/DMARC correctly configured for each sending domain?
- What's your current bounce and complaint rate? If you're already seeing elevated bounces (>2%) or complaints (approaching 0.3%), that's a more urgent signal than the raw volume math.

Happy to help you plan the domain/mailbox split if you tell me your target daily send volume.
