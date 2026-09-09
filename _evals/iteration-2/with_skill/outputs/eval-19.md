# Re: "SPF, DKIM, DMARC + footer unsubscribe link — am I compliant?"

Not fully. SPF/DKIM/DMARC covers authentication, but the unsubscribe piece is the part
most teams get wrong, and it sounds like you have.

**The gap:** a footer link is not the same thing as one-click unsubscribe. Google,
Yahoo, and Microsoft's bulk-sender requirements (RFC 8058) require the `List-Unsubscribe`
and `List-Unsubscribe-Post` **headers** — machine-readable headers the mail client reads
to render a native "unsubscribe" control right next to the sender name. A link buried in
the email body doesn't satisfy this, no matter how visible you make it. This is
specifically the requirement most often missed because a footer link *feels* like it
covers the same ground.

**Why this matters more than it used to:** since late 2025, non-compliant bulk mail is
**rejected outright**, not filtered to spam. There's no degraded-but-delivered state to
notice and fix later — it either arrives or it doesn't, so this isn't a "nice to have,
slightly better placement" gap, it's a hard delivery failure waiting to happen once
you're inconsistent on it.

**Two more pieces while we're here:**

- Opt-outs need to be honored within 2 days, automatically — not a manual queue.
- Spam complaint rate: **0.30% is where enforcement kicks in, not a safe target.** At
  roughly 3 complaints per 1,000 delivered you're already at the line. Treat **0.1% as
  your actual working ceiling.** Note Yahoo calculates this against inbox-delivered mail
  only (excluding what already landed in spam), so its denominator is smaller — you can
  pass at Google and fail at Yahoo on the same sending behavior. Seed-test across
  providers rather than trusting one aggregate number.

**Bottom line:** add the `List-Unsubscribe` / `List-Unsubscribe-Post` headers on every
sending domain (most ESPs/platforms support this natively — check your sending
platform's settings rather than hand-rolling headers), keep the footer link too (belt and
suspenders, and some clients still show it), and make sure suppression is automatic and
immediate. SPF/DKIM/DMARC alone gets you authenticated, not compliant.
