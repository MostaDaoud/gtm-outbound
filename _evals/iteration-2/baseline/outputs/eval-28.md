**Prompt:** "My reply rate is 2%. I rewrote the whole email and it went to 2.3%. What should I change next?"

A few things before you touch the copy again.

**1. Rewriting the whole email tells you almost nothing**

An email breaks down into separable blocks: **subject line, opening hook, value proposition, credibility/proof, and CTA.** When you rewrite all five at once and the number moves from 2% to 2.3%, you have no idea *which* of those five changes caused the movement — or whether any of them individually helped while another one hurt, netting out to a small overall gain. That's the core problem with whole-email rewrites as a testing method: you learn "something changed," not "this works." Going forward, change one block at a time (subject only, or CTA only, or the hook only) so each test result is attributable to something specific you can keep or scale.

**2. 2% → 2.3% is very likely noise, not a real lift**

Before reading anything into that 0.3-point move, run the numbers. On typical cold-email volumes, a jump from 2.0% to 2.3% needs a fairly large sample per variant to be distinguishable from random variation — with anything under a few thousand sends per version, that gap is well within the range you'd see from chance alone even with zero real difference between the emails. Rule of thumb: don't act on anything under roughly a 1000+ send sample per arm without running an actual significance check (two-proportion z-test or equivalent) — eyeballing percentage-point differences at this scale is a common way to chase noise and "optimize" your way into a worse email.

**3. Check upstream of copy before assuming copy is the constraint**

At a 2% reply rate, copy is not necessarily your bottleneck. Before doing more copy iteration, verify:
- **Deliverability/placement** — are these emails landing in the inbox, or spam/promotions? A domain reputation or SPF/DKIM/DMARC issue, or too-aggressive sending volume/warmup, can cap reply rate regardless of how good the copy is. Check actual inbox placement, not just "sent" and bounce rate.
- **List quality/fit** — are you emailing the right ICP, right title, right company size/stage? A perfectly written email to the wrong person still gets ignored. Check open rate, and if you can, segment reply rate by list source/segment to see if certain segments are dragging the average down.
- **Volume and sender health** — new domain/mailbox warmup status, sending too many per day per inbox, etc.

Only once placement and list are confirmed solid should you treat copy as the lever worth pulling — and even then, one block at a time, with a real significance check before declaring a winner.

**Suggested next steps in order:**
1. Confirm inbox placement and check for any deliverability red flags.
2. Segment current results by list/ICP to rule out a targeting mismatch.
3. If both check out, go back to block-level testing — pick one block (I'd start with subject line or CTA, since those tend to move reply rate the most), test only that, and don't call a winner until the sample size supports statistical significance.
