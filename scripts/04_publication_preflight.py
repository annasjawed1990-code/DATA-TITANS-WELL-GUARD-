"""Fail closed on common confidentiality leaks before GitHub upload.
Run in the public-repository root; does not modify/delete files.
"""
from pathlib import Path
import sys
root=Path(__file__).resolve().parents[1]
forbidden={'daily_production.parquet','well_jobs.parquet','production_failures.parquet'}
private_dirs={'data','outputs','raw','private','.venv'}
private_suffix={'.parquet','.pkl','.pickle','.joblib','.duckdb','.sqlite','.db'}
problems=[]
for p in root.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(root)
    if any(part in private_dirs for part in rel.parts):
        problems.append(str(rel)+' [private directory]')
    elif p.name.lower() in forbidden or p.suffix.lower() in private_suffix:
        problems.append(str(rel)+' [restricted file type]')
    elif p.suffix.lower()=='.csv' and p.name!='example_synthetic.csv':
        problems.append(str(rel)+' [CSV must be manually approved]')
    elif p.stat().st_size>35_000_000:
        problems.append(str(rel)+' [large file, inspect manually]')
if problems:
    print('WARNING: Do not publish this working directory without excluding:')
    for p in problems:print(' -',p)
    sys.exit(2)
print('PASS: No obvious raw or private files in this public-package directory.')
print('Reminder: this is NOT a substitute for manual line-by-line privacy and licensing review.')
