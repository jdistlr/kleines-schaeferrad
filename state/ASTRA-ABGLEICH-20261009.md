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

Die neueren expliziten Nutzerkorrekturen ersetzen ältere Nutzerformulierungen und synthetische Modellannahmen. **PHOTO-6828/6829 (Schöpftrog) und PHOTO-6830 (Rinne 1) sind am 11.10.2026 ausdrücklich als exakt den heutigen Bauteilen entsprechend bestätigt:** lesbare Maße und Form sind maßgeblich; den [Zeichnungs-/Fotoabgleich](../evidence/raw/Auffangtrog/ZEICHNUNGSABGLEICH.md) lesen. Offene Maßlinienbezüge sind Ablese-/Referenzaufgaben, keine fehlende heutige Geltung. Andere historische Zeichnungsmaße und unabhängige Fotoablesungen behalten ihren jeweiligen Quellenstatus.

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
- **Krümmlingstöße:** beidseitige Schetternbretter; vier durchgesteckte Holznägel (**Schetternägel**, bestätigte Schreibweise mit tt), zwei je Einsteckrichtung, Gegenseite verkeilt. Zusätzlich bleibt laut [Fachauskunft vom 11.10.2026](../evidence/raw/Kruemmlinge/BEFUND.md#stoßspalt-keil-und-verspannung) an jedem Segmentstoß ein kleiner Spalt, der durch einen Stoßkeil geschlossen wird. Der Keil erzeugt laut Nutzer Druck auf die Schetternägel und verspannt den ganzen Kranz. Die Krümmlinghölzer allein bilden keinen vollständig geschlossenen Kranz. Stoßkeil, Nagelendkeile und Armsitzkeile getrennt behandeln; Spaltweite, Keilmaße und Einsteckrichtung bleiben offen. Vorhandene Maßbilder zuerst analysieren, keine lückenlose Holzsegmentfolge aus der nominellen 60°-Teilung ableiten.
- **Land-/Wasserseite der Krümmlinge:** [Nutzerbestätigter Befund vom 11.10.2026](../evidence/raw/Kruemmlinge/BEFUND.md): Landseitig jeweils zwei zusätzliche Bohrungen für die Kumpfbefestigung; wasserseitig keine Kumpfbohrungen, in dieser Gegenüberstellung nur Schetternbrett-Bohrungen. Zweierbezug nicht als Gesamtlochzahl des Segments interpretieren. Lochbilder getrennt behandeln und zusätzliche Kumpfbohrungen nicht spiegeln. Armsitz und Flügelband-Durchtritte separat auswerten.
- **Flügelbretter:** etwa 35 cm breit, 90° zur Kranzebene, landseitige Anschrägung. U-Holzband über **Flügelbrett**, durch **Krümmling**, hinten verkeilt. Keine Verbindung zum Schetternbrett erfinden.
- **Welle:** gleichmäßiger Holzquerschnitt statt Holzverjüngung; zwei Eisenschellen je Ende; mittiger Dorn läuft unmittelbar im Holz.
- **Kumpfnägel:** Ø4 cm Kopf/Ausgangsholz, Ø2,6 cm geschnitzter Schaft; längerer Nagel für krümmlingabgewandte Seite. Fotoablesung tatsächlicher Längen und Kopfgeometrie, keine Überstandslänge als Gesamtlänge.
- **Radstadt:** Bezeichnung der gesamten Tragkonstruktion. 65 cm Armabstand mit offenem Bezug. Bock am Rad und A-Bock an Rinne als getrennte Baugruppen. Neuere [Fachangabe vom 11.10.2026](../evidence/raw/Radstadt/BEFUND.md): Obere Radstadt-Balken für die spätere vereinfachte Konstruktion mit **40 cm Breite × 20 cm Höhe** ansetzen. Korrigierte Nutzerangabe zur lichten Rahmenöffnung: **4,40 m parallel zum Land/Ufer × 3,40 m vom Land zum Wasser**. **2,40 m ist ausdrücklich zurückgenommen; die gemessenen 4,40 m sind nun als möglicherweise vermessen zur Prüfung gestellt.** Den [Maßabgleich](../evidence/raw/Radstadt/MASSABGLEICH.md) vor der Konstruktion lesen; 5,25 m Zeichnungsmaßkette, Schaufelüberstand und Rahmenhöhe dagegen prüfen. Als Innenflächenabstände behandeln; äußere Rahmenmaße, Holzlängen und Wellenlage gesondert bestimmen. Reale Brettstärken und Balkenbreiten variieren wegen des Naturmaterials; 400 × 200 mm sind keine individuell gemessenen Ist-Querschnitte. Nicht auf die getrennt beschriebenen 14 × 14 cm des Bocks oder A-Bocks verallgemeinern.
- **Bock am Rad:** oberer Querbalken 1,20 m, Balken 14 × 14 cm, ausgeklinkte/verkeilte Verbindung, Symmetrie im richtigen Geltungsbereich.
- **Schöpftrog/Rinne/A-Bock:** [Nachtrag vom 11.10.2026](../evidence/raw/Auffangtrog/BEFUND.md): **landseitiger Lagerbock → Rinne → Schöpftrog** als Kontaktfolge. Trog mit 45°-Stirnseiten links/rechts und trapezförmigem 50/32-cm-Querschnitt aus Zeichnung; 30 cm Trogtiefe von 16 cm Auslasstiefe trennen. Zwei Rinnenteile **überlappen**; A-Bock genau unter dieser Zone mit Füßen auf dem Gelände. Beine 14 × 14 cm, Aussparung 5 cm, Riegel 4 × 14 × 90 cm, oben/unten verkeilt; **80 cm Boden → Unterseite Rinnenboden**. Aktueller Code enthält die Baugruppe, aber nur einen stumpfen 55-%-Übergang und eine aus der Rinne abgeleitete Bodenhöhe. [Rinnenbefund](../evidence/raw/Rinne/BEFUND.md) und [A-Bock-Befund](../evidence/raw/A-Bock/BEFUND.md) vor der Umsetzung lesen. Gelände/Radstadt anhand IMG20261010121434 und IMG20261010121620 prüfen. Plausible Rinnenrichtung/-position ist vom Nutzer freigegeben; die Kontakte bleiben einzuhalten. 12° in Rinne-1-Zeichnung ist ein Endschnitt, kein Gesamtgefälle und kein gemessener Beinwinkel. Während der aktuellen Informationssammlung keine neue Geometrie oder Renderings. Riegellänge nicht als lichte Auflagenspannweite verwenden.
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
