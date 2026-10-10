# Drei prüfbare Referenzfälle

Die vollständigen früheren Ketten in [EVIDENCE-CHAINS.md](../EVIDENCE-CHAINS.md) bleiben erhalten. Hier wird ihr überprüfbarer Sollinhalt für v1 festgehalten. Pfade beziehen sich auf das Repository; Hashes und Sichtungsprotokoll stehen in `source-sighting.json`. Keine neue Fachentscheidung.

## Welle und Arm

| Schritt | Konkreter Nachweis | Zulässige Aussage / Grenze |
|---|---|---|
| Original und Bildregion | `evidence/raw/IMG_6816.jpeg`, lange Maßlinie links und Quermaß oben; IMG_6815–6817 als weitere Blattansichten | Auf dem Blatt stehen 370 / 37. Keine explizite lineare Einheit erkannt. |
| Bestehender Claim | CLAIM-0001/-0002, `historical-drawing`, `scope:documented-design`, `unit:null`, `as_built_eligible:false` | Keine 3,70-m-Ist-Welle daraus erzeugen. DOC-SHAFT ist ein Dokumenthintergrund, keine Serie unabhängiger Aufmaße. |
| Gegenquelle | PHOTO-6827, Titel und Wellenzeile; CLAIM-0346 / CONFLICT-03 | 4,50 m / 50 cm / 40 cm stehen in einer Empfehlung. Unterschiedliche Geltung ist zu prüfen, nicht Werte mitteln. |
| Aktuelle Beobachtung | PHOTO-6853, PHOTO-6855/-6856 und V2-IMG_6808-upload2: Eintrittszonen und Keilhölzer | Sichtbare Eintritte und äußere Oberflächen; keine Innenpaarung oder Mortisentiefen. |
| Fachauskunft | TH-20261009-13/-14/-15 → NARRATIVE-TH-CONSTRUCTION-20261009 | Konstanter Holzwellenquerschnitt, Endschellen, Dorn-/Holzlagerfunktion fachlich berichtet. Keine neuen Passmaße. |
| Modellbezug | `data/reconstruction-constraints.json:shaft`, `src/workbench/expert-corrections.mjs:applyExpertCorrections` | Kandidaten für Schellen-/Dornmaße bleiben Kandidaten; kein neuer Meshbeweis. |
| Rest und Untersuchung | GAP-02/-06 → TASK-ARM-BEFORE, TASK-ARM-RELEASE, TASK-MORTISE, TASK-ARM-PROFILE, TASK-KEI, TASK-BEARING | Endpartner, geöffnete Kontaktflächen, Keilrichtung und Lagerreferenzen am realen Teil. Tatsächlicher Demontagestand nicht bekannt. |

**Positivbeispiel:** „CLAIM-0001 transkribiert 370 aus DOC-SHAFT; Einheit und heutige Geltung sind nicht bestätigt.“ **Negativbeispiel:** „Zwei Wellenfotos bestätigen eine 3,70 m lange heutige Welle“ ist durch die Referenzakte nicht gedeckt. Die Prüfdatei kontrolliert Klasse, Einheit, Geltung, Provenienz und offene Aufgaben.

## Kumpf

| Schritt | Konkreter Nachweis | Zulässige Aussage / Grenze |
|---|---|---|
| Variantenblatt | PHOTO-6823, oberer/unterer Textblock; CLAIM-0040..0047, CLAIM-0344, CONFLICT-01 | 24/22 mm und unterschiedliche Nutangaben sind als Varianten-/Zuordnungsfrage erhalten. Keine Auswahl durch Assistenz. |
| Referenzoriginale | PHOTO-1000046420: offene Dauben/Nut/Lochpaare; -6421/-6422: unterschiedliche Endansichten; -6423: drei Bänder außen | Sichtbare Konstruktion am Referenzgefäß; Lage im Foto ist kein Endname. Maßstab ohne Endpunkt-/Perspektivdefinition ist keine automatische Maßfreigabe. |
| Zusätzliche Ansichten | Drei UUID-JPEGs unter `evidence/raw/originaltransfer-20261010/` | Ähnliche Referenzansichten mit anderen Bytes. Keine zusätzliche unabhängige Bestätigung und keine automatische Instanzfusion. |
| Fachauskunft | NARRATIVE-TH-KUMPF-20261008-01..03; CLAIM-0356..0361; TH-20261009-16..18 | Zwölf Dauben, Boden/Nut, drei Ringe und Lang-/Kurzfunktion fachlich dokumentiert. Referenz-Kumpf und eingebaute Varianten unterscheiden. |
| Technischer Referenzabgleich | COMP-KUMPF-NAILS → V2-IMG_6822 / V2-IMG_6832; Originale `IMG_6822.jpeg` / `IMG_6832.jpeg` | Paarfoto und Einzelstiftfoto waren vorhanden; nur die zwei Quellen-IDs waren falsch geschrieben. Bild und Hash bestätigen die Referenzkorrektur, nicht den inneren Nagelweg. |
| Gegenvergleich Ringlängen | PHOTO-6821: 780/875/968; PHOTO-6846/-6847: 784/880/972; CONFLICT-02 | Blattlänge, Überlappung und fertiger Umfang nicht gleichsetzen. Keine Mittelwertbildung. |
| Modellbezug | `data/hypothesis.parameters.json:variants`, `data/calibration-v3.json`, `data/reconstruction-constraints.json:nails`, `src/workbench/calibration.mjs:referenceKumpf` | Geometrie und `nailPath` sind Implementierungen/Kandidaten, keine beobachteten Bohrwege. |
| Rest und Untersuchung | GAP-04 → TASK-KUM-BEFORE, TASK-KUM-VARIANT, TASK-HOOPS, zusätzlich TASK-KEI | Reale Referenzinstanz, Nut-/Endmessung, drei Bandlagen, Nachbarn, vier Lochpositionen und beide Nagelwege. |

**Positivbeispiel:** „Die Referenzaufnahme zeigt drei Bänder; ihre Längen-/Variantenzuordnung bleibt CONFLICT-02.“ **Negativbeispiel:** „Die neuen UUID-Bilder bestätigen alle eingebauten Kümpfe mit denselben Maßen“ ist nicht gedeckt. Kontaktstreifen PHOTO-6833/-6845 bleiben REF-CONTACTSTRIPS mit unbewiesenem Radbezug.

## Kranz und Krümmlinge

| Schritt | Konkreter Nachweis | Zulässige Aussage / Grenze |
|---|---|---|
| Original und Region | PHOTO-6851, Text „Krümmling-Breite 14 cm“; PHOTO-6849/-6850, Radien 198/213 und Durchmesser 396/426 | Historischer Blattbefund aus DOC-RIM-DETAILED. V2-IMG_6790 und IMG_6791 sind weitere Ansichten, keine unabhängigen Maße. |
| Bereits geklärter Bezug | CONFLICT-04 `semantic-dimensions-resolved`, TH-20261009-26 | 14 cm axial und radiale Differenz 213−198 nicht als konkurrierende Messung derselben Strecke behandeln. CLAIM-0347 ist historischer Konfliktbefund. |
| Fachlich berichtete Topologie | TH-20261009-01..05, Fotos `image-1791540525839.jpg` und `image-1791540812566.jpg` | Armsitz in Segmentmitte und Schetternverbindung am Stoß; Foto allein zeigt nicht sämtliche verdeckten Flächen und Sicherungen. |
| Berichtete Maßgrundlage | TH-20261009-25/-26: 1,80 m lichter Abstand und 0,14 m axial | Expertenangaben, weiterhin `as_built_eligible:false`; keine unabhängige Feldmessung. |
| Abhängige Rechnung | TH-20261009-28 = 1,80+(0,14+0,14)/2 = 1,94 m; TH-29 = 1,80+2×0,14 = 2,08 m | Zwei gleiche axiale Breiten vorausgesetzt; vier Zahlen sind nicht vier unabhängige Messungen. `derived_from` bleibt erhalten. |
| Modellbezug | `reconstruction-constraints.json:rings,arms,schettern`; `property-readiness.mjs`; `expert-corrections.mjs` | Abgleich von Eingaben ist keine geometrische oder fertigungstechnische Abnahme. |
| Rest und Untersuchung | GAP-01/-03 → TASK-POSE, TASK-KRU-BEFORE, TASK-KRU-OPEN | Beide Kranzflächen, aktuelle Form, individuelle Stoßpartner, Loch-/Kontaktbilder und Bezugspunkte messen. |

**Positivbeispiel:** „Der axiale/radiale Bedeutungsunterschied ist geklärt; der reale Kranzstoß bleibt aufzunehmen.“ **Negativbeispiel:** „1,94 m ist gemessen und schließt GAP-01“ ist nicht gedeckt. Auch aus TH-06 / 90° zur Kranzebene folgt kein lokaler Schaufelpitch; TASK-PAD ist jetzt zusätzlich direkt GAP-09 zugeordnet.

## Gemeinsame Ausschlüsse und Reviewfrage

IMG_6875–6877 stützen keinen der drei Fälle als Zielobjektbeleg. Das Video ergänzt sichtbare Perspektiven, aber kein metrisches oder verborgenes Verbindungswissen. Seine Tonspur ist ungeprüft. Alle neun Gesamt-GAPs bleiben offen; es wurde keine neue Teilinstanz erfunden.

Reviewfrage: Trägt diese Referenzbasis die belegten Geltungsgrenzen und die vorhandenen Fachkorrekturen korrekt? Numerische Antworten, neue Zuordnungen oder eine Freigabe werden erst als neue nachvollziehbare Fachevidenz aufgenommen, nicht im Review vorweggenommen. Die bestehenden Fragen ENT-WELLE-01..03 / CONFLICT-01/-02 und die Antwortoption „nicht entscheidbar“ bleiben bestehen.
