# NEXT — KNOWLEDGE GRAPH & EVIDENCE CONSOLIDATION

**Arbeitsauftrag für eine gesonderte umfangreiche Work-/Astra-Session.** Stand: 2026-10-10. Repository ausschließlich `jdistlr/kleines-schaeferrad`.

## Ausgangspunkt und Sicherheitsgrenzen

Branch `work/evidence-graph-consolidation-20261010`, angelegt vom geprüften Entwurfsbranch `design/lab-ordnung-entwurf-20261010` (PR #19). Zuerst Remote-HEAD, PR #19 und Repository-Anweisungen selbst prüfen. Bereits vorhandene Arbeit übernehmen, nicht neu beginnen. Keine Änderungen an main, PR #18, PR #19, Preview, kanonischen Daten, F02/F03, 39 Thorsten-Fachkorrekturen, Geometrie, Modellparametern, lokalen Aufnahmen oder Deployments. Kein Merge, keine produktive UX, keine Migration. Nur Dokumente, nachvollziehbare Prüfartefakte und gegebenenfalls isolierte lesende Prüfskripte auf diesem Branch.

## Kritische Eingangsbedingung

Im Gespräch wurden 76 Fotoeingänge in acht Paketen und ein Video (`IMG_6857.mp4`) lokal inventarisiert. Die Dateien/Manifeste sind **nicht als auf GitHub archiviert nachgewiesen**. Die ursprünglichen Chat-Anhänge und lokale Sandbox-Dateien sind nicht automatisch in einer neuen Session verfügbar. Deshalb zuerst tatsächliche Originalverfügbarkeit, vorhandene Archivdateien, Prüfsummen und die übergebenen Manifeste prüfen. **Kein Quellen-Audit als abgeschlossen ausgeben, wenn Originalbytes fehlen.** Fehlende Originale in einem Transfer-/Zugriffsgate benennen; niemals aus Chat-Beschreibungen Originalprüfung fingieren. Binärdateien nur über einen verifizierten unterstützten Transferweg aufnehmen; keine Text-API als Ersatz.

## Arbeitspakete

1. **Q0 Quellenbilanz:** Alle vorhandenen Foto-/Video-/Zeichnungs-/Mess-/Aussagequellen aus Repository und zugänglichen Originalen inventarisieren. SHA-256-Dubletten, verschiedene Fotos desselben Blattes, Dokumentversionen, unabhängige und abgeleitete Quellen trennen. Bestehende `PHOTO-*`/Quellen-IDs wiederverwenden. Nicht zugängliche Quellen und nicht verifizierbare Beziehungen sichtbar kennzeichnen.
2. **Q1 Tatsächlichen Graphen ermitteln:** Vorhandene Datenverträge und fachliche IDs (`COMP-*`, `CLAIM-*`, `GAP-*`, `TASK-*`, `CONFLICT-*`, Modellbezüge) lesend analysieren. Knoten-/Kantentypen, Referenzintegrität, semantische Doppelungen, ungestützte Aussagen, unbeabsichtigte Beweiszirkelschlüsse und Quellengrenzen mit Dateipfaden und IDs dokumentieren. Keine neue Parallelontologie.
3. **Q2 Beweisketten an konkreten Fällen:** Welle/Armverbindung, Kumpf und Kranz exemplarisch verfolgen: Originalstelle → unmittelbare Beobachtung → konkrete Aussage → Beurteilung/Geltungsgrenze → Modellumsetzung/Approximation → Lücke → Untersuchung/Entscheidung. Fachlich bestätigte Bauweise ist kein gemessenes Ist-Maß; Modellumsetzung ist kein Beleg; fehlender Beleg kein Widerspruch; kein pauschaler Bauteil-Wahrheitsstatus und keine Vertrauensprozente.
4. **Q3 Asynchrones Entscheidungsregister:** Bestehende 21 Feldaufgaben und neun Lücken aus `state/lab-ordnung/20261010/G1-G2-AUFGABEN-LUECKEN-MATRIX.md` als Ausgangspunkt; keine Duplikate. Für Thorsten entscheidungsreife Fragen mit Quellen, alternativen Deutungen, Vorentscheidungen, Auswirkungen und Option 'nicht entscheidbar' aufbereiten. Unreife Fälle als Aufnahme-/Messauftrag oder Quellennachforderung führen. Keine Antwort oder Freigabe durch Assistenz.
5. **Stabilisierungsplan:** Kleine, priorisierte Korrekturliste: behalten / anders darstellen / fachlich zur Entscheidung vorlegen / erst nach Freigabe kanonisch korrigieren. Keine tatsächliche Datenkorrektur.

## Prüfpunkte

- Beweisstärke darf nicht durch mehrere Aufnahmen desselben Originals künstlich wachsen.
- Datum, Urheber, Aufnahmezustand und Perspektive nur angeben, wenn belegbar.
- Skizzenmaß, Materialempfehlung, Ist-Messung und angenommener Modellparameter dürfen nicht zusammenfallen.
- Videozeitpunkte als Verweise auf dasselbe Video, nicht als unabhängige Quellen behandeln.
- Bestehende 39 Fachkorrekturen und deren Begründungen nicht überschreiben.
- Jede behauptete Kante bekommt Quelle und Relationstyp; abgeleitete Beziehungen werden von belegten getrennt.

## Reviewpaket

Unter `state/evidence-consolidation/20261010/` ablegen: `SOURCE-ACCESS-GATE.md`, `SOURCE-INVENTORY.md`, `GRAPH-CONTRACT-AND-INTEGRITY.md`, `EVIDENCE-CHAINS.md`, `THORSTEN-DECISION-BILL.md`, `STABILIZATION-PLAN.md`, `REVIEW-SUMMARY.md`. Ergebnisse nur soweit belegen, wie Quellen tatsächlich verfügbar sind; bei fehlenden Binärquellen ausdrücklich CONDITIONAL REVIEW READY statt Vollständigkeit behaupten. Änderungen committen/pushen, eigenen Draft-PR gegen `design/lab-ordnung-entwurf-20261010` erstellen oder aktualisieren. Keine Merge-/Deployment-Aktion.

**Stop:** `KNOWLEDGE GRAPH & EVIDENCE CONSOLIDATION REVIEW READY` nur bei tatsächlich abgeschlossenen Gates; andernfalls `EVIDENCE SOURCE ACCESS BLOCKED — REVIEW READY` mit präziser Nachforderung. Danach auf Nutzerentscheidung warten.
