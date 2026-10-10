# Aktuelle Browsernachweise und Grenzen

Basis: tatsächlich veröffentlichtes `https://jdistlr.github.io/kleines-schaeferrad/`, 09.10.2026 21:56–22:03 UTC; die Abschlussprüfungen liegen in Deutschland bereits am 10. Oktober. Chromium 141.0.7390.37 / Playwright 1.62.1, frische Kontexte, ausschließlich mit SIMULATION gekennzeichnete Eingaben. Browserautomation beobachtet die veröffentlichte Site; kein Remote-Datenbestand wird verändert. Lokale Testdaten sind nicht Feldbeobachtungen.

## Durchgeführt

[Hauptbericht](evidence/live-browser/report.json) und [Folgebericht](evidence/live-followup/followup.json) enthalten Uhrzeit, Viewports, Text, Zielgrößen, Fehler und einzelne Journeyresultate.

| Prüfung | Ergebnis |
|---|---|
| Desktop 1440, 768, 390, 320; Start/Werkstatt/Feld | Alle 12 Screenshots erstellt, kein horizontaler Seitenüberlauf |
| 200% Text, 1280; drei Seiten | Alle drei Screenshots erstellt. Überlagerung am Startfoto trotz `scrollWidth == innerWidth`; visuell bestätigt |
| Reduced Motion, Desktop; drei Seiten | Screenshots erstellt. Media Query true, geänderte Canvasbilder bei angehaltenem Rad auch in Folgeprobe. Quelle hat keine reduzierte Kamerainterpolation. Keine unendliche Leerlaufrender-Schleife daraus ableiten: PR #15 hat gerade diesen Mechanismus verändert |
| Dark Preference, 390; drei Seiten | Screenshots erstellt, helle MUX-Flächen bleiben sichtbar; kein eigener Darkmode versprochen |
| Modell → Kumpf → Originalquelle → Truth/Brute → Kandidat B | Erfolgreich durchlaufen; aktueller Revisions-/Maßstatus sichtbar |
| Direkter Wasserlink | **FAIL der Auffindbarkeit:** unsichtbar; über „Alle Schritte“ → Aufgabe 17 erreichbar. Folgetest bestätigt `waterLinkVisible:false` |
| Deep-Link und Wiederaufnahme | Normale Feld-URL setzt fort; `?task=TASK-WATER` setzt nach Reload auf Schritt 1 zurück. Früh gelesener `next` ist asynchron noch alter Titel; Reload zeigt den nächsten Scanauftrag. Kein Beleg für verlorene Eingaben |
| Messung + Reload + Export/Import | 123 bewusst durch 456 ersetzt; 456 wiederhergestellt. Originalfoto 730.724 Bytes, SHA-256 `14931a3c2b10d1e9ba6d6121db1d434d7a63d790d15f099d9b2928ace9a1a492` vor/nach Export gleich |
| Konflikt-/Prüfsummenimport | Same-ID abweichender Aufgabenstand abgewiesen; manipulierte Bildprüfsumme abgewiesen |
| Medien entfernen | Zuordnung entfernt, Foto bleibt im Export/Budget: 0 Referenzen, 1 Original. UXR-07 bleibt; kein Verlustbeweis, Benennung/Bereinigung offen |
| Teile-/Partnernachweis | Synthetischer Teileintrag ohne Partner/Medien akzeptiert; bleibt unreviewed. Verbindungsspezifischer Pflicht-/Offenvertrag weiter nötig |
| Menü / Tastatur | Mobiles Menü und Feldwechsel funktionieren. Hauptlauf erreicht `close-index`; Folgeprobe meldet `field-back` nach Tab. Keine vollständige Fokusfallen-/Screenreader-Abnahme daraus ableiten |
| WebGL-Ausfall | Verständliche Meldung, Quellen/Teilfinder erreichbar, 103 Quellenlinks bei Kumpf. Keine Behauptung, dass ausgefallene Modellregler damit optimal bedienbar wären |
| Live offline | **Umgebungsbedingt nicht verifiziert:** 150-s-Bereitschaftswartezeit abgelaufen. Explizite Diagnose zeigt ServiceWorker-Registrierung `SecurityError`: SSL-Zertifikatsfehler beim Abruf von `sw.js`. Online-Seiten wurden über Proxy mit Kontext-Zertifikatsausnahme geladen; diese reicht für den Worker nicht. Nicht als nachgewiesener produktiver Offlinefehler zählen |

Der letzte Punkt ist durch [offline-diagnostic.json](evidence/offline-diagnostic.json) belegt. Bereits bestehende CI-Offline-/Frischkontextimporttests auf `6a19868` sowie initial `7bff823` sind separat grün. Das ersetzt weder direkten Live-Offline-Nachweis in einem vertrauenswürdigen Browser noch Safari-/iPhone-Praxisprüfung. Keine Zertifikats-/Netzwerkschutzmaßnahme der Produktseite wurde verändert.

## Sichtprüfung und Barrierefreiheit

Die aktuellen Bilder für 320/390/768 Werkstatt, Desktop Feld und 200%-Start wurden visuell inspiziert. Sie bestätigen gekürzte Auswahllabel, vorangestellte Expertenregler, fehlende direkte Wasseraktion und die Titel-/Bildkollision. Weitere Seiten/Präferenzen wurden automatisiert erfasst; keine vollständige manuelle Prüfung aller Pixel behauptet. Der dokumentierte Fokus und beschriftete Checkbox-Hitbereich zählen mehr als die nackte 22-px-Checkbox. 40/46-px-Labels sind im Bericht getrennt von kleinen Quelllinks aufgeführt. Galerieüberlauf ist nicht gleich Seitenüberlauf. Kontrast, Screenreader, reales Touchverhalten, Kameraformate, Speicherdruck und Drucker wurden nicht vollständig abgenommen.

## Vorversuche

`browser-run.log`: erwartete Chromium-151-Binärdatei nicht vorhanden. Explizit installierten Chromium 141 verwendet; keine Version verschleiert. `browser/report.json`: direkter Chromium-Zugriff ohne Proxy scheitert mit ERR_EMPTY_RESPONSE. `browser-proxy/report.json`: Proxy-Zertifikat nicht vertraut. `live-browser` ist der anschließende erfolgreiche Online-Durchlauf mit dokumentierter Testausnahme. Diese Umgebungsbefunde werden nicht in die Produktdefektzahl eingerechnet.
