import {activeContext} from './navigation.js';
import {contextQuery} from './context.mjs';
const $=id=>document.getElementById(id);let cycle=null;
function update(){if(!cycle)return;const degrees=Number($('cp-phase').value),waterLevel=Number($('cp-level').value),rotationRPM=Number($('cp-rpm').value);
 $('cp-phase-output').textContent=degrees+'°';$('cp-level-output').textContent=waterLevel.toLocaleString('de-DE',{minimumFractionDigits:2})+' m';$('cp-rpm-output').textContent=rotationRPM.toLocaleString('de-DE')+' U/min';
 const result=cycle(degrees*Math.PI/180,{waterLevel,rotationRPM});
 $('cp-cycle-result').textContent=`Kandidat bei ${degrees}°: ${result.state}. Modellfüllung ${Math.round(result.fill*100)} % des modellierten Innenraums — keine gemessene Wassermenge.`;
 const angle=degrees*Math.PI/180;$('cp-vessel-dot').setAttribute('cx',String(250-Math.sin(angle)*128));$('cp-vessel-dot').setAttribute('cy',String(200-Math.cos(angle)*128));
 const q=contextQuery({...activeContext(),from:'water'});q.set('view','betrieb');q.set('water',String(waterLevel));q.set('rpm',String(rotationRPM));$('cp-simulation-viewer').href=document.querySelector('.cp').dataset.base+'werkstatt/?'+q;
}
$('cp-load-simulation').onclick=async()=>{const button=$('cp-load-simulation');button.disabled=true;$('cp-simulation-status').textContent='Bestehendes Funktionsmodell wird geladen …';try{const mod=await import('../workbench/calibration.mjs');cycle=mod.calibratedCycle;$('cp-simulation').hidden=false;update();$('cp-simulation-status').textContent='Simulation geladen · ausschließlich synthetische Parameter.';button.hidden=true;$('cp-phase').focus()}catch{$('cp-simulation-status').textContent='Simulation konnte nicht geladen werden. Systemplan und Feldaufnahme bleiben erreichbar.';button.disabled=false}};
for(const id of ['cp-phase','cp-level','cp-rpm'])$(id).addEventListener('change',update);
$('cp-phase').addEventListener('input',update);document.addEventListener('cp-context',update);
