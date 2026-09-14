---
name: dispatch-plan-review
description: Sanitized SAC dispatch candidate review adapter.
license: MIT
compatibility: Agent Skills compatible
metadata: {version: 1.0.0}
---

# SAC Dispatch Review

## Purpose and use

Read-only review of a sanitized dispatch candidate. Use only after Candidate, ValidatorResult, GateResult, PlanDelta, and UserConstraint context exists. Do not activate a plan, write a device, or directly write a database.

## Inputs and workflow

Read backend authority facts and candidate lineage; compare the candidate with the active plan and constraints; include validator and gate findings; conditionally retrieve device or standards knowledge; pass every raw result through evidence support filtering; then produce a recommendation and explanation.

## Authority, evidence, capabilities, and approval

Backend runtime and validator facts outrank evidence and generated explanation. RAG is optional and may support device/standards knowledge only, never runtime facts. Identifier mismatch or no evidence returns `INSUFFICIENT` with zero citations. The capability set is state read, validation read, review, and evidence search; activation is denied.

## Outputs, failures, and edge cases

Return recommendation, explanation, trusted citations, and a structured trace without side effects. Stale candidates, unavailable authority, unsupported evidence, and RAG failure do not fabricate facts or activation claims. Example: “detail-review the pending candidate”; not “activate it”.
