# Re: "4 inboxes on one domain, 25/day each — is that safe?"

No. That's 100 sends/day on one domain, and the domain — not the individual inbox — is
where reputation is actually scored.

**The mechanism:** each inbox "looks" safe in isolation (25/day is inside the normal
15-25/inbox range), but mailbox providers evaluate volume and reputation substantially at
the domain level. Four inboxes each sending a compliant-looking 25 still puts 100/day of
aggregate volume on one domain, and the working ceiling there is roughly **30-50/day per
domain** — you're at 2-3x that. This is the most common way a technically conservative
setup still burns: everything checks out per-mailbox while the domain is silently
carrying double or triple what it should, and nothing warns you until reply rate falls
and the damage is already done.

**The fix is not fewer sends per inbox — it's more domains, not more mailboxes on the
one you have.** Adding mailboxes to a domain doesn't add capacity, it just splits the
same budget across more senders. Size it from the domain down:

```
target sends/day  ÷  40 per domain  =  domains needed
domains  ×  2-3 mailboxes           =  total mailboxes
```

For your case: if 100/day total is the real target, that's ~3 domains (100 ÷ 40 ≈ 2.5,
round up), at 2-3 mailboxes each, sending roughly 15-20/inbox — inside both the per-inbox
and per-domain ceilings. If you want to keep exactly these 4 inboxes, split them across
2 domains (2 inboxes/domain) rather than 1, which brings each domain to ~50/day — still
at the edge, so I'd lean toward 3 domains rather than 2 if the volume is fixed.

One more thing worth flagging: each of those domains needs its own SPF/DKIM/DMARC and a
full 14-day-minimum warmup before it carries live volume — don't just repoint the
existing mailboxes at new domains without warming them first, or you'll trade a domain
problem for a fresh cold-start problem.
