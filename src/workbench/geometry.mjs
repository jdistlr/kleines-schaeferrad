import {applyExpertCorrections} from './expert-corrections.mjs';
import {calibrateModel,cfg} from './calibration.mjs';
import * as T from 'three';
import {mergeGeometries} from 'three/addons/utils/BufferGeometryUtils.js';
import config from '../../data/hypothesis.parameters.json' with {type:'json'};
export {config};
export const p=Object.fromEntries(Object.entries(config.parameters).map(([k,v])=>[k,v.value]));
export const views={gesamt:[7,-9,6],land:[-9,0,0],wasser:[9,0,0],welle:[2,-7,3],kranz:[-9,0,0],kumpf:[-5,-4,3],schaufeln:[5,-5,3],tragwerk:[6,-8,4],lager:[5,-6,2],trog:[-5,-6,5],betrieb:[-6,-9,4]};
export const palette={wood:0xb79a70,arm:0xc6ae84,rim:0x9e8058,stave:0xc5a577,metal:0x575b5c,frame:0x9b8c73,water:0x739cac,unknown:0xbe914e};
// Mechanical frame: shaft X, transverse Y, gravity Z. Origin shaft / rim midplane.
// All dimensions are reconstruction coordinates. No member constitutes measured as-built geometry.
export function profilePrism(points,depth,holes=[]){const s=new T.Shape();points.forEach(([x,y],i)=>i?s.lineTo(x,y):s.moveTo(x,y));s.closePath();for(const [x,y,r]of holes){const h=new T.Path();h.absarc(x,y,r,0,Math.PI*2,true);s.holes.push(h)}const g=new T.ExtrudeGeometry(s,{depth,bevelEnabled:false,steps:1});g.translate(0,0,-depth/2);return g;}
function beam(a,b,w,d=w){const av=new T.Vector3(...a),bv=new T.Vector3(...b),v=bv.clone().sub(av),l=v.length(),c=Math.min(w,d)*.08;const g=profilePrism([[-w/2+c,-d/2],[w/2-c,-d/2],[w/2,-d/2+c],[w/2,d/2-c],[w/2-c,d/2],[-w/2+c,d/2],[-w/2,d/2-c],[-w/2,-d/2+c]],l);g.applyQuaternion(new T.Quaternion().setFromUnitVectors(new T.Vector3(0,0,1),v.normalize()));g.translate(...av.add(bv).multiplyScalar(.5).toArray());return g;}
export function curvedPin(length,hand=1){const verts=[],indices=[],rings=14,sides=10;for(let i=0;i<=rings;i++){const t=i/rings,xx=hand*(.025*Math.sin(t*Math.PI*.85)+.018*t*t),rr=t<.1?.002+t*.12:t>.83?.015+.018*Math.sin((t-.83)/.17*Math.PI):.014;for(let j=0;j<sides;j++){const a=j*Math.PI*2/sides;verts.push(xx+rr*Math.cos(a),rr*Math.sin(a),t*length)}}for(let i=0;i<rings;i++)for(let j=0;j<sides;j++){const a=i*sides+j,b=i*sides+(j+1)%sides;indices.push(a,b,b+sides,a,b+sides,a+sides)}for(let j=1;j<sides-1;j++){indices.push(0,j+1,j,rings*sides,rings*sides+j,rings*sides+j+1)}const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(verts,3));g.setIndex(indices);g.computeVertexNormals();return g;}
function latheX(points,n=16){const g=new T.LatheGeometry(points.map(x=>new T.Vector2(...x)),n);g.rotateZ(-Math.PI/2);return g;}
function ringSector(a,b,ri,ro,depth){const pts=[];for(let i=0;i<=24;i++){const t=a+(b-a)*i/24;pts.push([-Math.sin(t)*ro,Math.cos(t)*ro])}for(let i=24;i>=0;i--){const t=a+(b-a)*i/24;pts.push([-Math.sin(t)*ri,Math.cos(t)*ri])}const shape=new T.Shape(pts.map(p=>new T.Vector2(...p)));for(const t of[a+.024,b-.024]){const hole=new T.Path(),r=(ri+ro)/2;hole.absarc(-Math.sin(t)*r,Math.cos(t)*r,.014,0,Math.PI*2,true);shape.holes.push(hole)}const g=new T.ExtrudeGeometry(shape,{depth,bevelEnabled:false,steps:1});g.translate(0,0,-depth/2);g.applyMatrix4(new T.Matrix4().set(0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,1));return g;}
export function makeModel(variant='A',explode=0,options={}){
 const group=new T.Group();group.name='reconstructed-system';const shape=options.armShape||'dogleg',layers=options.armLayers||'staggered',joinery=options.joinery||'staggered',fasteners=options.fasteners||'pair';
 function add(id,family,g,pos=[0,0,0],rot=[0,0,0],stationary=false,color=palette.wood,extra={}){const material=new T.MeshStandardMaterial({color,roughness:.87,metalness:color===palette.metal?.35:0,side:T.DoubleSide});const m=new T.Mesh(g,material);m.name=id;m.position.set(...pos);m.rotation.set(...rot);m.userData={id,family,stationary,status:stationary?'context-hypothesis':'reconstructed-candidate',baseColor:color,sourceClass:'TECHNISCH PLAUSIBEL REKONSTRUIERT',...extra};group.add(m);return m;}
 // Octagonal shaft, tapered shoulders and distinct journal candidates from visible faceting.
 const r=p.shaftWidth/2/Math.cos(Math.PI/8),L=p.shaftLength/2;
 add('HYP-SHAFT','COMP-SHAFT',latheX([[.075,-L],[.075,-L+.18],[r*.76,-L+.27],[r,-L+.5],[r,L-.5],[r*.76,L-.27],[.075,L-.18],[.075,L]],8),[0,0,0],[0,0,0],false,palette.wood,{sources:['PHOTO-6853','PHOTO-6855','PHOTO-6816','V2-IMG_6800','V2-IMG_6808'],unknownInterior:true});
 for(const sign of[-1,1])add(`CAND-JOURNAL-${sign}`,'COMP-SHAFT',latheX([[.077,-.09],[.077,.09]],16),[sign*(L-.09),0,0],[0,0,0],false,palette.metal,{sources:['EXT-VZO'],contactCandidate:true});
 for(const [side,sign]of[['LAND',-1],['WATER',1]]){
  const x=sign*(p.ringDistance/2+explode*.7);
  for(let i=0;i<3;i++){
   const layer=joinery==='crossing'?0:layers==='coplanar'?0:(i-1)*.17*(layers==='reverse'?-1:1),off=shape==='straight'?0:sign*.22-layer;
   // Single continuous polygon, including central joining region; profile offset is candidate, not a measured bend.
   const centre=[[-2.275,off],[-1.975,off],[-.25,0],[.25,0],[1.975,off],[2.275,off]],w=p.armWidth;
   const width=z=>Math.abs(z)>1.976?w*.45:w;
   const outline=c=>[...c.map(([z,y])=>[y-width(z)/2,z]),...c.slice().reverse().map(([z,y])=>[y+width(z)/2,z])];
   const g=joinery==='independent'?mergeGeometries([profilePrism(outline([...centre.slice(0,2),[-.16,0]]),p.armDepth,[[off,-p.outerRadius-.095,.011]]),profilePrism(outline([[.16,0],...centre.slice(4)]),p.armDepth,[[off,p.outerRadius+.095,.011]])]):profilePrism(outline(centre),p.armDepth,[[off,-p.outerRadius-.095,.011],[off,p.outerRadius+.095,.011]]);g.applyMatrix4(new T.Matrix4().set(1,0,0,0,0,0,-1,0,0,1,0,0,0,0,0,1));
   add(`HIST-ARM-${side}-${i+1}-${i+4}`,'COMP-ARMS',g,[x+layer-sign*.22,0,0],[i*Math.PI/3,0,0],false,palette.arm,{armShape:shape,armLayers:layers,hiddenCenterOmitted:joinery==='independent',candidateJoinery:joinery,sources:['PHOTO-6820','PHOTO-6855','V2-IMG_6798','V2-IMG_6799','V2-IMG_6800','V2-IMG_6808'],sourceClass:'HISTORISCHE ZEICHNUNG / TECHNISCH REKONSTRUIERT'});
   for(const s of[-1,1])add(`CAND-WEDGE-${side}-${i}-${s}`,'COMP-FASTENERS',profilePrism([[-.045,-.12],[.045,-.12],[.035,.12],[-.035,.12]],.05),[x+layer-sign*.22,s*.21*Math.sin(i*Math.PI/3),s*.21*Math.cos(i*Math.PI/3)],[i*Math.PI/3,0,Math.PI/2],false,palette.unknown,{hiddenCandidate:true});
  }
  for(let i=0;i<6;i++){
   const a=i*Math.PI/3+.006,b=(i+1)*Math.PI/3-.006;
   add(`HIST-KRU-${side}-${String(i+1).padStart(2,'0')}`,'COMP-KRUEMMLINGE',ringSector(a,b,p.innerRadius,p.outerRadius,p.rimWidth),[x,-Math.sin((a+b)/2)*explode*.2,Math.cos((a+b)/2)*explode*.2],[0,0,0],false,palette.rim,{sources:['PHOTO-6849','PHOTO-6851'],jointCandidate:'butted-with-paired-pins'});
   for(const delta of[-.03,.03]){const t=i*Math.PI/3+delta;add(`CAND-RIM-PIN-${side}-${i}-${delta}`,'COMP-FASTENERS',latheX([[.014,-.082],[.014,.082]],8),[x,-Math.sin(t)*2.055,Math.cos(t)*2.055],[0,0,0],false,palette.unknown,{hiddenCandidate:true})}
  }
 }
 for(let i=0;i<p.vesselCount;i++){
  const a=i*2*Math.PI/p.vesselCount,r=p.outerRadius+.12+explode*.4,id=String(i+1).padStart(2,'0'),pose=new T.Matrix4().makeRotationX(a),local=new T.Matrix4().makeRotationY(.45).multiply(new T.Matrix4().makeRotationX(110*Math.PI/180));
  const position=new T.Vector3(-p.ringDistance/2-.2-explode,0,r);const staveParts=[],h=p.vesselHeight,th=config.variants[variant].staveThickness;
  // Individual curved staves, open mouth, rebated bottom; seams remain real gaps.
  for(let j=0;j<12;j++){const a0=j*2*Math.PI/12+.01,a1=(j+1)*2*Math.PI/12-.01,verts=[],idx=[];for(const z of[-h/2,-h*.28,h*.25,h/2]){const rr=.15+.025*(1-Math.pow(z/(h/2),2));for(const [rad,t] of[[rr,a0],[rr,a1],[rr-th,a0],[rr-th,a1]])verts.push(rad*Math.cos(t),rad*Math.sin(t),z)}for(let k=0;k<3;k++)for(const [u,v]of[[0,1],[3,2],[2,0],[1,3]]){const o=k*4;idx.push(o+u,o+v,o+v+4,o+u,o+v+4,o+u+4)}idx.push(0,2,3,0,3,1,12,13,15,12,15,14);const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(verts,3));g.setIndex(idx);g.computeVertexNormals();staveParts.push(g)}
  const vg=mergeGeometries(staveParts);staveParts.forEach(g=>g.dispose());vg.applyMatrix4(local);vg.translate(...position.toArray());vg.applyMatrix4(pose);
  add(`EXPECTED-KUM-${id}`,'COMP-KUEMPFE',vg,[0,0,0],[0,0,0],false,palette.stave,{slot:i,phase:a,part:'staves',sources:['PHOTO-6854','PHOTO-6823','V2-IMG_6809','V2-IMG_6810','V2-IMG_6811'],poseCandidate:'tangential-110deg-unmeasured'});
  const transform=g=>{g.applyMatrix4(local);g.translate(...position.toArray());g.applyMatrix4(pose);return g};
  const base=latheX([[0,-.012],[.127,-.012],[.127,.012],[0,.012]],16);base.rotateY(Math.PI/2);base.translate(0,0,-h/2+.03);add(`CAND-KUM-BASE-${id}`,'COMP-KUMPF-BASE',transform(base),[0,0,0],[0,0,0],false,palette.wood);
  for(const [n,z]of[-.17,0,.16].entries()){const rr=.15+.025*(1-Math.pow(z/(h/2),2)),g=new T.TorusGeometry(rr+.005,.008,4,32);g.translate(0,0,z);add(`CAND-HOOP-${id}-${n}`,'COMP-KUMPF-HOOPS',transform(g),[0,0,0],[0,0,0],false,palette.metal)}
  for(const [n,len]of(fasteners==='repair'?[.29,.26]:[.32,.22]).entries()){
   const pg=curvedPin(len,n?1:-1);if(fasteners==='tilt')pg.rotateY(n?.24:-.24);if(fasteners==='secure')pg.rotateX(.35);pg.translate(n?.1:-.1,-.1,fasteners==='tilt'?(n?-.12:-.2):-.17);add(`CAND-KUM-PIN-${id}-${n?'SHORT':'LONG'}`,'COMP-FASTENERS',transform(pg),[0,0,0],[0,0,0],false,palette.unknown,{fastenerCandidate:true,pair:id,role:'unresolved',candidate:fasteners,sources:['V2-IMG_6822','V2-IMG_6832']})
  }
  const pa=(i+.5)*Math.PI*2/p.paddleCount,pr=p.outerRadius+.12+explode*.4;
  add(`EXPECTED-PAD-${id}`,'COMP-PADDLES',beam([-p.ringDistance/2-.15,0,-.22],[p.ringDistance/2+.15,0,-.22],.055,.43),[0,-Math.sin(pa)*pr,Math.cos(pa)*pr],[pa,0,0],false,palette.arm,{phase:pa,partnerSlot:i});
 }
 // Stationary topology: two side trestles, lower sills, top bearers, braces, walk boards.
 for(const sx of[-1,1]){const x=sx*1.74;
  for(const y of[-1.85,1.85])add(`CTX-POST-${sx}-${y}`,'COMP-FRAME-MAIN',beam([x,y,-2.65],[x,y,.25],.23),[0,0,0],[0,0,0],true,palette.frame);
  for(const z of[-2.48,-.34])add(`CTX-RAIL-${sx}-${z}`,'COMP-FRAME-LOWER',beam([x,-2.5,z],[x,2.5,z],.24),[0,0,0],[0,0,0],true,palette.frame);
  for(const sy of[-1,1])add(`CTX-BRACE-${sx}-${sy}`,'COMP-FRAME-SIDE',beam([x,sy*1.8,-2.25],[x,sy*.2,-.4],.16),[0,0,0],[0,0,0],true,palette.frame);
  add(`CTX-BEARING-STAND-${sx}`,'COMP-BEARING-STANDS',beam([x,-.42,-.18],[x,.42,-.18],.34,.26),[0,0,0],[0,0,0],true,palette.wood);
  // U-shaped bearing seat has an explicit open journal contact, provisional material/clearance.
  const pts=[[-.22,-.20],[.22,-.20],[.22,.05],[.105,.05],[.105,-.04],[.04,-.077],[-.04,-.077],[-.105,-.04],[-.105,.05],[-.22,.05]],g=profilePrism(pts,.24);g.applyMatrix4(new T.Matrix4().set(0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,1));add(`HYP-BEARING-${sx}`,'COMP-BEARINGS',g,[x,0,0],[0,0,0],true,palette.metal,{contactCandidate:true});
 }
 for(const y of[-2.25,2.25])add(`CTX-CROSS-${y}`,'COMP-FRAME-MAIN',beam([-1.85,y,-1.95],[1.85,y,-1.95],.22),[0,0,0],[0,0,0],true,palette.frame);
 for(let j=0;j<4;j++)add(`CTX-WALK-${j}`,'COMP-FRAME-SIDE',beam([-1.6-j*.18,-2.55,-.65],[-1.6-j*.18,2.55,-.65],.16,.06),[0,0,0],[0,0,0],true,palette.frame);
 function channel(id,a,b,width,depth){const av=new T.Vector3(...a),bv=new T.Vector3(...b),v=bv.clone().sub(av),g=profilePrism([[-width/2,0],[width/2,0],[width/2,depth],[width/2-.035,depth],[width/2-.035,.035],[-width/2+.035,.035],[-width/2+.035,depth],[-width/2,depth]],v.length());const along=v.clone().normalize(),right=new T.Vector3(0,0,1).cross(along).normalize(),up=along.clone().cross(right);g.applyMatrix4(new T.Matrix4().makeBasis(right,up,along));g.translate(...av.add(bv).multiplyScalar(.5).toArray());return add(id,'COMP-TROUGH',g,[0,0,0],[0,0,0],true,palette.wood,{waterPath:true})}
 // Trough runs along Y at the outboard mouth, then turns toward a provisional bank.
 channel('CAND-TROUGH',[-1.18,-1.2,1.78],[-1.18,1.25,1.73],.30,.16);
 channel('CAND-CHANNEL',[-1.18,1.25,1.73],[-3.8,1.25,1.57],.32,.14);
 for(const y of[-1,1]){add(`CTX-TROUGH-POST-${y}`,'COMP-FRAME-SIDE',beam([-1.24,y,-.4],[-1.24,y,1.8],.14),[0,0,0],[0,0,0],true,palette.frame);add(`CTX-TROUGH-BRACE-${y}`,'COMP-FRAME-SIDE',beam([-1.58,y,-.2],[-1.24,y,1.3],.1),[0,0,0],[0,0,0],true,palette.frame)}
 for(const x of[-2.1,-3.6]){const top=1.73-(Math.abs(x)-1.18)*.16/2.62;add(`CTX-CHANNEL-SUPPORT-${x}`,'COMP-FRAME-SIDE',beam([x,1.25,-2.05],[x,1.25,top],.14),[0,0,0],[0,0,0],true,palette.frame)}
 if(options.calibration!==false){calibrateModel(group,p,{...options,referenceThickness:config.variants[variant].staveThickness},explode);applyExpertCorrections(group,p,{...cfg.production,...options},{truth:options.modelMode==='truth',explode});}
 group.updateMatrixWorld(true);return group;
}
export function matchesFamily(mesh,selected){const f=mesh.userData.family;if(selected==='ALL')return true;if(['COMP-RIMS','COMP-RIM-LAND','COMP-RIM-WATER'].includes(selected))return f==='COMP-KRUEMMLINGE'&&(!selected.endsWith('LAND')||mesh.userData.id.includes('LAND'))&&(!selected.endsWith('WATER')||mesh.userData.id.includes('WATER'));if(selected==='COMP-KUEMPFE')return ['COMP-KUEMPFE','COMP-KUMPF-BASE','COMP-KUMPF-HOOPS','COMP-KUMPF-NAILS'].includes(f)||mesh.userData.fastenerCandidate;if(selected.startsWith('COMP-HUB-'))return f==='COMP-SHAFT'||f==='COMP-ARMS';return f===selected;}
export function disposeModel(model){model.traverse(o=>{o.geometry?.dispose();for(const m of[].concat(o.material||[]))m.dispose()})}
