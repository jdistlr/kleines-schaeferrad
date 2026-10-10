# ITER-003 Truth Critic & Integration Readiness Audit

**Entscheidung: NO-GO für Integration von Commit 6999e93 in main.**

**Gate: ITER-003 INTEGRATION REVIEW READY**

Prüfdatum: 09.10.2026, Benutzerzeit Europe/Berlin. Die Ausführungsumgebung meldet abweichende UTC-Zeit; Laufzeitlogs behalten ihre Originalzeit. Unabhängige Prüfung der Implementierung, nicht Übernahme ihres Self-Audits. Kein neues Modell, keine produktive UX-Änderung, kein Merge, kein Deployment. Astro ist gemäß Nutzerhinweis keine Architekturvorgabe; die Abnahmekriterien sind technologieoffen.

## Eingefrorene Grundlage

- Repository: `jdistlr/kleines-schaeferrad`
- Prüfling: `work/astra-korrektur-iter003-20261009`, **6999e93146d2dc62337f60e9f72e8e84da2619e0**
- main: **f7b9185517856b7881530ba9d0553f170787cb09** (zwei Commits hinter Prüfling, gemeinsamer Ausgangspunkt).
- [Alle geprüften Quelldateien am unveränderlichen Commit](https://github.com/jdistlr/kleines-schaeferrad/tree/6999e93146d2dc62337f60e9f72e8e84da2619e0).
- Dieser Audit-PR enthält ausschließlich Auditdateien auf main. Die Korrekturimplementierung wird dadurch weder integriert noch freigegeben. Relative Pfade außerhalb dieses Auditordners bezeichnen den oben fixierten Prüfling.

## Entscheidung und Befunde

### F01 — P1 / Integrationsblocker: vollständiger Pages-Build bricht ab

`npm ci --ignore-scripts --no-audit --no-fund` erfolgreich, Node **v24.19.0**. Der tatsächliche Pipelinebefehl `npm run build` endet mit Exit 1 bereits in `prepare:workbench`:

```
RangeError: Maximum call stack size exceeded
src/workbench/projection.mjs:11:203
scripts/build-workbench.mjs:29:309
```

Ursache: `Math.min(...xs)` / `Math.max(...xs)` für die große projizierte Kantenliste. Das ist eigener JavaScript-Zeichnungscode, kein Astro-Frameworkfehler. Der separate Aufruf `astro build` funktioniert und enthält ITER-003 im Viewer-Bundle, umgeht jedoch Zeichnungs-/Feld-/Offline-Vorbereitung. Der erfolgreiche Astro-only-Build im Eigenbericht ist kein Nachweis eines funktionierenden GitHub-Pages-Builds. Siehe `build.txt` und `astro-only-build.txt`. Keine Behebung im Audit.

**Abnahme:** vollständigen tatsächlich eingesetzten Build einschließlich benötigter Folgeartefakte erfolgreich aus sauberem Checkout ausführen; Framework frei wählbar. Kein bloßer Teilbuild als Ersatznachweis.

### F02 — P1 / mechanisch unvollständig: 48 Kumpfnagelpfade durch Kranzmaterial

Alle **48/48 tatsächlichen Start-Ende-Mittellinien** schneiden Kranzdreiecke. Die unabhängige Probe folgt jedem transformierten Nagel, statt nur die im vorhandenen Audit benutzte axiale Linie am Endpunkt zu prüfen. Der alte Endpunkt-Proxy wurde zusätzlich mit 48/48 reproduziert. Beispiel `V3-KUM-01-NAIL-LONG`: Modelllänge 0,724875 m; erster Kranztreffer bei x≈−1,040 m. Diese Modelllänge ist ausdrücklich kein Ist-Maß.

Truth enthält keine Nagelpfade; Brute enthält 48 synthetische Pfade. Die Randbedingungen 26 mm Schaft / 40 mm Kopf sind Fachangaben, keine Begründung für den übrigen Pfad. 24 Kümpfe und 48 Nägel sind Modellwiederholungen, keine vollständig beobachtete physische Inventur. Die ebenfalls vorhandenen **48 Schetternnägel** sind eine andere Verbindungsfamilie und bestehen die vorhandene Durchgangsachsenprüfung.

**Abnahme:** reale Partnerflächen, Kranzbohrungen, Krümmungen und Einbauzuordnung erfassen; Anschlüsse anschließend separat korrigieren und volumetrisch prüfen. Bis dahin klar unfertiger Kandidat, keine mechanische Freigabe. Ein vollständiger Drehzyklus oder statischer Nachweis wurde weder vom Eigenbericht noch diesem Audit erbracht.

### F03 — P1 für Konstruktionsfreigabe / stationäre Auflager und Klemmungen offen

Radbock, A-Bock, Trog und unterer Rahmen enthalten unregistrierte Standort-/Höhenannahmen. Expertentopologie ist vorhanden; daraus folgt kein bestätigter Lastpfad. Rundes Schellenprofil um achteckige Welle, Dornspiel und Innenverankerung bleiben Kandidaten. Beim A-Bock liegen obere/untere Sicherungskörper jeweils etwa **2 mm vom Riegel entfernt** (Mesh-Bounds): geometrisch keine geschlossene Klemmung. Die Körper sind rechteckige Balken, keine nachgewiesenen Keilpassungen.

Die 0,80 m werden zwischen Rinnenunterkante z=1,262 m und synthetischem Datum z=0,462 m gesetzt. Die geneigten, nicht bodengerecht zugeschnittenen Füße reichen bis z≈0,447446 m, also ca. **14,6 mm unter dieses Datum**. Daher weder tatsächlicher Bodenbezug noch gemessene Beinlänge. Der Umfang dieser Probe ist in `probe.json` dokumentiert; Bounding-Box-Abstände belegen diese Trennungen, nicht alle Kontaktflächen der Anlage.

**Abnahme:** lokale Datumsdefinition, Fußflächen, Auflager-/Partnerkontakte und Keilwirkung explizit verifizieren. Fachlich belegte Form, synthetische Lage und tatsächliche Messwerte getrennt halten. Kein neuer Messwert oder neue Geometrie in diesem Audit.

### F04 — P2 / kanonische Abhängigkeiten nicht vollständig konsistent

39/39 Fachwerte stimmen mit dem ursprünglichen Intake überein; 39/39 Claims mit auflösbarer Provenienz und Komponentenverknüpfung; keine dangling Graph-Endpunkte; keine neu promovierten `current_value`/Ist-Werte in den geprüften Datensätzen. Alle **65/65** Thorsten-Originalfotos stimmen mit den Manifest-Prüfsummen überein.

Aber **TH-25 bis TH-29 fehlen in den `claim_ids` der `source-analyses`-Einträge**. Die Claims selbst haben Provenienz; betroffen ist der Rückverweis, nicht Verlust der Expertenaussage. Die Komponenten-Notiz zu `COMP-PADDLES` erklärt den geometrischen Bezugsbegriff weiter als ungeklärt, obwohl EDGE-021/CONFLICT-13 ihn bereits auf die Kranzebene auflösen. `COMP-PADDLES` heißt noch „Schaufeln / Schetter“, parallel zur jetzt separaten Familie Schetternbretter. RADSTATT und RADSTADT existieren als getrennte Knoten; keine defekte Referenz, aber Alias-/Identitätsregel prüfen. Historische Gegenbelege wurden bewahrt.

**Abnahme:** Rückverweise 25–29 und widersprechende Status-/Terminologietexte konsolidieren; Radstatt/Radstadt-Identität ausdrücklich regeln. Keinesfalls Expertenangaben zu Feldmessungen hochstufen.

### F05 — P2 / ausgelieferte Ansichten und Provenienz driften

`src/pages/werkstatt.astro` nennt Brute weiter ITER-001. `scripts/build-workbench.mjs` schreibt ITER-001 in Revisionsfußzeile und Projektionsdatensatz, obwohl `makeModel()` ITER-003 erzeugt. Das Lagerdetail KS-50 filtert weiter `HYP-BEARING--1`, `CTX-BEARING-STAND--1`, `CAND-JOURNAL--1`; diese IDs wurden entfernt, Auswahl ist leer. Der Produktionsbuild scheitert zuvor; dies ist ein belegter latenter Zeichnungsfehler, keine Behauptung über einen erfolgreich neu erzeugten Feldsatz.

Die 39 archivierten Auditansichten sind vollständig vorhanden. Ansicht 10 zeigt nach Segmentphasenänderung den Armsitz statt den namensgebenden Stoß; Fußnote und D1 machen das nachvollziehbar. Truth-Ansicht 13 ist absichtlich leer, da stationäre Geometrie ausgeschlossen wird. Das sind dokumentierte Einschränkungen, keine fehlenden Bilddateien.

**Abnahme:** funktionierende Bauteilselektion sowie zutreffende Iterations-/Quellenprovenienz für alle tatsächlich ausgelieferten Artefakte. Das erfordert keine neue UX-Designrichtung.

## Was bestanden hat

- **35/35 vorhandene Tests** erneut bestanden; sie decken den vollständigen Produktionsbuild nicht ab.
- GLB Truth: **296 Geometrieobjekte**, Brute: **945**. Beide GLBs unabhängig geladen und mit neu instanziierter Runtime verglichen: Positionsattribute identisch, Transformationsfehler nach Y-up-Rücktransformation ≤6,2×10⁻¹⁶, keine ID-/Indexabweichung bei Meshes. Truth exportiert drei Drahtgitterbretter als Linien; berücksichtigt, kein fehlender Export.
- Alle sechs dokumentierten Eingangsdatei-Hashes stimmen. **39/39 Bildprüfsummen** stimmen.
- 12 Armsitzstift-Mittellinien frei durch die Armöffnungen; 96 U-Bandschenkel-Mittellinien frei durch Kranzöffnungen. Das beweist keine vollständige Volumenfreiheit oder Klemmwirkung. Schetternzahl und gegenläufige Durchgangsachsen durch bestehende Tests bestätigt.
- Meshmaßkette 1,80 m lichte Weite + 2×0,14 m Breite = 2,08 m Außenweite; Mittelebenen 1,94 m. Mathematisch/technisch korrekt, weiterhin Expertenmaßkette ohne unabhängiges Ist-Aufmaß.
- Truth: keine stationären Teile, keine exakten Kumpfnagelpfade; `installedMetric` bleibt null, kein `asBuilt=true`.

## Verwendet GitHub Pages die aktualisierte Geometrie?

**Live: nein.** Erfolgreicher Build und Deploy [Run 37943980335](https://github.com/jdistlr/kleines-schaeferrad/actions/runs/37943980335) gehören zu main `f7b9185`, nicht `6999e93`. Direkt geladene Live-Werkstatt und ihr JS-Bundle enthalten weder ITER-003 noch die neuen Schettern-/A-Bockkennungen (`live-pages.json`). Dieser HTTP-Befund gilt für die direkt abgerufenen Serverdateien; bereits installierte Offline-Caches wurden nicht untersucht.

**Prüfbranch, Viewer-Code: ja.** `viewer.js → makeModel → calibrateModel → applyExpertCorrections`; der separate Astro-Bundlelauf enthält `ITER-003`, `TH-SCHETTER-`, `TH-BAND-`, `TH-A-CROSSBAR`, `TH-SEAT-`. Die GLBs in `state/.../models` sind Auditexporte, nicht die Datenquelle des interaktiven Viewers. Der GLTFLoader im Viewer lädt den Scan. Die vollständige Produktionspipeline kann den neuen Stand wegen F01 derzeit nicht ausliefern.

## Evidenzklassen und Grenzen

1. **Bestätigte Fachkonstruktion:** Aussagen des lokalen Fachkenners und sichtbare Topologie, etwa Schettern, U-Bänder, konstante Holzwelle, vier Schellen und zweigeteilte Rinne. Bestätigung betrifft den angegebenen Sachverhalt, nicht sämtliche synthetischen Ausführungsdetails.
2. **Tatsächliche Ist-Maße:** keine neue unabhängige Feldmessung in ITER-003 oder diesem Audit. Fotos mit verdeckten Endpunkten bleiben begrenzt; kein Zollstockbild wird global pixelmetrisch umgedeutet.
3. **Synthetische Modellannahmen:** Bohrbilder, Keilformen, Überstände, Standort, Neigungen, Zwischenräume, Innenverbindungen, Wasserparameter und Darstellungsmaße. Auch im Truth-Display brauchen sie eindeutige Qualifizierung.

30 angehängte historische/Kontextbilder wurden als Übersichten geöffnet; die zuvor gemeldeten Pfadfehler bestanden im tatsächlichen Arbeitslauf nicht mehr. Thorstens Quellenkontaktblätter wurden im Zusammenhang mit der Implementierung gesichtet; alle 65 Originale hashgeprüft, nicht jedes Original neu metrisch ausgemessen. Siehe `attachments.json`, `canonical.json`, `CLAIMS-39.md`, `VIEWS-39.md`, `probe.json`. Keine neu erfundenen physischen Instanzen. Kein Vollzyklus-, Festigkeits-, Montage- oder Demontagesicherheitsnachweis.

## Nächste Freigabe

NO-GO gilt für die jetzige Integration, nicht für die Bewahrung der wertvollen Fachkorrekturen. Zuerst F01 beheben und den vollständigen Zielbuild nachweisen; F04/F05 konsolidieren. F02/F03 separat als mechanisch offene Arbeit abnehmen oder ausdrücklich in einer auf Forschung beschränkten Folgefreigabe ausschließen. Ein CONDITIONAL GO wäre erst nach geschlossenen Software-/Provenienzblockern und ausdrücklich akzeptierter Begrenzung auf nicht montagefähige Kandidaten vertretbar. Der aktuelle Audit erteilt diese Folgefreigabe nicht.

Audit abgeschlossen am Gate **ITER-003 INTEGRATION REVIEW READY**. Kein automatischer Folgeschritt.
