# A-Bock: Rinnenüberlappung und Gelände

Stand: 11.10.2026. **Informationssammlung; keine neue 3D-Konstruktion.**

## Festgelegte Funktion und Maße

Der A-Bock trägt die Rinne **genau an der Überlappung ihrer beiden Teile**. Er steht mit beiden Füßen auf dem lokalen Gelände. Eine Lage an einem beliebigen Punkt der Rinne oder schwebend über dem Boden entspricht nicht der Nutzerbeschreibung.

| Eigenschaft | Nutzerbestätigter Wert |
|---|---:|
| Zwei schräg gestellte Balken | 14 × 14 cm |
| Aussparungsbreite | 5 cm |
| Durchgesteckter Riegel | 4 × 14 cm, 90 cm lang |
| Riegelsicherung | Keile oben und unten |
| Höhe am Rinnenübergang | **80 cm Boden → Unterseite Rinnenboden** |

Die Rinne liegt auf dem Riegel auf. Bei 14 cm vertikaler Riegelhöhe und unmittelbarem Kontakt liegt seine Unterseite rechnerisch bei 66 cm über dem gleichen lokalen Boden; das ist eine **bedingte Ableitung**, kein zusätzliches gemessenes Feldmaß. Bodengefälle, Keilanlage und Kontaktflächen beim Einbau berücksichtigen. Riegellänge 90 cm ist nicht automatisch lichte Weite oder Beinachsabstand.

## Maßfotos und Boden

[image-1791543497527.jpg](image-1791543497527.jpg) zeigt die oberen Balkenenden etwa im Skalenbereich 147–151 cm. Das sind Ablesekoordinaten entlang des schrägen Beins, keine vertikale Höhe. Eine sichere Balkenlänge braucht den passenden Null-/Fußbezug.

[5f0dbdce-2f7a-40c3-9b75-c66153bb40fd.jpeg](5f0dbdce-2f7a-40c3-9b75-c66153bb40fd.jpeg) und [image-1791543487137.jpg](image-1791543487137.jpg) zeigen Gesamtbock und Gelände, wobei Gras den exakten Stirnflächen-/Nullkontakt teilweise verdeckt. Das rot markierte Foto als vorhandenen Bezug mit prüfen. [image-1791543505768.jpg](image-1791543505768.jpg) und [image-1791543574540.jpg](image-1791543574540.jpg) zeigen Riegel/Keile im Auflagerbereich.

Die [neueren Rinnenfotos](../Rinne/README.md), besonders IMG20261003111015, zeigen ebenfalls die Füße auf dem Boden und die Verstärkung am Rinnenübergang. Für die Radstadt-/Geländehöhe ist [IMG20261010121434.jpg](<../Lagerboch Landseite/IMG20261010121434.jpg>) relevant; siehe den [Trog-Einbaubefund](../Auffangtrog/BEFUND.md#höhenbezug-und-noch-offene-auswertung).

Die **80 cm** allein bestimmen weder die Geländehöhe relativ zur Wellenachse/Radstadt noch den Fußabstand. Dafür sind zusätzlich Balkenachsrichtung, Aussparungslage, Riegelüberstände und Gelände nötig. Vor einer erneuten Messfrage vorhandene Zollstockbilder gezielt lesen. Bereits gegebene Querschnitte und Riegelmaße nicht erneut anfragen.

## Vorhandene Darstellung und spätere Korrektur

[expert-corrections.mjs](../../../src/workbench/expert-corrections.mjs) stellt den Bock bereits dar, setzt aber `ground = J.z - .8`. Das erhält den örtlichen Abstand zwischen Rinne und angenommener Bodenhöhe, registriert die Füße jedoch nicht mit dem dargestellten oder aufgenommenen Gelände. Der Bezugspunkt J selbst stammt aus einer willkürlichen 55-%-Teilung der Rinne.

[reconstruction-constraints.json](../../../data/reconstruction-constraints.json) kennzeichnet 1,50 m Beinlänge, 12° Beinwinkel, 60 cm Sitzachsabstand und 18 cm Schlitzhöhe als Darstellungskandidaten. Diese Werte hier nicht in gemessene Ist-Maße umstufen. Insbesondere sind die 12° am Rinnen-Endschnitt kein Beleg für 12° Beinwinkel.

Beim späteren Modellauftrag die Überlappung, Riegeloberseite und lokale Bodenauflagen gemeinsam bestimmen. Füße auf das Gelände setzen; Riegeloberseite an die Unterseite des Rinnenbodens bringen. Dabei die bestätigten 80 cm prüfen. Falls das Gelände für eine plausible Darstellung gewählt werden muss, es als Annahme ausweisen und mit dem Höhenfoto abgleichen.
