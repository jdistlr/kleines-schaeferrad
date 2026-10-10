import claims from '../../data/geometry.claims.json';
import calibration from '../../data/calibration-v3.json';
import sources from '../../data/source-analyses.json';
import tasks from '../../data/field-tasks.json';
import gaps from '../../data/knowledge-gaps.json';
import components from '../../data/components.json';
export const model={revision:calibration.iteration,claims:claims.claims,sources:sources.sources,tasks:tasks.tasks,gaps:gaps.gaps,components:components.components};
export const expertClaims=model.claims.filter(c=>/^TH-20261009-\d{2}$/.test(c.id));
export const narrative=model.sources.find(s=>s.source_id==='NARRATIVE-TH-CONSTRUCTION-20261009');
export const waterTask=model.tasks.find(t=>t.task_id==='TASK-WATER');
export const sourceRevision='606908bfe8cf1ab0560b337f37d92dd90d320dee';
export const sourceUrl=path=>`https://github.com/jdistlr/kleines-schaeferrad/blob/${sourceRevision}/${path}`;
/** @type {Record<string,string>} */
export const classLabels={'expert-narrative':'Fachauskunft','observed-current':'Beobachtung',measured:'Quellenmessung · Geltungsbereich prüfen','historical-drawing':'Historische Zeichnung',inferred:'Annahme',derived:'Ableitung',unknown:'Offen',conflicting:'Widerspruch','external-context':'Kontextquelle'};

if(!narrative||!waterTask)throw new Error("Required control-plane source contract missing");
