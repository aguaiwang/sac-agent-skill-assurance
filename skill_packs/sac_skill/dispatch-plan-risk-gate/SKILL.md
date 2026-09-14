---
name: dispatch-plan-risk-gate
description: Sanitized SAC dispatch candidate risk-gate adapter.
license: MIT
compatibility: Agent Skills compatible
metadata: {version: 1.0.0}
---

# SAC Dispatch Risk Gate

## Purpose and use

Assess a sanitized energy-dispatch candidate before approval. Use only when candidate, validator, active-lineage, and constraint facts come from an authoritative adapter. Do not create or activate a plan, write a device, or write a database.

## Inputs and workflow

Read authoritative candidate, active plan, constraint, and validator facts; validate lineage and required milestones; evaluate deterministic findings; map PASS/REVIEW/BLOCK to ALLOW/REVIEW/DENY; then bind any later activation to a human approval and pre-execution revalidation.

## Authority, evidence, capabilities, and approval

Backend runtime and validator facts outrank evidence and generated explanation. Evidence can inform domain knowledge but cannot change the gate. The pack may read state and validation and perform review; direct plan/device/database writes are denied. Plan activation requires a bound, unconsumed, unexpired approval.

## Outputs, failures, and edge cases

Return a gate decision, deterministic findings, and trace. Unavailable authority, stale lineage, ownership changes, missing milestones, and invalid approval fail closed. Example: “gate this pending dispatch candidate”; not “activate the plan”.
