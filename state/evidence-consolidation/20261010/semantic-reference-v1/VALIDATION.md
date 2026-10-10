# Prüfung und Reproduktion

Die Prüfung betrifft diese Reviewänderung gegenüber `727a0248c0234641453a08e4ae3984e27c9f970b`, nicht eine fachliche oder räumliche Freigabe. Alle Befehle im Repositorywurzelverzeichnis; vollständige Git-Historie und archivierte Quellen erforderlich.

```sh
python state/evidence-consolidation/20261010/semantic-reference-v1/verify-field-pack-reference.py
python state/evidence-consolidation/20261010/semantic-reference-v1/verify-reference-v1.py
python scripts/verify_evidence.py
node --test tests/integration-recovery.test.mjs tests/control-context.test.mjs tests/field-kit.test.mjs
git diff --check
```

Umgebung des dokumentierten Laufs: Python 3.12.14, Node 24.19.0, ReportLab 4.4.9, Pillow 12.3.0, DejaVu Sans. Die Node-Abhängigkeit `three` wurde aus dem bereits versionierten `vendor/three-0.180.0.tgz` lokal bereitgestellt; keine Änderung an Abhängigkeitsverträgen.

| Nachweis | Ergebnis / Bedeutung |
|---|---|
| `validation.json` | 62 Prüfungen: genaue erlaubte Deltas, Referenzen, Geltung, Quellenhashes und Bestandserhalt. `head_at_run` benennt den HEAD vor dem Sicherungscommit; geprüfte Eingaben sind zusätzlich mit SHA-256 aufgeführt. |
| `evidence-verification.log` | Unveränderter Bestandsprüfer: 43 historische Baseline-Originale, vier beigetragene Originale, zehn Ableitungen, 408 Claims, 117 Quellenanalysen und Graph-/Konfliktverweise. Die weiteren 77 Transferdateien prüft der v1-Prüfer. |
| `existing-tests.log` | Elf vorhandene Tests bestanden; darunter alle 39 Fachkorrekturen, Quellenadapter und Feldpaket-Vertrag. Die bestehenden Armkandidatentests laufen unverändert im Speicher; keine Geometrieiteration oder Artefakterzeugung. |
| `field-pack-equivalence.json` | Vorhandener PDF-/Visual-Renderer mit altem und neuem Aufgabenvertrag nur in Scratch. Kein Geometrieexport. Ausgabebytes beider Vergleichsläufe identisch; einzige Manifestdifferenz `task_source_sha256`. Keine neue visuelle Freigabe und keine Behauptung, dass diese Renderer-Version identische Bytes zum historischen Build erzeugt. |
| Bestandserhalt | Alle 1.115 Basisdateien erhalten: 1.102 byteidentisch, vier vollständig begrenzte JSON-Deltas und neun ausschließlich vorangestellte Hinweise. Alle ursprünglichen Berichtstexte bleiben erhalten. Neue Dateien nur im v1-Reviewverzeichnis. |

Die zwei Prüfer in diesem Verzeichnis lesen den Produktionsbestand ausschließlich. Der Feldpaketvergleich verwendet temporäre Kopien und lesende Verknüpfungen auf unveränderte Originale/Referenzbilder; sein Generator darf nur die temporären Ausgaben verändern. Alte Schutzskripte mit früheren Baselines wurden nicht umgeschrieben, um neue autorisierte Änderungen zu verstecken.

Nicht geprüft/freigegeben: Video-Toninhalt, Objektidentität IMG_6875–6877, alle unklaren Handschriftdetails, aktuelle Feldmaße, verdeckte Partnerflächen und reale Topologie. Kein umfassender Produkt-/Browser-Abnahmelauf. F02/F03, Produktcode, Geometrie, bestehende Zeichnungen und Originalquellen sind durch den Bytevergleich geschützt.
