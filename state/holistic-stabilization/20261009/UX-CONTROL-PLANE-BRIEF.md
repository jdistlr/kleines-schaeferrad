# UX und Model Control Plane — Entwurf

**CONDITIONAL GO für die Planung; keine produktive UX-Abnahme.** Ein ruhiger Einstieg in die bestehende Werkstatt genügt. Kein neues Portal, Frameworkwechsel oder zweites Datenmodell. Die MUX-Grammatik aus `docs/MUX-DESIGN-GRAMMAR-V2.md` (Inhalt v3) bleibt maßgeblich: Manrope, Papier, Ink, feine Linien, kompakte Werkstatt, Skizze vor Eingabe im Feld. Ocker steht für Unbekannt/Konflikt; Lime ist keine Wahrheitsampel.

## Aktuelle Beobachtungen

Die veröffentlichte Seite wurde erneut direkt geprüft: Chromium 141 mit Playwright 1.62.1, Desktop 1440, Tablet 768, 390, 320 und exakt verdoppelten berechneten Schriftgrößen bei 1280 px; zusätzlich Reduced Motion und Dark Preference. 21 Seitenscreenshots in [live-browser](evidence/live-browser/). Browserzugriff erforderte den Umgebungsproxy und eine Zertifikatsausnahme für dessen Testumgebung. Die beiden fehlgeschlagenen Vorversuche bleiben dokumentiert. Dies ist kein Safari-/OS-Dynamiktext- oder TLS-Sicherheitsaudit.

[Live-Abgleich](evidence/live-compare.json): alle drei HTML-Seiten, ausgeliefertes JS/CSS und KS-50 sind bytegleich mit dem aktuellen lokalen Build. Main-Deploy ist durch Actions bestätigt. Offline-Manifest und Service Worker sind nicht bytegleich: vollständige Deploymentidentität und PDF-Reproduzierbarkeit daraus **nicht** behaupten. Der Vergleich ist gezielt, kein Vollhash aller veröffentlichten Dateien.

| Befund | Aktueller Nachweis | Konsequenz |
|---|---|---|
| Dringende Wasseraufnahme unsichtbar | Live-Klick auf sichtbaren Link nicht möglich; CSS `field-context p` weiterhin versteckt; Desktop-Feldbild | UXR-01 / R1 weiterhin P1; sichtbare Aktion plus kontextuelle Originalvideo-/Messblatthinweise |
| 200%-Text überlagert Foto | `text200-story.png`, visuell geprüft | UXR-05 / R4 weiterhin P1; intrinsischer Umbruch, keine neue Gestaltung |
| Varianten vor Arbeitsfrage | `phone320-werkstatt.png`, `phone390-werkstatt.png`, `tablet-werkstatt.png` | UXR-04 weiterhin P1; selektive Offenlegung, Ansichts-/Bauteilauswahl zuerst |
| Nur eine Feldmessung je Antwort | Live 123→456, Reload und Import bewahren 456; Formular besitzt sechs Messfelder | UXR-02 bleibt P1. Absichtliches Überschreiben ist kein nachgewiesener zufälliger Datenverlust; additive Messliste separat planen |
| Fach-/Kandidatenstatus | Live-Modus „Rekonstruktionsvorschlag · ITER-003“, Truth ergänzt „Maße offen“ | PR #15 hat Revisionssprache verbessert. Nicht die alte UI unverändert behaupten; „führend“ bei 1,8 m/s bleibt erklärungsbedürftig |
| Quellen prüfen | Kumpfinspektor, Originalquelle, Truth/Brute und Kandidat B live erreichbar | Vorhandenen Weg erhalten; keine neue Galerie erfinden |

Kein aus dieser Prüfung belegter unmittelbarer P0-Datenverlust. Das Aufnahmefenster hat dennoch P0-**Arbeitspriorität**. Ein fehlgeschlagener Sichtbarkeitstest und eine ausstehende Hardwareprüfung sind unterschiedliche Befundarten. Aktuelle komplette Journey-Ergebnisse und Grenzen stehen in [BROWSER-RESULTS.md](BROWSER-RESULTS.md).

## Ein zusammenhängender Arbeitsbereich

Desktop: eine schmale Revisions-/Statuszeile, darunter Bauteilsuche links, Viewer in der Hauptfläche, eigenschaftsbezogener Inspektor rechts. Feldansicht bleibt eine Aufgabe mit Skizze und einer nächsten Aktion. 768/390/320: dieselbe Information in der Reihenfolge **Arbeitsfrage → ausgewähltes Teil → Bild/Skizze → offene Eigenschaft → Befund erfassen**. Technische Varianten in vorhandenem Details-Bereich, kein paralleles Dashboard voller Kacheln.

| Hierarchie | Sichtbarer Inhalt | Interaktion / Grenze |
|---|---|---|
| Revision | „ITER-003 · Arbeitsmodell · Maße offen“, Quelldatum, Link zur geprüften Revision | Kein pauschales grünes „bereit“ |
| Wissensqualität | „Fachauskunft“, „beobachtet“, „gemessen und geprüft“, „Annahme“, „offen“ je Eigenschaft | Zähler nur mit Nenner und Definition; 39 Aussagen sind keine 39 Messungen |
| Komponenten | Lokaler Name + stabile Familien-ID; reale Teil-ID nur wenn aufgenommen | Radstadt/Radstatt auf einen Eintrag auflösen; Schettern und Flügelbretter getrennt |
| Offene Maße | die nächste entscheidende Frage, Endpunkte, Einheit, Aufnahmefenster | Ein Knopf „Befund festhalten“; bei Unzugänglichkeit begründet offen |
| Evidenz und Entscheidungen | Original, Aussage, Interpretation, Entscheidung, Reviewer/Revision | Quelle öffnen und Gegenevidenz möglich; kein Bild wird automatisch bestätigte Metrik |
| Viewer-Modi | „Quellenbasierte Teilgeometrie · Maße offen“ / „Rekonstruktionskandidat“ | interner truth/brute-Wert unverändert; Betrieb/Strömung ausdrücklich Simulation |

Der gewählte Bauteil-/Eigenschaftskontext bleibt beim Wechsel Entdecken → Genauer prüfen → Festhalten erhalten. Expertenregler sind weiterhin erreichbar, aber verdrängen nicht den Einstieg. Eine verworfene Annahme bleibt über Versionsgeschichte lesbar.

## Messkarte am Beispiel Krümmling

[Entwurf als SVG](measurement-card.svg) ist eine **nichtmetrische Skizze**, kein technisches Blatt und keine Ist-Geometrie. Axiale Dicke: Endpunkt A äußere Stirnfläche, Endpunkt B innere Stirnfläche desselben eindeutig identifizierten Segments; Markierungen müssen im Aufnahmefoto bestätigt werden. Anzeige: „140 mm — Fachauskunft TH-26; Ist-Wert offen“. Die Skizze schreibt keinen Feldwert vor.

- Blaue Maßlinie A–B plus Buchstaben: ausgewählte Messstrecke, nicht Qualitätsstatus.
- Ocker/gestrichelt plus „offen“: ungeklärte zweite Eigenschaft. Bestätigung wird durch Text, Reviewer und Quelle vermittelt, nie nur Farbe.
- Felder: Teilinstanz, Zustand eingebaut/ausgebaut, Endpunktdefinitionen, Wert/Einheit, Werkzeug/Auflösung, Unsicherheit, Person/Zeit, Originalfoto und Ereignis/Partner bei Verbindung.
- Drei getrennte Zeilen: **Fachauskunft 140 mm**, **Ist-Messung offen**, **Modell verwendet 140 mm nach Fachauskunft**. „Bestätigt“ erst nach eigenständigem Review für diese Eigenschaft.
- Link „Was entscheidet diese Messung?“ führt zu TH-25/26→TH-28/29: Kranzabstände und Modellbreite prüfen. Die Dicke allein entscheidet weder die Nagelbohrung noch Tragfähigkeit.

## Schrittweise Umsetzung nach Review

1. R1/R4 auf aktuellem main, unveränderte 21 Task-IDs/Reihenfolge, v1-Import und Originalbytes; erst nach gesicherter Feldaufnahme veröffentlichen. Eigener Stop `UX R1+R4 REVIEW READY`.
2. Lesende Revisions-/Statusdarstellung und begrenzte progressive Offenlegung in vorhandener Werkstatt. Vorher/Nachher bei allen fünf Profilen; keine Geometrieänderung.
3. Messkarten zunächst als Sicht auf vorhandene Eigenschaften. Mehrfachmessungen nur in separatem additivem Speicherkontrakt mit v1-Lesbarkeit, Konfliktbehandlung und Rückwärtsweg.

Abnahme: Wasserauftrag in höchstens zwei sichtbaren Aktionen; keine 200%-Überlagerung; Tastaturfokus/Labels/Fehlermeldungen erhalten; keine Statusbehauptung ohne Quelle; Export/Import/Offline und Rückkehr zum Arbeitsschritt funktionieren. Screenreader, echtes iPhone/Safari, Speichergrenze und zweites Gerät bleiben ausdrückliche physische Gates. Prüfungen gegen Kandidatendarstellung dürfen nicht als Engineering-Freigabe erscheinen.
