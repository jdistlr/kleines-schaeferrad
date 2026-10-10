"""Read-only provenance inventory. Run at repository root. Writes only audit evidence."""
import json, hashlib, subprocess
from pathlib import Path
out=Path('state/holistic-stabilization/20261009/evidence')
def read(p): return json.loads(Path(p).read_text())
def git(*a): return subprocess.check_output(['git',*a],text=True).strip()
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
intake=read('evidence/contributions/thorsten-20261009.json')['claims']; claims={c['id']:c for c in read('data/geometry.claims.json')['claims']}; analyses=read('data/source-analyses.json')['sources']; components=read('data/components.json')['components']; graph=read('data/assembly.graph.json'); photos=read('evidence/contributions/thorsten-20261009-photos.json')['images']; probe=read(out/'probe.json')
photo_by_path={p['path']:p for p in photos}
old=git('show','origin/work/iter003-truth-critic-20261009:state/reconstruction-loop/ITER-003/independent-audit/CLAIMS-39.md')
view_map={line.split('|')[1].strip():line.split('|')[-2].strip() for line in old.splitlines() if line.startswith('| TH-')}
rows=[]
for i in intake:
 c=claims.get(i['id']); cid=i['id']; canonical_subjects=c['subject'].split('/')
 rows.append({'id':cid,'statement':i['statement'],'original_sources':[{'path':s,'exists':Path(s).exists(),'sha256':sha(s) if Path(s).exists() else None,'manifest_id':photo_by_path.get(s,{}).get('id'),'hash_matches':sha(s)==photo_by_path[s]['sha256'] if s in photo_by_path else None} for s in i.get('sources',[])], 'canonical':c,'intake_value_equal':i['value']==c['value'],'analyses_backlinks':[a['source_id'] for a in analyses if cid in a['claim_ids']], 'provenance_without_reciprocal_claim':[p['source_id'] for p in c['provenance'] if not any(a['source_id']==p['source_id'] and cid in a['claim_ids'] for a in analyses)],'component_backlinks':[x['id'] for x in components if cid in x['claim_ids']],'subject_without_component_backlink':[s for s in canonical_subjects if not any(x['id']==s and cid in x['claim_ids'] for x in components)],'graph_relations':[e['id'] for e in graph['relations'] if cid in e.get('claim_ids',[])],'runtime_meshes':{m:probe['models'][m]['claimMeshCoverage'][cid] for m in ['truth','brute']},'drawing_view_reference_from_PR14':view_map.get(cid),'ui_contract':'Component inspector reads canonical component claim_ids and normalized assets; direct live journey is sampled, not every claim individually clicked.'})
(out/'claims-39-trace.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
branches=[]
for ref in git('for-each-ref','--format=%(refname:short)','refs/remotes/origin').splitlines():
 if ref=='origin/HEAD': continue
 behind,ahead=map(int,git('rev-list','--left-right','--count','origin/main...'+ref).split())
 branches.append({'branch':ref,'sha':git('rev-parse',ref),'behind_main':behind,'ahead_main':ahead,'last_commit':git('show','-s','--format=%aI %an %s',ref),'unique_changes':git('diff','--stat','origin/main...'+ref)})
(out/'branches.json').write_text(json.dumps(branches,ensure_ascii=False,indent=2)+'\n')
source_results=[dict(path=p['path'],expected=p['sha256'],actual=sha(p['path']),match=sha(p['path'])==p['sha256']) for p in photos]
protected=git('ls-files','data','evidence','src','tests','.github','scripts','state/reconstruction-loop/ITER-003/models','state/reconstruction-loop/ITER-003/views').splitlines()
(out/'protected-hashes.json').write_text(json.dumps({p:sha(p) for p in protected},indent=2)+'\n')
(out/'thorsten-hashes.json').write_text(json.dumps(source_results,indent=2)+'\n')
summary={'base':git('rev-parse','origin/main'),'audit_start':git('rev-parse','HEAD'),'claims':len(rows),'intake_value_mismatches':[r['id'] for r in rows if not r['intake_value_equal']],'photo_paths':len(photos),'unique_photo_hashes':len(set(p['sha256'] for p in photos)),'all_photo_hashes_match':all(p['match'] for p in source_results),'claims_no_analysis':[r['id'] for r in rows if not r['analyses_backlinks']],'claims_incomplete_provenance_backlinks':{r['id']:r['provenance_without_reciprocal_claim'] for r in rows if r['provenance_without_reciprocal_claim']},'claims_subject_backlink_gaps':{r['id']:r['subject_without_component_backlink'] for r in rows if r['subject_without_component_backlink']},'claims_no_graph':[r['id'] for r in rows if not r['graph_relations']],'claims_no_brute_mesh_tag':[r['id'] for r in rows if not r['runtime_meshes']['brute']]}
(out/'canonical-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False,indent=2))
