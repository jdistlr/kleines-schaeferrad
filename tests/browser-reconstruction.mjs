import {chromium,devices} from 'playwright';import http from 'node:http';import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';import crypto from 'node:crypto';
const root=path.resolve('dist'),out='test-results/reconstruction';fs.mkdirSync(out,{recursive:true});const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.pdf':'application/pdf','.svg':'image/svg+xml','.json':'application/json','.webmanifest':'application/manifest+json','.woff2':'font/woff2','.jpeg':'image/jpeg','.png':'image/png','.webp':'image/webp','.glb':'model/gltf-binary'};
const server=http.createServer((req,res)=>{let p=decodeURIComponent(new URL(req.url,'http://localhost').pathname).replace(/^\/kleines-schaeferrad\//,'');if(p.endsWith('/')||!p)p+='index.html';const f=path.resolve(root,p);if(!f.startsWith(root+path.sep)||!fs.existsSync(f)||!fs.statSync(f).isFile()){res.writeHead(404);return res.end('not found')}res.setHeader('Content-Type',mime[path.extname(f)]||'application/octet-stream');fs.createReadStream(f).pipe(res)});await new Promise(r=>server.listen(Number(process.env.KS_TEST_PORT||4322),'127.0.0.1',r));
const browser=await chromium.launch({headless:true,executablePath:process.env.KS_CHROMIUM_PATH||undefined,args:['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader']}),base=`http://127.0.0.1:${process.env.KS_TEST_PORT||4322}/kleines-schaeferrad/`;
const result={source_commit:process.env.GITHUB_SHA||null,gate:'automated checks only; independent visual review required',scope:'automated emulation, no human or physical Safari evidence',started_at:new Date().toISOString(),profiles:[],checks:[],status:'running'};let active;
async function zoomText(page){await page.evaluate(()=>{const rows=[...document.querySelectorAll('body,body *')].filter(e=>e instanceof HTMLElement&&!e.dataset.zoomChecked).map(e=>[e,getComputedStyle(e).fontSize,getComputedStyle(e).lineHeight]);for(const [e,size,line]of rows){e.style.fontSize=(parseFloat(size)*2)+'px';if(line!=='normal')e.style.lineHeight=(parseFloat(line)*2)+'px';e.dataset.zoomChecked='true'}})}
async function normalLanguage(page,name){
 const visible=await page.locator('body').innerText();
 const forbidden=visible.match(/\b(?:Research|Evidence|Claims|Conflict Matrix|Field Pack|Hypothesis|Ghosted|mapping to confirm|LAND\/WATER)\b|(?:TASK|COMP|CLAIM)-[A-Z0-9-]+|[←↑→↓↗↘↔]|\p{Extended_Pictographic}/gu)||[];
 assert.deepEqual(forbidden,[],`${name} default UI contains technical IDs, English or decorative symbols`);
}
async function layout(page,name){const o=await page.evaluate(()=>({w:innerWidth,scroll:document.documentElement.scrollWidth}));assert.ok(o.scroll<=o.w+1,`${name} overflow ${JSON.stringify(o)}`);const small=await page.locator('button:visible').evaluateAll(ns=>ns.filter(n=>{const r=n.getBoundingClientRect();return r.width<44||r.height<44}).map(n=>n.textContent));assert.deepEqual(small,[],`${name} touch controls`)}
const image=fs.readFileSync('evidence/raw/IMG_6858.jpeg'),sha=crypto.createHash('sha256').update(image).digest('hex');
try{
 for(const profile of [{name:'desktop',viewport:{width:1440,height:1000}},{name:'320px',viewport:{width:320,height:740}},{name:'iphone13-emulation',...devices['iPhone 13 Pro']},{name:'text200',viewport:{width:1280,height:1000},zoom:true}]){
  const {name,zoom,...opts}=profile,ctx=await browser.newContext({locale:'de-DE',...opts}),page=await ctx.newPage();active=page;page.setDefaultTimeout(30000);const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base+'feld/');await page.waitForFunction(()=>document.querySelector('#field-storage').textContent==='Lokal gesichert');await page.waitForFunction(()=>document.querySelector('#offline-status').textContent.includes('Offline bereit'),null,{timeout:120000});
  if(zoom)await zoomText(page);await layout(page,name);await normalLanguage(page,name+' field');await page.screenshot({path:`${out}/${name}-field-initial.png`,fullPage:true});await page.locator('[data-field=person]').fill('SIMULATION TEST');await page.locator('#field-next').click();await layout(page,name+' photos');
  for(const view of ['Übersicht von A','Übersicht von B','Pfeile und Person im Bild']){await page.locator('#photo-view').selectOption({label:view});await page.locator('#field-photos').setInputFiles({name:'SIMULATION-'+view+'.jpeg',mimeType:'image/jpeg',buffer:image});await page.waitForFunction(()=>!document.querySelector('#field-next').disabled)}
  await page.reload();await page.waitForSelector('#field-photos');assert.equal(await page.locator('.media-line').count(),3);await page.locator('#field-next').click();await page.locator('[data-field=quote]').fill('SIMULATION - kein reales Feldwissen');await page.locator('#field-next').click();await page.locator('[data-field=reviewed]').check();await page.locator('#field-next').click();await page.waitForFunction(()=>document.querySelector('#task-title').textContent.includes('Bleibende Referenzen und Kontrollmaß setzen'));
  await page.locator('#open-index').click();assert.match(await page.locator('[data-task="0"]').innerText(),/Aufgenommen/);await page.locator('#close-index').click();if(zoom){await zoomText(page);await layout(page,name+' resumed field')}await page.screenshot({path:`${out}/${name}-field.png`,fullPage:true});
  if(name==='desktop'){
   const guides=JSON.parse(fs.readFileSync('data/visual-guides.json'));
   const tasks=JSON.parse(fs.readFileSync('data/field-tasks.json')).tasks;
   const drawing=guides.guides.find(g=>g.visual_kind==='shared-geometry-projection');
   assert.ok(drawing,'a geometry-derived operational field guide exists');
   const ti=tasks.findIndex(t=>drawing.tasks.includes(t.task_id));assert.ok(ti>=0);
   await page.locator('#open-index').click();await page.locator(`[data-task="${ti}"]`).click();
   await page.screenshot({path:`${out}/desktop-field-technical.png`,fullPage:true});
   await normalLanguage(page,'technical field guide');
   await page.locator('#open-index').click();await page.locator('[data-task="1"]').click();await page.waitForFunction(()=>document.querySelector('#task-title').textContent.includes('Bleibende Referenzen und Kontrollmaß setzen'));
  }

  await page.goto(base+'werkstatt/');await page.waitForFunction(()=>document.querySelector('#render-status').textContent.includes('Ziehen:'));if(zoom)await zoomText(page);await layout(page,name+' workshop');await normalLanguage(page,name+' workshop');await page.screenshot({path:`${out}/${name}-workshop.png`,fullPage:true});
  if(name==='desktop'){
    const partIds=await page.locator('[data-part]').evaluateAll(ns=>ns.map(n=>n.dataset.part));
    for(const id of partIds){await page.locator(`[data-part="${id}"]`).click();await normalLanguage(page,'part '+id);assert.doesNotMatch(await page.locator('#selection').innerText(),/is not a proven|separate hub component/);}
    await page.locator('#reset').click();await page.evaluate(()=>scrollTo(0,0));
    for(const mode of ['betrieb','welle','exploded','schnitt','evidenz','scan']){
      await page.locator('#scene-mode').selectOption(mode);
      if(mode==='betrieb'){await page.locator('#play').click();assert.equal(await page.locator('#play').getAttribute('aria-pressed'),'true');}
      if(mode==='scan')await page.waitForFunction(()=>document.querySelector('#scan-status').textContent.includes('Punkte'));
      await page.evaluate(()=>new Promise(resolve=>{let n=0;function frame(){if(++n===60)resolve();else requestAnimationFrame(frame)}requestAnimationFrame(frame)}));
      await page.screenshot({path:`${out}/desktop-${mode}.png`,fullPage:true});
    }
    await page.locator('.technical-settings').evaluate(el=>el.open=true);
    for(const candidate of ['A','B','C'])await page.locator('#fastener-variant').selectOption(candidate);
    await page.locator('#fastener-variant').selectOption('A');
    for(const candidate of ['staggered','independent','crossing']){await page.locator('#joinery').selectOption(candidate);assert.match(await page.locator('#candidate-result').innerText(),/Rang/);}
    await page.locator('#joinery').selectOption('staggered');
    result.checks.push({test:'three nail mappings and three joinery variants selectable',status:'passed'});
    await page.locator('#scan-settings').evaluate(el=>el.open=true);
    await page.locator('#scan-source').selectOption('glb');
    await page.waitForFunction(()=>document.querySelector('#scan-status').textContent.includes('Oberflächenmodell'));
    await page.screenshot({path:`${out}/desktop-scan-glb.png`,fullPage:true});
    await page.locator('#scene-mode').selectOption('gesamt');
    assert.equal(await page.locator('#scan-host').isVisible(),false);
    result.checks.push({test:'scan workspace entry, separate PLY and GLB, return to model',status:'passed'});
  }
  await page.goto(base);if(zoom)await zoomText(page);await layout(page,name+' story');await normalLanguage(page,name+' story');await page.screenshot({path:`${out}/${name}-story.png`,fullPage:true});assert.deepEqual(errors,[]);result.profiles.push({name,status:'passed',capture_resume:true,views:true,overflow:false,min_target_px:44,text_zoom:!!zoom});
  if(name==='desktop'){
   await page.goto(base+'feld/');await page.waitForFunction(()=>document.querySelector('#offline-status').textContent.includes('Offline bereit'));await ctx.setOffline(true);await page.reload();await page.waitForFunction(()=>document.querySelector('#field-storage').textContent==='Lokal gesichert');assert.match(await page.locator('#task-title').innerText(),/Bleibende Referenzen und Kontrollmaß setzen/);
   await page.locator('#open-index').click();await page.locator('[data-task="0"]').click();await page.locator('#field-next').click();await page.locator('#photo-view').selectOption({label:'Übersicht von A'});await page.locator('#field-photos').setInputFiles(Array.from({length:25},(_,i)=>({name:`SIMULATION-LOAD-${i}.jpeg`,mimeType:'image/jpeg',buffer:image})));await page.waitForFunction(()=>document.querySelectorAll('.media-line').length===28&&!document.querySelector('#field-next').disabled,null,{timeout:120000});await page.reload();await page.waitForFunction(()=>document.querySelectorAll('.media-line').length===28);
   await page.locator('#open-register').click();for(const [k,v] of Object.entries({id:'KS-ARM-001',local_name:'SIMULATION Arm',installed_position:'TEST A',partners:'KS-KEI-001',condition:'TEST',removal_event:'EVT-SIM-001',storage_location:'TEST Lager',person:'SIMULATION'}))await page.locator(`#instance-form [name=${k}]`).fill(v);await page.locator('#instance-form [name=observed]').check();await page.locator('#instance-form button[type=submit]').click();await page.waitForFunction(()=>document.querySelector('#instance-list').textContent.includes('KS-ARM-001'));await page.locator('#close-register').click();
   await page.locator('#open-backup').click();const d=page.waitForEvent('download');await page.locator('#field-export').click();const download=await d,exportPath=`${out}/offline-capture.json`;await download.saveAs(exportPath);const exported=JSON.parse(fs.readFileSync(exportPath));assert.equal(exported.media.length,28);assert.equal(exported.session.instances.length,1);assert.equal(exported.session.events.length,1);for(const m of exported.media){const b=Buffer.from(m.base64,'base64');assert.equal(b.length,image.length);assert.equal(crypto.createHash('sha256').update(b).digest('hex'),sha)}
   await ctx.setOffline(false);const restoreCtx=await browser.newContext({locale:'de-DE'}),restore=await restoreCtx.newPage();await restore.goto(base+'feld/');await restore.waitForFunction(()=>document.querySelector('#offline-status').textContent.includes('Offline bereit'));await restoreCtx.setOffline(true);await restore.locator('#open-backup').click();await restore.locator('#field-import').setInputFiles(exportPath);await restore.waitForFunction(()=>document.querySelector('#backup-status').textContent.includes('Prüfsummen bestätigt'),null,{timeout:120000});await restore.reload();await restore.waitForFunction(()=>document.querySelectorAll('.media-line').length===28);await restore.screenshot({path:`${out}/offline-restored.png`,fullPage:true});await restoreCtx.close();
   result.checks.push({test:'offline reload + 25 additional photos + resume + instance/event + offline export + offline fresh-context import',status:'passed',photo_count:28,photo_bytes:28*image.length,sha256_verified:true,fixture:'Repeated original JPEG with SIMULATION filenames; not a physical field session'});
   fs.writeFileSync(`${out}/capture-summary.json`,JSON.stringify({session:exported.session,media:exported.media.map(({base64,...m})=>m)},null,2));fs.unlinkSync(exportPath);
  }
  await ctx.close();
 }
 result.status='passed';
}catch(e){result.status='failed';result.error=e.stack;if(active&&!active.isClosed())await active.screenshot({path:`out`.replace('out',out)+'/failure.png',fullPage:true}).catch(()=>{});throw e}finally{result.finished_at=new Date().toISOString();fs.writeFileSync(`${out}/validation.json`,JSON.stringify(result,null,2));await browser.close();await new Promise(r=>server.close(r))}
