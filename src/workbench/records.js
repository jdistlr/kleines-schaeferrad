export const SCHEMA='ks-field-capture/v1';
const storagePrefix=import.meta.env?.PUBLIC_STORAGE_NAMESPACE;
const workbenchDatabase=storagePrefix?storagePrefix+'-field-workbench':'ks-field-workbench';
export const kinds=['measurement','observation','identification','expert-narrative','risk'];
export function validateRecord(r){
 if(!r||typeof r!=='object'||!/^OBS-/.test(r.id)||!kinds.includes(r.kind))throw Error('Ungültiger Observation Record.');
 if(!Array.isArray(r.component_ids)||!r.component_ids.length||!r.component_ids.every(x=>typeof x==='string'))throw Error('Bauteilbezug fehlt.');
 if(typeof r.timestamp!=='string'||!Number.isFinite(Date.parse(r.timestamp)))throw Error('Zeitstempel fehlt.');
 if(typeof r.question_id!=='string'||typeof r.event_id!=='string'||typeof r.person!=='string'||!r.person.trim()||!r.event_id.trim())throw Error('Frage, Ereignis oder Person fehlt.');
 if(!['LAND','WATER','UNKNOWN'].includes(r.side)||!['installed','during-release','removed'].includes(r.state))throw Error('Ungültiger Einbaukontext.');
 if(r.kind==='measurement'&&!r.unknown){if(typeof r.value!=='number'||!Number.isFinite(r.value)||typeof r.uncertainty!=='number'||!Number.isFinite(r.uncertainty)||r.uncertainty<0||!r.unit||!r.tool||!r.endpoints?.a||!r.endpoints?.b)throw Error('Messung braucht Zahl, Einheit, Endpunkte, Werkzeug und Unsicherheit.');}
 if(!Array.isArray(r.media))throw Error('Medienliste fehlt.');
 for(const m of r.media){if(typeof m.name!=='string'||typeof m.id!=='string')throw Error('Ungültige Medienreferenz.');if(m.data_url&&!/^data:image\/(jpeg|png|webp);base64,[a-zA-Z0-9+/=]+$/.test(m.data_url))throw Error('Nicht unterstützte Bilddaten.');}
 return r;
}
export function mergeImport(existing,payload){
 if(payload?.schema!==SCHEMA||!Array.isArray(payload.records))throw Error('Kein unterstützter Feldprotokoll-Export.');
 const map=new Map(existing.map(r=>[r.id,r]));
 for(const r of payload.records){validateRecord(r);if(map.has(r.id)&&JSON.stringify(map.get(r.id))!==JSON.stringify(r))throw Error(`ID-Konflikt ${r.id}: nichts importiert; Original und Import separat sichern.`);map.set(r.id,r)}
 return [...map.values()];
}
export function openStore(){return new Promise((resolve,reject)=>{const req=indexedDB.open(workbenchDatabase,1);req.onupgradeneeded=()=>req.result.createObjectStore('state');req.onerror=()=>reject(req.error);req.onsuccess=()=>resolve(req.result)})}
export function readStore(db){return new Promise((resolve,reject)=>{const req=db.transaction('state').objectStore('state').get('session');req.onsuccess=()=>resolve(req.result);req.onerror=()=>reject(req.error)})}
export function writeStore(db,value){return new Promise((resolve,reject)=>{const tx=db.transaction('state','readwrite');tx.objectStore('state').put(value,'session');tx.oncomplete=()=>resolve();tx.onerror=()=>reject(tx.error);tx.onabort=()=>reject(tx.error||Error('Speicherung abgebrochen'))})}
