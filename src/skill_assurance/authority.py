from .contracts.models import AuthorityFact
class AuthorityResolver:
 def resolve(self,facts,precedence):
  key=lambda source: source.value if hasattr(source,"value") else str(source)
  rank={key(x):i for i,x in enumerate(precedence)}; canonical={}; conflicts=[]
  for fact in facts:
   old=canonical.get(fact.key)
   if old is None or rank.get(key(fact.source),999)<rank.get(key(old.source),999):
    if old and old.value!=fact.value: conflicts.append((fact.key,old,fact))
    canonical[fact.key]=fact
   elif old.value!=fact.value: conflicts.append((fact.key,fact,old))
  return canonical,conflicts
