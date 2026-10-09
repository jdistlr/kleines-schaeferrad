/** ITER-003: expert topology with explicitly qualified display dimensions. */
import * as T from 'three';
import {mergeGeometries} from 'three/addons/utils/BufferGeometryUtils.js';
import C from '../../data/reconstruction-constraints.json' with {type:'json'};
export {C};
const tau=Math.PI*2, rad=d=>d*Math.PI/180;
const source=(...ns)=>ns.map(n=>`TH-20261009-${String(n).padStart(2,'0')}`);
function prism(points,depth){const s=new T.Shape(points.map(p=>new T.Vector2(...p)));const g=new T.ExtrudeGeometry(s,{depth,bevelEnabled:false,steps:1});g.translate(0,0,-depth/2);return g;}
function beam(a,b,w,d=w){const A=new T.Vector3(...a),B=new T.Vector3(...b),v=B.clone().sub(A);const g=new T.BoxGeometry(w,d,v.length());g.applyQuaternion(new T.Quaternion().setFromUnitVectors(new T.Vector3(0,0,1),v.normalize()));g.translate(...A.add(B).multiplyScalar(.5).toArray());return g;}
function cylinderX(radius,length){const g=new T.CylinderGeometry(radius,radius,length,12);g.rotateZ(Math.PI/2);return g;}
function arcShape(a,b,ri,ro,reinforcement=null){const points=[];const inner=t=>ri-(reinforcement?C.rings.seatReinforcementDepth*Math.max(0,1-Math.abs(t-reinforcement.mid)/C.rings.seatReinforcementHalfAngle):0);for(let i=0;i<=40;i++){const t=a+(b-a)*i/40;points.push(new T.Vector2(-Math.sin(t)*ro,Math.cos(t)*ro))}for(let i=40;i>=0;i--){const t=a+(b-a)*i/40;points.push(new T.Vector2(-Math.sin(t)*inner(t),Math.cos(t)*inner(t)))}return new T.Shape(points);}
function extrudeArc(shape,lo,hi){const g=new T.ExtrudeGeometry(shape,{depth:hi-lo,bevelEnabled:false,curveSegments:12});g.translate(0,0,lo);g.applyMatrix4(new T.Matrix4().set(0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,1));return g;}
function hole(shape,t,r,radius){const h=new T.Path();h.absarc(-Math.sin(t)*r,Math.cos(t)*r,radius,0,tau,true);shape.holes.push(h);}
function merge(gs){const result=mergeGeometries(gs);gs.forEach(g=>g.dispose());return result;}
// Radial passages are actual voids, formed by axial slabs with angular intervals removed.
export function correctedRimGeometry(index,p,c){
 const start=index*Math.PI/3-Math.PI/6,end=start+Math.PI/3,mid=(start+end)/2,r=(p.innerRadius+p.outerRadius)/2,w=p.rimWidth;
 const cuts=[-w/2,-C.rings.seatAxialWidth/2,-(C.bands.width+.002)/2,(C.bands.width+.002)/2,C.rings.seatAxialWidth/2,w/2].sort((a,b)=>a-b),parts=[];
 for(let k=0;k<cuts.length-1;k++){
  const lo=cuts[k],hi=cuts[k+1],x=(lo+hi)/2,slots=[];
  if(Math.abs(x)<C.rings.seatAxialWidth/2)slots.push([mid-(p.armDepth+.002)/(2*r),mid+(p.armDepth+.002)/(2*r)]);
  if(Math.abs(x)<(C.bands.width+.002)/2)for(let j=-p.paddleCount;j<2*p.paddleCount;j++)for(const s of [-1,1]){const t=(j+c.paddlePhaseSlots)*tau/p.paddleCount+s*C.bands.legSpacing/(2*r);slots.push([t-(C.bands.thickness+.008)/(2*r),t+(C.bands.thickness+.008)/(2*r)])}
  let intervals=[[start+.006,end-.006]];
  for(const [a,b]of slots){intervals=intervals.flatMap(([u,v])=>b<=u||a>=v?[[u,v]]:[[u,Math.min(a,v)],[Math.max(b,u),v]].filter(([l,h])=>h-l>1e-6))}
  for(const [a,b]of intervals){const sh=arcShape(a,b,p.innerRadius,p.outerRadius,{mid});for(const joint of [start,end])for(let n=0;n<4;n++){const t=joint+C.schettern.pinTangentialOffsets[n]/r,rr=r+C.schettern.pinRadialOffsets[n];if(t>a+.01&&t<b-.01)hole(sh,t,rr,C.schettern.pinDiameter/2+.001)}parts.push(extrudeArc(sh,lo,hi))}
 }
 return merge(parts);
}
export function paddleGeometry(span,height,thickness){
 // X is shaft, Z radial: land end is bevelled; exact cut remains a candidate.
 const l=C.paddles.landBevelLength,d=C.paddles.landBevelDepth;
 const g=prism([[-span/2,-height/2+d],[-span/2+l,-height/2],[span/2,-height/2],[span/2,height/2],[-span/2,height/2]],thickness);g.rotateX(Math.PI/2);return g;
}
export function applyExpertCorrections(group,p,c,{truth=false,explode=0}={}){
 const wood=0xab8962,metal=0x656b69;
 function add(name,family,g,ids,stationary=false,extra={},color=wood){const m=new T.Mesh(g,new T.MeshStandardMaterial({color,roughness:.88,metalness:color===metal?.5:0,side:T.DoubleSide}));m.name=name;m.userData={id:name,family,stationary,baseColor:color,status:stationary?'synthetic-expert-constrained-site':'expert-topology-candidate-realization',iteration:'ITER-003',sources:source(...ids),metricStatus:'expert-sizes-with-explicit-unmeasured-display-details',installedMetric:null,poseStatus:stationary?'site-pose-unregistered':'candidate-layout-not-observed-pose',physicalInstanceId:null,...extra};group.add(m);return m;}
 function remove(pred){for(const m of [...group.children])if(pred(m)){group.remove(m);m.geometry?.dispose();m.material?.dispose()}}
 // Eliminate contradictory old fasteners/shoulders; keep 12 historical rim slot IDs.
 remove(m=>m.name.startsWith('CAND-RIM-PIN'));
 for(const m of group.children){
  if(m.name==='HYP-SHAFT'){m.geometry.dispose();const r=p.shaftWidth/2/Math.cos(Math.PI/8);m.geometry=new T.CylinderGeometry(r,r,p.shaftLength,8);m.geometry.rotateZ(Math.PI/2);Object.assign(m.userData,{sources:source(13,15),constantWoodSection:true,metricStatus:'constant-section-expert; size-and-faceting-historical-candidate'})}
  if(m.userData.family==='COMP-KRUEMMLINGE'){const i=Number(m.name.slice(-2))-1;m.geometry.dispose();m.geometry=correctedRimGeometry(i,p,c);Object.assign(m.userData,{sources:source(1,2,4,5,25,26,28,29),jointCandidate:'paired-schettern-four-alternating-nails',segmentMidAngle:i*Math.PI/3,radialPassages:true,metricStatus:'expert-axial-width; historical-radii; seat-and-hole-metrics-candidate'})}
  if(m.userData.family==='COMP-ARMS')Object.assign(m.userData,{sources:[...m.userData.sources,...source(1,3,27)],crossSection:[p.armWidth,p.armDepth],axisAssignment:C.arms.axisAssignment,metricStatus:'expert-section; axis-assignment-and-central-joinery-candidate'});
 }
 const r=(p.innerRadius+p.outerRadius)/2;
 for(const [side,sign]of [['LAND',-1],['WATER',1]]){
  const x=sign*(p.ringDistance/2+explode*.7);
  for(let j=0;j<6;j++){
   const joint=j*Math.PI/3-Math.PI/6;
   for(const s of [-1,1]){const sh=arcShape(joint-C.schettern.length/(2*r),joint+C.schettern.length/(2*r),r-C.schettern.radialDepth/2,r+C.schettern.radialDepth/2);for(let n=0;n<4;n++)hole(sh,joint+C.schettern.pinTangentialOffsets[n]/r,r+C.schettern.pinRadialOffsets[n],C.schettern.pinDiameter/2+.001);const g=extrudeArc(sh,-C.schettern.thickness/2,C.schettern.thickness/2);g.translate(x+s*(p.rimWidth+C.schettern.thickness)/2,0,0);add(`TH-SCHETTER-${side}-${j}-${s}`,'COMP-SCHETTERNBRETTER',g,[4,5],false,{joint:j,side,metricStatus:C.schettern.metricStatus})}
   for(let n=0;n<4;n++){
    const t=joint+C.schettern.pinTangentialOffsets[n]/r,rr=r+C.schettern.pinRadialOffsets[n],dir=n%2?1:-1,len=p.rimWidth+2*C.schettern.thickness+.07,pos=[x,-Math.sin(t)*rr,Math.cos(t)*rr];
    const g=cylinderX(C.schettern.pinDiameter/2,len);g.translate(...pos);add(`TH-SCHETTER-PIN-${side}-${j}-${n}`,'COMP-FASTENERS',g,[5],false,{joint:j,insertionDirection:dir,connection:'schettern-through-rim',candidateMetric:true});
    const head=cylinderX(.021,.018);head.translate(x-dir*len/2,pos[1],pos[2]);add(`TH-SCHETTER-HEAD-${side}-${j}-${n}`,'COMP-FASTENERS',head,[5]);
    const wedge=prism([[-.012,-.045],[.012,-.045],[.006,.045],[-.006,.045]],.008);wedge.translate(x+dir*(len/2-.012),pos[1],pos[2]);add(`TH-SCHETTER-WEDGE-${side}-${j}-${n}`,'COMP-FASTENERS',wedge,[5]);
   }
   const a=j*Math.PI/3;
   for(const s of [-1,1]){const tip=C.arms.tipAxialWidth/2,edge=C.rings.seatAxialWidth/2;const g=prism([[s*tip,-.03],[s*edge,-.03],[s*(edge+.008),.07],[s*tip,.07]],p.armDepth);g.rotateX(Math.PI/2);g.translate(x,0,p.outerRadius);g.rotateX(a);add(`TH-SEAT-WEDGE-${side}-${j}-${s}`,'COMP-FASTENERS',g,[3],false,{metricStatus:'expert-two-wedges; wedge-shape-placement-candidate'})}
   const pin=cylinderX(.010,.12);pin.rotateZ(Math.PI/2);pin.rotateX(a);pin.translate(x,-Math.sin(a)*(p.outerRadius+.095),Math.cos(a)*(p.outerRadius+.095));add(`TH-SEAT-PIN-${side}-${j}`,'COMP-FASTENERS',pin,[3],false,{metricStatus:'expert-rear-pin; exact-hole-and-path-candidate'});
  }
  // Rectangular split-stock band, bent over paddle. Radial legs align with actual rim passages.
  const slots=truth?[0,1,2]:Array.from({length:p.paddleCount},(_,i)=>i);
  for(const i of slots){const a=(i+c.paddlePhaseSlots)*tau/p.paddleCount,half=C.bands.legSpacing/2,top=c.paddleRadius+c.paddleHeight/2+.009,bottom=p.innerRadius-.075;
   const path=[[-half,bottom],[-half,top-.025],[-half+.025,top],[half-.025,top],[half,top-.025],[half,bottom]],pieces=[];
   for(let k=0;k<path.length-1;k++)pieces.push(beam([x,path[k][0],path[k][1]],[x,path[k+1][0],path[k+1][1]],C.bands.width,C.bands.thickness));
   const g=merge(pieces);g.rotateX(a);add(`TH-BAND-${side}-${i}`,'COMP-WOOD-BANDS',g,[9,10,11,12],false,{slot:i,metricStatus:C.bands.metricStatus,connection:'over-paddle-through-rim'});
   for(const s of [-1,1]){const g=prism([[-.035,-.008],[.035,-.008],[.035,.006],[-.035,.012]],.055);g.translate(x,s*half,p.innerRadius-.03);g.rotateX(a);add(`TH-BAND-WEDGE-${side}-${i}-${s}`,'COMP-FASTENERS',g,[12],false,{slot:i,candidateMetric:true})}
  }
 }
 // Shaft clamps are visible topology in Truth; their dimensions are not promoted.
 for(const sign of [-1,1])for(let i=0;i<2;i++){const rr=p.shaftWidth/2/Math.cos(Math.PI/8),s=new T.Shape();s.absarc(0,0,rr+C.shaft.clampThickness,0,tau,false);const h=new T.Path();h.absarc(0,0,rr+.001,0,tau,true);s.holes.push(h);const g=extrudeArc(s,-C.shaft.clampWidths[i]/2,C.shaft.clampWidths[i]/2);g.translate(sign*(p.shaftLength/2-C.shaft.clampInset[i]),0,0);add(`TH-SHAFT-CLAMP-${sign}-${i}`,'COMP-SHAFT-CLAMPS',g,[14],false,{metricStatus:C.shaft.metricStatus},metal)}
 if(!truth)rebuildStationary(group,p,c,add,remove);
 if(truth)for(const m of group.children){m.userData.installedMetric=null;m.userData.asBuilt=false;}
 group.userData.iteration='ITER-003';group.userData.expertConstraints='data/reconstruction-constraints.json';group.updateMatrixWorld(true);
}
function rebuildStationary(group,p,c,add,remove){
 // Keep lower Radstadt context; replace the false local bearing frames and channel posts.
 remove(m=>m.userData.family==='COMP-BEARINGS'||m.userData.family==='COMP-BEARING-STANDS'||m.name.startsWith('CAND-JOURNAL')||m.name.startsWith('CTX-CHANNEL-SUPPORT')||m.name==='CAND-CHANNEL');
 const B=C.radBock,b=B.beamSection,jr=C.shaft.journalDiameter/2;
 for(const s of [-1,1]){const x=s*(p.shaftLength/2+C.shaft.journalExtension/2),g=cylinderX(jr,C.shaft.journalExtension);g.translate(x,0,0);add(`TH-JOURNAL-${s}`,'COMP-SHAFT',g,[15],false,{metricStatus:C.shaft.metricStatus},0x656b69);
  // Two cheeks around a genuinely open journal notch; no metal bearing liner.
  const pts=[[-.20,-.20],[.20,-.20],[.20,.04],[jr+.003,.04]];for(let i=0;i<=20;i++){const a=i*Math.PI/20;pts.push([(jr+.003)*Math.cos(a),-(jr+.003)*Math.sin(a)])}pts.push([-jr-.003,.04],[-.20,.04]);const bearing=prism(pts,b);bearing.rotateY(Math.PI/2);bearing.rotateX(Math.PI/2);bearing.translate(x,0,0);add(`TH-WOOD-BEARING-${s}`,'COMP-BEARINGS',bearing,[15],true,{metricStatus:'wood-contact-expert; notch-diameter-and-clearance-candidate'});
  const sill=beam([x,-.56,-.25],[x,.56,-.25],b,b);add(`TH-BEARING-SILL-${s}`,'COMP-BEARING-STANDS',sill,[21,22],true);
  // Synthetic lower load path only: site ground and foundations remain unregistered.
  for(const y of [-B.postSpacing/2,B.postSpacing/2])add(`ITER003-CONTEXT-POST-${s}-${y}`,'COMP-FRAME-LOWER',beam([x,y,-2.65],[x,y,B.baseZ-b/2],b),[],true,{metricStatus:'synthetic lower support; dimensions and ground unmeasured',status:'synthetic-site-context'});
  const low=beam([x,-.60,B.baseZ],[x,.60,B.baseZ],b,b);add(`TH-BOCK-BASE-${s}`,'COMP-FRAME-LOWER',low,[19],true);
  // Posts penetrate real openings in top bar; lower post shoulder supports the bar.
  const sh=new T.Shape([new T.Vector2(-B.topLength/2,-b/2),new T.Vector2(B.topLength/2,-b/2),new T.Vector2(B.topLength/2,b/2),new T.Vector2(-B.topLength/2,b/2)]);
  for(const y of [-B.postSpacing/2,B.postSpacing/2]){const h=new T.Path();h.moveTo(y-.036,-.036);h.lineTo(y+.036,-.036);h.lineTo(y+.036,.036);h.lineTo(y-.036,.036);h.closePath();sh.holes.push(h)}
  const top=new T.ExtrudeGeometry(sh,{depth:b,bevelEnabled:false});top.translate(0,0,-b/2);top.applyMatrix4(new T.Matrix4().set(0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1));top.translate(x,0,B.topZ);add(`TH-BOCK-TOP-${s}`,'COMP-TROUGH-SUPPORT',top,[21,22,23,24],true,{metricStatus:B.metricStatus});
  for(const y of [-B.postSpacing/2,B.postSpacing/2]){add(`TH-BOCK-POST-${s}-${y}`,'COMP-TROUGH-SUPPORT',beam([x,y,B.baseZ+b/2],[x,y,B.topZ-b/2],b),[22,23],true);add(`TH-BOCK-TENON-${s}-${y}`,'COMP-TROUGH-SUPPORT',beam([x,y,B.topZ-b/2],[x,y,B.topZ+b/2+.10],.07),[23],true);add(`TH-BOCK-WEDGE-${s}-${y}`,'COMP-FASTENERS',beam([x-.09,y,B.topZ+b/2+.035],[x+.09,y,B.topZ+b/2+.035],.02,.025),[23],true)}
 }
 // A two-piece channel whose splice actually lies on the crossbar (candidate global placement).
 const A=new T.Vector3(c.troughX,1.25,c.troughZ-.05),D=new T.Vector3(-3.8,1.25,c.troughZ-.21),J=A.clone().lerp(D,.55),width=.32,depth=.14;
 const channel=(name,a,b)=>{const len=a.distanceTo(b),g=prism([[-width/2,0],[width/2,0],[width/2,depth],[width/2-.035,depth],[width/2-.035,.035],[-width/2+.035,.035],[-width/2+.035,depth],[-width/2,depth]],len),v=b.clone().sub(a).normalize(),right=new T.Vector3(0,0,1).cross(v).normalize(),up=v.clone().cross(right);g.applyMatrix4(new T.Matrix4().makeBasis(right,up,v));g.translate(...a.clone().add(b).multiplyScalar(.5).toArray());return add(name,'COMP-CHANNEL',g,[30,31],true,{metricStatus:'two sections expert; lengths/profile/slope/site pose candidate'})};
 channel('TH-CHANNEL-1',A,J);channel('TH-CHANNEL-2',J,D);
 const ab=C.aBock,ground=J.z-ab.channelUndersideAboveGround,crossZ=J.z-ab.crossbarSection[1]/2,angle=rad(ab.displayLegAngleDeg),seatH=crossZ-ground,L=ab.displayLegLength,seat=ab.displaySeatAxisSpacing/2;
 add('TH-A-CROSSBAR','COMP-A-BOCK',beam([J.x,J.y-ab.crossbarLength/2,crossZ],[J.x,J.y+ab.crossbarLength/2,crossZ],ab.crossbarSection[0],ab.crossbarSection[1]),[34,35,36],true,{metricStatus:ab.metricStatus,localGround:ground,channelUnderside:J.z});
 for(const s of [-1,1]){const footY=J.y+s*(seat+seatH*Math.tan(angle)),a=new T.Vector3(J.x,footY,ground),v=new T.Vector3(0,-s*Math.sin(angle),Math.cos(angle)),seatAlong=seatH/Math.cos(angle),sh=new T.Shape([new T.Vector2(-ab.legSection/2,0),new T.Vector2(ab.legSection/2,0),new T.Vector2(ab.legSection/2,L),new T.Vector2(-ab.legSection/2,L)]),h=new T.Path();h.moveTo(-ab.openingWidth/2,seatAlong-ab.openingHeight/2);h.lineTo(ab.openingWidth/2,seatAlong-ab.openingHeight/2);h.lineTo(ab.openingWidth/2,seatAlong+ab.openingHeight/2);h.lineTo(-ab.openingWidth/2,seatAlong+ab.openingHeight/2);h.closePath();sh.holes.push(h);const g=new T.ExtrudeGeometry(sh,{depth:ab.legSection,bevelEnabled:false});g.translate(0,0,-ab.legSection/2);g.applyMatrix4(new T.Matrix4().makeBasis(new T.Vector3(1,0,0),v,new T.Vector3(1,0,0).cross(v)));g.translate(...a.toArray());add(`TH-A-LEG-${s}`,'COMP-A-BOCK',g,[32,33,38],true,{metricStatus:ab.metricStatus,footprintStatus:'unresolved-display-only',openingHeightStatus:'candidate',localGround:ground});
  for(const sign of [-1,1]){const z=crossZ+sign*(ab.crossbarSection[1]/2+.008);add(`TH-A-WEDGE-${s}-${sign}`,'COMP-FASTENERS',beam([J.x,J.y+s*seat-.12,z],[J.x,J.y+s*seat+.12,z],.04,.012),[36],true,{metricStatus:'expert upper/lower wedges; exact shape candidate'})}
 }
 group.userData.aBock={channelUndersideAboveGround:.8,footprintVerified:false,legLengthVerified:false};
}
