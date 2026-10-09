import {C,paddleGeometry} from './expert-corrections.mjs';
import * as T from 'three';
import cfg from '../../data/calibration-v3.json' with {type:'json'};
export {cfg};
const rad=d=>d*Math.PI/180;
export const referenceSources=cfg.reference.sources;
export const colors={expert:0x668e94,observed:0x9aaba6,historical:0xaeb6c1,synthetic:0xbe925c,wood:0xab8962,metal:0x656b69};
export function vesselPose(angle=0,options={}){
 const c={...cfg.production,...options},q=new T.Quaternion().setFromEuler(new T.Euler(rad(c.pitchDeg),rad(c.yawDeg),0,'YXZ'));
 // Reverse candidate changes the entire handed pose, not just the animation arrow.
 if(c.overlapDirection<0)q.setFromEuler(new T.Euler(-rad(c.pitchDeg),rad(c.yawDeg),0,'YXZ'));
 const axis=new T.Vector3(0,0,1).applyQuaternion(q),across=new T.Vector3(1,0,0).addScaledVector(axis,-axis.x).normalize(),around=axis.clone().cross(across);
 q.setFromRotationMatrix(new T.Matrix4().makeBasis(across,around,axis));
 const spin=new T.Quaternion().setFromAxisAngle(new T.Vector3(1,0,0),angle);
 return {position:new T.Vector3(c.centerX,0,c.radius).applyQuaternion(spin),quaternion:spin.multiply(q)};
}
export const radiusAt=(z,r=cfg.reference)=>r.baseRadius+(r.mouthRadius-r.baseRadius)*(z/r.height+.5);
function staveGeometry(j,r){
 const pieces=[],H=r.height/2,b=-H+r.baseOffset,g=r.grooveWidth/2;
 for(const [lo,hi,groove] of [[-H,b-g,false],[b-g,b+g,true],[b+g,H,false]]){
  const th=r.thickness-(groove?r.grooveDepth:0),s=new T.Shape(),w=z=>radiusAt(z,r)*Math.tan(Math.PI/12)-.00035;
  s.moveTo(-w(lo),lo);s.lineTo(w(lo),lo);s.lineTo(w(hi),hi);s.lineTo(-w(hi),hi);s.closePath();
  if(r.drilledStaves.includes(j))for(const offset of r.holeOffsets){const z=H-offset;if(z-r.holeRadius>lo&&z+r.holeRadius<hi){const h=new T.Path();h.absarc(0,z,r.holeRadius,0,Math.PI*2,true);s.holes.push(h)}}
  const geo=new T.ExtrudeGeometry(s,{depth:th,bevelEnabled:false,curveSegments:20,steps:1}),p=geo.attributes.position;
  for(let i=0;i<p.count;i++){const u=p.getX(i),z=p.getY(i),d=p.getZ(i);p.setXYZ(i,radiusAt(z,r)-th+d,u,z)}
  geo.rotateZ(j*Math.PI/6);geo.computeVertexNormals();pieces.push(geo);
 }
 // Keep cut-out topology without a CSG approximation; merged below manually.
 const positions=[],normals=[];for(const g of pieces){positions.push(...g.attributes.position.array);normals.push(...g.attributes.normal.array);g.dispose()}
 const out=new T.BufferGeometry();out.setAttribute('position',new T.Float32BufferAttribute(positions,3));out.setAttribute('normal',new T.Float32BufferAttribute(normals,3));return out;
}
function bandGeometry(z,r){
 const rr=radiusAt(z,r)/Math.cos(Math.PI/12)+.002;
 const profile=[new T.Vector2(rr-.003,-.009),new T.Vector2(rr+.001,-.009),new T.Vector2(rr+.001,.009),new T.Vector2(rr-.003,.009),new T.Vector2(rr-.003,-.009)];
 const g=new T.LatheGeometry(profile,48);g.rotateX(Math.PI/2);g.translate(0,0,z);return g;
}
function pinGeometry(a,b){
 // Straight passage candidate: no synthetic bend through the four reference holes.
 return new T.TubeGeometry(new T.LineCurve3(new T.Vector3(...a),new T.Vector3(...b)),18,C.nails.shaftDiameter/2,12,false);
}
export function referenceKumpf({mode='brute',slot=0,pose=null,explode=0,reference=cfg.reference,nails=true,mapping='A',mountOptions={},ringMidplane=C.rings.midplane,rimWidth=C.rings.axialWidth}={}){
 const group=new T.Group(),r=reference,id=String(slot+1).padStart(2,'0');
 function add(name,family,g,color,extra={}){const mesh=new T.Mesh(g,new T.MeshStandardMaterial({color:mode==='truth'?colors.expert:color,roughness:.88,metalness:family==='COMP-KUMPF-HOOPS'?.45:0,side:T.DoubleSide}));mesh.name=name;mesh.userData={id:name,family,slot,part:family,stationary:false,baseColor:mode==='truth'?colors.expert:(color?.isColor?color.getHex():color),iteration:'ITER-003',sources:referenceSources,status:mode==='truth'?'expert-topology-reference-display':'reconstructed-candidate',metricStatus:r.metricStatus,installedMetric:null,poseStatus:'candidate-layout-not-observed-pose',physicalInstanceId:null,...extra};group.add(mesh);return mesh}
 for(let j=0;j<12;j++){const m=add(j===0?`EXPECTED-KUM-${id}`:`V3-KUM-${id}-STAVE-${j+1}`,'COMP-KUEMPFE',staveGeometry(j,r),new T.Color(colors.wood).multiplyScalar(.91+(j%5)*.035),{staveIndex:j,drilled:r.drilledStaves.includes(j),holes:r.drilledStaves.includes(j)?r.holeOffsets.map((d,k)=>({id:`H${j===0?'A':'B'}${k+1}`,offsetFromMouth:d,metricStatus:'photo-estimate'})):[],groove:true});m.position.set(Math.cos(j*Math.PI/6)*explode*.1,Math.sin(j*Math.PI/6)*explode*.1,0)}
 const bg=new T.CylinderGeometry(radiusAt(-r.height/2+r.baseOffset,r)-r.thickness+r.grooveDepth-.0005,radiusAt(-r.height/2+r.baseOffset,r)-r.thickness+r.grooveDepth-.0005,r.grooveWidth-.001,12);bg.rotateX(Math.PI/2);bg.rotateZ(Math.PI/12);bg.translate(0,0,-r.height/2+r.baseOffset-explode*.12);add(`V3-KUM-${id}-BASE`,'COMP-KUMPF-BASE',bg,colors.wood,{retention:'base-edge-in-real-stave-groove',grooveClearance:.001});
 for(const [j,d]of r.hoopOffsets.entries()){const z=r.height/2-d;const m=add(`V3-KUM-${id}-HOOP-${j+1}`,'COMP-KUMPF-HOOPS',bandGeometry(z,r),colors.metal,{offsetFromMouth:d});m.scale.setScalar(1+explode*.13)}
 if(nails&&mode!=='truth')for(const [j,d]of r.holeOffsets.entries()){
  const z=r.height/2-d,rr=radiusAt(z,r),reverse=mapping==='B',cross=mapping==='C',start=[-rr-C.nails.headLength/2,0,z];
  // Common inner rim exit plane makes the tilted overlapping mount require unequal lengths.
  const mount=pose||vesselPose(0,mountOptions),across=new T.Vector3(1,0,0).applyQuaternion(mount.quaternion),along=new T.Vector3(0,0,1).applyQuaternion(mount.quaternion),exitX=-ringMidplane/2+rimWidth/2+C.nails.rimPenetration;
  const end=[(exitX-mount.position.x-along.x*z)/across.x,0,cross?r.height/2-r.holeOffsets[1-j]:z];
  if(reverse){start[0]*=-1;end[0]*=-1}
  const g=pinGeometry(start,end),m=add(`V3-KUM-${id}-NAIL-${j===0?'LONG':'SHORT'}`,'COMP-KUMPF-NAILS',g,colors.synthetic,{fastenerCandidate:true,pair:id,candidate:mapping,shaftDiameter:C.nails.shaftDiameter,nailPath:{start,end,exitPlaneX:exitX,holes:[`HA${j+1}`,`HB${cross?2-j:j+1}`]},role:'kumpf-to-kruemmling',lengthReason:'far-side-to-current-rim-plane-candidate',metricStatus:'diameter-expert; path-and-total-length-unverified',sources:['TH-20261009-16','TH-20261009-18','NARRATIVE-TH-KUMPF-20261008-02','NARRATIVE-TH-KUMPF-20261008-03','PHOTO-1000046423','V2-IMG_6822','V2-IMG_6832']});
  m.position.x=-explode*.23;
  const head=new T.CylinderGeometry(C.nails.headDiameter/2,C.nails.headDiameter/2,C.nails.headLength,8);head.rotateZ(Math.PI/2);head.translate(...start);const h=add(`${m.name}-HEAD`,'COMP-KUMPF-NAILS',head,colors.synthetic,{fastenerCandidate:true,pair:id,nailHead:true,candidate:mapping,headDiameter:C.nails.headDiameter,headLength:C.nails.headLength,sources:['TH-20261009-17'],metricStatus:'head-diameter-expert; head-length-photo-interval-candidate'});h.position.x=-explode*.23;
 }
 if(pose){group.position.copy(pose.position);group.quaternion.copy(pose.quaternion)}
 group.updateMatrixWorld(true);return group;
}
export function calibrateModel(group,p,options={},explode=0){
 const mode=options.modelMode||'brute',c={...cfg.production,...options},truth=mode==='truth';
 for(const m of [...group.children])if(m.userData.family==='COMP-KUEMPFE'||m.userData.family==='COMP-KUMPF-BASE'||m.userData.family==='COMP-KUMPF-HOOPS'||m.userData.fastenerCandidate||m.userData.family==='COMP-PADDLES'){group.remove(m);m.geometry.dispose();m.material.dispose()}
 if(truth)for(const m of [...group.children]){
  const keep=['COMP-SHAFT','COMP-ARMS','COMP-KRUEMMLINGE'].includes(m.userData.family)&&!m.userData.contactCandidate;
  if(!keep){group.remove(m);m.geometry.dispose();m.material.dispose();continue}
  m.userData={...m.userData,status:'historical-or-observed-topology-display',metricStatus:'historical-convention-not-installed-metric',poseStatus:'non-metric-display',installedMetric:null};m.material.color.setHex(colors.historical);m.userData.baseColor=colors.historical;
 }
 // Rebuild the provisional receiving path in the same coordinates used by the cycle.
 if(!truth)for(const m of group.children){
  if(m.name.startsWith('CTX-TROUGH-POST')){m.geometry.translate(-.4,0,-.35);m.userData.status='synthetic-outboard-support'}
  if(m.name.startsWith('CTX-TROUGH-BRACE')){m.geometry.translate(-.4,0,-.35);m.userData.status='synthetic-outboard-support'}
  if(m.name==='CAND-TROUGH'){const v=m.geometry.attributes.position;for(let i=0;i<v.count;i++){const x=v.getX(i),y=v.getY(i),z=v.getZ(i);v.setXYZ(i,c.troughX+(x+1.18)*(2*c.troughHalfWidth/.30),y,z-1.78+c.troughZ)}v.needsUpdate=true;m.geometry.computeVertexNormals();m.userData.sources=['PHOTO-6829','V2-IMG_6812'];m.userData.status='synthetic-receiving-candidate'}
  if(m.name==='CAND-CHANNEL'){const v=m.geometry.attributes.position;for(let i=0;i<v.count;i++){const x=v.getX(i),t=Math.max(0,Math.min(1,(x+3.8)/2.62));v.setXYZ(i,x+(c.troughX+1.18)*t,v.getY(i),v.getZ(i)-1.78+c.troughZ)}v.needsUpdate=true;m.geometry.computeVertexNormals()}
 }
 const slots=options.slots||Array.from({length:truth?3:p.vesselCount},(_,i)=>i);
 for(const i of slots){
  const a=i*2*Math.PI/p.vesselCount,r={...cfg.reference,thickness:options.referenceThickness||cfg.reference.thickness,...c.variants?.[i]},pose=vesselPose(a,c);if(explode)pose.position.x-=explode*.5;
  const v=referenceKumpf({mode,slot:i,pose,reference:r,mapping:c.nailMapping,mountOptions:c,ringMidplane:p.ringDistance,rimWidth:p.rimWidth,explode:options.componentExplode||0});
  for(const m of [...v.children]){m.applyMatrix4(v.matrixWorld);group.add(m)}
 }
 // Paddle plane = shaft X + local radial R; normal = tangent T. V2 had X+T, normal R.
 for(const i of slots){const phase=(i+c.paddlePhaseSlots)*Math.PI*2/p.paddleCount,a=phase+rad(c.paddlePitchDeg),g=paddleGeometry(p.ringDistance+p.rimWidth+2*c.paddleAxialOverhang,c.paddleHeight,c.paddleThickness);g.rotateX(a);g.translate(0,-Math.sin(phase)*c.paddleRadius,Math.cos(phase)*c.paddleRadius);
  const m=new T.Mesh(g,new T.MeshStandardMaterial({color:truth?colors.expert:colors.wood,roughness:.9,wireframe:truth}));m.name=`EXPECTED-PAD-${String(i+1).padStart(2,'0')}`;m.userData={id:m.name,family:'COMP-PADDLES',stationary:false,slot:i,phase,partnerSlot:i,status:truth?'expert-plane-constraint-display-pitch-unresolved':'ranked-radial-paddle-candidate',metricStatus:'width-approx-expert; overhang-bevel-pitch-candidate',outerFaceOverhang:c.paddleAxialOverhang,span:p.ringDistance+p.rimWidth+2*c.paddleAxialOverhang,pitchStatus:'candidate-not-truth',baseColor:truth?colors.expert:colors.wood,sources:['NARRATIVE-TH-PADDLE-20261008-01','TH-20261009-06','TH-20261009-07','TH-20261009-08','V2-IMG_6809','PHOTO-6861']};group.add(m)
 }
 group.userData={model:mode,iteration:'ITER-003',asBuilt:false,truthConstraints:truth?cfg.truth:undefined,candidate:truth?null:c,renderPolicy:cfg.truth.renderPolicy};
 group.updateMatrixWorld(true);return group;
}
/** Stateless periodic cycle derived from actual pose and open-vessel free-surface capacity. No CFD. */
export function calibratedCycle(angle,{waterLevel=cfg.production.waterLevel,...options}={}){
 const c={...cfg.production,...options},r=cfg.reference,a=((angle%(2*Math.PI))+2*Math.PI)%(2*Math.PI);
 const mouthAt=t=>{const pose=vesselPose(t,c),normal=new T.Vector3(0,0,1).applyQuaternion(pose.quaternion),mouth=pose.position.clone().addScaledVector(normal,r.height/2);return {pose,normal,mouth}};
 // Candidate available volume below the lowest lip plane: deterministic interior quadrature.
 const capacity=t=>{const {pose,normal,mouth}=mouthAt(t),lip=mouth.z-(r.mouthRadius-r.thickness)*Math.sqrt(Math.max(0,1-normal.z**2));let n=0,held=0;for(let iz=0;iz<18;iz++){const z=-r.height/2+r.baseOffset+r.grooveWidth/2+(r.height-r.baseOffset-r.grooveWidth/2)*(iz+.5)/18,rr=radiusAt(z,r)-r.thickness;for(let k=0;k<12;k++)for(let ir=0;ir<3;ir++){const v=new T.Vector3(rr*Math.sqrt((ir+.5)/3)*Math.cos(k*Math.PI/6),rr*Math.sqrt((ir+.5)/3)*Math.sin(k*Math.PI/6),z).applyQuaternion(pose.quaternion).add(pose.position),w=rr*rr;n+=w;if(v.z<lip)held+=w}}return held/n};
 // Precomputed phase table keyed by pose, geometry and water level, so animation is cheap.
 const key=JSON.stringify([c,waterLevel]);let table=cycleCache.get(key);
 if(!table){table=[];let fill=0;for(let lap=0;lap<2;lap++)for(let i=0;i<180;i++){const t=i*Math.PI/90,{normal,mouth}=mouthAt(t),low=mouth.z-(r.mouthRadius-r.thickness)*Math.sqrt(1-normal.z**2),wet=low<waterLevel,cap=capacity(t),before=fill;fill=wet?Math.max(fill,Math.min(1,(waterLevel-low)/.15)):Math.min(fill,cap);if(lap)table.push({fill,wet,lost:Math.max(0,before-fill)})}cycleCache.set(key,table)}
 const index=Math.floor(a/Math.PI*90)%180,record=table[index],{pose,normal,mouth}=mouthAt(a),discharging=record.lost>.0001&&!record.wet;
 // Explicit outflow velocity + rigid-body tangential velocity, then gravity; never bend a stream toward its target.
 const omega=c.rotationRPM*Math.PI/30,velocity=normal.clone().multiplyScalar(c.jetSpeed).add(new T.Vector3(0,-omega*mouth.z,omega*mouth.y));
 const fallTime=z=>mouth.z>z?(velocity.z+Math.sqrt(velocity.z**2+19.62*(mouth.z-z)))/9.81:0;
 const t=fallTime(c.troughZ+.035),landing=mouth.clone().addScaledVector(velocity,t);landing.z-=4.905*t*t;
 const inTrough=discharging&&t>0&&Math.abs(landing.x-c.troughX)<c.troughHalfWidth-.035&&landing.y>c.troughY[0]&&landing.y<c.troughY[1];
 const endTime=inTrough?t:fallTime(waterLevel),stream=Array.from({length:13},(_,i)=>{const dt=endTime*i/12,v=mouth.clone().addScaledVector(velocity,dt);v.z-=4.905*dt*dt;return v.toArray()});
 return {angle:a,y:pose.position.y,z:pose.position.z,center:pose.position.toArray(),mouth:mouth.toArray(),mouthDirection:normal.toArray(),fill:record.fill,immersed:record.wet,discharging,inTrough,lost:record.lost,landing:landing.toArray(),stream,jetSpeed:c.jetSpeed,state:record.wet?'füllt sich':discharging?(inTrough?'schüttet in den Trog':'Überlauf außerhalb Trog'):record.fill>0?'hebt Wasser':'leer'};
}
const cycleCache=new Map();
