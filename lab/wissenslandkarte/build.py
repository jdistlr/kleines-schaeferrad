"""Read-only projection of semantic-reference-v1. No canonical writes."""
import json,hashlib,base64,io
from pathlib import Path
from PIL import Image,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
BASE='f2bf574c6c6fed3a64ac0073823cd07ac24ee537'
def read(p):return json.loads((ROOT/p).read_text())
def thumb(p,size):
 im=ImageOps.exif_transpose(Image.open(ROOT/p));im.thumbnail(size);o=io.BytesIO();im.convert('RGB').save(o,format='JPEG',quality=57);return 'data:image/jpeg;base64,'+base64.b64encode(o.getvalue()).decode()
cases=read('state/evidence-consolidation/20261010/semantic-reference-v1/reference-cases.json')['cases']
claims=read('data/geometry.claims.json')['claims'];ids={i for c in cases for i in c['claims']};selected=[c for c in claims if c['id'] in ids]
assets=read('evidence/manifest.json')['assets']+read('evidence/additions-v2.json')['assets'];analyses=read('data/source-analyses.json')['sources']
sourceids={p['source_id'] for c in selected for p in c['provenance']}
sources={s['source_id']:s for s in analyses if s['source_id'] in sourceids}
for sid,s in sources.items():
 a=next((a for a in assets if a['id']==sid),None)
 path=(a or {}).get('archive',{}).get('path')
 if path:
  s['path']=path;s['sha256']=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
  if Path(path).suffix.lower() in ['.jpeg','.jpg','.png']:s['thumbnail']=thumb(path,(300,300))
 if not path:
  for f in sorted((ROOT/'evidence/contributions').glob('*.json')):
   if sid in f.read_text():s['path']=str(f.relative_to(ROOT));break
D={'baseline':BASE,'cases':cases,'claims':selected,'sources':sources,'components':read('data/components.json')['components'],'gaps':read('data/knowledge-gaps.json')['gaps'],'tasks':read('data/field-tasks.json')['tasks'],'conflicts':read('data/conflicts.json')['conflicts'],'overview':thumb('evidence/raw/IMG_6812.jpeg',(780,620))}
template=(HERE/'view.html').read_text();fragment=template.replace('/*DATA*/',json.dumps(D,ensure_ascii=False).replace('</','<\\/'))
(HERE/'preview.html').write_text(fragment)
(HERE/'index.html').write_text('<!doctype html><html lang="de"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Schäferrad · Wissenslabor</title><body style="margin:0">'+fragment+'</body></html>')
print(json.dumps({'claims':len(selected),'sources':len(sources),'bytes':len(fragment.encode()),'baseline':BASE}))
