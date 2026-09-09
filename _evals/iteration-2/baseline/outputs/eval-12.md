**Prompt:** "variant B got 52 positive replies out of 800 sends, variant A got 40 out of 800. B wins right? scaling it now"

Not yet — hold off on scaling B. That result isn't statistically significant, even though it looks like a clear win at first glance.

**The numbers**

- Variant A: 40/800 = 5.0%
- Variant B: 52/800 = 6.5%
- Absolute lift: 1.5 points (a 30% relative lift, which is what makes it *look* exciting)

Running a two-proportion significance test on this:
- Pooled conversion rate: 92/1600 = 5.75%
- Standard error: ~1.16%
- Z-score: ~1.29
- Two-tailed p-value: ~0.20

A z-score of 1.29 is well short of the ~1.96 threshold you'd want for a conventional 95% confidence level (p < 0.05). A p-value of ~0.20 means there's roughly a 1-in-5 chance you'd see a gap this size (or larger) between two variants that are actually performing identically, just from random noise in an 800-person sample. That's not a foundation to commit budget/volume to.

**What sample size would actually settle it**

To reliably detect a real difference between a 5.0% and a 6.5% reply rate (80% power, 95% confidence — the standard bar for "confident enough to act"), you'd need roughly **3,800 sends per variant (about 7,600 total)** — nearly 5x what you've currently run. If the true lift is smaller than 1.5 points, you'd need even more; if it's larger, less.

**What I'd do instead of scaling now**

1. Keep running both variants at the current split rather than committing sends to B.
2. Re-check significance at your next natural checkpoint (e.g., every additional 800-1000 sends per arm) rather than continuously peeking, which inflates false-positive risk.
3. Only declare a winner and shift volume once you clear a real significance threshold with a sample size in the range above — or until the trend has held consistently across a couple of checkpoints, which is a decent informal signal even before you hit the "textbook" sample size.

Rough guide for how much lift you'd need to see at your *current* 800-per-arm sample to already be significant: it would take closer to a 9-10 point absolute gap (e.g., 5% vs ~14%+) at n=800 for a swing that large to clear significance — anything more modest than that, like the current 1.5-point gap, needs a bigger sample before you can trust it.
