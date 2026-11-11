# Using Agent Market in ChatGPT

ChatGPT does not load skill folders, so set it up as a Custom GPT or a Project.

## Custom GPT
1. In ChatGPT, open Explore GPTs and choose Create, then Configure.
2. Name: Agent Market.
3. Instructions: paste everything in `../agent-market/SKILL.md` below the second `---` line.
4. Knowledge: upload `../agent-market/catalog/agents.json`.
5. Turn off web browsing if you want answers to come only from the catalog.

## Project
Create a Project, paste the same instructions into its instructions box, and add `agents.json` as a project file. Every chat in that project can then recommend agents.
