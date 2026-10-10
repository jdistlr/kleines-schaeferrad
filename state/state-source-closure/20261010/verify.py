"""Read-only PR #17 preservation audit; emits JSON to stdout. Run from repo root."""
import hashlib
import json
from pathlib import Path
import subprocess

BASE = '118e5f7da51a89eaf04bfe85072169e902f4b532'
START = '52cf6227b5ff91fd994cd6864c1f23761a3d017a'
NARRATIVE = 'NARRATIVE-TH-CONSTRUCTION-20261009'
def read(p):
    return json.loads(Path(p).read_text())
def git_bytes(ref, p):
    return subprocess.check_output(['git', 'show', f'{ref}:{p}'])
def sha(b):
    return hashlib.sha256(b).hexdigest()
# Later annotated original: independent byte check; historical output stays reproducible.
new_photo = read('evidence/contributions/torsten-20261010-original.json')['images'][0]
new_bytes = Path(new_photo['path']).read_bytes()
assert len(new_bytes) == new_photo['bytes'] == 559904
assert sha(new_bytes) == new_photo['sha256'] == '048708cdf56fd72025b12c1bc1e0bd4bc8c201dc74654c4fb2c55ed45fe23eb5'
assert hashlib.sha1(b'blob ' + str(len(new_bytes)).encode() + b'\0' + new_bytes).hexdigest() == new_photo['git_blob_sha']
assert new_photo['claim_ids'] == ['TH-20261009-37'] and not new_photo['as_built_eligible']
photos = read('evidence/contributions/thorsten-20261009-photos.json')['images']
assert len(photos) == 65
rows = []
for a in photos:
    b = Path(a['path']).read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
    assert sha(b) == a['sha256'] and len(b) == a['bytes'] and blob == a['git_blob_sha'], a['path']
    assert b == git_bytes(BASE, a['path']) == git_bytes(START, a['path']), a['path']
    rows.append(dict(path=a['path'], bytes=len(b), sha256=sha(b), git_blob_sha=blob, manifest_match=True, baseline_and_start_preserved=True))
assert len({a['sha256'] for a in rows}) == 63
intake_path = 'evidence/contributions/thorsten-20261009.json'
canonical_path = 'data/geometry.claims.json'
for p in [intake_path, canonical_path, 'evidence/contributions/thorsten-20261009-photos.json']:
    assert Path(p).read_bytes() == git_bytes(BASE,p) == git_bytes(START,p), p
intake = read(intake_path)['claims']
canonical = {c['id']:c for c in read(canonical_path)['claims']}
analyses = {s['source_id']:s for s in read('data/source-analyses.json')['sources']}
expected = {f'TH-20261009-{i:02}' for i in range(1,40)}
assert len(intake) == 39 and {c['id'] for c in intake} == expected
backlinks = analyses[NARRATIVE]['claim_ids']
assert len(backlinks) == 39 and set(backlinks) == expected
photo_by_path = {a['path']:a for a in photos}
claim_rows = []
for c in intake:
    k = canonical[c['id']]
    for field in ['subject','predicate','value','unit','scope']:
        assert c[field] == k[field], (c['id'],field)
    prov = {p['source_id'] for p in k['provenance']}
    assert NARRATIVE in prov and not k['as_built_eligible']
    source_rows = []
    for path in c['sources']:
        a = photo_by_path[path]
        assert a['id'] in prov and c['id'] in analyses[a['id']]['claim_ids'], (c['id'],path)
        source_rows.append(dict(path=path,sha256=a['sha256'],reciprocal=True))
    claim_rows.append(dict(id=c['id'],value=k['value'],unit=k['unit'],intake_value_equal=True,canonical_record_preserved=True,narrative_reciprocal=True,as_built_eligible=k['as_built_eligible'],photo_sources=source_rows))
print(json.dumps(dict(schema='ks-state-source-closure/v1',baseline=BASE,inherited_head=START,photos=rows,claims=claim_rows,summary=dict(photo_paths=65,unique_payloads=63,claims=39,narrative_reciprocal=39,all_checks_pass=True)),ensure_ascii=False,indent=2))
