# Drei exemplarische Beweisketten

Stand 2026-10-10. Alle genannten archivierten Dateien sind vorhanden und bytegeprüft. Einzelbild-Sichtprüfung dieser Session: PHOTO-6816, PHOTO-6827, PHOTO-6823, PHOTO-6851, PHOTO-6853, PHOTO-1000046420..6423, PHOTO-TH-20261009-image-1791540525839 und PHOTO-TH-20261009-image-1791540812566. Zusätzlich Sichtung der fünf Kontaktübersichten aller 76 Transferfotos und drei Videozeitpunkte. Bildvergleich dient Beobachtung und Geltungsabgrenzung, nicht neuer Maßfreigabe.

Im Folgenden sind `beobachtet`, `Quelle berichtet`, `Registerbeziehung` und `abgeleitet` bewusst getrennt. Die Prüfketten verwenden bestehende IDs; keine neue fachliche Ontologie. SHA-256 und Bytezuordnung: `audit-results.json`. Nicht jede verwandte Aufnahme wurde in dieser Session erneut einzeln visuell bewertet.

## Welle und Armverbindung

| Stufe | Quelle / konkreter Ort | Aussage und Geltungsgrenze |
|---|---|---|
| Unmittelbare Beobachtung | `evidence/raw/IMG_6816.jpeg` / PHOTO-6816, linke lange Maßlinie, oberes Quermaß, unterer Querschnitt | Auf dem fotografierten Blatt stehen 370 und 37; zwei Schlitzgruppen und ein gekreuzter Querschnitt sind gezeichnet. Im betrachteten Blatt keine explizite lineare Einheit erkannt. |
| Bestehende Aussagen | `data/geometry.claims.json`: CLAIM-0001/-0002/-0007/-0008 | Historische Zeichnung, `documented-design`, `as_built_eligible:false`. PHOTO-6817 ist laut Quellenregister ein anderes Foto desselben DOC-SHAFT, keine unabhängige Maßbestätigung. IMG_6815 ist eine visuell korrespondierende zusätzliche Aufnahme, noch ohne kanonische ID. |
| Unmittelbarer Gegenvergleich | `evidence/raw/IMG_6827.jpeg` / PHOTO-6827, Titel und Zeile „Welle“ | Titel nennt ausdrücklich empfohlene Holzmaße; Zeile nennt 4,50 m, 50 cm und Einbaugröße 40 cm. Das ist als Material-/Beschaffungsempfehlung lesbar, kein dokumentiertes Aufmaß der abgebildeten Welle. |
| Bestehender Prüfbedarf | CLAIM-0346 / CONFLICT-03 | Vergleich von 370/37 mit allgemeinen Holzempfehlungen. Eine Vermischung der Geltungsbereiche ist plausibel; der Konflikt wird hier nicht eigenmächtig aufgelöst. |
| Aktuelles Foto | `evidence/raw/IMG_6853.jpeg` / PHOTO-6853, beide Eintrittszonen der Welle | Sichtbar sind verwitterte Holzoberfläche, einsetzende Arme und keilartige Hölzer. Innere Paarung, Tiefe, versteckte Kontaktflächen und vollständige Mortisengeometrie sind nicht sichtbar. Unterstützt die Begrenzung von CLAIM-0253 und CLAIM-0336; kein Beweis für eine bestimmte Innenverbindung. |
| Fachauskunft | `evidence/contributions/thorsten-20261009.json`: TH-20261009-13/-14/-15; kanonische Provenienz NARRATIVE-TH-CONSTRUCTION-20261009 | Gleichmäßiger Holzwellenquerschnitt, zwei Eisenschellen je Ende, Dorn im Holzlager sind dokumentierte Fachangaben. Der Beitrag ist als semantische Transkription gespeichert, nicht als Tonoriginal. Exakte Kontur und Passungsmaße folgen daraus nicht. |
| Modellumsetzung | `data/reconstruction-constraints.json:shaft`; `src/workbench/expert-corrections.mjs:applyExpertCorrections` | Code ersetzt HYP-SHAFT durch konstanten Kandidatenquerschnitt und erzeugt Schellen. `clampWidths`, `clampInset`, `journalDiameter` und `journalExtension` bleiben gemäß metricStatus Kandidaten. Kein neuer Mesh-Nachweis; Quellcodezuordnung bestätigt nur Implementierungsabsicht. |
| Lücke / Untersuchung | GAP-02, GAP-06; TASK-ARM-BEFORE, TASK-ARM-RELEASE, TASK-MORTISE, TASK-ARM-PROFILE, TASK-KEI, TASK-BEARING | Partnerbezüge, Ein-/Austrittsflächen, Keilrichtung, Tiefen und Lagerreferenzen am realen Teil festhalten. Erfüllung und noch verfügbare Aufnahmefenster sind nicht nachgewiesen. |
| Entscheidung | ENT-WELLE-01/-02/-03 aus bestehendem Entscheidungsentwurf | Thorsten kann Geltung/Einheiten/Varianten erläutern oder „nicht entscheidbar“ wählen. Die derzeitige Akte trägt keine aktuelle Wellenlänge, keine Innengeometriefreigabe und keine technische Fertigungszeichnung. |

**Kettentypen:** PHOTO-6816 → CLAIM-0001/-0002 ist eine bestehende Zeichnungsprovenienz; PHOTO-6827 → CONFLICT-03 ein bestehender Vergleichskontext; PHOTO-6853 → sichtbare Oberfläche eine visuelle Beobachtung; TH-13/-14 → Modellfunktion ein lesender Codeabgleich. Ein Modellbild wird an keiner Stelle als Rückbeweis verwendet.

## Kumpf, Dauben, Ringe und Befestigung

| Stufe | Quelle / konkreter Ort | Aussage und Geltungsgrenze |
|---|---|---|
| Unmittelbare Beobachtung | `evidence/raw/IMG_6823.jpeg` / PHOTO-6823, oberer und unterer Textblock | Zwei Beschriftungsfamilien: 24 bzw. 22 mm Dauben; Nutangaben 244/264 bzw. 248/268. Dies sind Blattangaben. Welcher aktuelle Kumpf welcher Familie entspricht, ist nicht durch das Blatt bewiesen. |
| Bestehende Aussagen | CLAIM-0040..0047, CLAIM-0344 / CONFLICT-01 | Varianten-/Zuordnungsfrage, keine durch die Assistenz gewählte „richtige“ Stärke. Historische Werte bleiben getrennt. |
| Unmittelbare Beobachtung | PHOTO-1000046420, Innenansicht mit fehlenden Dauben und Maßstab; PHOTO-1000046421/-6422, Endansichten; PHOTO-1000046423, Außenansicht | Bodenaufnahme/Nut, Dauben und Öffnungen sind sichtbar; Außenansicht zeigt drei Metallbänder. Der Maßstab erlaubt ohne festgelegte Endpunkte und Perspektivprüfung keine automatische Übernahme eines Ist-Maßes. |
| Fachauskunft | `evidence/contributions/kumpf-20261008.json:source,claims,supplementary_sources`; NARRATIVE-TH-KUMPF-20261008-01..03 | Zwölf Dauben, ein Boden, Nutaufnahme und drei Ringe; gefertigte Varianten; Referenz-Kumpf laut Fachkenner „mit dem richtigen Maß“. Daraus folgt keine Gleichheit aller verbauten Kümpfe. |
| Kanonische Einordnung | CLAIM-0356..0361; CONFLICT-02 | Konstruktive Angaben sind erfasst. Variantenfamilie bestätigt, numerische Zuordnung der Ringlängen weiterhin offen. Die in Beiträgen vorhandenen EXPERT-KUMPF-IDs und kanonischen CLAIM-IDs beschreiben teilweise denselben Fachbeitrag, nicht zusätzliche unabhängige Zeugen. |
| Befestigungsfunktion | NARRATIVE-TH-KUMPF-20261008-02/-03, TH-20261009-16/-17/-18 | Fachlich beschriebene Kumpfnägel und Lang-/Kurzpaarfunktion bleiben erhalten. Unregistrierte Verweise PHOTO-6822/-6832 sind ein Identitätsproblem im Komponentenvertrag; die Originale liegen als V2-IMG_6822/-6832 vor. Exakte Nagelwege bleiben offen. |
| Modellumsetzung | `data/hypothesis.parameters.json:variants`, `data/calibration-v3.json`, `data/reconstruction-constraints.json:nails`, `src/workbench/calibration.mjs:referenceKumpf` | Modellvarianten/Referenzgeometrie und Kandidaten für Pfade, Kopfmaß, Luft und Eindringtiefe. `nailPath` im Code ist ein berechneter Kandidat, keine beobachtete innere Bohrung. Keine Modellvariante als ausgeführtes Teil ausgewählt. |
| Lücke / Untersuchung | GAP-04; TASK-KUM-BEFORE, TASK-KUM-VARIANT, TASK-HOOPS; ergänzend TASK-KEI | Referenzinstanz eindeutig kennzeichnen; beide Enden und Nut aufnehmen; Ringlage, fertige Länge und Überlappung getrennt messen; Befestigung über Nachbarkümpfe samt Ein-/Austritten vor Lösen dokumentieren. |
| Entscheidung | CONFLICT-01/-02 als bestehende Anker | Welche Zahlenfamilie gilt für welche benannte Instanz? Fachkenner kann Zuordnung bestätigen, einschränken oder weitere Messung verlangen. Ohne Zuordnung bleiben beide Familien im Register. |

Die drei UUID-Bilder aus dem Transferarchiv zeigen ähnliche Referenzansichten, haben aber andere Bytes. Sie werden nicht als zusätzliche unabhängige Bestätigung der Referenzmaße gezählt. Im SHA-256-Inventar ist diese Abgrenzung sichtbar.

## Kranz und Krümmlingsanschlüsse

| Stufe | Quelle / konkreter Ort | Aussage und Geltungsgrenze |
|---|---|---|
| Unmittelbare Beobachtung | `evidence/raw/IMG_6851.jpeg` / PHOTO-6851, rechter oberer Rand und radiale Maßlinien | Beschriftung „Krümmling-Breite 14 cm“, Radien 198/213 sowie Durchmesserbeschriftungen 396/426 sichtbar. Die Zeichnung allein ist kein heutiges Aufmaß. |
| Gemeinsamer Quellhintergrund | DOC-RIM-DETAILED: PHOTO-6848..6852; V2-IMG_6790 und neue Ansicht IMG_6791 | Mehrere Fotos mit übereinstimmenden Zeichenmerkmalen, keine Vielzahl unabhängiger Konstruktionsentscheidungen. Keine neue Versionschronologie aus Dateinummern. |
| Bereits dokumentierte Einordnung | CONFLICT-04 / CLAIM-0347; TH-20261009-26 | Der Konfliktvertrag ist `semantic-dimensions-resolved`: 14 cm axial und Differenz der historischen Radien 213−198 betreffen unterschiedliche Richtungen. Dies ist Übernahme des gespeicherten Reviewstands, keine neue fachliche Auflösung durch Assistenz. |
| Aktuelle Originalstelle | PHOTO-TH-20261009-image-1791540525839, mittiger Armsitz; PHOTO-TH-20261009-image-1791540812566, seitliche Bretter/überstehende Hölzer am Kranz | Bilder zeigen Anschlussdetails aus begrenzten Perspektiven. Nicht alle verdeckten Flächen und Sicherungen sind sichtbar. Foto mit Maßstab wird hier nicht neu metrisch abgelesen. |
| Fachauskunft | TH-20261009-01..05 im Originalbeitrag | Arm durch Segmentmitte; örtliche Verstärkung; Keile/Sicherung; Schetternbretter verbinden Segmente. Die vollständige Konstruktionsbeschreibung stammt aus Fachauskunft, nicht allein aus zwei Detailfotos. |
| Maßkette | TH-20261009-25/-26 → TH-20261009-28/-29 | 1,80 m lichter Abstand und 0,14 m axiale Breite sind expert-reported. 1,94 m Mittelebenenabstand = 1,80+(0,14+0,14)/2; 2,08 m Außenbreite = 1,80+2×0,14. Symmetrische gleiche Breiten vorausgesetzt; beide Ergebnisse sind Ableitungen, keine unabhängigen Messungen. |
| Modellbezug | `data/reconstruction-constraints.json:rings,arms,schettern`; `src/control/property-readiness.mjs`; `src/workbench/expert-corrections.mjs` | Fünf Maßmappings sind explizit. Armsitz-Toleranzen, Verstärkungsgeometrie, Brettstärke und Lochlayout enthalten Kandidaten. Das Modell darf diese Annahmen darstellen, aber weder Messung noch Freigabe ersetzen. |
| Lücke / Untersuchung | GAP-01/GAP-03; TASK-POSE, TASK-KRU-BEFORE, TASK-KRU-OPEN | Bezugsebenen, aktuelle Ringform und beide Stoßflächen samt Partnern aufnehmen; Endpunkte/Einheiten/Unsicherheit dokumentieren. Die übernommene Topologie schließt aktuelle Form- und Zustandslücken nicht. |
| Entscheidung | Bestehende TH-25/-26/-28/-29 und GAP-03 | Keine erneute Abstimmung über die bereits berichtete axiale 14-cm-Korrektur verlangen. Zu klären bleiben Geltungsinstanzen, nachgewiesene Endpunkte sowie zulässige Darstellung der offenen Anschlussmaße. |

## Nicht überbrückte Stellen

Die drei Ketten enthalten bewusst offene Übergänge zwischen Quelleninhalt, konkreter aktueller Teilinstanz und technisch freigegebener Geometrie. Die fehlenden IMG_6875/6876 werden für keinen neuen Bildbefund dieser Ketten verwendet. Aus dem Video werden keine Maß- oder Bewegungsfreigaben abgeleitet. Ein abgeschlossenes Dossier bedeutet hier: Quellen, Abhängigkeiten und noch benötigte Entscheidungen sind nachvollziehbar — nicht: das Bauteil ist vollständig bewiesen.
