# Schäferrad — ein gemeinsamer Einstieg ins Wissenslabor

**Visuelle Referenzbasis, lesender Prototyp zur Review.** Einstieg: `index.html`, ohne Server oder neue Produktinstallation. Die gleiche Ansicht wird direkt im Gespräch gezeigt. Keine Veröffentlichung, keine produktive Route, keine kanonische Datenänderung.

Die aktuelle Nutzerfreigabe führt den bisherigen Reviewstand in eine verständliche Laboransicht weiter. Baseline ist `f2bf574c6c6fed3a64ac0073823cd07ac24ee537`. Originalbilder, 39 Fachkorrekturen, F02/F03, Geometrie und sämtliche vorherigen Dateien bleiben unverändert.

## Ein Arbeitsstand

`project-snapshot.json` hält die sieben offenen PRs und ihre tatsächliche Git-Abstammung fest. Der aktuelle Leseausgangspunkt umfasst die Köpfe von PR #18, #19 und #20. Die anderen vier PR-Köpfe sind nicht vollständig Vorfahren dieses Stands; daraus folgt weder, dass ihre Inhalte fehlen, noch dass sie weggeworfen werden dürfen. Sie bleiben unberührt. Es wurde kein neuer PR eröffnet, kein alter geschlossen und keine Zusammenführung vorgenommen. Die Anzeige der Referenzbasis erfordert keine Aufarbeitung dieser historischen Zweige durch den Nutzer.

## Lesende Projektion

- Radübersicht → drei Bereiche → 38 bestehende Referenzaussagen → Belege / Ableitung → offene Untersuchungen.
- 34 Gegenstände aus dem bestehenden Register, mit deutschen Typbezeichnungen. Armzone, Teilfamilie und reales Teil bleiben unterscheidbar. Kein neues Ontologieschema.
- Belegpfade aus der tatsächlichen Claim-Provenienz; abgeleitete Maße verlinken zurück auf ihre Grundlagen. Keine Zahl unabhängiger Belege aus Fotoanzahlen.
- Konflikt CLAIM-0347 bleibt erhalten, seine spätere semantische Auflösung wird sichtbar gemacht.
- Modellstellen und Aufgaben sind auf **Bereichsebene** aus den drei geprüften Referenzfällen übernommen. Keine erfundene direkte Zuordnung jeder Frage oder Modelldatei zu jedem Claim.
- Quellen- und Registerlinks sind auf den unveränderlichen Basiscommit fixiert. Verkleinerte Originalansichten sind eingebettet; keine neue Interpretation durch Bildbearbeitung.
- Deutsche Beschriftungen sind reine Darstellung. Originalwerte, IDs, Geltungsbereiche und Status werden nicht zurückgeschrieben. Keine Scores, pauschalen Bauteilampeln oder Freigaben.

## Reproduktion und Prüfgrenzen

`python lab/wissenslandkarte/build.py` erzeugt deterministisch `index.html` und `preview.html` aus `view.html` und dem vorhandenen Datenbestand. Python benötigt Pillow. Keine neuen Produktionsabhängigkeiten.

`NODE_PATH=<jsdom-Installation>/node_modules node lab/wissenslandkarte/check-dom.cjs` prüft alle 38 Auswahlen, Ableitungsnavigation, unbekannte Einheit, historischen Konflikt, Begriffsregister und Bestandsschutz. DOM-Prüfung mit jsdom 26.1.0 bestanden, siehe `validation.json`.

`check.cjs` enthält zusätzlich die vorbereitete Browserprüfung für Desktop und Smartphone. **Diese Prüfung konnte hier wegen verweigerter Socket-Erstellung des Browsers nicht laufen.** Es gibt keine behauptete visuelle Browserabnahme und keine erzeugten Screenshots. Die Darstellung ist zur direkten Durchsicht bereit; die Responsive-CSS-Regeln sind noch kein visueller Abnahmenachweis.

Tonspur und Identität der drei Kontextbilder bleiben dokumentierte Grenzen der Referenzbasis. Keine erneute Dateianforderung. Nach Sicherung und Vorlage wird am Review-Gate gestoppt.
