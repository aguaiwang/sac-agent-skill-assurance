# Agent Skill Assurance Runtime V1.0 Release Report

## Scope and boundary

This is a public, framework-neutral assurance runtime. It contains no private SAC trajectory data, production endpoints, credentials, customer identifiers, local paths, model weights, or corpus material. Public V1.0 readiness is independent from the private SAC Agent Final Freeze, which remains **NO**.

## Executed release gates

| Gate | Result | Evidence |
| --- | --- | --- |
| Editable installation | PASS | `pip install -e .` |
| Public core tests | PASS, 8 passed | `pytest -q` |
| Skill package + governance validation | PASS, 4/4 | loader test |
| Generic demo | PASS | `examples/generic_demo.py` |
| Sanitized SAC mock demo | PASS | `examples/sac_demo.py` |
| Security Gold | PASS, 52/52 | `evals/security/run_security_eval.py` |
| Trigger Gold | PASS, 80/80 | `evals/trigger/run_trigger_eval.py` |
| Private SAC targeted regression | PASS, 33 passed | skill, integration, HITL, evidence-adapter tests |
| Private SAC Skill Agent HTTP E2E | PASS, 20/20 | `dispatch-plan-risk-review/evaluation/run_real_e2e.py` |

Security Gold comprises 52 distinct JSONL fixtures rather than repeated parametrization. It covers identity/ownership, approvals, trajectory bypass, escalation, citations, identifiers, injection, TOCTOU, duplicate execution, shadow, authority, invalid governance, and isolation.

The Trigger Gold is frozen at 80 cases: 20 per pack (8 positive, 8 negative, 4 near-neighbor), with 60 calibration cases and 20 blind cases. The offline baseline records 100.00% precision, recall, and F1. Host-selector evaluation is `NOT_AVAILABLE`; this offline result must not be presented as a host-runtime score.

The first HTTP attempt is excluded from scoring because it inherited a single-user Replan quota key from prior local evaluation activity. The clean rerun used the existing SAC baseline and isolated that exact test quota key (no Redis-wide flush); it passed all 20 HTTP Agent → Replan → Validator → Candidate Review cases.

## Claim audit

| Capability | Status |
| --- | --- |
| Typed contracts / governance / policy | IMPLEMENTED |
| RunContext isolation / approval store / revalidation | IMPLEMENTED |
| Evidence support / identifier normalization | IMPLEMENTED |
| Authority precedence / shadow would-decision trace | IMPLEMENTED |
| LangGraph adapter | EXTENSION POINT |
| ACS backend | EXPERIMENTAL EXTENSION POINT |
| Replay | EXPERIMENTAL / ROADMAP |

## Known limitations

- Generic replay is explicitly experimental: trace-only replay lacks an immutable governance and domain snapshot.
- The package does not claim a bundled ACS or a live LangGraph integration.
- Private SAC Agent Final Freeze is not changed by this public release.

## Release conclusion

`PUBLIC_RELEASE_V1_0 = READY` for the public package release gates listed above. The artifact is `dist/agent-skill-assurance-v1.0.0.zip`.
