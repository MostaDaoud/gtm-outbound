# Task 12 Response

Hold off — I wouldn't scale this yet. The difference is not statistically significant at your current sample size.

## The numbers

- Variant A: 40/800 = 5.0% positive reply rate
- Variant B: 52/800 = 6.5% positive reply rate
- Observed lift: +1.5 percentage points (a 30% relative lift, which sounds big, but the sample is thin)

Running a two-proportion z-test:
- z = 1.29
- two-sided p-value ≈ 0.20
- 95% confidence interval on the difference: **-0.78 to +3.78 percentage points**

That confidence interval crosses zero — meaning the data is consistent with B actually being *worse* than A, not just better. At a standard 95% confidence threshold, you'd normally want p < 0.05 before calling a winner; you're at p ≈ 0.20, nowhere close.

## What this means in practice

With 800 sends per variant and single-digit-percent response rates, you simply don't have enough volume yet to distinguish a 5% rate from a 6.5% rate with confidence. A 1.5pp gap on a ~5% baseline needs a lot more data to separate from noise — realistically you'd want somewhere in the range of 3,000-6,000 sends per variant to detect an effect this size reliably (depends on the true effect size and how much power you want, but 800 is well short).

## What I'd do instead

1. **Don't scale on this result.** If you commit budget/domains/reputation to "B" now and it turns out to be noise (or worse, actually equal to or below A), you've made a real decision on a coin flip.
2. **Keep both variants running** until you hit a sample size that gives you real power — or at minimum, don't declare a winner until the confidence interval stops crossing zero.
3. **Watch for the peeking problem.** If you've been checking this test daily and B looked good today, there's a good chance you're stopping right when random variance happens to favor B. Pre-committing to a sample size (or using a sequential testing method) avoids this trap.
4. **Consider whether "positive reply" is even the right metric to optimize.** If you have booked-meeting or show-rate data downstream, that's a more decision-relevant number than positive replies — sometimes a variant that gets more replies gets fewer of them to actually book.

Bottom line: B is *ahead* directionally, and it's fine to keep leaning into it as you gather more data, but "B wins, scaling now" is a call you can't support statistically yet.
