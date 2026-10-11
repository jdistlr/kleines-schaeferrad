> **Abgelöst am 11.10.2026.** Diese Datei ist kein Arbeitsauftrag mehr. Maßgeblich sind [AGENTS.md](../AGENTS.md), der [Wissenskern](../kern/README.md) und der [Ordnungsplan](../docs/ordnung/PLAN.md). Neue Fachangaben nicht hier anhängen, sondern wie in AGENTS.md beschrieben in `kern/` eintragen.

# NEXT WORK SESSION

Branch: `work/pre-disassembly-baseline-20261007`. Ausgangspunkt dieser Understanding-Session: `806819dc599c640ca6ec9c87e01efc9c322f5892`; danach den aktuellen Branch-Head und Remote-Archivnachweis prüfen.

Gate: **BASELINE UNDERSTANDING READY** nach erfolgreichem Writeback/Archivnachweis. Hier stoppen. Keine automatische Modellierungsfortsetzung.

## Exakter Fortsetzungszustand

43 Rohdateien vollständig inventarisiert/analysiert; zehn zuvor nicht registrierte Fotos aufgenommen. Alle bisherigen 33 Hashes stimmen. Originalbytes unverändert unter `evidence/raw/`; nach Checkout mit `python scripts/verify_evidence.py` prüfen. Alle 40 JPEGs, Screenshot, PLY/GLB wurden individuell geprüft. Frühere Contact Sheets nicht erreichbar; neue vollständige Sheets sind Derivate. Historische Chats nur sichtbarer Auszug + sekundäre Zusammenfassung, kein vollständiges Transkript.

Claims/Quelle/Gruppen: `data/geometry.claims.json`, `data/source-analyses.json`. Ontologie/Graph: `data/components.json`, `data/assembly.graph.json`. Historische und extern erwartete Slots sind keine aktuellen Teile. Aktuelle physischen Instanzenliste bewusst leer. Welle vs Armzone und durchgehender Arm vs Speichenende nicht wieder vermischen.

Konflikte: `data/conflicts.json`. Feldframe: `data/reference-system.json`; alle physischen Maße/Transforms null. Scan-Dateistatistik ist measured/digital-artifact-only. Achsenkandidat PLY→GLB unterstützt, mechanische Registrierung ausstehend. Keine Rohgeometrie repariert/segmentiert/modelliert.

## Nächste autorisierte Phase erst nach Human Gate

1. Vier Fragen aus `docs/HUMAN-CALIBRATION.md` beantworten lassen; Antworten mit Person/Datum und Foto-/Teilbezug als eigene Claims führen.
2. Vor/während der Demontage GAP-01 bis GAP-08 aus `docs/CAPTURE-BEFORE-DISASSEMBLY.md` erfassen. Termine/Seiten/Nummern vor Ort bestätigen.
3. Neue Messungen und Teilbilder unverändert ingestieren, vollständige physische KS-IDs und Partner-/Ereignisregister anlegen. Zeichnungsvarianten erst nach Gegenprüfung auswählen.
4. Danach separates Registrierungs-/Rekonstruktions-Gate planen; keinen finalen Viewer, Splats oder ästhetisches Modell vorziehen.

Keine Quelle gewinnt automatisch. Fehlende Werte null halten; Konflikte nicht löschen. Bei neuem Material nur betroffene Claims weiterentwickeln, Originale und frühere Interpretation nachvollziehbar behalten.
