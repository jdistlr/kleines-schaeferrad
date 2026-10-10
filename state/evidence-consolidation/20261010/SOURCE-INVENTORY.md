> **Aktuelle Fortsetzung:** [Semantische Referenzbasis v1](semantic-reference-v1/SEMANTIC-REFERENCE-V1.md) dokumentiert Einzelbildsichtung, technische Referenzkorrekturen und verbleibende Grenzen. Der nachfolgende Bericht bleibt unverändert als früherer Prüfstand erhalten. Kontextbilder sind verfügbar, ihre Objektidentität ist weiterhin unbestätigt.

# Quellenbilanz und Unabhängigkeit

Stand 2026-10-10. Grundlage: unveränderte Repositoryverträge und unabhängig von GitHub zurückgelesene Originalbytes. Quellenprüfung und inhaltliche Geltung sind getrennt.

## Umfang und Zugriff

- Transferarchiv: 76 Fotos, ein Video, ein unverändertes Inventar. 77/77 SHA-256- und Größenprüfungen erfolgreich; Bytevergleich gegen ZIP ebenfalls erfolgreich. Zwei Foto-Dublettenpaare; 74 unterschiedliche Fotobytefolgen.
- Gesamter `evidence/raw`-Bestand im geprüften Snapshot: 210 Dateien / 147 unterschiedliche SHA-256-Werte, davon eine Inventar-JSON. Das ist keine Zahl unabhängiger Quellen.
- 215 Archiv-/Kontext-/Derivat-Registereinträge mit Dateipfad geprüft, 146 verschiedene referenzierte Pfade: kein fehlender Pfad, keine SHA-256-/Größenabweichung dort, wo Sollwerte vorliegen. Einträge ohne Sollhash sind als vorhanden, nicht als extern originalverifiziert gewertet.
- 61 der 77 Medien-Dateieingänge passen per SHA-256 auf bereits registrierte Quellen. 16 passen nicht exakt; sie bleiben dateibasiert inventarisiert. Keine neue PHOTO-/CLAIM-ID und kein Überschreiben des historischen Manifests.
- Vorhandene 39 Fachkorrekturen: `evidence/contributions/thorsten-20261009.json`, korrespondierende Claims und Reviewhistorie erhalten. Autor und fachliche Geltung stammen aus dem gespeicherten Beitrag; Aufnahmedatum der Fotos wird daraus nicht abgeleitet.

## Fehlende bzw. nicht unabhängig zugängliche Quellen

`IMG_6875` und `IMG_6876` werden nur in `docs/CONTEXT-EVIDENCE-6875-6876.md` beschrieben; Original-/Screenshotbytes sind weder im Transferarchiv noch in den inventarisierten Rohdateien vorhanden. `data/reconstruction-evidence-map.json` benennt dies selbst. Die Texte sind sekundärer Kontext, kein in dieser Session bestätigter Pixelbefund. Keine dieser Dateien wird durch ähnlich aussehende Bilder stillschweigend ersetzt. Für einen uneingeschränkten Originalquellen-Audit werden genau diese zwei Dateien samt Herkunft benötigt — oder eine ausdrückliche Entscheidung, den betroffenen Kontext aus dem Prüfbereich auszuschließen.

Frühere unbenannte Kontaktbögen bleiben laut Manifest nicht verfügbar; vorhandene neue Kontaktbögen sind Derivate. Noch nicht durchgeführte Feldmessungen und zukünftige Demontageaufnahmen sind erwartete Evidenz, keine verloren gegangenen Originaldateien. Externe Webseiten wurden nur als gespeicherte Repositoryreferenzen geprüft, nicht neu abgerufen.

## Unabhängigkeit und Dokumentversionen

Byteidentische Dateien sind derselbe Inhalt. Andere Foto-Bytes desselben Blattes ergänzen Lesbarkeit und Perspektive, erhöhen aber nicht die Zahl unabhängiger Maßbelege. Das Register enthält DOC-ORDER-OLD/NEW sowie DOC-LAYOUT-OLD: diese Bezeichnungen dokumentieren den bisherigen Katalog, keine neu bewiesene Datierung oder Versionsreihenfolge. Autor, Erstellungsdatum, Aufnahmezeit und heutiger Einbauzustand bleiben offen, soweit nicht explizit belegt.

Die fünf Kontaktübersichten mit allen 76 Transferfotos wurden zur Eingangsorientierung angesehen. Das ersetzt keine vollständige Maßtranskription jedes Blattes. Für die drei Beweisketten wurden die in EVIDENCE-CHAINS genannten Einzeloriginale gezielt angesehen. Kein Maß aus Pixelabständen geschätzt.

## Visuelle Gruppierung der neu eingegangenen Bytevarianten (Prüfvorschläge)

| Eingänge | Beobachtete Beziehung / bestehender Anker | Grenze |
|---|---|---|
| IMG_6790/6791 und IMG_6848–6852 | gleiche charakteristische radiale Zeichnung und farbige Markierungen; 6790 ist bytegleich zu V2-IMG_6790, spätere Ansichten in DOC-RIM-DETAILED | Blattidentität visuell plausibel; keine zusätzliche unabhängige Maßquelle und keine sichere Datierung |
| IMG_6792–6794 | mehrfach fotografierte Skizze mit zwei Längsteilen; vorhandene V2-IDs für die bytegleichen Eingänge | Bauteil-/Versionszuordnung bleibt auslegungsbedürftig |
| IMG_6795–6797 | ähnliche Ansichten desselben karierten Blatts mit Maßketten | IMG_6796 ohne Hash-ID-Treffer; keine neue Fachidentität vergeben |
| IMG_6798/6799 | längliche, gekröpfte Bauteilskizze; bestehende V2-IDs | Zeichnungsmaße, keine Bestandsmessungen |
| IMG_6815–6817 | Wellenblatt mit 370/37 und gekreuztem Querschnitt; 6816/6817 sind DOC-SHAFT | 6815 neuer Fotobytestand desselben sichtbar entsprechenden Blatts; Einheiten bleiben ungesichert |
| IMG_6826/6827 | allgemeine Holzempfehlungstabelle, gleiche Überschrift und Struktur | 6826 neue Bildbytes; keine zweite unabhängige Wellenmessung |
| IMG_6834/6835 | Ausschnitt einer gedruckten Beschilderung mit eingebettetem Radfoto | Foto eines Fotos, kein unabhängiger aktueller Vor-Ort-Befund; Ursprungsdatum offen |
| drei UUID-JPEGs | teilzerlegter Kumpf und Maßstab, ähnliche Ansichten wie PHOTO-1000046420/6421 | abweichende Bytes und teils abweichender Ausschnitt; nur visuelle Korrespondenz, keine erwiesene Identität derselben Aufnahme/Teilinstanz |
| IMG_6802/6805/6806/6807/6813/6814 | zusätzliche aktuelle Rad-/Wellen-/Tragwerksperspektiven | nicht aus Ähnlichkeit als byteidentisch oder als neue unabhängige Messungen werten |

## Video

`evidence/raw/originaltransfer-20261010/IMG_6857.mp4`: 21,266667 s, 512 × 910 Pixel, 638 Videoframes laut FFprobe; Tonspur vorhanden, hier nicht transkribiert oder als Fachauskunft ausgewertet. Vollständiges technisches Decoding erfolgreich. Visuelle Stichproben bei 0 s (unterer Kranz/Tragwerk), 10 s (Wellenende/Tragwerk), 20 s (oberer Kranz/Kümpfe). Alle drei sind Ausschnitte derselben Quelle. Keine vollständige Bewegungsanalyse, kein metrischer Maßstab, keine neue Drehrichtungs- oder Bauzustandsfreigabe.

## Bestehende Dokument-/Aufnahmegruppen

Gruppen sind aus `data/source-analyses.json` übernommen, nicht neu entschieden.

| Gruppe | Quellen-IDs |
|---|---|
| `CAPTURE-01` | `SCAN-20261007-01-PLY`, `SCAN-20261007-01-GLB` |
| `DOC-BENDING-DIE` | `PHOTO-6836`, `PHOTO-6837` |
| `DOC-BOARD` | `PHOTO-6842`, `PHOTO-6843`, `PHOTO-6844` |
| `DOC-CIRCULAR-NOTES` | `PHOTO-6839` |
| `DOC-CONTACTSTRIPS` | `PHOTO-6833`, `PHOTO-6845` |
| `DOC-FASTENER-LIST` | `PHOTO-6824`, `PHOTO-6825` |
| `DOC-HOOPS` | `PHOTO-6846`, `PHOTO-6847` |
| `DOC-KUMPF-FIELD` | `PHOTO-6821` |
| `DOC-LAYOUT-OLD` | `PHOTO-6838`, `PHOTO-6840` |
| `DOC-MOUNT-OLD` | `PHOTO-6820` |
| `DOC-ORDER-NEW` | `PHOTO-6831` |
| `DOC-ORDER-OLD` | `PHOTO-6818`, `PHOTO-6819` |
| `DOC-POLYGON` | `PHOTO-6841` |
| `DOC-RIM-DETAILED` | `PHOTO-6848`, `PHOTO-6849`, `PHOTO-6850`, `PHOTO-6851`, `PHOTO-6852` |
| `DOC-RINNE` | `PHOTO-6830` |
| `DOC-SHAFT` | `PHOTO-6816`, `PHOTO-6817` |
| `DOC-STAVE-VARIANTS` | `PHOTO-6823` |
| `DOC-STOCK-TABLE` | `PHOTO-6827` |
| `DOC-TROUGH` | `PHOTO-6828`, `PHOTO-6829` |
| `TH-20261009-a-bock` | `PHOTO-TH-20261009-image-1791543487137`, `PHOTO-TH-20261009-image-1791543497527`, `PHOTO-TH-20261009-image-1791543505768`, `PHOTO-TH-20261009-image-1791543574540`, `PHOTO-TH-20261009-image-1791543757351` |
| `TH-20261009-arm-kruemmling` | `PHOTO-TH-20261009-image-1791540525839`, `PHOTO-TH-20261009-image-1791540649435`, `PHOTO-TH-20261009-image-1791540668918` |
| `TH-20261009-bock-radstadt` | `PHOTO-TH-20261009-image-1791543053651`, `PHOTO-TH-20261009-image-1791542327774`, `PHOTO-TH-20261009-image-1791542342950`, `PHOTO-TH-20261009-image-1791542237069`, `PHOTO-TH-20261009-image-1791542257101`, `PHOTO-TH-20261009-image-1791542108092`, `PHOTO-TH-20261009-image-1791542120355`, `PHOTO-TH-20261009-image-1791542146990`, `PHOTO-TH-20261009-image-1791542161221`, `PHOTO-TH-20261009-image-1791542172733` |
| `TH-20261009-dorn-lager` | `PHOTO-TH-20261009-image-1791541666129` |
| `TH-20261009-expert-construction` | `NARRATIVE-TH-CONSTRUCTION-20261009` |
| `TH-20261009-fluegelbretter` | `PHOTO-TH-20261009-image-1791541209669`, `PHOTO-TH-20261009-image-1791541224562`, `PHOTO-TH-20261009-image-1791541247032`, `PHOTO-TH-20261009-image-1791541265923`, `PHOTO-TH-20261009-image-1791541278244` |
| `TH-20261009-holzbaender` | `PHOTO-TH-20261009-image-1791541421696`, `PHOTO-TH-20261009-image-1791541435456`, `PHOTO-TH-20261009-image-1791541442395` |
| `TH-20261009-kumpf-einbau` | `PHOTO-TH-20261009-image-1791541735045`, `PHOTO-TH-20261009-image-1791541761724`, `PHOTO-TH-20261009-image-1791541781288`, `PHOTO-TH-20261009-image-1791541790124`, `PHOTO-TH-20261009-image-1791541863916` |
| `TH-20261009-kumpfnaegel` | `PHOTO-TH-20261009-image-1791542499680`, `PHOTO-TH-20261009-image-1791542573592`, `PHOTO-TH-20261009-image-1791542586169` |
| `TH-20261009-schetternbretter` | `PHOTO-TH-20261009-1000046540`, `PHOTO-TH-20261009-1000046539`, `PHOTO-TH-20261009-1000046538`, `PHOTO-TH-20261009-1000046537`, `PHOTO-TH-20261009-1000046536`, `PHOTO-TH-20261009-image-1791542766365`, `PHOTO-TH-20261009-image-1791542778932`, `PHOTO-TH-20261009-1000046530`, `PHOTO-TH-20261009-image-1791540812566`, `PHOTO-TH-20261009-image-1791540831514`, `PHOTO-TH-20261009-1000046542`, `PHOTO-TH-20261009-1000046541`, `PHOTO-TH-20261009-1000046535`, `PHOTO-TH-20261009-1000046534`, `PHOTO-TH-20261009-1000046533`, `PHOTO-TH-20261009-1000046532`, `PHOTO-TH-20261009-1000046531`, `PHOTO-TH-20261009-image-1791541084264` |
| `TH-20261009-trog-rinne` | `PHOTO-TH-20261009-image-1791542028869`, `PHOTO-TH-20261009-image-1791542045602`, `PHOTO-TH-20261009-image-1791541961389`, `PHOTO-TH-20261009-image-1791541967728`, `PHOTO-TH-20261009-image-1791541979278`, `PHOTO-TH-20261009-image-1791541887655`, `PHOTO-TH-20261009-image-1791541908195`, `PHOTO-TH-20261009-image-1791541920559` |
| `TH-20261009-welle-schellen` | `PHOTO-TH-20261009-image-1791541554648`, `PHOTO-TH-20261009-image-1791541561160`, `PHOTO-TH-20261009-image-1791541576861`, `PHOTO-TH-20261009-image-1791541641609` |
| `TH-KUMPF-REF` | `PHOTO-1000046420`, `PHOTO-1000046421`, `PHOTO-1000046422`, `PHOTO-1000046423`, `NARRATIVE-TH-KUMPF-20261008-01`, `NARRATIVE-TH-KUMPF-20261008-02`, `NARRATIVE-TH-KUMPF-20261008-03` |
| `TH-PADDLE-CORRECTION` | `NARRATIVE-TH-PADDLE-20261008-01` |

## Vollständige Transferzuordnung

Hashbeziehungen sind nachgewiesen; optische Ähnlichkeiten aus der Tabelle oben werden nicht als Hashgleichheit ausgegeben. SHA-256 und sämtliche byteidentischen Bestandspfade stehen in `audit-results.json → transfer_mapping` und `original-transfer-checksums.json`.

| Originaldatei (unter evidence/raw/originaltransfer-20261010/) | Vorhandene ID durch identische SHA-256 | Bytes |
|---|---|---:|
| `IMG_6790(1).jpeg` | `V2-IMG_6790` | 697816 |
| `IMG_6791.jpeg` | noch keine exakte Hash-Zuordnung | 685918 |
| `IMG_6792(1).jpeg` | `V2-IMG_6792` | 636432 |
| `IMG_6793(1).jpeg` | `V2-IMG_6793` | 643412 |
| `IMG_6794(1).jpeg` | `V2-IMG_6794` | 644026 |
| `IMG_6795(1).jpeg` | `V2-IMG_6795` | 661919 |
| `IMG_6796.jpeg` | noch keine exakte Hash-Zuordnung | 598740 |
| `IMG_6797(1).jpeg` | `V2-IMG_6797` | 591715 |
| `IMG_6798(1).jpeg` | `V2-IMG_6798` | 624476 |
| `IMG_6799(1).jpeg` | `V2-IMG_6799` | 644845 |
| `IMG_6800(1).jpeg` | `V2-IMG_6800` | 889040 |
| `IMG_6801(1).jpeg` | `V2-IMG_6801` | 867812 |
| `IMG_6802.jpeg` | noch keine exakte Hash-Zuordnung | 866050 |
| `IMG_6803(2).jpeg` | `V2-IMG_6803`, `V2-IMG_6803-upload2` | 881427 |
| `IMG_6804(1).jpeg` | `V2-IMG_6804` | 903302 |
| `IMG_6805.jpeg` | noch keine exakte Hash-Zuordnung | 859804 |
| `IMG_6806.jpeg` | noch keine exakte Hash-Zuordnung | 869284 |
| `IMG_6807.jpeg` | noch keine exakte Hash-Zuordnung | 759888 |
| `IMG_6808(2).jpeg` | `V2-IMG_6808-upload2` | 791892 |
| `IMG_6809(1).jpeg` | `V2-IMG_6809` | 678661 |
| `IMG_6810(1).jpeg` | `V2-IMG_6810` | 734269 |
| `IMG_6811(1).jpeg` | `V2-IMG_6811` | 816407 |
| `IMG_6812(1).jpeg` | `V2-IMG_6812` | 559161 |
| `IMG_6813.jpeg` | noch keine exakte Hash-Zuordnung | 907396 |
| `IMG_6814.jpeg` | noch keine exakte Hash-Zuordnung | 900586 |
| `IMG_6815.jpeg` | noch keine exakte Hash-Zuordnung | 578685 |
| `IMG_6816(1).jpeg` | `PHOTO-6816` | 583092 |
| `IMG_6817(1).jpeg` | `PHOTO-6817` | 585855 |
| `IMG_6818(1).jpeg` | `PHOTO-6818` | 692267 |
| `IMG_6819(1).jpeg` | `PHOTO-6819` | 643786 |
| `IMG_6820(1).jpeg` | `PHOTO-6820` | 664801 |
| `IMG_6821(1).jpeg` | `PHOTO-6821` | 652049 |
| `IMG_6822(1).jpeg` | `V2-IMG_6822` | 1017003 |
| `IMG_6823(1).jpeg` | `PHOTO-6823` | 569999 |
| `IMG_6824(1).jpeg` | `PHOTO-6824` | 756961 |
| `IMG_6825(1).jpeg` | `PHOTO-6825` | 751485 |
| `IMG_6826.jpeg` | noch keine exakte Hash-Zuordnung | 592262 |
| `IMG_6827(1).jpeg` | `PHOTO-6827` | 579107 |
| `IMG_6828(1).jpeg` | `PHOTO-6828` | 336665 |
| `IMG_6829(1).jpeg` | `PHOTO-6829` | 340602 |
| `IMG_6829(2).jpeg` | `PHOTO-6829` | 340602 |
| `IMG_6830(1).jpeg` | `PHOTO-6830` | 604678 |
| `IMG_6831(1).jpeg` | `PHOTO-6831` | 642742 |
| `IMG_6832(1).jpeg` | `V2-IMG_6832` | 973243 |
| `IMG_6833(1).jpeg` | `PHOTO-6833` | 632468 |
| `IMG_6834.jpeg` | noch keine exakte Hash-Zuordnung | 594499 |
| `IMG_6835.jpeg` | noch keine exakte Hash-Zuordnung | 577437 |
| `IMG_6836(1).jpeg` | `PHOTO-6836` | 653769 |
| `IMG_6837(1).jpeg` | `PHOTO-6837` | 666758 |
| `IMG_6838(1).jpeg` | `PHOTO-6838` | 671013 |
| `IMG_6838(2).jpeg` | `PHOTO-6838` | 671013 |
| `IMG_6839(1).jpeg` | `PHOTO-6839` | 520541 |
| `IMG_6840(1).jpeg` | `PHOTO-6840` | 577720 |
| `IMG_6841(1).jpeg` | `PHOTO-6841` | 570465 |
| `IMG_6842(1).jpeg` | `PHOTO-6842` | 578855 |
| `IMG_6843(1).jpeg` | `PHOTO-6843` | 564636 |
| `IMG_6844(1).jpeg` | `PHOTO-6844` | 572183 |
| `IMG_6845(1).jpeg` | `PHOTO-6845` | 757953 |
| `IMG_6846(1).jpeg` | `PHOTO-6846` | 670869 |
| `IMG_6847(1).jpeg` | `PHOTO-6847` | 698290 |
| `IMG_6848(2).jpeg` | `PHOTO-6848` | 750020 |
| `IMG_6849(1).jpeg` | `PHOTO-6849` | 745533 |
| `IMG_6850(1).jpeg` | `PHOTO-6850` | 660844 |
| `IMG_6851(2).jpeg` | `PHOTO-6851` | 666537 |
| `IMG_6852(2).jpeg` | `PHOTO-6852` | 680615 |
| `IMG_6853(4).jpeg` | `PHOTO-6853` | 896233 |
| `IMG_6854(2).jpeg` | `PHOTO-6854` | 532942 |
| `IMG_6855(2).jpeg` | `PHOTO-6855` | 794918 |
| `IMG_6856(2).jpeg` | `PHOTO-6856` | 819887 |
| `IMG_6858(2).jpeg` | `PHOTO-6858` | 730724 |
| `IMG_6859(2).jpeg` | `PHOTO-6859` | 728900 |
| `IMG_6860(2).jpeg` | `PHOTO-6860` | 723424 |
| `IMG_6861(2).jpeg` | `PHOTO-6861` | 788482 |
| `a6c861c8-05ce-4a8f-aa8a-636ffd464f11.jpeg` | noch keine exakte Hash-Zuordnung | 435898 |
| `da76dde4-72ef-442c-b7e8-3feac8f39255.jpeg` | noch keine exakte Hash-Zuordnung | 467251 |
| `09bf54b5-ebe2-43f7-badc-310aee910605.jpeg` | noch keine exakte Hash-Zuordnung | 448966 |
| `IMG_6857.mp4` | noch keine exakte Hash-Zuordnung | 13408295 |

Die vollständige Rohdateiliste samt Hashgruppen und alle Archivprüfungen sind im maschinenlesbaren Audit enthalten. Keine Originale wurden dedupliziert oder neu kodiert.
