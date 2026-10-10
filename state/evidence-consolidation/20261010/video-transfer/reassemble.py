"""Reassemble exact original bytes from SHA-256 checked transport parts."""
import hashlib
import json
from pathlib import Path
import os

root = Path(__file__).resolve().parents[4]
manifest = json.loads((Path(__file__).parent / 'parts.json').read_text())
assert manifest['target'] == 'evidence/raw/originaltransfer-20261010/IMG_6857.mp4'
assert manifest['sha256'] == 'bfcf16efd88f912f63bb7e66a9bed6fb6e6148da751659f6ef390598a85344ab'
parts = []
for row in manifest['parts']:
    content = (root / row['path']).read_bytes()
    assert len(content) == row['bytes']
    assert hashlib.sha256(content).hexdigest() == row['sha256']
    parts.append(content)
content = b''.join(parts)
assert len(content) == manifest['bytes'] == 13408295
assert hashlib.sha256(content).hexdigest() == manifest['sha256']
target = root / manifest['target']
if target.exists():
    assert target.read_bytes() == content, 'Refusing to overwrite different original bytes'
else:
    target.write_bytes(content)
receipt = {'status': 'PASS', 'source_commit': os.environ.get('GITHUB_SHA'), 'target': manifest['target'], 'bytes': len(content), 'sha256': hashlib.sha256(content).hexdigest(), 'parts': manifest['parts'], 'method': 'Ordered byte concatenation; no transcoding'}
(root / 'state/evidence-consolidation/20261010/video-reassembly-receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
print('Original video reconstructed, SHA-256 PASS')
