from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
import json
from typing import Any
from pydantic import BaseModel, ConfigDict, Field

class StrictModel(BaseModel): model_config = ConfigDict(extra="forbid")
class Capability(str, Enum): READ="read"; REVIEW="review"; EXECUTE="execute"; APPROVE="approve"
class PolicyDecision(str, Enum): ALLOW="ALLOW"; REVIEW="REVIEW"; DENY="DENY"
class GateDecision(str, Enum): ALLOW="ALLOW"; REVIEW="REVIEW"; DENY="DENY"
class AuthoritySource(str, Enum): DOMAIN_RUNTIME="DOMAIN_RUNTIME"; VALIDATOR="VALIDATOR"; POLICY_GATE="POLICY_GATE"; TRUSTED_EVIDENCE="TRUSTED_EVIDENCE"; GENERATIVE_REASONING="GENERATIVE_REASONING"
class ClaimType(str, Enum): runtime_fact="runtime_fact"; domain_fact="domain_fact"; identifier_fact="identifier_fact"; policy_fact="policy_fact"; generated_explanation="generated_explanation"
class ExecutionPrincipal(StrictModel): user_id:str; agent_id:str; tenant_id:str; session_id:str|None=None; roles:set[str]=set(); scopes:set[str]=set()
class SkillDescriptor(StrictModel): name:str; version:str="1"; risk_tier:str="low"; mode:str="enforce"
class DomainSubject(StrictModel): id:str; version:str; owner_id:str; tenant_id:str; attributes:dict[str, Any]=Field(default_factory=dict)
class DomainRuntimeState(StrictModel): subject_id:str; subject_version:str; facts:dict[str, Any]=Field(default_factory=dict)
class ValidationResult(StrictModel): passed:bool; reasons:list[str]=Field(default_factory=list)
class ChangeDelta(StrictModel): subject_id:str; before_version:str; after_version:str; changes:dict[str, Any]=Field(default_factory=dict)
class AuthorityFact(StrictModel): source:AuthoritySource; key:str; value:Any
class RawEvidence(StrictModel): content:str; source:str; citation:str|None=None; score:float=0
class TrustedEvidence(RawEvidence): supported_claims:list[str]=Field(default_factory=list)
class Claim(StrictModel): type:ClaimType; text:str; identifier:str|None=None
class Citation(StrictModel): source:str; locator:str
class GateFinding(StrictModel): code:str; severity:str; message:str
class ReviewDecision(StrictModel): decision:GateDecision; reason:str; citations:list[Citation]=Field(default_factory=list)
class ApprovalRequest(StrictModel): principal:ExecutionPrincipal; skill:str; subject_id:str; subject_version:str; action:str; normalized_args:dict[str, Any]
class ApprovalGrant(ApprovalRequest):
    approval_id:str
    issued_at:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))
    expires_at:datetime
    consumed:bool=False
    def fingerprint(self)->str: return sha256(json.dumps(self.model_dump(mode="json", exclude={"approval_id","issued_at","expires_at","consumed"}),sort_keys=True).encode()).hexdigest()
class TrajectoryMilestone(StrictModel): name:str
class TraceEvent(StrictModel): event:str; timestamp:datetime=Field(default_factory=lambda:datetime.now(timezone.utc)); data:dict[str, Any]=Field(default_factory=dict)
