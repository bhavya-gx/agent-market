# Security

Agent Market is plain text: one instruction file and one JSON list. It runs no code on your computer, sends no data anywhere, and has no accounts or tracking.

## How the catalog stays clean
- Every change arrives as a pull request and needs the maintainer's approval before it merges.
- An automated check rejects entries with links in text fields, markup, hidden characters, link shorteners, or text that reads like instructions to an AI.
- Outside contributors can only edit `agent-market/catalog/agents.json`.

## Reporting a problem
If you find a listing that is false, promotional, or tries to steer the AI, open an issue or use GitHub's private vulnerability reporting on this repo.
