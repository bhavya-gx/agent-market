# Which Agent

An open-source skill that tells you which AI agent already exists for the job you're doing, right inside Claude or ChatGPT.

You're drafting your tenth follow-up email of the day in a chat. Which Agent notices and says: "Fyxer can draft these in your inbox. Free tier, SOC 2 claimed, page checked 4 Nov 2026." Then it gets back to work.

- **Free and MIT licensed.** No sign-up and no tracking.
- **No pay-to-play.** Nobody can buy a listing or a ranking.
- **Every listing shows its proof.** Each agent records whether its official page was read and on what date. "Checked" never means "tested", and the skill says so.

## Install

**Claude Code**
```bash
git clone https://github.com/OWNER/which-agent.git
cp -r which-agent/which-agent ~/.claude/skills/
```

**Claude.ai and the Claude desktop app**: zip the `which-agent` folder and upload it under Settings, then Capabilities, then Skills.

**ChatGPT**: follow [chatgpt/README.md](chatgpt/README.md) to set it up as a Custom GPT or Project.

## What's in the catalog

30 agents across 10 categories: personal assistants, general agents, inbox, calendar, meetings, content, sales, workflow automation, browser agents and coding. 27 official pages read on 4 Nov 2026. Genspark, Gamma and Lovable blocked the check.

## Ask it things like
- "I spend two hours a day on email. Is there an agent for that?"
- "I can't code. What can build me a simple booking site?"
- "What could I add to Claude to handle my meeting notes?"

## Contribute
Add an agent with a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License
MIT
