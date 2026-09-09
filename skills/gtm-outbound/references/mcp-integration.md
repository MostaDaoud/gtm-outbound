# MCP Integration — Optional Live Data

Load when a sub-skill wants live campaign data instead of a manual export.

**This skill never requires MCP.** Every workflow must work with local files alone. MCP is
an accelerator on the read path, nothing more. A skill that hard-depends on a connector
breaks for anyone who has not configured it, and breaks silently when auth expires.

## The Boundary

| Direction | Policy |
|---|---|
| **Read** — stats, replies, campaign lists, lead status | Use MCP when available |
| **Write** — send, launch, resume, push a sequence live | **Never through this skill** |

The write prohibition is not caution about tooling quality. Sending is irreversible,
outward-facing, and operates at scale: a wrong campaign id or an unfiltered list emails
thousands of real people, and there is no recall. That action belongs to a human clicking
a button in the platform, having seen exactly what is about to go out.

If the user explicitly asks the skill to launch a campaign, produce the configuration and
tell them plainly it is theirs to send. Do not treat a general "set up my campaign" as
authorisation to transmit.

## Availability Check

Never assume a connector exists. Check, then branch:

1. Attempt the cheapest read the server offers — a campaign list, an account summary.
2. **If it succeeds**, proceed with live data and say so in the output, including when the
   data was pulled.
3. **If it fails or is absent**, fall back silently to the export path. Do not error, do
   not lecture the user about installing anything mid-task. Ask for the CSV.

Report which path was used. A diagnosis run on a three-week-old export and one run on live
data deserve different confidence, and the reader cannot tell them apart otherwise.

## Where It Helps

### `gtm-outbound-diagnose`

The strongest case. The diagnostic loop is currently: export CSV, save it, point the
script at it. Live stats remove that friction entirely, which matters because diagnosis is
something you do repeatedly, not once.

Pull per-inbox and per-campaign figures, write them to a local CSV in the shape
`diagnose_campaign.py` already expects, then run the script unchanged:

```bash
python scripts/diagnose_campaign.py live-export.csv --group-by inbox
```

**Keep the analysis in the script even when the data arrives live.** The layer ordering,
the suppression logic, and the thresholds are the valuable part, and they are only
trustworthy because they are deterministic. Do not reimplement them conversationally
against MCP output.

### `gtm-outbound-reply`

Pull recent replies into the CSV shape `reply_classify.py` expects, then classify.

The deterministic first pass still runs. **Opt-out detection must never move into a
conversational read of MCP output** — an unsubscribe missed because a model was
summarising is a compliance failure, not a bug.

Drafting replies remains draft-only. Do not send them.

### Not Worth Wiring

**List building and enrichment.** Running credit-consuming operations through an agent
loop, with no preview of what is about to be spent, inverts the cost discipline the rest
of this skill enforces. Generate the spec; let the human run it.

**Campaign creation.** The specification is the hard part and this skill already produces
it. Clicking is not the bottleneck.

## Recording It

When live data is used, note it in the output artifact:

```
Data source: live (pulled 2026-08-04 14:20 UTC) | manual export (file dated ...)
```

This matters when a diagnosis is revisited weeks later and nobody remembers whether the
numbers were current.

## If a Connector Is Missing

Say what would be gained and let the user decide, once, without repeating it every run:

> Smartlead exposes campaign stats over MCP. Connecting it would let diagnosis run without
> a manual export each time. For now, export the campaign CSV and point me at it.

Never block a workflow on a missing connector.
