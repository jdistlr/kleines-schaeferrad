# Die alte 3D-Werkbank: was sie kann und was das neue Modell können muss

Stand 12.10.2026. Grundlage ist der Quellcode in `src/workbench/` (viewer.js, geometry.mjs, calibration.mjs, expert-corrections.mjs, mechanics.mjs, projection.mjs, client.js) und die Seite `src/pages/werkstatt.astro`.

## Ist sie verloren?

Nein. Der gesamte Code der 3D-Werkbank liegt unverändert in `main`. Verloren ging am 11.10.2026 nur die **gebaute** Fassung auf GitHub Pages, weil das Cockpit sie überschrieben hat. Wiederherstellen lässt sie sich auf zwei Wegen:

- **Neu bauen.** Auf einem Rechner mit Internetzugang `npm install`, dann `npm run build`, dann `python scripts/kern/veroeffentliche_cockpit.py --seite dist`. In dieser Arbeitsumgebung geht das nicht, weil das npm-Verzeichnis gesperrt ist und `node_modules` unvollständig ist.
- **Altes Pages-Artefakt.** Es läuft am 12.10.2026 um 20:21 Uhr ab. Danach bleibt nur das Neubauen.

## Funktionen der alten Werkbank

| Bereich | Funktion |
|---|---|
| Ansichten | Gesamtanlage, Seite A/B (Land/Wasser), Welle/Arme, Kranz, Kumpf/Schaufel, Schaufeln, Tragwerk, Lager, Trog/Rinne, Betrieb; Kamera fährt weich |
| Darstellung | orthografische Kamera, Drehen/Verschieben/Zoomen, Achsenkreuz, Auseinanderziehen mit Stärke-Regler, Schnittebene mit Versatz, Isolieren einer Baugruppe |
| Ebenen | Rad, Tragwerk, historische Kandidaten als Drahtgitter, Fragen-Stecknadeln |
| Varianten | Dauben 24/22 mm, Armform (gekröpft/gerade/unbekannt), Armlagen, Verbindungsart der Arme mit Rangfolge, Nagelweg A/B/C, Überlappungsrichtung, Schaufelneigung, Modellmodus |
| Betrieb | Rad dreht mit einstellbarer Drehzahl; 24 Kümpfe füllen sich unter dem Wasserspiegel, heben an und geben am Trog ab; Wasserstand und Strahlgeschwindigkeit regelbar; Statuszeile |
| Evidenz | Färbung nach Belegstatus, Fotovergleich (aktuelles Foto, historische Skizze, Armprofil) |
| Scan | Punktwolke (PLY) oder Oberflächenmodell (GLB) vom 07.10.2026 nebeneinander, Achsenangleich, grobe Ausrichtung, Registrierung über Passpunkte mit Restfehler |
| Auswahl | Klick auf ein Teil öffnet dessen Familie in der Seitenleiste, Einstellungen werden gespeichert |

## Schwächen, die das neue Modell nicht erben soll

- **Maße nicht aus dem Kern.** Alles kommt aus `data/hypothesis.parameters.json` und den Kalibrierdateien. Fünf Werte weichen vom Kern ab, am deutlichsten die Kumpfhöhe: 0,44 m im Modell gegen 0,60 m in Skizze und Foto. Siehe [MODELL-BRUECKE.md](MODELL-BRUECKE.md).
- **Keine Herkunft am Teil.** Man sieht nicht, ob ein Maß gemessen, überliefert oder angenommen ist.
- **Arme kreuzen sich.** Die Arme kreuzen sich als feste Annahme, und der Prüftest erzwingt das. Das widerspricht Thorstens Aussage (F-005).
- **Lagerung fehlt.** Achshöhe, Dorn und Lagerschlitz fehlen; die Lage zur Radstadt ist geschätzt.
- **Ein großes Bedienfeld.** Viele Schalter liegen gleichrangig nebeneinander. Das gleiche Problem hatte das erste Cockpit.

## Was das neue Modell können muss

Mindestens alles aus der Tabelle oben. Dazu kommen:

1. **Maße aus dem Kern.** Jedes Teil kennt seine Kern-IDs. Offene Werte erscheinen sichtbar anders, etwa schraffiert oder mit gestrichelter Kante. Annahmen sind als solche markiert.
2. **Aufbau und Abbau als Ablauf.** Die Schritte aus `kern/arbeitsschritte.json` in Reihenfolge abspielen: Welle einlegen, Arme durchschieben und verkeilen, Krümmlinge mit Schetternbrettern stoßen, Kümpfe nageln. Vor und zurück, mit Werkzeug und Personenzahl.
3. **Maße nachschlagen.** Ein Klick auf ein Teil zeigt dieselbe Karte wie im Cockpit, mit Maßblatt, Fragen und Fotos. Die Messstelle wird am Teil angezeigt.
4. **Geschichte.** Zu jedem Bauteil eine kurze Überlieferung, Skizzenbezug und Vereinsbegriff.
5. **Figuren und Modell aus denselben Zahlen.** Die Anatomie-Figuren (zuerst „Drei Armtypen“) und das 3D-Modell lesen dieselben Kern-Angaben. Eine Korrektur im Kern ändert beides.

## Reihenfolge

1. Jetzt erledigt: Bestandsaufnahme (diese Datei) und Brücke Modell ↔ Kern (`scripts/kern/modell_bruecke.py`).
2. Nach den Antworten zu F-001, F-003, F-005 und F-034, also der Grundgeometrie: eine Parameterdatei, die aus dem Kern erzeugt wird und `hypothesis.parameters.json` ersetzt. Jeder Wert trägt dabei Kern-ID und Status.
3. Danach das neue Modell schrittweise umstellen, zuerst Welle, Arme und Lager, dann Kranz und Kümpfe. Zum Schluss kommt der Aufbau-Ablauf.
4. Möglichkeiten und Ausbaustufen der Szene: [3D-VISION.md](3D-VISION.md).
5. Parallel weitere Hero-Figuren: Welle mit Dorn, Schellen und Lagerschlitz; Krümmlingstoß mit Schetternbrett und Stoßkeil.
