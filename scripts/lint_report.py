#!/usr/bin/env python3
"""Helpful Markdown structural checks for research drafts; never asserts factual validity."""
from __future__ import annotations
import argparse, re
from pathlib import Path


def inspect(text: str) -> list[tuple[str, str]]:
    issues=[]
    h1=[s.strip() for s in text.splitlines() if s.startswith('# ')]
    h2=[s.strip() for s in text.splitlines() if s.startswith('## ')]
    if not h1: issues.append(('STRUCTURE','missing report title (#)'))
    if not h2: issues.append(('STRUCTURE','missing section headings (##)'))
    vague=('行业概况','公司介绍','市场分析','未来展望','投资逻辑','发展前景')
    for s in h2:
        if any(s.removeprefix('## ').strip()==v for v in vague):
            issues.append(('READABILITY',f'non-argumentative heading: {s}'))
    for line_no, line in enumerate(text.splitlines(),1):
        if re.search(r'(?<![\d\w])(20\d{2})(?![\d\w])',line) and '来源' not in line and len(line)>150:
            issues.append(('REVIEW',f'line {line_no}: check date, units, source and A/E tags'))
        if re.search(r'(未来可期|赋能发展|持续推进高质量发展|景气广阔)',line):
            issues.append(('READABILITY',f'line {line_no}: replace vague phrase with verifiable claim'))
    if '风险' not in text: issues.append(('RELEASE','risk section appears missing'))
    if not re.search(r'(来源|资料来源|参考资料|Source)',text,re.I):
        issues.append(('RELEASE','sources/footnotes appear missing'))
    return issues


def main():
    p=argparse.ArgumentParser();p.add_argument('path',type=Path);p.add_argument('--strict',action='store_true');a=p.parse_args()
    findings=inspect(a.path.read_text(encoding='utf-8'))
    for severity,detail in findings: print(f'{severity}: {detail}')
    print(f'Findings: {len(findings)}. Static checks cannot validate claims, citations, calculations, copyright or regulatory compliance.')
    if a.strict and findings: raise SystemExit(1)
if __name__=='__main__': main()
