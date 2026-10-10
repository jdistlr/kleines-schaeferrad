// Read-only diagnosis: compare legacy sampling domain with actual selected arm bounds.
import fs from 'node:fs';import * as T from 'three';import {makeModel,disposeModel,p} from '../../../../src/workbench/geometry.mjs';
const result={ringDistance:p.ringDistance,domain:{x:[-.65,-.05],y:[-.22,.22],z:[-.22,.22]},variants:[]};
const domain=new T.Box3(new T.Vector3(-.65,-.22,-.22),new T.Vector3(-.05,.22,.22));
for(const joinery of ['staggered','independent','crossing']){const m=makeModel('A',0,{joinery}),a=m.children.filter(x=>x.userData.family==='COMP-ARMS'&&x.userData.id.includes('LAND'));result.variants.push({joinery,selected:a.length,arms:a.map(x=>{const b=new T.Box3().setFromObject(x);return {id:x.userData.id,bounds:[b.min.toArray(),b.max.toArray()],intersectsLegacyBox:b.intersectsBox(domain)}})});disposeModel(m)}
fs.writeFileSync('state/holistic-stabilization/20261009/evidence/legacy-domain.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result));
