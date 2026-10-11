# Brücke: altes 3D-Modell ↔ Wissenskern

Erzeugt von `scripts/kern/modell_bruecke.py`. Nicht von Hand bearbeiten.

Das alte Modell (`src/workbench/`, Seite `/werkstatt/`) ist vollständig im Repository erhalten. Seine Maße stammen aus `data/hypothesis.parameters.json` und den Kalibrierdateien, nicht aus dem Kern. Diese Tabelle zeigt, wo beide übereinstimmen und wo nicht. Sie ändert nichts; das Umstellen des Modells beginnt erst nach Phase 2 des Ordnungsplans.

## Parameter des alten Modells

| Parameter | Modell | Kern-Angabe | Kern (umgerechnet, m) | Urteil |
|---|---|---|---|---|
| `outerRadius` | 2,13 | CLAIM-0236 (Außenradius (Notiz), offen) | 2,13 | stimmt |
| `outerRadius` | 2,13 | CLAIM-0234 (Außendurchmesser (Notiz) / 2, offen) | 2,13 | stimmt |
| `innerRadius` | 1,98 | CLAIM-0237 (Innenradius (Notiz), offen) | 1,98 | stimmt |
| `innerRadius` | 1,98 | CLAIM-0235 (Innendurchmesser (Notiz) / 2, offen) | 1,98 | stimmt |
| `rimWidth` | 0,14 | TH-20261009-26 (Thorsten, offen) | 0,14 | stimmt |
| `rimWidth` | 0,14 | CLAIM-0239 (Skizze, offen) | 0,14 | stimmt |
| `rimWidth` | 0,14 | AN-20261012-40 (Foto, offen) | 0,14 | stimmt |
| `ringDistance` | 1,94 | TH-20261009-28 (abgeleitet, offen) | 1,94 | stimmt |
| `shaftLength` | 3,7 | CLAIM-0001 (Skizze, offen) | 3,7 | stimmt |
| `shaftWidth` | 0,37 | AN-20261011-11 (über Ecken, offen) | 0,37 | stimmt |
| `shaftWidth` | 0,37 | AN-20261012-20 (Foto, offen) | 0,37 | stimmt |
| `armWidth` | 0,14 | AN-20261012-09 (Foto, offen) | 0,14 | stimmt |
| `armWidth` | 0,14 | AN-20261012-06 (Armzeichnung, offen) | 0,14 | stimmt |
| `armDepth` | 0,065 | AN-20261012-10 (Foto, offen) | 0,07 | weicht ab |
| `vesselRadius` | 0,16 | CLAIM-0026 (Außendurchmesser unten / 2 (Skizze, mm), offen) | 0,14 | weicht ab |
| `vesselRadius` | 0,16 | CLAIM-0025 (Außendurchmesser oben / 2 (Skizze, mm), offen) | 0,105 | weicht ab |
| `vesselHeight` | 0,44 | CLAIM-0024 (Skizze, mm, offen) | 0,6 | weicht ab |
| `vesselHeight` | 0,44 | AN-20261012-46 (Foto am Neubau-Kumpf, offen) | 0,6 | weicht ab |
| `vesselCount` | 24 | CLAIM-0329 (Kontext, offen) | 24 | stimmt |
| `paddleCount` | 24 | – | – | noch keine Kern-Angabe |
| `armsPerPlane` | 3 | CLAIM-0326 (Kontext, offen) | 3 | stimmt |
| `armsPerPlane` | 3 | CLAIM-0018 (Skizze, offen) | 3 | stimmt |
| `segmentsPerPlane` | 6 | CLAIM-0328 (Kontext, offen) | 6 | stimmt |
| `stationaryContext` | – | – | – | noch keine Kern-Angabe |
| `jointGeometry` | – | – | – | noch keine Kern-Angabe |

## Abweichungen

- `armDepth`: Modell 0,065, Kern AN-20261012-10 (Foto) 0,07
- `vesselRadius`: Modell 0,16, Kern CLAIM-0026 (Außendurchmesser unten / 2 (Skizze, mm)) 0,14
- `vesselRadius`: Modell 0,16, Kern CLAIM-0025 (Außendurchmesser oben / 2 (Skizze, mm)) 0,105
- `vesselHeight`: Modell 0,44, Kern CLAIM-0024 (Skizze, mm) 0,6
- `vesselHeight`: Modell 0,44, Kern AN-20261012-46 (Foto am Neubau-Kumpf) 0,6

## Was das neue Modell zusätzlich braucht

Diese Angaben kennt das alte Modell nicht. Ein aus dem Kern gespeistes Modell kann sie nutzen.

| Kern-ID | Eigenschaft | Wert | Grundlage |
|---|---|---|---|
| AN-20261012-30 | Wellenmitte über Oberkante Radstadt (Landseite) | 0,345 m | ableitung |
| AN-20261012-21 | Überstand des Dorns über die Stirnfläche | 0,175 m | foto |
| AN-20261012-22 | Durchmesser des Dorns | 0,075 m | foto |
| AN-20261012-19 | Kerbe liegt in der Armmitte | True  | ableitung |
| AN-20261012-12 | Kerblänge | 0,09 m | foto |
| AN-20261012-11 | Kerbtiefe | 0,05 m | foto |
| AN-20261012-05 | Versatz der Kröpfung (Skizze) | 4  | skizze |
| AN-20261012-03 | Zapfenlänge (Skizze) | 30  | skizze |
| AN-20261012-34 | Querschnitt Breite × Höhe | [0.41, 0.205] m | foto |
| AN-20261011-04 | Lichte Weite parallel zum Ufer | 4,4 m | muendlich |
| AN-20261012-28 | Oberkante Lagerklotz über Oberkante Radstadt | 0,46 m | foto |
