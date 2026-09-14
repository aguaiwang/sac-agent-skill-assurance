# Source audit

| Source | Role | Classification | Public handling |
|---|---|---|---|
| `ai-service/skills/loader.py:DispatchRiskSkillRuntime` | Registry/package loader | SAC adapter | Describe only; no frozen package copied |
| `ai-service/skills/v2_runtime.py:DispatchRiskGateV2Runtime` | Gate/review composition | Generic pattern + SAC adapter | Map decisions in sanitized pack |
| `ai-service/skills/v2_runtime.py:EvidenceOnlyProductionAdapter` | Raw/trusted evidence boundary | Generic core | Reimplemented minimal interface |
| `ai-service/agents/knowledge_agent.py:KnowledgeEvidence` | Evidence model | Generic contract | Sanitized contract |
| `ai-service/agent/hitl_v2.py` | Pending approval lifecycle | Generic pattern | Approval fingerprint contract |
| `ai-service/agent/observability_v2.py:TraceRecorder` | Trace events | Generic core | JSONL trace sink |
| `backend/planning/*` | SAC authority/validator | SAC-only | External adapter boundary; not copied |

Private URLs, credentials, real IDs, local paths, corpus and runtime data are excluded.
