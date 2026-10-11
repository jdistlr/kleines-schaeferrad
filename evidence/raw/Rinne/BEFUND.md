# Rinne: zwei Teile, Überlappung und Auflager

Stand: 11.10.2026. **Informationssammlung; kein Modellumbau.**

## Nutzerbestätigt

- Die Rinne liegt am Rad auf dem **landseitigen Lagerbock** auf. Der Schöpftrog liegt auf der Rinne auf; siehe [Trog- und Einbaubefund](../Auffangtrog/BEFUND.md).
- Von dort läuft die Rinne diagonal/landwärts zum Wasserauslass. Der Nutzer erlaubt eine plausible Wahl des Grundrisswinkels und der Position zum Wasserrad. Gewählte Winkel sind Annahmen, keine Fotomesswerte.
- Die Rinne besteht aus **zwei Teilen**. Die Teile **überlappen sich** am Übergang; die bisherige reine Stoßbeschreibung wird damit präzisiert.
- Der **A-Bock steht genau unter diesem Überlappungsbereich**, mit seinen Füßen auf dem Gelände. Seine Position folgt aus dem tatsächlichen Übergang der beiden Teile.
- An dieser Stelle ist die **Unterseite des Rinnenbodens 80 cm über dem lokalen Boden**. Der A-Bock-Riegel trägt dort die Rinne.

Wasserlauf: Schöpftrog-Auslass → radnaher Rinnenteil → Überlappung auf A-Bock → zweiter Rinnenteil → Wasserauslass. Überlappung und etwaige Höhenstaffelung müssen den Abfluss erlauben; eine konkrete Falz- oder Laschengeometrie ist bisher nicht belegt. Seitliche Verstärkungsbretter sind auf den Fotos sichtbar, aber nicht mit einer schon exakt vermessenen Bodenüberlappung gleichzusetzen.

## Zeichnung: Rinne 1 hinter Trog

[IMG_6830.jpeg](IMG_6830.jpeg), Quelle PHOTO-6830; bestehende Claims CLAIM-0142 bis CLAIM-0151 in [geometry.claims.json](../../../data/geometry.claims.json).

| Eintrag | Ablesung / Status |
|---|---|
| Titel | „Rinne 1 (hinter Trog)“; nicht als Zeichnung beider Teile behandeln. |
| Lange Maßlinie | ausdrücklich 480 cm |
| Weitere Längeneinträge | 415 und 422; andere Konturen/Endschnittbezüge vor Übernahme zuordnen |
| Abschnittsabstände | 100 cm; zusätzliche Rand-/Anfangsbezüge in der Zeichnung |
| Querschnitt innen | 18 cm breit |
| Querschnitt außen | maximal 23 cm breit |
| Seitenhöhe | 20 cm |
| Stirn-/Endschnitt | 12°; **kein Nachweis für Gesamtgefälle, Grundrisswinkel oder A-Bock-Beinwinkel** |
| Weiteres Endmaß | 22 cm; genauen Bezug anhand Zeichnung prüfen |
| Konstruktionshinweise | „Leiste“ und „Latte“ |

Die Länge des zweiten Rinnenteils und die Überlappungslänge sind damit noch nicht sicher bestimmt. 480 und 415/422 nicht zu einer Zweiteil-Gesamtlänge addieren. Für die spätere Konstruktion zunächst vorhandene Fotos/Zeichnungsbezüge auswerten; verbleibende Ersatzmaße ausdrücklich als Kandidaten führen.

## Geeignete Fotos

- [IMG20261003110312.jpg](IMG20261003110312.jpg): zusammenhängende Ansicht von Wasserrad, Rinne, A-Bock und Wasserauslass.
- [IMG20261003111006.jpg](IMG20261003111006.jpg), [IMG20261003111009.jpg](IMG20261003111009.jpg): unterer Rinnenteil und Auslass.
- [IMG20261003111015.jpg](IMG20261003111015.jpg): Rinnenübergang mit seitlicher Verstärkung und A-Bock.
- [IMG20261003111022.jpg](IMG20261003111022.jpg), [IMG20261003111029.jpg](IMG20261003111029.jpg): Verbindung Schöpftrog/Rinne/Lagerbock.
- [IMG20261010121518.jpg](<../Lagerboch Landseite/IMG20261010121518.jpg>): Rinnenlage über dem landseitigen Bock aus der Draufsicht.
- [Ältere A-Bock-Fotos](../A-Bock/README.md): Überlappungsbereich, Riegel, Keile, Bodenkontakt.

IMG20261003111022 1.jpg und IMG20261003111022.jpg besitzen identische Git-Blobs. Die zweite Datei ist kein unabhängiger Blickwinkel und kein zusätzlicher Messbeleg. Beide vorhandenen Dateinamen bleiben erhalten.

## Abweichung im vorhandenen Code

[expert-corrections.mjs](../../../src/workbench/expert-corrections.mjs), `rebuildStationary`, enthält bereits `TH-CHANNEL-1`, `TH-CHANNEL-2` und `TH-A-CROSSBAR`. Es fehlt also nicht die gesamte Baugruppe. Die Umsetzung ihrer Lage und Verbindung passt jedoch noch nicht zu den präzisierten Informationen:

- Übergang `J = A.lerp(D, .55)`: willkürlich bei 55 % einer synthetischen Gesamtstrecke; nicht aus Teilmaßen oder Überlappung bestimmt.
- Beide Teilgeometrien enden/beginnen bei J. Das ist ein stumpfer Anschluss **ohne reale Überlappung**.
- Profil 32 cm breit / 14 cm tief ist ein Darstellungskandidat; es entspricht nicht unmittelbar den 18/23/20-cm-Bezügen der Rinne-1-Zeichnung.
- Rinnenlauf hat ein konstantes globales Y; sein Winkel ist nicht aus Fotos registriert. Eine plausible neue Richtung darf gewählt werden, sobald die Auflagerbeziehungen dabei mitgeführt werden.
- Der A-Bock ist an J gebunden, sein Gelände jedoch aus J abgeleitet. Ein tragender Anschluss im Code belegt keinen Bodenkontakt zur tatsächlichen Geländeoberfläche.

Bei einem späteren Modellauftrag erst beide Teile mit markierter Überlappung anlegen, dann den A-Bock unter diese Zone setzen. Den Riegel quer zur gewählten lokalen Rinnenrichtung orientieren. Anschließend Kontakt am Lagerbock und den [Geländebezug](../A-Bock/BEFUND.md) prüfen. Teilmaße und Überlappung als getrennte Parameter führen.
