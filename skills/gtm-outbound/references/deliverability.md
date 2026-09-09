# Deliverability — Infrastructure, Warmup & Smartlead Configuration

Load when configuring sending in `gtm-outbound-copy`.

Mailbox provider behavior changes without notice. The numbers below are a working default
profile, not platform limits or guarantees. Treat observed inbox placement as the
authority and adjust.

## Default Sending Profile

| Setting | Default | Reasoning |
|---|---|---|
| Sends per inbox per day | 15-25 | Conservative enough to absorb a reputation dip without pausing |
| **Sends per DOMAIN per day** | **30-50** | **The binding constraint. See below.** |
| Warmup before first send | 14 days minimum | Shorter does not establish enough history to look like a real mailbox |
| Warmup emails per day | 40 | Sustained volume well above the send volume |
| Ramp-up ladder | 10 → 15 → 20 → 25 | Step up only while reply rate holds |
| Warmup reply rate | 30-40% | Signals engagement; higher becomes its own detectable pattern |
| Randomized warmup | On | Fixed intervals are a machine signature |
| **Gap between sends** | **25-30 min, never under 10** | A mailbox firing every 90 seconds is not a person |
| Mailboxes per domain | 2-3 (5 absolute maximum) | Contains blast radius when a domain degrades |
| Open tracking | Off | Costs more in placement than the data is worth |
| Link tracking | Custom domain only | Shared tracking domains inherit others' reputation |

**Warmup and campaign volume share one budget.** Once a mailbox is live, the working
split is 25 warmup + 25 campaign = 50/day total. During the warmup phase warmup runs at 40;
**drop it to 20-25 when live sending starts** rather than leaving it at 40 and stacking
campaign volume on top. The number that matters is the combined figure per domain, not the
campaign figure alone.

**Why 25 rather than more.** Providers evaluate volume against history. A mailbox that has
never sent 100 emails suddenly sending 100 is the pattern being screened for. 25 leaves
room to absorb variance without hitting a limit that forces a pause mid-campaign.

### The Per-Domain Ceiling Binds Before the Per-Inbox One

**Reputation is scored substantially at the domain level, not only per mailbox.** Three
mailboxes each sending a "safe" 25 puts 75 a day on one domain, and practitioner reporting
through 2026 places the working ceiling nearer **30-50 per domain per day**.

This is the most common way a technically conservative configuration still burns:
every inbox looks compliant in isolation while the domain is carrying double what it
should.

Plan from the domain down, not the inbox up:

```
target sends/day  ÷  40 per domain  =  domains needed
domains  ×  2-3                     =  mailboxes
```

At 2 mailboxes per domain, 15-20 per inbox lands inside the ceiling. At 3 mailboxes,
10-15 each. Adding mailboxes to a domain does not add capacity — it splits the same
budget.

Treat 30-50 as reported rather than proven, and let your own placement data overrule it.
But size against the domain figure, because the failure is silent: nothing warns you that
the aggregate is too high, and by the time reply rate falls the domain is already damaged.

**Why warmup continues during sending.** Warmup is not a phase that ends — and given the
account-termination risk around automated warmup networks (see Warmup Schedule), it is
never fully off during campaigns either; run it reduced and continuous. Running it
alongside live sending maintains the engagement ratio that keeps placement stable —
especially important when live replies are, by design, a small fraction of sends.

**Why open tracking off.** The tracking pixel is a spam signal, and since Apple Mail
Privacy Protection began pre-fetching images, open data is unreliable enough that it
cannot justify the placement cost. Measure replies, which are the only signal that
matters — see *Open Rates: Demoted to a Trend Signal* for how far the metric has fallen.

## Domain Strategy

**Never send cold outbound from the primary company domain.** A deliverability incident on
your main domain affects invoices, support, and every internal thread. This is not
recoverable in a day.

Use dedicated sending domains:

- Close variants of the primary: `getacme.com`, `tryacme.com`, `acmeapp.com`
- Redirect each to the main site — an unresolvable sending domain is itself a negative
  signal, and a recipient who checks is exactly the recipient worth keeping
- ~3 mailboxes per domain
- Each domain fully warmed before use

*Domain-selection guidance below checked 2026-09-09.*

- These are **secondary domains, not subdomains of the primary.** A subdomain inherits
  the parent's reputation; a sibling domain does not. Validity's 2025 research reported
  +31% placement for senders on dedicated secondary domains (vendor-claimed,
  https://www.smartlead.ai/blog/email-domains-list).
- Avoid `.biz` and `.online` TLDs alongside those listed in the buying table below.

### How to buy the domain

The domain itself carries reputation before you have sent anything.

| Rule | Detail |
|---|---|
| **Registrar** | GoDaddy, Porkbun or Cloudflare. **Avoid the deep-discount registrars** — they are where bulk spam domains are bought, and that is visible |
| **TLD** | `.com` first. Failing that `.ai`, `.io`, `.net`, `.me`, or the local ccTLD (`.com.sa` in Saudi). Avoid `.xyz`, `.click`, `.agency` |
| **No hyphens, no digits** | `acme-partner1.com` reads as disposable. Plain words only |
| **Carry the brand** | The domain should be recognisably yours. A recipient who does not connect the sending domain to the company treats it as a stranger's |

**Budget for replacement from the start.** A sending domain is consumable. Its lifespan
depends on message quality, offer quality, list quality, and recipient behaviour — the
first three are yours to control, the fourth is not. In practice a domain lasts anywhere
from one month to over a year, and who you send to moves that a long way: CEOs at banks
behave differently from founders at ten-person startups. Buy spares before you need them,
because a replacement bought under pressure still needs its two to three weeks of warmup.

Sizing: `gtm_math.py size` returns the required inbox and domain count. Add roughly 20%
spare capacity — domains do get degraded, and rebuilding one costs two weeks.

## Bulk Sender Requirements

*Provider requirements and enforcement claims in this section checked 2026-09-09:
http://techcommunity.microsoft.com/blog/microsoftdefenderforoffice365blog/strengthening-email-ecosystem-outlook%E2%80%99s-new-requirements-for-high%E2%80%90volume-senders/4399730 · https://staging.dmarcian.com/yahoo-and-google-dmarc-required · http://www.mailgun.com/blog/deliverability/microsoft-sender-requirements · https://easydmarc.com/blog/outlook-new-email-sender-policy-update*

Google, Yahoo, Microsoft, and Apple iCloud now all publish bulk-sender requirements.
Google's took effect 1 February 2024, with Yahoo's alongside it. Microsoft Outlook
announced its requirements on 5 May 2025, began routing non-compliant mail to Junk from
August 2025, and has permanently rejected it at SMTP level (`550 5.7.515`) since November
2025. Apple iCloud now publishes bulk-sender requirements of its own. The regimes have
converged on a shared baseline: roughly 5,000+ messages per day, SPF plus DKIM plus DMARC
(`p=none` minimum, aligned to the visible From domain), RFC 8058 one-click unsubscribe,
and a spam-complaint rate under 0.3%.

**The key shift: non-compliance now means SMTP-level rejection, not merely worse
placement.** Microsoft additionally weighs IP reputation alongside domain reputation, so
a clean domain on a dirty IP no longer rescues the send. Google's error-code ladder
remains — `4.7.x` is a temporary rate-limiting failure (`4.7.27` SPF, `4.7.30` DKIM),
`5.7.x` is a permanent block (`5.7.27`) — but the degraded-but-delivering state is now
narrower than it once was, and mail still arriving is not evidence of compliance. That is
why the seed-testing below is not optional.

| Requirement | Detail |
|---|---|
| **SPF, DKIM, DMARC** | All three, on every sending domain. DMARC may start at `p=none`, aligned with SPF or DKIM. |
| **One-click unsubscribe** | `List-Unsubscribe` (RFC 2369) plus `List-Unsubscribe-Post: List-Unsubscribe=One-Click` (RFC 8058, which defines the second header only). A footer link alone does not satisfy this. |
| **Honour opt-outs within 2 days** | Processing must be automatic, not a manual queue. |
| **Spam complaint rate** | Below 0.30%. Google advises staying under 0.1%. |
| **Valid forward and reverse DNS** | PTR record resolving correctly. |
| **TLS for transmission** | Standard on reputable providers. |

**The 5,000/day threshold** triggers formal bulk-sender status, measured per sending
domain. Most cold campaigns sit well below it — but the authentication, unsubscribe, and
complaint-rate expectations are applied broadly regardless, so treat the whole list as
baseline rather than as something only large senders need.

**One-click unsubscribe is the item most often missed.** Teams add a footer link and
assume they are covered. The requirement is a *header* the mail client reads, rendering a
native unsubscribe control next to the sender name. Its purpose is to give recipients an
alternative to the spam button — and a spam complaint damages reputation in ways an
unsubscribe does not. Adding it protects the domain even below the volume threshold.

**Implementing it.** `List-Unsubscribe-Post` is the most often missed item of the two
headers, so verify rather than assume: confirm the ESP emits both `List-Unsubscribe` and
`List-Unsubscribe-Post: List-Unsubscribe=One-Click` (Smartlead and Instantly do, but
verify per campaign in the current UI — ESP settings move); send one test message and
read its received headers to confirm both appear; and keep the ESP's unsubscribe webhook
pointed at the suppression process, so a one-click opt-out suppresses the address
everywhere automatically.

**Yahoo's complaint maths is stricter.** Its spam rate is calculated against
*inbox-delivered* mail, excluding messages already routed to spam. The same sending
behaviour can pass at Google and fail at Yahoo, because Yahoo's denominator is smaller.
Compliance at one provider is not compliance everywhere — seed-test across providers
rather than reading a single aggregate number.

**0.30% is where enforcement starts, not a safe operating point.** At roughly three
complaints per thousand delivered, you are already at the line. Treat 0.1% as the working
ceiling — which is what `diagnose_campaign.py` warns at.

## DNS Records

All three, on every sending domain, before any warmup begins.

| Record | Purpose | Note |
|---|---|---|
| **SPF** | Authorizes sending hosts | One SPF record per domain. Multiple records fail. |
| **DKIM** | Cryptographic signature | Enables the receiver to verify nothing was altered |
| **DMARC** | Policy for failures | Start at `p=none` to monitor, then tighten |

DMARC progression: `p=none` → `p=quarantine` → `p=reject`. Moving straight to `p=reject`
before confirming SPF and DKIM pass will silently reject your own legitimate mail.

Also configure: custom tracking domain, MX records, and a valid reverse DNS entry.

**BIMI, as a footnote** (checked 2026-09-09): displaying a logo through BIMI requires
DMARC at enforcement (`p=quarantine` or `p=reject`) plus a purchased VMC or CMC
certificate. Cold sending domains stay at `p=none`, so never promise a user logo display
from a `p=none` domain — the two are mutually exclusive.

## Warmup Schedule

| Phase | Days | Warmup/day | Live sends/day |
|---|---|---|---|
| Cold start | 1-7 | Ramp 5 → 40 | 0 |
| Establish | 8-14 | 40 | 0 |
| First sends | 15-21 | Drop to 20-25 | Ramp 10 → 25 |
| Steady state | 22+ | 20-25 | 25 |

**Warmup drops when live sending starts.** It does not stop — it makes room. Leaving warmup
at 40 while adding 25 campaign sends puts 65 a day through one mailbox and blows the
per-domain ceiling with three mailboxes on it.

**Launch against a sample first.** Send to roughly 500 before opening the taps. That is
enough to read a reply rate, and cheap enough to abandon. Scale only while reply rate holds
between 1-5% with positive replies in the 20-50% band; below that, something upstream is
wrong and more volume makes it worse.

**Sending begins on day 15 at the earliest.** Front-loading here is the most common cause
of a campaign that never recovers — and the damage is not visible for the first week,
which is exactly why people do it.

Add roughly three weeks to any campaign timeline that requires new infrastructure. Say
this out loud during planning; it is usually the binding constraint on launch date, not
copy or list build.

*Warmup-risk figures in the paragraphs below checked 2026-09-09.*

**Warmup is now risk-bearing.** Google and Microsoft classify automated warmup networks as
engagement manipulation and terminate accounts over them — GMass shut down its Gmail-API
warmup entirely after a Google ultimatum
(https://gmass.co/blog/warmup-shutting-down). Shared warmup pools compound the exposure:
a domain inherits the behaviour of every other participant in the pool
(https://www.inboxally.com/docs/warm-up-sending-strategy/the-dangers-of-using-an-automated-email-warmup-service).

The practice still measurably works. Across 17,247 warmup inboxes, median inbox placement
was 95% in week one and 98% by week two, and sender domain age was irrelevant to
placement (Pearson r = −0.096)
(https://www.warmupinbox.com/blog/uncategorized/is-email-warmup-dead). The posture that
reconciles the two: keep warmup running through live campaigns at *reduced* volume —
never fully off, since a mailbox that goes silent loses its history — and prefer buying
aged domains outright over pre-warmed purchases whose history cannot be audited.

MailReach describes a 14-day warmup ramping from 5-10/day to roughly 50/day, capped near
100 per inbox per day — vendor-reported, not independently verified
(https://www.mailreach.co/blog/gmail-warmup).

## Content Hygiene

Placement is decided partly by what is *inside* the message, not only by who sent it.

**Minimise or remove entirely:** attachments, images, tracking pixels, and links. Every
one of them is a signal that this is bulk marketing rather than a person writing to a
person. One plain link in a later step is tolerable; none in email 1 is better.

**Spam-trigger vocabulary.** Words that read as commercial rather than conversational —
`free`, `buy`, `purchase`, `ASAP`, discount and pricing language, urgency framing. None is
individually fatal, and the filters are more sophisticated than a word list, but density
matters. Run the draft through a spam checker, or simply ask a model to flag commercial
vocabulary and propose conversational replacements.

**Spintax raises uniqueness, and uniqueness helps placement.** Identical bodies sent
across hundreds of recipients look like exactly what they are. This is a second, separate
reason to spin greetings, bridges, and sign-offs — beyond the reply-rate argument in
`copy-frameworks.md`. Validate with `validate_spintax.py` before sending.

## Double Verification

**Do not trust a data provider's own "valid" flag.** Apollo and similar mark addresses
valid that will still bounce. Their incentive is coverage; yours is deliverability. Run
every address through a dedicated verification tool regardless of what the source claims —
this is the single cheapest insurance in the whole stack, and skipping it is the most
common cause of a bounce rate above the 4% line.

## When You Cannot Wait Three Weeks

Warmup takes what it takes, and rushing it is the most common self-inflicted wound. But
there is a legitimate way to move faster: **burner domains.**

Buy extra domains beyond what the campaign needs. Use them for the first two weeks to test
messaging while the real domains warm properly. Accept from the outset that the burners may
be unusable afterwards — that is the trade you are making, and it only makes sense if
message-testing speed is genuinely worth more than the domain cost.

What this does **not** do is let you skip warmup on the domains you intend to keep. Those
still take their two to three weeks.

## Procurement

Setting up SPF, DKIM, and DMARC by hand is not difficult but is fiddly, and providers exist
that pre-configure it. Resellers of Google Workspace and Outlook mailboxes typically price
well below buying direct — roughly half — and some sending platforms integrate the purchase
so domains and mailboxes arrive with DNS already correct. Buying through the sending
platform is usually worth the small premium purely for skipping the DNS work.

### Mailbox provider ranking

**Google first, by a clear margin.** As of late 2025 the ordering practitioners report is:

1. **Google Workspace** — the most reliable for cold sending, and the gap widened during 2025
2. **Private SMTP** on your own server — viable second option, materially more setup
3. **Outlook / Microsoft 365** — degraded noticeably through 2025
4. **Zoho** — not recommended for cold outbound at all

This ordering has moved before and will move again. It is worth re-checking rather than
inheriting, because the cost of being wrong is a domain rather than a setting.

**Vendor quality varies enough to matter.** Mailbox resellers are not interchangeable —
a bad one delivers mailboxes with broken or half-configured DNS, and you discover it as a
placement problem weeks later rather than as a setup error on day one. Buy from a provider
someone has actually run volume through.

*Pricing and vendor names in this space change constantly — treat any figure you are quoted
as current-only, and re-check before building a cost model on it.*

## Monitoring

*Monitoring additions in this section checked 2026-09-09.*

| Metric | Healthy | Act |
|---|---|---|
| Bounce rate | Under 2% | Ladder below — investigate at 2%, pull the domain at 3%, pause at 4% |
| Spam complaint rate | Under 0.1% | Over 0.3% — pause, the copy or list is wrong |
| Reply rate | 3-8% cold | Under 1% — placement problem, not a copy problem |
| Inbox placement | Over 80% primary | Under 60% — pause sending, extend warmup |

**The bounce-rate ladder is family policy**
(https://www.unifygtm.com/explore/cold-email-2026-domain-setup-deliverability-sequences):
at or under 2% is healthy; above 2% is elevated — check list source and verification
before the next send day; above 3% is danger — pull the domain from rotation and
re-verify; above 4% — pause the campaign. Never ride through the danger tier waiting for
the pause line.

**Register both reputation dashboards before launch, not after a problem.** Google
Postmaster Tools and Microsoft SNDS are the standard monitoring pair; together they are
claimed to cover roughly 49% of B2B inboxes (emailbison.com — vendor-claimed). Postmaster
reads Gmail-side reputation and complaint data; SNDS is Microsoft's own view of your
sending IPs.

**A sudden reply rate collapse is a deliverability event, not a copy event.** Copy
performance degrades gradually. Placement collapses. If replies fall off a cliff while
the copy is unchanged, check placement before rewriting anything.

Seed-test placement weekly with mailboxes across Google Workspace, Outlook, and at least
one other provider. Placement varies enormously by provider, and an aggregate number
hides a total failure at one of them.

## Open Rates: Demoted to a Trend Signal

*Figures in this section checked 2026-09-09:
https://www.geysera.com/blog/email-marketing/are-email-open-rates-dead-in-2026-what-apple-mpp-gmail-proxy-and-bot-opens-mean-for-your-data · https://www.lemlist.com/blog/cold-email-open-rates.*

Open counts no longer measure humans reading mail:

- **Apple Mail Privacy Protection** pre-fetches images for Apple Mail users and accounts
  for an estimated ~49-55% of tracked opens, inflating measured rates by 15-20+ points.
- **AI bot clicks** peaked at over 3M per day in March 2025; major ESPs began
  auto-filtering them from December 2025.
- **iOS 18 Link Tracking Protection** strips UTM parameters from clicked links, so even
  click attribution degrades at the source.

The consequence: open rate is a trend and deliverability signal only. It is never a KPI,
never a success metric, and never the judge of an A/B test. Belkins' 2026 study (7.53M
emails) stopped tracking opens entirely. Report and diagnose on bounce, complaint, and
reply signals instead.

## Recovery

*Recovery timelines in this section checked 2026-09-09 against the 17,247-inbox study
cited in Warmup Schedule
(https://www.warmupinbox.com/blog/uncategorized/is-email-warmup-dead).*

When a domain degrades:

1. Stop sending from it immediately. Continuing makes it worse, not slower.
2. Keep warmup running.
3. Re-verify the entire list — bounces are the most common root cause.
4. Wait 2-4 weeks before resuming.
5. Resume at half the previous volume and ramp again.

**Timelines scale with how fast you catch it.** A reputation catch younger than ~3 days
typically heals in 7-9 days; left 15+ days, recovery stretches to 57-74 days with roughly
51% odds of full recovery. Gmail is the earliest warning signal — Outlook placement lags
it by about a day, so a Google-side dip predicts an Outlook one.

Some domains do not recover. Budget for replacement rather than waiting indefinitely on
one that has stopped landing.

## Compliance

Requirements vary by jurisdiction and this is not legal advice. What belongs in the
configuration regardless:

- A real physical mailing address in the footer
- A working, honored opt-out — process suppressions immediately and permanently
- Accurate sender identity and subject lines
- Suppression lists shared across every campaign and domain, not per campaign

### Jurisdiction

**"The EU" is not one regime.** GDPR sets the data-processing basis, but individual
member states layer their own rules on unsolicited commercial email on top of it, and
those differ sharply. Treating the EU as uniform is the most common error here, and it
runs in the dangerous direction — assuming the most permissive member state applies
everywhere.

| Jurisdiction | The shape of it |
|---|---|
| **United States** | CAN-SPAM — opt-out regime. Cold B2B email is broadly permitted with accurate headers, a physical address, and a honored opt-out. |
| **France** | GDPR legitimate interest is generally available for B2B to a professional address on a work-relevant topic, with a documented balancing assessment. |
| **Germany** | Substantially stricter. The UWG (Act Against Unfair Competition) has generally been applied to require **prior consent** for unsolicited commercial email, including B2B. Germany also has an active `Abmahnung` (cease-and-desist) enforcement culture that makes this a live commercial risk, not a theoretical one. |
| **Canada** | CASL — consent-based, stricter than CAN-SPAM, with individual liability. |
| **UK** | PECR alongside UK GDPR; corporate subscribers are treated differently from sole traders and partnerships. |

**Practical rule:** never tell a user that an EU campaign is fine because it relies on
legitimate interest. Name the specific countries in the target list, flag Germany
explicitly whenever it appears, and say that the basis needs confirming per member state.

This is a summary for campaign planning, not legal advice, and enforcement practice
shifts. Recommend the user confirm their basis with counsel before sending, and never
assert that a given configuration is compliant.

## Placement Testing, Not Guessing

Reply rate tells you something is wrong. **A placement test tells you where the mail is
landing**, which is the thing you actually need before deciding whether copy or
infrastructure is at fault.

Seed-testing tools — Smartlead's own, or a standalone — send to a panel of seeded mailboxes
across providers and score each **sending mailbox and each domain** on what share reached
the primary inbox rather than spam or promotions.

Use it at three moments:

| When | Why |
|---|---|
| **After warmup, before the first campaign** | Confirms the infrastructure works before you spend list on it |
| **Weekly while sending** | Placement degrades gradually; reply rate reports it late and ambiguously |
| **The moment reply rate drops** | Separates a placement problem from a copy problem in one step, which is the whole diagnostic question in `gtm-outbound-diagnose` |

**Below ~50% inbox placement, replace the domain rather than tuning it.** Recovery is
slower than replacement, and every day spent tuning is sent volume at a degraded rate.

**Pause outlier mailboxes rather than the whole campaign.** A single mailbox scoring far
below its siblings is a mailbox problem, not a campaign problem: take it out of rotation,
raise its warmup to 40, leave it a week or two, and retire it if it does not recover.

## Mailbox Presentation

Small things that are checked by exactly the people worth reaching.

- **A real photo on the sending account.** It renders next to the sender name in most
  clients. A default avatar reads as a mailbox nobody uses.
- **A plain-text signature** — name and company. No logo, no image, no link stack, no
  social icons. Each one is a bulk-mail signal, and the signature is where they accumulate.
- **The sending domain must resolve** to your real site. Covered above, and it is the first
  thing a curious recipient checks.

## Sending Window

Configure the schedule in the recipient's timezone, not yours, and match their working week.

**In the Gulf that is Sunday to Thursday** — a Western Monday-to-Friday schedule sends into
a weekend twice and skips two working days. See `gcc-market.md`. Set a wide daytime window
and let the tool distribute within it rather than clustering sends.

### Three settings decide volume, and the smallest one wins

Daily volume is not the number in the daily-limit box. It is the **minimum** of three
independent settings, and platforms let you set them inconsistently without warning:

```
effective sends/day = min( window ÷ gap ,  mailbox daily limit ,  campaign daily limit )
```

A 9am-5pm window with a 20-minute gap is 8 hours ÷ 20 min = **24 sends**, no matter what
the daily limit says. Set the limit to 50 and you still get 24. Conversely a mailbox limit
of 2 caps the campaign at 2 however wide the window is.

**This is the most common reason a campaign "isn't sending".** The volume is silently
throttled by whichever setting is tightest, and nothing flags the mismatch — the campaign
just under-delivers against its projection. Newer platform versions show a predicted send
count on the review screen; when the prediction is below your target, this arithmetic is
almost always why.

Work it backwards: decide sends per inbox per day, then set the gap to
`window_minutes ÷ target_sends` and confirm the mailbox and campaign limits both sit at or
above the target.
