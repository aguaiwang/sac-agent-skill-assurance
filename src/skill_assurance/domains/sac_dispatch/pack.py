from ...contracts.models import *
def map_sac_gate(decision:str)->GateDecision: return {"PASS":GateDecision.ALLOW,"REVIEW":GateDecision.REVIEW,"BLOCK":GateDecision.DENY}[decision]
def sanitized_candidate(plan_id="candidate-demo",version="1",owner_id="demo-user",tenant_id="demo-tenant") -> DomainSubject:
 return DomainSubject(id=plan_id,version=version,owner_id=owner_id,tenant_id=tenant_id,attributes={"status":"PENDING_APPROVAL","validator":"PASS","delta":"sanitized"})
