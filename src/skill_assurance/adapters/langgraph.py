class LangGraphAdapter:
 """Optional adapter: returns an interrupt-shaped review payload without importing LangGraph."""
 def review_interrupt(self, thread_id, decision): return {"thread_id":thread_id,"interrupt":decision=="REVIEW","decision":decision}
 def resume(self, thread_id, approval): return {"thread_id":thread_id,"resume":approval}
