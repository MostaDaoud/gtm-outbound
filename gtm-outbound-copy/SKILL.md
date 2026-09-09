---
name: gtm-outbound-copy
description: >
  Writes low-friction, high-relevance cold email and LinkedIn sequences using the "Poke
  the Bear" framework — an observation about the prospect leading into an open-ended
  pain question, with no pitch in the first message. Keeps every message under 80 words,
  embeds validated spintax across greetings, body and CTAs, builds soft-CTA and hard-CTA
  test arms, and produces the Smartlead sending, warmup and domain configuration. Every
  merge tag is validated against the Clay schema before output. Use when the user says
  "draft a Poke the Bear copy sequence", "write the outbound emails", "cold email
  sequence", "spintax", "email variations", "set up a Smartlead deliverability spec",
  "warmup settings", "subject lines", or "LinkedIn message sequence".
argument-hint: "[path to clay-table.json or a campaign description]"

---
<!-- fable-discipline-gate:v1 -->

## Pre-flight gate: Fable Discipline (run FIRST)

Before executing any instruction below, adopt the Fable Mindset operating manual at
`C:\Users\mosta\.claude\skills\fable-mindset\SKILL.md`. Apply its Decision Loop
(GROUND -> REASON -> ACT -> OBSERVE -> RE-EVALUATE -> VERIFY -> NARRATE) and its
7 execution rules to every step of this skill. FD runs first; this skill's own
instructions begin only after the discipline is adopted.
# GTM Outbound — Spintax Copy & Deliverability

The execution layer. Two jobs: write messages that earn a reply, and configure sending
so they arrive in the primary inbox.

## Inputs

Read from the working directory if present: `icp.json` for sub-niche and UVP variants,
`allowed_vars.json` or `clay-table.json` for the merge variables that actually exist.

If neither exists, write the copy anyway, but mark every merge tag as unvalidated in the
output and say plainly that the tags cannot be checked against a real schema. Do not
silently emit unverifiable tags — that is exactly the failure this stage exists to catch.

## Step 1 — Write Email 1

Load `references/copy-frameworks.md`. It carries the five blocks, the five structures, and
the spintax rules.

**Treat the email as five blocks**, each with its own job and each independently testable:
subject, hook, value proposition, credibility, CTA. Rewriting the whole email tells you
nothing about which change moved the number — hold four constant and vary one.

**Pick the structure from what you can credibly lead with.** Poke the Bear is the default
and the only one of the five that does not end in an ask, which is why it suits a first
touch. If there is no observable signal for this prospect, do not manufacture one — drop
to Question → Value → Ask and carry the message on segment relevance. A fabricated
observation is the most recognisable tell in cold email.

Poke the Bear, in order:

1. **Observation** — specific and verifiable about *them*, from a research variable. Not
   their industry. Not "I saw your website."
2. **Bridge** — one clause connecting the observation to a plausible problem.
3. **Open question** — about the problem, ending the email.

That is the whole email. No pitch, no company description, no feature list, no calendar
link, no "quick 15 minutes", no "I help X do Y" opener, no compliment as an opener.

The mechanism: a question about a real problem is cheap to answer, and a pitch is expensive
to refuse. **The first reply is the goal, not the meeting.**

**Hard limit: 80 words in the longest spintax variant** — not the shortest, not the one
written first. The validator computes the worst case.

### Relevance before personalization

Speaking the recipient's functional vocabulary beats shallow personalization, and shallow
personalization is worse than none because it advertises that a line was generated to fill
a slot. Two tests, both in the reference: if this went to a thousand people would it carry
the same meaning, and does the email still make sense with the personalized opening
removed? When personalization at volume would be thin, build segmented lists with a
narrative per function instead.

### Separate what you know from what you are guessing

Load `references/personalization-depth.md`. Before writing the observation, record the
verified fact with its source and date, the inference it supports, the hypothesis that
follows, your confidence, and the innocent alternative explanation. "They are hiring
salespeople" does not prove a messaging problem. Stating a hypothesis as fact claims
knowledge you do not have, and a recipient who knows better stops reading.

**One hedge per message** — "it looks like", "I may be wrong, but", "teams at that stage
often" — not one per sentence. `score_message.py` flags three or more.

That reference also carries the appropriateness boundary. Public availability is not
permission: if the recipient would have to wonder how you found something, or it touches
family, health, location, or private activity, do not use it however findable it is.

## Step 2 — Embed Spintax

Confirm the platform first. Smartlead overloads one delimiter — `{{first_name}}` is a merge
tag and `{{Hey|Hi}}` is spintax, with a pipe the only difference. Instantly separates them.
Pass `--dialect` to the validator to match.

Spin the greeting, the observation phrasing, the bridge, the CTA, and the sign-off — full
table and rules in `references/copy-frameworks.md`. **Vary structure, not synonyms**, never
nest, and keep total variants under a few thousand per message or you cannot read what
ships.

**2026 reframe — mechanical spintax is now a footprint.** ESPs and buyers pattern-match
template-family text, and statistically-similar AI copy is the named cause of the recent
reply-rate decline. Prefer N genuinely distinct human-written variants over one draft
mechanically spun, and rotate at least five distinct subject lines. The validator stays:
its worst-case word count is the guard, not an endorsement of heavy spintax. The reframe
and its evidence live in `references/copy-frameworks.md`.

For the CTA specifically, load `references/cta-design.md`. Reply is
motivation × ability × prompt, and at first touch motivation is low by definition — the
only lever you control is making the ask trivially easy.

## Step 3 — Build the CTA Test Arms

Write the sequence twice at the CTA only, holding everything else constant:

- **Soft CTA** — "Worth a look?" / "Is that on your radar?" / open question, no ask.
- **Hard CTA** — a direct, specific, time-bound ask.

Soft CTAs generally lift raw reply rate; hard CTAs generally lift meeting rate from a
lower reply base. Which wins depends on ACV and sales capacity, and it is genuinely not
predictable in advance — which is the point of testing it rather than asserting it.

Size the test before running it, so the result can mean something:

```bash
python scripts/gtm_math.py ab --baseline-rate 5 --min-detectable-lift 30 --sends-per-day 240
```

## Step 4 — The Follow-Up Cadence

Three or four steps total, on the same thread. Each follow-up must add something — a new
angle, a specific proof point, a different problem. A follow-up whose content is "just
bumping this" teaches the recipient to ignore the thread.

Follow-ups earn disproportionate replies — roughly 42% of all replies and a large share
of positive ones arrive after step 1 — yet they get a fraction of the drafting care email
1 receives. `references/copy-frameworks.md` carries a follow-up section with three named
patterns (Surrender, Presumptive Negative, last-email close) and the sequence-structure
data. Draft follow-ups with the same block discipline as email 1.

The final message closes the loop cleanly and stops. No fifth attempt, no guilt, no
"I'll assume you're not interested" framing.

For the LinkedIn track: connection request with no note, then a message after acceptance
that mirrors the email observation without repeating it verbatim. Running identical text
on both channels reads as automation, because it is.

**For a phone track, load `references/cold-call.md`.** Calling is a second signal on the
same account, not a separate campaign — it works best placed a few days after email 1 so
the name has already appeared once. The opener is four moves: name yourself, state the
reason for the call, offer the hypothesis qualified, then ask for thirty seconds rather
than a meeting.

**For full multichannel orchestration** — video touches, WhatsApp (GCC), conditional
branching between channels, signal-triggered timing, and the Agoge-style cadence
skeleton — load `references/multichannel-orchestration.md`. This step's default is
email-first with a phone and LinkedIn track; that reference owns the orchestration layer
above it.

**If `icp.json` contains a `buying_committee` map, write one track per role.** Load
`references/buying-committee.md`. The observation can stay constant across roles; the
bridge and the question must not. Stagger the threads 5-8 days — the same message
landing on three people at one company in one week reads as a blast and burns the
account.

## Step 5 — Validate Before Output

This is a gate, not a suggestion. Do not present copy that has not passed:

```bash
python scripts/validate_spintax.py SEQUENCE.md --vars allowed_vars.json --max-words 80
```

```bash
python scripts/score_message.py SEQUENCE.md --vars allowed_vars.json --max-words 80
```

The two check different things and both are gates. `validate_spintax.py` checks the
sequence is **syntactically sound** — braces balanced, tags resolvable, worst-case word
count. `score_message.py` checks it is **any good** — banned openers, recipient focus,
hedging discipline, CTA friction, specificity.

A message can pass the first while opening "I hope this finds you well" and asking for
fifteen minutes. It expands spintax before checking, so a banned phrase hidden inside a
spin block is still caught.

Any error-severity finding fails the message regardless of score. Fix every error and
re-run. Report remaining warnings with your reasoning rather than silently accepting them.

## Step 6 — Smartlead Configuration

Load `references/deliverability.md` from the parent skill for the full spec and the
reasoning behind each number.

Default sending profile:

| Setting | Default | Why |
|---|---|---|
| Sends per inbox per day | 15-25 | Per-inbox figure; the binding constraint is per-domain — see below |
| Warmup duration before sending | 14 days minimum | Shorter warmup does not establish history |
| Warmup emails per day | 40 | Sustained, well above the send volume |
| Ramp-up increment | 5 per day | Gradual enough not to look like a spike |
| Warmup reply rate | 30-40% | High enough to signal engagement, not so high it patterns |
| Randomized warmup | On | Fixed intervals are a detectable signature |

**The per-domain ceiling is the number that actually binds:** roughly 40 sends/day per
domain across all its mailboxes (reported working band 30-50; reputation is scored at the
domain level). Three mailboxes at 25/day each put 75/day on one domain — double the
ceiling while every mailbox looks safe. `gtm_math.py size` sizes domains from daily
volume, and `diagnose_campaign.py` flags violations after launch. Warmup is also now
risk-bearing, not free — warmup networks are an enforcement target, so load the warmup
caveats in `references/deliverability.md` rather than assuming 2022-era mechanics.

These are defaults from a working playbook, not platform limits. State them as a
starting configuration and note that they should move with observed inbox placement.

Also specify: a separate sending domain from the primary company domain, SPF, DKIM and
DMARC on every sending domain, roughly three mailboxes per domain, and custom tracking
domains. Leave open tracking off — the pixel costs more in placement than the open rate
is worth, and open data has been unreliable since Apple Mail Privacy Protection.

## Outputs

- `SEQUENCE.md` from `assets/templates/sequence.md` — all steps, both CTA arms, spintax
  inline, validator output included.
- `smartlead-config.json` — sending, warmup, and domain configuration.

## Compliance Note

Include a real physical address and a working opt-out in the sending configuration. Where
recipients are in the EU or Canada, flag that GDPR legitimate interest and CASL impose
requirements beyond CAN-SPAM, and recommend the user confirm their basis rather than
asserting that the setup is compliant. The jurisdiction gate itself — geography, consent
model, required artifacts — belongs to the list stage and lives in
`references/compliance-gates.md`; if it has not run, stop and route back before
configuring a send.
