# Das Kleine Schäferrad in 3D: Möglichkeiten und Ausbaustufen

**Verbindliche Vision**, von Johannes am 12.10.2026 festgelegt: Das ist die Zielstufe für das 3D-Modell, und sie darf übertroffen werden, nie unterschritten. Jede Arbeit am Modell, an Figuren und an der Szene richtet sich danach. Die Vision selbst ist **kein Bauauftrag**: Gebaut wird erst auf ausdrücklichen Auftrag und in den Ausbaustufen unten. Ergänzt die Bestandsaufnahme in [3D-WERKBANK-INVENTAR.md](3D-WERKBANK-INVENTAR.md) und die Brücke zum Kern in [MODELL-BRUECKE.md](MODELL-BRUECKE.md).

## Für jeden, der später am Modell baut

- Vor jeder Arbeit an Modell, Figuren oder Szene diese Datei ganz lesen.
- Jeder Schritt muss auf eine Ausbaustufe und einen Abschnitt hier einzahlen. Was der Vision widerspricht (Geometrie ohne Kern, versteckte Unsicherheit, Effekt statt Wahrheit), wird nicht gebaut.
- Neue Ideen, die darüber hinausgehen, werden hier ergänzt, nicht in Übergabedateien.

## Leitgedanke

**Der Wow-Effekt kommt aus der Wahrheit, nicht trotz ihr.** Ein Wasserrad, das sich dreht und Wasser schöpft, kennt jeder aus Animationen. Neu ist ein Rad, das genau so gebaut ist, wie der Verein es seit Generationen baut: jeder Keil an seinem Platz, jedes Maß mit Herkunft, jede Unsicherheit ehrlich gezeigt. Das tragende Erlebnis ist, dass man das Rad zerlegen, wieder aufbauen und an jedem Teil nachfragen kann: Woher wissen wir das?

Daraus folgen drei Regeln für jede Idee unten:

1. **Geometrie nur aus dem Kern.** Jedes Teil wird aus `kern/` erzeugt und trägt seine Kern-IDs. Atmosphäre darf erfinden (Wolken, Vögel); Konstruktion nicht.
2. **Unsicherheit ist ein Gestaltungsmittel, kein Makel.** Offene Werte sehen anders aus als bestätigte, und zwar schön.
3. **Eine Datenquelle für alles.** Cockpit, Anatomie-Figuren und 3D-Modell lesen dieselben Angaben. Eine Korrektur im Kern ändert alle drei.

## 1. Das Rad selbst: Holz, Eisen, Spuren

| Idee | Was man sieht | Grundlage im Kern / in den Belegen |
|---|---|---|
| Echte Bauteilformen | Zwölfeck-Welle mit Armöffnungen, Arme mit Kerben und Hals, Krümmlinge mit ausgeklinktem Stoß, Schetternbretter, Stoß- und Armkeile, Kümpfe aus 12 Dauben mit drei Reifen | AN-20261011-10…13, AN-20261012-01…49, Skizzen IMG_6798, 6816, 6831 |
| Holzarten | Eiche (Welle, Arme, Schettern) gegenüber Föhre (Krümmlinge, Kümpfe, Rinne): unterschiedliche Maserung, Farbe, Porenbild | Holzliste IMG_6827 (CLAIM-0057 ff.) |
| Hirnholz mit Jahresringen | An jeder Schnittfläche echte Jahresringe; Mark liegt dort, wo der Stamm war | ableitbar aus Querschnitt und Rohholzdurchmesser der Holzliste |
| Gebrauchsspuren | bemooste Außenzonen, saubere dunkle Zone um die Kerben (dort steckt der Arm in der Welle), nasse Verfärbung unter der Wasserlinie, ausgefranste Kanten | AN-20261012-18 und die Messfotos selbst |
| Eisen | rostige zweiteilige Wellenschellen mit Laschen und Sechskantschrauben, Dorn mit Laufrillen, Kumpfreifen, Nagelköpfe | AN-20261012-21/22/24, Wellenbefund |
| Zeichen am Holz | eingeschlagene Ziffern auf den Armen (gerade landseitig, schräg wasserseitig), „L“ am Lagerklotz | CLAIM-0010 ff., Foto IMG20261010121733 |
| Texturen aus den eigenen Fotos | Oberflächen werden aus unseren 129 Messfotos gewonnen statt aus Bildarchiven: das Rad trägt seine eigene Haut | evidence/raw |
| Abgleich mit dem Scan | Punktwolke vom 07.10.2026 als zuschaltbarer Geist über dem Modell: wo passt es, wo nicht? | Scaniverse PLY/GLB, F-025…F-027 |

## 2. Wasser: der eigentliche Darsteller

| Idee | Was man sieht |
|---|---|
| Fließende Regnitz | Strömung mit Fließrichtung, kleine Wirbel hinter den Pfosten der Radstadt, Lichtspiegelung |
| Schaufeln greifen ins Wasser | Spritzer und Schaum, wo die Flügelbretter eintauchen; Bugwelle; das Rad wird sichtbar vom Wasser getrieben, nicht von einem Motor |
| Kümpfe schöpfen | jeder der 24 Kümpfe füllt sich unten, trägt das Wasser hoch, kippt oben über dem Trog aus; Tropfen, die unterwegs herauslaufen |
| Wasserweg bis aufs Feld | Trog → Rinne 1 → A-Bock → Rinne 2 → Auslass, mit sichtbarem Fluss; eine Zahl zeigt, wie viele Liter pro Minute ankommen |
| Kaustik | Lichtnetz vom Wasser auf der Unterseite der Krümmlinge und Balken |
| Wasserstand als Regler | Niedrig-, Mittel- und Hochwasser: das Rad läuft langsamer, schneller oder taucht zu tief ein |

Grundlage: F-016 (Wasserstand zur Achse), Kumpfmaße, Drehzahl aus Beobachtung. Der Betriebsmodus der alten Werkbank (Füllen, Heben, Ausgießen) ist ein guter Startpunkt.

## 3. Licht, Wetter, Jahreszeit

| Idee | Wirkung |
|---|---|
| Echter Sonnenstand | Sonne für den tatsächlichen Standort und jedes Datum und jede Uhrzeit: Schatten fallen wie an der Regnitz |
| Tageszeiten | Morgennebel über dem Fluss, Mittagslicht, goldene Stunde, blaue Stunde |
| Atmosphäre | Dunst in der Ferne, Lichtstrahlen durch die Speichen, Himmel mit Wolkenzug |
| Leben am Ufer | Schilf im Wind, Weidenblätter, Libellen über dem Wasser, gelegentlich ein Vogel auf dem Kranz – sparsam, nie störend |
| Jahreskreis | Frühjahr: Aufbau. Sommer: Betrieb, Felder grün. Herbst: Laub (wie auf den Abbaufotos), Abbau. Winter: Radstadt allein im Wasser, die Teile eingewickelt im Lager |

## 4. Klang

Rauschen des Wassers, das Knarzen des Holzes im Takt der Umdrehung, das Plätschern beim Ausgießen in den Trog, Hammerschläge beim Verkeilen im Aufbau-Ablauf. Räumlich: Wer nah an den Trog fährt, hört das Ausgießen lauter. Standardmäßig leise und abschaltbar.

## 5. Zerlegen und Hineinschauen

| Idee | Was man sieht |
|---|---|
| Gestufte Explosion | Anlage → Rad → Kranz → Krümmling → Keil: auf jeder Ebene weich auseinander und wieder zusammen, mit Federbewegung wie in den Anatomie-Figuren |
| Schnitt durch die Armzone | Ein Schnitt durch die Welle zeigt, wie die drei Arme mit ihren Kerben ineinandergreifen. Genau das, was wir noch nicht wissen (F-005, F-034): bis zur Antwort als ehrliche Varianten zum Umschalten |
| Röntgenblick | Holz wird glasig, Keile, Nägel und Eisen bleiben sichtbar: man sieht, was das Rad zusammenhält |
| Einzelteil auf dem Werktisch | Ein Teil wird herausgenommen und liegt wie auf den Fotos vom Abbau im Gras, mit Zollstock daneben |
| Stückliste im Raum | Alle Teile einer Art aufgereiht: 6 Arme, 12 Krümmlinge, 24 Kümpfe, 48 Froschkeile … mit Zählern aus dem Kern |

## 6. Aufbau und Abbau als Film und als Werkzeug

Die Arbeitsschritte aus `kern/arbeitsschritte.json` (AS-AUF-01 … 07) werden zum Ablauf mit Zeitleiste:

- Welle einlegen, Arme durchschieben und verschränken, mit Wellenkeil sichern, Krümmlinge aufsetzen, Stöße mit Schetternbrettern nageln, Kranz mit Stoßkeilen verspannen, Kümpfe nageln, Flügelbretter binden.
- Vor und zurück spulen, an jedem Schritt anhalten. Das Werkzeug des Schritts erscheint (F-011), die Zahl der Helfer, die Dauer.
- **Rückwärts ist es der Abbau vom 10.10.2026**: An den Stellen, an denen ein Foto gemacht wurde, blendet das echte Foto aus derselben Blickrichtung ein.
- Später als Arbeitshilfe für den Verein: Der Aufbau-Messplan fürs Frühjahr hängt an denselben Schritten.

## 7. Kamera

| Idee | Erlebnis |
|---|---|
| Anflug | Vom Himmel über die Regnitz, die Felder und das Ufer hinunter zum Rad |
| Durch die Speichen | Die Kamera fährt zwischen den Armen hindurch zur Welle |
| **Mitfahrt im Kumpf** | Eine Umdrehung aus Sicht eines Kumpfes: eintauchen, füllen, hochsteigen über den Fluss, oben auskippen in den Trog |
| Dem Wasser folgen | Vom Ausguss durch Trog und Rinnen bis aufs Feld |
| Foto-Standpunkte | Jedes Abbau-Foto als kleiner Rahmen im Raum; anklicken, und die Kamera steht genau dort, das Foto legt sich über das Modell |
| Ruhige Bahn | Langsamer Rundflug für die Ausstellung, ohne Bedienung |
| Rundgang | Auf Augenhöhe am Ufer und auf dem Laufsteg gehen |

## 8. Wissen im Raum

- **Maße am Teil**: Maßlinien erscheinen bei Bedarf, mit Wert, Kern-ID und Status; offene Maße gestrichelt, Bereiche (z. B. 0,31–0,38 m) als schmales Band statt als Strich.
- **Widersprüche sichtbar**: Die Radstadt kann zwischen 4,40 m und 5,25 m umgeschaltet werden; man sieht, wo der Drehkreis anstößt (F-001).
- **Herkunft am Teil**: Farbe nach Grundlage (gemessen, mündlich, Skizze, Foto, Annahme) als zuschaltbare Ansicht.
- **Klick auf ein Teil** öffnet dieselbe Karte wie im Cockpit: Maßblatt mit Belegen, Skizzen, offene Fragen, Antworten.
- **Fragen im Raum**: Kleine Marken an den Stellen, zu denen eine Frage offen ist; die Antwort kann man direkt dort geben.

## 9. Geschichte und Kultur

- Die alten Vereinsskizzen als Überblendung über das Modell: So hat man es gezeichnet, so ist es gebaut.
- Eine Zeitleiste der Überlieferung: wer wann was weitergegeben hat (aus den Aussagen im Kern, mit Einverständnis der Personen).
- Vereinsbegriffe als Etiketten am Teil (Krümmling, Schettern, Kumpf, Radstadt), mit Erklärung.
- Hintergrund zu Wasserschöpfrädern an der Regnitz und ihrer Bedeutung für die Bewässerung. Inhalte vorher mit Quellen prüfen; nichts aus dem Gedächtnis übernehmen.

## 10. Physik zum Ausprobieren

Strömung erhöhen, und das Rad dreht schneller; Wasserstand senken, und die Kümpfe schöpfen weniger. Ein Zähler zeigt die gehobene Wassermenge pro Stunde und Tag. Alle Formeln offen gelegt; Werte, die geschätzt sind, als Schätzung markiert.

## 11. Ausstellung und Reichweite

- **Ausstellungsmodus**: Vollbild, ruhige Kamerabahn, ein Tipp startet die Führung.
- **Geführte Tour** in Kapiteln: Ort, Rad, Wasser, Aufbau, Geschichte.
- **Erweiterte Realität** auf dem Handy: das Rad im Maßstab 1:20 auf den Tisch stellen, oder lebensgroß im Garten.
- **Bild- und Posterausgabe**: hochaufgelöste Ansichten und Explosionszeichnungen für Vereinsheft, Homepage und Infotafel.
- **Vereinshomepage**: dieselbe Szene eingebettet, mit Link ins Cockpit.

## 12. Technik

- three.js (im Repository vorhanden, Version 0.180), später WebGPU, wo es der Browser kann.
- Geometrie wird aus einer Parameterdatei erzeugt, die selbst aus dem Kern erzeugt wird (ersetzt `data/hypothesis.parameters.json`).
- Wiederholte Teile (Kümpfe, Keile, Nägel) als Instanzen; Detailstufen je Entfernung; Ziel: flüssig auf einem Mittelklasse-Handy.
- Nachbearbeitung zurückhaltend: Umgebungsverdeckung, filmische Tonwerte, Tiefenschärfe nur bei Nahaufnahmen.
- Prüfungen wie bei den Anatomie-Figuren: Kollisionsprüfung gegen die Kern-Geometrie, Bildvergleich per Bildschirmfoto bei jeder Änderung, Lesbarkeit auf 390 px Breite.
- Funktioniert ohne Ton, ohne Bewegung (reduzierte Bewegung) und mit Tastatur.

## Ausbaustufen

| Stufe | Inhalt | Voraussetzung |
|---|---|---|
| **1 · Wahrheit** | Bauteile aus dem Kern, Zerlegen, Maße und Herkunft am Teil, Klick öffnet Cockpit-Karte | Antworten zu F-001, F-005, F-034; Parameterdatei aus dem Kern |
| **2 · Leben** | Material und Spuren, Wasser mit Schöpfen, Sonnenstand, Klang | Stufe 1 |
| **3 · Erlebnis** | Aufbau-Film mit Fotos, Kamerafahrten inklusive Kumpf-Mitfahrt, Ausstellungsmodus, AR | Stufe 2; Arbeitsschritte von Thorsten bestätigt (F-017) |

## Die fünf stärksten Momente

1. **Mitfahrt im Kumpf**: eine Umdrehung aus Sicht des Wassers.
2. **Der Abbau rückwärts**: das Modell setzt sich zusammen, und an jeder Stelle blendet das echte Foto vom 10.10.2026 ein.
3. **Schnitt durch die Armzone**: das Geheimnis der Verschränkung, sobald Thorsten es erklärt hat.
4. **Die Radstadt im Jahreskreis**: Sommerbetrieb, Herbstlaub, Winterstille, Frühjahrsaufbau.
5. **Woher wissen wir das?** Auf jedes Teil tippen und das Foto mit Zollstock sehen, aus dem das Maß stammt.
