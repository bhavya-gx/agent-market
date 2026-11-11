# Adding or updating an agent

1. Fork the repo and edit `agent-market/catalog/agents.json`.
2. Fill every field from the agent's **official site only**. No review blogs, no affiliate pages.
3. Set `verification.status`:
   - `page_read`: you read the official page. Add today's date as `checked_on`.
   - `blocked`: the site would not load for you.
   - `unchecked`: you are adding it from memory. A maintainer will check it.
4. Run `python3 scripts/validate.py` and fix anything it reports.
5. Open a pull request with the page you read in the description.

## What we never accept
- Payment, sponsorship or affiliate links in exchange for listing or ranking.
- Claims we can't trace to the vendor's own page.

If you work for the company you are listing, say so in the PR.
