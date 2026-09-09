# Clay Cross-Table Mechanics & HTTP API

Load when data needs to move between tables, when one row must become many, or when
connecting a tool Clay does not natively integrate.

---

## The problem these solve

Clay tables are flat. A single row holds a single entity. But enrichments routinely return
**lists** — five contacts at a company, 200 lookalikes, a dozen job openings — and a list
crammed into one cell cannot be filtered, enriched, scored, or sent.

Write to Table converts a list into rows. Lookup joins the context back.

---

## Write to Table

### Recognizing a list

Clay marks list-typed cells with a curly-bracket badge showing a count: `{5}`. That badge
means the cell holds nested objects with their own attributes.

**Write to Table only accepts an actual list input.** Pointing it at a plain column fails —
it will not recognize the column as valid. Check for the badge before building.

### The four configuration parts

1. **Destination table** — new, or existing. Choose existing only when you are genuinely
   appending to a list that is already there; otherwise create new.
2. **The list to expand** — the list column that becomes one row per item.
3. **Attributes from that list** — each nested attribute becomes a column in the
   destination. Expand one list item to see what is available.
4. **Other data from this table** — fields from the *source* row to carry across, which is
   how company context stays attached to contact rows.

Part four is what people miss, and its absence is why contact tables arrive with no
company data attached.

### Constants versus per-row values

This is the part that silently breaks builds.

| Field type | Behavior | How to map |
|---|---|---|
| Company-level (funding, headcount, founded) | Identical for every contact from that company | Mark as constant, map with the column token |
| Contact-level (name, title, profile URL) | Different per contact | Map by **attribute name**, typed literally — not with a token |

Using a token for a per-contact field yields the same value repeated down every row from
that company. It looks like it worked. To find the correct attribute name, expand one item
in the list and read the attribute labels.

### Preparing the destination

A quick way to build a destination table matching your source schema: export the source as
CSV, re-import it as a new table, clear the data, then add the extra columns you need.
That gives you a column-for-column match without hand-building each one.

### The implicit case

Going from a companies table to a people table via `find people` runs Write to Table for
you, and creates the lookup column automatically. You only configure it manually for
custom fan-outs — lookalikes, jobs, search results.

---

## Lookup row in other table

The reverse join. Matches on a key you specify and pulls the matching row's data across.

Used for:

- Reattaching company context to a contact table
- Checking whether a newly sourced row already exists in an existing list — the clean way
  to suppress rows already in a sequence or already customers
- Deduplicating lookalike output against the seed set

**Choose a key that is genuinely unique and normalized.** Domain is reliable; company name
is not, since the same company appears as several strings.

---

## HTTP API

Connects Clay to anything with a web API. Low code rather than no code.

### Methods

Two cover nearly everything:

| Method | Direction | Use |
|---|---|---|
| `GET` | Retrieve | Fetch data from an endpoint |
| `POST` | Send | Push data to an endpoint and get a result back |

`PATCH`, `PUT`, and `DELETE` exist for data-modification work and are rarely needed in an
enrichment context.

### Before hand-building

Check in this order:

1. **Templates** — prebuilt configurations for common tools Clay does not yet integrate
   natively.
2. **AI-assisted configuration** — supply the endpoint and let Clay draft the initial
   setup.
3. **Saved configurations** — your own past setups, reusable across tables and workbooks.

Only hand-build after those three miss.

### Authentication

Most APIs need a key, a bearer token, or similar in the request. Some public endpoints
need nothing. JWT authentication has a separate mode, used only when the target API
requires it — otherwise the mechanics are identical.

**Never put credentials in a spec document.** Reference which credential is needed and
where it goes; leave the value to the person building.

### The pattern worth copying

When an API's required parameters vary by row — a case where one record needs two inputs
and another needs five — build **one HTTP API column per shape**, and gate each with a
conditional run on the row matching that shape. Then merge the outputs into a single final
column.

That is the general solution to variable-shape API calls in a flat table, and it reuses
the same conditional-run mechanism as everything else. It costs nothing extra: only the
matching column runs per row.

### Getting a list back

A `GET` that returns a collection lands entirely in one cell. Run it through Write to
Table to make it usable — the same mechanic as any other list.

---

## Export

The destination side of FETE.

| Destination | Notes |
|---|---|
| CRM (HubSpot, Salesforce, others) | Native integrations |
| Email sequencer | Native for major tools |
| Anything else | HTTP API, or a workflow tool as intermediary |
| CSV | Always available |

### The ordering trap

**Create custom fields in the destination before mapping them in Clay.** Clay can only map
to fields that already exist on the other side; refresh the field list after creating
them.

A column that exists in Clay but was never mapped renders **blank** in the send. The data
is correct, the export ran, nothing errors, and the email goes out with an empty gap where
the personalization should be. Neither tool flags it.

This is the same failure `validate_spintax.py --vars` catches on the copy side. Both
checks are needed: one confirms the variable is produced, the other confirms it is
exported.
