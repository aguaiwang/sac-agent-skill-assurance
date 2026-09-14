from ...contracts.models import *
def risk_gate(subject:DomainSubject, validation:ValidationResult)->ReviewDecision:
 if not validation.passed: return ReviewDecision(decision=GateDecision.DENY,reason="validation failed")
 if subject.attributes.get("risk") in {"high","critical"}: return ReviewDecision(decision=GateDecision.REVIEW,reason="approval required")
 return ReviewDecision(decision=GateDecision.ALLOW,reason="low risk validated")
