from ..runtime import AssuranceRuntime
class PlainPythonAdapter:
 def __init__(self,runtime=None): self.runtime=runtime or AssuranceRuntime()
 def run(self,*args,**kwargs): return self.runtime.execute(*args,**kwargs)
