<!--
Synthetic fixture. Reproduces the STRUCTURE of a widely circulated direct-response
consulting sequence in original wording -- no source text is copied. Every message here
is meant to fail: it exists to prove the DR-inversion checks in score_message.py fire.

Expected: all three messages fail. Email 3 must raise DR_FORMULA, TITLE_CASE_SUBJECT and
SHOUTY_CAPS; Email 5 must raise FALSE_SCARCITY and GUILT_CLOSE. Email 1 must raise
MULTIPLE_ASKS. The line wrapping is deliberate -- phrases straddle line breaks, which is
what the whitespace-flattening in analyse() exists to survive.
-->

# Email 1 — primary outreach

Subject: Hey. I'd Like To Help You Get More Paying Customers

Hi {{first_name}},

I recently stumbled across your website and noticed it isn't set up to convert.
Because of that, you're leaving real money on the table.

This is quite easy to fix. I've been helping founders like yourself grow revenue
for years and I'd like to help you rebuild the site. That would let you generate
new customers predictably, every month, and grow the business substantially.

We can discuss details, but first I wanted to see whether this interests you. If
so, would it be okay if I sent over a few ideas? You can also grab a slot on my
calendar here.

# Email 3 — the strategy session

Subject: The Real Secret To Generating High-Ticket Clients On Demand

Hi {{first_name}},

Right on. It's always a pleasure to work with someone open to new opportunities.

Based on your situation I've identified 3 fundamental elements that, once
optimized, could fuel serious growth. The system is completely automated, custom
tailored, and you don't have to do anything technical yourself.

If you're open to it, we can schedule a 30-min private strategy session. It is
completely FREE and you'll walk away with valuable insights either way. Go ahead
and reserve your spot right now on the link here.

# Email 5 — the breakup

Subject: Goodbye from Alex

{{first_name}},

I was looking forward to helping you fix your conversion problem, but I haven't
heard back. This will be my last email and your last chance to find out how you
could double your sales.

I'd hate to see you leave money on the table, so I'll hold the opportunity open
for 12 more hours. After that it's gone. Book your FREE 30-min strategy session
right here to fix these critical mistakes.
