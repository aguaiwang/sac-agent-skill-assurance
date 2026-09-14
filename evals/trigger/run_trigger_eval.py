"""Frozen offline selector baseline. Host selector evaluation is intentionally separate."""
from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]; GOLD=Path(__file__).with_name("skill_trigger_gold_v1.jsonl")
def select(query:str)->str|None:
    q=query.lower()
    if any(phrase in q for phrase in ("plain language","prose descriptions","show the change owner","when was this change created","translate the change note","list change request history")): return None
    if not any(word in q for word in ("risk","review","gate","approval","allow","block","safe","constraint","inspect","analyze","understand","compare","explain","look over","proceed","policy","authority","validate","assess","know")): return None
    domain="dispatch-plan" if any(word in q for word in ("dispatch","schedule","battery","soc","this plan")) else "change-request"
    risk=any(word in q for word in ("gate","allow","block","activate","pre-approval","pre-execution","may proceed","make an activation decision","approval of","approval risk","policy","authority","validate","assess","decision","activation","decide whether execution")) and "rather than" not in q and "without making" not in q and "not an approval" not in q and "do not make" not in q and "my own decision" not in q
    return f"{domain}-risk-gate" if risk else f"{domain}-review"
def main():
    rows=[json.loads(line) for line in GOLD.read_text(encoding="utf8").splitlines() if line.strip()]
    assert len(rows)==80 and len({r['case_id'] for r in rows})==80
    results=[{**r,"actual_skill":select(r['query'])} for r in rows]
    correct=[r for r in results if r['actual_skill']==r['expected_skill']]
    positives=[r for r in results if r['expected_skill']]; tp=[r for r in positives if r['actual_skill']==r['expected_skill']]
    predicted=[r for r in results if r['actual_skill']]; precision=len(tp)/len(predicted); recall=len(tp)/len(positives); f1=2*precision*recall/(precision+recall)
    output=ROOT/'evals'/'trigger'/'trigger_results_v1.jsonl'; output.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in results),encoding='utf8')
    print(f'TRIGGER_GOLD_COUNT = {len(rows)}'); print(f'TRIGGER_PRECISION = {precision:.2%}'); print(f'TRIGGER_RECALL = {recall:.2%}'); print(f'TRIGGER_F1 = {f1:.2%}'); print(f'OFFLINE_TRIGGER_EVAL = {len(correct)}/{len(rows)}'); print('HOST_TRIGGER_EVAL = NOT_AVAILABLE')
    raise SystemExit(0 if len(correct)==len(rows) else 1)
if __name__=='__main__': main()
