# Reproduzieren

Dieser Audit-PR basiert ausschließlich auf main. Zur Prüfung **separaten Checkout von 6999e93146d2dc62337f60e9f72e8e84da2619e0** anlegen und nur diesen Auditordner hineinkopieren. Keine Quellenänderung erforderlich. Auditproben schreiben ausschließlich ihre Ergebnisdateien in diesen Ordner. Node 24.19.0 wurde verwendet.

```sh
npm ci --ignore-scripts --no-audit --no-fund
node --test tests/*.test.mjs
node state/reconstruction-loop/ITER-003/independent-audit/probe.mjs
python state/reconstruction-loop/ITER-003/independent-audit/canonical.py
npm run build
```

Erwartung: 35 bestandene Tests, 48 reale Nagel-Mittellinien mit Kranztreffern, vollständiger Build scheitert in `projection.mjs:11`. Der Vergleichscommit f7b9185 muss für canonical.py im Git-Objektspeicher liegen. Ausgangsdateien nicht durch die ursprünglichen Export-/Render-/Reconcile-Skripte überschreiben.

Optionaler isolierter Bundle-Nachweis, **kein Ersatz für den Produktionsbuild**:

```sh
./node_modules/.bin/astro build
```

Die Bauschritte können generierte lokale Dateien erzeugen. In separatem Checkout laufen lassen; keine dieser Änderungen in den Audit-PR übernehmen. Kein Deploy-Befehl ist erforderlich.

`probe.mjs` lädt beide unveränderten GLBs, prüft IDs, Positionsattribute, Meshindizes und Welttransformationen nach Aufhebung der Y-up-Exportrotation. Drahtgitter-Paddles im Truth-GLB sind Linien; Dreiecksindizes und Linienindizes werden deshalb nicht gleichgesetzt. Kein externer glTF-Schemavalidator, kein Textur-/Animationstest und keine neue Meshrekonstruktion.

Die Nagelprobe folgt dem wirklichen transformierten Start-Ende-Segment. Eine Mittellinienpenetration belegt ungeschnittenes Material; ein freier Mittellinienstrahl beweist umgekehrt keine Volumenfreiheit. Diese Asymmetrie gilt auch für Band-/Armsitzproben. Keine Festigkeitsrechnung.

`canonical.py` kontrolliert alle 39 Intake-Werte, Provenienz und Komponenten-/Graph-/Analysebezüge, Hashes der 65 Thorsten-Fotos und neu hinzugekommene nichtleere Ist-Wertfelder in den drei benannten Dateien. Kein pauschaler Beweis über alle möglichen Eigenschaften des gesamten Repositorys.

Die Sichtprotokolle sind menschlich lesbare Prüfbeobachtungen sämtlicher 39 Ansichten. Ein erneuter Pixelrender wurde bewusst nicht erzeugt. Input- und Bildhashes verknüpfen das Protokoll mit den archivierten Dateien.
