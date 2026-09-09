#!/usr/bin/env python3
"""
Purpose: Deterministic GTM campaign arithmetic. Outbound planning fails in two
         directions -- building a list too small to hit the goal, or scaling a
         variant off a sample that never proved anything. Both are arithmetic
         problems, so they belong in code rather than in a language model.

Subcommands:
    size       Back-solve list size, send volume, inbox and domain count from a
               meetings goal and assumed funnel rates.
    economics  Cost per meeting, CAC, payback period, ROI.
    ab         Required sample size per arm before an A/B test can conclude anything.
    ab-eval    Whether an in-flight test has actually reached significance.

Output:  Human-readable table by default; --json for chaining into other steps.
         Exit 0 normally, exit 1 if a hard sanity check fails.

Usage:
    python gtm_math.py size --meetings-goal 10 --reply-rate 5 --positive-rate 25
    python gtm_math.py economics --acv 24000 --close-rate 20 --meetings 10 --inboxes 8
    python gtm_math.py ab --baseline-rate 5 --min-detectable-lift 30
    python gtm_math.py ab-eval --a-sends 2000 --a-conv 100 --b-sends 2000 --b-conv 130
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from statistics import NormalDist
from typing import Any

# Benchmarks used only to flag assumptions that would make a plan fictional.
# These are sanity rails, not targets -- override them as your own data lands.
PLAUSIBLE_REPLY_RATE_MAX = 15.0
PLAUSIBLE_POSITIVE_SHARE_MAX = 50.0
INBOX_COUNT_WARN = 50
MAILBOXES_PER_DOMAIN = 3
DEFAULT_SENDS_PER_INBOX_DAY = 25

# Reputation is scored substantially at the domain level. Three mailboxes each sending a
# "safe" 25 puts 75/day on one domain, well past the reported 30-50 working ceiling.
# Domains are therefore sized from the daily send volume, not from the mailbox count.
SENDS_PER_DOMAIN_DAY = 40


def pct(value: float) -> float:
    """Accept 5 or 0.05 for a percentage and normalize to a 0-1 fraction."""
    if value < 0:
        raise ValueError("Percentages cannot be negative")
    return value / 100.0 if value > 1 else value


class Sanity:
    """Collects non-fatal warnings and fatal errors during a calculation."""

    def __init__(self) -> None:
        self.warnings: list[str] = []
        self.errors: list[str] = []

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def fail(self, msg: str) -> None:
        self.errors.append(msg)

    def as_dict(self) -> dict[str, Any]:
        return {"warnings": self.warnings, "errors": self.errors}


def cmd_size(args: argparse.Namespace) -> dict[str, Any]:
    """
    Size the campaign from either end.

    Backward (--meetings-goal): how big a list does this goal require?
    Forward  (--prospects):     what does a list this size support?

    Both directions matter in practice -- planning runs backward, but a user who
    already has a list runs forward, and forcing that through a goal they have not
    set produces a made-up number.
    """
    s = Sanity()

    if args.meetings_goal is None and args.prospects is None:
        raise ValueError("Provide either --meetings-goal or --prospects.")
    if args.meetings_goal is not None and args.prospects is not None:
        raise ValueError("--meetings-goal and --prospects are mutually exclusive.")

    forward = args.prospects is not None

    if forward:
        if args.reply_rate is None:
            args.reply_rate = 4.0
            s.warn("No reply rate given; assumed 4% for cold B2B. Replace with your own.")
        if args.positive_rate is None:
            args.positive_rate = 25.0
            s.warn("No positive rate given; assumed 25% of replies. Replace with your own.")
    elif args.reply_rate is None or args.positive_rate is None:
        raise ValueError("--reply-rate and --positive-rate are required with --meetings-goal.")

    reply = pct(args.reply_rate)
    positive = pct(args.positive_rate)
    booking = pct(args.meeting_rate)
    bounce = pct(args.bounce_rate)
    verify_pass = pct(args.verify_pass_rate)

    if args.reply_rate > PLAUSIBLE_REPLY_RATE_MAX:
        s.warn(
            f"A {args.reply_rate}% reply rate is above the {PLAUSIBLE_REPLY_RATE_MAX}% "
            f"ceiling typical of genuinely cold outbound. If this came from a warm or "
            f"referral list the model holds; if it is an assumption, the plan is "
            f"optimistic and every number below inherits that."
        )
    if args.positive_rate > PLAUSIBLE_POSITIVE_SHARE_MAX:
        s.warn(
            f"{args.positive_rate}% of replies being positive is unusually high -- "
            f"most cold campaigns sit well below half, since replies include "
            f"unsubscribes and referrals out."
        )

    conversion = reply * positive * booking
    if conversion <= 0:
        s.fail("Funnel rates multiply to zero -- no list size can reach the goal.")
        return {"sanity": s.as_dict()}

    if forward:
        prospects = args.prospects
        meetings = prospects * conversion
        if meetings < 1:
            s.warn(
                f"A list this size yields {meetings:.2f} meetings per month at these "
                f"rates. Below one, most months return zero -- judge over a quarter."
            )
    else:
        meetings = args.meetings_goal
        prospects = math.ceil(args.meetings_goal / conversion)
    # Verification discards invalid addresses, so the raw scrape must be larger.
    raw_leads = math.ceil(prospects / verify_pass) if verify_pass > 0 else prospects
    sends = prospects * args.sequence_steps
    sends_per_day = math.ceil(sends / args.working_days)
    inboxes = math.ceil(sends_per_day / args.sends_per_inbox_day)
    # Size domains from daily volume, not from mailbox count. Dividing inboxes by
    # mailboxes-per-domain silently permits several times the domain-level ceiling.
    domains = max(
        math.ceil(sends_per_day / args.sends_per_domain_day),
        math.ceil(inboxes / MAILBOXES_PER_DOMAIN),
    )
    mailboxes_per_domain = inboxes / domains if domains else 0
    expected_bounces = round(prospects * bounce)

    if mailboxes_per_domain and args.sends_per_inbox_day * mailboxes_per_domain > args.sends_per_domain_day:
        s.warn(
            f"At {args.sends_per_inbox_day}/inbox across {mailboxes_per_domain:.1f} "
            f"mailboxes per domain, each domain carries "
            f"{args.sends_per_inbox_day * mailboxes_per_domain:.0f}/day against a "
            f"{args.sends_per_domain_day}/day ceiling. Lower the per-inbox rate or add "
            f"domains -- adding mailboxes to a domain splits its budget, it does not "
            f"raise it."
        )

    if inboxes > INBOX_COUNT_WARN:
        s.warn(
            f"{inboxes} inboxes is a substantial infrastructure footprint to warm and "
            f"monitor. Improving reply rate or ACV is usually cheaper than adding "
            f"sending capacity at this scale."
        )
    if args.bounce_rate > 3:
        s.warn(
            f"A {args.bounce_rate}% assumed bounce rate exceeds the 3% danger threshold "
            f"where domains get pulled from rotation; 4% is the throttling line. Tighten "
            f"verification first."
        )
    if args.tam is not None:
        if raw_leads > args.tam:
            s.fail(
                f"This plan needs {raw_leads:,} raw leads but the stated TAM is only "
                f"{args.tam:,}. The goal cannot be reached against this ICP -- widen "
                f"the segment, raise reply rate, or lower the goal."
            )
        elif raw_leads > args.tam * 0.5:
            s.warn(
                f"This consumes {raw_leads / args.tam:.0%} of the stated TAM in a "
                f"single month. Burning half a market on one campaign leaves nothing "
                f"to iterate against."
            )

    return {
        "mode": "forward (from list size)" if forward else "backward (from meetings goal)",
        "goal": {
            "meetings_per_month": round(meetings, 2),
            "derived": forward,
        },
        "funnel": {
            "reply_rate": round(reply, 5),
            "positive_share_of_replies": round(positive, 5),
            "booking_rate": round(booking, 5),
            "prospect_to_meeting_rate": round(conversion, 6),
        },
        "list": {
            "prospects_needed": prospects,
            "raw_leads_to_scrape": raw_leads,
            "expected_bounces": expected_bounces,
        },
        "sending": {
            "sequence_steps": args.sequence_steps,
            "total_sends": sends,
            "sends_per_day": sends_per_day,
            "sends_per_inbox_day": args.sends_per_inbox_day,
            "inboxes_required": inboxes,
            "mailboxes_per_domain": round(mailboxes_per_domain, 1),
            "domains_required": domains,
            "working_days": args.working_days,
        },
        "sanity": s.as_dict(),
    }


def cmd_economics(args: argparse.Namespace) -> dict[str, Any]:
    """Cost per meeting, CAC, payback, ROI."""
    s = Sanity()

    close = pct(args.close_rate)
    margin = pct(args.gross_margin)

    infra = args.inboxes * args.cost_per_inbox_month
    data = args.leads * args.cost_per_lead
    monthly_cost = infra + data + args.tooling_month + args.labor_month

    customers = args.meetings * close
    cost_per_meeting = monthly_cost / args.meetings if args.meetings else float("inf")
    cac = monthly_cost / customers if customers else float("inf")

    gross_profit_per_customer = args.acv * margin
    if args.contract_months and args.contract_months > 0:
        monthly_gross_profit = gross_profit_per_customer / args.contract_months
        payback_months = (
            cac / monthly_gross_profit if monthly_gross_profit > 0 else float("inf")
        )
    else:
        monthly_gross_profit = gross_profit_per_customer
        payback_months = cac / monthly_gross_profit if monthly_gross_profit > 0 else float("inf")

    new_revenue = customers * args.acv
    roi = (new_revenue - monthly_cost) / monthly_cost if monthly_cost else float("inf")
    ltv_cac = gross_profit_per_customer / cac if cac not in (0, float("inf")) else float("inf")

    if customers < 1:
        s.warn(
            f"At these rates the campaign produces {customers:.2f} customers per month. "
            f"Below one, monthly averages hide the fact that most months return zero -- "
            f"judge this over a quarter, not a month."
        )
    if cac != float("inf") and cac > gross_profit_per_customer:
        s.fail(
            f"CAC ({cac:,.0f}) exceeds gross profit per customer "
            f"({gross_profit_per_customer:,.0f}). The campaign loses money on every "
            f"deal it wins."
        )
    if payback_months != float("inf") and payback_months > 12:
        s.warn(
            f"Payback of {payback_months:.1f} months exceeds a year. Outbound at this "
            f"payback needs financing, not just a bigger list."
        )
    if ltv_cac != float("inf") and ltv_cac < 3:
        s.warn(
            f"Gross-profit-to-CAC ratio is {ltv_cac:.1f}x. Below 3x the channel is "
            f"usually not worth scaling without fixing conversion or price first."
        )

    def clean(x: float) -> float | None:
        return None if x == float("inf") else round(x, 2)

    return {
        "costs": {
            "infrastructure": round(infra, 2),
            "data": round(data, 2),
            "tooling": round(args.tooling_month, 2),
            "labor": round(args.labor_month, 2),
            "total_monthly": round(monthly_cost, 2),
        },
        "outcomes": {
            "meetings": args.meetings,
            "close_rate": round(close, 4),
            "customers_per_month": round(customers, 2),
            "new_revenue_per_month": round(new_revenue, 2),
        },
        "unit_economics": {
            "cost_per_meeting": clean(cost_per_meeting),
            "cac": clean(cac),
            "gross_profit_per_customer": round(gross_profit_per_customer, 2),
            "payback_months": clean(payback_months),
            "roi_multiple": clean(roi),
            "gross_profit_to_cac": clean(ltv_cac),
        },
        "sanity": s.as_dict(),
    }


def cmd_ab(args: argparse.Namespace) -> dict[str, Any]:
    """Required sample size per arm for a two-proportion test."""
    s = Sanity()

    p1 = pct(args.baseline_rate)
    lift = pct(args.min_detectable_lift)
    p2 = p1 * (1 + lift)

    if p2 >= 1:
        s.fail("Baseline plus lift exceeds 100% -- check the inputs.")
        return {"sanity": s.as_dict()}

    alpha = 1 - pct(args.confidence)
    beta = 1 - pct(args.power)
    z_alpha = NormalDist().inv_cdf(1 - alpha / 2)
    z_beta = NormalDist().inv_cdf(1 - beta)

    pooled = (p1 + p2) / 2
    numerator = (
        z_alpha * math.sqrt(2 * pooled * (1 - pooled))
        + z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))
    ) ** 2
    n_per_arm = math.ceil(numerator / ((p2 - p1) ** 2))
    total = n_per_arm * 2

    days = None
    if args.sends_per_day:
        days = math.ceil(total / args.sends_per_day)
        if days > 60:
            s.warn(
                f"At {args.sends_per_day} sends/day this test takes {days} days to "
                f"conclude. Over that horizon seasonality and list decay contaminate "
                f"the comparison -- test a bigger swing instead of a subtle one."
            )

    if n_per_arm > 20000:
        s.warn(
            f"Detecting a {args.min_detectable_lift}% lift on a {args.baseline_rate}% "
            f"baseline needs {n_per_arm:,} per arm. Small lifts on small baselines are "
            f"effectively unmeasurable in outbound -- test bigger structural changes."
        )

    return {
        "test_design": {
            "baseline_rate": round(p1, 5),
            "target_rate": round(p2, 5),
            "min_detectable_lift": round(lift, 4),
            "confidence": round(pct(args.confidence), 4),
            "power": round(pct(args.power), 4),
        },
        "requirement": {
            "sample_per_arm": n_per_arm,
            "total_sample": total,
            "days_to_conclude": days,
        },
        "sanity": s.as_dict(),
    }


def cmd_ab_eval(args: argparse.Namespace) -> dict[str, Any]:
    """Two-proportion z-test on an in-flight experiment."""
    s = Sanity()

    if args.a_sends <= 0 or args.b_sends <= 0:
        s.fail("Both arms need a positive send count.")
        return {"sanity": s.as_dict()}
    if args.a_conv > args.a_sends or args.b_conv > args.b_sends:
        s.fail("Conversions cannot exceed sends.")
        return {"sanity": s.as_dict()}

    p1 = args.a_conv / args.a_sends
    p2 = args.b_conv / args.b_sends
    pooled = (args.a_conv + args.b_conv) / (args.a_sends + args.b_sends)
    se = math.sqrt(pooled * (1 - pooled) * (1 / args.a_sends + 1 / args.b_sends))

    if se == 0:
        s.fail("Zero standard error -- no conversions in either arm yet.")
        return {"sanity": s.as_dict()}

    z = (p2 - p1) / se
    p_value = 2 * (1 - NormalDist().cdf(abs(z)))
    alpha = 1 - pct(args.confidence)
    significant = p_value < alpha

    observed_lift = (p2 - p1) / p1 if p1 > 0 else float("inf")

    if not significant:
        s.warn(
            f"p = {p_value:.4f} does not clear the {alpha:.2f} threshold. The "
            f"{observed_lift:+.1%} difference is within what random variation produces "
            f"at this sample size. Do not scale the winner yet."
        )
    if min(args.a_conv, args.b_conv) < 5:
        s.warn(
            "One arm has fewer than 5 conversions. The normal approximation behind "
            "this test is unreliable that low, so treat the p-value as indicative only."
        )

    return {
        "arms": {
            "a": {"sends": args.a_sends, "conversions": args.a_conv, "rate": round(p1, 5)},
            "b": {"sends": args.b_sends, "conversions": args.b_conv, "rate": round(p2, 5)},
        },
        "result": {
            "observed_lift": round(observed_lift, 4) if observed_lift != float("inf") else None,
            "z_score": round(z, 4),
            "p_value": round(p_value, 6),
            "confidence": round(pct(args.confidence), 4),
            "significant": significant,
            "verdict": (
                f"Arm {'B' if p2 > p1 else 'A'} wins -- safe to scale"
                if significant
                else "Inconclusive -- keep running or accept no difference"
            ),
        },
        "sanity": s.as_dict(),
    }


def render(result: dict[str, Any], title: str) -> str:
    lines = [title, "=" * len(title), ""]

    def walk(obj: dict[str, Any], indent: int = 0) -> None:
        for key, value in obj.items():
            if key == "sanity":
                continue
            label = key.replace("_", " ")
            if isinstance(value, dict):
                lines.append(f"{' ' * indent}{label}:")
                walk(value, indent + 2)
            else:
                if value is None:
                    shown = "n/a"
                elif isinstance(value, bool):
                    shown = "yes" if value else "no"
                elif isinstance(value, float):
                    shown = f"{value:,.4f}".rstrip("0").rstrip(".")
                elif isinstance(value, int):
                    shown = f"{value:,}"
                else:
                    shown = str(value)
                lines.append(f"{' ' * indent}{label:<34} {shown}")

    walk(result)

    sanity = result.get("sanity", {})
    for err in sanity.get("errors", []):
        lines.append("")
        lines.append(f"BLOCKER  {err}")
    for warn in sanity.get("warnings", []):
        lines.append("")
        lines.append(f"warning  {warn}")

    return "\n".join(lines)


def add_json_flag(p: argparse.ArgumentParser) -> None:
    """
    Accept --json on the subcommand as well as before it.

    argparse binds top-level options only ahead of the subcommand, so
    `gtm_math.py size --json` would otherwise be rejected -- which is exactly where
    people type it. SUPPRESS stops an absent subcommand flag from overwriting a
    top-level one.
    """
    p.add_argument("--json", action="store_true", default=argparse.SUPPRESS,
                   help="Emit JSON")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Deterministic GTM outbound math.")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("size", help="Size a campaign from a goal or from a known list")
    p.add_argument("--meetings-goal", type=float, help="Meetings per month (backward mode)")
    p.add_argument("--prospects", type=int, help="Known list size (forward mode)")
    p.add_argument("--reply-rate", type=float, help="%% of prospects who reply")
    p.add_argument("--positive-rate", type=float, help="%% of replies that are positive")
    p.add_argument("--meeting-rate", type=float, default=60, help="%% of positives that book (default 60)")
    p.add_argument("--sequence-steps", type=int, default=4, help="Emails per prospect (default 4)")
    p.add_argument("--sends-per-inbox-day", type=int, default=DEFAULT_SENDS_PER_INBOX_DAY)
    p.add_argument("--sends-per-domain-day", type=int, default=SENDS_PER_DOMAIN_DAY,
                   help="Daily ceiling per sending domain (default 40)")
    p.add_argument("--working-days", type=int, default=22)
    p.add_argument("--bounce-rate", type=float, default=3, help="Expected bounce %% (default 3 -- deliberately conservative; the family target is under 2, 3 is the pull-domain line)")
    p.add_argument("--verify-pass-rate", type=float, default=70, help="%% of scraped leads surviving verification (default 70)")
    p.add_argument("--tam", type=int, help="Total addressable contacts, for a reality check")
    add_json_flag(p)
    p.set_defaults(func=cmd_size, title="Campaign Sizing")

    p = sub.add_parser("economics", help="CAC, payback, ROI")
    p.add_argument("--acv", type=float, required=True, help="Annual contract value")
    p.add_argument("--meetings", type=float, required=True, help="Meetings per month")
    p.add_argument("--close-rate", type=float, required=True, help="%% of meetings that close")
    p.add_argument("--gross-margin", type=float, default=80, help="Gross margin %% (default 80)")
    p.add_argument("--contract-months", type=int, default=12, help="Contract length (default 12)")
    p.add_argument("--inboxes", type=int, default=0)
    p.add_argument("--cost-per-inbox-month", type=float, default=3.0)
    p.add_argument("--leads", type=int, default=0)
    p.add_argument("--cost-per-lead", type=float, default=0.10)
    p.add_argument("--tooling-month", type=float, default=0.0)
    p.add_argument("--labor-month", type=float, default=0.0)
    add_json_flag(p)
    p.set_defaults(func=cmd_economics, title="Campaign Economics")

    p = sub.add_parser("ab", help="Required sample size per arm")
    p.add_argument("--baseline-rate", type=float, required=True, help="Current rate %%")
    p.add_argument("--min-detectable-lift", type=float, required=True, help="Relative lift %% to detect")
    p.add_argument("--confidence", type=float, default=95)
    p.add_argument("--power", type=float, default=80)
    p.add_argument("--sends-per-day", type=int, help="To estimate days to conclude")
    add_json_flag(p)
    p.set_defaults(func=cmd_ab, title="A/B Sample Size")

    p = sub.add_parser("ab-eval", help="Significance of a running test")
    p.add_argument("--a-sends", type=int, required=True)
    p.add_argument("--a-conv", type=int, required=True)
    p.add_argument("--b-sends", type=int, required=True)
    p.add_argument("--b-conv", type=int, required=True)
    p.add_argument("--confidence", type=float, default=95)
    add_json_flag(p)
    p.set_defaults(func=cmd_ab_eval, title="A/B Significance")

    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        result = args.func(args)
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2

    print(json.dumps(result, indent=2) if args.json else render(result, args.title))
    return 1 if result.get("sanity", {}).get("errors") else 0


if __name__ == "__main__":
    sys.exit(main())
