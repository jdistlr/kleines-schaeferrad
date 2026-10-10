// Read-only independent probe. Run from repository root; only audit output is written.
import fs from 'node:fs';
import crypto from 'node:crypto';
import {gunzipSync} from 'node:zlib';
import * as T from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {makeModel,disposeModel,p} from '../../../../src/workbench/geometry.mjs';
import {C} from '../../../../src/workbench/expert-corrections.mjs';
import {cfg} from '../../../../src/workbench/calibration.mjs';
const dir='state/reconstruction-loop/ITER-003', out='state/holistic-stabilization/20261009/evidence';
const read=p=>JSON.parse(fs.readFileSync(p)),hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const report={scope:'Default pose, centreline probes and export fidelity; no full-cycle or structural certification',models:{}};
const vec=a=>new T.Vector3(...a),box=m=>new T.Box3().setFromObject(m);
function hits(a,b,objects){const d=b.clone().sub(a);return new T.Raycaster(a,d.clone().normalize(),1e-7,d.length()-1e-7).intersectObjects(objects,false).map(h=>({mesh:h.object.userData.id||h.object.name,distance:h.distance,point:h.point.toArray()}))}
for(const mode of ['truth','brute']){
 const model=makeModel('A',0,{modelMode:mode}),meshes=model.children.filter(m=>m.isMesh), bytes=gunzipSync(fs.readFileSync(`${dir}/models/${mode}.glb.gz`));
 const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
 const loaded=[];gltf.scene.traverse(m=>{if(m.isMesh||m.isLine)loaded.push(m)});
 const loadedById=new Map(loaded.map(m=>[m.userData.id,m]));
 const mismatch=[];let maxPositionError=0,maxMatrixError=0;
 const undo=new T.Matrix4().makeRotationX(Math.PI/2);gltf.scene.updateMatrixWorld(true);
 for(const m of meshes){const l=loadedById.get(m.userData.id);if(!l){mismatch.push([m.name,'missing']);continue}const a=m.geometry.attributes.position,b=l.geometry.attributes.position;if(a.count!==b.count){mismatch.push([m.name,'vertex-count']);continue}for(let i=0;i<a.count;i++)for(const k of ['getX','getY','getZ'])maxPositionError=Math.max(maxPositionError,Math.abs(a[k](i)-b[k](i)));const restored=new T.Matrix4().multiplyMatrices(undo,l.matrixWorld);for(let i=0;i<16;i++)maxMatrixError=Math.max(maxMatrixError,Math.abs(restored.elements[i]-m.matrixWorld.elements[i]));const ai=m.geometry.index,bi=l.geometry.index;if(!l.isLine&&ai&&bi&&(ai.count!==bi.count||ai.array.some((v,i)=>v!==bi.array[i])))mismatch.push([m.name,'indices']);}
 const families={};for(const m of meshes)families[m.userData.family]=(families[m.userData.family]||0)+1;
 const claims=read('data/geometry.claims.json').claims.filter(c=>c.id.startsWith('TH-20261009-'));
 report.models[mode]={sha256:hash(bytes),bytes:bytes.length,meshes:meshes.length,glbMeshes:loaded.length,exportMismatch:mismatch,maxPositionError,maxMatrixError,families,claimMeshCoverage:Object.fromEntries(claims.map(c=>[c.id,meshes.filter(m=>m.userData.sources?.includes(c.id)).map(m=>m.name)])),installedMetricNonNull:meshes.filter(m=>m.userData.installedMetric!=null).map(m=>m.name),asBuiltTrue:meshes.filter(m=>m.userData.asBuilt===true).map(m=>m.name),stationary:meshes.filter(m=>m.userData.stationary).length};
 if(mode==='brute'){
  const rims=meshes.filter(m=>m.userData.family==='COMP-KRUEMMLINGE');
  report.nailPaths=meshes.filter(m=>m.userData.nailPath).map(m=>{const a=vec(m.userData.nailPath.start).applyMatrix4(m.matrixWorld),b=vec(m.userData.nailPath.end).applyMatrix4(m.matrixWorld);return {id:m.name,start:a.toArray(),end:b.toArray(),length:a.distanceTo(b),actualCentrelineRimHits:hits(a,b,rims),endpointAxialProxyHits:hits(b.clone().add(new T.Vector3(.2,0,0)),b.clone().add(new T.Vector3(-.2,0,0)),rims)}});
  report.bandPassages=[];for(const side of [-1,1])for(let i=0;i<p.paddleCount;i++)for(const leg of [-1,1]){const a=(i+cfg.production.paddlePhaseSlots)*2*Math.PI/p.paddleCount,spin=new T.Matrix4().makeRotationX(a),x=side*p.ringDistance/2,u=vec([x,leg*C.bands.legSpacing/2,p.innerRadius-.07]).applyMatrix4(spin),v=vec([x,leg*C.bands.legSpacing/2,p.outerRadius+.07]).applyMatrix4(spin);report.bandPassages.push({side,slot:i,leg,hits:hits(u,v,rims)})}
  report.stationaryBounds=meshes.filter(m=>/TH-(BOCK|BEARING|WOOD-BEARING|A-|CHANNEL)|ITER003-CONTEXT/.test(m.name)).map(m=>({id:m.name,min:box(m).min.toArray(),max:box(m).max.toArray()}));
  report.armPinCentreline=meshes.filter(m=>m.name.startsWith('TH-SEAT-PIN')).map(m=>{const side=m.name.includes('LAND')?-1:1,j=Number(m.name.split('-').at(-1)),a=j*Math.PI/3,rot=new T.Matrix4().makeRotationX(a),center=vec([side*p.ringDistance/2,0,p.outerRadius+.095]).applyMatrix4(rot),axis=vec([0,1,0]).applyMatrix4(rot);return {id:m.name,armHits:hits(center.clone().addScaledVector(axis,-.061),center.clone().addScaledVector(axis,.061),meshes.filter(x=>x.userData.family==='COMP-ARMS'))}});
 }
 disposeModel(model);disposeModel(gltf.scene);
}
const manifest=read(dir+'/models/manifest.json');report.inputHashes=Object.entries(manifest.inputs).map(([path,expected])=>({path,expected,actual:hash(fs.readFileSync(path)),match:expected===hash(fs.readFileSync(path))}));
report.views=read(dir+'/views/manifest.json').views.map(v=>({path:v.path,mode:v.mode,camera:v.camera,hashMatches:hash(fs.readFileSync(v.path))===v.sha256}));
fs.writeFileSync(out+'/probe.json',JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({models:Object.fromEntries(Object.entries(report.models).map(([k,v])=>[k,{meshes:v.meshes,mismatch:v.exportMismatch,maxPositionError:v.maxPositionError,maxMatrixError:v.maxMatrixError}])),nails:report.nailPaths.length,actualRimHitPaths:report.nailPaths.filter(n=>n.actualCentrelineRimHits.length).length,proxyRimHitPaths:report.nailPaths.filter(n=>n.endpointAxialProxyHits.length).length,bandLegs:report.bandPassages.length,bandLegHitPaths:report.bandPassages.filter(n=>n.hits.length).length,armPinHitPaths:report.armPinCentreline.filter(n=>n.armHits.length).length,views:report.views.length,inputHashes:report.inputHashes.every(x=>x.match)}));
