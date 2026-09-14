from __future__ import annotations
import re
from typing import Protocol
from .contracts.models import Claim, ClaimType, RawEvidence, TrustedEvidence
class IdentifierExtractor:
 def __init__(self, patterns:dict[str,str]|None=None): self.patterns=patterns or {"standard":r"\b(?:IEC|ISO|EN|GB\s*/\s*T)[\s-]*\d+(?:[\s-]*\d+)?\b","model":r"\b(?:[A-Z][A-Z0-9]+(?:-[A-Z0-9]+)+|[A-Z][A-Z0-9]+(?:\s+[A-Z0-9]+){1,2})\b","error":r"\b(?:ERR|E|BAT)[-_\s]?\d{3,}\b","document_version":r"\bV?\d+\.\d+(?:\.\d+)?\b"}
 def extract(self,text): return [(k,m.group(0)) for k,p in self.patterns.items() for m in re.finditer(p,text,re.I)]
class IdentifierNormalizer:
 def normalize(self,value:str)->str:
  normalized=re.sub(r"[^A-Z0-9]","",value.upper())
  return normalized[1:] if re.fullmatch(r"V\d+",normalized) else normalized
class IdentifierMatcher:
 def __init__(self,extractor:IdentifierExtractor|None=None,normalizer:IdentifierNormalizer|None=None): self.extractor=extractor or IdentifierExtractor(); self.normalizer=normalizer or IdentifierNormalizer()
 def matches(self,identifier:str,evidence_text:str)->bool:
  target=self.normalizer.normalize(identifier)
  return any(self.normalizer.normalize(found)==target for _,found in self.extractor.extract(evidence_text))
class EvidenceSupportStrategy(Protocol):
 def supports(self,claim:Claim,item:RawEvidence)->bool: ...
class IdentifierSupportStrategy:
 def __init__(self,matcher:IdentifierMatcher|None=None): self.matcher=matcher or IdentifierMatcher()
 def supports(self,claim,item): return bool(claim.identifier and self.matcher.matches(claim.identifier,item.content+" "+item.source))
class TextSupportStrategy:
 def supports(self,claim,item):
  tokens=set(re.findall(r"[A-Za-z0-9]{3,}",(claim.text or "").lower()))
  return bool(tokens and tokens.issubset(set(re.findall(r"[A-Za-z0-9]{3,}",(item.content+" "+item.source).lower()))))
class EvidenceSupportFilter:
 def __init__(self,identifier_strategy:IdentifierSupportStrategy|None=None,text_strategy:TextSupportStrategy|None=None): self.identifier_strategy=identifier_strategy or IdentifierSupportStrategy(); self.text_strategy=text_strategy or TextSupportStrategy()
 def support(self, claim:Claim, raw:list[RawEvidence])->list[TrustedEvidence]:
  out=[]
  for item in raw:
   strategy=self.identifier_strategy if claim.type is ClaimType.identifier_fact or claim.identifier else self.text_strategy
   if item.citation and strategy.supports(claim,item): out.append(TrustedEvidence(**item.model_dump(),supported_claims=[claim.text]))
  return out
 def decide(self, claim, raw):
  trusted=self.support(claim,raw)
  return ("SUPPORTED",trusted) if trusted else ("INSUFFICIENT",[])
