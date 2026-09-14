---
name: change-request-review
description: Review a change request using authoritative facts and supported evidence.
license: MIT
compatibility: Agent Skills compatible
metadata: {version: 1.0.0}
---

# Change Request Review

## Purpose and use

Explain an already selected change request after subject and validation facts are available. Do not use for execution, approval, or creating a request.

## Inputs and workflow

Inputs are a principal, versioned subject, runtime and validator facts, and optional raw evidence. Read authoritative facts first; compare the proposed and baseline state; filter raw evidence into trusted evidence; then return findings and an explanation. Unsupported domain or identifier claims are `INSUFFICIENT` and have no citation.

## Authority, capabilities, and approval

Runtime, validator, and policy facts outrank evidence and generated prose. This pack is read/review-only, has no direct-write capability, and cannot replace approval or the risk gate.

## Outputs, failures, and edge cases

Return structured findings, a review explanation, trusted citations, and a trace. Missing authority, stale subject versions, or evidence without support must fail closed or abstain. Example: “review change CR-42 against its baseline”; not “execute CR-42”.
