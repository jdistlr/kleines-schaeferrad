"""Read-only audit of existing contracts; JSON stdout. No canonical writes."""
import collections
import hashlib
import json
from pathlib import Path
import re
import subprocess

root = Path(__file__).resolve().parents[3]
def read(name): return json.loads((root/name).read_text())
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
claims=read('data/geometry.claims.json')['claims']; comps=read('data/components.json')['components']
sources=read('data/source-analyses.json')['sources']; tasks=read('data/field-tasks.json')['tasks']
gaps=read('data/knowledge-gaps.json')['gaps']; conflicts=read('data/conflicts.json')['conflicts']; assembly=read('data/assembly.graph.json')
manifest=read('evidence/manifest.json'); definitions=collections.defaultdict(list); assets=[]
def register(row,file,pointer,idkey='id'):
    ident=row.get(idkey)
    if ident: definitions[ident].append({'file':file,'pointer':pointer,'entry':row})
    p=row.get('archive_path') or row.get('path') or (row.get('archive') or {}).get('path')
    if p:
        asset={'id':ident,'registry':file,'pointer':pointer,'path':p,'expected_sha256':row.get('sha256'),'kind':row.get('kind') or row.get('evidence_class'),'group':row.get('group')}
        target=root/p;asset['exists']=target.is_file()
        if target.is_file():
            asset['sha256']=digest(target);asset['bytes']=target.stat().st_size
            asset['hash_matches']=asset['expected_sha256'] is None or asset['sha256']==asset['expected_sha256']
            asset['size_matches']=row.get('bytes') is None or row['bytes']==asset['bytes']
        assets.append(asset)
for key in ['assets','derived_assets','context_sources']:
    for i,r in enumerate(manifest[key]): register(r,'evidence/manifest.json',f'/{key}/{i}')
for i,r in enumerate(read('evidence/additions-v2.json')['assets']): register(r,'evidence/additions-v2.json',f'/assets/{i}')
for p in sorted((root/'evidence/contributions').glob('*.json')):
    d=json.loads(p.read_text())
    for key in ['images','assets','supplementary_sources']:
        value=d.get(key,[])
        if isinstance(value,list):
            for i,r in enumerate(value):
                if isinstance(r,dict):register(r,str(p.relative_to(root)),f'/{key}/{i}')
for i,r in enumerate(sources):register(r,'data/source-analyses.json',f'/sources/{i}','source_id')
for i,r in enumerate(read('data/external-construction-research-v2.json')['sources']):register(r,'data/external-construction-research-v2.json',f'/sources/{i}')
C={r['id'] for r in claims}; B={r['id'] for r in comps}; G={r['id'] for r in gaps}; T={r['task_id'] for r in tasks}; F={r['id'] for r in conflicts}; S=set(definitions)
edges=[]; errors=[]
def edge(a,b,rel,file,ptr,expected=None):
    edges.append({'from':a,'to':b,'type':rel,'file':file,'pointer':ptr,'derivation':'explicit-contract-reference'})
    if expected is not None and b not in expected:errors.append(edges[-1])
for i,c in enumerate(claims):
    for j,p in enumerate(c.get('provenance',[])):
        edge(c['id'],p['source_id'],'cites-source','data/geometry.claims.json',f'/claims/{i}/provenance/{j}',S|C)
    for j, dep in enumerate(c.get('derived_from', [])):
        edge(c['id'],dep,'derived-from-claim','data/geometry.claims.json',f'/claims/{i}/derived_from/{j}',C)
    for subject in c['subject'].split('/'):
        edge(c['id'],subject,'about-subject','data/geometry.claims.json',f'/claims/{i}/subject')
for i,c in enumerate(comps):
    for j,cid in enumerate(c.get('claim_ids',[])):edge(c['id'],cid,'indexes-claim','data/components.json',f'/components/{i}/claim_ids/{j}',C)
    for j,s in enumerate(c.get('provenance',[])):edge(c['id'],s,'cites-source','data/components.json',f'/components/{i}/provenance/{j}',S)
for i,s in enumerate(sources):
    for j,c in enumerate(s.get('claim_ids',[])):edge(s['source_id'],c,'indexes-claim','data/source-analyses.json',f'/sources/{i}/claim_ids/{j}',C)
for i,t in enumerate(tasks):
    edge(t['task_id'],t['component'],'captures-component','data/field-tasks.json',f'/tasks/{i}/component',B)
    for j,s in enumerate(t.get('source_refs',[])):
        edge(t['task_id'],s,'investigates-gap' if s in G else 'references-context','data/field-tasks.json',f'/tasks/{i}/source_refs/{j}',G|S|C|F if not s.startswith('HUMAN-') else None)
for i,g in enumerate(gaps):
    for j,f in enumerate(g.get('conflict_ids',[])):edge(g['id'],f,'tracks-conflict','data/knowledge-gaps.json',f'/gaps/{i}/conflict_ids/{j}',F)
for i,f in enumerate(conflicts):
    for key,target,rel in [('claim_ids',C,'compares-claim'),('sources',S,'cites-source'),('subjects',B,'about-component')]:
        for j,v in enumerate(f.get(key,[])):edge(f['id'],v,rel,'data/conflicts.json',f'/conflicts/{i}/{key}/{j}',target)
    for v in f.get('resolution_capture','').split('/'):
        edge(f['id'],v,'requires-capture','data/conflicts.json',f'/conflicts/{i}/resolution_capture',G if not v.startswith('HUMAN-') else None)
for i,e in enumerate(assembly['relations']):
    edge(e['from'],e['to'],e['type'],'data/assembly.graph.json',f'/relations/{i}',B)
    if e['from'] not in B:errors.append({'assembly_from':e['from'],'id':e['id']})
    for key,target in [('provenance',S),('claim_ids',C)]:
        for j,v in enumerate(e.get(key,[])):edge(e['id'],v,'cites-source' if key=='provenance' else 'supported-by-claim','data/assembly.graph.json',f'/relations/{i}/{key}/{j}',target)
for i,c in enumerate(read('data/reconstruction-evidence-map.json')['components']):
    for j,s in enumerate(c.get('sources',[])):edge(c['component'],s,'model-map-cites','data/reconstruction-evidence-map.json',f'/components/{i}/sources/{j}',S|C)
raw=[]; by_hash=collections.defaultdict(list)
for p in sorted((root/'evidence/raw').rglob('*')):
    if p.is_file():
        h=digest(p);row={'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':h};raw.append(row);by_hash[h].append(row['path'])
source_hashes=collections.defaultdict(set)
for a in assets:
    if a.get('sha256') and a['id']:source_hashes[a['sha256']].add(a['id'])
transfer=read('state/evidence-consolidation/20261010/original-transfer-checksums.json')
mapping=[dict(r,existing_source_ids=sorted(source_hashes[r['sha256']]),byte_identical_paths=by_hash[r['sha256']]) for r in transfer['originals']]
semantic=collections.defaultdict(list)
for c in claims:semantic[json.dumps([c.get(k) for k in ['subject','predicate','value','unit','scope']],sort_keys=True,ensure_ascii=False)].append(c['id'])
urls=[]
for sid,ds in definitions.items():
    found=sorted({d['entry']['url'] for d in ds if d['entry'].get('url')})
    if len(found)>1:urls.append({'id':sid,'urls':found,'registries':[d['file'] for d in ds]})
# Support graph only: excludes reciprocal navigational indexes and assembly relations.
support=collections.defaultdict(list)
for e in edges:
    if e['type'] in ('cites-source','derived-from-claim') and e['from'] in C:support[e['from']].append(e['to'])
cycles=[]
def visit(n,stack):
    if n in stack:
        cycle=stack[stack.index(n):]+[n]
        if cycle not in cycles:cycles.append(cycle)
        return
    for v in support.get(n,[]):
        if v in C:visit(v,stack+[n])
for c in C:visit(c,[])
report={
 'scope':'Read-only contract and byte audit; not a metric/physical release; all counts refer to this snapshot',
 'commit':subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip(),
 'counts':{'claims':len(claims),'components':len(comps),'source_analyses':len(sources),'source_ids_in_union':len(S),'gaps':len(gaps),'tasks':len(tasks),'conflicts':len(conflicts),'assembly_nodes':len(assembly['nodes']),'assembly_relations':len(assembly['relations']),'historical_slots':len(assembly['instances']),'physical_instances':len(read('data/instance-register.json')['instances']),'raw_files':len(raw),'raw_unique_hashes':len(by_hash)},
 'duplicate_ids':{k:[x for x,n in collections.Counter(rows).items() if n>1] for k,rows in [('claims',[r['id'] for r in claims]),('components',[r['id'] for r in comps]),('sources',[r['source_id'] for r in sources]),('tasks',[r['task_id'] for r in tasks])]},
 'reference_candidates':errors,'edges':edges,'asset_checks':assets,'raw_files':raw,
 'raw_byte_duplicates':[{'sha256':h,'paths':p} for h,p in by_hash.items() if len(p)>1],
 'transfer_mapping':mapping,'source_definitions':{k:[{'file':v['file'],'pointer':v['pointer']} for v in vs] for k,vs in definitions.items()},
 'document_groups':{g:[s['source_id'] for s in sources if s.get('document_group')==g] for g in sorted({s['document_group'] for s in sources if s.get('document_group')})},
 'unregistered_subjects':sorted({part for c in claims for part in c['subject'].split('/') if part not in B}),
 'measured_claims':[{'id':c['id'],'scope':c.get('scope'),'as_built_eligible':c.get('as_built_eligible')} for c in claims if c['evidence_class']=='measured'],
 'claims_without_provenance':[c['id'] for c in claims if not c.get('provenance')],
 'assembly_relations_without_provenance':[e['id'] for e in assembly['relations'] if not e.get('provenance')],
 'semantic_duplicate_candidates':[ids for ids in semantic.values() if len(ids)>1],
 'source_url_collisions':urls,'claim_support_cycles':cycles,
 'gap_tasks':{g['id']:[t['task_id'] for t in tasks if g['id'] in t.get('source_refs',[])] for g in gaps},
 'tasks_without_gap':[t['task_id'] for t in tasks if not G.intersection(t.get('source_refs',[]))],
 'evidence_classes':dict(collections.Counter(c['evidence_class'] for c in claims)),
 'claim_statuses':dict(collections.Counter(c.get('status','not-set') for c in claims)),
 'conflict_statuses':{f['id']:f['status'] for f in conflicts},
 'protected_inputs':{str(p.relative_to(root)):digest(p) for folder in ['data','src','evidence/contributions'] for p in sorted((root/folder).rglob('*')) if p.is_file()},
}
print(json.dumps(report,ensure_ascii=False,indent=2))
