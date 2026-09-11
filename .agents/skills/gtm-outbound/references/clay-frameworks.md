# Clay Frameworks — FETE, Jigsaw, SPICE

Load when constructing a Clay table or writing any prompt that will run at row scale.

Three frameworks. They are not branding — each one resolves a specific failure mode that
costs money or produces empty columns.

**Provenance, checked 2026-08-15.** FETE and Jigsaw are Clay's own: Clay University
publishes lessons under both names, and the definitions below match them. **SPICE is not
in Clay's published curriculum** — it is absent from the Claygent lesson and the AI
prompt-writing docs, and it does not appear in the GTM course either. Treat it as a local
convention for structuring row-scale prompts, useful on its own terms, until someone can
point at a source. Do not describe it to a client as Clay's.

---

## FETE — the order of operations

**Find → Enrich → Transform → Export.**

| Step | What it does |
|---|---|
| Find | Get initial rows into the table — native sources or imported data |
| Enrich | Add data to those rows — waterfalls, integrations, AI web research |
| Transform | Reshape what you have into what you will actually send |
| Export | Push to CRM, sequencer, or another destination |

The failure this prevents is **transforming before enriching**. A snippet prompt written
against a field that has not been populated yet does not error — it generates confidently
from nothing, or returns empty, and you find out after it has run across the whole table.

Clay calls the alternative the *blank canvas problem*: the tool is flexible enough that
without an order to work in, people build sideways and never finish a working pipeline.

---

## Jigsaw — the dependency rule

Building an enrichment workflow is assembling a puzzle. You place **corner pieces** first,
then **edges**, then fill the middle.

### Corner pieces

Everything downstream keys off these. Get them before anything else runs.

| Leg | Corners |
|---|---|
| Company | `company_domain` **and** company LinkedIn profile URL |
| Person | personal LinkedIn profile URL **and** `full_name` |

If you only have a company name, recover the domain via Google search or Claygent before
proceeding. If you only have a full name, recover the LinkedIn URL from name + job title
+ company domain.

You *can* start an email waterfall from full name + company domain alone. Coverage is
measurably worse than with both corners present — treat it as a fallback, not a plan.

### Edges

`enrich company` and `enrich person` are single calls that each return a wide block of
data: headcount, industry, HQ, description on the company side; job title, bio, education,
full experience history on the person side.

Run these **before** building anything custom. Most "I need a Claygent column for this"
requests are answered by a field the enrichment already returned — the person enrichment
alone returns over two dozen distinct fields, several of them nested arrays containing
dozens more.

### Middle

Only now: research columns, derived scores, snippets, anything bespoke.

### Why the order is load-bearing

**A column missing its corner piece does not fail loudly.** It returns empty for that row
and the table keeps running. An email waterfall keyed on a domain that never resolved will
call every provider in sequence and return nothing, at full cost.

So: resolve corners, then gate every downstream column on the corner being non-empty.

---

## SPICE — prompt structure at row scale

Chat prompting and Clay prompting are different disciplines. In chat you refine across
turns. In Clay you write **one prompt that must work first time across thousands of rows.**

Five sections, delimited with `#` headers so the model can tell structure from content:

```
# Variables
{first_name}   = First Name column
{company}      = Company Name column
{profile}      = Enriched Profile column

# Context
You are an expert writer skilled at short, succinct, personalized notes
based on someone's work profile and history.

# Instructions
Keep the output to no more than 10 words.
Always use second person.
Complete the sentence using the steps below:
1. If {profile} shows an award in the last year, reference the award.
2. If not, check for a promotion or new role in the last year; reference that.
3. If neither, use a job anniversary, certification, or volunteer experience.
4. If none of the above are present, return empty.

# Examples
<award>congrats on making it to President's Club this year</award>
<newjob>congrats on the new role at Acme</newjob>
<promotion>congrats on the promotion to Director last quarter</promotion>
```

### Section notes

**Variables** — bind each column to a curly-bracket name once at the top, then reference
the name everywhere else. When a column gets renamed or swapped you edit one line instead
of hunting through prose. This is the single biggest maintenance win in the framework.

**Context** — narrows an model trained on everything down to the task. Keep it to who the
writer is and what register they write in.

> **Never state that the task is cold email or outbound.** Clay's own guidance: the
> training data behind those phrases is thousands of SEO-driven pages of mediocre advice,
> and invoking the frame pulls the register down with it. Ask for a short, friendly,
> succinct writer instead.

**Instructions** — numbered and explicit, with a **fallback chain**. Personalization data
is unevenly available; a prompt without an ordered fallback will either invent something
for the sparse rows or return unusable output. End the chain with an explicit empty
return.

**Examples** — wrap in tags so they read as examples rather than instructions. Include one
per branch of the fallback chain. Most valuable for copywriting and data cleaning; less
so for web research, where output shape matters more than register.

### The rule that governs all of it

**Always permit an empty return.** A prompt with no failure path produces confident
fabrication on the rows where the data was not there — and that is precisely the output
that reaches a prospect who knows it is false.

---

## Applying SPICE to AI formulas

You do not need it. AI formulas run on a purpose-built model with a narrow job, so plain
instructions work and there is far more margin for error. Save the structure for AI
columns and Claygent, where the output goes to a prospect.

## Save the agent, not just the prompt

A Claygent you will run more than once should be built once and saved as a reusable agent
rather than rewritten per table. Clay lets you define the agent — model, prompt, output
shape — ahead of any table, then drop it into new tables by name.

Build them for the classification questions that recur across every campaign:

- Is this company B2B or B2C?
- Is this a SaaS product or a service business?
- Have they raised funding, and when?
- Does this company match the ICP as written?

**A worked example — a SaaS classifier.** The prompt that works reads the company's own
site first (homepage, product, pricing, about, docs), treats the presence of API
documentation or a self-serve pricing page as positive evidence, then corroborates against
third-party sources where a listing is itself a signal — a G2 or Capterra profile is
meaningful evidence of SaaS in a way a LinkedIn page is not. Output is constrained to a
small enum: `SaaS` / `Not SaaS` / `Unclear`.

**This beats the provider's own firmographic flag.** Apollo's B2B/B2C and SaaS
classifications are unreliable enough that filtering on them silently corrupts a segment. A
Claygent that reads the actual website and shows its reasoning is both more accurate and
auditable — you can see *why* a row was classified, which you cannot with a vendor flag.

Two rules carry over from SPICE: constrain the output to an enum rather than prose, and
allow an explicit `Unclear`. A classifier with no escape hatch fabricates confidently, and
a fabricated classification is worse than an empty cell because it silently passes the
filter.
