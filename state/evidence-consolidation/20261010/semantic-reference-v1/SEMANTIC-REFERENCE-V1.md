# Semantische Referenzbasis v1 — Reviewfassung

Stand 10.10.2026, fortgeführt ab PR #20 / `727a0248c0234641453a08e4ae3984e27c9f970b`. Diese Referenzbasis erläutert und prüft die bestehenden Verträge. Sie ersetzt weder `data/` noch die Originalquellen durch eine zweite Ontologie. Fachliche Abnahme steht aus.

**SEMANTIC REFERENCE V1 — REVIEW READY, mit ausdrücklich offener Audioauswertung und Objektidentität der Kontextbilder.** Dies ist kein uneingeschränkter Abschluss aller Quellenprüfungen und keine Zeichnungs-/Fertigungsfreigabe.

## Einstieg und Ergebnis

- [Quellensichtung](SOURCE-SIGHTING.md): alle 76 Transferfotos einzeln, Video zeitlich vollständig in Frameübersichten und 43 größeren Stichproben, drei nicht identifizierte Kontextbilder, sechs gezielte Referenzoriginale. Hash-/ID-Zuordnung in `source-sighting.json`. Tonspur inhaltlich ungeprüft.
- [Drei Referenzfälle](REFERENCE-CASES.md): Originalstelle → Aussage → Geltung → Modellannahme → offene Lücke → bestehender Untersuchungsauftrag. `reference-cases.json` enthält Prüfbeispiele mit bestehenden IDs, keine neuen Fachobjekte.
- [Korrekturen und Restbefunde](CORRECTIONS-AND-LIMITS.md): sechs Quellenverweise repariert; vorhandene TASK-PAD mit GAP-09 verknüpft; Kontextregel berichtigt. Keine Maß-, Status- oder Geometrieänderung.
- `verify-reference-v1.py` prüft Referenzen, Schutzgrenzen, alle 39 Fachkorrekturen, Klassen/Geltung der Beispiele und die unveränderten Originale. `validation.json` und die Prüfprotokolle dokumentieren den Lauf. Der Prüfer bewertet keine fachliche Wahrheit und ersetzt kein visuelles Review.

## Wo die bestehende Bedeutung festgelegt ist

| Frage | Maßgeblicher Bestand | Leseregel |
|---|---|---|
| Was ist die Quelle? | `evidence/manifest.json`, `evidence/additions-v2.json`, `evidence/contributions/*`, Transfer-Prüfsummen | Datei/Hash, Quellen-ID, Blatt/Aufnahmegruppe und abgebildetes Objekt sind verschiedene Identitäten. |
| Was wurde daraus abgelesen? | `data/source-analyses.json`, `data/geometry.claims.json` | Claim samt `provenance.region`, `evidence_class`, `scope`, `unit`, `as_built_eligible` lesen. Hohe Lesesicherheit ist keine aktuelle Maßsicherheit. |
| Worüber wird gesprochen? | `data/components.json` | `kind` unterscheidet Teilfamilie, Region und Referenzobjekt. Ein Gruppenlabel ersetzt keine reale Teil-ID. |
| Welches konkrete Teil? | `data/instance-register.json` | Register ist noch leer; reale IDs erst nach Beobachtung/Markierung. Historische Slots aus `assembly.graph.instances` sind keine 66 vermessenen Teile. |
| Welche Verbindung? | `data/assembly.graph.json` | Relationen samt Herkunft/Geltung lesen; historische Topologie nicht automatisch aktueller Ist-Zustand. |
| Welche Aussage hat Vorrang? | `data/evidence-authority.json` | Vorrang gilt innerhalb passender Eigenschaft und Geltung. Fachauskunft kann Bauweise klären, ersetzt aber keine aktuelle metrische Aufnahme. |
| Was ist Modell? | `data/reconstruction-constraints.json`, `data/hypothesis.parameters.json`, `data/calibration-v3.json`, `src/workbench/*` | Eingaben und Umsetzung belegen Modellverhalten; niemals rückwärts als Beweis der Realität verwenden. |
| Was fehlt, wie wird es geklärt? | `data/knowledge-gaps.json`, `data/field-tasks.json`, `data/conflicts.json` | Lücke, Widerspruch, verlorene Aufnahme und unklare Identität getrennt lesen. Zugeordneter Auftrag ist keine erledigte Aufnahme. |
| Welcher räumliche Bezug? | `data/reference-system.json` | Axial entlang der Welle, radial zur Achse. Seitenvorzeichen und Feldregistrierung noch nicht bestätigt. |

## Begriffe ohne neue IDs

| Begriff | Bestehender Anker | Abgrenzung |
|---|---|---|
| Welle / Achse | COMP-SHAFT | Physischer Holzkörper; Dorn, Schellen und Lagerkontakt getrennt betrachten. |
| Armzone / vermeintliche Nabe | COMP-HUB-LAND, COMP-HUB-WATER | Regionen der Welle, kein dadurch nachgewiesenes separates Nabenbauteil. |
| Arm / Speichenende | COMP-ARMS | Durchgehendes Armholz und sichtbares radiales Ende nicht gleichzählen. Historische Paarung nicht auf verdeckte aktuelle Enden übertragen. |
| Kranz / Krümmling | COMP-RIMS, COMP-RIM-LAND, COMP-RIM-WATER / COMP-KRUEMMLINGE | Gesamtanordnung, benannte Ringseite und einzelnes Segment sind verschiedene Betrachtungsebenen. |
| Schetternbrett | COMP-SCHETTERNBRETTER | Fachlich berichteter Verbinder am Segmentstoß; Armsitz laut TH-01 in Segmentmitte. |
| Kumpf / Schöpfgefäß | COMP-KUEMPFE | Teilfamilie; Referenzgefäß, historische Variante und konkreter eingebauter Kumpf getrennt. |
| Daube, Boden, Spannring | COMP-KUMPF-STAVES, COMP-KUMPF-BASE, COMP-KUMPF-HOOPS | Bauteile des Gefäßes, keine Synonyme für den gesamten Kumpf. |
| Kumpfnagel / Lang-Kurz-Paar | COMP-KUMPF-NAILS | Funktion durch lokale Fachauskunft; konkrete Wege durch Nachbarkümpfe weiterhin aufzunehmen. Nicht mit Wehrnadeln gleichsetzen. |
| Flügelbrett / Schaufel | COMP-PADDLES | 90° zur Kranzebene ist geklärter Ebenenbezug; radialer Pitch und Kontaktgeometrie bleiben GAP-09. |
| U-Holzband / Spannring | COMP-WOOD-BANDS / COMP-KUMPF-HOOPS | Unterschiedliche Funktion und Partner; trotz Wort „Band“ nicht verschmelzen. |
| Radstatt / Radstadt | COMP-RADSTATT / COMP-RADSTADT | Lokale Namenskorrektur TH-19 erhalten. Beide vorhandenen Einträge bleiben bestehen; daraus weder zwei physische Tragwerke noch eine automatische ID-Fusion ableiten. |
| Biegematrize / Kontaktstreifen / Brettvorlage | TOOL-BENDING-DIE / REF-CONTACTSTRIPS / REF-BOARD | Werkzeug und Referenzunterlagen sind nicht allein durch Ablage in der Mappe verbaute Radteile. |

Dies ist ein Leseverzeichnis, keine neue Aliasauflösung im Produkt. Ähnliche Wörter, Werte oder Fotos reichen nicht zur Gleichsetzung von Objekten oder Instanzen.

## Evidenzregeln für jeden Referenzfall

1. **Erst Identität und Geltung, dann Stützung:** Welches Blatt, welche Aufnahme, welches Objekt, welcher Zustand und welche Eigenschaft? IMG_6875–6877 bleiben Vergleichsmaterial ohne bestätigten Zielbezug. Ähnliche Umgebung, Dateinummer oder Suchanfrage ersetzen keinen Identitätsbeleg.
2. **Quelle → Claim ist Interpretation mit Ort:** Auflösbare `source_id` beweist den Zugang zur Quelle. Sie bestätigt nicht automatisch den Wert oder die Interpretation. Mehrere Fotos desselben Blattes erhöhen Lesbarkeit, nicht die Zahl unabhängiger Maßquellen.
3. **Eigenschaft statt Bauteil-Wahrheitsstempel:** Die Existenz der Welle, ihre berichtete Bauweise und ein unbekanntes Innenmaß dürfen gleichzeitig unterschiedlich gut belegt sein. Vorhandene pauschale `confidence`-Labels sind keine Freigabe für alle Eigenschaften.
4. **Historische Zeichnung / Empfehlung / Ist-Maß:** `documented-design` ist dokumentierter Entwurf; eine Empfehlung bleibt Empfehlung; `digital-artifact-only` betrifft Scan-/Dateieigenschaften. Keine dieser Klassen wird hier zu einem heutigen Feldmaß.
5. **Fachauskunft / Ableitung:** TH-25/-26 bleiben berichtete Werte; TH-28/-29 bleiben davon abhängige Ableitungen. Die übernommene semantische Transkription ist keine wörtliche Audioaufnahme. Eine Rechenprüfung bestätigt die Formel, nicht die Messgrundlage.
6. **Modell und Evidenz strikt gerichtet:** Original → Beobachtung/Fachauskunft → Claim → Modell ist nachvollziehbar. Modell → Originalmaß ist kein unabhängiger Rückbeweis. Navigationsrückverweise sind keine zusätzlichen Belege.
7. **Konflikt ist nicht jede offene Frage:** CLAIM-0347 bleibt historisch erhalten, CONFLICT-04 dokumentiert die spätere axiale/radiale Auflösung. Aufnahmeverlust, fehlende Registrierung und offener Pitch behalten ihre eigenen Zustände; keine pauschale Zahl „13 Widersprüche“.
8. **Teilklärung schließt keine Gesamt-GAP:** Zugeordnete Feldaufgaben und Akzeptanznachweise bleiben erforderlich. Neun Lücken, 21 Aufgaben und deren Status bleiben erhalten. Fehlender Beleg ist weder Widerlegung noch stillschweigende Bestätigung.

Diese Regeln konkretisieren bestehende Verträge und das frühere Reviewpaket; keine neue Evidenzklasse, kein Score und keine zweite Statusmaschine wurden eingeführt.

## Was v1 als Referenz leisten kann

Ein fachlicher Reviewer kann für die drei Fälle auf Original, Claim-ID, Geltung, abhängige Ableitungen, Umsetzung und konkrete Nachforderung zeigen. Technische Integrationen können die mitgelieferten positiven und negativen Prüfbeispiele verwenden. Die Reviewfassung liefert damit eine überprüfbare semantische Ausgangsbasis, keine vollständige physische Ground Truth des Rades.

Vor einer späteren technischen Zeichnung fehlen je nach Eigenschaft weiterhin reale Teilidentität, Messendpunkte, Einheit, Werkzeug/Unsicherheit, Bezugssystem, Partnerflächen und fachliche Abnahme. Auch die Tonspur bleibt eine tatsächlich offene Sichtungsarbeit. Nach diesem Paket keine Arbeit im Hintergrund, kein Merge, kein Deployment.
