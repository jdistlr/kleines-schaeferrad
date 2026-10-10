import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const base='/kleines-schaeferrad/';
function walk(dir){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(d=>d.isDirectory()?walk(path.join(dir,d.name)):[path.join(dir,d.name)])}
// Application shell, technical sheets and raw evidence are one explicit offline preload.
// Original evidence is cached unchanged, never rewritten. User media stays in IndexedDB.
const files=walk('dist').filter(p=>!p.endsWith('/sw.js')&&!p.endsWith('/offline-manifest.json'));
const fingerprint=crypto.createHash('sha256');for(const f of files.sort()){fingerprint.update(f);fingerprint.update(fs.readFileSync(f))}
const cache_name='ks-field-'+fingerprint.digest('hex').slice(0,16),urls=files.map(f=>base+f.slice(5).split('/').map(encodeURIComponent).join('/'));
for(const route of ['', 'feld/','werkstatt/','control/','control/water/','control/evidence/'])urls.push(base+route);
const info={schema:'ks-offline-preload/v1',cache_name,urls,bytes:files.reduce((s,p)=>s+fs.statSync(p).size,0),scope:base,policy:'Atomic complete install; old cache kept on failure; local captures in IndexedDB, never in SW cache.'};
fs.writeFileSync('dist/offline-manifest.json',JSON.stringify(info,null,2));
fs.writeFileSync('dist/sw.js',`const CACHE=${JSON.stringify(cache_name)},URLS=${JSON.stringify([...urls,base+'offline-manifest.json'])},BASE=${JSON.stringify(base)};
self.addEventListener('install',e=>e.waitUntil((async()=>{const cache=await caches.open(CACHE);try{for(const url of URLS){const r=await fetch(new Request(url,{cache:'reload'}));if(!r.ok)throw Error('Offline preload '+url);await cache.put(url,r)}await self.skipWaiting()}catch(error){await caches.delete(CACHE);throw error}})()));
self.addEventListener('activate',e=>e.waitUntil((async()=>{for(const key of await caches.keys())if(key.startsWith('ks-field-')&&key!==CACHE)await caches.delete(key);await self.clients.claim()})()));
self.addEventListener('fetch',e=>{const url=new URL(e.request.url);if(e.request.method!=='GET'||url.origin!==self.location.origin||!url.pathname.startsWith(BASE))return;e.respondWith((async()=>{const cache=await caches.open(CACHE);const key=url.origin+url.pathname;const cached=await cache.match(key);if(cached)return cached;try{return await fetch(e.request)}catch(error){return new Response('Nicht im Offline-Vorrat. Zur Feldseite zurückkehren.',{status:503,headers:{'Content-Type':'text/plain;charset=utf-8'}})}})())});`);
fs.mkdirSync('state/field-kit',{recursive:true});fs.writeFileSync('state/field-kit/offline-build-manifest.json',JSON.stringify(info,null,2));console.log('Offline shell:',urls.length,'files,',info.bytes,'bytes');
