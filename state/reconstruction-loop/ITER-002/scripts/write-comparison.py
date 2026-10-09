"""Materialize the manually reviewed comparison; never writes canonical data."""
import json
from pathlib import Path
O=Path('state/reconstruction-loop/ITER-002')
intake=json.load(open('evidence/contributions/thorsten-20261009.json'))
def save(n,x): (O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
# status, runtime value, finding/visual assessment, proposed action, source-code anchor
rows=[
('abweichend',False,'Armenden bei 0°+60°k; Segmentmitten bei 30°+60°k. Arme sitzen an Segmentstößen. Nahfotos zeigen Durchsteckung; die vollständige Segmentmitte ist zusätzlich Fachangabe.','Relative Phase um 30° korrigieren; reale Stoßlagen und Armenden gemeinsam prüfen.','geometry.mjs: makeModel, Arm-/Sektorschleifen'),
('fehlend',False,'ringSector hat konstanten Innen-/Außenradius; Fotos zeigen örtlich verbreiterten Sitz.','Lokale Sitzkontur separat parametrisieren; Ausdehnung/Tiefe noch offen.','geometry.mjs: ringSector'),
('fehlend',{'rim_seat_wedges':0,'rear_pin':0},'Vorhandene CAND-WEDGE liegen am Zentrum bei Radius 0,21 m, nicht am Kranz. Fotos zeigen seitliche Keile und Querstift.','Zwei Sitzkeile und rückseitigen Armstift als eigene Kontakte anlegen.','geometry.mjs: CAND-WEDGE'),
('fehlend',0,'Keine Schetternbretter. Nackte Sektoren mit synthetischen Endbohrungen/Stiften ersetzen keine beidseitigen Stoßbretter. Fotos zeigen Bretter in Gegenansichten.','Paar je Stoß mit eigener Kontur und Quelle anlegen; keine direkte Endverbindung behaupten.','geometry.mjs: ringSector, CAND-RIM-PIN'),
('abweichend',{'pins_per_joint':2,'alternating_insertion':False,'wedges':False},'Zwei kurze axial gleiche Stifte je Stoß statt vier durchgesteckter Nägel. Köpfe und verkeilte Enden in Fotos; genaue Lochkoordinaten noch verdeckt.','Vier Nägel, zwei je Richtung, rückseitige Keile und durchgehende Kontakte planen.','geometry.mjs: CAND-RIM-PIN'),
('teilweise-konsistent',90,'Aktive Brettfläche enthält Wellenachse X und radiale Richtung; ihre Ebene steht 90° zur Kranzebene YZ. Radialpitch 0° bleibt Kandidat und wird durch 90° nicht bewiesen.','Ebenenbeziehung bewahren; Pitch separat bestimmen.','calibration.mjs: calibrateModel, Paddle plane'),
('fehlend',False,'Aktiver Quader ohne Abschrägung. Foto 1278244 zeigt Schräge nahe Kumpf; Kumpf als Kollisionspartner plausibel, noch nicht eindeutig belegt.','Landseitige Kontur erfassen, Partner bestätigen, Swept-volume-Prüfung planen.','calibration.mjs: BoxGeometry'),
('abweichend',0.43,'Brettbreite im Modell als paddleHeight 0,43 m; Fachangabe etwa 0,35 m. Differenz etwa 0,08 m, keine exakte Ist-Toleranz.','Breite ungefähr 0,35 m hinterlegen; Gesamtlänge/Dicke getrennt halten.','calibration.mjs: c.paddleHeight'),
('fehlend',None,'Kein Holzband. U-Form fotografisch sichtbar; Eiche, Spalten und Kochen nur Fachangabe.','Werkstoff/Herstellung als Fachwissen, U-Topologie als Verbindung aufnehmen.','geometry.mjs/calibration.mjs: keine Bandbaugruppe'),
('fehlend',None,'4–5 cm bezeichnet Ast vor Spaltung, nicht fertigen runden Bandquerschnitt.','Rohmaterialbereich erhalten; gespaltenen Querschnitt nicht als Vollrund modellieren.','keine Bandbaugruppe'),
('offener-bezug',None,'Etwa 1,20 m: abgewickelte Länge oder gebogenes Maß nicht ausdrücklich definiert; kein geeigneter Maßstab am gesamten Band.','Längenbezug klären, bis dahin kein 1,20-m-U-Schenkel erfinden.','keine Bandbaugruppe'),
('fehlend',None,'Fotos zeigen U über Flügelbrett, Beine durch Krümmling, rückseitige Sicherung. Ältere Schettern-Zuordnung ist ersetzt.','Verbindung Flügelbrett–Band–Krümmling mit hinteren Keilen anlegen.','keine Bandbaugruppe'),
('abweichend',False,'Holzwelle verjüngt sich auf Radius 0,075 m an beiden Enden. Fotos zeigen kräftiges Holz bis zum Stirnende und separaten Dorn.','Holzkörper ohne synthetische Schulterverjüngung; genaue Außenkontur/Querschnitt noch bestimmen.','geometry.mjs: HYP-SHAFT/latheX'),
('fehlend',0,'Keine Wellenschellen. Fotos eines Endes zeigen zwei axial getrennte eiserne Schellen. Gesamtzahl vier ist Fachangabe, kein aus einem Foto verdoppelter Messbefund.','Zwei Schellen je Ende; Breiten, Abstand, Schrauben und Sitz separat erfassen.','geometry.mjs: HYP-SHAFT'),
('abweichend',{'metal_journals':2,'metal_bearing_candidates':2},'Dornkandidaten vorhanden, aber U-Lager als Metall statt unmittelbarer Holzauflage. Foto zeigt Dorn zwischen Holzflächen; Inneres der Welle bleibt unsichtbar.','Holzlagerkontakt und separaten Dorn definieren; keine durchgehende Metallachse behaupten.','geometry.mjs: CAND-JOURNAL, HYP-BEARING'),
('teilweise-konsistent',{'long_chord_m':0.7263529495,'short_chord_m':0.5948792239},'Aktive V3-Nägel ungleich lang, aber aus Kandidatpose und fixem exitX=-0,495 abgeleitet. Zuordnung krümmlingabgewandt nicht als beobachteter Kontakt gesichert. Fotos loser Nägel nur bedingt metrisch auswertbar.','Lang/kurz nach realer Kumpf-Kranz-Seite zuordnen; Länge entlang Kurve, Sehne und Überstand trennen.','calibration.mjs: referenceKumpf, pinGeometry'),
('abweichend',0.048,'Zylindrisch polygonaler Modellkopf Ø48 mm; Fachangabe Ausgangsholz/Kopf etwa Ø40 mm. Fotos zeigen Rinde und unregelmäßige Stirnform.','40-mm-Ausgangsholz berücksichtigen; Kopfhöhe separat aus Foto PR-04 behandeln.','calibration.mjs: CylinderGeometry(.024,.024,.025,8)'),
('abweichend',0.018,'Modellschaft Ø18 mm; Fachmaß Ø26 mm. Foto PR-05 mit 24–29 mm vereinbar. Referenzloch Ø24 mm ist kleiner als neuer Schaft.','Schaft und Loch-/Spielbezug gemeinsam prüfen, nicht Ø26 in Ø24 erzwingen.','calibration.mjs: pinGeometry; calibration-v3.json: holeRadius'),
('semantik',None,'Radstadt bezeichnet gesamtes Tragwerk. Runtime hat FRAME/Bearing/Trough-Familien, keine eindeutige begriffliche Gruppierung.','Oberbegriff Radstadt mit Unterbaugruppen; keine neue Einzelstrebe Radstadt nennen.','geometry.mjs: stationary topology'),
('offener-bezug',None,'Etwa 0,65 m Armabstand zur Radstadt ohne benannte Flächen, Armphase oder Richtung. Kein eindeutiges Ist-Maß ableitbar.','Endpunkte und Stellung bestimmen, dann Abstand aus Weltgeometrie prüfen.','geometry.mjs: Arm-Layer und CTX-*'),
('abweichend',None,'Kein eindeutig entsprechender oberer 1,20-m-Bockquerbalken. CTX-BEARING-STAND ist 0,84 m lang, aber Lagerunterlage, nicht identischer oberer Balken.','Radbock als eigene Baugruppe mit oberem Querbalken 1,20 m aufbauen.','geometry.mjs: CTX-BEARING-STAND, CTX-RAIL'),
('abweichend',{'posts_m':0.23,'rails_m':0.24,'braces_m':0.16},'Synthetischer Rahmen verwendet andere Querschnitte; lokale Trogstützen 0,14 m sind kein Nachweis des Radbocks.','14×14 cm nur am beschriebenen Bock anwenden.','geometry.mjs: CTX-POST/RAIL/BRACE'),
('fehlend',False,'Rahmenbalken ohne Ausklinkung/Schlitz/Keil. Fotos 2327774/2342950 zeigen oberen Anschluss und herausstehenden Keil.','Ausgeklinkte Stütze, Querbalkenaussparung und Holzkeil als Kontakte anlegen.','geometry.mjs: beam/CTX-*'),
('offener-geltungsbereich',None,'Synthetischer Rahmen wird teils um X/Y gespiegelt. Fotos und Fachkontext betreffen Bock, nicht das gesamte asymmetrische Trog-/Kumpfsystem.','Lokale Bockachse definieren; keine globale Spiegelregel.','geometry.mjs: sx/sy-Schleifen'),
('abweichend',1.01,'Aus tatsächlichen Kranzgrenzen gemessen: 1,00999999 m lichte Weite. Neue Fachkorrektur 1,80 m.','Innenflächenabstand als führende Größe; Mittelebenen 1,94 m ableiten.','geometry.mjs: x=sign*p.ringDistance/2; runtime-audit.rims'),
('konsistent',0.14,'Aktive axiale Kranzbreite bereits 0,14 m. Korrektur ersetzt frühere axiale 0,15 m, nicht historische radiale Tiefe 2,13−1,98=0,15 m.','0,14 m bewahren; historische axiale Falschangabe mit Supersedes-Beziehung dokumentieren.','geometry.mjs: ringSector(depth=p.rimWidth)'),
('abweichend',{'axial_main_m':0.14,'tangential_depth_m':0.12,'axial_tip_m':0.063},'Armcode hardcodiert w=.14 und Extrusion .12; tip=.45*w. JSON armWidth/armDepth steuern diesen Code nicht. Zuordnung der neuen 14×6,5 cm zu Achsen noch offen.','Querschnittsachsen klären; hardcodierte Geometrie an echte Parameter binden.','geometry.mjs: centre,width,profilePrism'),
('abweichend',1.15,'ringDistance ist Mittelebenenabstand. 1,80+(0,14+0,14)/2=1,94 m, unter Annahme paralleler gleich breiter Kränze.','1,94 m künftig abgeleitet führen; +0,79 m Gesamtdifferenz.','geometry.mjs: p.ringDistance'),
('abweichend',1.29,'Außenflächenabstand 1,29 m statt abgeleitet 2,08 m. Kein Maß für Flügel-/Kumpfüberstände.','2,08 m ableiten; zusätzliche Außenüberstände gesondert definieren.','runtime-audit.rims; calibrateModel paddle span'),
('abweichend',1,'Es gibt einen Sammeltrog und eine durchgehende Rinne; zwei COMP-TROUGH-Meshes bedeuten nicht zwei Rinnenteile.','Rinne in zwei Teile mit explizitem Stoß gliedern.','geometry.mjs: CAND-TROUGH/CAND-CHANNEL'),
('fehlend',False,'Zwei senkrechte Kanalstützen, kein A-Bock unter Teilstoß. Fotoübersicht lokalisiert A-Bock an Rinnenverbindung.','A-Bock und Stoßposition gemeinsam anlegen.','geometry.mjs: CTX-CHANNEL-SUPPORT'),
('fehlend',None,'Senkrechte Hilfsstützen .14 m vorhanden, aber keine beiden schrägen A-Beine.','A-Beine mit 14×14 cm, tatsächlicher Neigung und Fußauflagen planen.','geometry.mjs: CTX-CHANNEL-SUPPORT'),
('fehlend',None,'Keine Aussparung modelliert; 5 cm ist Fachangabe, nicht aus Pixeln gemessener Wert.','5-cm-Öffnung definieren; Höhe und Lage offen halten.','geometry.mjs: beam'),
('fehlend',None,'Kein A-Bockriegel; Fachquerschnitt 4×14 cm. Welches Maß im konkreten Aufstand vertikal liegt, nicht blind annehmen.','Querschnitt und Achsorientierung gemeinsam festlegen.','geometry.mjs: CTX-CHANNEL-SUPPORT'),
('fehlend',None,'Kein Riegel. 90 cm ist gesamte Riegellänge, nicht lichte Spannweite und nicht Fußabstand.','Gesamtlänge .90 m mit Durchsteckung/Überständen separat führen.','geometry.mjs: CTX-CHANNEL-SUPPORT'),
('fehlend',False,'Keine Durchsteckung, obere/untere Keile oder Riegelauflage. Foto3574540 zeigt Last-/Sicherungspfad.','Rinne→Riegel→A-Beine→lokaler Boden als Kontaktkette erfassen.','geometry.mjs: CTX-CHANNEL-SUPPORT'),
('nicht-vergleichbar',None,'Aktuelles Modell nutzt globale Z-Werte ohne registrierten lokalen Boden am A-Bock. Fachmaß .80 m endet an Unterseite Rinnenboden.','Lokales Geländedatum definieren; keine Gleichsetzung mit troughZ=1.4.','geometry.mjs: channel; calibration.mjs: troughZ'),
('foto-bedingt',None,'Skala am oberen Beinende etwa147–151 cm lesbar; unterer Null-/Fußbezug im Gras ungesichert. Keine belastbare exakte Beinlänge, keine vertikale Höhe.','PR-01/02 verwenden; Nullbezug bestätigen, dann Länge/Neigung ableiten.','kein A-Bein im Runtime'),
('scan-offen',None,'PLY/GLB und neue Fotos geprüft. Horizontale Struktur im Suchband z=2.8–3.5 als Trogkandidat, aber Zuordnung und mechanische Registrierung nicht eindeutig.','Korrespondenzen und unabhängige Prüfstrecke bestimmen; AXIS_NORMALIZED bewahren.','data/scan-transforms.json; scripts/scan-inspect.py')]
assert len(rows)==39
records=[]
for c,r in zip(intake['claims'],rows):
 status,current,finding,action,anchor=r
 records.append({'claim_id':c['id'],'subject':c['subject'],'property':c['predicate'],'intake':c,'comparison_status':status,'current_runtime':{'value':current,'unit':c.get('unit'),'anchor':anchor,'scope':'unchanged main / default V3 brute; absence is not a metric zero'},'finding':finding,'proposed_action':action,'applied':False,'as_built_promoted':False})
save('CONSTRAINT-DELTA.json',{'schema':'ks-astra-comparison/v1','base_commit':'f7b9185517856b7881530ba9d0553f170787cb09','canonical_changes':False,'entries':records,'historical_dimensions':intake['historical_dimensions'],'historical_policy':'Historical design and conditional cm interpretation remain separate from current expert measures. Approximate and open values retain intake qualifiers.'})
text='''# ITER-002 — Evidenzvergleich

Basis: `jdistlr/kleines-schaeferrad`, main `f7b9185517856b7881530ba9d0553f170787cb09` (Merge PR #13). Arbeitsbranch: `work/astra-abgleich-iter002-20261009`. Nur Vergleich; keine kanonische Übernahme oder Geometriekorrektur.

## Methode und Ergebnisgrenzen

Alle 65 Originaldateien aus dem Manifest wurden anhand ihrer tatsächlichen Bildinhalte visuell betrachtet (63 unterschiedliche Bildbytes, 67 Attachment-Vorkommen). Kontaktblätter sind aus diesen Originalen erzeugt; Maßbereiche zusätzlich vergrößert. SHA-256 und Git-Blob-Hashes stimmen. Die gesonderten historischen Zeichnungen wurden ebenfalls visuell betrachtet. Ein Dateiname ist kein Bildbefund. Quellen, Doppelnennungen und Einschränkungen stehen in `PHOTO-OBSERVATIONS.json`, Ablesungen in `PHOTO-READOUTS.json`.

`makeModel('A',0,{modelMode:'brute'})` wurde mit aktiver V3-Kalibrierung instanziiert. Gezählt und vermessen wurden die transformierten tatsächlichen Meshes (591 Meshes), außerdem Truth-Anzeige (70) und Nagelreferenz (20). Die alten 0,32/0,22-m-Pins aus geometry.mjs werden von calibrateModel entfernt und sind **nicht** der aktive Nagelbefund. `evidence/runtime-audit.json` und Meshregister sichern Zahlen und Input-Hashes. Viewer-Standard und Optionen entsprechen dem geprüften Zustand. Truth-Anzeige bedeutet nicht metrisch bestätigtes Ist-Modell: auch sie enthält u. a. die falsche Wellenverjüngung und synthetische Armgeometrie.

Fotos begründen sichtbare Topologie; verdeckte Form, absolute Pose und globale Maße folgen daraus nicht automatisch. Die 39 Fachangaben behalten ihre eigene Autorität. Näherungswerte und abgeleitete Werte werden nicht als neue Messungen ausgegeben.

## Vollständige Claim-Matrix

ID-Präfix aller Zeilen: `TH-20261009-`. Vollständige Originalquellen, Property-Namen, Werte, Einheiten, Korrekturbeziehungen und Formeln stehen je Zeile in `CONSTRAINT-DELTA.json` (eingebetteter Intake unverändert).

| Claim / Baugruppe | Neue Angabe | Tatsächlicher Ist-Code | Befund / Fotoabgleich | Konkrete spätere Maßnahme |
|---|---|---|---|---|
'''
for c,r in zip(intake['claims'],rows):
 status,current,finding,action,anchor=r
 vals=[c['id'][-2:]+' / '+c['subject'],c['statement'],anchor,('**'+status+'**: '+finding),action]
 text+='| '+' | '.join(v.replace('|','/') for v in vals)+' |\n'
text+='''
## Abhängigkeiten, die eine reine Parameteränderung übersehen würde

- Kränze: Innenflächen 1,80 m → Mittelebenen 1,94 m → Außenflächen 2,08 m. Die beiden Mittelebenen verschieben sich bei symmetrischer Lage jeweils um 0,395 m. Wellenkontakt, Arme, Nägel, Kumpfpositionen und Trog dürfen dabei nicht auf alten X-Koordinaten verbleiben.
- Flügelbrettspanne: aktuell `ringDistance + 2*paddleAxialOverhang = 1.29`. Die .07 m werden ab Mittelebene gerechnet und entsprechen genau der halben Kranzbreite; somit **kein axialer Überstand über die Außenflächen**. Nur ringDistance zu ändern ergäbe 2,08 m mit demselben Nullüberstand. Reale Brettgesamtlänge und Überstand benötigen eigene Semantik. Radialer Überstand ist hiervon getrennt.
- Arme: `armWidth` und `armDepth` im JSON suggerieren Steuerbarkeit, die hardcodierten .14/.12 im Generator bieten sie nicht. Zentraler Dogleg und Layer-Abstände sind weiterhin Kandidaten, nicht durch die neue Querschnittsangabe bestätigt.
- Kumpfnägel: `exitX=-.495` und der interne Aufruf `vesselPose(0)` verwenden den Default statt sämtlicher äußerer Varianten. Neue Kranzlage oder Kumpfpose propagiert nicht zuverlässig. Ø26 mm Schaft kollidiert zudem mit den bisherigen Ø24-mm-Referenzlöchern. Lochbild, Spiel und Pose müssen gemeinsam überprüft werden.
- Historische Zeichnungen 6828/6829 zeigen einen Trog mit unterschiedlichen Ober-/Unterbreiten (50/32 bei bedingter cm-Auslegung), kein rechteckiges U-Profil wie der Kandidat. 250 außen und 244 an einer weiteren Maßlinie sind keine frei austauschbaren Längen. Rinne 6830 ist eine separate Konstruktion; ihre mehrteiligen Maßketten dürfen nicht auf die aktuelle Rinne übertragen werden, ohne Endpunkte zuzuordnen.
- Kranzzeichnung 6848–6852: 426/396 sowie 213/198 und 60° sind konsistent unter cm-Auslegung; Ø4,26 m ist Kranzaußenkontur. Die radiale Tiefe 15 cm bleibt unabhängig von der korrigierten axialen Breite 14 cm. Wiederholte Aufnahmen desselben Blattes sind keine unabhängigen Maßbestätigungen.

## Kanonische Reconciliation als nächster, hier nicht ausgeführter Schritt

Die 369 bestehenden `geometry.claims` und 21 Assembly-Relationen werden nicht überschrieben. Neue Properties ergänzen sie mit Intake-ID und Quellenbezug. `EDGE-019` (Kumpfnagel→Krümmling) bleibt gültig; `EDGE-020` (Überlappung) braucht den präziseren Langnagel-/Seitenbezug. `EDGE-021` / `CLAIM-0369` können den nun benannten Bezug zur Kranzebene erhalten, aber keinen bestätigten Radialpitch. `CLAIM-0340` (aktuelle Zahl/Phase) bleibt offen; 24 Slots sind keine bestätigte Inventur. Historische `CLAIM-0053` (48 Schetternägel) bleibt historische Zählung.

Intake-Bezeichnungen `COMP-SCHETTERNBRETTER`, `COMP-WOOD-BANDS`, `COMP-TROUGH-SUPPORT`, `COMP-A-BOCK` sind noch keine zugesicherten kanonischen IDs. Radbock gegen vorhandene FRAME/BEARING-STANDS, A-Bock gegen CHANNEL-SUPPORT abgrenzen; weder beide Böcke noch Sammeltrog/Rinne gleichsetzen. Neue Verbindungen brauchen Loch-/Sitz-/Auflagebeziehungen mit offener Metrik. Supersedes: axial 15→14 cm; 1,80 m→lichte Innenweite; Band über Schettern→über Flügelbrett; Schetternbrett ist Stoßverbinder.

ITER-001-Auditgrenzen bleiben bestehen: keine Feldregistrierung des Scans, keine bestätigten Instanz-IDs, kein As-built-Status, keine Replikationsfreigabe aller 24 Kumpf-/Flügel-Slots. Die alten offenen Befestigungsprinzipien sind durch die neuen Aussagen teilweise beantwortet; nur Restfragen stehen in `OPEN-QUESTIONS.md`.

## Technische Ansichten

Die sieben Bildpaare unter `views/01-*.png` bis `07-*.png` vergleichen unveränderte Laufzeitdreiecke mit Originalfotos. `views/manifest.json` nennt Selektion, Kamera und Quelle. Die Ansichten sind orthografische technische Visualisierungen mit einfacher Tiefensortierung, **keine metrisch registrierten Foto-Overlays**; kein Pixelabstand zwischen den Hälften ist eine Messung. Scan-Suchansicht separat in `views/scan-search.png`.
'''
(O/'EVIDENCE-COMPARISON.md').write_text(text)
save('MODEL-DELTA.json',{'base_commit':'f7b9185517856b7881530ba9d0553f170787cb09','mode':'comparison-only','applied':False,'runtime_files_changed':[],'canonical_files_changed':[],'model_corrected':False,'truth_model_changed':False,'deployment':False,'merge':False,'proposals':'CONSTRAINT-DELTA.json'})
print('39 comparison records written')

with (O/'EVIDENCE-COMPARISON.md').open('a') as f: f.write('\n## Auswirkungen auf bestehende Konflikt- und Lückenregister (nur Vorschlag)\n\n| Bestehende ID | Reviewbefund für eine spätere Reconciliation |\n|---|---|\n| CONFLICT-01/02 | Dauben-/Nut- und Metallbandvarianten unverändert; neue Kumpfnagelmaße lösen diese nicht. |\n| CONFLICT-03 | Gleichmäßiger Holzquerschnitt präzisiert Form, löst aber370/37 gegenüber anderen historischen Wellen-/Rohholzmaßen nicht. |\n| CONFLICT-04 | Axial14cm versus radial15cm jetzt eindeutig getrennt; kein Zahlenmittel. |\n| CONFLICT-05 | Armsitz und Querschnitt präzisiert, verdeckte Zentralverbindung/Armfolge weiterhin offen. |\n| CONFLICT-06 | Schetternnägel, Kumpfnägel, Holzband und Keile funktional getrennt; mehrere frühere Grundfragen beantwortet. |\n| CONFLICT-07/08 | Aktuelle Vollzählung und Scanlücken nicht durch lokale Detailfotos gelöst. |\n| CONFLICT-09/10 | Exportachsen plausibel dokumentiert; mechanische Registrierung und Feldmaßstab weiterhin offen. |\n| CONFLICT-11 | Katalogkorrektur bleibt erhalten; keine Neuzuordnung historischer Metallteile als Kumpfnägel. |\n| CONFLICT-12 | Trog250/244 bleibt endpunktbezogen offen. |\n| CONFLICT-13 |90° zur Kranzebene geklärt; lokaler Pitch und Anschlüsse nicht automatisch korrigiert. |\n| GAP-01 | Innenweite und axiale Breite beantwortet; Datums-/Lager-/Seitenbezug und Kontrollmaße bleiben. |\n| GAP-02/03 | Befestigungsprinzipien beantwortet, individuelle Markierungen/Lochbilder/Passflächen erst beim Ausbau. |\n| GAP-04 | Langnagelseite und26/40mm präzisiert; Lochzuordnung, Kurvenlänge und Einbaupose weiter offen. |\n| GAP-05/08 | Umfangsinventur und Ereignis-/Partnerlog weiter nötig; keine automatische physische Instanzzuweisung. |\n| GAP-06 | Direktes Holzlager und Dorn beschrieben, metrische Lagerzentren und Kontakte offen. |\n| GAP-07 | Zweiteilige Rinne, A-Bock und80-cm-Endpunkt ergänzt; Wasserlinie, Drehrichtung und registrierte Trogpose weiter offen. |\n| GAP-09 | Ebenenbezug beantwortet; Pitch-/Kontaktprüfung als Restaufgabe eingrenzen. |\n')
