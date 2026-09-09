# SPF + DKIM + DMARC + footer unsubscribe link — are you compliant?

Not fully, and the gap is a meaningful one. SPF/DKIM/DMARC cover email **authentication** — proving the message really came from your domain. That's necessary but it's a separate requirement from what Gmail and Yahoo now enforce for **bulk senders**, which is where your footer link falls short.

## The gap: footer link ≠ one-click unsubscribe

A clickable "unsubscribe" link in the email body/footer is not the same thing as **one-click unsubscribe** as defined by RFC 8058. What's actually required is the `List-Unsubscribe` and `List-Unsubscribe-Post` **email headers**, which let the recipient's mail client (Gmail, Yahoo, Outlook) surface a native "Unsubscribe" button and process the opt-out with a single click — no landing page, no confirmation page, no login. A footer link that takes someone to a webpage to manage preferences does not satisfy this, even if it technically unsubscribes them eventually.

If you're sending any meaningful volume (Google/Yahoo's bulk sender rules apply at roughly 5,000+ messages/day to their domains, though it's safest to just build to the standard regardless of volume), you need the header-based mechanism, not just a body link.

## Why this matters more than it used to

This isn't a "you'll get spam-foldered" issue anymore — since Google and Yahoo's 2024 bulk sender requirements took effect, **non-compliant mail can be outright rejected** at the SMTP level rather than delivered-but-filtered. That's a harder failure mode: you don't get inbox placement data to diagnose it, you just get bounces/rejections.

## The other number you need to be watching: spam complaint rate

Compliance isn't just a technical checklist — Google explicitly ties enforcement to your **spam complaint rate**:
- **0.3%** is the hard enforcement threshold — cross it and you risk being blocked/throttled outright.
- **0.1%** is the working ceiling you actually want to operate under as a safety margin; treat 0.3% as the line you never want to get close to, not a target.

One-click unsubscribe actually helps here — recipients who would otherwise hit "report spam" because there's no easy opt-out now have a frictionless alternative, which tends to lower complaint rates.

## What to fix

1. Implement `List-Unsubscribe` (mailto: or https: link) and `List-Unsubscribe-Post: List-Unsubscribe=One-Click` headers on every bulk/cold email — most modern ESPs and sending tools support this natively, it's usually a configuration toggle rather than custom engineering.
2. Keep the footer link too (good practice, and required in some jurisdictions like under CAN-SPAM/GDPR/CASL), but don't treat it as satisfying the one-click requirement.
3. Instrument and monitor your spam complaint rate per domain/mailbox, with alerting if you approach 0.1%.
4. Verify honor of unsubscribes within a reasonable window (immediately is best; CAN-SPAM requires within 10 business days, but for cold outbound reputation purposes you want it near-instant).

Want me to walk through how to add these headers in whatever sending platform you're using?
