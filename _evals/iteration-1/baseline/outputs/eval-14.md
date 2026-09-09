# Task 14 Response

Realistically: you can start setup work next week, but you should not be sending real cold volume on brand-new domains next week. Doing so is the single fastest way to burn domain reputation before the campaign even gets going.

## Why the timeline is the constraint, not the tooling

New domains have no sending history, no reputation with mailbox providers (Google/Microsoft especially), and no established sender score. Mailbox providers actively watch for exactly this pattern — brand-new domain, sudden high-volume outbound — and will route it straight to spam, or worse, blacklist it early. This isn't a "best practice" nicety, it's how the math of deliverability actually works.

## What's realistic on this timeline

**Week 1 (next week): Infrastructure setup, not sending**
- Register domains (use variants of your main domain, not the primary domain itself, to protect your core brand's reputation)
- Set up SPF, DKIM, DMARC correctly on each domain (this alone can take a few days to propagate/verify)
- Set up mailbox forwarding/aliases, connect to your sending tool
- Begin **domain warm-up**: low-volume automated sending/receiving (warm-up tools or manual seed-list exchanges) starting at ~5-10 emails/day per inbox, increasing gradually
- Build/verify your prospect list and finalize sequence copy in parallel — this doesn't depend on domain readiness

**Weeks 2-3: Warm-up continues, volume increases gradually**
- Ramp sending volume up (roughly doubling every few days, staying well under provider thresholds — typically capping around 20-40 emails/day per inbox during warmup)
- Monitor deliverability metrics closely (bounce rate, spam complaints, inbox placement) — this is where problems get caught before they become expensive

**Week 4 and beyond: Real campaign volume**
- By roughly 3-4 weeks in, domains typically have enough sending history and reputation to support full campaign volume reliably
- This is also when you'd expect to trust your reply-rate data as representative, rather than artificially low due to warmup-stage spam filtering

## The honest tradeoff

If "next week" is a hard deadline for *some* outbound activity, here's what's actually realistic:
- **Low-volume, high-quality outbound next week** on the new domains (very targeted list, low volume, careful monitoring) is fine and is effectively the start of warm-up.
- **Full-scale campaign volume next week** is not realistic without risking the domains you just bought.
- If you need volume immediately, consider running initial volume through an already-warm, established domain/inbox (if you have one) while the new domains warm up in parallel, then transition volume over once they're ready.

Bottom line: plan for a soft launch next week and full volume in 3-4 weeks, not full volume next week.
