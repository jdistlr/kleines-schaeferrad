from pathlib import Path
import json,hashlib,struct
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[4];OUT=ROOT/'state/reconstruction-loop/ITER-002'
p=ROOT/'evidence/raw/Scaniverse 2026-10-07 173556.ply';b=p.read_bytes();end=b.index(b'end_header\n')+len(b'end_header\n');dt=np.dtype([('x','<f4'),('y','<f4'),('z','<f4'),('r','u1'),('g','u1'),('b','u1')]);a=np.frombuffer(b[end:],dt);xyz=np.array([a[k] for k in 'xyz']).T;c=np.array([a[k] for k in 'rgb']).T/255.
sel=(xyz[:,2]>2.8)&(xyz[:,2]<3.5)
fig,axs=plt.subplots(1,3,figsize=(16,6))
for ax,(i,j) in zip(axs,[(0,1),(0,2),(1,2)]):
 ax.scatter(xyz[:,i],xyz[:,j],c='#dedede',s=.4);ax.scatter(xyz[sel,i],xyz[sel,j],c=c[sel],s=2);ax.set_aspect('equal');ax.set_xlabel('XYZ'[i]+' (native export)');ax.set_ylabel('XYZ'[j]);ax.grid(alpha=.2)
fig.suptitle('Trog-Suchbereich: native Z 2.8–3.5 | keine mechanische Registrierung');fig.tight_layout();fig.savefig(OUT/'views/scan-search.png',dpi=120);plt.close(fig)
g=ROOT/'evidence/raw/Scaniverse 2026-10-07 173556.glb';gb=g.read_bytes();jlen,jtype=struct.unpack_from('<II',gb,12);gj=json.loads(gb[20:20+jlen]);report={'ply':{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(b).hexdigest(),'points':len(a),'bounds':[xyz.min(axis=0).tolist(),xyz.max(axis=0).tolist()]},'glb':{'path':str(g.relative_to(ROOT)),'sha256':hashlib.sha256(gb).hexdigest(),'accessors':gj['accessors'],'nodes':gj['nodes']},'search':{'native_z_interval':[2.8,3.5],'points':int(sel.sum()),'status':'candidate-region-not-registered'},'mechanical_transform':None,'field_scale':None}
(OUT/'evidence/scan-inspection.json').write_text(json.dumps(report,indent=2))
