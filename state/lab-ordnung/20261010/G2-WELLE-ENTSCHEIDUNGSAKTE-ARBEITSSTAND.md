# G2 – Thorstens Entscheidungsakte Welle (Arbeitsstand)

Stand: 2026-10-10. **Entscheidungsvorbereitung, keine Fachentscheidung.** Gegenstand `COMP-SHAFT`. Alle Schlussfolgerungen zur Bauweise und zu Maßen bleiben Thorsten vorbehalten.

## Frage A: Was ist die Wellenkonstruktion im realen Bestand?

| Aussage | Grundlage | Reichweite und Grenze |
|---|---|---|
| `CLAIM-0001`: historische Längsmaßzahl **370** | `PHOTO-6816`, `PHOTO-6817`, Region linke Längsmaßlinie | `unit:null`, `scope:documented-design`, `as_built_eligible:false`; nicht als Ist-Länge lesen |
| `CLAIM-0002`: historische Quermaßzahl **37** | dieselben zwei Fotos desselben Blattes, oberes Quermaß | Einheit ungesichert, keine unabhängige Messung |
| `CLAIM-0007`: zwei gezeichnete Schlitzgruppen | Längsansicht derselben Zeichnung | historische Darstellung, keine aktuelle verdeckte Geometrie |
| `CLAIM-0008`: drei gezeichnete gekreuzte Armdurchtritte pro Gruppe | schematischer Querschnitt | Loch-/Keilkontur nicht maßhaltig belegt |
| `CLAIM-0253`: verwitterte Wellenoberfläche | `PHOTO-6853`, Bildmitte | fotografierte Topologie, keine kalibrierte Messung |
| `TH-20261009-13`: gleichbleibender hölzerner Wellenquerschnitt laut Fachauskunft | `NARRATIVE-TH-CONSTRUCTION-20261009` und vier zugeordnete Fotos | `expert-intake-pending-property-review`; exakte Querschnittskontur und -maße offen |
| `TH-20261009-14`: zwei Eisenklammern pro Ende laut Fachauskunft | dieselbe Fachauskunft und zugeordnete Fotos | keine zusätzliche metrische Bestätigung |
| `CLAIM-0336`: innere Durchtritts-/Mortisengeometrie unbekannt | `CTX-USER-20261007` | offener Nachweis, nicht automatisch ein Widerspruch |

`PHOTO-6816` und `PHOTO-6817` sind laut `data/source-analyses.json` zwei Fotografien **desselben Blatts** (`DOC-SHAFT`), also nicht zwei unabhängige Quellen.

## Frage B: Sind die divergierenden Wellenmaße überhaupt vergleichbar?

`CLAIM-0346` markiert den Konflikt »370/37 shaft sketch vs generic stock 4.50 m/50 cm, installation 40 cm«, referenziert `PHOTO-6816` und `PHOTO-6827`. Die Quellenanalyse für `PHOTO-6827` kennzeichnet ausdrücklich eine **allgemeine Beschaffungs-/Empfehlungstabelle**, keine Ist-Stückliste dieses Rades. **Prüfverdacht:** möglicherweise vermischte Gegenstände/Geltungsbereiche, nicht zwingend zwei widersprechende Messungen. Thorsten muss den Vergleich beurteilen; Konflikt nicht eigenmächtig auflösen.

## Zielmodell und fehlende Evidenz

`data/reconstruction-constraints.json:shaft` enthält u.a. `constantWoodSection:true`, `clampsPerEnd:2`, aber auch Kandidaten für Kontur, Klammermaße und Zapfen. `asBuilt:false`. Das begrenzte Mapping `src/control/property-readiness.mjs` bildet die oben genannten Wellenclaims nicht explizit auf Modellparameter ab. **Keine Modellfreigabe**.

Bestehende Untersuchung `GAP-02`: Einstecktiefen, Keilrichtung, Armfolge und Mortisen beim Lösen dokumentieren; `GAP-06`: Lagerzentren, Zapfen und Auflager vor der Wellenanhebung erfassen. Bestehende `TASK-ARM-BEFORE` und verwandte Feldaufgaben für die genaue Ausführung prüfen.

## Thorsten vorzulegende Entscheidungen (nicht vorwegnehmen)

1. Bezieht sich die Skizze `PHOTO-6816/6817` auf die ausgeführte Welle, einen Entwurf oder eine Variante? Welche Einheiten und Endpunkte sind fachlich belegbar?
2. Sind die Angaben in `PHOTO-6827` überhaupt vergleichbar, oder ist `CLAIM-0346` als Gegenstands-/Geltungsbereichsproblem zu klassifizieren?
3. Welche Eigenschaften der aktuellen Welle sind anhand der Fotos und bisherigen Fachauskunft bestätigt; welche benötigen zusätzliche Ansichten oder Messungen?
4. Welche konkreten Approximationen in `shaft` dürfen für eine **anschauliche** Modellvariante verwendet werden, und welche bleiben für technische Zeichnung/Fertigung gesperrt?
5. Welche Demontagebeobachtung würde konkurrierende Hypothesen tatsächlich unterscheiden?

Zulässige Antwort je Frage: bestätigen, einschränken, korrigieren, widersprechen, nicht entscheidbar, weitere Aufnahme verlangen. Originalantwort, Zeitpunkt, Bezug und Geltungsgrenze festhalten.

## Originalprüfung – klare Grenze

`PHOTO-6816`, `PHOTO-6817`, `PHOTO-6827` sind als Bilddateien im Gespräch verfügbar; die obigen Befunde wurden **aus den kanonischen JSON-Quellenanalysen und Claims** extrahiert, nicht durch eine in dieser Arbeitssession dokumentierte erneute Pixelprüfung oder SHA-256-Verifikation der GitHub-Originalbytes. Diese Prüfung ist vor einer fachlichen Entscheidungsübergabe ausdrücklich nachzuholen. `PHOTO-6853` und die vier TH-Fotos wurden hier nicht als Originaldateien erneut geprüft. Keine Vollständigkeit der Belegmappe behaupten.

## Keine Änderung

Alle 39 Fachkorrekturen, F02/F03, Claims, Originale, Modelle und lokalen Aufnahmen bleiben unverändert. Keine Entscheidung im Namen Thorstens.
