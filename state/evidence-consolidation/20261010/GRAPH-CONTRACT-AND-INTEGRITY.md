# Bestehender Graph und Referenzintegrität

Stand: 2026-10-10. Lesender Snapshot der Fachverträge auf `9c1bf563465b89e4aeded9935775efe0b17c3e26`. Spätere Berichtcommits verändern diese Fachverträge nicht. Reproduktion: `python state/evidence-consolidation/20261010/audit-evidence.py`. Vollständige Ergebnisse samt JSON-Pointern: `audit-results.json`. Kein neues Laufzeitmodell.

## Tatsächliche Verträge

| Bestand | Anzahl | Vertrag und Bedeutung |
|---|---:|---|
| Aussagen | 408 | `data/geometry.claims.json`: Aussage, Gegenstand, Wert, Einheit, Klasse, Geltung, Provenienz; nicht je eine physische Tatsache |
| Komponenten/Gegenstände | 34 | `data/components.json`: Familien/Regionen, keine vollständige Stückliste physischer Instanzen |
| Quellenanalysen | 117 | `data/source-analyses.json`; weitere Quellen liegen in Manifesten und Beiträgen |
| Quellen-IDs in geprüfter Registerunion | 159 | Einschließlich Kontext, externer Referenzen, Analyse-IDs und V2-Eingänge; nicht 159 unabhängige Belege |
| Montagetopologie | 30 Knoten / 31 Relationen | `data/assembly.graph.json`: mehrere Kanten mit ausdrücklich historischem Geltungsbereich |
| Historische/erwartete Plätze | 66 | `assembly.graph.instances`; keine bestätigte aktuelle Teileinventur |
| Registrierte physische Instanzen | 0 | `data/instance-register.json`; leeres Register beweist nicht das Fehlen realer Teile |
| Lücken / Aufgaben / Konflikte | 9 / 21 / 13 | Eigene bestehende Verträge, verschiedene Arbeits- und Fachzustände |

Die 2.887 im Prüfartefakt extrahierten Referenzen tragen Relationstyp, Quelldatei und JSON-Pointer. Es handelt sich um eine Auswertung vorhandener Verweise; kein neuer kanonischer Graph. Nicht jeder im Repository denkbare Freitextverweis ist damit erfasst.

## Welche Relationen was bedeuten

- `cites-source`: Aussage oder Bestandskante nennt eine Quelle. Das Vorhandensein des Verweises bestätigt nicht die Interpretation.
- `indexes-claim`: Komponenten-/Quellenregister bietet Navigation zu Aussagen. Diese Rückverweise sind kein zusätzlicher Beweis.
- `derived-from-claim`: ausdrücklich hinterlegte Ableitung, insbesondere TH-20261009-28/-29 aus -25/-26.
- `about-subject`, `about-component`: Zuordnung zu Gegenstand oder Referenzobjekt; keine Maßevidenz.
- `model-map-cites`: bestehende Modellzuordnung nennt eine Quelle/Aussage; keine umgekehrte Bestätigung durch das Modell.
- `investigates-gap`, `captures-component`, `tracks-conflict`, `requires-capture`: Arbeitsbeziehungen; keine erledigte Feldaufnahme.
- Montagekanten übernehmen den vorhandenen `type`, z.B. `region_of`. Ihr Geltungsbereich und die Originalprovenienz stehen in `data/assembly.graph.json`.

## Maschineller Befund und nachgeprüfte Einordnung

Keine doppelten IDs innerhalb der geprüften Claim-, Komponenten-, Quellenanalyse- und Aufgabenlisten. Alle 408 Claims haben Provenienz; alle 31 Montagekanten haben Provenienz. Sämtliche `components[].claim_ids` sind auflösbar. Die zuvor gemeldeten 20 Claim-Quellenverweise außerhalb von `source-analyses` lösen sich in der erweiterten Quellenunion auf: kein Nachweis von 20 fehlenden Quellen.

Der strenge Registervergleich meldet 16 Kandidaten. Nach lesender Auflösung verbleiben **sechs nicht exakt passende Quellverweise auf drei unterschiedliche IDs**:

| Verweis | Belegstelle | Befund / zulässige nächste Aktion |
|---|---|---|
| `PHOTO-6822`, `PHOTO-6832` | `data/components.json`, COMP-KUMPF-NAILS, `/components/14/provenance/0..1` | Diese IDs sind nicht in den geprüften Quellenregistern definiert. Originalbytes sind unter `V2-IMG_6822`, `V2-IMG_6832` nachgewiesen; Transferzuordnung per SHA-256 bestätigt. Nach Freigabe Referenz auf bestehende IDs prüfen; keine neue Quelle erzeugen. |
| `V2-IMG_6808` (vier Verweise) | `data/reconstruction-evidence-map.json`, COMP-SHAFT, COMP-ARMS, COMP-FASTENERS, COMP-BEARINGS | Vorhandenes Register heißt `V2-IMG_6808-upload2`; passende Bildbytes sind archiviert. Alias-/Referenzkorrektur vorschlagen, keine Geometrie ändern. |
| `H-ARM-01..04` (acht Verweise) | `data/field-tasks.json` | In `docs/ARM-SHAFT-HYPOTHESES.md` als Überschriften definiert. Dokumentarische Hypothesen, keine fehlenden Fotoquellen. |
| `REF-Welle`, `CAPTURE-01` (zwei Verweise) | `data/conflicts.json`, CONFLICT-03/-10 | Typfremd gegenüber reinen COMP-IDs, semantisch vorhandenes Empfehlungsobjekt bzw. Scan-Aufnahmegruppe. Kein automatisch fehlendes Bauteil. |

`HUMAN-01..05` sind in `docs/HUMAN-CALIBRATION.md` dokumentierte Fragen. Der Prüfer akzeptiert HUMAN-Verweise als gesonderten Dokumentnamensraum; dies ist im Skript explizit, kein stillschweigender Beweisstatus.

## Bedeutungsprobleme, die nicht mit Löschung gelöst werden dürfen

1. **Quellen-ID mit zwei URLs:** `EXT-VZO` verweist in `evidence/manifest.json` auf `wasserrad.html`, in `data/external-construction-research-v2.json` auf `info.html`. Historische Abrufpfade und gespeicherte Aussagen vor späterer Korrektur abgleichen. Keine erneute Webrecherche in dieser ausschließlich repositorybezogenen Prüfung; externe Webseiten nicht als frisch überprüft ausgeben.
2. **24 semantische Doppelungskandidaten:** gleiche Kombination aus Gegenstand, Prädikat, Wert, Einheit und Geltung, etwa CLAIM-0263/-0268. Unterschiedliche Provenienzen und Bildperspektiven sind erhalten. Die Vergleichsregel ist nur ein Gruppierungshinweis; keine automatischen Zusammenführungen. Vollständige Liste in `semantic_duplicate_candidates`.
3. **29 Gegenstandsbezeichner außerhalb COMP:** überwiegend REF-, Scan-, Projekt-/Aufnahmebezüge. Sie erfordern eine typisierte Darstellung; nicht pauschal fehlende Komponenten melden.
4. **Elf `measured`-Claims:** CLAIM-0307..0310, -0314..0320 betreffen Vertexzahlen, digitale Ausdehnungen, Topologie und ähnliche Scanmerkmale, alle `scope:digital-artifact-only`, `as_built_eligible:false`. Keine verifizierten Bestandsabmessungen daraus ableiten.
5. **Konfliktregister ist heterogen:** CONFLICT-04 ist bereits `semantic-dimensions-resolved`; -08 ist ein Aufnahmeverlust; -09 ohne Registrierung nicht vergleichbar; -13 hat geklärten Ebenenbezug bei offenem Pitch. Eine pauschale rote „13 Widersprüche“-Anzeige wäre sachlich falsch. Historische `unresolved_conflict`-Claimtexte wie CLAIM-0347 müssen mit dem späteren Konfliktstatus zusammen lesbar sein; hier keine Änderung.
6. **GAP-09 hat keine direkte Aufgabenverknüpfung:** TASK-PAD ist inhaltlich einschlägig, nennt aber andere GAP-IDs. Bestehende Aufgabe nach Freigabe zuordnen, nicht ein zweites Schaufelprojekt anlegen. Alle 21 Aufgaben haben bereits mindestens eine andere GAP-Verknüpfung.
7. **16 Transferdateien ohne exakten Register-Hash-Treffer:** neue Bytevarianten bzw. neues Video, nicht automatisch neue unabhängige Quellen. Sichtbare Blatt-/Ansichtsähnlichkeiten stehen in SOURCE-INVENTORY; keine neuen kanonischen IDs angelegt.

## Zirkelschlüsse und Modellgrenzen

Im expliziten gerichteten Claim-Provenienz-/Ableitungsgraphen findet der lesende Prüfer keinen Zyklus. Die wechselseitigen Claim-/Quellen-Indizes wurden zu Recht nicht als Beweiszyklen gezählt. Dies schließt versteckte inhaltliche Zirkelschlüsse in Freitext oder ungeprüften Implementierungsdetails nicht aus.

Konkretes Risiko: TH-20261009-25/-26 → abgeleitete 1,94/2,08 m → Modellparameter → gerendertes Bild darf nicht zurück als unabhängiger Maßbeleg dienen. Ebenso bleiben PLY und GLB Ableitungen derselben Aufnahmegruppe CAPTURE-01; zwei Formate sind keine zwei unabhängigen Messungen. Videozeitpunkte verweisen auf ein einziges Video.

`src/control/property-readiness.mjs` bildet nur fünf TH-Maßangaben auf Parameter ab. Weitere Zuordnungen existieren in `src/workbench/expert-corrections.mjs` und `calibration.mjs`. Ein leeres Adapterfeld beweist deshalb keine fehlende Modellumsetzung. `geometry.mjs` erzeugt zunächst Kandidaten und ruft anschließend `calibrateModel` und `applyExpertCorrections` auf. Frühere Erzeugungsschritte isoliert zu lesen würde den Endzustand falsch beurteilen. Hier erfolgte nur Codelektüre, keine neue Mesh-/Browservalidierung.

## Ergebnis

Der vorhandene Graph ist nachvollziehbar auswertbar. Die prioritären Probleme sind Identitätsverweise, Quellenabhängigkeit, Statusdarstellung und fehlende eigenschaftsbezogene Freigaben. Alle vorgeschlagenen Korrekturen bleiben Vorschläge; kanonische Daten und die 39 Thorsten-Fachkorrekturen wurden nicht verändert.
