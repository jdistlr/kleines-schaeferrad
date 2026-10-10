# Laborordnung – Entwurfsprüfung (10.10.2026)

Basis: PR #18, dokumentierter Commit c31bf8ae5cdc9d79090c1b53bfea1c867f255eb7. **Entwurf, keine Freigabe, keine kanonische Datenänderung.**

## Gezielte Diagnose
- `src/pages/control/evidence.astro` stellt Quellenregister, Fachreview und ein Claim-Ledger nebeneinander. Technische Prädikate bleiben englisch, während die Bedienung deutsch ist. Das erschwert die Antwort auf eine konkrete Untersuchungsfrage.
- `src/control/model.js` enthält bereits getrennte Komponenten, Claims, Quellen, Aufgaben und Lücken. Keine zweite Ontologie erforderlich.
- `src/control/property-readiness.mjs` mappt lediglich TH-25 bis TH-29 auf Rekonstruktionsparameter. Gleichheit von Zahlen ist ausdrücklich keine Prüfung der Mesh-Geometrie; andere Eigenschaften bleiben ohne Zuordnung.
- `data/components.json` enthält Komponenten-Konfidenzen, obwohl `data/geometry.claims.json` Eigenschaftsaussagen mit Scope und Provenienz besitzt. Komponenten-Konfidenz darf nicht als Gesamtwahrheit angezeigt werden.
- `state/control-plane/20261010/EXPERIENCE-ARCHITECTURE.md` beschreibt fünf Softwarebereiche; die neue Primärnavigation soll fachliche Fragen statt diese Bereiche zeigen.

## Fallakte: Welle / Achse (COMP-SHAFT)
- `CLAIM-0001`: historische Zeichnung, Längsmaßzahl 370, Einheit **nicht angegeben**, `scope=documented-design`, `as_built_eligible=false`. Originalbelege `PHOTO-6816`, `PHOTO-6817`, beide Fotos desselben Blattes, keine unabhängigen Bestätigungen. Im aktuellen Gespräch ist `IMG_6816.jpeg` und `IMG_6817.jpeg` als Bilddatei vorhanden; die Quellenanalyse `data/source-analyses.json` benennt Lesbarkeitsgrenzen.
- `CLAIM-0002`: historische Quermaßzahl 37, Einheit nicht gesichert; gleiche Belege und Grenzen.
- `CLAIM-0007`: zwei eingezeichnete Schlitzgruppen; dies belegt die historische Zeichnung, nicht automatisch die ausgeführte Welle.
- `CLAIM-0008`: drei gekreuzte Armdurchtritte pro Gruppe im schematischen Querschnitt; verdeckte Loch-/Keilform nicht maßhaltig ableitbar.
- `data/components.json`: `COMP-SHAFT` ist als physisches Teil verzeichnet; die land- und wasserseitigen Armzonen sind ausdrücklich keine bewiesenen separaten Naben.
- Fehlender Nachweis: aktuelle Endpunktmessung, Einheitenklärung, Passungen/Keile, Vergleich Zeichnung–Ist-Zustand und unabhängige Prüfung. **Keine Freigabe**.
- Modellbezug: für diese vier historischen Claims ist im begrenzten Adapter `src/control/property-readiness.mjs` keine explizite Eigenschaft-zu-Modell-Zuordnung enthalten. Das bedeutet nicht, dass die Welle im Modell fehlt; der konkrete Abgleich ist nicht nachgewiesen.
- Die GitHub-Originalbytes wurden in dieser Entwurfsprüfung nicht unabhängig per Hash verifiziert. Nicht als erneute Quellenfreigabe ausgeben.

## Kleine Wissensordnung (Darstellung des Bestands, kein neues Schema)
1. Gegenstand: bestehende Komponenten-ID.
2. Aussage: Claim-ID, Eigenschaft, Wert/Einheit und Bezug (Entwurf oder Ist).
3. Beleg: source_id, Originalansicht, Quelltyp und konkrete Bildregion.
4. Beurteilung: was folgt daraus, was gerade nicht, welche Einschränkung.
5. Modell: vorhandene Zuordnung, Annahme oder nicht nachgewiesener Abgleich.
6. Nächste Untersuchung: bestehende Aufgabe oder ausdrücklich vorgeschlagene Frage.

**Fehlender Beleg ≠ Widerspruch. Modellumsetzung ≠ Bestätigung. Historische Maßzahl ≠ Ist-Maß.**

## Entwurfsentscheidungen
- Ein Radbild als fachlicher Einstieg; Auswahl eines Gegenstands öffnet seine Untersuchung.
- Eine Aussage erhält einen eigenen, lesbaren Belegpfad und eine offene Frage.
- Originalfoto und Modell sind Arbeitsmaterial, keine Navigationshauptwelten.
- Wasserverhalten, Modellvergleich und Feldaufnahme erscheinen kontextbezogen an der passenden Fragestellung.
- Schmale Ansicht: dieselbe Reihenfolge vertikal; keine dauerhafte Seitenleiste.
- Keine Prozentwerte oder pauschalen Bauteil-Ampeln.

## Begrenzter Umsetzungsvorschlag
**Behalten:** bestehende IDs, Claim-/Source-Verträge, Field-Aufgaben, Modell und Wasserberechnung.
**Anders darstellen:** objektzentrierte Arbeitsfläche, deutsche Benennungen, Belegpfad und Eigenschaftsgrenzen.
**Fachlich zur Prüfung vorschlagen:** fehlende Einheiten/Endpunkte klären; konkrete Modellzuordnungen je Eigenschaft ergänzen, erst nach Review. Kanonische Daten unverändert lassen.

## Reviewfragen
1. Ist die Welle als erster Fall fachlich geeignet, oder soll die nächste Iteration einen Kumpf behandeln?
2. Soll der Einstieg primär über die Radansicht oder über eine Liste offener Untersuchungsfragen erfolgen?
3. Reicht die Trennung »Zeichnung belegt / Ist ungeprüft / Modellabgleich offen« als erste verständliche Darstellung?
