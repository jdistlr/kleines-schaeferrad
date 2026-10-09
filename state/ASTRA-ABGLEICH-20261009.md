# Nächster Astra-Abgleich — neue Fachinformationen vom 09.10.2026

Status: **EVIDENCE INTAKE READY FOR ASTRA COMPARISON**
Geprüfte Basis: `36ea5c01d57ee1c0017f99941034a76adbe4790e`.
Arbeitsbranch des Pakets: `work/fachbeitrag-astra-20261009` im Fork ThorstenHalsch/kleines-schaeferrad.
Dieses Paket ist eine neue Eingabe für den 3D-Abgleich; noch kein fertig korrigiertes 3D-Modell.

## Start

1. Repository mit diesem Paket verwenden (PR-Branch oder nach Merge main); Commit/Branch zu Beginn nennen.
2. [Fachbeitrag](../docs/FACHBEITRAG-KONSTRUKTION-20261009.md) komplett lesen.
3. [39 strukturierte Claims](../evidence/contributions/thorsten-20261009.json) und [Fotomanifest](../evidence/contributions/thorsten-20261009-photos.json) lesen.
4. Alle relevanten **Originalfotos visuell öffnen**, Maßstäbe vergrößern; Bilder nicht nur anhand des Dateinamens als ausgewertet behandeln.
5. Danach bestehende V3-Baseline, Evidenzautorität, Source-Reconciliation, Assembly-Graph, Knowledge-Gaps und ITER-001 Truth-Critic-Audit lesen.

Die neueren expliziten Nutzerkorrekturen ersetzen ältere Nutzerformulierungen und synthetische Modellannahmen. Historische Zeichnungsmaße und Fotoablesungen bleiben als solche kenntlich.

## Auftrag

Gleiche die aktuelle 3D-Konstruktion vollständig mit den neuen Informationen ab. Beginne mit dem Befund und der Evidenzzuordnung. Prüfe implementierte Geometrie, nicht nur Metadaten oder veraltete Skizzen.

Ausgangsdateien:
- `src/workbench/geometry.mjs`
- `src/workbench/calibration.mjs`
- `src/workbench/viewer.js`
- `data/hypothesis.parameters.json`
- `data/calibration-v3.json`
- `data/geometry.claims.json`, `components.json`, `assembly.graph.json`
- `data/conflicts.json`, `knowledge-gaps.json`, `source-analyses.json`
- `data/scan-transforms.json`, archivierte PLY/GLB
- `state/reconstruction-loop/ITER-001/truth-critic/AUDIT.md`
- `state/reconstruction-loop/PROTOCOL.md`

Supplemental Intake wird von bestehender Anwendung noch **nicht** automatisch gelesen. Reconciliation muss Claims, Quellen, Komponenten, Verbindungen, Konflikte und offene Aufgaben kontrolliert in die kanonischen Daten übernehmen; bestehende IDs und historische Werte nicht zerstören.

## Besonders entscheidende Prüfungen

- **Kranzabstand:** 1,80 m Innenflächen; 14 cm axial je Kranz → 1,94 m Mittelebenen, 2,08 m Außenflächen. Nicht blind `ringDistance=1.80` setzen, wenn der Code Ringmittelpunkte positioniert. Paddle-span, Welle, Armpositionen, Kumpfnägel, Trog und Kollisionsprüfungen folgen dieser Semantik.
- **Arme:** 14 × 6,5 cm, Orientierung im Querschnitt prüfen. Armsitz mittig im Krümmling, lokale Verstärkung, zwei Keile und zusätzlicher rückseitiger Sicherungsstift. Ein Phasenversatz von Segmenten muss zu realen Stößen und Schetternbrettern passen.
- **Krümmlingstöße:** beidseitige Schetternbretter; vier durchgesteckte Holznägel, zwei je Einsteckrichtung, Gegenseite verkeilt.
- **Flügelbretter:** etwa 35 cm breit, 90° zur Kranzebene, landseitige Anschrägung. U-Holzband über **Flügelbrett**, durch **Krümmling**, hinten verkeilt. Keine Verbindung zum Schetternbrett erfinden.
- **Welle:** gleichmäßiger Holzquerschnitt statt Holzverjüngung; zwei Eisenschellen je Ende; mittiger Dorn läuft unmittelbar im Holz.
- **Kumpfnägel:** Ø4 cm Kopf/Ausgangsholz, Ø2,6 cm geschnitzter Schaft; längerer Nagel für krümmlingabgewandte Seite. Fotoablesung tatsächlicher Längen und Kopfgeometrie, keine Überstandslänge als Gesamtlänge.
- **Radstadt:** Bezeichnung der gesamten Tragkonstruktion. 65 cm Armabstand mit offenem Bezug. Bock am Rad und A-Bock an Rinne als getrennte Baugruppen.
- **Bock am Rad:** oberer Querbalken 1,20 m, Balken 14 × 14 cm, ausgeklinkte/verkeilte Verbindung, Symmetrie im richtigen Geltungsbereich.
- **Rinne/A-Bock:** zwei Rinnenteile, Stoß auf A-Bock. Beine 14 × 14, Aussparung 5 cm breit, Riegel 4 × 14 × 90 cm, oben/unten verkeilt. Unterseite Rinnenboden 80 cm über lokalem Boden. Riegellänge nicht als lichte Auflagenspannweite verwenden.
- **Zeichnungen:** Trog 6828/6829, Rinne 6830; Kranzdetail 6848–6852 mit 426/396 und 213/198, 60°. Ø4,26 m ist bedingte cm-Interpretation der Kranzaußenkontur; Flügel-/Kumpfüberstände separat.
- **Scan:** Trog gezielt lokalisieren, alte wiedererkennbare Merkmale zuordnen, Maßstab/Achse/Seitenbezug registrieren. Keine `MECHANICALLY_REGISTERED`-Promotion ohne Korrespondenzen und Prüfstrecke.

## Fotoablesungen und A-Bock-Berechnung

Vor numerischer Übernahme dokumentieren: Foto, Pixel-/Rulerregion, Nullpunkt, Endpunkte, Bezugsebene, Einheiten und Unsicherheit. Länge am schrägen Bein nicht mit vertikaler Höhe verwechseln. Zahlen bei unzureichender Lesbarkeit offen lassen und den konkreten Grund nennen.

Für Fußabstand zuerst Riegelaufstand, Balkenachsrichtung, Position der Aussparung entlang des Beins, Überstände und Gelände bestimmen. Nur mit gesicherter Geometrie herleiten. 80 cm und volle Balkenlänge allein sind unzureichend.

Balkenlänge ist bereits fotografisch geliefert; neue Bilder erst anfragen, wenn die vorhandenen Maßstäbe nach Sichtprüfung tatsächlich nicht entscheiden.

## Erwartete Ergebnisse

Unter `state/reconstruction-loop/ITER-002/` als **Abgleich**, noch ohne pauschalen As-built-Status:
- `EVIDENCE-COMPARISON.md`: Baugruppe → neue Quelle → Ist-Code → Abweichung → konkrete Maßnahme.
- `CONSTRAINT-DELTA.json`: Property-genaue aktuelle, ungefähre, abgeleitete, historische und offene Werte.
- `PHOTO-READOUTS.json`: belastbare Ablesungen samt Unsicherheit und ausdrücklich erfolglose Ablesungen.
- `OPEN-QUESTIONS.md`: nur wirklich offene Fragen; angekündigte Ausbauvermessung getrennt.
- Technische Vergleichsansichten zu Kranz/Arm/Schetternbrett, Flügelbrett/Band, Welle/Lager, Kumpfnägeln und beiden Böcken.
- Umsetzungsreihenfolge und betroffene Parameter/Funktionen.

Falls Modellkorrekturen im anschließenden Arbeitsauftrag umgesetzt werden: erst kanonische Evidenz konsistent reconciliieren, danach Geometrie und alle abhängigen Kontakte/Abstände aktualisieren; technische Ansichten und angemessene Checks erneuern. Synthetische Kandidaten von belegten Verbindungen und metrischen Ist-Maßen trennen. Keine ungeprüfte automatische Änderung an Produktion/Hosting oder Merge.

Nicht auf sämtliche morgigen Maße warten, um den jetzigen **Abgleich** auszuführen. Belegte Topologie ist bereits ausreichend für konkrete Korrekturbefunde; verdeckte metrische Eigenschaften bleiben offen.

## Arbeitsunterlagen

- `output/pdf/KS-Werkstatt-Aufnahmeplan-A3.pdf`: 11 Blätter; KS-00,10/11,20,31,40,50,51 besonders relevant.
- `output/pdf/KS-Kurzplan-A4.pdf`
- `docs/SAMSTAG-ABBAU-AUFNAHMEPLAN.md`
- `state/reconstruction-loop/ITER-001/truth-critic/CAPTURE-PLAN.md`

Ältere noch offene Einträge zu Befestigungsprinzipien wurden teilweise beantwortet. Nach Reconciliation Frage-/Statuslisten und Skizzen entsprechend aktualisieren, nicht das ganze alte Fragenpaket erneut an Thorsten stellen.
