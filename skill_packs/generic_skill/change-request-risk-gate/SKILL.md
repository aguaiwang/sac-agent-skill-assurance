---
name: change-request-risk-gate
description: Deterministically assess a change request before execution.
license: MIT
compatibility: Agent Skills compatible
metadata: {version: 1.0.0}
---

# Change Request Risk Gate

## Purpose and use

Deterministically assess a selected change before execution. Use only when owner, version, risk, and validation facts exist. Do not execute a change, manufacture approval, or bypass a domain action guard.

## Inputs and workflow

Inputs are the principal, versioned subject, validator result, authority facts, and optional supported evidence. Validate identity and lineage; apply required milestones; evaluate governance capabilities; emit `ALLOW`, `REVIEW`, or `DENY`; then require a separately bound human approval and pre-execution revalidation for any execute action.

## Authority, evidence, and approval

Runtime and validator facts outrank evidence; evidence never overrides a failing validator. Capabilities and the governance sidecar define permitted actions. Approval is bound to principal, subject version, action, normalized arguments, expiry, and single use.

## Outputs, failures, and edge cases

Return the gate decision, reasons, and trace without database or external side effects. Missing validation, stale state, changed ownership, invalid approval, or unsupported evidence produces `REVIEW`/`DENY`. Example: “gate this validated configuration change”; not “apply it now”.
