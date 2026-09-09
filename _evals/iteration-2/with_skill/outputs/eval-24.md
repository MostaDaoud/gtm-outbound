# Re: "Saudi campaign reply rate fell off a cliff last week — pause domains and re-verify the list?"

Not yet. Check the calendar before you touch the domains.

**Why:** a reply-rate collapse in a MENA campaign is genuinely ambiguous in the data — a
calendar effect (Ramadan, Eid, or another local holiday/travel period) and a
deliverability event produce the *same signature*: replies drop off a cliff with no
change in your copy or list. Diagnostic tooling on the ESP export can't tell these apart;
it can only tell you replies dropped, not why. Pausing domains and re-verifying the list
on the assumption it's deliverability, when it's actually a seasonal/calendar effect,
costs you 2-4 weeks of downtime and a re-warm cycle for a problem that would have
resolved itself.

**What to check first, in order:**

1. **What week is "last week," specifically, and does it overlap a known Saudi
   holiday or travel period?** The last 10 days of Ramadan and the Eid windows are the
   classic culprits — replies drop sharply and Eid can flatten them to effectively zero.
   Given the current date, this campaign is unlikely to be sitting inside Ramadan/Eid
   right now, so also check for other calendar effects that hit the same way: summer is
   a heavy travel/vacation period for Gulf professionals (many are out of office for
   extended stretches through July-August), national holidays, or a Hijri new
   year/Ashura-adjacent lull. Any of these can crater reply rate with zero deliverability
   cause.
2. **Sunday-Thursday scheduling.** If this is still running on a Monday-Friday Western
   send window, confirm that isn't compounding the drop — two of your five send days may
   be landing on the Gulf weekend.
3. **Only after ruling out calendar/schedule causes**, look at deliverability signals
   properly: run the diagnostic grouped by inbox first (one dead mailbox in spam can
   look exactly like "everything stopped"), check bounce rate (act above 4%) and spam
   complaint rate (working ceiling 0.1%, enforcement line 0.3%) before assuming placement
   failed.

**Don't pause blindly.** If it turns out to genuinely be a placement issue, pausing and
re-verifying is the right recovery — but do that on evidence (bounce/complaint numbers,
per-inbox variance, seed-test placement across providers), not on "reply rate dropped
last week" alone, because that same sentence is equally consistent with "half your list
is on a beach in August."

If you can share the ESP export (grouped by inbox/segment if possible) and confirm the
exact dates, I can run the actual diagnosis rather than reasoning about it in the
abstract.
