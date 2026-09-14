from datetime import datetime,timedelta,timezone
from skill_assurance.contracts.models import *
from skill_assurance.domains.change_request.pack import risk_gate
from skill_assurance.runtime import AssuranceRuntime
owner=ExecutionPrincipal(user_id="alice",agent_id="demo",tenant_id="acme",scopes={"read","review","execute"})
runtime=AssuranceRuntime(); low=DomainSubject(id="CR-1",version="1",owner_id="alice",tenant_id="acme",attributes={"risk":"low"}); high=DomainSubject(id="CR-2",version="1",owner_id="alice",tenant_id="acme",attributes={"risk":"high"})
print("ALLOW",risk_gate(low,ValidationResult(passed=True)).decision.value); print("REVIEW",risk_gate(high,ValidationResult(passed=True)).decision.value); print("DENY",risk_gate(low,ValidationResult(passed=False)).decision.value)
