"""Reproduce contact sheets/crops from repository originals; no retouching."""
from pathlib import Path
from collections import defaultdict
import json
from PIL import Image,ImageOps,ImageDraw
ROOT=Path(__file__).resolve().parents[4]; O=ROOT/'state/reconstruction-loop/ITER-002/evidence'
groups=defaultdict(list)
for p in json.loads((ROOT/'evidence/contributions/thorsten-20261009-photos.json').read_text())['images']:groups[p['group']].append(p['path'])
groups['historical']=[f'evidence/raw/IMG_{n}.jpeg' for n in [6828,6829,6830,6848,6849,6850,6851,6852]]
for group,paths in groups.items():
 paths=sorted(paths)
 for start in range(0,len(paths),4):
  batch=paths[start:start+4]; canvas=Image.new('RGB',(1600,2100),'white'); draw=ImageDraw.Draw(canvas)
  for i,path in enumerate(batch):
   src=ImageOps.exif_transpose(Image.open(ROOT/path)).convert('RGB');src.thumbnail((770,990));x=(i%2)*800;y=(i//2)*1050;draw.text((x+10,y+10),Path(path).name,fill='black');canvas.paste(src,(x+(800-src.width)//2,y+40))
  canvas.save(O/f'{group}-{start//4+1}.jpg',quality=90)
for c in json.loads((O/'crop-regions.json').read_text()):
 im=ImageOps.exif_transpose(Image.open(ROOT/c['source'])).crop(c['box_xyxy']);im=im.rotate(c.get('rotation_deg',0),expand=True);im=im.resize((int(im.width*c['scale']),int(im.height*c['scale'])),Image.Resampling.LANCZOS);im.save(O/c['crop'])
