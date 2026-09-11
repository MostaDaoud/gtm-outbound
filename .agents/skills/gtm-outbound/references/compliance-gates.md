# Compliance Gates

Three places in this family require compliance behavior (the orchestrator's scope
boundary, the score skill's category 5, the deliverability jurisdiction table) and none
of them owned the procedure. This file does. Run the gate at **list-build time**, not
send time — a jurisdiction discovered after warmup is a sunk domain, not a legal defense.

The skill flags obligations and documents a basis; it never asserts that a specific
campaign is compliant. Counsel confirms. That line is not hedging — the fines below are
real, and none of them were issued against a framework.

*All legal claims checked 2026-09-09. Statutes move; re-verify before any non-domestic
campaign.*

## The Gate

Three questions, in order, before a single contact is sourced:

1. **Geography.** Where do the *recipients* sit — not where the sender sits. A UK sender
   mailing German contacts is a German compliance question.
2. **Consent model.** What does that jurisdiction require for cold B2B outreach —
   opt-out, consent, or documented legitimate interest?
3. **Required artifacts.** What must exist in writing *before* the first send.

| Jurisdiction | Consent model for B2B cold email | Max exposure | Notes |
|---|---|---|---|
| US (CAN-SPAM) | Opt-out regime; B2B treated same as B2C | $53,088 per email (single-source figure) | Physical postal address required; no prior-relationship exemption |
| Canada (CASL) | Consent regime | CAD 10M per violation; CRTC signaling heightened expectations 2026 | Applies cross-border to messages *accessed* in Canada — origin is not the test |
| Germany | Double opt-in, even B2B (UWG) | GDPR + UWG fines | Strictest EU market; treat "documented legitimate interest" as unavailable |
| Italy | Consent-leaning; active enforcement | €1M+ cold-email fines recorded | Second-strictest EU market |
| FR / NL / IE / SE / UK | Documented legitimate interest accepted | GDPR scale | Requires a documented LIA — see artifacts below |
| UK (PECR + UK GDPR) | Legitimate interest for B2B | £17.5M or 4% global turnover (Data (Use and Access) Act 2025, in force 5 Feb 2026) | Single source for the ceiling figure; Jan 2026 ICO fines £225k across two companies |
| Saudi Arabia (PDPL) | **Consent — no ePrivacy-style customer exception** | SAR 5M, doubled for repeat | Fully enforced since 14 Sep 2024; SDAIA actively enforcing as of Feb 2026 (high confidence — CMS, DLA Piper) |
| UAE | Federal PDPL in force Jan 2022; Executive Regulations unpublished | Unclear | Enforcement posture murky; treat as consent-leaning until regulations land |
| Egypt | **NOT VERIFIED as of 2026-09-09** | — | Run a dedicated legal check before any Egypt campaign; do not assume GCC neighbors' rules transfer |

GDPR enforcement context: marketing enforcement rose roughly 340% in Q1 2026 vs Q1 2023,
including a CNIL fine of €500k for outbound prospecting (July 2026). The trend line is
against volume cold outreach, not in favor of it.

## Required Artifacts

Exist in writing before first send. `score` checks for them; their absence is a hard
gate, not a deduction.

1. **Consent basis per jurisdiction** — one line per country in the ICP blueprint stating
   the model relied on and why.
2. **Documented LIA** (legitimate interest assessment) wherever legitimate interest is
   the model — what the interest is, why the processing is necessary, whether the
   recipient's interest overrides. Undocumented LIA is the difference between FR and DE
   treatment.
3. **Suppression process** — cross-campaign, cross-domain, with a named owner. See
   `suppression-mechanics.md`.
4. **Physical postal address** in the footer of every send.
5. **Working opt-out** — RFC 8058 one-click unsubscribe plus a monitored reply path; both
   must be tested on a received email, not assumed from ESP settings. Opt-outs processed
   within 2 days.
6. **Data-source records** — where each contact came from and when. A source that cannot
   be named cannot be defended.

## What the Operator Does vs What Counsel Does

The operator: identifies jurisdictions, picks the consent model, produces the artifacts,
flags residual risk in plain language ("KSA requires consent; this list is scraped —
that combination needs counsel before launch").

Counsel: asserts that a specific basis is valid for a specific campaign.

This skill produces the first list and recommends the second conversation. It does not
perform the second role, and no prompt phrasing makes it perform that role.
