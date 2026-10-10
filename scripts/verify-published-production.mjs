import fs from 'node:fs';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
const base='https://jdistlr.github.io/kleines-schaeferrad/';
const hashes=JSON.parse(fs.readFileSync('test-results/pages-preview/production-sha256.json'));
const entries=Object.entries(hashes);let verified=0;
await Promise.all(Array.from({length:4},async()=>{for(;;){const entry=entries.pop();if(!entry)return;const [file,expected]=entry;const r=await fetch(base+file.split('/').map(encodeURIComponent).join('/'),{signal:AbortSignal.timeout(60000)});assert.equal(r.status,200,file);assert.equal(crypto.createHash('sha256').update(Buffer.from(await r.arrayBuffer())).digest('hex'),expected,file);verified++}}));
fs.writeFileSync('test-results/pages-preview/production-live-before.json',JSON.stringify({base,verified,status:'passed',checkedAt:new Date().toISOString()},null,2));
console.log('Published production matches original artifact:',verified,'files');
