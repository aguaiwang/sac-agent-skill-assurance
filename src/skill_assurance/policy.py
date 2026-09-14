from __future__ import annotations
from typing import Protocol
from .contracts.models import Capability, ExecutionPrincipal, PolicyDecision, SkillDescriptor
class PolicyBackend(Protocol):
 def evaluate(self, skill:SkillDescriptor, principal:ExecutionPrincipal, capability:Capability, *, approval_valid:bool=False)->PolicyDecision: ...
class BuiltinPolicyBackend:
 def __init__(self, governance=None): self.governance=governance
 def evaluate(self, skill, principal, capability, *, approval_valid=False):
  value=capability.value if hasattr(capability,"value") else str(capability)
  g=self.governance
  if g:
   if value in g.capabilities.deny: return PolicyDecision.DENY
   if value not in set(g.capabilities.allow)|set(g.capabilities.require_approval): return PolicyDecision.DENY
   if value not in principal.scopes and "*" not in principal.scopes: return PolicyDecision.DENY
   if value in g.capabilities.require_approval and not approval_valid: return PolicyDecision.REVIEW
   return PolicyDecision.ALLOW
  if value not in principal.scopes and "*" not in principal.scopes: return PolicyDecision.DENY
  if skill.risk_tier in {"high","critical"} and value=="execute" and not approval_valid: return PolicyDecision.REVIEW
  return PolicyDecision.ALLOW
class ACSBackend:
 """Experimental extension point; ACS is not bundled or release-certified."""
 def __init__(self, client): self.client=client
 def evaluate(self, skill, principal, capability, *, approval_valid=False): return self.client.evaluate(skill, principal, capability, approval_valid=approval_valid)
class CapabilityResolver:
 def __init__(self, backend:PolicyBackend|None=None): self.backend=backend or BuiltinPolicyBackend()
 def resolve(self, skill, principal, capability, *, approval_valid=False): return self.backend.evaluate(skill,principal,capability,approval_valid=approval_valid)
