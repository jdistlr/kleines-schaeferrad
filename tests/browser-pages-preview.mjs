import {chromium} from 'playwright';
import fs from 'node:fs';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {spawn} from 'node:child_process';
import {serve} from './control-server.mjs';
const remote=process.env.KS_REVIEW_URL;
const server=remote?null:await serve(process.env.KS_COMBINED_DIST||'combined-dist',4331);
const base=remote||server.base+'review/pr-18/';
assert.ok(base.endsWith('/kleines-schaeferrad/review/pr-18/'));
const prod=base.replace(/review\/pr-18\/$/,'');
const out=process.env.KS_TEST_OUTPUT||'test-results/pages-preview';fs.mkdirSync(out,{recursive:true});
const report={preview:base,production:prod,physicalIPhone:false,checks:[],status:'running'};
const browser=await chromium.launch({executablePath:process.env.KS_CHROMIUM_PATH||undefined,args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
try{
 // A new isolated browser context, never a real user's field records.
 const ctx=await browser.newContext({viewport:{width:390,height:844}}),p=await ctx.newPage();
 await p.goto(prod+'feld/');
 await p.waitForFunction(()=>document.querySelector('#offline-status')?.textContent.includes('Offline bereit'),null,{timeout:300000});
 const productionState=await p.evaluate(async()=>{
  const read=name=>new Promise((resolve,reject)=>{const r=indexedDB.open(name);r.onsuccess=()=>{const db=r.result,q=db.transaction('state').objectStore('state').get('session');q.onsuccess=()=>{resolve(q.result);db.close()};q.onerror=()=>reject(q.error)};r.onerror=()=>reject(r.error)});
  return {session:await read('ks-pre-disassembly'),caches:await caches.keys()};
 });
 await p.goto(base+'control/water/?part=COMP-KUEMPFE&property=GAP-07');
 await p.waitForSelector('#cp-part');
 assert.equal(await p.locator('#cp-part').inputValue(),'COMP-KUEMPFE');
 await p.locator('[data-water-capture]').click();
 await p.waitForFunction(()=>document.querySelector('#field-storage')?.textContent.includes('Lokal gesichert'));
 await p.locator('[data-field="person"]').fill('PREVIEW ISOLATION — SYNTHETIC');
 await p.locator('#field-next').click();await p.waitForSelector('#field-photos');
 await p.waitForFunction(()=>document.querySelector('#offline-status')?.textContent.includes('Offline bereit'),null,{timeout:300000});
 await p.reload();await p.waitForSelector('#field-photos');
 const isolated=await p.evaluate(async()=>{
  const read=name=>new Promise((resolve,reject)=>{const r=indexedDB.open(name);r.onsuccess=()=>{const db=r.result,q=db.transaction('state').objectStore('state').get('session');q.onsuccess=()=>{resolve(q.result);db.close()};q.onerror=()=>reject(q.error)};r.onerror=()=>reject(r.error)});
  return {production:await read('ks-pre-disassembly'),preview:await read('ks-preview-pr18-pre-disassembly'),caches:await caches.keys(),scope:navigator.serviceWorker.controller?.scriptURL,registrations:(await navigator.serviceWorker.getRegistrations()).map(r=>r.scope)};
 });
 assert.deepEqual(isolated.production,productionState.session);
 assert.notEqual(isolated.preview.id,productionState.session.id);
 assert.ok(isolated.scope.startsWith(base));
 for(const c of productionState.caches)assert.ok(isolated.caches.includes(c));
 assert.ok(isolated.caches.some(c=>c.startsWith('ks-preview-pr18-cache-')));
 await p.screenshot({path:out+'/phone-field.png',fullPage:true});
 await ctx.setOffline(true);await p.reload();await p.waitForSelector('#field-photos');
 await p.goto(base+'control/');await p.waitForSelector('.cp-nav');await ctx.setOffline(false);
 // Install the original parent worker again after the preview exists: its cleanup must not touch preview caches.
 await p.goto(prod+'feld/');
 await p.evaluate(async productionURL=>{const regs=await navigator.serviceWorker.getRegistrations();for(const r of regs)if(r.scope===productionURL)await r.unregister();const r=await navigator.serviceWorker.register(productionURL+'sw.js',{scope:productionURL});await new Promise((resolve,reject)=>{const w=r.installing||r.waiting||r.active;if(w.state==='activated')return resolve();w.addEventListener('statechange',()=>{if(w.state==='activated')resolve();if(w.state==='redundant')reject(Error('parent SW failed'))})})},prod);
 assert.ok(await p.evaluate(async()=> (await caches.keys()).some(c=>c.startsWith('ks-preview-pr18-cache-'))));
 await p.goto(base+'feld/');await p.waitForSelector('#field-photos');
 report.checks.push({productionFirstPreviewSecond:true,productionSessionUnchanged:true,separateSessionIDs:true,previewWorkerScope:isolated.scope,parentWorkerReinstallPreservesPreviewCache:true,previewOfflineReload:true});
 await ctx.close();
 // Check every production file against the original published artifact, not a rebuild.
 const hashFile=process.env.KS_PRODUCTION_HASHES||'test-results/pages-preview/production-sha256.json';
 const hashes=JSON.parse(fs.readFileSync(hashFile)),entries=Object.entries(hashes);let checked=0;
 await Promise.all(Array.from({length:4},async()=>{for(;;){const entry=entries.pop();if(!entry)return;const [file,expected]=entry;const r=await fetch(prod+file.split('/').map(encodeURIComponent).join('/'));assert.equal(r.status,200,file);assert.equal(crypto.createHash('sha256').update(Buffer.from(await r.arrayBuffer())).digest('hex'),expected,file);checked++}}));
 report.checks.push({productionFilesVerified:checked});
 // Reuse full existing acceptance against the combined local tree or actual HTTPS URL.
 await new Promise((resolve,reject)=>{const child=spawn(process.execPath,['tests/browser-control-plane.mjs'],{stdio:'inherit',env:{...process.env,KS_REVIEW_URL:base,KS_TEST_OUTPUT:out+'/acceptance'}});child.on('error',reject);child.on('exit',code=>code===0?resolve():reject(Error('Control Plane acceptance exit '+code)))});
 report.status='passed';
}catch(e){report.status='failed';report.error=e.stack;throw e}
finally{fs.writeFileSync(out+'/results.json',JSON.stringify(report,null,2));await browser.close();if(server)await server.close()}
