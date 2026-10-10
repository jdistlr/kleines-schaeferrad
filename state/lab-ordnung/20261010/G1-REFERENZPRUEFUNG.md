# G1 – Referenzprüfung und erste Klassifikation

Datum: 2026-10-10. Rein lesende Prüfung des Entwurfsbranches `design/lab-ordnung-entwurf-20261010`. Kein vollständiger Repository-Audit, keine kanonische Änderung.

## Reproduzierbare Prüfmethode

Sechs JSON-Verträge über GitHub am Entwurfsbranch geladen: `data/geometry.claims.json`, `data/components.json`, `data/source-analyses.json`, `data/knowledge-gaps.json`, `data/field-tasks.json`, `data/reconstruction-constraints.json`. IDs und Verweise in der gelesenen Datenmenge verglichen.

- 408 Aussagen (`claims`)
- 34 Komponenten/Gegenstände (`components`)
- 117 Quellenanalyse-Einträge (`sources`)
- 9 Wissenslücken (`gaps`)
- 21 Feldaufgaben (`tasks`)
- 0 nicht auflösbare `components[].claim_ids` in `claims[].id`
- 20 `claims[].provenance[].source_id`-Verweise ohne identische ID in `source-analyses.sources`. Beispiele: `CLAIM-0325 → EXT-VZO-INFO`, `CLAIM-0334 → CTX-USER-20261007`, `CLAIM-0335 → CTX-RETRIEVED-20261007`. **Nicht als defekte Quellen behaupten:** andere Register und externe Quellen können beabsichtigt sein; Herkunftspfad gezielt prüfen.
- 138 Claims mit `subject`, das nicht exakt `components[].id` entspricht (ohne slash-getrennte Subjects). Beispiele `CLAIM-0057 → REF-Welle`, `CLAIM-0061 → REF-Arme`. **Nicht automatisch fehlende Komponenten:** Referenzobjekte sind womöglich absichtlich separat.

## Beispiel Welle – erste Querverbindung

`COMP-SHAFT` enthält u.a. `CLAIM-0001` (historische Maßzahl 370, Einheit null, `documented-design`, Quellen `PHOTO-6816`/`PHOTO-6817`), `CLAIM-0253` (fotografierte verwitterte Oberfläche), `CLAIM-0336` (innere Zapfen-/Schlitzgeometrie unbekannt), `CLAIM-0346` (expliziter Konflikt 370/37 Skizze vs. generische Lager-/Bestandsangaben), `TH-20261009-13` (Fachauskunft zum konstanten hölzernen Wellenquerschnitt) und `TH-20261009-14` (zwei Eisenklammern pro Ende). Das sind **verschiedene Aussagearten**, keine pauschale Wahrheitsstufe.

`data/reconstruction-constraints.json:shaft` enthält Modellparameter, deren Maß-/Konturangaben ausdrücklich Kandidaten bleiben. Eine direkte Zuordnung `CLAIM-0001 → shaft.*` ist im begrenzten Adapter `src/control/property-readiness.mjs` nicht hinterlegt. Nicht aus dieser fehlenden Adapterzuordnung schließen, dass die Welle im 3D-Modell fehlt.

## Vorläufige Einordnung und nächste Prüfungen

1. Daten- oder Bedeutungsproblem **möglich**: gemischte Subjektnamensräume `REF-*` vs `COMP-*`; erst ihre beabsichtigte Semantik und referenzierte Quellen prüfen.
2. Vorhandene, schlecht dargestellte Beziehung: Claim-Provenienz, Geltungsbereich und Quellenart existieren, werden jedoch nicht als einfache Nachweiskette gezeigt.
3. Tatsächlicher Konfliktfall: `CLAIM-0346`; konkrete betroffene Maße und die jeweilige Quelle vor irgendeiner Bereinigung individuell prüfen.
4. Quellenregisterlücke **nicht erwiesen**: externe und Kontext-IDs müssen zunächst in anderen vorhandenen Beständen gesucht werden.
5. Originale `PHOTO-6816`/`PHOTO-6817` wurden in diesem Schritt nicht neu anhand der GitHub-Originalbytes geprüft. Keine neue Integritätsbestätigung behaupten.

## Korrekturdisziplin

Ein separates, zunächst nur vorgeschlagenes Korrekturprotokoll wird später je Eintrag enthalten: aktuelle ID, beanstandete Bedeutung, Originalbeleg, mögliche Korrektur, Auswirkungen auf andere Aussagen/Modelle, fachlicher Entscheider und Reviewstatus. Bis dahin keine Änderungen an `data/`, `evidence/`, F02/F03, Fachkorrekturen, lokalen Aufnahmen oder Modellgeometrie.

**G1 läuft. G2/G3/G4 nicht abgeschlossen.**
