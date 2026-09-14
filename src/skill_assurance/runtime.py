from __future__ import annotations
from datetime import datetime, timezone
from .contracts.models import *
from dataclasses import dataclass, field
from uuid import uuid4
from typing import Protocol, Any
from .policy import CapabilityResolver
@dataclass
class AssuranceRunContext:
 run_id:str; task_id:str; principal:ExecutionPrincipal; skill_name:str; skill_version:str; subject_id:str; subject_version:str
 completed_milestones:set[str]=field(default_factory=set); executed_actions:set[str]=field(default_factory=set); approval_state:dict=field(default_factory=dict); trace_events:list=field(default_factory=list)
class ApprovalStore(Protocol):
 def issue(self,grant:ApprovalGrant)->ApprovalGrant: ...
 def lookup(self,approval_id:str)->ApprovalGrant|None: ...
 def consume(self,approval_id:str)->bool: ...
 def invalidate(self,approval_id:str)->bool: ...
class InMemoryApprovalStore:
 def __init__(self): self.items={}
 def issue(self,grant): self.items[grant.approval_id]=grant; return grant
 def lookup(self,approval_id): return self.items.get(approval_id)
 def consume(self,approval_id):
  g=self.items.get(approval_id)
  if not g or g.consumed: return False
  self.items[approval_id]=g.model_copy(update={"consumed":True}); return True
 def invalidate(self,approval_id):
  g=self.items.get(approval_id)
  if not g:return False
  self.items[approval_id]=g.model_copy(update={"consumed":True}); return True
class AssuranceRuntime:
 def __init__(self, resolver=None, mode="enforce", approval_store=None): self.resolver=resolver or CapabilityResolver(); self.mode=mode; self.approval_store=approval_store or InMemoryApprovalStore()
 def new_context(self,principal,skill,subject,task_id=None): return AssuranceRunContext(uuid4().hex,task_id or uuid4().hex,principal,skill.name,skill.version,subject.id,subject.version)
 def trace(self,context,event,**data):
  row=TraceEvent(event=event,data={"run_id":context.run_id,**data}); context.trace_events.append(row); return row
 def activate(self, context, skill, capability):
  self.trace(context,"skill_activation_requested",skill=skill.name); d=self.resolver.resolve(skill,context.principal,capability); self.trace(context,"policy_decision",decision=d.value,capability=str(capability)); return d
 def complete(self,context,milestone): context.completed_milestones.add(milestone); self.trace(context,"milestone_completed",milestone=milestone)
 def approval_valid(self, grant:ApprovalGrant|None, request:ApprovalRequest):
  now=datetime.now(timezone.utc)
  return bool(grant and not grant.consumed and grant.expires_at>now and grant.fingerprint()==ApprovalGrant(approval_id=grant.approval_id,issued_at=grant.issued_at,expires_at=grant.expires_at,consumed=grant.consumed,**request.model_dump()).fingerprint())
 def execute(self,context:AssuranceRunContext,skill:SkillDescriptor,subject:DomainSubject,action:str,args:dict[str,Any],required=(),grant:ApprovalGrant|None=None,adapter=None,capability:Capability|str|None=None):
  if subject.owner_id!=context.principal.user_id or subject.tenant_id!=context.principal.tenant_id: self.trace(context,"action_denied",reason="identity"); return PolicyDecision.DENY
  required=required or ()
  if any(x not in context.completed_milestones for x in required): self.trace(context,"action_denied",reason="trajectory"); return PolicyDecision.DENY
  key=f"{action}:{sorted(args.items())}"
  if key in context.executed_actions: self.trace(context,"action_denied",reason="duplicate"); return PolicyDecision.DENY
  request=ApprovalRequest(principal=context.principal,skill=skill.name,subject_id=subject.id,subject_version=subject.version,action=action,normalized_args=args)
  stored=self.approval_store.lookup(grant.approval_id) if grant else None
  valid=bool(grant and stored and not stored.consumed and self.approval_valid(stored,request))
  if adapter and not adapter.revalidate_before_execute(context,subject): self.trace(context,"action_denied",reason="revalidation"); return PolicyDecision.REVIEW
  requested_capability=capability or Capability.EXECUTE
  d=self.resolver.resolve(skill,context.principal,requested_capability,approval_valid=valid); self.trace(context,"policy_decision",would_decision=d.value,capability=str(requested_capability))
  if self.mode=="shadow": self.trace(context,"action_executed",action=action,shadow=True); return PolicyDecision.ALLOW
  if d is PolicyDecision.ALLOW:
   context.executed_actions.add(key); self.approval_store.consume(grant.approval_id) if grant else None; self.trace(context,"action_executed",action=action); return d
  self.trace(context,"action_denied",reason=d.value); return d
class JSONLTraceSink(list):
 def write(self,path):
  from pathlib import Path
  Path(path).write_text("".join(x.model_dump_json()+"\n" for x in self),encoding="utf8")
class ReplayRunner:
 def replay(self, events, runtime):
  """Experimental only: traces lack a complete immutable policy snapshot."""
  return {"status":"EXPERIMENTAL_NO_POLICY_REPLAY","events":len(events)}
