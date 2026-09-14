# GitHub publishing

Recommended repository name: `agent-skill-assurance`

Description: Reusable governance and assurance runtime for Agent Skills with capability control, domain authority, evidence grounding, approval binding and trajectory policies.

Suggested topics: `agent-skills`, `ai-agents`, `agent-governance`, `langgraph`, `rag`, `llm`, `human-in-the-loop`, `agent-evaluation`, `ai-safety`, `python`.

Create the GitHub repository first, then initialize and tag the extracted public package:

```bash
git init
git branch -M main
git add .
git commit -m "release: agent skill assurance runtime v1.0.0"
git tag v1.0.0
```

After creating a repository, replace the placeholder with its actual URL:

```bash
git remote add origin <USER_GITHUB_REPOSITORY_URL>
git push -u origin main
git push origin v1.0.0
```

Do not claim a bundled ACS, MCP firewall, production router, or Host-selector runtime evaluation. Trigger metrics are frozen offline-Gold results.
