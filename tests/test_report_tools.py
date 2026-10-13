import unittest
from scripts.audit_release import audit
from scripts.lint_report import inspect

class ReportTests(unittest.TestCase):
    def test_no_false_approval(self):
        self.assertIn('review incomplete: institutional_approval_recorded',audit({'institutional_approval_recorded':False}))
    def test_vague_heading(self):
        issues=inspect('# 标题\n## 行业概况\n内容')
        self.assertTrue(any('non-argumentative' in msg for typ,msg in issues))
    def test_complete_packet_does_not_assess_truth(self):
        data={
           'report_title':'X','report_version':'v1','report_date':'2026-10-13',
           'evidence_ledger_path':'doc','model_path':'model','final_draft_path':'final',
           'chart_provenance_checked':True,'data_fact_checked':True,'copyright_cleared':True,
           'confidentiality_checked':True,'risk_disclosure_checked':True,
           'institutional_approval_recorded':True,'approval_reference':'approval-1'
        }
        self.assertFalse(audit(data))

if __name__=='__main__':unittest.main()
