"""Deterministic offscreen EGL renders of the exported Three.js triangles; no artist redraws."""
import os,json,hashlib,math
from pathlib import Path
import numpy as np
import moderngl
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[4];TMP=Path('/tmp/ks-iter003');OUT=ROOT/'state/reconstruction-loop/ITER-003/views';OUT.mkdir(exist_ok=True,parents=True)
W,H=1440,860
ctx=moderngl.create_standalone_context(backend='egl');ctx.enable(moderngl.DEPTH_TEST)
prog=ctx.program(vertex_shader='''#version 330
in vec3 position;in vec3 normal;in vec3 color;uniform mat4 vp;uniform mat4 model;out vec3 n;out vec3 c;out vec3 p;
void main(){vec4 w=model*vec4(position,1);p=w.xyz;n=mat3(model)*normal;c=color;gl_Position=vp*w;}
''',fragment_shader='''#version 330
in vec3 n;in vec3 c;in vec3 p;out vec4 frag;uniform vec4 clip;uniform int truth;uniform int water;uniform vec3 eye;
void main(){if(dot(clip.xyz,p)+clip.w>0.00001)discard;vec3 nn=normalize(n);if(!gl_FrontFacing)nn=-nn;
float diffuse=max(dot(nn,normalize(vec3(-3,-4,8))),0.0);float rim=max(dot(nn,normalize(vec3(4,2,3))),0.0);
float grain=truth==1?1.0:0.94+0.05*sin(320.0*p.x+4.0*sin(14.0*p.z))+0.015*sin(1040.0*p.x+7.0*p.y);
vec3 col=c*(0.48+0.48*diffuse+0.14*rim)*grain;
if(water==1){float ripple=sin(p.y*23+p.x*8)*sin(p.x*4-p.y*7);col=vec3(.34,.52,.58)*(0.90+.08*ripple);}
if(truth==0&&water==0&&p.z < -1.95)col*=.70;
frag=vec4(pow(max(col,vec3(0)),vec3(.85)),1);}
''')
fbo=ctx.simple_framebuffer((W,H),components=3,samples=4);resolved=ctx.simple_framebuffer((W,H),components=3)
fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font=lambda n:ImageFont.truetype(fontpath,n)
cache={}
def load(name):
 if name not in cache:
  data=np.fromfile(TMP/f'{name}.bin',dtype='f4').reshape(-1,9);buf=ctx.buffer(data.tobytes());vao=ctx.vertex_array(prog,[(buf,'3f 3f 3f','position','normal','color')]);meta=json.loads((TMP/f'{name}.json').read_text());cache[name]=(vao,meta,data,buf)
 return cache[name]
def normalize(x):return x/np.linalg.norm(x)
def matrix(cam):
 eye=np.array(cam['eye'],float);target=np.array(cam['target'],float);f=normalize(target-eye);up=np.array([0.,0,1.]);
 if abs(np.dot(f,up))>.999:up=np.array([0.,1.,0.])
 right=normalize(np.cross(f,up));up=np.cross(right,f);v=np.eye(4);v[0,:3]=right;v[1,:3]=up;v[2,:3]=-f;v[:3,3]=-v[:3,:3]@eye
 h=cam['height'];w=h*W/H;p=np.diag([2/w,2/h,-2/100,1.]);p[2,3]=-1
 return (p@v).astype('f4')
def select(m,f):
 fam=m.get('family','');name=m['name'];slot=m.get('slot',-1)
 if f=='all':return True
 if f=='moving':return not m.get('stationary')
 if f=='shaft-arms':return fam in ['COMP-SHAFT','COMP-ARMS']
 if f.startswith('bearing'):return (fam in ['COMP-SHAFT','COMP-SHAFT-CLAMPS','COMP-BEARINGS','COMP-BEARING-STANDS','COMP-TROUGH-SUPPORT']) and (fam=='COMP-SHAFT' or ((sum([m['bounds']['min'][0],m['bounds']['max'][0]])<0) if f.endswith('land') else (sum([m['bounds']['min'][0],m['bounds']['max'][0]])>0)))
 if f=='rim-detail':return ('LAND' in name and (fam in ['COMP-KRUEMMLINGE','COMP-SCHETTERNBRETTER','COMP-ARMS'] or 'SCHETTER-' in name or 'SEAT-' in name))
 if f=='local':return slot==0 or fam=='COMP-KRUEMMLINGE'
 if f=='cluster':return 0<=slot<=2 or fam=='COMP-KRUEMMLINGE' and 'LAND' in name
 if f=='frame':return m.get('stationary') and fam!='COMP-TROUGH'
 if f=='trough':return fam in ['COMP-TROUGH','COMP-CHANNEL','COMP-A-BOCK'] or 'TH-A-WEDGE' in name or 0<=slot<=2
 if f=='reference':return True
 return False
waterdata=np.array([[-7,-8,-1.95,0,0,1,.4,.6,.7],[7,-8,-1.95,0,0,1,.4,.6,.7],[7,8,-1.95,0,0,1,.4,.6,.7],[-7,-8,-1.95,0,0,1,.4,.6,.7],[7,8,-1.95,0,0,1,.4,.6,.7],[-7,8,-1.95,0,0,1,.4,.6,.7]],dtype='f4')
wb=ctx.buffer(waterdata.tobytes());wv=ctx.vertex_array(prog,[(wb,'3f 3f 3f','position','normal','color')])
def render(name,cam,truth=False,angle=0,operation=False):
 vao,meta,data,buf=load(name);fbo.use();fbo.clear(.951,.946,.928,1,depth=1);prog['vp'].write(matrix(cam).T.tobytes());prog['model'].write(np.eye(4,dtype='f4').T.tobytes());prog['clip'].value=tuple(cam.get('clip',[0,0,0,0]));prog['truth'].value=int(truth);prog['water'].value=0
 # eye is optimized out on some GL implementations.
 spin=np.eye(4,dtype='f4');spin[1:3,1:3]=[[math.cos(angle),-math.sin(angle)],[math.sin(angle),math.cos(angle)]]
 for m in meta:
  if not select(m,cam.get('filter','all')):continue
  prog['model'].write((np.eye(4,dtype='f4') if m.get('stationary') else spin).T.tobytes());ctx.wireframe=bool(truth and m.get('pitchStatus')=='candidate-not-truth');vao.render(vertices=m['count'],first=m['first']);ctx.wireframe=False
 if operation and not truth:
  prog['model'].write(np.eye(4,dtype='f4').T.tobytes());prog['water'].value=1;wv.render();prog['water'].value=0
 ctx.copy_framebuffer(resolved,fbo);im=Image.frombytes('RGB',(W,H),resolved.read(components=3,alignment=1)).transpose(Image.Transpose.FLIP_TOP_BOTTOM);return im

def plate(im,title,subtitle,truth=False,note='',footer=''):
 page=Image.new('RGB',(1440,1040),'#faf9f5');page.paste(im,(0,110));d=ImageDraw.Draw(page)
 d.text((38,20),title,font=font(27),fill='#24333b');d.text((38,61),subtitle,font=font(17),fill='#52646b')
 d.text((38,978),note,font=font(16),fill='#35434b');d.text((38,1009),footer or 'ITER-003 | Fachkorrekturen mit offenen Detailmaßen | Kein bestätigtes Ist-Aufmaß',font=font(14),fill='#66757b')
 if truth:
  d.rectangle((1010,26,1030,46),fill='#668e94');d.text((1042,27),'Topologie / Kandidat',font=font(15),fill='#35434b');d.rectangle((1010,57,1030,77),fill='#aeb6c1');d.text((1042,58),'historische / beobachtete Form',font=font(15),fill='#35434b')
 else:
  d.rectangle((1050,28,1070,48),fill='#ab8962');d.text((1082,27),'Holz · Kandidat',font=font(15),fill='#35434b');d.rectangle((1050,59,1070,79),fill='#656b69');d.text((1082,58),'Metall · Kandidat',font=font(15),fill='#35434b')
 return page


manifest=[]
cameras=json.loads((ROOT/'data/canonical-cameras.json').read_text())
for cam in cameras['views']:
 for mode in ['truth','brute']:
  name=mode+('-exploded' if cam.get('exploded') else '')
  im=render(name,cam,mode=='truth',cam.get('angle',0),cam.get('operation',False))
  note='Experten-Topologie; Detailmaße/Einbaupose teils Kandidaten. Kein aktuelles Feldaufmaß.'
  if mode=='truth' and cam['id'] in ['08','09','13','14','16']:note='Unregistrierter Standort / Betrieb bleibt in Truth ausgespart.'
  if cam['id']=='10':note='Eingefrorene Vergleichskamera zeigt jetzt Armsitz; neuer Stoß zusätzlich in Detail D1.'
  page=plate(im,f"{cam['id']}  {cam['title']}",mode.upper()+' · Vergleichskamera aus ITER-001 unverändert',mode=='truth',note)
  path=OUT/f"{cam['id']}-{mode}.jpg";page.save(path,quality=88);manifest.append({'path':str(path.relative_to(ROOT)),'mode':mode,'camera':cam,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
  print(path.name,flush=True)
details=[
 ('D1','Krümmlingstoß / vier gegenläufige Nägel',[-4,-3,4],[-.97,1.0275,1.779],1.20,'rim-detail'),
 ('D2','Armsitz / lokale Verstärkung / Keile',[-4,-3,4],[-.97,0,2.13],.70,'rim-detail'),
 ('D3','Flügelbrett / U-Holzband',[-4,-4,4],[-.65,-.27,2.30],1.80,'local'),
 ('D4','Welle / Schellen / Holzlager',[-4,-4,2],[-1.85,0,0],1.20,'bearing-land'),
 ('D5','Kumpfnägel / poseabhängige Pfade',[-4,-4,4],[-1.2,-.25,2.08],1.6,'local'),
 ('D6','Radbock / oberer Querbalken',[-4,-4,2],[-1.94,0,.08],1.65,'frame'),
 ('D7','A-Bock / Rinnenstoß',[-5,-6,3],[-2.92,1.25,1.0],2.7,'trough')]
for id,title,eye,target,height,filter in details:
 cam={'id':id,'eye':eye,'target':target,'height':height,'filter':filter};page=plate(render('brute',cam),id+' '+title,'ERGÄNZENDE DETAILKAMERA · ITER-003',False,'Topologie korrigiert; unbekannte Detailmaße und Standort bleiben gekennzeichnete Kandidaten.')
 path=OUT/f'{id}-detail.jpg';page.save(path,quality=90);manifest.append({'path':str(path.relative_to(ROOT)),'mode':'brute','camera':cam,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(OUT/'manifest.json').write_text(json.dumps({'renderer':ctx.info['GL_RENDERER'],'source':'actual runtime triangles with depth buffer','views':manifest},indent=2))
for mode in ['truth','brute']:
 contact=Image.new('RGB',(1440,1040),'white')
 for j,cam in enumerate(cameras['views']):
  im=Image.open(OUT/f"{cam['id']}-{mode}.jpg");im.thumbnail((360,260));contact.paste(im,((j%4)*360,(j//4)*260))
 contact.save(OUT/f'contact-{mode}.jpg',quality=92)
