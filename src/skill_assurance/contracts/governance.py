from __future__ import annotations
from pathlib import Path
import yaml
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
class Strict(BaseModel): model_config=ConfigDict(extra="forbid")
class RiskTier(str,Enum): low="low"; medium="medium"; high="high"; critical="critical"
class ExecutionMode(str,Enum): shadow="shadow"; enforce="enforce"
class Skill(Strict): name:str; risk_tier:RiskTier
class CapabilitiesPolicy(Strict): allow:list[str]=Field(default_factory=list); require_approval:list[str]=Field(default_factory=list); deny:list[str]=Field(default_factory=list)
class AuthorityPolicy(Strict): precedence:list[str]=Field(default_factory=list)
class Evidence(Strict): required_for:list[str]=Field(default_factory=list); abstain_on_unsupported:bool=True
class Trajectory(Strict): required_before:dict[str,list[str]]=Field(default_factory=dict)
class Approval(Strict): ttl_seconds:int=0; bind_subject_version:bool=True; bind_arguments:bool=True
class ExecutionPolicy(Strict): mode:ExecutionMode=ExecutionMode.enforce
class GovernanceFile(Strict): skill:Skill; capabilities:CapabilitiesPolicy; authority:AuthorityPolicy; evidence:Evidence; trajectory:Trajectory; approval:Approval; execution:ExecutionPolicy
SkillGovernance=GovernanceFile
def load_governance(path: str|Path)->GovernanceFile: return GovernanceFile.model_validate(yaml.safe_load(Path(path).read_text(encoding="utf8")))
