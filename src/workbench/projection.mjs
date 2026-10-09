import * as T from 'three';
/** Orthographic drafting from actual mesh triangles. A CPU depth buffer classifies hidden edges. */
export function projectMeshes(meshes,{view=[6,-8,5],section=null,clipBox=null,roll=0,resolution=700}={}){
 const box=new T.Box3();meshes.forEach(m=>box.expandByObject(m));const center=box.getCenter(new T.Vector3()),cam=new T.PerspectiveCamera();cam.up.set(0,0,1);cam.position.copy(center).add(new T.Vector3(...view).normalize().multiplyScalar(20));cam.lookAt(center);cam.rotateZ(roll);cam.updateMatrixWorld(true);
 const toView=v=>v.clone().applyMatrix4(cam.matrixWorldInverse).toArray(),edges=[],triangles=[],cuts=[],cutGroups=[];
 const planes=[...(section?[{axis:section.axis,value:section.value,sign:1}]:[]),...Object.entries(clipBox||{}).flatMap(([axis,[lo,hi]])=>[{axis,value:lo,sign:-1},{axis,value:hi,sign:1}])];
 const clipPoly=vs=>{for(const plane of planes){const out=[];for(let i=0;i<vs.length;i++){const a=vs[i],b=vs[(i+1)%vs.length],da=(a[plane.axis]-plane.value)*plane.sign,db=(b[plane.axis]-plane.value)*plane.sign;if(da<=1e-8)out.push(a);if((da<0)!==(db<0))out.push(a.clone().lerp(b,da/(da-db)))}vs=out}return vs};
 const clipEdge=(a,b)=>{for(const plane of planes){let da=(a[plane.axis]-plane.value)*plane.sign,db=(b[plane.axis]-plane.value)*plane.sign;if(Math.abs(da)<1e-8)da=0;if(Math.abs(db)<1e-8)db=0;if(da>1e-8&&db>1e-8)return null;if((da>0)!==(db>0)){const hit=a.clone().lerp(b,da/(da-db));if(da>0)a=hit;else b=hit}}return [a,b]};
 for(const mesh of meshes){const localCuts=[];const g=mesh.geometry,p=g.attributes.position,index=g.index,world=i=>new T.Vector3().fromBufferAttribute(p,i).applyMatrix4(mesh.matrixWorld);for(let i=0;i<(index?index.count:p.count);i+=3){const vs=[0,1,2].map(j=>world(index?index.getX(i+j):i+j)),poly=clipPoly(vs);for(let j=1;j+1<poly.length;j++)triangles.push([poly[0],poly[j],poly[j+1]].map(toView));if(section){const hit=[];for(let j=0;j<3;j++){const a=vs[j],b=vs[(j+1)%3],da=a[section.axis]-section.value,db=b[section.axis]-section.value;if((da<0)!==(db<0))hit.push(a.clone().lerp(b,da/(da-db)))}if(hit.length===2){const cut=clipEdge(...hit);if(cut){const segment=cut.map(toView);cuts.push(segment);localCuts.push(segment)}}}}
 cutGroups.push(localCuts.map(e=>e.map(p=>p.slice(0,2))));const eg=new T.EdgesGeometry(g,24),ep=eg.attributes.position;for(let i=0;i<ep.count;i+=2){let a=new T.Vector3().fromBufferAttribute(ep,i).applyMatrix4(mesh.matrixWorld),b=new T.Vector3().fromBufferAttribute(ep,i+1).applyMatrix4(mesh.matrixWorld);const edge=clipEdge(a,b);if(!edge)continue;edges.push({p:edge.map(toView),candidate:!!(mesh.userData.hiddenCandidate||mesh.userData.fastenerCandidate)})}eg.dispose()}
 const all=edges.flatMap(e=>e.p);if(!all.length)return {visible:[],hidden:[],cuts:[],bounds:[0,1,0,1],camera:cam.matrixWorldInverse.toArray()};let minX=Infinity,maxX=-Infinity,minY=Infinity,maxY=-Infinity;for(const point of all){if(point[0]<minX)minX=point[0];if(point[0]>maxX)maxX=point[0];if(point[1]<minY)minY=point[1];if(point[1]>maxY)maxY=point[1]}const bounds=[minX,maxX,minY,maxY],[xmin,xmax,ymin,ymax]=bounds,R=resolution,sc=(R-3)/Math.max(xmax-xmin,ymax-ymin),pixel=p=>[(p[0]-xmin)*sc+1,(p[1]-ymin)*sc+1,p[2]],depth=new Float32Array(R*R).fill(-Infinity);
 for(const tr of triangles){const [a,b,c]=tr.map(pixel),den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1]);if(Math.abs(den)<1e-9)continue;for(let y=Math.max(0,Math.floor(Math.min(a[1],b[1],c[1])));y<=Math.min(R-1,Math.ceil(Math.max(a[1],b[1],c[1])));y++)for(let x=Math.max(0,Math.floor(Math.min(a[0],b[0],c[0])));x<=Math.min(R-1,Math.ceil(Math.max(a[0],b[0],c[0])));x++){const u=((b[1]-c[1])*(x-c[0])+(c[0]-b[0])*(y-c[1]))/den,v=((c[1]-a[1])*(x-c[0])+(a[0]-c[0])*(y-c[1]))/den,w=1-u-v;if(u>=-.002&&v>=-.002&&w>=-.002)depth[y*R+x]=Math.max(depth[y*R+x],u*a[2]+v*b[2]+w*c[2])}}
 const visible=[],hidden=[];for(const e of edges){const [a,b]=e.p,n=Math.max(1,Math.min(12,Math.ceil(Math.hypot(a[0]-b[0],a[1]-b[1])*sc/18)));for(let i=0;i<n;i++){const part=[i/n,(i+1)/n].map(t=>a.map((v,k)=>v+(b[k]-v)*t)),mid=pixel(part[0].map((v,k)=>(v+part[1][k])/2)),x=Math.round(mid[0]),y=Math.round(mid[1]),front=depth[y*R+x];(mid[2]>=front-.016?visible:hidden).push({p:part.map(p=>p.slice(0,2)),candidate:e.candidate})}}
 return {visible,hidden,cutGroups,cuts:cuts.map(e=>e.map(p=>p.slice(0,2))),bounds,camera:cam.matrixWorldInverse.toArray(),method:'orthographic-triangle-depth-buffer; sectional triangle intersections'};
}
export function projectPoint(point,projection){return new T.Vector3(...point).applyMatrix4(new T.Matrix4().fromArray(projection.camera)).toArray().slice(0,2)}
/** Parallel hatch clipped to actual section contours (even/odd rule retains holes). */
export function hatchSection(cuts,spacing=.025,contains=null){
 if(!cuts.length)return [];
 const offsets=cuts.flatMap(e=>e.map(p=>p[1]-p[0])),lo=Math.min(...offsets),hi=Math.max(...offsets),result=[];
 for(let k=Math.ceil(lo/spacing)*spacing;k<hi;k+=spacing){const hits=[];
  for(const [a,b]of cuts){const da=a[1]-a[0]-k,db=b[1]-b[0]-k;if((da<0)===(db<0))continue;const t=da/(da-db);hits.push(a[0]+(b[0]-a[0])*t)}
  hits.sort((a,b)=>a-b);const unique=hits.filter((x,i)=>i===0||Math.abs(x-hits[i-1])>1e-6);
  for(let i=0;i+1<unique.length;i+=contains?1:2){const mid=(unique[i]+unique[i+1])/2;if(!contains||contains([mid,mid+k]))result.push([[unique[i],unique[i]+k],[unique[i+1],unique[i+1]+k]])}
 }
 return result;
}

/** Test section material in the source mesh, avoiding hatching an open vessel cavity. */
export function sectionMaterial(mesh,projection,section){
 const inverse=new T.Matrix4().fromArray(projection.camera).invert();
 const direction=new T.Vector3(0,0,1).transformDirection(inverse),cast=new T.Vector3(1,.137,.071).normalize();
 return point=>{const world=new T.Vector3(point[0],point[1],0).applyMatrix4(inverse);if(Math.abs(direction[section.axis])<1e-8)return false;world.addScaledVector(direction,(section.value-world[section.axis])/direction[section.axis]);
  // Offset a tiny amount into retained material to avoid grazing the section plane.
  world[section.axis]-=1e-7;
  const hits=new T.Raycaster(world,cast,1e-7,100).intersectObject(mesh).map(h=>h.distance).filter((d,i,a)=>!i||Math.abs(d-a[i-1])>1e-6);return hits.length%2===1;
 };
}
