from pathlib import Path
import re
import yaml
from .package import SkillPackage
from ..contracts.governance import load_governance
from ..contracts.models import SkillDescriptor
class SkillPackageLoader:
 @staticmethod
 def load(path):
  root=Path(path); md=root/'SKILL.md'; gov=root/'governance.yaml'
  if not md.is_file() or not gov.is_file(): raise ValueError('managed skill requires SKILL.md and governance.yaml')
  match=re.match(r'^---\s*\n(.*?)\n---',md.read_text(encoding='utf8'),re.S)
  if not match: raise ValueError('invalid Agent Skills frontmatter')
  front=yaml.safe_load(match.group(1)) or {}; allowed={'name','description','license','compatibility','metadata'}
  if set(front)-allowed or not isinstance(front.get('name'),str) or not isinstance(front.get('description'),str): raise ValueError('unsupported or missing frontmatter')
  governance=load_governance(gov)
  if governance.skill.name!=front['name']: raise ValueError('skill name mismatch')
  return SkillPackage(root,SkillDescriptor(name=front['name'],version=str((front.get('metadata')or{}).get('version','1.0.0')),risk_tier=governance.skill.risk_tier.value,mode=governance.execution.mode.value),md,governance,root/'references',(root/'scripts') if (root/'scripts').exists() else None,(root/'assets') if (root/'assets').exists() else None)
