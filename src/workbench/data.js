import additions from '../../evidence/additions-v2.json';
import reconstruction from '../../data/reconstruction-evidence-map.json';
import components from '../../data/components.json';
import claims from '../../data/geometry.claims.json';
import conflicts from '../../data/conflicts.json';
import gaps from '../../data/knowledge-gaps.json';
import graph from '../../data/assembly.graph.json';
import manifest from '../../evidence/manifest.json';
import risks from '../../data/craft-risks.json';
import {normalizeAsset} from './assets.mjs';
export const db={components:components.components,terms:components.local_term_map,claims:claims.claims,conflicts:conflicts.conflicts,gaps:gaps.gaps,graph,manifest:{...manifest,assets:[...manifest.assets,...additions.assets].map(normalizeAsset)},risks,reconstruction:reconstruction.components};
export const gapMap={ 'COMP-SHAFT':['GAP-01','GAP-02','GAP-06'], 'COMP-ARMS':['GAP-02','GAP-08'], 'COMP-HUB-LAND':['GAP-02'], 'COMP-HUB-WATER':['GAP-02'], 'COMP-RIMS':['GAP-03','GAP-01'], 'COMP-RIM-LAND':['GAP-03','GAP-01'], 'COMP-RIM-WATER':['GAP-03','GAP-01'], 'COMP-KRUEMMLINGE':['GAP-03','GAP-08'], 'COMP-KUEMPFE':['GAP-04','GAP-05'], 'COMP-KUMPF-STAVES':['GAP-04'], 'COMP-KUMPF-BASE':['GAP-04'], 'COMP-KUMPF-HOOPS':['GAP-04'], 'COMP-PADDLES':['GAP-05','GAP-08'], 'COMP-FASTENERS':['GAP-02','GAP-04','GAP-08'], 'COMP-BEARINGS':['GAP-06'], 'COMP-RADSTATT':['GAP-01','GAP-07'], 'COMP-TROUGH':['GAP-07'], 'COMP-RINNE':['GAP-07'], 'COMP-BEARING-STANDS':['GAP-06','GAP-01'], 'COMP-FRAME-MAIN':['GAP-01','GAP-06'], 'COMP-FRAME-LOWER':['GAP-01','GAP-06'], 'COMP-FRAME-SIDE':['GAP-01','GAP-07'] };
export function relatedFamilies(id){return id.includes('RIM')||id==='COMP-KRUEMMLINGE'?['COMP-RIMS','COMP-RIM-LAND','COMP-RIM-WATER','COMP-KRUEMMLINGE']:id.includes('KUMPF')||id==='COMP-KUEMPFE'?['COMP-KUEMPFE','COMP-KUMPF-STAVES','COMP-KUMPF-BASE','COMP-KUMPF-HOOPS']:[id]}
export function context(id){const families=relatedFamilies(id);return {component:db.components.find(x=>x.id===id),claims:db.claims.filter(c=>families.includes(c.subject)),conflicts:db.conflicts.filter(c=>c.subjects.some(s=>families.includes(s))),gaps:(gapMap[id]||['GAP-08']).map(g=>db.gaps.find(x=>x.id===g)),relations:db.graph.relations.filter(r=>families.includes(r.from)||families.includes(r.to)),risks:db.risks.topics.filter(r=>r.components.some(c=>families.includes(c)))}}
