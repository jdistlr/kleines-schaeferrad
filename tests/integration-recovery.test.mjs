import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import {normalizeAsset,isImageAsset} from '../src/workbench/assets.mjs';
const read=p=>JSON.parse(fs.readFileSync(p));
const original=[...read('evidence/manifest.json').assets,...read('evidence/additions-v2.json').assets];
test('all source schema variants resolve without mutating evidence; Thorsten JPEGs and narrative remain usable',()=>{
  const assets=original.map(normalizeAsset);
  for(let i=0;i<assets.length;i++){
    const a=assets[i];assert.equal(a.id,original[i].id);assert.equal(a.sha256,original[i].sha256);
    if(a.archive)assert.ok(fs.existsSync(a.archive.path),a.archive.path);
    assert.doesNotThrow(()=>isImageAsset(a));
  }
  const photos=assets.filter(a=>a.id.startsWith('PHOTO-TH-'));
  assert.equal(photos.length,65);assert.ok(photos.every(isImageAsset));
  for(const a of photos)assert.equal(crypto.createHash('sha256').update(fs.readFileSync(a.archive.path)).digest('hex'),a.sha256);
  const narrative=assets.find(a=>a.id==='NARRATIVE-TH-CONSTRUCTION-20261009');
  assert.equal(isImageAsset(narrative),false);assert.equal(narrative.archive.path,'evidence/contributions/thorsten-20261009.json');
  assert.equal(isImageAsset(normalizeAsset({id:'external'})),false);
});
test('all 39 expert statements keep canonical backlinks and no as-built promotion',()=>{
  const claims=read('data/geometry.claims.json').claims.filter(c=>c.id.startsWith('TH-20261009-'));
  const analyses=read('data/source-analyses.json').sources;
  assert.equal(claims.length,39);
  for(const c of claims){assert.equal(c.as_built_eligible,false);assert.ok(analyses.some(a=>a.claim_ids.includes(c.id)),c.id);}
});
