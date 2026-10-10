"""Read-only verification. Run in a fresh GitHub checkout AFTER binary upload.
Prints one JSON receipt to stdout; never modifies files. Python standard library only.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
manifest = json.loads((Path(__file__).parent / 'original-transfer-checksums.json').read_text())
results = []
for entry in manifest['originals']:
    path = root / entry['path']
    row = {'path': entry['path'], 'expected_sha256': entry['sha256']}
    if not path.is_file():
        row['status'] = 'MISSING'
    else:
        content = path.read_bytes()
        row.update(bytes=len(content), sha256=hashlib.sha256(content).hexdigest())
        row['status'] = 'PASS' if row['bytes'] == entry['bytes'] and row['sha256'] == entry['sha256'] else 'MISMATCH'
    results.append(row)
receipt = {
    'commit': subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip(),
    'scope': 'Original-byte comparison only; remote provenance requires a separately documented fresh GitHub checkout',
    'expected_count': 77,
    'passed': sum(row['status'] == 'PASS' for row in results),
    'files': results,
}
print(json.dumps(receipt, ensure_ascii=False, indent=2))
sys.exit(0 if len(results) == 77 and receipt['passed'] == 77 else 1)
