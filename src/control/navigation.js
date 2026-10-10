import {readContext,contextQuery} from './context.mjs';
const root=document.querySelector('.cp'),base=root.dataset.base,model=JSON.parse(root.dataset.context);
const current=location.pathname.includes('/water/')?'water':location.pathname.includes('/evidence/')?'evidence':'overview';
let context={...readContext(location.search,model.components,model.gaps),from:current};
const incoming=new URLSearchParams(location.search);if(model.tasks.some(t=>t.task_id===incoming.get('task'))){context.task=incoming.get('task');if(/^[0-4]$/.test(incoming.get('step')||''))context.step=incoming.get('step')}
if(!context.part)context.part=current==='water'?'COMP-TROUGH':'COMP-SHAFT';
if(!context.property)context.property=current==='water'?'GAP-07':'GAP-01';
const part=document.getElementById('cp-part'),property=document.getElementById('cp-property');
if(part&&[...part.options].some(o=>o.value===context.part))part.value=context.part;
if(property&&[...property.options].some(o=>o.value===context.property))property.value=context.property;
export function activeContext(){return {...context}}
function update(){
 if(part)context.part=part.value;if(property)context.property=property.value;
 const query=contextQuery(context);
 for(const a of document.querySelectorAll('[data-context-link]')){
  const type=a.dataset.contextLink,q=new URLSearchParams(query);let route='control/';
  if(type==='construction'){route='werkstatt/';if(current==='water')q.set('view','betrieb')}
  if(type==='water')route='control/water/';if(type==='evidence')route='control/evidence/';
  if(type==='field'){route='feld/';/* Resume existing field work unless water context explicitly requests it. */if(current==='water')q.set('task','TASK-WATER')}
  if(type==='field'&&context.task){q.set('task',context.task);if(context.step)q.set('step',context.step)}
  a.href=base+route+'?'+q;
 }
 for(const a of document.querySelectorAll('[data-water-capture]')){const q=new URLSearchParams(query);q.set('task','TASK-WATER');if(context.task!=='TASK-WATER')q.delete('step');q.set('from','water');q.set('property','GAP-07');a.href=base+'feld/?'+q}
 const url=new URL(location.href);for(const key of ['part','property'])url.searchParams.set(key,context[key]);history.replaceState(null,'',url);
 document.dispatchEvent(new CustomEvent('cp-context',{detail:context}));
}
part?.addEventListener('change',update);property?.addEventListener('change',update);update();
