# ITER-002 — Astra Comparison Review

**ASTRA COMPARISON REVIEW READY**

Repository: `jdistlr/kleines-schaeferrad` · Branch: `work/astra-abgleich-iter002-20261009` · Ausgangs-main: `f7b9185517856b7881530ba9d0553f170787cb09` (Merge PR#13). Datum:2026-10-09.

Der Vergleichsauftrag aus `state/ASTRA-ABGLEICH-20261009.md` ist abgearbeitet. Die dortige frühere Fork-/Intakebasis wurde durch den ausdrücklichen Nutzerauftrag ersetzt. Es wurden ausschließlich Ergebnisse unter diesem ITER-002-Ordner geschrieben. Runtime, kanonisches Truth Model und bestehende Evidenzregister bleiben unverändert.

## Ergebnis

- 65 Originaldateien visuell ausgewertet und mit SHA-256/Git-Blob-Hash geprüft;63 unabhängige Bildpayloads. Zusätzlich historische Trog-/Rinnen-/Kranzzeichnungen und Scanansichten geprüft.
- 39/39 Fachangaben einzeln gegen tatsächlich instanziierte V3-Geometrie und Generatorcode abgeglichen.
- 14 dokumentierte Fotoableseversuche: bedingte Lesebänder einschließlich Nagellängen-/Kopf-/Schaftbezug und Schetternvorlage; ausdrücklich erfolglose Ablesungen bei verdeckten Endpunkten.
- Sieben technische Modell/Originalfoto-Vergleichstafeln plus Scan-Suchansicht. Kein Foto-Fit, keine korrigierte Geometrie.
- Property-Delta, verbleibende Fragen und konkrete Umsetzungsreihenfolge einschließlich abhängiger Kontakte gesichert.

## Wesentliche Befunde

Lichte Kranzweite tatsächlich1,01m statt1,80m; Mittelebenen müssen künftig1,94m statt1,15m betragen. Axiale14cm sind bereits richtig. Armenden liegen an Segmentstößen statt Segmentmitten. Sitzverstärkung/-sicherung, Schetternbretter, U-Holzbänder und vier Wellenschellen fehlen. Die Holzwelle ist fälschlich verjüngt, Lager sind Metallkandidaten. Aktive Nagelschäfte18mm statt26mm und Köpfe48mm statt40mm; bisherige24-mm-Löcher müssen mitgeprüft werden. Radbock und A-Bock/Rinnenstoß sind im synthetischen Rahmen nicht richtig abgebildet.

Die vorhandenen Bilder erlauben keine sichere vollständige A-Bock-Standweitenberechnung und keine metrische Scanregistrierung. Das obere A-Beinende ist bei Skalenwert147–151cm lesbar; der Fuß-/Nullbezug bleibt verdeckt. Ergebnisse werden mit diesen Grenzen zur Prüfung vorgelegt, nicht als As-built-Modell freigegeben.

## Einstieg in die Unterlagen

1. [EVIDENCE-COMPARISON.md](EVIDENCE-COMPARISON.md) — vollständige Matrix und Abhängigkeiten.
2. [CONSTRAINT-DELTA.json](CONSTRAINT-DELTA.json) — alle39 Properties, Originalclaims und Ist-Befunde.
3. [PHOTO-READOUTS.json](PHOTO-READOUTS.json), [PHOTO-OBSERVATIONS.json](PHOTO-OBSERVATIONS.json) — Ablesungen/Unsicherheit und65 Bildnachweise.
4. [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md), [SCAN-COMPARISON.md](SCAN-COMPARISON.md), [IMPLEMENTATION-SEQUENCE.md](IMPLEMENTATION-SEQUENCE.md).
5. [views/manifest.json](views/manifest.json), [evidence/runtime-audit.json](evidence/runtime-audit.json), [VALIDATION.json](VALIDATION.json), [REPRODUCE.md](REPRODUCE.md).

Keine Modellkorrektur, keine kanonische Promotion, kein Deployment, kein Merge. Der vollständige Modelliterations-/Exportzyklus aus PROTOCOL.md wurde entsprechend dem engeren Nutzerauftrag nicht ausgeführt.
