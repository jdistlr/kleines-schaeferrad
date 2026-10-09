"""Verify archived original bytes and structured evidence references; no mutations."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return json.loads((ROOT / path).read_text())

def git_blob_sha1(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

manifest = read('evidence/manifest.json')
manifest_assets = manifest['assets']
baseline_assets = [a for a in manifest_assets if a.get('archive', {}).get('status') == 'archived']
additional_assets = [a for a in manifest_assets if a not in baseline_assets]
assert len(baseline_assets) == manifest['raw_asset_count'] == 43
assert len({a['id'] for a in manifest_assets}) == len(manifest_assets)
source_ids = {a['id'] for a in manifest_assets} | {s['id'] for s in manifest['context_sources']}
assert len({a['sha256'] for a in baseline_assets}) == len(baseline_assets)

for a in additional_assets:
    if a.get('sha256'):
        data = (ROOT / a['path']).read_bytes()
        assert hashlib.sha256(data).hexdigest() == a['sha256'], a['id']
    elif a.get('path'):
        assert (ROOT / a['path']).is_file(), a['id']

for a in baseline_assets:
    data = (ROOT / a['archive']['path']).read_bytes()
    assert len(data) == a['bytes'], a['id']
    assert hashlib.sha256(data).hexdigest() == a['sha256'], a['id']
    assert git_blob_sha1(data) == a['git_blob_sha1'], a['id']
    check = a['prior_manifest_check']
    assert check.get('missing_from_prior_manifest') or (check['size_matches'] and check['sha256_matches'])

for d in manifest['derived_assets']:
    assert hashlib.sha256((ROOT / d['path']).read_bytes()).hexdigest() == d['sha256']
    assert set(d['parents']) <= source_ids

# Expert contributions extend the live baseline without rewriting the historical 43-file manifest.
contribution_files = sorted((ROOT / 'evidence' / 'contributions').glob('*.json'))
contribution_assets = []
for path in contribution_files:
    c = json.loads(path.read_text())
    if source := c.get('source'):
        if source.get('id'):
            source_ids.add(source['id'])
    for s in c.get('supplementary_sources', []):
        if s.get('id'):
            source_ids.add(s['id'])
    for a in c.get('assets', []):
        contribution_assets.append(a)
        source_ids.add(a['id'])
        data = (ROOT / a['archive']['path']).read_bytes()
        assert len(data) == a['bytes'], a['id']
        assert hashlib.sha256(data).hexdigest() == a['sha256'], a['id']
        assert git_blob_sha1(data) == a['git_blob_sha1'], a['id']

claims_doc = read('data/geometry.claims.json')
allowed_classes = set(claims_doc['classes'])
claims = claims_doc['claims']
claim_ids = {c['id'] for c in claims}
assert len(claim_ids) == len(claims)
for c in claims:
    assert c['evidence_class'] in allowed_classes, (c['id'], c['evidence_class'])
    assert c['confidence'] in {'high','medium','low','unknown','qualified'}
    assert c['provenance'] and {p['source_id'] for p in c['provenance']} <= source_ids, c['id']
    assert not c['as_built_eligible']

analyses = read('data/source-analyses.json')['sources']
analysis_ids = {s['source_id'] for s in analyses}
assert len(analysis_ids) == len(analyses)
# Historical baseline coverage remains mandatory.
assert {a['id'] for a in baseline_assets} <= analysis_ids
# Every expert contribution source and contributed image used by baseline claims must be analyzed.
assert {a['id'] for a in contribution_assets} <= analysis_ids
expert_source_ids = set()
for path in contribution_files:
    c = json.loads(path.read_text())
    if c.get('source', {}).get('id'):
        expert_source_ids.add(c['source']['id'])
    expert_source_ids |= {s['id'] for s in c.get('supplementary_sources', []) if s.get('id')}
assert expert_source_ids <= analysis_ids
for s in analyses:
    assert set(s['claim_ids']) <= claim_ids

graph = read('data/assembly.graph.json')
nodes = {n['id'] for n in graph['nodes']}
for e in graph['relations']:
    assert e['from'] in nodes and e['to'] in nodes, e['id']
    assert set(e['provenance']) <= source_ids, e['id']
    assert set(e['claim_ids']) <= claim_ids, e['id']
for instance in graph['instances']:
    assert instance['family'] in nodes and set(instance['provenance']) <= source_ids

for component in read('data/components.json')['components']:
    assert set(component['claim_ids']) <= claim_ids, component['id']

for conflict in read('data/conflicts.json')['conflicts']:
    assert set(conflict['claim_ids']) <= claim_ids, conflict['id']
    if conflict.get('conflict_claim') is not None:
        assert conflict['conflict_claim'] in claim_ids, conflict['id']
    assert set(conflict['sources']) <= source_ids, conflict['id']
    assert conflict['selected_as_built_value'] is None

print(
    f"Verified {len(baseline_assets)} historical baseline originals, "
    f"{len(contribution_assets)} contributed originals, "
    f"{len(manifest['derived_assets'])} derivatives, "
    f"{len(claims)} claims, {len(analyses)} source analyses and graph/conflict references"
)
