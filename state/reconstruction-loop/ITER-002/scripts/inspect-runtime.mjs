// Read-only instantiation of the committed runtime. Writes only ITER-002 artifacts.
import fs from 'node:fs';
import crypto from 'node:crypto';
import * as T from 'three';
import {makeModel,p,disposeModel} from '../../../../src/workbench/geometry.mjs';
import {referenceKumpf,cfg} from '../../../../src/workbench/calibration.mjs';
const out='state/reconstruction-loop/ITER-002';
const digest=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const inputs=['src/workbench/geometry.mjs','src/workbench/calibration.mjs','src/workbench/viewer.js','data/hypothesis.parameters.json','data/calibration-v3.json'];
const audit={base:'f7b9185517856b7881530ba9d0553f170787cb09',inputs:Object.fromEntries(inputs.map(f=>[f,digest(f)])),models:{},parameters:p,calibration:cfg.production};
function dump(model,key){
 model.updateMatrixWorld(true);let offset=0;const chunks=[],meta=[],counts={};
 model.traverse(m=>{if(!m.isMesh)return;const g=m.geometry.index?m.geometry.toNonIndexed():m.geometry.clone();g.applyMatrix4(m.matrixWorld);g.computeBoundingBox();const pos=g.attributes.position,norm=g.attributes.normal,buf=new Float32Array(pos.count*9),col=m.material.color.toArray();for(let i=0;i<pos.count;i++)buf.set([pos.getX(i),pos.getY(i),pos.getZ(i),norm.getX(i),norm.getY(i),norm.getZ(i),...col],i*9);chunks.push(Buffer.from(buf.buffer));const bounds={min:g.boundingBox.min.toArray(),max:g.boundingBox.max.toArray()};meta.push({name:m.name,first:offset,count:pos.count,bounds,...m.userData});offset+=pos.count;counts[m.userData.family]=(counts[m.userData.family]||0)+1;g.dispose()});
 fs.writeFileSync(`/tmp/iter002-${key}.bin`,Buffer.concat(chunks));fs.writeFileSync(`${out}/evidence/${key}-mesh-register.json`,JSON.stringify(meta,null,2));audit.models[key]={meshes:meta.length,family_counts:counts,vertices:offset};return meta;
}
for(const mode of ['brute','truth']){const model=makeModel('A',0,{modelMode:mode});const m=dump(model,mode);if(mode==='brute'){
 const rims=m.filter(x=>x.family==='COMP-KRUEMMLINGE');const land=rims.filter(x=>x.name.includes('LAND')),water=rims.filter(x=>x.name.includes('WATER'));
 audit.rims={inner_gap:Math.min(...water.map(x=>x.bounds.min[0]))-Math.max(...land.map(x=>x.bounds.max[0])),outer_width:Math.max(...water.map(x=>x.bounds.max[0]))-Math.min(...land.map(x=>x.bounds.min[0])),midplane_distance:p.ringDistance,axial_width:p.rimWidth,required_midplane_distance:1.8+.14,required_outer_width:1.8+2*.14,delta_midplane:.79};
 audit.topology={arm_end_angles_deg:[0,60,120,180,240,300],segment_mid_angles_deg:[30,90,150,210,270,330],segment_boundary_phase_deg:0,required_relative_phase_change_deg:30,schettern_mesh_count:m.filter(x=>/SCHETTERN/i.test(x.family)).length,wood_band_mesh_count:m.filter(x=>/WOOD-BAND/i.test(x.family)).length,shaft_clamp_mesh_count:m.filter(x=>/CLAMP|SCHELLE/i.test(x.name)).length};
 audit.paddles={axial_span:p.ringDistance+2*cfg.production.paddleAxialOverhang,height:cfg.production.paddleHeight,thickness:cfg.production.paddleThickness,if_only_ring_distance_changed:1.94+2*cfg.production.paddleAxialOverhang,note:'2.08 m would end on rim outer faces, leaving no outer-face overhang; rebuild span semantics explicitly.'};
 }disposeModel(model)}
const ref=referenceKumpf();const meta=dump(ref,'nail-reference');audit.nails=meta.filter(m=>m.nailPath).map(m=>({...m.nailPath,name:m.name,chord_length:new T.Vector3(...m.nailPath.start).distanceTo(new T.Vector3(...m.nailPath.end)),shaft_diameter:.018,head_diameter:.048,head_axial_length:.025,exit_x_hardcoded:-.495}));disposeModel(ref);
fs.writeFileSync(`${out}/evidence/runtime-audit.json`,JSON.stringify(audit,null,2));console.log(JSON.stringify({rims:audit.rims,topology:audit.topology,paddles:audit.paddles,nails:audit.nails,models:audit.models},null,2));
