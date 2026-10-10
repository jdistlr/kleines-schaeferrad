"""Read-only referential and provenance checks, independent of implementation tests."""
import json,hashlib,subprocess
from pathlib import Path
R=Path('.');O=R/'state/reconstruction-loop/ITER-003/independent-audit'
def read(p):return json.loads((R/p).read_text())
claims=read('data/geometry.claims.json')['claims'];th=[c for c in claims if c['id'].startswith('TH-20261009-')]; intake=read('evidence/contributions/thorsten-20261009.json')['claims']; comps=read('data/components.json')['components'];g=read('data/assembly.graph.json');sources=read('data/source-analyses.json')['sources'];assets=read('evidence/manifest.json')['assets'];ids={x['id'] for x in assets};nodes={x['id'] for x in g['nodes']};ci={x['id'] for x in comps};claimids={x['id'] for x in claims}
rows=[]
for c in th:
 original=next(x for x in intake if x['id']==c['id'])
 rows.append({'id':c['id'],'intake_value_equal':original['value']==c['value'],'as_built_eligible':c['as_built_eligible'],'provenance_resolves':all(p['source_id'] in ids for p in c['provenance']),'source_analyses':[x['source_id'] for x in sources if c['id'] in x.get('claim_ids',[])],'components':[x['id'] for x in comps if c['id'] in x.get('claim_ids',[])],'graph_edges':[x['id'] for x in g['relations'] if c['id'] in x.get('claim_ids',[])],'derived_from_resolves':all(x in claimids for x in c.get('derived_from',[]))})
photos=[]
for a in assets:
 if a['id'].startswith('PHOTO-TH-20261009'):
  p=R/a['path']; b=p.read_bytes();h=hashlib.sha256(b).hexdigest();photos.append({'id':a['id'],'path':a['path'],'sha256':h,'manifest_sha256':a.get('sha256'),'match':h==a.get('sha256')})
result={'claims':rows,'graph_dangling_endpoints':[x for x in g['relations'] if x['from'] not in nodes or x['to'] not in nodes],'graph_nodes_missing_in_components':[x for x in nodes-ci if x.startswith('COMP-')],'source_photos':photos,'new_measured_current_values':[]}
# Diff records with any non-null current_value; distinguish untouched baseline values.
for f in ['data/hypothesis.parameters.json','data/geometry.claims.json','data/knowledge-gaps.json']:
 cur=(R/f).read_text();base=subprocess.check_output(['git','show','f7b9185:'+f],text=True)
 def walk(x,path=''):
  if isinstance(x,dict):
   for k,v in x.items():
    if k in ['current_value','installedMetric','selected_as_built_value'] and v is not None:yield [path+'/'+k,v]
    yield from walk(v,path+'/'+k)
  elif isinstance(x,list):
   for i,v in enumerate(x):yield from walk(v,path+'/'+str(i))
 old=list(walk(json.loads(base)));new=list(walk(json.loads(cur)));result['new_measured_current_values'] += [{'file':f,'entry':x} for x in new if x not in old]
(O/'canonical.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'claims':len(rows),'changedValues':[r['id'] for r in rows if not r['intake_value_equal']],'missingProvenance':[r['id'] for r in rows if not r['provenance_resolves']],'missingComponents':[r['id'] for r in rows if not r['components']],'missingAnalyses':[r['id'] for r in rows if not r['source_analyses']],'danglingEdges':len(result['graph_dangling_endpoints']),'nodesMissingComponents':result['graph_nodes_missing_in_components'],'photos':len(photos),'photoHashFailures':sum(not p['match'] for p in photos),'newMeasuredValues':result['new_measured_current_values']},ensure_ascii=False))
