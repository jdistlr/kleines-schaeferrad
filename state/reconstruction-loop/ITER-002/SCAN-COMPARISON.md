# Scanvergleich — Trog gezielt gesucht, Registrierung nicht freigegeben

Die archivierte PLY und GLB wurden aus diesem Repository geprüft. PLY enthält75.619 Punkte; GLB56.117 Positionsvertices und78.043 Dreiecke. Hashes und native Bounds: `evidence/scan-inspection.json`. Die Exporte sind unterschiedliche Repräsentationen derselben Aufnahme, keine unabhängigen Messungen.

Die dokumentierte Exportrelation PLY(x,y,z)→GLB(x,z,−y) erklärt die andere Aufwärtsachse. Die kanonische GLB-Normalisierung Rx(+90°) ergibt wieder PLY-artige Z-Hoch-Darstellung. Damit ist die mechanische Wellenachse noch nicht registriert. Bestehender Status `AXIS_NORMALIZED`, `field_scale=null`, `adopted_mechanical_transform=null` bleibt unverändert.

## Visuelle Suche und Kandidaten

Gesamtansichten `evidence/derived/ply-spatial.png` und `ply-orthographic.png` sowie die neu berechnete `views/scan-search.png` wurden angesehen. Die neue Ansicht färbt13.246 Punkte im nativen Höhenband2,8<Z<3,5 und lässt den übrigen Scan grau. Sie stellt drei orthografische Projektionen dar, ohne neue Pose oder Skalierung.

| Merkmal | Scanbeobachtung in nativen Koordinaten | Fotobezug / Einstufung |
|---|---|---|
| Kranz-/Armbereich | Kreisbogen und radial angeordnete Hölzer vor allem in XZ sichtbar; ungefähre Normalrichtung entlang nativerY. | Radkontext erkennbar; keine einzeln identifizierten identischen Armenden und keine signierte Wellenachse. |
| Längliche Struktur A | EtwaX−2,3…0,8, Y−0,9…−0,25, Z3,0…3,35; abschnittsweise horizontale Rand-/Flächenstruktur. | Trog-/Rinnenkandidat gegenüber1887655/1908195/1920559; noch keine eindeutige Zuordnung bestimmter Endkanten. |
| Längliche Struktur B | EtwaX0,7…1,4, Y0…2,4 im selben Höhenband; längliche rechteckige Kontur. | Alternativ tragendes/rotierendes Brett oder Teil des Wasserwegs; nur nach räumlicher Einbauzuordnung entscheiden. |
| Tragwerk | Senkrechte und waagerechte Fragmente unter Rad-/Oberbau. | Neue Bockfotos liefern mögliche Anschlussmerkmale; genaue Identität einzelner Stützen nicht belegt. |

Die genannten Grenzen sind grobe Suchregionen aus den Darstellungen, keine vermessenen Bauteilgrenzen. Sie enthalten auch Flügel/Arme/Tragwerk. Die Existenz eines erkennbaren Trogkontexts aus TH-39 ist damit untersuchbar, aber nicht gleichbedeutend mit einer vollständigen, metrisch isolierten Trogoberfläche.

## Ergebnis des Registrierungsversuchs

Eine zuverlässige Transformationsschätzung wurde nicht angesetzt: Für beide Kandidaten fehlen drei eindeutig identische, nichtkollineare 3D-Korrespondenzen mit bekannten mechanischen Koordinaten. Das neue Maß1,80m betrifft Innenflächen, die in den Kandidaten nicht eindeutig beidseitig identifiziert sind. Land-/Wasserseite ist nicht mit signierter Scanachse verknüpft; ein kreisförmiger Fit lässt Drehlage und Spiegel-/Seitenzuordnung offen. Historische426/396 sind keine unabhängige Feldprüfstrecke. Ein ICP gegen die nachweislich falsche synthetische Geometrie würde diese Probleme verbergen.

Daher: mechanischer Transform=null, registrierte Trogpose=null, Skalierungsfaktor=null, Residuum=nicht berechenbar. Es wird weder `ROUGH_ALIGNED` noch `MECHANICALLY_REGISTERED` behauptet. Das ist ein dokumentiertes negatives Vergleichsergebnis, keine unversuchte Übernahme des alten Status.

## Nächste prüfbare Korrespondenzen

1. Identischen sichtbaren Trogendpunkt/Abgang im Scan und Foto markieren, zweite Endkante sowie einen seitlich versetzten Anschluss identifizieren. Herkunft und Picking-Unsicherheit speichern.
2. Zwei nachgewiesene Dorn-/Wellenzentren als Achsbezug und Land-/Wasserseite verknüpfen; kein beliebiges Kreisbogen-Zentrum als Wellenende verwenden.
3. Aktuelle Kontrollstrecke außerhalb des Fits, plus Höhen-/Bodenbezug verwenden. Drei nichtkollineare Kontrollen reichen zur Pose nur bei sicherem metrischem Bezug; zusätzliche Strecke prüft Maßstab/Fehler.
4. Transform, Determinante, Korrespondenzresiduen und Holdout-Fehler dokumentieren. Erst dann Trogkontur gegen geometrische Kandidaten prüfen und Status property-genau erhöhen.
