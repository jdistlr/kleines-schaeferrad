"""Validate comparison coverage and unchanged canonical baseline; no app build."""
from pathlib import Path
import json,hashlib,subprocess
from PIL import Image
ROOT=Path(__file__).resolve().parents[4];O=ROOT/'state/reconstruction-loop/ITER-002';BASE='f7b9185517856b7881530ba9d0553f170787cb09';PREFIX='state/reconstruction-loop/ITER-002/'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT).decode().strip()
def load(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert git('branch','--show-current')=='work/astra-abgleich-iter002-20261009'
assert git('remote','get-url','origin')=='https://github.com/jdistlr/kleines-schaeferrad.git'
subprocess.run(['git','merge-base','--is-ancestor',BASE,'HEAD'],cwd=ROOT,check=True)
changed=git('diff','--name-only',BASE).splitlines()+git('ls-files','--others','--exclude-standard').splitlines()
assert all(x.startswith(PREFIX) for x in changed),changed
intake=load('evidence/contributions/thorsten-20261009.json')['claims'];entries=json.loads((O/'CONSTRAINT-DELTA.json').read_text())['entries']
assert len(entries)==39 and {e['claim_id'] for e in entries}=={c['id'] for c in intake}
for c,e in zip(intake,entries):
 assert e['intake']==c and not e['applied'] and not e['as_built_promoted']
 assert e['finding'] and e['current_runtime']['anchor'] and e['proposed_action']
 for p in c['sources']:assert (ROOT/p).is_file()
photos=load('evidence/contributions/thorsten-20261009-photos.json')['images'];obs=json.loads((O/'PHOTO-OBSERVATIONS.json').read_text())['photos']
assert len(photos)==len(obs)==65 and len({p['sha256'] for p in photos})==63
assert {p['path'] for p in photos}=={p['path'] for p in obs}
for p in photos:
 b=(ROOT/p['path']).read_bytes();assert hashlib.sha256(b).hexdigest()==p['sha256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==p['git_blob_sha'];assert len(b)==p['bytes']
for p in obs:assert p['visually_reviewed'] and (O/p['contact_sheet']).is_file()
reads=json.loads((O/'PHOTO-READOUTS.json').read_text())['readouts'];assert len(reads)==14
for r in reads:
 assert (ROOT/r['source']).is_file() and not r['canonical_promotion'];assert r['zero'] and r['endpoints'] and r['uncertainty']
 if r['status']=='unresolved':assert r['value'] is None
 with Image.open(ROOT/r['source']) as im:w,h=im.size
 for x0,y0,x1,y1 in r['pixel_regions_xyxy']:assert 0<=x0<x1<=w and 0<=y0<y1<=h,(r['id'],[w,h])
images=[];jsons=[]
for p in O.rglob('*'):
 if p.suffix in ['.png','.jpg']:
  with Image.open(p) as im: im.verify()
  images.append(str(p.relative_to(O)))
 if p.suffix=='.json':json.loads(p.read_text());jsons.append(str(p.relative_to(O)))
views=json.loads((O/'views/manifest.json').read_text());assert len(views)==7
for v in views:
 assert (ROOT/v['path']).is_file() and (ROOT/v['source']).is_file() and v['photo_alignment']=='none' and v['mesh_names']
 with Image.open(ROOT/v['path']) as im:assert im.size==(1800,1180)
a=json.loads((O/'evidence/runtime-audit.json').read_text())
for p,h in a['inputs'].items():assert sha(ROOT/p)==h
assert abs(a['rims']['inner_gap']-1.01)<1e-6 and abs(a['rims']['outer_width']-1.29)<1e-6
assert a['models']['brute']['meshes']==591 and a['models']['truth']['meshes']==70
assert abs(a['nails'][0]['chord_length']-.7263529495)<1e-8
assert abs(a['nails'][1]['chord_length']-.5948792239)<1e-8
required=['ITERATION-REPORT.md','EVIDENCE-COMPARISON.md','CONSTRAINT-DELTA.json','PHOTO-READOUTS.json','PHOTO-OBSERVATIONS.json','OPEN-QUESTIONS.md','IMPLEMENTATION-SEQUENCE.md','SCAN-COMPARISON.md','MODEL-DELTA.json','CRITIQUE-READY.md','REPRODUCE.md']
for p in required:assert (O/p).is_file()
assert load('data/scan-transforms.json')['state']=='AXIS_NORMALIZED'
for p in [O/'ITERATION-REPORT.md',O/'CRITIQUE-READY.md']:assert 'ASTRA COMPARISON REVIEW READY' in p.read_text()
# Every baseline-tracked file is byte-identical; no protected modification hidden by staging.
protected=[]
for p in git('ls-tree','-r','--name-only',BASE).splitlines():
 if p.startswith(PREFIX):continue
 assert (ROOT/p).is_file(),p
 # Git worktree hash avoids printing source contents and is checked against baseline blob.
 protected.append(p)
assert not git('diff',BASE,'--',':(exclude)'+PREFIX)
report={'status':'PASS','base_commit':BASE,'repository':'jdistlr/kleines-schaeferrad','branch':git('branch','--show-current'),'comparison_only':True,'claims_reviewed':len(entries),'original_files_verified':65,'unique_photo_payloads':63,'readouts':len(reads),'conditional_readouts':sum(r['status']=='conditional-readout' for r in reads),'unresolved_readouts':sum(r['status']=='unresolved' for r in reads),'technical_comparison_plates':7,'image_artifacts_decoded':len(images),'baseline_files_protected':len(protected),'out_of_scope_changes':[],'canonical_and_runtime_unchanged':True,'scan_state':'AXIS_NORMALIZED','visual_QA':'All 7 comparison plates and scan search visually reviewed; source photo sheets and scale crops visually reviewed. Automated decode is supplementary, not visual review.','limits':['No as-built promotion','No calibrated photo metrology','No successful mechanical scan registration','No deployment, merge, or runtime correction'],'artifact_sha256':{str(p.relative_to(O)):sha(p) for p in sorted(O.rglob('*')) if p.is_file() and p.name!='VALIDATION.json'}}
(O/'VALIDATION.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='artifact_sha256'},indent=2))
