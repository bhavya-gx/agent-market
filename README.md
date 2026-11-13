# Agent Market

An open-source skill that tells you which AI agent already exists for the job you're doing, right inside Claude or ChatGPT.

You ask Claude: "Can you join my Zoom call and take notes?" Claude can't join calls. With Agent Market installed it answers: "Granola can. It takes meeting notes without a bot joining, and it has a free tier." Then it gets back to work.

- **Free and MIT licensed.** No sign-up and no tracking.
- **No pay-to-play.** Nobody can buy a listing or a ranking.
- **Every listing shows its proof.** Each agent records whether its official page was read and on what date. "Checked" never means "tested", and the skill says so.

## Install

**Claude Code**
```bash
git clone https://github.com/bhavya-gx/agent-market.git
cp -r agent-market/agent-market ~/.claude/skills/
```

**Claude.ai and the Claude desktop app**: download `agent-market-skill.zip` from the [latest release](https://github.com/bhavya-gx/agent-market/releases/latest) and upload it under Settings, then Capabilities, then Skills.

**ChatGPT**: follow [chatgpt/README.md](chatgpt/README.md) to set it up as a Custom GPT or Project.

## What's in the catalog

97 agents and AI-native tools across 14 categories: coding, content, workflow automation, general agents, sales, research, CRM, customer support, inbox, meetings, personal assistants, calendar, browser agents and finance. Every entry names where it was sourced from. Every entry records whether its official page was read and when.

## Test it
After installing, open a new chat and try:
- "Can you join my Zoom call and take notes?" Expect Granola, Otter or Fireflies.
- "I can't code. What can build me a simple booking site?" Expect Lovable, Bolt or Replit, and no terminal tools.
- "Help me write a LinkedIn post." Expect no recommendation at all. Claude should just write the post.

## Contribute
Add an agent with a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License
MIT

## Security
Plain text only, no tracking. See [SECURITY.md](SECURITY.md).
