> **Neue Fachinformationen 09.10.2026:** Der [Konstruktionsbeitrag](../../docs/FACHBEITRAG-KONSTRUKTION-20261009.md) ergänzt diese V3-Baseline. Neueste explizite Nutzerkorrekturen haben Vorrang; siehe [Astra-Abgleich](../ASTRA-ABGLEICH-20261009.md). Supplemental Intake ist noch nicht in alle kanonischen Daten oder das 3D-Modell übernommen.

# BASELINE V3 — Local Expert Refresh

Datum: 2026-10-08  
Branch: `work/baseline-refresh-thorsten-20261008`

## Verdict

**BASELINE V3 READY FOR RECONSTRUCTION**

Diese Baseline ersetzt nicht die Samstag-Vor-Ort-Vermessung. Sie ersetzt jedoch den bisherigen Wissensstand überall dort, wo lokale Fachauskunft von ThorstenHalsch frühere externe Analogien oder unbelegte Modellannahmen korrigiert.

## Authority

ThorstenHalsch wird für diesen Wissensstand als **Wasserrad-Mitinitiator / lokaler Fachkenner** geführt.

Prioritätsregel:
1. direkte aktuelle Messung / registrierte Geometrie,
2. direkte aktuelle Beobachtung,
3. lokale Fachauskunft direkt beteiligter Fachleute,
4. lokale historische Zeichnung,
5. unregistrierter lokaler Scan,
6. externe Analogie,
7. synthetische Rekonstruktion.

Details: `data/evidence-authority.json`.

## Neue kanonische Baseline-Claims

### Referenz-Kumpf
- 12 Dauben.
- 1 Boden.
- Boden sitzt in einer Einfräsung/Nut der Dauben.
- 3 Metallbänder.
- Unterschiedliche historische Band-/Ringderivate wurden gefertigt.
- Der fotografierte Kumpf ist laut Fachkenner die passende Maßreferenz für die zugehörige Variante.

### Kumpfbefestigung
- 2 der 12 Dauben haben je 2 Löcher.
- 2 Kumpfnägel pro Referenzbefestigung: 1 lang, 1 kurz.
- Kumpfnägel führen durch die gelochten Dauben und befestigen den Kumpf am Krümmling.
- Benachbarte Kümpfe überlappen.
- Die Überlappung erklärt laut Fachauskunft die unterschiedlichen Nagellängen.

### Schaufeln
- Lokale Fachkorrektur: Schaufelbretter stehen im 90°-Winkel zum Rad.
- Exakter geometrischer Referenzbezug ist noch zu definieren/prüfen; daher noch keine automatische Modellrotation.

## Neu geordnete Unsicherheiten

### Nicht mehr primäre Hypothese
„Lang/kurz bestimmt die Kumpfneigung“ wird herabgestuft.

### Primäre Funktionsbaseline
„Lang/kurz wegen Überlappung benachbarter Kümpfe“ wird als lokale Expertenaussage priorisiert.

### Weiter offen
- Zuordnung der vier Lochpositionen zu den zwei Nagelwegen.
- Nagellängen, Querschnitte, Krümmung und Einsteckrichtung.
- Überlappungsrichtung und Überlappungsmaß.
- Übertragbarkeit des Referenz-Kumpfaufbaus auf jeden aktuellen Kumpf.
- Zuordnung historischer Bandlängen zum Referenz-Kumpf.
- geometrische Definition der 90°-Schaufelkorrektur.
- dedizierte Nagel-/Schaufel-Punktewolken.
- aktuelle Stückzahlen und metrische Ist-Maße.

## Baseline-Dateien

- `data/evidence-authority.json`
- `data/geometry.claims.json`
- `data/components.json`
- `data/assembly.graph.json`
- `data/conflicts.json`
- `data/knowledge-gaps.json`
- `data/kumpf-fastener-hypotheses.json`
- `data/reconstruction-evidence-map.json`
- `data/source-analyses.json`
- `evidence/contributions/kumpf-20261008.json`
- `evidence/contributions/schaufelstellung-20261008.json`
- `docs/reconstruction/SOURCE-RECONCILIATION.md`

## Konsequenz für Astra

Der nächste Astra-Lauf darf nicht aus dem alten V2-Kumpf-/Stiftmodell fortschreiben, ohne diese Baseline neu einzulesen.

Pflicht-Rekalibrierung:
1. Referenz-Kumpf geometrisch aus den vier neuen Fotos rekonstruieren.
2. 12 Dauben + Nutboden + 3 Metallbänder explizit abbilden.
3. Zwei Befestigungsdauben mit vier Lochpositionen modellieren.
4. Lang-/Kurz-Kumpfnagel als Kumpf→Krümmling-Verbindung mit Überlappungsconstraint neu aufbauen.
5. Drei benachbarte Kümpfe als Überlappungsgruppe modellieren und Montage-/Umfangsrichtung als Kandidat testen.
6. Schaufelstellung gegen Thorstens 90°-Korrektur mit explizitem Koordinatenbezug neu untersuchen.
7. Erst danach Wasseraufnahme/Ausschüttung und Betriebsanimation neu kalibrieren.
8. Truth Model und Brute-Force Model getrennt fortführen.

## Stop-Gate

Baseline-Arbeit ist abgeschlossen, wenn:
- atomare Claims integriert,
- Komponenten/Graph aktualisiert,
- Konflikte neu bewertet,
- alte Hypothesen neu gerankt,
- offene Samstag-Fragen präzisiert,
- Quelle/Autorität dokumentiert,
- Konsistenztests grün sind.
