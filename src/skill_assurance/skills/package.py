from dataclasses import dataclass
from pathlib import Path
from ..contracts.governance import GovernanceFile
from ..contracts.models import SkillDescriptor
@dataclass(frozen=True)
class SkillPackage:
 root_path:Path; descriptor:SkillDescriptor; instructions_path:Path; governance:GovernanceFile; references:Path; scripts:Path|None; assets:Path|None
