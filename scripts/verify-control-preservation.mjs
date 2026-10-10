import {execFileSync} from 'node:child_process';import fs from 'node:fs';import crypto from 'node:crypto';import assert from 'node:assert/strict';
const baseline='606908bfe8cf1ab0560b337f37d92dd90d320dee',git=(...args)=>execFileSync('git',args,{encoding:'utf8'}).trim();
const protectedPaths=['data','evidence','output','src/workbench/geometry.mjs','src/workbench/calibration.mjs','src/workbench/expert-corrections.mjs'];
// Only the database name selection may differ; every v1 storage operation stays byte-identical.
for(const [file,variable,name] of [['src/field/store.js','fieldDatabase','ks-pre-disassembly'],['src/workbench/records.js','workbenchDatabase','ks-field-workbench']]){
 const original=execFileSync('git',['show',baseline+':'+file],{encoding:'utf8'});
 const actual=fs.readFileSync(file,'utf8').replace(/^const storagePrefix=.*\n/m,'').replace(new RegExp('^const '+variable+'=.*\\n','m'),'').replace('indexedDB.open('+variable+',','indexedDB.open(\''+name+'\',');
 assert.equal(actual,original,'Only database namespace selection is authorized: '+file);
}
const changed=git('diff',baseline,'--name-only','--',...protectedPaths);assert.equal(changed,'','protected geometry/evidence/storage path changed');
const claims=JSON.parse(fs.readFileSync('data/geometry.claims.json')).claims.filter(c=>c.id.startsWith('TH-20261009-'));assert.equal(claims.length,39);assert.ok(claims.every(c=>c.as_built_eligible===false));
const tasks=JSON.parse(fs.readFileSync('data/field-tasks.json')).tasks;assert.equal(tasks.length,21);
const photo=JSON.parse(fs.readFileSync('evidence/contributions/torsten-20261010-original.json')).images[0];const hash=crypto.createHash('sha256').update(fs.readFileSync(photo.path)).digest('hex');assert.equal(hash,photo.sha256);
const result={baseline,head:git('rev-parse','HEAD'),protectedPaths,changed,expertStatements:claims.length,taskOrder:tasks.map(t=>t.task_id),annotatedOriginal:{path:photo.path,sha256:hash},status:'passed',meaning:'Byte-preservation, not independent metric or engineering acceptance'};
fs.mkdirSync('test-results/control-plane',{recursive:true});fs.writeFileSync('test-results/control-plane/preservation.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));
