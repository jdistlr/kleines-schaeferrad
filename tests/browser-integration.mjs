import {chromium} from 'playwright';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
const root=path.resolve('dist'),out='test-results/integration';fs.mkdirSync(out,{recursive:true});
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.svg':'image/svg+xml','.json':'application/json','.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.woff2':'font/woff2'};
const server=http.createServer((req,res)=>{let p=decodeURIComponent(new URL(req.url,'http://localhost').pathname).replace(/^\/kleines-schaeferrad\//,'');if(p.endsWith('/'))p+='index.html';const f=path.resolve(root,p);if(!f.startsWith(root+path.sep)||!fs.existsSync(f)){res.writeHead(404);return res.end()}res.setHeader('Content-Type',mime[path.extname(f)]||'application/octet-stream');fs.createReadStream(f).pipe(res)});
await new Promise(r=>server.listen(4325,'127.0.0.1',r));
const browser=await chromium.launch({headless:true,executablePath:process.env.KS_CHROMIUM_PATH||undefined,args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const result={status:'running',checks:[],scope:'Chromium simulation; no physical device or engineering release'},base='http://127.0.0.1:4325/kleines-schaeferrad/';
try{
 const ctx=await browser.newContext(),page=await ctx.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base+'werkstatt/');await page.waitForFunction(()=>document.querySelector('#storage-status').textContent.includes('Lokal gesichert'));
 await page.waitForFunction(()=>document.querySelector('#render-status').textContent.includes('Ziehen:'));
 const canvas=page.locator('#canvas-host canvas');
 // The idle viewer must release the shared GPU; continuous redraw starved the
 // second context's startup in field acceptance on software WebGL.
 async function frameCount(){return Number(await canvas.getAttribute('data-render-count'))}
 async function settled(){
  // Wall-clock silence is not proof of idleness when a software-GPU frame is
  // still in flight. Observe completed animation frames instead; an always-
  // rendering viewer cannot pass this assertion even on a stalled runner.
  await page.evaluate(()=>{window.__lastRenderCount=null;window.__stableRenderFrames=0});
  await page.waitForFunction(()=>{
   const count=document.querySelector('#canvas-host canvas')?.dataset.renderCount;
   window.__stableRenderFrames=window.__lastRenderCount===count?window.__stableRenderFrames+1:0;
   window.__lastRenderCount=count;
   return Number(count)>0&&window.__stableRenderFrames>=12;
  });
 }
 await settled();
 const second=await browser.newContext(),secondPage=await second.newPage();
 await secondPage.goto(base+'werkstatt/');
 await secondPage.waitForFunction(()=>document.querySelector('#storage-status').textContent.includes('Lokal gesichert'));
 await secondPage.waitForFunction(()=>Number(document.querySelector('#canvas-host canvas')?.dataset.renderCount)>0);
 await second.close();
 await page.locator('#scene-mode').selectOption('betrieb');await settled();
 const stopped=await frameCount();await page.locator('#play').click();
 await page.waitForFunction(n=>Number(document.querySelector('#canvas-host canvas').dataset.renderCount)>n+2,stopped);
 await page.locator('#play').click();await settled();
 // settled() requires twelve consecutive animation frames without a redraw.
 await page.locator('#reset').click();await settled();
 const beforeDrag=await frameCount(),bounds=await canvas.boundingBox();
 await page.mouse.move(bounds.x+bounds.width/2,bounds.y+bounds.height/2);await page.mouse.down();
 await page.mouse.move(bounds.x+bounds.width/2+80,bounds.y+bounds.height/2+30,{steps:4});await page.mouse.up();
 await settled();assert.ok(await frameCount()>beforeDrag,'orbit interaction must redraw');
 result.checks.push({idleRendering:'12 consecutive animation frames without redraw',concurrentContext:'ready',animation:'runs and pauses',orbit:'redraws'});

 for(const mode of ['truth','brute']){
  await page.locator('#model-mode').selectOption(mode);assert.equal(await canvas.getAttribute('data-model-mode'),mode);
  const stationary=Number(await canvas.getAttribute('data-stationary-count')),nails=Number(await canvas.getAttribute('data-nail-path-count'));
  assert.equal(nails,mode==='truth'?0:48);assert.ok(mode==='truth'?stationary===0:stationary>0);
  await page.screenshot({path:`${out}/${mode}.png`});result.checks.push({mode,stationary,nails,meshCount:Number(await canvas.getAttribute('data-mesh-count'))});
 }
 const modes=await page.locator('#scene-mode option').evaluateAll(ns=>ns.map(n=>n.value));
 for(const mode of modes){await page.locator('#scene-mode').selectOption(mode);if(mode==='scan')await page.waitForFunction(()=>document.querySelector('#scan-status').textContent.includes('Punktewolke'));}
 await page.locator('#scene-mode').selectOption('gesamt');
 const ids=await page.locator('[data-part]').evaluateAll(ns=>ns.map(n=>n.dataset.part));
 for(const id of ids){await page.locator(`[data-part="${id}"]`).click();assert.ok(await page.locator('#selection h3').innerText());}
 for(const photo of await page.locator('#selection img').all()){await photo.evaluate(img=>img.loading='eager');}
 assert.deepEqual(errors,[]);result.checks.push({allSceneModes:modes,allComponentInspectors:ids.length});await ctx.close();
 // A failed WebGL context must not prevent editing and persistent capture.
 const noGL=await browser.newContext();await noGL.addInitScript(()=>{const original=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(type,...args){return /webgl/i.test(type)?null:original.call(this,type,...args)}});
 const fallback=await noGL.newPage();await fallback.goto(base+'werkstatt/');await fallback.waitForFunction(()=>document.querySelector('#storage-status').textContent.includes('Lokal gesichert'));await fallback.waitForFunction(()=>document.querySelector('#render-status').textContent.includes('3D nicht verfügbar'));assert.match(await fallback.locator('#render-status').innerText(),/3D nicht verfügbar/);assert.ok(await fallback.locator('[data-part]').count());await fallback.screenshot({path:`${out}/webgl-fallback.png`});await noGL.close();result.checks.push({webglUnavailable:'capture still saved'});
 const noDB=await browser.newContext();await noDB.addInitScript(()=>{IDBFactory.prototype.open=function(){throw new DOMException('Simulated storage denial','SecurityError')}});
 const denied=await noDB.newPage();await denied.goto(base+'werkstatt/');await denied.waitForFunction(()=>document.querySelector('#storage-status').textContent.includes('Speicher nicht verfügbar'));await denied.waitForFunction(()=>document.querySelector('#render-status').textContent.includes('Ziehen:'));const d=denied.waitForEvent('download');await denied.locator('#export').click();await (await d).saveAs(`${out}/storage-denied-export.json`);assert.equal(JSON.parse(fs.readFileSync(`${out}/storage-denied-export.json`)).schema,'ks-field-capture/v1');await noDB.close();result.checks.push({storageDenied:'viewer and JSON export available'});
 result.status='passed';
}catch(e){result.status='failed';result.error=e.stack;throw e}finally{fs.writeFileSync(`${out}/results.json`,JSON.stringify(result,null,2));await browser.close();await new Promise(r=>server.close(r))}
