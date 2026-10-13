#!/usr/bin/env python3
"""Check release packet completeness, never approve external publication."""
from __future__ import annotations
import argparse,json
from pathlib import Path

REQUIRED={
 'report_title':str,'report_version':str,'report_date':str,
 'evidence_ledger_path':str,'model_path':str,'final_draft_path':str,
 'chart_provenance_checked':bool,'data_fact_checked':bool,
 'copyright_cleared':bool,'confidentiality_checked':bool,
 'risk_disclosure_checked':bool,'institutional_approval_recorded':bool,
 'approval_reference':str,
}

def audit(packet:dict)->list[str]:
   reasons=[]
   for name,kind in REQUIRED.items():
       value=packet.get(name)
       if not isinstance(value,kind) or (kind is str and not value.strip()):
           reasons.append(f'missing or invalid: {name}')
   for field in ('chart_provenance_checked','data_fact_checked','copyright_cleared','confidentiality_checked','risk_disclosure_checked','institutional_approval_recorded'):
       if packet.get(field) is not True: reasons.append(f'review incomplete: {field}')
   return sorted(set(reasons))

def main():
 p=argparse.ArgumentParser();p.add_argument('packet',type=Path);a=p.parse_args()
 issues=audit(json.loads(a.packet.read_text(encoding='utf-8')))
 if issues:
  print('BLOCKED: packet is incomplete, NOT approved for release')
  for x in issues:print('- '+x)
  raise SystemExit(1)
 print('Packet fields complete; verify the human approvals and evidence independently. This tool never authorizes publication.')
if __name__=='__main__':main()
