# Threat model

Controls address prompt and indirect injection, malicious skill references, capability escalation, confused deputy/cross-user access, approval replay and TOCTOU, unsupported evidence/citation laundering, trajectory bypass, duplicate execution, and action loops. Enforcement is deterministic at the runtime boundary; LLM output cannot override authority facts.
