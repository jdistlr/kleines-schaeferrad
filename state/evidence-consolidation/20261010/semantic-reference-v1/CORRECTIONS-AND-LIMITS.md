# Technische Korrekturen und verbleibende Grenzen

Ausgangspunkt: Remote-HEAD von PR #20 am 10.10.2026 erneut geprüft, `727a0248c0234641453a08e4ae3984e27c9f970b`. Offener Draft gegen `design/lab-ordnung-entwurf-20261010`; keine fremde Arbeit überschrieben. Kein AGENTS.md, CLAUDE.md oder Copilot-Anweisungsfile im Checkout gefunden. README, Projektkontext, Fortsetzungsauftrag und vollständiges Reviewpaket einschließlich Kontextidentitäts-Nachtrag wurden gelesen. Der aktuelle Nutzerauftrag autorisiert belegte technische Referenzkorrekturen über den früheren rein lesenden Auftrag hinaus.

## Umgesetzte Änderungen

| Vorher | Nachher | Beleg und Grenze |
|---|---|---|
| COMP-KUMPF-NAILS nennt PHOTO-6822 / PHOTO-6832 | V2-IMG_6822 / V2-IMG_6832 | Exakte vorhandene IDs aus `evidence/additions-v2.json`; archivierte Hashes passen zum Transfer. Einzelbilder zeigen Stiftpaar bzw. Einzelstift. Keine neue Quelle/Geometrie. |
| Vier Modellquellenverweise nennen V2-IMG_6808 | V2-IMG_6808-upload2 | Register, Originalbytes und gesichtete Wellenansicht passen. COMP-SHAFT, COMP-ARMS, COMP-FASTENERS, COMP-BEARINGS. Keine Ausweitung der Evidenzgeltung. |
| TASK-PAD referenziert nur GAP-05/-08 | Zusätzlich GAP-09 | Auftrag nennt bereits radialen Pitch, Kranzbezug, Kontaktpartner und drei Schaufeln; deckt den Gegenstand von GAP-09 ab. Nur Kante ergänzt; Aufgabe, Akzeptanzbedingungen und OPEN-Status unverändert. |
| Regel „IMG_6875/6876 … Originale fehlen“ | Archiviert, aber Identität unbestätigt; keine Zielbestätigung | Durch Nachtrag und aktuelle Originalsichtung belegt. Historischer Kontexttext bekommt vorangestellten Hinweis. Keine Anpassung der Kontext-/Ghost-Geometrie. |

Die abhängige `task_source_sha256` im Feldpaket-Manifest wird auf den neuen Aufgabenvertrag gesetzt. Der vorhandene PDF-Renderer wird dafür mit altem und neuem Aufgabenvertrag ausschließlich in einem temporären Arbeitsverzeichnis ausgeführt, ohne Geometrieexport. `field-pack-equivalence.json` belegt unveränderte Ausgabebytes zwischen beiden Läufen; einzige Manifestdifferenz ist die Eingabeprüfsumme. Bestehende Zeichnungen, PDFs, Visuals und ihre Abnahme bleiben unangetastet. Die Vergleichshashes sind keine neue visuelle Freigabe.

Exakte Änderungsliste: `reference-corrections.json`. Der Prüfer rekonstruiert diese begrenzten Änderungen aus dem Basiscommit und vergleicht die vollständigen JSON-Verträge; zusätzliche Wert-/Statusänderungen würden fehlschlagen. Frühere Berichte erhalten nur einen aktuellen Wegweiser, ihr Inhalt bleibt als Historie vollständig erhalten.

## Was technisch ausgeräumt ist

Die sechs fehlerhaften Quellenverweise lösen sich nun auf. GAP-09 hat eine direkte Kante zur bestehenden Untersuchung; alle neun Lücken sind an mindestens eine vorhandene Feldaufgabe angebunden. 408 Claims, 34 Komponenten, 117 Quellenanalysen, neun GAPs und 21 Aufgaben bleiben erhalten. Dies schließt Referenzfehler, keine fachlichen Lücken.

Der lesende Graphaudit wird unverändert weiterverwendet. Seine zehn verbleibenden strengen Typkandidaten sind die acht dokumentierten H-ARM-Verweise sowie REF-Welle und CAPTURE-01; Auflösungsorte siehe frühere GRAPH-CONTRACT-AND-INTEGRITY.md. Der Prüfer wird nicht durch Löschen dieser Meldungen „grün gemacht“. Zusätzliche unbekannte Quellreferenzen werden gesondert abgewiesen.

## Bewusst nicht zusammengeführt

| Befund | Behandlung in v1 | Noch benötigter Nachweis |
|---|---|---|
| 24 Gruppen semantisch ähnlicher Claims | Beibehalten; `duplicate-review.json` zeigt je Claim Klasse, Geltung, Provenienz und Dokumentgruppe. Gleiches Werttupel ist keine automatische gleiche Evidenz. | Einzelfallentscheidung über Darstellung/Verlinkung; keine Löschung erforderlich. |
| EXT-VZO mit `wasserrad.html` und `info.html` | Nicht umbenannt/umgebogen. EXT-VZO-INFO existiert bereits, dennoch ist die historische Zuordnung der Aussagen nicht bewiesen. | Gesicherte Abrufinhalte und Aussageherkunft abgleichen. Keine externe Webprüfung innerhalb dieses reinen Repositoryauftrags behauptet. |
| COMP-RADSTATT / COMP-RADSTADT | Namensbeziehung und TH-19 im Begriffsverzeichnis kenntlich; beide IDs erhalten. | Prüfen, ob Bedeutungsumfang vollständig identisch ist, bevor irgendeine ID-Migration erfolgt. |
| 16 Transferdateien ohne exakten Register-ID-Hash-Treffer | Alle einzeln gesichtet oder als Video geprüft; weiterhin über unveränderlichen Pfad/Hash referenzierbar. | Keine automatische neue Quellen-ID und keine optische Gleichsetzung mit anderen Bytevarianten. |
| Quellenindex enthält mehrere Ebenen | Foto-/Blatt-/Aufnahme-/Objektidentität ausdrücklich getrennt. | Herkunft und heutige Instanzzuordnung bleiben eigenschaftsweise erforderlich. |

## Sichtungs- und fachliche Grenzen

1. **Tonspur IMG_6857:** vorhanden, vollständig technisch dekodierbar, aber nicht gehört oder transkribiert. Kein geeignetes Audioanalysewerkzeug verfügbar. Eine vollständige audiovisuelle Quellensichtung bleibt deshalb offen. Sie muss nachgereicht werden, falls v1 als uneingeschränkt abgeschlossenes Quellenreview akzeptiert werden soll; keine Aussage daraus verwendet.
2. **IMG_6875–6877:** lesbar und archiviert; Objektidentität weiterhin ausdrücklich unbestätigt. Weder untereinander noch mit dem Zielrad gleichgesetzt. Benötigt nachvollziehbare Fundstelle/Ort oder begründete ortskundige Zuordnung. Kein erneuter Dateitransfer nötig.
3. **Visuelle Auflösung:** 76 Fotos jeweils als Einzelbild bis 1050 Pixel Kantenlänge; sechs Referenzoriginale zusätzlich unmittelbar; Video 638 Frames als kleine Übersicht plus 43 größere Zeitbilder. Keine lückenlose neue Zifferntranskription jedes Blattes, keine Detailprüfung jedes Videoframes in voller Auflösung. Zweifelhafte Beschriftungen bleiben ungeklärt statt erraten.
4. **Sachstand vor Ort:** aktuelle Demontage, reale Partner/Teilmarkierungen und noch verfügbare Aufnahmefenster nicht bekannt. Historische Slots sind kein reales Instanzregister. Keine neue heutige Stückzahl.
5. **Metrik und Verbindungen:** Arm-Innenpaarung, Nagelwege, Stoßflächen, Kranz-/Lagerpose, Referenzinstanzen und Schaufelpitch brauchen die bestehenden Feldnachweise. Keiner der neun Gesamt-GAPs geschlossen.
6. **Geometrie/Kollision:** keine räumliche Kollisionssimulation oder Browserabnahme durchgeführt. F02/F03, Geometrie, Modellparameter und produktive UX unverändert; semantische Referenzprüfung sagt nichts über Kollisionsfreiheit aus.
7. **Externe Quellen:** nur gespeicherte Verträge geprüft; kein Live-Web-Audit und keine daraus abgeleitete neue Fachentscheidung.

## Review-Gate

Die semantische Referenzbasis v1 ist in ihrem dokumentierten Umfang reviewfähig. Ein bedingungsloses „alle Quellen vollständig ausgewertet“ wäre wegen der Audio- und Auflösungsgrenzen falsch. Johannes entscheidet über Annahme dieser Reviewbasis und nachfolgende Arbeit; fachliche Geltungs-/Instanzfragen bleiben beim Fachreview. Keine Fragen an Thorsten versendet, keine Freigaben erfunden. Kein Merge, kein Deployment. Nach Sicherung auf GitHub gestoppt.
