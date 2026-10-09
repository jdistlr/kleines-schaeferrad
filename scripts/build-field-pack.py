"""A3 technical capture pack: mesh-derived projections plus original-photo overlays."""
from pathlib import Path
import json, hashlib, shutil, math, io, base64, gzip
from xml.sax.saxutils import escape
from PIL import Image, ImageOps, ImageEnhance
from reportlab.pdfgen import canvas
from reportlab import rl_config
rl_config.useA85=0
from reportlab.lib.pagesizes import A3,A4,landscape
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'output/pdf';OUT.mkdir(parents=True,exist_ok=True)
PUBLIC=ROOT/'public/field-pack';PUBLIC.mkdir(parents=True,exist_ok=True)
VIS=ROOT/'public/field-visuals';VIS.mkdir(parents=True,exist_ok=True)
D=json.loads(gzip.decompress((ROOT/'docs/field-kit/model-projections.json.gz').read_bytes()));sheets=D['sheets']
T=json.loads((ROOT/'data/field-tasks.json').read_text());G=json.loads((ROOT/'data/visual-guides.json').read_text())
E=json.loads((ROOT/'data/pre-disassembly-evidence-gate.json').read_text())
for sheet in sheets:
 if sheet['id'] in E['sheet_notes']:sheet['notes']=E['sheet_notes'][sheet['id']]
 if sheet['id']=='KS-31':sheet['title']='Kumpfnägel: Wege und Nachbarüberlappung'
for name,file in [('KS','DejaVuSans.ttf'),('KSB','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
W,H=420,297
c=canvas.Canvas(str(OUT/'KS-Werkstatt-Aufnahmeplan-A3.pdf'),pagesize=landscape(A3),invariant=1,pageCompression=1)
c.setTitle(f'Kleines Schäferrad · Technischer Aufnahmeplan {D["iteration"]}');c.setAuthor('Kleines Schäferrad')
def line(a,b,color='#333333',width=.3,dash=None):
 c.setStrokeColor(color);c.setLineWidth(width*mm);c.setDash(*([1.7*mm,1*mm] if dash else []));c.line(a[0]*mm,a[1]*mm,b[0]*mm,b[1]*mm);c.setDash()
def text(s,x,y,size=3.4,bold=False,color='#292d2d'):
 c.setFillColor(color);c.setFont('KSB' if bold else 'KS',size*mm);c.drawString(x*mm,y*mm,s)
def wrap(s,x,y,w,size=3.2):
 words=s.split();buf='';h=size*1.5
 for word in words:
  test=(buf+' '+word).strip()
  if pdfmetrics.stringWidth(test,'KS',size*mm)>w*mm and buf:text(buf,x,y,size);y-=h;buf=word
  else:buf=test
 if buf:text(buf,x,y,size);y-=h
 return y
photos={}
# Per-photo locations in EXIF-oriented coordinates; circles locate a region, never a metric endpoint.
photo_locations={
 'IMG_6812.jpeg':[(.46,.52),(.55,.88)],
 'IMG_6808-upload2.jpeg':[(.50,.64),(.43,.42)],
 'IMG_6804.jpeg':[(.50,.60),(.31,.73)],
 'IMG_6809.jpeg':[(.40,.39),(.54,.60)],
 'IMG_6811.jpeg':[(.47,.38),(.39,.49)],
 'IMG_6822.jpeg':[(.35,.54),(.69,.65)]
}
def photo(name,rect,overlay=False,locations=None):
 if name not in photos:
  p=ROOT/'evidence/raw'/name
  if not p.exists():p=ROOT/name
  if not p.exists():raise FileNotFoundError(p)
  im=ImageOps.exif_transpose(Image.open(p)).convert('RGB');im.thumbnail((1600,1600))
  # Print-only exposure compensation for dark synthetic render plates; originals unchanged.
  if name.startswith('output/calibration/'):
   im=ImageEnhance.Brightness(im).enhance(1.42)
   im=ImageEnhance.Contrast(im).enhance(1.08)
  photos[name]=im
 im=photos[name];x,y,w,h=rect;scale=min(w/im.width,h/im.height);iw,ih=im.width*scale,im.height*scale;px=x+(w-iw)/2;py=y+(h-ih)/2
 buf=io.BytesIO();im.save(buf,format='JPEG',quality=88);buf.seek(0);c.drawImage(ImageReader(buf),px*mm,py*mm,iw*mm,ih*mm)
 if overlay:
  for i,(u,v) in enumerate(locations if locations is not None else photo_locations.get(name,[]),1):
   xx,yy=px+u*iw,py+(1-v)*ih;c.setFillColor('#fff8e8');c.setStrokeColor('#a56f27');c.circle(xx*mm,yy*mm,2.2*mm,fill=1,stroke=1);text(str(i),xx-.7,yy-.9,2.6,True)
 return im

def project(v,rect):
 pr=v['projection'];x,y,w,h=rect;a,b,d,e=pr['bounds'];scale=min((w-8)/max(b-a,.001),(h-12)/max(e-d,.001));xy=lambda p:(x+w/2+(p[0]-(a+b)/2)*scale,y+h/2+(p[1]-(d+e)/2)*scale)
 # Centerlines through projected mechanical origin, with standard dash-dot convention.
 cam=pr['camera'];ox,oy=xy((cam[12],cam[13]));c.setDash([4*mm,1*mm,.7*mm,1*mm]);c.setStrokeColor('#a7aaa8');c.setLineWidth(.16*mm)
 if y<oy<y+h:c.line(x*mm,oy*mm,(x+w)*mm,oy*mm)
 if x<ox<x+w:c.line(ox*mm,y*mm,ox*mm,(y+h)*mm)
 c.setDash()
 if pr.get('waterline'):
  wa,wb=map(xy,pr['waterline']);line(wa,wb,'#5a8496',.5,True);text('Wasserlinie · Arbeitsannahme',x+2,wa[1]+2,2.6,color='#3d687a')
 for kind in ['hidden','visible']:
  for seg in pr[kind]:line(xy(seg['p'][0]),xy(seg['p'][1]),'#ad7b32' if seg['candidate'] else '#929592' if kind=='hidden' else '#252a2b',.17 if kind=='hidden' else .32,kind=='hidden')
 for seg in pr['cuts']:line(xy(seg[0]),xy(seg[1]),'#a56f27',.65)
 for seg in pr.get('hatch',[]):line(xy(seg[0]),xy(seg[1]),'#9f8055',.18)
 if pr.get('measure'):
  p,q=map(xy,pr['measure']);dx,dy=q[0]-p[0],q[1]-p[1];L=math.hypot(dx,dy)
  if L>.1:
   nx,ny=-dy/L*5,dx/L*5;aa=(p[0]+nx,p[1]+ny);bb=(q[0]+nx,q[1]+ny);line(p,aa,'#a56f27',.2);line(q,bb,'#a56f27',.2);line(aa,bb,'#a56f27',.25)
   for start,end in [(aa,bb),(bb,aa)]:
    ang=math.atan2(end[1]-start[1],end[0]-start[0]);path=c.beginPath();path.moveTo(start[0]*mm,start[1]*mm)
    for sg in[-1,1]:path.lineTo((start[0]+math.cos(ang+sg*.38)*2.7)*mm,(start[1]+math.sin(ang+sg*.38)*2.7)*mm)
    path.close();c.setFillColor('#a56f27');c.drawPath(path,fill=1,stroke=0)
  text(v.get('measureLabel','Ist-Maß: ____ mm'),x+2,y-3,3.1)

pages=[]
for i,s in enumerate(sheets):
 if i:c.showPage()
 text('KLEINES SCHÄFERRAD',13,283,3.3,True);text(s['id'],370,283,4.2,True);text(s['title'],13,269,7,True);wrap(s['action'],13,257,394,3.5)
 if s['id']=='KS-70':
  events=[('Welle innen','IMG_6808-upload2.jpeg','STOPP vor erstem Keilzug','Danach: Innenraum, Eintritt / Austritt und Tiefe.'),('Kumpfnägel / Nachbarn','IMG_6809.jpeg','STOPP vor Herausziehen','Danach: beide Wege, Köpfe, Sitze und Partner.'),('Lagerkontakt','IMG_6804.jpeg','STOPP vor Entlastung','Danach: Zapfen und Kontaktfläche, beidseitig.'),('Krümmlingstoß','IMG_6804.jpeg','STOPP vor Trennen','Danach: beide Stoßflächen, Löcher und Partner.'),('Wasserübergabe','IMG_6812.jpeg','Vor Stillsetzen filmen','Aufnahme unten, Heben, Trog und Rinne gemeinsam.')]
  for k,(title,file,before,after) in enumerate(events):
   col=k%3;row=k//3;xx=13+col*133;yy=143-row*107
   text(f'{k+1} · {title}',xx,yy+91,3.8,True);photo(file,(xx,yy+26,125,60),True,{'Krümmlingstoß':[(.51,.12),(.67,.33)],'Wasserübergabe':[(.64,.29),(.51,.85)]}.get(title))
   wrap(before,xx,yy+20,125,3.1);wrap(after,xx,yy+11,125,3.0)
  text('Je Ereignis festhalten',280,112,4,True)
  for k,tx in enumerate(['Teil / Partner: __________________','Foto vorher: __________________','Foto danach: __________________','Maß / Werkzeug: ______________','Person / Reihenfolge: __________','Sicherung geprüft: _____________']):text(tx,280,99-k*11,3.2)
  line((13,19),(407,19),'#9da5a0',.25);text(f'{D["iteration"]} · {i+1:02}/{len(sheets)} · A3 quer · Aufnahmebereiche, keine Perspektivmaße',13,13,2.7);text('Originalfotos / Samstagplan · tatsächliche Kontaktstellen nah ergänzen',13,7,2.7)
  pages.append({'page':i+1,'code':s['id'],'title':s['title'],'visual':'five-original-photo-event-panels','status':'REVIEW_REQUIRED'})
  continue
 n=len(s['views']);ww=394/n
 # Existing source and canonical images only: no new geometry or reconstruction render.
 decision_images={
  'KS-11':['evidence/raw/IMG_6856.jpeg','output/calibration/ITER-001/canonical/07-truth.png'],
  'KS-30':['evidence/raw/1000046420.jpg','evidence/raw/1000046421.jpg','evidence/raw/1000046422.jpg'],
  'KS-31':['evidence/raw/IMG_6809.jpeg','output/calibration/ITER-001/comparisons/06-nail-candidates-ABC.png'],
  'KS-40':['evidence/raw/IMG_6854.jpeg','output/calibration/ITER-001/comparisons/03-paddle-v2-v3.png'],
  'KS-51':['evidence/raw/IMG_6812.jpeg','output/calibration/ITER-001/operation/pickup-lift-discharge-channel.jpg']}
 imgs=decision_images.get(s['id'])
 if imgs:
  for k,img in enumerate(imgs):
   xx=13+k*394/len(imgs);wwi=394/len(imgs)-6
   text(('ORIGINALQUELLE' if img.startswith('evidence/') else 'ITER-001 · ÄLTERER KANDIDAT / UNBESTÄTIGT'),xx,242,3.2,True)
   photo(img,(xx,100,wwi,135));wrap(Path(img).name,xx,96,wwi,2.5)
  text('Entscheidung offen: am realen Teil zeigen und mit Messreferenz aufnehmen.',13,84,3.3,True)
 # Retain existing frozen projections on other pages.

 for j,v in enumerate([] if imgs else s['views']):
  xx=13+j*ww;text(v['label'],xx,243,3.5,True)
  if s['id']=='KS-31' and j==0:
   photo(s['photo'],(xx,91,ww-6,145));text('Beobachtetes Stiftpaar · unbemaßte Originalaufnahme',xx,86,3)
  else:project(v,(xx,91,ww-6,145))
 line((13,78),(407,78),'#bcc1bc',.2)
 note_x=13;note_w=394
 if s.get('photo'):
  photo(s['photo'],(13,27,88,45),True,[(.51,.12),(.67,.33)] if s['id']=='KS-20' else None);text('Foto: Arbeitsbereich 1 / Umfeld 2',13,23,2.6);note_x=109;note_w=298
 yy=69
 for note in s['notes']:yy=wrap(note,note_x,yy,note_w,3.4)-2
 text('Teil / Partner: ___________________    Maß / Werkzeug: ___________________',note_x,max(yy-3,37),3.2)
 line((note_x,29),(407,29),'#bcc1bc',.2);text('Person / Datum / Reihenfolge: __________________________________________',note_x,24,3)
 line((13,19),(407,19),'#9da5a0',.25);text(f'{D["iteration"]} · {i+1:02}/{len(sheets)} · A3 quer · 09.10.2026 · nicht maßhaltig',13,13,2.7)
 text('TRUTH CRITIC · OFFEN · keine Demontagefreigabe',190,13,2.7)
 wrap(('Quellen: '+', '.join(imgs)) if imgs else s['source'],13,7,390,2.3)
 pages.append({'page':i+1,'code':s['id'],'title':s['title'],'visual':'existing-source-and-candidate-decision-view' if imgs else 'frozen-mesh-projection / original-photo','status':'REVIEW_REQUIRED'})
c.save()
# Guides retain task identity but discard obsolete primitives and their unrelated coordinates.
photo_specs={
 'GUIDE-SYSTEM':('IMG_6812.jpeg',[(.46,.52,'1'),(.55,.88,'2'),(.26,.63,'3')],['1 · Gesamtes Rad und Tragwerk','2 · Wasserlinie mit Achsbezug','3 · Feste Referenzen am Rahmen']),
 'GUIDE-ARM-BEFORE':('IMG_6808-upload2.jpeg',[(.50,.64,'1'),(.43,.42,'2'),(.56,.76,'3')],['1 · Welle und Eintrittsstelle','2 · Axiale Armstaffelung','3 · Lagerumfeld; Kontakt zusätzlich nah']),
 'GUIDE-RIM':('IMG_6804.jpeg',[(.51,.12,'1'),(.67,.33,'2'),(.47,.55,'3')],['1 · Kranzstöße beidseitig aufnehmen','2 · Radiale Tiefe / axiale Breite trennen','3 · Orientierung zur Welle halten']),
 'GUIDE-KUMPF':('IMG_6809.jpeg',[(.40,.39,'1'),(.54,.60,'2'),(.79,.47,'3')],['1 · Dauben und Reifen','2 · Sichtbaren Holzkopf und Gegenseite aufnehmen','3 · Benachbarte Schaufel mit im Bild']),
 'GUIDE-PADDLE':('IMG_6811.jpeg',[(.47,.38,'1'),(.39,.49,'2'),(.41,.61,'3')],['1 · Schaufel mit Kumpf','2 · Befestigung und Orientierung','3 · Kranz als Bezug halten']),
 'GUIDE-CONTEXT':('IMG_6804.jpeg',[(.50,.60,'1'),(.31,.73,'2'),(.68,.79,'3')],['1 · Wellenauflager: näher fotografieren','2 · Untere Rahmenverbindung','3 · Pfosten / Strebe / Grundholz gemeinsam']),
 'GUIDE-WATER-SCAN':('IMG_6812.jpeg',[(.64,.29,'1'),(.51,.85,'2'),(.26,.57,'3')],['1 · Übergabe oben und Trog gesondert filmen','2 · Wasserlinie zur Achse messen','3 · Drei bleibende Referenzen und Kontrollmaß'])}
for g in G['guides']:
 name=photo_specs.get(g['id'])
 if name:
  file,markers,labels=name;im=ImageOps.exif_transpose(Image.open(ROOT/'evidence/raw'/file)).convert('RGB');im.thumbnail((1400,1100));im.save(VIS/(g['id']+'.jpg'),quality=88);ww,hh=im.size;encoded=base64.b64encode((VIS/(g['id']+'.jpg')).read_bytes()).decode('ascii');data_url='data:image/jpeg;base64,'+encoded
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {ww} {hh}" role="img"><title>{escape(g["title"])}</title><image href="{data_url}" xlink:href="{data_url}" width="{ww}" height="{hh}"/>'
  for u,v,num in markers:
   x,y=u*ww,v*hh;r=max(16,ww*.018);svg+=f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff8e8" stroke="#93601b" stroke-width="3"/><text x="{x}" y="{y+r*.34}" text-anchor="middle" font-family="sans-serif" font-size="{r*1.1}" font-weight="bold">{num}</text>'
  svg+='</svg>';(VIS/(g['id']+'.svg')).write_text(svg)
  g['labels']=labels;g['visual_kind']='current-photo-overlay';g['photo_source']=file
 else:
  # Preserve checked-in frozen field projection; do not trigger geometry export.
  frozen=VIS/(g['id']+'.svg')
  if not frozen.exists():raise FileNotFoundError(frozen)
  g['labels']=['Drei geometrische Innenkandidaten im gleichen Blick','Nach Öffnung: beide Partnerflächen und Einstecktiefe','Aktuellen Arm mit gerader Latte vollständig aufnehmen'];g['visual_kind']='shared-geometry-projection'
 g['visual_asset']='field-visuals/'+g['id']+'.svg';g['note']='Aufnahmepunkte markieren Arbeitsbereiche, keine fotogrammetrischen Maße.' if name else 'Geometrische Kandidaten; keine bestätigte Innenverbindung.'
 g.pop('primitives',None);g.pop('callouts',None)
(ROOT/'data/visual-guides.json').write_text(json.dumps(G,ensure_ascii=False,indent=2)+'\n')
# Two-page concise A4 route, same task-to-sheet mapping.
A=canvas.Canvas(str(OUT/'KS-Kurzplan-A4.pdf'),pagesize=landscape(A4),invariant=1,pageCompression=1);gmap={g['id']:g for g in G['guides']}
route=[next(t for t in T['tasks'] if t['task_id']==p['task_id']) for p in E['priorities']]
for page in range(2):
 if page:A.showPage()
 A.setFont('KSB',17);A.drawString(12*mm,191*mm,'Kleines Schäferrad · Aufnahmefolge')
 A.setFont('KS',8);A.drawString(12*mm,10*mm,D['iteration']+' · Keine Ist-Maße / keine Demontagefreigabe');A.drawString(12*mm,181*mm,'Reihenfolge mit den Monteuren abstimmen. Erst aufnehmen, dann lösen.')
 for j,t in enumerate(route[page*11:(page+1)*11]):
  yy=(167-j*12)*mm;A.setFont('KSB',9);A.drawString(12*mm,yy,('KS-30/31' if t['task_id']=='TASK-KUM-BEFORE' else gmap[G['task_visual_map'][t['task_id']]]['sheet']));A.setFont('KS',9);A.drawString(38*mm,yy,(t['capture_priority']['priority']+' '+t['title'])[:78])
  A.setFont('KS',7);A.drawString(38*mm,yy-4*mm,t['capture_priority']['window']+' | '+t['task_id'])
 A.setFont('KS',8);A.drawString(12*mm,20*mm,'Abschluss: Partner zugeordnet · Originale gesichert · Sicherung auf zweitem Gerät geöffnet')
A.save()
manifest={'schema':'ks-field-pack/v2','iteration':D['iteration'],'geometry_dependencies':D['geometry_dependencies'],'task_source':'data/field-tasks.json','task_source_sha256':hashlib.sha256((ROOT/'data/field-tasks.json').read_bytes()).hexdigest(),'visual_source':'data/visual-guides.json','visual_source_sha256':hashlib.sha256((ROOT/'data/visual-guides.json').read_bytes()).hexdigest(),'task_ids':[t['task_id'] for t in T['tasks']],'task_to_sheet':{tid:gmap[gid]['sheet'] for tid,gid in G['task_visual_map'].items()},'task_additional_sheets':{'TASK-KUM-BEFORE':['KS-31']},'evidence_gate_source':'data/pre-disassembly-evidence-gate.json','evidence_gate_sha256':hashlib.sha256((ROOT/'data/pre-disassembly-evidence-gate.json').read_bytes()).hexdigest(),'pages':pages,'format':'A3 landscape','physical_instances_precreated':0,'geometry_sha256':D['geometry_sha256'],'quality_gate':'PENDING_VISUAL_AUDIT'}
review_path=ROOT/'state/reconstruction/quality-review.json'
if review_path.exists():
 review=json.loads(review_path.read_text())
 if review.get('pdf_sha256')==hashlib.sha256((OUT/'KS-Werkstatt-Aufnahmeplan-A3.pdf').read_bytes()).hexdigest() and review.get('geometry_sha256')==D['geometry_sha256'] and review.get('drawing_verdict')=='TECHNICAL DRAWING QUALITY PASS':
  manifest['quality_gate']='TECHNICAL DRAWING QUALITY PASS'
  manifest['review']='state/reconstruction/quality-review.json'
  for page in manifest['pages']:page['status']='VISUALLY_REVIEWED'
critic_review=ROOT/'state/reconstruction-loop/ITER-001/truth-critic/pdf-visual-review.json'
if critic_review.exists():
 review=json.loads(critic_review.read_text())
 if review.get('pdf_sha256')==hashlib.sha256((OUT/'KS-Werkstatt-Aufnahmeplan-A3.pdf').read_bytes()).hexdigest() and review.get('a4_sha256')==hashlib.sha256((OUT/'KS-Kurzplan-A4.pdf').read_bytes()).hexdigest() and review.get('verdict')=='VISUAL REVIEW PASS':
  manifest['quality_gate']='EVIDENCE CAPTURE LAYOUT REVIEWED'
  manifest['review']='state/reconstruction-loop/ITER-001/truth-critic/pdf-visual-review.json'
  for page in manifest['pages']:page['status']='VISUALLY_REVIEWED'
(ROOT/'docs/field-kit/field-pack-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
for name in['KS-Werkstatt-Aufnahmeplan-A3.pdf','KS-Kurzplan-A4.pdf']:shutil.copyfile(OUT/name,PUBLIC/name)
shutil.copyfile(OUT/'KS-Werkstatt-Aufnahmeplan-A3.pdf',PUBLIC/'KS-Field-Pack-A3.pdf');shutil.copyfile(OUT/'KS-Kurzplan-A4.pdf',PUBLIC/'KS-Einsatzleitung-A4.pdf');shutil.copyfile(OUT/'KS-Werkstatt-Aufnahmeplan-A3.pdf',OUT/'KS-Field-Pack-A3.pdf');shutil.copyfile(OUT/'KS-Kurzplan-A4.pdf',OUT/'KS-Einsatzleitung-A4.pdf')
print('Generated 11 A3 technical sheets, 2 A4 route pages and 8 evidence-based field visuals.')
