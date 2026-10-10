// URL context is navigation only. No field payload or storage schema changes.
export function readContext(search,components,gaps){
 const q=new URLSearchParams(search),alias=q.get('part')==='COMP-RADSTADT'?'COMP-RADSTATT':q.get('part');
 return {part:components.some(c=>c.id===alias)?alias:null,property:gaps.some(g=>g.id===q.get('property'))?q.get('property'):null,from:['water','evidence','overview'].includes(q.get('from'))?q.get('from'):'overview'};
}
export function contextQuery(context){const q=new URLSearchParams();for(const k of ['part','property','from','task','step'])if(context[k])q.set(k,context[k]);return q}
export function boundedParameter(value,min,max){if(value===null||value==='')return null;const n=Number(value);return Number.isFinite(n)&&n>=min&&n<=max?n:null}
