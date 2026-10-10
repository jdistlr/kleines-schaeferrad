import {execFileSync} from 'node:child_process';import fs from 'node:fs';import crypto from 'node:crypto';import assert from 'node:assert/strict';
const baseline='606908bfe8cf1ab0560b337f37d92dd90d320dee',git=(...args)=>execFileSync('git',args,{encoding:'utf8'}).trim();
const protectedPaths=['data','evidence','output','src/workbench/geometry.mjs','src/workbench/calibration.mjs','src/workbench/expert-corrections.mjs','src/workbench/records.js','src/field/store.js'];
const changed=git('diff',baseline,'--name-only','--',...protectedPaths);assert.equal(changed,'','protected geometry/evidence/storage path changed');
const claims=JSON.parse(fs.readFileSync('data/geometry.claims.json')).claims.filter(c=>c.id.startsWith('TH-20261009-'));assert.equal(claims.length,39);assert.ok(claims.every(c=>c.as_built_eligible===false));
const tasks=JSON.parse(fs.readFileSync('data/field-tasks.json')).tasks;assert.equal(tasks.length,21);
const photo=JSON.parse(fs.readFileSync('evidence/contributions/torsten-20261010-original.json')).images[0];const hash=crypto.createHash('sha256').update(fs.readFileSync(photo.path)).digest('hex');assert.equal(hash,photo.sha256);
const result={baseline,head:git('rev-parse','HEAD'),protectedPaths,changed,expertStatements:claims.length,taskOrder:tasks.map(t=>t.task_id),annotatedOriginal:{path:photo.path,sha256:hash},status:'passed',meaning:'Byte-preservation, not independent metric or engineering acceptance'};
fs.mkdirSync('test-results/control-plane',{recursive:true});fs.writeFileSync('test-results/control-plane/preservation.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));
