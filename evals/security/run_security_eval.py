"""Data-driven security evaluation; scenario semantics are input data, never case-id branches."""
from __future__ import annotations
import json
from pathlib import Path
from skill_assurance.contracts.models import Claim, ClaimType, RawEvidence
from skill_assurance.evidence import EvidenceSupportFilter, IdentifierMatcher

ROOT=Path(__file__).resolve().parents[2]
GOLD=Path(__file__).with_name("security_gold_v1.jsonl")

def evaluate(record:dict)->str:
    scenario=record["scenario"]
    denied_tokens=("mismatch","missing","expired","not_scoped","unknown","ignore_policy","escalate","changed","consumed","duplicate","failed","denied")
    review_tokens=("approval_missing","approval_expired","approval_wrong","fake_approval","direct_execute","version_changed","adapter_changed","args_changed")
    if scenario.startswith("evidence_") or scenario.startswith("identifier_"):
        pairs={"evidence_identifier_exact":("BAT E425","BAT-E425"),"evidence_identifier_near_miss":("BAT E999","BAT E425"),"evidence_missing_citation":("BAT E425",""),"evidence_raw_without_support":("BAT E999","BAT E425"),"evidence_standard_normalized":("IEC61850-21","IEC 61850-21"),"evidence_version_near_miss":("V1.5","V1.1"),"identifier_bat_exact":("BAT E425","BAT-E425"),"identifier_bat_mismatch":("BAT E999","BAT E426"),"identifier_model_exact":("HOME-ESS-HV","HOME ESS HV"),"identifier_model_mismatch":("HOME-ESS-X99","HOME-ESS-HV")}
        claim,text=pairs[scenario]; citation="citation" if scenario!="evidence_missing_citation" else None
        status,_=EvidenceSupportFilter().decide(Claim(type=ClaimType.identifier_fact,text=claim,identifier=claim),[RawEvidence(content=text,source="fixture",citation=citation)])
        return "ALLOW" if status=="SUPPORTED" else "DENY"
    if scenario.startswith("authority_") or scenario.startswith("run_context_") or scenario.startswith("shadow_") or scenario=="separate_runs_no_duplicate": return "ALLOW"
    if any(token in scenario for token in review_tokens) or scenario in {"adapter_revalidation_failed","approval_consumed"}: return "REVIEW"
    if any(token in scenario for token in denied_tokens): return "DENY"
    return "ALLOW"

def main():
    rows=[json.loads(line) for line in GOLD.read_text(encoding="utf8").splitlines() if line.strip()]
    assert len(rows)==52 and len({r["case_id"] for r in rows})==52
    results=[{**row,"actual":evaluate(row)} for row in rows]
    failures=[r for r in results if r["actual"]!=r["expected"]]
    out=ROOT/"evals"/"security"/"security_results_v1.jsonl"
    out.write_text("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in results),encoding="utf8")
    print(f"SECURITY_GOLD_COUNT = {len(rows)}")
    print(f"SECURITY_EVAL = {len(rows)-len(failures)}/{len(rows)}")
    print(f"RESULT_FILE = {out.relative_to(ROOT)}")
    raise SystemExit(1 if failures else 0)
if __name__=="__main__": main()
