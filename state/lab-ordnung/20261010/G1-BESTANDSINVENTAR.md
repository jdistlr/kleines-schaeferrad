# G1 – Gezieltes, lesendes Bestandsinventar (Beginn)

Stand 2026-10-10. Branch `design/lab-ordnung-entwurf-20261010`, Basis PR #18 `c31bf8ae5cdc9d79090c1b53bfea1c867f255eb7`. Keine Datenänderung.

## Geprüfte Verträge und Beziehungen

| Bestehender Vertrag | Tatsächlich vorhandene Information | Grenze für das Board |
|---|---|---|
| `data/components.json` | Gegenstand-IDs, Typen, Claim-Verweise, Herkunft | `confidence` auf Komponenten nicht als Bauteilwahrheit verwenden |
| `data/geometry.claims.json` | Einzelbehauptungen mit `id`, `subject`, `predicate`, `value`, `unit`, `scope`, `provenance` | historische Angaben nicht zu Ist-Maßen befördern |
| `data/source-analyses.json` | Originalquellen-IDs, Einzelanalysen, Grenzen, Claim-Verweise | zwei Fotos eines Blatts sind keine unabhängigen Beweise |
| `data/knowledge-gaps.json` | `GAP-01` bis mindestens `GAP-06`, Verlustfenster, konkrete Aufnahme- und Nachweisanforderungen, Konflikt-IDs | Lücke ist nicht automatisch Widerspruch |
| `data/field-tasks.json` | bestehende Aufgaben, Endpunkte, Werkzeuge, Fotos, Zeitfenster und Status | lokale Aufnahmen nicht anfassen |
| `data/reconstruction-constraints.json` | `ITER-003`-Modellparameter und je Bereich Kandidaten-/Geltungsgrenzen, `asBuilt:false` | Parameterübernahme ist kein Geometrie- oder Fertigungsnachweis |
| `src/control/property-readiness.mjs` | fünf explizite Zuordnungen TH-25…29 | fehlende Zuordnung ist nicht gleich fehlende Geometrie |

## Konkrete Querverbindungen

- `COMP-SHAFT` → `CLAIM-0001` (historische Maßzahl 370, ohne gesicherte Einheit) → `PHOTO-6816` und `PHOTO-6817` (zwei Aufnahmen desselben Blatts) → `data/reconstruction-constraints.json:shaft` (modellierte Welle, jedoch Kandidatenparameter) → keine direkte Zuordnung dieser historischen Claim-ID im begrenzten `property-readiness`-Adapter.
- `GAP-02`: Arm-/Keil-/Mortisen- und Orientierungsbeziehungen; `CONFLICT-05`, `CONFLICT-06`; der erforderliche Nachweis ist eine Aufnahme der realen Kontakt-/Einsteckflächen beim Lösen.
- `GAP-04`: Kumpf-Nut und Kumpfnagelwege; bekannte Fachkonstruktion ausdrücklich bewahren, unbekannte exakte Wege und Lochpositionen nicht erfinden.
- `TASK-ORIENT`: Vor dem Lösen Blickseiten dokumentieren, Status OPEN; `TASK-DATUM`: Referenzen mit Einheiten, Endpunkten, Werkzeug und Unsicherheit; `TASK-POSE`: Ringebenen und Achslage vor dem Lösen.
- `reconstruction-constraints.json`: `rings.clearInner=1.8` ist eine Expertenangabe im Modellvertrag, `rings.seatTangentialClearance=0.002` eine Modellkandidatenannahme; beide dürfen nicht denselben Nachweisstatus erhalten.

## G1-Risiken und nicht behauptete Ergebnisse

- Ein vollständiger automatisierter Integritäts-/Referenzcheck aller JSON-IDs und sämtlicher Originaldatei-Hashes wurde **noch nicht** durchgeführt.
- Der genaue aktuelle Remote-HEAD von PR #18 und main muss vor einem späteren Umsetzungsauftrag erneut abgefragt werden; der Entwurfsbranch ist ausdrücklich an den bekannten dokumentierten PR-18-Commit gebunden.
- Repositoryweite Anweisungen in Unterverzeichnissen sind noch nicht vollständig geprüft.
- Kein vollständiger Beleg-zu-Modell-Mapping-Nachweis; nur gezielte Beispiele verifiziert.
- Kein fachliches GO und keine fertige G2/G3/G4-Abnahme.

## Nächster begrenzter Schritt

G1 vervollständigen: Referenzintegrität, Quelltypen, Abhängigkeiten, Modellmapping und tatsächliche Originalzugänglichkeit für **einen** ausgewählten Fall prüfen. Anschließend G2 Fallakte und G3 zusammenhängende Desktop-/Smartphone-Entwürfe, erst dann Reviewgate G4. Keine produktiven Änderungen.
