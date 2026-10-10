"""Read-only review gate. No geometry generation or canonical writes.

Run from any directory with Python 3. Needs git and the complete baseline commit.
Reports assertions about contracts/bytes, NOT physical truth or visual inspection.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = '727a0248c0234641453a08e4ae3984e27c9f970b'
PREFIX = str(HERE.relative_to(ROOT)) + '/'

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])

def read(path):
    return json.loads((ROOT / path).read_text())

def original(path):
    return git('show', f'{BASE}:{path}')

checks = []
def check(name, condition, detail=None):
    checks.append({'check': name, 'pass': bool(condition), 'detail': detail})

claims = read('data/geometry.claims.json')['claims']
C = {c['id']: c for c in claims}
components = read('data/components.json')['components']
B = {c['id']: c for c in components}
tasks = read('data/field-tasks.json')['tasks']
T = {t['task_id']: t for t in tasks}
gaps = read('data/knowledge-gaps.json')['gaps']
G = {g['id']: g for g in gaps}
conflicts = read('data/conflicts.json')['conflicts']
F = {c['id']: c for c in conflicts}
audit = json.loads(subprocess.check_output([sys.executable, str(HERE.parent/'audit-evidence.py')]))
S = set(audit['source_definitions'])

# Construct the only permitted canonical deltas from the immutable baseline.
allowed_data = ['data/components.json', 'data/field-tasks.json', 'data/reconstruction-evidence-map.json', 'docs/field-kit/field-pack-manifest.json']
expected = {p: json.loads(original(p)) for p in allowed_data}
comp = next(x for x in expected[allowed_data[0]]['components'] if x['id'] == 'COMP-KUMPF-NAILS')
comp['provenance'] = [{'PHOTO-6822':'V2-IMG_6822', 'PHOTO-6832':'V2-IMG_6832'}.get(s,s) for s in comp['provenance']]
task = next(x for x in expected[allowed_data[1]]['tasks'] if x['task_id'] == 'TASK-PAD')
task['source_refs'].append('GAP-09')
emap = expected[allowed_data[2]]
emap['rules'][2] = 'IMG_6875–6877 sind archiviert, ihre Objektidentität ist unbestätigt. Ohne Identitätsnachweis keine Bestätigung von Topologie, Maßen oder Zustand des Zielrads. Siehe state/evidence-consolidation/20261010/CONTEXT-IDENTITY-ADDENDUM.md.'
for row in emap['components']:
    row['sources'] = ['V2-IMG_6808-upload2' if s == 'V2-IMG_6808' else s for s in row['sources']]
expected[allowed_data[3]]['task_source_sha256'] = hashlib.sha256((ROOT/'data/field-tasks.json').read_bytes()).hexdigest()
for path, value in expected.items():
    check('exact-authorized-delta:' + path, read(path) == value)

old_claims = {c['id']: c for c in json.loads(original('data/geometry.claims.json'))['claims']}
th = [f'TH-20261009-{i:02}' for i in range(1,40)]
check('all-39-expert-corrections-unchanged', all(C.get(i) == old_claims.get(i) and i in C for i in th))
check('all-408-claims-byte-preserved', (ROOT/'data/geometry.claims.json').read_bytes() == original('data/geometry.claims.json'))
check('nine-gaps-21-tasks-no-new-instances', len(G)==9 and len(T)==21 and read('data/instance-register.json')['instances']==[])
check('GAP-09-linked-to-existing-TASK-PAD', 'GAP-09' in T['TASK-PAD']['source_refs'] and audit['gap_tasks']['GAP-09']==['TASK-PAD'])
check('no-broken-source-reference-in-claim-component-model', not [e for e in audit['reference_candidates'] if e.get('type') in ['cites-source','model-map-cites']])
check('no-claim-support-cycle', not audit['claim_support_cycles'])
check('no-missing-provenance-or-duplicate-ids', not audit['claims_without_provenance'] and not audit['assembly_relations_without_provenance'] and not any(audit['duplicate_ids'].values()))
check('all-registered-assets-intact', all(a['exists'] and a.get('hash_matches') and a.get('size_matches') for a in audit['asset_checks']))

cases = json.loads((HERE/'reference-cases.json').read_text())['cases']
check('three-reference-cases', [c['name'] for c in cases]==['Welle/Arm','Kumpf','Kranz'])
for case in cases:
    for key, registry in [('claims',C),('components',B),('sources',S),('gaps',G),('tasks',T),('conflicts',F)]:
        missing = [i for i in case[key] if i not in registry]
        check(case['name']+':'+key+'-resolve', not missing, missing)
    check(case['name']+':model-files-exist', all((ROOT/p).is_file() for p in case['model_files']))
    check(case['name']+':qualifiers-preserved', all({k:C[i].get(k) for k in q}==q for i,q in case['expected_claim_qualifiers'].items()))
    check(case['name']+':gaps-investigated-by-existing-tasks', all(any(g in T[t]['source_refs'] for t in case['tasks']) for g in case['gaps']))
    check(case['name']+':no-context-target-promotion', case['target_confirmation_from_context_allowed'] is False and all('6875' not in s and '6876' not in s and '6877' not in s for s in case['sources']))

# Explicit semantic counterexamples. No new production truth evaluator is introduced.
check('shaft-370-is-not-current-metres', C['CLAIM-0001']['value']==370 and C['CLAIM-0001']['unit'] is None and C['CLAIM-0001']['scope']=='documented-design' and C['CLAIM-0001']['as_built_eligible'] is False)
sources = {s['source_id']:s for s in read('data/source-analyses.json')['sources']}
check('shaft-photos-share-document-not-independent-measurements', sources['PHOTO-6816']['document_group']==sources['PHOTO-6817']['document_group']=='DOC-SHAFT')
check('contactstrips-not-current-wheel-geometry', all(sources[s]['current_geometry_authority'] is False for s in ['PHOTO-6833','PHOTO-6845']))
check('axial-radial-conflict-already-resolved', F['CONFLICT-04']['status']=='semantic-dimensions-resolved')
check('derived-distances-not-independent-field-measures', all(C[i]['evidence_class']=='derived' and C[i]['as_built_eligible'] is False and C[i]['derived_from']==['TH-20261009-25','TH-20261009-26'] for i in ['TH-20261009-28','TH-20261009-29']))
inner,width=C['TH-20261009-25']['value'],C['TH-20261009-26']['value']
check('derivation-arithmetic-only', abs(C['TH-20261009-28']['value']-(inner+width))<1e-12 and abs(C['TH-20261009-29']['value']-(inner+2*width))<1e-12)
check('digital-measurement-not-field-measurement', all(c['scope']=='digital-artifact-only' and c['as_built_eligible'] is False for c in claims if c['evidence_class']=='measured'))

sighting = json.loads((HERE/'source-sighting.json').read_text())
transfer = read('state/evidence-consolidation/20261010/original-transfer-checksums.json')['originals']
photos = {r['path']:r for r in sighting['photos']}
expected_photos = {r['path'] for r in transfer if r['path'].endswith('.jpeg')}
check('76-photo-review-records-no-omission', len(sighting['photos'])==76 and set(photos)==expected_photos)
check('all-review-media-hashes-match', all(hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==r['sha256'] for r in sighting['photos']+sighting['context']+sighting['focused_reference_originals']+[sighting['video']]))
check('77-original-transfer-files-intact', len(transfer)==77 and all((ROOT/r['path']).stat().st_size==r['bytes'] and hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==r['sha256'] for r in transfer))
check('three-context-images-identity-unconfirmed', len(sighting['context'])==3 and all(r['identity']=='unconfirmed' and r['target_support_allowed'] is False for r in sighting['context']))
check('30-attachments-byte-matched-to-repository', len(sighting['attachments'])==30 and all(r['matches'] and all((ROOT/p).is_file() and hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==r['sha256'] for p in r['matches']) for r in sighting['attachments']))
check('all-sighting-anchors-resolve', all(x in C or x in B or x in G or x in F for r in sighting['photos'] for x in r['existing_anchors']))
frames=[i for lo,hi in sighting['video']['overview_viewed_frame_ranges'] for i in range(lo,hi+1)]
check('video-recorded-overview-coverage-638', frames==list(range(638)) and len(sighting['video']['detailed_sample_seconds'])==43)
check('audio-limit-explicit-not-complete-source-review', 'not listened to or transcribed' in sighting['video']['audio'])

equivalence = json.loads((HERE/'field-pack-equivalence.json').read_text())
check('field-pack-reference-change-preserves-rendered-outputs', equivalence['passed'] is True and equivalence['byte_identical_output_count'] > 0 and equivalence['manifest_changed_keys']==['task_source_sha256'])
check('field-pack-equivalence-inputs-match', equivalence['new_task_source_sha256']==hashlib.sha256((ROOT/'data/field-tasks.json').read_bytes()).hexdigest() and equivalence['old_task_source_sha256']==hashlib.sha256(original('data/field-tasks.json')).hexdigest())

# Preserve every baseline file outside exact canonical deltas and additive notices.
notices = {
 'docs/CONTEXT-EVIDENCE-6875-6876.md',
 *['state/evidence-consolidation/20261010/'+p for p in ['REVIEW-SUMMARY.md','SOURCE-ACCESS-GATE.md','SOURCE-INVENTORY.md','GRAPH-CONTRACT-AND-INTEGRITY.md','EVIDENCE-CHAINS.md','THORSTEN-DECISION-BILL.md','STABILIZATION-PLAN.md','CONTEXT-IDENTITY-ADDENDUM.md']],
}
tree = git('ls-tree','-r','--full-tree',BASE).decode().splitlines()
unchanged, notices_ok, unexpected = [], [], []
for line in tree:
    meta,path=line.split('\t',1)
    mode,kind,oid=meta.split()
    p=ROOT/path
    if not p.is_file():
        unexpected.append({'path':path,'reason':'missing'});continue
    current=git('hash-object','--',path).decode().strip()
    if current==oid:
        unchanged.append(path)
    elif path in allowed_data:
        continue
    elif path in notices and p.read_bytes().endswith(original(path)):
        notices_ok.append(path)
    else:
        unexpected.append({'path':path,'reason':'unapproved modification'})
check('all-baseline-files-preserved-except-exact-deltas-and-prepended-notices', not unexpected, unexpected)
baseline_paths={line.split('\t',1)[1] for line in tree}
new_paths=set(git('ls-files','--cached','--others','--exclude-standard').decode().splitlines())-baseline_paths
check('new-files-confined-to-review-package', all(p.startswith(PREFIX) for p in new_paths), sorted(p for p in new_paths if not p.startswith(PREFIX)))

summary_keys=['counts','reference_candidates','duplicate_ids','source_url_collisions','semantic_duplicate_candidates','claim_support_cycles','gap_tasks','conflict_statuses']
result={'baseline':BASE,'head_at_run':git('rev-parse','HEAD').decode().strip(),'run_scope':'Working tree compared to immutable baseline; head_at_run is pre-commit HEAD', 'input_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in allowed_data+['data/geometry.claims.json',PREFIX+'reference-cases.json',PREFIX+'source-sighting.json',PREFIX+'field-pack-equivalence.json']}, 'purpose':'Contract and preservation checks only; no physical, audio or geometric approval','passed':all(c['pass'] for c in checks),'check_count':len(checks),'checks':checks,'preservation':{'baseline_files':len(tree),'byte_identical':len(unchanged),'exact_data_delta_files':allowed_data,'additive_notice_files':notices_ok,'unexpected':unexpected},'audit_summary':{k:audit[k] for k in summary_keys}}
print(json.dumps(result,ensure_ascii=False,indent=2))
sys.exit(0 if result['passed'] else 1)
