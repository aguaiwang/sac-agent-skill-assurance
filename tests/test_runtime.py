from datetime import datetime, timedelta, timezone

from skill_assurance.authority import AuthorityResolver
from skill_assurance.contracts.models import *
from skill_assurance.evidence import EvidenceSupportFilter, IdentifierMatcher
from skill_assurance.runtime import AssuranceRuntime, ReplayRunner
from skill_assurance.skills.loader import SkillPackageLoader
from pathlib import Path


def setup(user="user-a", tenant="tenant-a", subject_id="subject-a", version="1"):
    principal=ExecutionPrincipal(user_id=user,agent_id="agent-a",tenant_id=tenant,scopes={"execute","read","review"})
    skill=SkillDescriptor(name="change-request-review",risk_tier="high")
    subject=DomainSubject(id=subject_id,version=version,owner_id=user,tenant_id=tenant)
    return principal,skill,subject


def grant_for(runtime, principal, skill, subject, action="execute", args=None, **changes):
    request=ApprovalRequest(principal=principal,skill=skill.name,subject_id=subject.id,subject_version=subject.version,action=action,normalized_args=args or {})
    fields={**request.model_dump(),"approval_id":"approval-"+subject.id,"expires_at":datetime.now(timezone.utc)+timedelta(minutes=5),**changes}
    grant=ApprovalGrant(**fields)
    runtime.approval_store.issue(grant)
    return grant


def test_approval_trajectory_and_single_use():
    p,s,sub=setup(); runtime=AssuranceRuntime(); ctx=runtime.new_context(p,s,sub)
    assert runtime.execute(ctx,s,sub,"execute",{},["validation.pass"]) is PolicyDecision.DENY
    runtime.complete(ctx,"validation.pass"); grant=grant_for(runtime,p,s,sub)
    assert runtime.execute(ctx,s,sub,"execute",{},["validation.pass"],grant) is PolicyDecision.ALLOW
    assert runtime.execute(ctx,s,sub,"execute",{},["validation.pass"],grant) is PolicyDecision.DENY


def test_context_milestone_and_duplicate_are_isolated():
    p,s,sub=setup(); runtime=AssuranceRuntime(); a=runtime.new_context(p,s,sub); b=runtime.new_context(p,s,sub)
    runtime.complete(a,"validated")
    assert "validated" not in b.completed_milestones
    assert runtime.execute(b,s,sub,"read-action",{},["validated"],capability=Capability.READ) is PolicyDecision.DENY
    assert runtime.execute(a,s,sub,"read-action",{},["validated"],capability=Capability.READ) is PolicyDecision.ALLOW
    assert runtime.execute(b,s,sub,"read-action",{},[],capability=Capability.READ) is PolicyDecision.ALLOW


def test_cross_user_and_tenant_isolation():
    p,s,sub=setup(); runtime=AssuranceRuntime(); outsider,_,_=setup(user="user-b"); other_tenant,_,_=setup(user="user-a",tenant="tenant-b")
    assert runtime.execute(runtime.new_context(outsider,s,sub),s,sub,"read",{},capability=Capability.READ) is PolicyDecision.DENY
    assert runtime.execute(runtime.new_context(other_tenant,s,sub),s,sub,"read",{},capability=Capability.READ) is PolicyDecision.DENY


def test_approval_binding_and_stale_protection():
    p,s,sub=setup(); runtime=AssuranceRuntime(); ctx=runtime.new_context(p,s,sub); runtime.complete(ctx,"validated")
    expired=grant_for(runtime,p,s,sub,expires_at=datetime.now(timezone.utc)-timedelta(seconds=1))
    assert runtime.execute(ctx,s,sub,"execute",{},["validated"],expired) is PolicyDecision.REVIEW
    live=grant_for(runtime,p,s,sub)
    changed=sub.model_copy(update={"version":"2"})
    assert runtime.execute(ctx,s,changed,"execute",{},["validated"],live) is PolicyDecision.REVIEW
    fresh=grant_for(runtime,p,s,sub,args={"limit":1})
    assert runtime.execute(ctx,s,sub,"execute",{"limit":2},["validated"],fresh) is PolicyDecision.REVIEW


def test_adapter_revalidation_and_shadow_trace():
    class Changed:
        def revalidate_before_execute(self, context, subject): return False
    p,s,sub=setup(); runtime=AssuranceRuntime(); ctx=runtime.new_context(p,s,sub); runtime.complete(ctx,"validated"); g=grant_for(runtime,p,s,sub)
    assert runtime.execute(ctx,s,sub,"execute",{},["validated"],g,Changed()) is PolicyDecision.REVIEW
    shadow=AssuranceRuntime(mode="shadow"); sc=shadow.new_context(p,s,sub)
    assert shadow.execute(sc,s,sub,"read",{},capability=Capability.READ) is PolicyDecision.ALLOW
    assert any(e.data.get("would_decision")=="ALLOW" for e in sc.trace_events)


def test_identifier_matching_and_no_evidence_abstention():
    matcher=IdentifierMatcher()
    assert matcher.matches("IEC61850-21", "IEC 61850-21 applies")
    assert matcher.matches("GB/T36549-2018", "GB/T 36549-2018")
    assert matcher.matches("BAT E425", "BAT-E425")
    assert not matcher.matches("BAT E999", "BAT E425 and BAT E426")
    assert matcher.matches("HOME-ESS-HV", "HOME ESS HV")
    assert not matcher.matches("HOME-ESS-X99", "HOME-ESS-HV")
    assert matcher.matches("V1.1", "version 1.1") and not matcher.matches("V1.5", "V1.1")
    status,items=EvidenceSupportFilter().decide(Claim(type=ClaimType.identifier_fact,text="claim",identifier="BAT-E999"),[RawEvidence(content="BAT E425",source="doc",citation="x")])
    assert status=="INSUFFICIENT" and not items


def test_authority_precedence_and_experimental_replay():
    facts=[AuthorityFact(source=AuthoritySource.GENERATIVE_REASONING,key="gate",value="ALLOW"),AuthorityFact(source=AuthoritySource.POLICY_GATE,key="gate",value="DENY"),AuthorityFact(source=AuthoritySource.TRUSTED_EVIDENCE,key="model",value="A"),AuthorityFact(source=AuthoritySource.VALIDATOR,key="model",value="B")]
    canonical, conflicts=AuthorityResolver().resolve(facts,[AuthoritySource.DOMAIN_RUNTIME,AuthoritySource.VALIDATOR,AuthoritySource.POLICY_GATE,AuthoritySource.TRUSTED_EVIDENCE,AuthoritySource.GENERATIVE_REASONING])
    assert canonical["gate"].value=="DENY" and canonical["model"].value=="B" and conflicts
    assert ReplayRunner().replay([],AssuranceRuntime())["status"]=="EXPERIMENTAL_NO_POLICY_REPLAY"


def test_all_four_skill_packages_validate():
    root=Path(__file__).resolve().parents[1] / "skill_packs"
    packages=[SkillPackageLoader.load(path) for group in sorted(root.iterdir()) if group.is_dir() for path in sorted(group.iterdir()) if path.is_dir()]
    assert len(packages)==4
    assert all(package.references.is_dir() for package in packages)
    assert {package.descriptor.name for package in packages}=={"change-request-risk-gate","change-request-review","dispatch-plan-risk-gate","dispatch-plan-review"}
