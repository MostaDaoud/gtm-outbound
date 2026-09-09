#!/usr/bin/env python3
"""
Purpose: Diagnose a live outbound campaign from an ESP export and route the fix to the
         correct layer.

         The ordering is the entire point. Operators reach for a copy rewrite by
         default, because copy is the visible part. But a campaign with 6% bounce or
         one dead inbox produces the same symptom -- replies fell off -- and rewriting
         the copy cannot fix either. This tool checks the layers in the order that the
         causes actually stack, and refuses to advance to the next layer while an
         earlier one is broken.

         Layer order: infrastructure -> list -> offer -> copy.

Input:   CSV export from Smartlead, Instantly, or any tool that reports per-row sends,
         bounces, replies. Column names are matched flexibly (see COLUMN_ALIASES).

Output:  Ranked diagnosis with the responsible layer, evidence, and an explicit
         "do not do this yet" list. --json for machine consumption.

Usage:
    python diagnose_campaign.py export.csv
    python diagnose_campaign.py export.csv --group-by inbox --json
    python diagnose_campaign.py export.csv --baseline-reply-rate 5
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Thresholds. These are the same lines used in references/deliverability.md -- if you
# change one, change both. Bounce ladder: under 2% healthy, over 2% elevated, over 3%
# danger (pull the domain from rotation), over 4% throttling.
BOUNCE_CRITICAL = 0.04
BOUNCE_DANGER = 0.03
BOUNCE_WARN = 0.02
COMPLAINT_CRITICAL = 0.003
COMPLAINT_WARN = 0.001
REPLY_FLOOR = 0.01
POSITIVE_SHARE_FLOOR = 0.15
POSITIVE_SHARE_TARGET = 0.20  # practitioner benchmark: aim 20-30% of replies positive
INBOX_OUTLIER_RATIO = 0.4  # an inbox below 40% of median reply rate is suspect

# Reputation is scored substantially at the DOMAIN level, so three "safe" 25/day inboxes
# put 75/day on one domain. Reported working ceiling is 30-50. This is the constraint
# that actually binds, and nothing in an ESP warns you about it.
SENDS_PER_DOMAIN_DAY_CEILING = 50
SENDS_PER_DOMAIN_DAY_TARGET = 40

# LinkedIn runs on a different funnel and different numbers. Acceptance is evaluated on
# the sender's profile before a single word is read, which has no email equivalent.
LI_ACCEPT_FLOOR = 0.10
LI_ACCEPT_HEALTHY = 0.20
LI_REPLY_FLOOR = 0.10
LI_REPLY_HEALTHY = 0.20

COLUMN_ALIASES: dict[str, tuple[str, ...]] = {
    "sent": ("sent", "emails_sent", "sent_count", "total_sent", "sends",
             "invites_sent", "connections_sent", "requests_sent"),
    "accepted": ("accepted", "connections_accepted", "accepts", "accepted_count"),
    "delivered": ("delivered", "delivered_count"),
    "bounced": ("bounced", "bounce", "bounces", "bounced_count", "hard_bounces"),
    "opened": ("opened", "opens", "open_count", "unique_opens"),
    "replied": ("replied", "replies", "reply_count", "total_replies"),
    "positive": ("positive", "positive_replies", "interested", "positive_reply_count"),
    "unsubscribed": ("unsubscribed", "unsubscribes", "opt_outs", "optouts"),
    "complaints": ("complaints", "spam_complaints", "spam", "complaint_count"),
    "inbox": ("inbox", "sender", "from_email", "sender_email", "mailbox", "account"),
    "domain": ("domain", "sending_domain", "sender_domain", "from_domain"),
    "step": ("step", "sequence_step", "email_number", "variant_step"),
    "campaign": ("campaign", "campaign_name"),
    "segment": ("segment", "list", "list_name", "audience"),
}


@dataclass
class Finding:
    layer: str          # infrastructure | list | offer | copy
    severity: str       # blocker | warning | info
    headline: str
    evidence: str
    action: str

    def as_dict(self) -> dict[str, str]:
        return {
            "layer": self.layer,
            "severity": self.severity,
            "headline": self.headline,
            "evidence": self.evidence,
            "action": self.action,
        }


@dataclass
class Totals:
    sent: float = 0.0
    accepted: float = 0.0
    delivered: float = 0.0
    bounced: float = 0.0
    opened: float = 0.0
    replied: float = 0.0
    positive: float = 0.0
    unsubscribed: float = 0.0
    complaints: float = 0.0
    rows: int = 0

    def add(self, other: dict[str, float]) -> None:
        for key in (
            "sent", "accepted", "delivered", "bounced", "opened",
            "replied", "positive", "unsubscribed", "complaints",
        ):
            setattr(self, key, getattr(self, key) + other.get(key, 0.0))
        self.rows += 1

    @property
    def effective_delivered(self) -> float:
        """Delivered if reported, else sent minus bounced."""
        return self.delivered if self.delivered > 0 else max(self.sent - self.bounced, 0.0)

    def rate(self, numerator: str, denominator: str = "sent") -> float:
        den = self.effective_delivered if denominator == "delivered" else getattr(self, denominator)
        return getattr(self, numerator) / den if den > 0 else 0.0


def normalize_header(name: str) -> str:
    return name.strip().lower().replace(" ", "_").replace("-", "_")


def build_column_map(fieldnames: list[str]) -> dict[str, str]:
    """Map canonical names to whatever the export actually calls them."""
    present = {normalize_header(f): f for f in fieldnames}
    mapping: dict[str, str] = {}
    for canonical, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in present:
                mapping[canonical] = present[alias]
                break
    return mapping


def to_number(raw: str | None) -> float:
    if raw is None:
        return 0.0
    cleaned = str(raw).strip().replace(",", "").replace("%", "")
    if not cleaned:
        return 0.0
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def load(
    path: Path, group_by: str | None
) -> tuple[Totals, dict[str, Totals], dict[str, Totals], list[str]]:
    warnings: list[str] = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row.")
        colmap = build_column_map(reader.fieldnames)

        if "sent" not in colmap:
            raise ValueError(
                f"No 'sent' column found. Looked for {COLUMN_ALIASES['sent']}. "
                f"Header was: {reader.fieldnames}"
            )
        for needed in ("bounced", "replied"):
            if needed not in colmap:
                warnings.append(
                    f"No '{needed}' column found -- checks that depend on it are skipped."
                )

        group_col = colmap.get(group_by) if group_by else None
        if group_by and not group_col:
            warnings.append(f"No '{group_by}' column found; group analysis skipped.")

        # Always aggregate by inbox as well, so the domain-load check can run
        # regardless of what the caller asked to group by.
        inbox_col = colmap.get("inbox")

        overall = Totals()
        groups: dict[str, Totals] = {}
        inbox_groups: dict[str, Totals] = {}

        for row in reader:
            values = {
                canonical: to_number(row.get(source))
                for canonical, source in colmap.items()
                if canonical not in ("inbox", "domain", "step", "campaign", "segment")
            }
            overall.add(values)
            if group_col:
                key = (row.get(group_col) or "(blank)").strip() or "(blank)"
                groups.setdefault(key, Totals()).add(values)
            if inbox_col:
                ikey = (row.get(inbox_col) or "").strip()
                if ikey:
                    inbox_groups.setdefault(ikey, Totals()).add(values)

    return overall, groups, inbox_groups, warnings


def domain_of(sender: str) -> str | None:
    """Extract the sending domain from a mailbox address."""
    sender = (sender or "").strip().lower()
    if "@" in sender:
        domain = sender.rsplit("@", 1)[1].strip()
        return domain or None
    # Some exports carry a bare domain rather than an address.
    return sender if "." in sender else None


def check_domain_load(
    inbox_groups: dict[str, Totals], days: int
) -> list[Finding]:
    """
    Aggregate per-inbox sends up to the domain and compare against the daily ceiling.

    This catches the failure no ESP surfaces: every mailbox individually inside its
    limit while the domain carries several times what it should. Reputation is scored
    substantially at the domain level, so the aggregate is the number that binds.
    """
    findings: list[Finding] = []
    if days <= 0:
        return findings

    by_domain: dict[str, float] = {}
    mailboxes: dict[str, int] = {}
    for name, totals in inbox_groups.items():
        domain = domain_of(name)
        if not domain:
            continue
        by_domain[domain] = by_domain.get(domain, 0.0) + totals.sent
        mailboxes[domain] = mailboxes.get(domain, 0) + 1

    if not by_domain:
        return findings

    over = {
        d: (sent / days, mailboxes[d])
        for d, sent in by_domain.items()
        if sent / days > SENDS_PER_DOMAIN_DAY_CEILING
    }
    if over:
        listed = ", ".join(
            f"{d} ({rate:.0f}/day across {n} mailbox{'es' if n != 1 else ''})"
            for d, (rate, n) in sorted(over.items(), key=lambda x: -x[1][0])
        )
        findings.append(Finding(
            "infrastructure", "blocker",
            f"{len(over)} domain(s) sending above the {SENDS_PER_DOMAIN_DAY_CEILING}/day ceiling",
            f"{listed}. Period assumed {days} days.",
            f"Individual mailboxes may each look safe -- the domain aggregate is what "
            f"providers score. Cut to roughly {SENDS_PER_DOMAIN_DAY_TARGET}/day per "
            f"domain, or spread the same volume across more domains. Adding mailboxes "
            f"to an existing domain does not add capacity; it splits the same budget.",
        ))
    else:
        near = {
            d: sent / days for d, sent in by_domain.items()
            if sent / days > SENDS_PER_DOMAIN_DAY_TARGET
        }
        if near:
            findings.append(Finding(
                "infrastructure", "warning",
                f"{len(near)} domain(s) above the {SENDS_PER_DOMAIN_DAY_TARGET}/day target",
                ", ".join(f"{d} ({r:.0f}/day)" for d, r in sorted(near.items(), key=lambda x: -x[1])),
                "Inside the hard ceiling but with no headroom. Any volume increase "
                "pushes these over.",
            ))
    return findings


def diagnose_linkedin(overall: Totals) -> list[Finding]:
    """
    LinkedIn has its own funnel: invite -> accept -> reply -> positive.

    Acceptance is the layer with no email analogue. The recipient evaluates the sender's
    profile before reading anything, so a low acceptance rate is frequently the profile
    rather than the targeting -- and no amount of message rewriting reaches it.
    """
    findings: list[Finding] = []

    accept_rate = overall.accepted / overall.sent if overall.sent > 0 else 0.0
    base = overall.accepted if overall.accepted > 0 else overall.sent
    reply_rate = overall.replied / base if base > 0 else 0.0
    positive_share = overall.positive / overall.replied if overall.replied > 0 else None

    if overall.accepted > 0:
        if accept_rate < LI_ACCEPT_FLOOR:
            findings.append(Finding(
                "profile", "blocker",
                f"Connection acceptance {accept_rate:.0%} is at or below the 10% floor",
                f"{overall.accepted:,.0f} accepted of {overall.sent:,.0f} invites.",
                "Two causes, in this order: the sending profile is not credible to this "
                "audience, or the targeting is wrong. Fix the profile first -- headline, "
                "banner, about section, recent activity. Nothing you write in the message "
                "is being read yet.",
            ))
        elif accept_rate < LI_ACCEPT_HEALTHY:
            findings.append(Finding(
                "profile", "warning",
                f"Connection acceptance {accept_rate:.0%} is below the 20% healthy band",
                f"{overall.accepted:,.0f} accepted of {overall.sent:,.0f} invites.",
                "Optimised profiles reach 30-40%. Check that requests are sent without a "
                "note -- notes lower acceptance because most are used to pitch.",
            ))
        else:
            findings.append(Finding(
                "profile", "info",
                f"Connection acceptance {accept_rate:.0%} is healthy",
                f"{overall.accepted:,.0f} accepted of {overall.sent:,.0f} invites.",
                "The profile and targeting are working. Look further down the funnel.",
            ))

    if overall.replied > 0 or base >= 50:
        if reply_rate < LI_REPLY_FLOOR:
            findings.append(Finding(
                "copy", "blocker",
                f"Reply rate {reply_rate:.0%} of accepted connections is below 10%",
                f"{overall.replied:,.0f} replies on {base:,.0f} accepted.",
                "They accepted, so the profile passed. Three candidates in order: the "
                "message is too long, the targeting is wrong within an accepting "
                "audience, or the offer is weak. Shorten first -- LinkedIn messages "
                "should run under 50 words.",
            ))
        elif reply_rate < LI_REPLY_HEALTHY:
            findings.append(Finding(
                "copy", "warning",
                f"Reply rate {reply_rate:.0%} is in the low half of the 10-20% band",
                f"{overall.replied:,.0f} replies on {base:,.0f} accepted.",
                "Shorten the message and lower the CTA friction before rewriting it.",
            ))

    if positive_share is not None and overall.replied >= 20:
        if positive_share < POSITIVE_SHARE_TARGET:
            findings.append(Finding(
                "offer", "blocker" if positive_share < POSITIVE_SHARE_FLOOR else "warning",
                f"Only {positive_share:.0%} of replies are positive, against a 20-30% target",
                f"{overall.positive:,.0f} positive of {overall.replied:,.0f} replies.",
                "People are engaging and declining. That is the offer or the CTA, not the "
                "message. Change the campaign narrative rather than the wording.",
            ))

    if not findings:
        findings.append(Finding(
            "none", "info", "No LinkedIn threshold breaches detected",
            f"Acceptance {accept_rate:.0%}, reply {reply_rate:.0%}.",
            "Scale volume within LinkedIn's limits, or start a structured test.",
        ))

    order = {"profile": 0, "list": 1, "offer": 2, "copy": 3, "none": 4}
    sev = {"blocker": 0, "warning": 1, "info": 2}
    findings.sort(key=lambda f: (order.get(f.layer, 5), sev[f.severity]))
    return findings


def diagnose(
    overall: Totals,
    groups: dict[str, Totals],
    group_by: str | None,
    baseline_reply_rate: float | None,
    has_bounce: bool,
    has_reply: bool,
    inbox_groups: dict[str, Totals] | None = None,
    days: int = 22,
) -> list[Finding]:
    findings: list[Finding] = []

    # Domain load is checked first: it is an infrastructure blocker that no ESP reports,
    # and every mailbox can look compliant while the domain is carrying double.
    if inbox_groups:
        findings.extend(check_domain_load(inbox_groups, days))

    bounce = overall.rate("bounced", "sent")
    complaint = overall.rate("complaints", "sent")
    reply = overall.rate("replied", "delivered")
    positive_share = overall.positive / overall.replied if overall.replied > 0 else None
    unsub = overall.rate("unsubscribed", "delivered")

    # ---- Layer 1: infrastructure -------------------------------------------------
    if has_bounce and bounce > BOUNCE_CRITICAL:
        findings.append(Finding(
            "infrastructure", "blocker",
            f"Bounce rate {bounce:.1%} is past the {BOUNCE_CRITICAL:.0%} throttling line",
            f"{overall.bounced:,.0f} bounces on {overall.sent:,.0f} sends.",
            "Pause sending. Re-verify the entire list before another send. Reputation "
            "damage extends to every domain in the pool, not just this campaign.",
        ))
    elif has_bounce and bounce > BOUNCE_DANGER:
        findings.append(Finding(
            "infrastructure", "warning",
            f"Bounce rate {bounce:.1%} is in the danger zone (above {BOUNCE_DANGER:.0%})",
            f"{overall.bounced:,.0f} bounces on {overall.sent:,.0f} sends.",
            "Pull the sending domain from rotation now, before placement degrades for "
            "every campaign sharing it. Re-verify the list, then ramp back at half volume.",
        ))
    elif has_bounce and bounce > BOUNCE_WARN:
        findings.append(Finding(
            "infrastructure", "warning",
            f"Bounce rate {bounce:.1%} is elevated",
            f"{overall.bounced:,.0f} bounces on {overall.sent:,.0f} sends.",
            "Tighten verification. Drop catch-all and unknown before the next batch.",
        ))

    if complaint > COMPLAINT_CRITICAL:
        findings.append(Finding(
            "infrastructure", "blocker",
            f"Spam complaint rate {complaint:.2%} is past the danger line",
            f"{overall.complaints:,.0f} complaints on {overall.sent:,.0f} sends.",
            "Pause. Complaints at this level mean the list or the offer is wrong for "
            "these recipients -- this is not a copy tweak.",
        ))
    elif complaint > COMPLAINT_WARN:
        findings.append(Finding(
            "infrastructure", "warning",
            f"Spam complaint rate {complaint:.2%} is rising",
            f"{overall.complaints:,.0f} complaints on {overall.sent:,.0f} sends.",
            "Check relevance of the segment before scaling volume.",
        ))

    # A single dead inbox drags the aggregate down and looks exactly like bad copy.
    if group_by == "inbox" and len(groups) >= 3 and has_reply:
        rates = {
            name: t.rate("replied", "delivered")
            for name, t in groups.items()
            if t.effective_delivered >= 50
        }
        if len(rates) >= 3:
            median = statistics.median(rates.values())
            if median > 0:
                laggards = {
                    n: r for n, r in rates.items() if r < median * INBOX_OUTLIER_RATIO
                }
                if laggards:
                    listed = ", ".join(
                        f"{n} ({r:.1%})" for n, r in sorted(laggards.items(), key=lambda x: x[1])
                    )
                    findings.append(Finding(
                        "infrastructure", "blocker",
                        f"{len(laggards)} inbox(es) far below the median reply rate",
                        f"Median {median:.1%}; laggards: {listed}.",
                        "These inboxes are likely landing in spam. Pause them, keep "
                        "warmup running, and seed-test placement. The aggregate reply "
                        "rate is being dragged by infrastructure, not by the copy.",
                    ))

    infra_blocked = any(
        f.layer == "infrastructure" and f.severity == "blocker" for f in findings
    )

    # ---- Layer 2: list -----------------------------------------------------------
    if not infra_blocked:
        if has_reply and overall.effective_delivered >= 200 and reply < REPLY_FLOOR:
            findings.append(Finding(
                "list", "blocker",
                f"Reply rate {reply:.2%} is below the {REPLY_FLOOR:.0%} floor",
                f"{overall.replied:,.0f} replies on {overall.effective_delivered:,.0f} delivered.",
                "At this level the problem is almost never wording. Work the standard "
                "protocol in order: (1) run a placement test, (2) check the list and "
                "targeting, (3) check CTA friction -- a high-friction ask attached to a "
                "low-value proposition produces exactly this. Do not rewrite sentences "
                "until all three are clear.",
            ))

        if group_by == "segment" and len(groups) >= 2 and has_reply:
            rates = {
                n: t.rate("replied", "delivered")
                for n, t in groups.items()
                if t.effective_delivered >= 100
            }
            if len(rates) >= 2:
                best = max(rates.items(), key=lambda x: x[1])
                worst = min(rates.items(), key=lambda x: x[1])
                if worst[1] > 0 and best[1] >= worst[1] * 2.5:
                    findings.append(Finding(
                        "list", "warning",
                        "Reply rate varies sharply by segment",
                        f"Best: {best[0]} at {best[1]:.1%}. Worst: {worst[0]} at {worst[1]:.1%}.",
                        f"Concentrate spend on '{best[0]}' and cut or re-spec "
                        f"'{worst[0]}'. This is a targeting gain available without "
                        f"touching the copy.",
                    ))

    # ---- Layer 3: offer ----------------------------------------------------------
    if not infra_blocked and positive_share is not None and overall.replied >= 20:
        if positive_share < POSITIVE_SHARE_FLOOR:
            findings.append(Finding(
                "offer", "blocker",
                f"Only {positive_share:.0%} of replies are positive",
                f"{overall.positive:,.0f} positive of {overall.replied:,.0f} replies.",
                "People are reading and answering, so delivery and copy are working. "
                "They are saying no. That is an offer or segment problem -- re-score the "
                "Value Equation and check which lever is weakest. Rewriting the email "
                "will not change the answer.",
            ))
        elif positive_share >= 0.35:
            findings.append(Finding(
                "offer", "info",
                f"{positive_share:.0%} of replies are positive -- the offer is landing",
                f"{overall.positive:,.0f} positive of {overall.replied:,.0f} replies.",
                "Scale volume before touching messaging. The constraint is reach, "
                "not persuasion.",
            ))

    if unsub > 0.02:
        findings.append(Finding(
            "offer", "warning",
            f"Unsubscribe rate {unsub:.1%} is high",
            f"{overall.unsubscribed:,.0f} opt-outs on {overall.effective_delivered:,.0f} delivered.",
            "Recipients find this irrelevant rather than merely uninteresting. Narrow "
            "the segment before sending more.",
        ))

    # ---- Layer 4: copy -----------------------------------------------------------
    upstream_blocked = any(
        f.severity == "blocker" and f.layer in ("infrastructure", "list", "offer")
        for f in findings
    )
    if not upstream_blocked and has_reply:
        if baseline_reply_rate is not None:
            baseline = baseline_reply_rate / 100 if baseline_reply_rate > 1 else baseline_reply_rate
            if reply < baseline * 0.7:
                findings.append(Finding(
                    "copy", "warning",
                    f"Reply rate {reply:.1%} is well below your {baseline:.1%} baseline",
                    "Infrastructure, list, and offer checks are clean.",
                    "This is the point where a copy test is the right move. Change the "
                    "observation line first -- it carries more weight than the CTA.",
                ))
            else:
                findings.append(Finding(
                    "copy", "info",
                    f"Reply rate {reply:.1%} is in range against your {baseline:.1%} baseline",
                    "No upstream blockers.",
                    "Test structural variants rather than wording. Size the test with "
                    "gtm_math.py ab before running it.",
                ))
        elif REPLY_FLOOR <= reply < 0.03:
            findings.append(Finding(
                "copy", "warning",
                f"Reply rate {reply:.1%} is low but not floor-level",
                "Infrastructure, list, and offer checks are clean.",
                "Copy is now the most likely lever. Start with the observation line.",
            ))

    if not findings:
        findings.append(Finding(
            "none", "info", "No threshold breaches detected",
            f"Bounce {bounce:.1%}, reply {reply:.1%}, "
            f"positive share {positive_share:.0%}." if positive_share is not None
            else f"Bounce {bounce:.1%}, reply {reply:.1%}.",
            "Nothing is broken. Scale volume or start a structured A/B test.",
        ))

    order = {"infrastructure": 0, "list": 1, "offer": 2, "copy": 3, "none": 4}
    sev = {"blocker": 0, "warning": 1, "info": 2}
    findings.sort(key=lambda f: (order[f.layer], sev[f.severity]))
    return findings


def render(result: dict[str, Any]) -> str:
    m = result["metrics"]
    channel = result.get("channel", "email")
    lines = [
        f"Campaign Diagnosis ({channel})",
        "=" * (20 + len(channel)),
        "",
    ]

    if channel == "linkedin":
        lines += [
            f"  invites sent     {m['invites_sent']:>11,.0f}",
            f"  accepted         {m['accepted']:>11,.0f}",
            f"  acceptance rate  {m['acceptance_rate']:>11.1%}",
            f"  reply of accepted{m['reply_rate_of_accepted']:>11.1%}",
        ]
    else:
        lines += [
            f"  sends           {m['sent']:>12,.0f}",
            f"  delivered       {m['delivered']:>12,.0f}",
            f"  bounce rate     {m['bounce_rate']:>12.2%}",
            f"  reply rate      {m['reply_rate']:>12.2%}",
        ]
    if m.get("positive_share") is not None:
        lines.append(f"  positive share  {m['positive_share']:>12.1%}")
    if m.get("complaint_rate"):
        lines.append(f"  complaint rate  {m['complaint_rate']:>12.3%}")
    lines.append("")

    lines.append(f"  Verdict: fix the {result['primary_layer'].upper()} layer first.")
    lines.append("")

    for f in result["findings"]:
        mark = {"blocker": "BLOCKER", "warning": "warning", "info": "info   "}[f["severity"]]
        lines.append(f"  [{f['layer']}] {mark}  {f['headline']}")
        lines.append(f"      evidence: {f['evidence']}")
        lines.append(f"      action:   {f['action']}")
        lines.append("")

    if result["do_not_yet"]:
        lines.append("  Do NOT do these yet:")
        for item in result["do_not_yet"]:
            lines.append(f"    - {item}")
        lines.append("")

    for w in result["warnings"]:
        lines.append(f"  note: {w}")

    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Diagnose an outbound campaign from an ESP export."
    )
    ap.add_argument("path", help="CSV export")
    ap.add_argument(
        "--group-by",
        choices=["inbox", "segment", "step", "campaign"],
        help="Break the analysis down by this column when present",
    )
    ap.add_argument(
        "--baseline-reply-rate",
        type=float,
        help="Your historical reply rate, for comparison (percent)",
    )
    ap.add_argument(
        "--channel",
        choices=["email", "linkedin"],
        default="email",
        help="Which funnel to diagnose (default: email)",
    )
    ap.add_argument(
        "--days",
        type=int,
        default=22,
        help="Sending days the export covers, for the per-domain daily load check "
             "(default: 22)",
    )
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    path = Path(args.path)
    if not path.is_file():
        print(json.dumps({"error": f"File not found: {path}"}), file=sys.stderr)
        return 2

    try:
        overall, groups, inbox_groups, warnings = load(path, args.group_by)
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2

    if overall.sent <= 0:
        print(json.dumps({"error": "No sends found in the export."}), file=sys.stderr)
        return 2

    has_bounce = not any("'bounced'" in w for w in warnings)
    has_reply = not any("'replied'" in w for w in warnings)

    if args.channel == "linkedin":
        findings = diagnose_linkedin(overall)
        order = ["profile", "list", "offer", "copy"]
    else:
        findings = diagnose(
            overall, groups, args.group_by, args.baseline_reply_rate, has_bounce,
            has_reply, inbox_groups=inbox_groups, days=args.days,
        )
        order = ["infrastructure", "list", "offer", "copy"]

    primary = next((f.layer for f in findings if f.severity == "blocker"), None)
    if primary is None:
        primary = next((f.layer for f in findings if f.severity == "warning"), "none")
    do_not_yet: list[str] = []
    if primary in order:
        for later in order[order.index(primary) + 1:]:
            do_not_yet.append(
                f"Do not work the {later} layer until the {primary} issue is resolved -- "
                f"changes there will be masked by it."
            )

    positive_share = overall.positive / overall.replied if overall.replied > 0 else None

    if args.channel == "linkedin":
        base = overall.accepted if overall.accepted > 0 else overall.sent
        metrics = {
            "invites_sent": overall.sent,
            "accepted": overall.accepted,
            "acceptance_rate": overall.accepted / overall.sent if overall.sent else 0.0,
            "reply_rate_of_accepted": overall.replied / base if base else 0.0,
            "positive_share": positive_share,
            "rows": overall.rows,
        }
    else:
        metrics = {
            "sent": overall.sent,
            "delivered": overall.effective_delivered,
            "bounce_rate": overall.rate("bounced", "sent"),
            "reply_rate": overall.rate("replied", "delivered"),
            "positive_share": positive_share,
            "complaint_rate": overall.rate("complaints", "sent"),
            "unsubscribe_rate": overall.rate("unsubscribed", "delivered"),
            "rows": overall.rows,
        }

    result = {
        "channel": args.channel,
        "metrics": metrics,
        "primary_layer": primary,
        "findings": [f.as_dict() for f in findings],
        "do_not_yet": do_not_yet,
        "warnings": warnings,
    }

    print(json.dumps(result, indent=2) if args.json else render(result))
    return 1 if any(f.severity == "blocker" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
