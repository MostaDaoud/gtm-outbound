# GCC & MENA Market Adaptations

Load whenever the target list includes Saudi Arabia, the UAE, Egypt, or the wider Gulf.
Every default in this skill is calibrated on North American and European outbound. Several
of them are wrong here, and the failure mode is silent.

Adapted from the GCC-specific GTM lesson in the course transcripts. Coverage figures are
the source's observations, recorded 2024; re-verify quarterly before sizing any campaign —
contact-data coverage drifts materially.

## 1. Data Coverage Is the Binding Constraint

This is the difference that breaks imported playbooks.

Figures for Saudi Arabia (recorded 2024 — historical context, not current supply):

| Layer | Approximate |
|---|---|
| LinkedIn users in market | ~10,000,000 |
| Profiles available in Apollo | ~1,700,000 (under 20%) |
| Verified emails available | ~443,000 (roughly 4% of the market) |

Do not size from these numbers. List sizing must re-check live coverage at build time
(`gtm_math.py --tam`) rather than trusting any figure recorded here.

Tools like Apollo and Sales Navigator were built for Western markets — their coverage,
their taxonomies, and their user base all skew that way.

**Consequences for the list stage:**

- A single-source list is not viable. Multi-source plus heavy enrichment is mandatory,
  not an optimisation.
- Waterfall enrichment matters far more here than in US or EU campaigns, and expect a
  lower hit rate at every step.
- Phone numbers are as hard as emails.
- Size the raw scrape far above the Western defaults in `gtm_math.py size`. A 70%
  verification pass rate is a Western assumption; expect materially worse.

**Flag this explicitly when scoping a MENA campaign.** A goal that is reachable in the US
against a 4,000-company TAM may be unreachable here purely on data availability, and that
finding belongs in the offer stage, not after the list build fails.

## 2. Sales Cycles Are Longer

A deal that closes in a week in the US can take **3–5 months** in Saudi or Egypt. An
"interested" reply is the beginning of a relationship, not the start of a close.

Feed this into `gtm_math.py economics` via `--contract-months` and expect payback to
stretch. A campaign judged on 30-day pipeline will look like a failure while working
correctly.

## 3. The Calendar Is Different

**The working week is Sunday to Thursday.** Weekends are Friday and Saturday. Sending
Monday–Friday on a Western schedule wastes two send days and lands on two weekend days.

**Public holidays crater reply rates:**

| Period | Effect |
|---|---|
| Last 10 days of Ramadan | Replies drop sharply, especially in Saudi |
| Eid | Effectively zero response |

Plan sending windows around both. When diagnosing a reply-rate collapse in a MENA
campaign, **check the calendar before checking placement** — this is a genuine confound
that `diagnose_campaign.py` cannot see, and it will look exactly like a deliverability
event.

## 4. Language: Segment, Do Not Blanket-Rule

The common advice — "Saudi means Arabic only" — is wrong. It depends entirely on who
receives the email.

| Segment | Prefer |
|---|---|
| Saudized departments, HR especially | Arabic |
| IT and software roles | English — largely Indian and Pakistani expatriate staff |
| UAE generally | English — more dominant than in Saudi |
| Saudi government-facing correspondence | Arabic |

**Reply rate can roughly double** when Arabic-speaking recipients in Saudi receive Arabic
copy. That is a larger effect than any copy framework in this skill.

**Sales Navigator has a Profile Language filter.** Use it to split the list into Arabic
and English tracks rather than guessing from geography. This is the single most actionable
tactic in this reference.

The Gulf is multi-cultural — one company's list may include American, European, Indian,
Pakistani, and Filipino recipients. Language is a property of the contact, not the country.

**UAE is not Saudi.** Treating them identically is a real mistake: English is far more
prevalent in the UAE, while Arabic carries further in Saudi.

## 5. E-commerce Runs on Different Platforms

Western ecommerce plays target Shopify and WooCommerce. In Saudi, **Zid and Salla** hold
the larger share.

Neither is well covered by Apollo or Sales Navigator. Storeleads does carry them. A
"Shopify brands in Saudi" campaign built on Western sourcing assumptions will return a
small, unrepresentative slice of the actual market.

## 6. WhatsApp Is a Legitimate Business Channel

In many Western markets WhatsApp reads as friends-and-family and using it for outbound is
intrusive. In Saudi the culture is more open to business conversation there, and it can
outperform email.

Treat it as a real channel in the multi-channel plan rather than importing the Western
taboo. Apply the same consent and opt-out discipline as email.

### Never open on WhatsApp — earn it with a prior touch

A cold WhatsApp message to a stranger is an intrusion into a personal channel and gets
blocked. **Sequenced second, it is one of the highest-reply steps available here.**

Send email or a LinkedIn message first. Then open on WhatsApp by referring to it:

> I sent a note to *<their email>* and wasn't sure it reached you, so thought I'd try here.

That framing works because it is true, it explains how you got the number, and it gives
them something to react to. Reply rates in the 20-30% range are reported for this step —
several times what the same message achieves cold.

**Volume discipline is not optional.** 10-20 new contacts per day per number, text varied
between contacts, spaced out. WhatsApp blocks aggressively on bulk-identical sends, and the
number is harder to replace than a sending domain.

Two rules complete the picture (checked 2026-09-09). Run from a **business profile, never
a personal number** — a personal number is both a platform-policy problem and a trust
problem. And messages are **human-timed, never automated blasts**: the opt-in expectation
is higher than for email, so the email or LinkedIn touch lands consent first, and the
volume discipline above is a floor, not a license.

The lawful basis does not change when the channel does: **Saudi PDPL consent applies
here too** (section 7).

This family treats WhatsApp as its least-developed channel: everything above is an
operating floor, not a complete playbook. Full orchestration context lives in
multichannel-orchestration.md.

## 7. Saudi PDPL Changes the Consent Math

The PDPL (Saudi Arabia's Personal Data Protection Law) has been fully enforced since
September 14, 2024 and is actively enforced by SDAIA as of February 2026 (checked
2026-09-09). Fines run up to SAR 5M and are doubled for repeat offenses.

The part that matters for outbound: **marketing email requires consent.** There is no
ePrivacy-style customer exception that keeps cold outreach legal by default.

Practical consequence: cold outreach into KSA needs an opt-in basis or documented
legitimate interest reviewed by counsel. **This skill flags the requirement; it never
asserts your basis is lawful.** Route the decision through compliance-gates.md before the
list build.

Status across the wider region (checked 2026-09-09):

| Market | Status |
|---|---|
| Saudi Arabia | PDPL fully enforced since Sep 14, 2024; actively enforced by SDAIA |
| UAE | Federal PDPL in force since January 2022, but Executive Regulations remain unpublished — enforcement posture is murky |
| Egypt | NOT VERIFIED as of 2026-09-09; do not assume either way — get a local read before sizing an Egypt track |

Sources (checked 2026-09-09):

- https://cms.law/en/int/expert-guides/cms-expert-guide-to-data-protection-and-cyber-security-laws/saudi-arabia
- https://www.dlapiperdataprotection.com/?c=SA
- UAE: https://www.dlapiperdataprotection.com/?c=AE&t=law

## 8. Tools Do Not Rescue Fundamentals

Stated plainly in the source, and worth repeating because tooling is the most common thing
teams reach for first: no amount of Clay, Smartlead, or automation fixes a weak offer, bad
copy, or wrong targeting. Get the offer right before buying the stack.

## 9. Localization Is Not Translation

Translating an English sequence into Arabic is not localization. Localization means
knowing:

- When the holidays fall and what they do to response rates
- What local business culture expects in a first approach
- What reads as disrespectful
- Which channels are acceptable for a stranger to use

A fluent Arabic email that ignores Ramadan timing and opens with a Western-style hard CTA
is worse than a plain English one.

## 10. What Actually Works Here — Tooling Specifics

Western defaults fail quietly in this market. These are the substitutions that matter.

| Job | In MENA use | Why |
|---|---|---|
| **Email enrichment** | **Findymail and LeadMagic first** | Consistently the strongest hit rates on Middle East contacts. Providers tuned on US/EU data underperform here, and a waterfall ordered by Western benchmarks wastes its cheap steps |
| **Translating names to Latin script** | **Google Translate, not an LLM** | LLMs collapse distinct Arabic names that differ by one letter — ألاء and علاء become the same string. A merge tag rendering the wrong name is worse than no personalization |
| **Saudi local business** | `maroof.sa` | The Saudi business register. Not covered by Apollo or Sales Navigator |
| **Saudi e-commerce** | Store Leads for Zid and Salla | See section 5 |

### Finding people by nationality, when no filter exists

Neither LinkedIn nor Apollo can filter on nationality. **University is the workable proxy:**
filter on graduates of Cairo University, AUC, GUC or Alexandria University to reach
Egyptians working in the Gulf. This is a large, real segment — an expatriate-focused real
estate campaign built this way reached tens of thousands of qualifying profiles.

Use it for genuine segment relevance — shared language, shared context, a product that
actually fits expatriate buyers. **Do not use it as a proxy for anything a filter on
nationality would be improper for.** The line is whether the inference is about a business
need or about the person; see the appropriateness boundary in `personalization-depth.md`.

### Language: decide per contact, and Sales Navigator can tell you

Sales Navigator carries a **profile language filter**. In markets where the working
population is genuinely multilingual — Saudi and the UAE both are — this is the cheapest
way to split an Arabic list from an English one before writing a word.

**Arabic sequences return a higher positive-reply share** than English ones into the same
segment, and the gap is widest in heavily Saudized functions such as HR. Segment on the
signal rather than assuming from country.

## Checklist for a MENA Campaign

- [ ] Multi-source list build; single-source rejected on coverage grounds
- [ ] Raw scrape sized well above Western defaults
- [ ] Sending schedule set to Sunday–Thursday
- [ ] Ramadan and Eid windows excluded or de-prioritised
- [ ] List split by Profile Language into Arabic and English tracks
- [ ] UAE and Saudi treated as separate segments, not one Gulf bucket
- [ ] Zid and Salla used as sources if targeting Saudi ecommerce
- [ ] WhatsApp considered as a channel
- [ ] KSA consent basis decided — opt-in or counsel-reviewed legitimate interest (section 7)
- [ ] Sales cycle assumption lengthened in the economics model
