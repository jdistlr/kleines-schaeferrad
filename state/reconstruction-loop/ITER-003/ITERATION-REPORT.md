# ITER-003 – Fachkorrekturen in kanonischen Abhängigkeiten und Geometrie

Status: CALIBRATION ITERATION READY FOR TRUTH CRITIC

Repository: jdistlr/kleines-schaeferrad. Branch: work/astra-korrektur-iter003-20261009.
Ausgangspunkt: vollständiger Vergleich ITER-002, Commit 6017ba310d4a91158fe5f3d6edc8eb1bf3f5b6b5, auf PR-13-Merge f7b9185517856b7881530ba9d0553f170787cb09.
Die anschließende Nutzerfreigabe erlaubt Modell- und kanonische Korrekturen. Kein Merge, kein Deployment.

## Evidenz und Kanon

65 Originalfotos und 39 Fachangaben aus PR 13 sind über Manifest, source-analyses, geometry.claims, Komponenten und assembly.graph angebunden. Der visuelle Quellenabgleich, Fotoablesungen einschließlich Unsicherheiten und Scanprüfung bleiben unverändert in ITER-002 erhalten. Diese Iteration setzt dessen Befunde um; sie behauptet keine neue unabhängige Messung. Historische Aussagen werden nicht gelöscht. Maßangaben des Experten sind von Feldmessungen getrennt; current_value/installedMetric bleiben unbekannt.

Die 39 Einzelfälle stehen in CLAIM-IMPLEMENTATION.md und MODEL-DELTA.json. Der Bezugsfehler „90°“ ist auf die Kranzebene aufgelöst; daraus folgt kein gesicherter radialer Pitch. Schettern, U-Holzbänder, Kumpfnägel und Armsitzkeile sind getrennte Verbindungen. Radstadt bedeutet Gesamtrahmen; die lokale Bocksymmetrie bestimmt keine globale Standortgeometrie.

## Tatsächlich geänderte Geometrie

- Kränze: 1.80 m lichte Weite, .14 m axiale Breite, 1.94 m Mittelebenen, 2.08 m Außenweite; alle Werte an Geometriegrenzen geprüft.
- Arme: .14/.065 m Querschnitt, Enden in verstärkten Segmentmitten; Durchstecköffnungen, zwei obere Keile und hinterer Stift. Achszuordnung und Sitzdetails bleiben Kandidaten.
- Kranzstöße: 24 Schetternbretter, 48 gegenläufig angeordnete Nägel mit tatsächlichen Durchgangslöchern; genaue Abmessungen/Lochbilder sind Kandidaten.
- Flügelbretter: etwa .35 m breit, 2.22 m synthetische Gesamtspanne einschließlich .07 m Überstand je Außenfläche. Landseitige Abschrägung und U-Holzbänder mit Kranzdurchführungen ergänzt. Rohastmaß und fertiger Querschnitt bleiben getrennt.
- Welle: konstanter Holzquerschnitt, vier Schellen. Brute zeigt separate Dorne im Holzlager; Durchmesser und Spiel bleiben Kandidaten.
- Kumpfnägel: .026 m Schaft, .04 m Kopf, poseabhängige Pfade zur korrigierten Kranzlage. Kopf-/Bogenlänge und Kranzbohrungen bleiben offen.
- Radbock: 1.20 m oberer Balken, .14 m Holzquerschnitt, abgesetzte/verkeilte Pfosten. Unterbau bleibt als synthetischer Standortkontext erhalten.
- Rinne: zwei Abschnitte, Stoß über A-Bock; .90 m Riegel, .04/.14 m Querschnitt, .05 m Schlitz, .14 m Beine, .80 m Unterkante über lokalem Boden. Beinlänge, Neigung, Schlitzhöhe und Standort sind Anzeigeannahmen.

## Truth / Brute

Truth enthält fachlich belegte Topologie und markierte historische bzw. expertenbasierte Darstellung, ohne behauptete Ist-Metrik. Unregistrierte stationäre Einbaupositionen und genaue Nagelpfade bleiben ausgespart. Sichtbare Details benötigen dennoch explizite Anzeigemaße; diese sind keine bestätigten Truth-Messwerte. Brute ergänzt Standort, Lager, Bock und Rinne mit qualifizierten Kandidaten. Keine physische Instanz wurde erfunden oder als beobachtet registriert.

## Prüfung und Grenzen

32 kanonische Ansichten (16 je Modell) verwenden unveränderte Kameradefinitionen; 7 ergänzende Detailkameras dokumentieren neue Verbindungen. Renderdaten stammen aus den tatsächlichen Runtime-Dreiecken mit Tiefenpuffer. Vergleichskamera 10 zeigt durch die korrigierte Segmentphase nun den Armsitz; D1 zeigt den versetzten Stoß.

Tests prüfen Geometriegrenzen, echte Arm-/Schetterdurchgänge, Nagelpfade bei veränderter Pose, Wellenquerschnitt, Bauteilzahlen und fehlende Ist-Promotion. Der Webseiten-Build wurde separat geprüft, ohne Deployment. Historische veröffentlichte Feld-PDFs wurden nicht als neue Prüfunterlagen ausgegeben; aktuelle Prüfunterlagen sind ausschließlich in ITER-003.

TECHNICAL-AUDIT.json ist ausdrücklich ein begrenzter Anschlusscheck: AABB-Kandidaten sind keine bewiesenen Kollisionen. Es liegt weder eine vollständige Drehzyklus-Kollisionsfreiheit noch ein statischer oder montagetechnischer Nachweis vor. 48 Nagelpfade schneiden derzeit unentlastetes Kranzmaterial; fehlende Bohrungen dürfen nicht als fertig konstruierter Anschluss gelten. SELF-AUDIT.md nennt die verbleibenden P1/P2-Punkte. Die Iteration ist zur Kritik bereit, nicht zur Fertigung oder als bestätigter Ist-Zustand.
