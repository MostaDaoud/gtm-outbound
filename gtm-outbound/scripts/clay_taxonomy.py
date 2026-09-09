#!/usr/bin/env python3
"""
Purpose: Generate and validate the Clay table schema that backs an outbound campaign.
         A Clay table is a dependency graph -- every column consumes upstream columns
         and burns credits when it runs. Hand-built tables fail in two expensive ways:
         a merge tag in the copy that no column produces, and an enrichment waterfall
         that calls the costly provider before the cheap one.

Subcommands:
    generate  Build clay-table.json from an ICP, sources, and a provider waterfall.
    validate  Check an existing clay-table.json for orphans, ordering, and gating.
    vars      Print the merge variables a table produces (feeds validate_spintax.py).

Output:  JSON to stdout or --output; human report for validate.
         Exit 0 clean, 1 on validation errors.

Usage:
    python clay_taxonomy.py generate --waterfall leadmagic,findymail,prospeo \\
        --personalize case_study_result,recent_launch --output clay-table.json
    python clay_taxonomy.py validate clay-table.json
    python clay_taxonomy.py vars clay-table.json > allowed_vars.json

NOTE ON THE PROVIDER REGISTRY: cost tiers and coverage below are starting defaults,
not fixed truth. Provider pricing and match rates move on a quarterly cadence -- edit
PROVIDER_REGISTRY to match the rates you are actually paying.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# tier: relative cost per successful match (1 = cheapest). Order a waterfall so the
# cheap, high-coverage providers run first and the expensive ones only see the
# leftovers. Edit to match your contracted rates.
PROVIDER_REGISTRY: dict[str, dict[str, Any]] = {
    "leadmagic": {"tier": 1, "kind": "email", "notes": "Broad B2B coverage, low cost per hit"},
    "findymail": {"tier": 1, "kind": "email", "notes": "Strong on verified work emails"},
    "prospeo": {"tier": 2, "kind": "email", "notes": "Good LinkedIn-sourced coverage"},
    "datagma": {"tier": 2, "kind": "email", "notes": "Useful EU coverage"},
    "dropcontact": {"tier": 2, "kind": "email", "notes": "GDPR-friendly, EU-focused"},
    "hunter": {"tier": 3, "kind": "email", "notes": "Pattern-based, verify before sending"},
    "apollo": {"tier": 3, "kind": "email", "notes": "Wide but staler data"},
    "bettercontact": {"tier": 3, "kind": "email", "notes": "Waterfall-of-waterfalls, priciest per hit"},
    # DEPRECATED 2026-09-09: Clearbit was acquired by HubSpot and folded into the Breeze
    # stack; no longer viable as a standalone waterfall provider. Kept in the registry so
    # old table specs still validate -- new builds should use dropcontact (GDPR-clean EU)
    # or datagma for company resolution and firmographics.
    "clearbit": {"tier": 3, "kind": "company", "notes": "DEPRECATED (HubSpot/Breeze). Use dropcontact or datagma"},
    "claygent": {"tier": 2, "kind": "research", "notes": "LLM web research, cost scales with prompt"},
    "millionverifier": {"tier": 1, "kind": "verify", "notes": "Bulk verification, cheap per check"},
    "bounceban": {"tier": 3, "kind": "verify", "notes": "Higher accuracy, higher price -- worth it when bounce rate is the binding constraint"},
}

STAGES = [
    "source", "resolve", "enrich", "people", "email", "verify",
    "transform", "personalize", "export",
]

# What a column costs to run. Most transform work in Clay is free -- AI formulas and
# the native tool functions (normalize, extract, count, score, order, map, group) cost
# no credits to create or run. Paying an AI column to do that work is the most common
# avoidable cost in a Clay build, and nothing in the product flags it.
CREDIT_CLASSES = ("free", "credit", "ai")

# Verbs that describe work a free AI formula or native function already does. An `ai`
# column whose name or notes match one of these is probably a paid column doing free
# work. Heuristic -- it warns, never errors.
FREE_WORK_HINTS = (
    "extract", "count", "concat", "normalize", "normalise", "lowercase", "uppercase",
    "format", "clean", "split", "parse", "dedupe", "deduplicate", "trim", "titlecase",
    "strip", "round", "sort", "rename",
)


def infer_credit_class(provider: str | None, stage: str) -> str:
    """A column with no provider costs nothing. Research providers bill per model call;
    everything else bills per row."""
    if provider is None:
        return "free"
    if PROVIDER_REGISTRY.get(provider, {}).get("kind") == "research":
        return "ai"
    return "credit"


def col(
    name: str,
    stage: str,
    provider: str | None,
    inputs: list[str],
    *,
    run_condition: str = "always",
    smartlead_field: str | None = None,
    dtype: str = "string",
    notes: str = "",
    credit_class: str | None = None,
) -> dict[str, Any]:
    return {
        "name": name,
        "stage": stage,
        "provider": provider,
        "type": dtype,
        "inputs": inputs,
        "run_condition": run_condition,
        "smartlead_field": smartlead_field,
        "credit_class": credit_class or infer_credit_class(provider, stage),
        "notes": notes,
    }


def cmd_generate(args: argparse.Namespace) -> dict[str, Any]:
    waterfall = [p.strip().lower() for p in args.waterfall.split(",") if p.strip()]
    personalize = [p.strip() for p in (args.personalize or "").split(",") if p.strip()]
    sources = [s.strip() for s in (args.sources or "manual").split(",") if s.strip()]

    unknown = [p for p in waterfall if p not in PROVIDER_REGISTRY]
    if unknown:
        raise ValueError(
            f"Unknown provider(s): {', '.join(unknown)}. "
            f"Known: {', '.join(sorted(PROVIDER_REGISTRY))}. "
            f"Add them to PROVIDER_REGISTRY with a cost tier if they are new."
        )

    columns: list[dict[str, Any]] = [
        col("company_name", "source", None, [], notes=f"From: {', '.join(sources)}"),
        col("company_url", "source", None, [], notes="Raw URL as scraped"),
        col(
            "signal_detected_at",
            "source",
            None,
            [],
            dtype="date",
            notes="When the trigger was observed. Without it you cannot prioritise by "
                  "freshness or suppress stale rows.",
        ),
        col(
            "signal_age_days",
            "source",
            None,
            ["signal_detected_at"],
            dtype="number",
            notes="Days since detection. Sort the send queue ascending, work the "
                  "freshest first, suppress past the decay window.",
        ),
        col(
            "company_domain",
            "resolve",
            "datagma",
            ["company_name", "company_url"],
            notes="Normalized root domain; everything downstream keys off this",
        ),
        col(
            "headcount",
            "enrich",
            "datagma",
            ["company_domain"],
            run_condition="company_domain is not empty",
            dtype="number",
        ),
        col(
            "industry",
            "enrich",
            "datagma",
            ["company_domain"],
            run_condition="company_domain is not empty",
        ),
        col("first_name", "people", None, [], smartlead_field="first_name"),
        col("last_name", "people", None, [], smartlead_field="last_name"),
        col("job_title", "people", None, [], smartlead_field="job_title"),
        col("linkedin_url", "people", None, [], notes="Needed for the LinkedIn track"),
    ]

    # Email waterfall: each provider runs only on rows the previous one missed.
    for idx, provider in enumerate(waterfall):
        prior = f"email_{waterfall[idx - 1]}" if idx else None
        columns.append(
            col(
                f"email_{provider}",
                "email",
                provider,
                ["first_name", "last_name", "company_domain"],
                run_condition="always" if idx == 0 else f"{prior} is empty",
                notes=(
                    f"Tier {PROVIDER_REGISTRY[provider]['tier']} -- "
                    f"{PROVIDER_REGISTRY[provider]['notes']}"
                ),
            )
        )

    columns.append(
        col(
            "work_email",
            "email",
            None,
            [f"email_{p}" for p in waterfall],
            notes="Coalesce: first non-empty result from the waterfall",
            smartlead_field=None,
        )
    )
    columns.append(
        col(
            "email_status",
            "verify",
            "millionverifier",
            ["work_email"],
            run_condition="work_email is not empty",
            notes="Gate sending on 'valid' only; keeps bounce rate in the healthy band (under 2%; 3% pulls the domain)",
        )
    )
    columns.append(
        col(
            "verified_email",
            "verify",
            None,
            ["work_email", "email_status"],
            run_condition="email_status is valid",
            smartlead_field="email",
            notes="The only address that may reach the sender",
        )
    )

    # Research columns are the most expensive per row, so they run last and only on
    # rows that already have a deliverable address.
    for var in personalize:
        columns.append(
            col(
                var,
                "personalize",
                "claygent",
                ["company_domain", "verified_email"],
                run_condition="verified_email is not empty",
                smartlead_field=var,
                notes="LLM web research -- gated so it never runs on undeliverable rows",
            )
        )

    return {
        "version": 1,
        "sources": sources,
        "waterfall": waterfall,
        "columns": columns,
    }


def validate_table(table: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    columns = table.get("columns", [])

    if not columns:
        return {"ok": False, "errors": ["Table has no columns."], "warnings": []}

    names = [c.get("name") for c in columns]
    seen: set[str] = set()
    for n in names:
        if n in seen:
            errors.append(f"Duplicate column name '{n}'.")
        seen.add(n)

    # Every input must be produced by a column defined earlier in the table.
    produced: set[str] = set()
    for c in columns:
        for dep in c.get("inputs", []):
            if dep not in produced:
                if dep in seen:
                    errors.append(
                        f"Column '{c['name']}' consumes '{dep}', which is defined later "
                        f"in the table. Clay runs top down, so this reads empty."
                    )
                else:
                    errors.append(
                        f"Column '{c['name']}' consumes '{dep}', which no column produces."
                    )
        produced.add(c.get("name"))

    # Merge fields exported to the sender must have a producing column.
    exported = {c["smartlead_field"]: c["name"] for c in columns if c.get("smartlead_field")}
    if "email" not in exported:
        errors.append(
            "No column maps to the 'email' Smartlead field. The campaign has no "
            "address to send to."
        )

    # Waterfall must run cheap to expensive, and everything after the first must gate.
    email_cols = [c for c in columns if c.get("stage") == "email" and c.get("provider")]
    tiers = [
        (c["name"], PROVIDER_REGISTRY.get(c["provider"], {}).get("tier"))
        for c in email_cols
    ]
    for (n1, t1), (n2, t2) in zip(tiers, tiers[1:]):
        if t1 is None or t2 is None:
            warnings.append(
                f"No cost tier registered for one of '{n1}'/'{n2}' -- ordering unchecked."
            )
        elif t2 < t1:
            errors.append(
                f"Waterfall runs '{n1}' (tier {t1}) before '{n2}' (tier {t2}). The "
                f"cheaper provider should go first so the expensive one only sees "
                f"leftovers."
            )

    for c in email_cols[1:]:
        if c.get("run_condition", "always") == "always":
            errors.append(
                f"'{c['name']}' runs unconditionally. Every later waterfall step must "
                f"be gated on the previous one coming back empty, or you pay every "
                f"provider for every row."
            )

    verify_cols = [c for c in columns if c.get("stage") == "verify"]
    if not verify_cols:
        errors.append(
            "No verification stage. Sending unverified addresses drives bounce rate "
            "past the 4% throttling threshold."
        )

    for c in columns:
        if c.get("stage") == "personalize" and c.get("run_condition", "always") == "always":
            warnings.append(
                f"Research column '{c['name']}' is ungated. LLM research is the most "
                f"expensive column type -- gate it on a verified email so it never "
                f"runs on rows you cannot contact."
            )

    # --- Credit classification -------------------------------------------------
    for c in columns:
        klass = c.get("credit_class")
        if klass is None:
            warnings.append(
                f"Column '{c['name']}' has no credit_class. Regenerate the table, or "
                f"set it to one of {', '.join(CREDIT_CLASSES)} so cost is auditable."
            )
            continue
        if klass not in CREDIT_CLASSES:
            errors.append(
                f"Column '{c['name']}' has credit_class '{klass}'. "
                f"Must be one of {', '.join(CREDIT_CLASSES)}."
            )

    # A paid column whose job is data manipulation is almost always a free AI formula
    # or native function that was built as an AI column by mistake.
    for c in columns:
        if c.get("credit_class") != "ai":
            continue
        haystack = f"{c.get('name', '')} {c.get('notes', '')}".lower()
        hit = next((v for v in FREE_WORK_HINTS if v in haystack), None)
        if hit:
            warnings.append(
                f"Column '{c['name']}' is class 'ai' but looks like '{hit}' work. "
                f"Extraction, counting, formatting and normalization are free in Clay "
                f"via AI formulas or native tool functions -- reclassify unless this "
                f"genuinely needs judgment or data not already in the table."
            )

    # Every paid column should be gated on something. Ungated paid columns run on every
    # row including the ones that were never going to be usable.
    for c in columns:
        if c.get("credit_class") in ("credit", "ai") and c.get("run_condition") == "always":
            if c.get("stage") in ("source", "resolve"):
                continue  # entry points legitimately run on everything
            if c["name"] not in {f"email_{p}" for p in table.get("waterfall", [])[:1]}:
                warnings.append(
                    f"Paid column '{c['name']}' runs unconditionally. Gate it on its "
                    f"corner piece being present, or you pay for rows that cannot "
                    f"produce a result."
                )

    cost_split = {k: sum(1 for c in columns if c.get("credit_class") == k) for k in CREDIT_CLASSES}

    return {
        "ok": not errors,
        "columns": len(columns),
        "exported_fields": sorted(exported),
        "cost_split": cost_split,
        "errors": errors,
        "warnings": warnings,
    }


def cmd_validate(args: argparse.Namespace) -> dict[str, Any]:
    table = json.loads(Path(args.path).read_text(encoding="utf-8"))
    return validate_table(table)


def cmd_vars(args: argparse.Namespace) -> dict[str, Any]:
    table = json.loads(Path(args.path).read_text(encoding="utf-8"))
    return {
        "columns": [
            {"name": c["name"], "smartlead_field": c["smartlead_field"]}
            for c in table.get("columns", [])
            if c.get("smartlead_field")
        ]
    }


def render_validation(result: dict[str, Any]) -> str:
    lines = [
        f"Clay table validation: {'PASS' if result['ok'] else 'FAIL'}",
        f"  {result.get('columns', 0)} columns, "
        f"{len(result['errors'])} errors, {len(result['warnings'])} warnings",
    ]
    if result.get("exported_fields"):
        lines.append(f"  Exported merge fields: {', '.join(result['exported_fields'])}")
    if result.get("cost_split"):
        cs = result["cost_split"]
        lines.append(
            f"  Cost split: {cs.get('free', 0)} free, "
            f"{cs.get('credit', 0)} credit, {cs.get('ai', 0)} ai"
        )
    for e in result["errors"]:
        lines.append(f"\n  ERROR    {e}")
    for w in result["warnings"]:
        lines.append(f"\n  warning  {w}")
    return "\n".join(lines)


def add_json_flag(p: argparse.ArgumentParser) -> None:
    """Accept --json on the subcommand as well as before it (argparse binds
    top-level options only ahead of the subcommand, which is not where people
    type them). SUPPRESS stops an absent flag from overwriting a top-level one."""
    p.add_argument("--json", action="store_true", default=argparse.SUPPRESS,
                   help="Emit JSON")


def main() -> int:
    parser = argparse.ArgumentParser(description="Clay table schema generator/validator.")
    parser.add_argument("--json", action="store_true", help="Force JSON output")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("generate", help="Build a clay-table.json")
    p.add_argument("--waterfall", required=True, help="Ordered providers, comma-separated")
    p.add_argument("--sources", help="Sourcing channels, comma-separated")
    p.add_argument("--personalize", help="Research variables, comma-separated")
    p.add_argument("--output", "-o", type=Path, help="Write JSON here")
    add_json_flag(p)
    p.set_defaults(func=cmd_generate)

    p = sub.add_parser("validate", help="Check an existing table")
    p.add_argument("path", help="Path to clay-table.json")
    add_json_flag(p)
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("vars", help="Print merge variables the table produces")
    p.add_argument("path", help="Path to clay-table.json")
    add_json_flag(p)
    p.set_defaults(func=cmd_vars)

    args = parser.parse_args()

    try:
        result = args.func(args)
    except (ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(json.dumps({"error": f"File not found: {exc.filename}"}), file=sys.stderr)
        return 2

    if args.command == "generate":
        payload = json.dumps(result, indent=2)
        if args.output:
            args.output.write_text(payload + "\n", encoding="utf-8")
            check = validate_table(result)
            print(f"Wrote {args.output} ({len(result['columns'])} columns)")
            print(render_validation(check))
            return 0 if check["ok"] else 1
        print(payload)
        return 0

    if args.command == "validate" and not args.json:
        print(render_validation(result))
        return 0 if result["ok"] else 1

    print(json.dumps(result, indent=2))
    return 0 if result.get("ok", True) else 1


if __name__ == "__main__":
    sys.exit(main())
