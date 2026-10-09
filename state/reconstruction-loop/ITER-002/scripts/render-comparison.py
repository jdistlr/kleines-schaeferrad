"""Orthographic projections of unchanged runtime triangles beside original photos.
No new geometry, no pose fitting, no inferred hidden parts. Painter's algorithm;
use the mesh registers/code for numeric conclusions, not apparent occlusion.
"""
from pathlib import Path
import json,textwrap
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[4];OUT=ROOT/'state/reconstruction-loop/ITER-002';fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def font(n):return ImageFont.truetype(fontpath,n)
D={k:np.fromfile('/tmp/iter002-'+k+'.bin',dtype='f4').reshape(-1,9) for k in ['brute','truth','nail-reference']}
M={k:json.loads((OUT/f'evidence/{k}-mesh-register.json').read_text()) for k in D}
def render(key,pred,eye):
 chosen=[m for m in M[key] if pred(m)];data=np.concatenate([D[key][m['first']:m['first']+m['count']] for m in chosen]);tris=data.reshape(-1,3,9);v=tris[:,:,:3];cent=(v.min(axis=(0,1))+v.max(axis=(0,1)))/2
 f=np.array(eye,float);f=f/np.linalg.norm(f);up=np.array([0,0,1.]);right=np.cross(up,f);right/=np.linalg.norm(right);up=np.cross(f,right);basis=np.array([right,up,f]);q=(v-cent)@basis.T;lo=q[:,:,:2].min(axis=(0,1));hi=q[:,:,:2].max(axis=(0,1));scale=min(810/max(hi[0]-lo[0],.01),720/max(hi[1]-lo[1],.01));mid=(lo+hi)/2;xy=(q[:,:,:2]-mid)*scale;xy[:,:,0]+=450;xy[:,:,1]=410-xy[:,:,1]
 norm=tris[:,:,3:6].mean(axis=1);light=np.array([-1,-2,4.]);light/=np.linalg.norm(light);shade=.48+.48*np.abs(norm@light);col=(np.clip(tris[:,:,6:9].mean(axis=1)*shade[:,None],0,1)*255).astype(int);im=Image.new('RGB',(900,800),'#f2f0e9');d=ImageDraw.Draw(im)
 for i in np.argsort(q[:,:,2].mean(axis=1)):d.polygon([tuple(p) for p in xy[i]],fill=tuple(col[i]))
 return im,[m['name'] for m in chosen]
specs=[
('01-kranz-arme','Kranz / Arme: Segmentphase',lambda m:m['family'] in ['COMP-ARMS','COMP-KRUEMMLINGE'],[-1,-.1,.12],'image-1791540525839.jpg',['Ist: Armenden liegen an Sektorgrenzen; lokale Verstärkung fehlt.','Fachbeitrag: Arm in Segmentmitte; zwei Keile und rückseitiger Stift.','Nächster Schritt: Phase um 30° relativ zu Armen prüfen, Anschluss separat aufbauen.']),
('02-schettern','Krümmlingstoß / Schetternbretter',lambda m:(m['family']=='COMP-KRUEMMLINGE' and m['name'].endswith('LAND-01')) or 'RIM-PIN-LAND-0' in m['name'],[-3,-1,1],'image-1791542766365.jpg',['Ist: nackter Sektor mit synthetischen Bohrungen / Stiften; keine Stoßbretter.','Foto: Brett auf beiden Seiten, Köpfe und verkeilte Enden in Gegenansichten.','Vier Nägel, zwei je Richtung: Fachangabe; Lochbilder nach Ausbau dokumentieren.']),
('03-fluegelband','Flügelbrett / U-Holzband',lambda m:m['family']=='COMP-PADDLES' and m.get('slot')==0,[-2,-3,2],'image-1791541421696.jpg',['Ist: unverjüngter Quader, 1,29 × 0,055 × 0,43 m in Modellkoordinaten.','Foto: U-Band über Brett; Anschrägung in 1278244 sichtbar.','Breite etwa 0,35 m; Gesamtlänge / Pitch / Überstand separat klären.']),
('04-welle-lager','Welle / Dorn / Holzlager',lambda m:m['family'] in ['COMP-SHAFT','COMP-BEARINGS','COMP-BEARING-STANDS'],[-3,-6,2],'image-1791541561160.jpg',['Ist: verjüngte Holzwelle, Metalllager-Kandidat; vier Schellen fehlen.','Foto: Holz bleibt bis zum beschlagenen Ende stark; Dorn zwischen Lagerhölzern.','Dorn-/Kontaktmaße offen; keine durchgehende innere Metallwelle behaupten.']),
('05-kumpfnaegel','Kumpfnägel: Geometrie und Maßbezug',lambda m:m['family']=='COMP-KUMPF-NAILS',[-1,-3,1],'image-1791542499680.jpg',['Ist: Ø18-mm-Schäfte / Ø48-mm-Köpfe; 726 / 595 mm Endpunktsehnen.','Fachangabe: Ø26-mm-Schaft / Ø40-mm-Kopf; Foto zeigt stärkere Krümmung.','Foto-Projektion und Bogenlänge nicht gleichsetzen; Nagelpfade neu ableiten.']),
('06-bock-rad','Bock am Rad / Radstadt',lambda m:m.get('stationary') and m['family']!='COMP-TROUGH',[-4,-5,3],'image-1791542172733.jpg',['Ist: synthetisches Rahmensystem mit 0,23-/0,24-m-Hölzern.','Foto: Querbalken über Stützen, ausgeklinkte / verkeilte Anschlüsse.','Fachmaße: Querbalken 1,20 m, Querschnitt 14 × 14 cm; lokale Symmetrie prüfen.']),
('07-abock-rinne','A-Bock / zweiteilige Rinne',lambda m:m['family']=='COMP-TROUGH' or 'CHANNEL-SUPPORT' in m['name'],[-5,-6,3],'image-1791543487137.jpg',['Ist: eine Ableitung plus zwei senkrechte Stützen; kein A-Bock.','Foto: geneigte Beine, Riegel mit Keilen, Stoßlasche an Rinne.','Fachmaß 80 cm betrifft Unterseite Rinnenboden über lokalem Boden.'])]
manifest=[]
for stem,title,pred,eye,photo,notes in specs:
 key='nail-reference' if stem.startswith('05') else 'brute';im,names=render(key,pred,eye);page=Image.new('RGB',(1800,1180),'#faf9f5');d=ImageDraw.Draw(page);d.text((30,18),title,font=font(30),fill='#263a43');d.text((30,65),'IST: unveränderte Laufzeitgeometrie',font=font(21),fill='#596970');d.text((930,65),'QUELLE: Originalfoto, eigenständige Perspektive',font=font(21),fill='#596970');page.paste(im,(0,110));src=ROOT/'evidence/raw/thorsten-20261009'/photo;pi=ImageOps.exif_transpose(Image.open(src));pi.thumbnail((870,800));page.paste(pi,(900+(900-pi.width)//2,110+(800-pi.height)//2));d.text((925,925),photo,font=font(18),fill='#596970')
 for j,n in enumerate(notes):d.text((30,970+j*43),n,font=font(21),fill='#263a43')
 d.text((30,1115),'ITER-002 • Vergleich, keine Modellkorrektur • f7b9185 • Bildpaar ist kein metrisches Foto-Overlay',font=font(19),fill='#596970');p=OUT/'views'/f'{stem}.png';page.save(p);manifest.append({'path':str(p.relative_to(ROOT)),'source':str(src.relative_to(ROOT)),'model':key,'mesh_names':names,'eye_direction':eye,'projection':'orthographic-auto-fit','renderer':'actual runtime triangles; depth-sorted PIL projection','photo_alignment':'none','notes':notes})
(OUT/'views/manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
print('Rendered',len(specs),'comparison plates')
