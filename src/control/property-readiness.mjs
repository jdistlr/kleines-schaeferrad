import constraints from '../../data/reconstruction-constraints.json' with {type:'json'};
// Read-only, explicitly bounded mapping to existing model inputs, not mesh verification.
const inputMap={
 'TH-20261009-25':['rings.clearInner','Lichter Abstand der inneren Kranzflächen',constraints.rings.clearInner],
 'TH-20261009-26':['rings.axialWidth','Axiale Krümmlingsbreite',constraints.rings.axialWidth],
 'TH-20261009-27':['arms.section','Armquerschnitt',constraints.arms.section],
 'TH-20261009-28':['rings.midplane','Abstand der Kranzmittelebenen',constraints.rings.midplane],
 'TH-20261009-29':['rings.outerWidth','Breite über äußere Kranzflächen',constraints.rings.outerWidth]
};
export function propertyReadiness(claim){
 const mapped=inputMap[claim.id];
 return {id:claim.id,label:mapped?.[1]||claim.predicate,sourceValue:claim.value,unit:claim.unit,sourceClass:claim.evidence_class,metricStatus:claim.metric_status||'Geltungsbereich und Messverfahren an der Quelle prüfen',modelPath:mapped?.[0]||null,modelValue:mapped?.[2]??null,agreement:mapped?JSON.stringify(claim.value)===JSON.stringify(mapped[2]):null,release:'Keine automatische Zeichnungs- oder Fertigungsfreigabe',missing:claim.remaining_unknown||'Teilinstanz, Messendpunkte, Werkzeug/Genauigkeit und unabhängigen eigenschaftsbezogenen Review nachweisen.'};
}
