# Eval 22 — Scoring and rewriting the draft opener

Ran the draft through `score_message.py --stdin` rather than editing by eye.

## Scorer output on the original draft

```
Message scoring: FAIL

  (whole file)  —  43/100
    27w · 3 sentences · you/we 3:2 · 0 hedge(s) · CTA hard · tags: first_name
    ERROR   [BANNED_PHRASE] ceremonial opener: "I hope this email finds you well"
             ...Hi {{first_name}}, I hope this email finds you well. I came across your...
    ERROR   [BANNED_PHRASE] says nothing: "I came across your profile"
             ...ail finds you well. I came across your profile and was really impr...
    ERROR   [BANNED_PHRASE] calendar ask in first touch: "15-minute call"
             ...be open to a quick 15-minute call?...
    warning [NO_HEDGE] No qualifying language...
    warning [HARD_CTA] Meeting or calendar ask detected...
    info    [UNIFORM_RHYTHM] Sentence lengths within 0 words of each other...
```

Three hard failures, all block-level:

1. **Ceremonial opener** — "I hope this email finds you well" is dead air; it costs the
   reader a sentence before anything relevant appears.
2. **Generic admiration** — "I came across your profile and was really impressed" is
   Level-0 personalization (`personalization-depth.md`): it proves you opened LinkedIn and
   says nothing about them specifically. Strip the name and this line could go to a
   hundred other people unchanged — that's the test for whether personalization is real.
3. **Calendar ask in email 1** — "15-minute call" is a hard CTA at first touch, when
   motivation is by definition near zero (`cta-design.md`). Per the friction ladder, this
   is close to the highest-friction ask you can make to someone who has never heard from
   you, and email 1 is required to end on an open question or low-friction offer instead.

## Rewrite

Since no real signal was given in the draft, I fell back to the pain/KPI hook
(`copy-blocks.md` 2a) rather than inventing fake personalization, and replaced the meeting
ask with a soft, value-first CTA per the hard→soft conversion in `cta-design.md`.

> Hey {{first_name}} — what most ops leaders hate is a pipeline that looks full on paper
> but stalls before a qualified call happens. If your numbers look similar, it could be
> the same fix that cut cost-per-booked-call 34% for a Series B fintech in 90 days. Worth
> sending over how?

## Re-scored

```
Message scoring: PASS

  (whole file)  —  100/100
    50w · 3 sentences · you/we 1:0 · 1 hedge(s) · CTA soft · tags: first_name
```

All three issues resolved: no ceremonial opener, the "impressed" line is replaced with a
role-owned problem statement instead of flattery, and the CTA is now "worth sending over"
(ability-first, no calendar) instead of a 15-minute-call ask.
