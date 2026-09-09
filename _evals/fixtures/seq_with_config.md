## Email 1 - Poke the Bear

{{Hey|Hi}} {{first_name}},

{{Saw|Noticed}} {{company_name}} just closed a round.

{{How are you handling|What is your approach to}} pipeline right now?

Best,
Mostafa

## Smartlead Configuration

Sends per inbox per day is set to 25, which is conservative enough to absorb a
reputation dip without forcing a pause mid-campaign. Warmup runs for a minimum of
fourteen days before the first live send, at forty warmup emails per day, ramping up
by five per day with randomisation enabled and a warmup reply rate between thirty and
forty percent. Domains are separate from the primary company domain, with SPF, DKIM
and DMARC configured on each, roughly three mailboxes per domain, and a custom
tracking domain. Open tracking is disabled deliberately.

## Compliance Checklist

Physical address in the footer, working opt-out honoured immediately and permanently,
suppression list shared across every campaign and domain rather than per campaign.
