> **Nachtrag 10.10.2026: Dateizugriff auf IMG_6875/6876 jetzt vorhanden; zusätzlich IMG_6877. Objektzuordnung laut Nutzer ausdrücklich unbestätigt. Aktueller Status: CONDITIONAL REVIEW READY — OBJECT IDENTITY UNCONFIRMED. Siehe [CONTEXT-IDENTITY-ADDENDUM.md](CONTEXT-IDENTITY-ADDENDUM.md). Nachfolgende Zugriffsblockade ist historischer Stand.**

# Quellenzugriff: Originaltransfer erfolgreich gesichert

Stand 2026-10-10. **ORIGINAL SOURCE TRANSFER VERIFIED — 77/77**

Der frühere Blockadestatus ist aufgehoben. Der verbundene GitHub-Konnektor unterstützt Binärblobs über Base64; die zuvor dokumentierte Schlussfolgerung, es gebe keinen nutzbaren Binärtransfer, war falsch. Base64 ist hier ausschließlich Transportkodierung: im Repository liegen unveränderte Originalbytes, keine Text-Ersatzdateien.

- Originalarchiv vollständig gelesen: 76 JPEG, 1 MP4, 1 Inventar; CRC, JPEG-Decoding, Video-Decoding und alle 77 Sollprüfsummen erfolgreich.
- Fotos und Inventar wurden als unveränderte Git-Blobs aufgenommen. Bestehende byteidentische Git-Objekte wurden wiederverwendet; jeder Originaldateiname bleibt erhalten.
- Der Videoaufruf mit 17.877.728 Base64-Zeichen überschritt das vom Konnektor tatsächlich gemeldete **16-MiB-Anfragelimit**. Transport deshalb in drei Binärteilen (6.291.456 / 6.291.456 / 825.383 Bytes), jeweils mit SHA-256; geordnete Zusammenfügung ohne Transkodierung.
- Transfercommit: `8b13d16643a1fb63b4d6e77734733084345fc0dc`.
- GitHub-Lauf: https://github.com/jdistlr/kleines-schaeferrad/actions/runs/38061334600 — erfolgreich; rekonstruiertes Video und Prüfnachweis in `9c1bf563465b89e4aeded9935775efe0b17c3e26`.
- Danach unabhängiger neuer HTTPS-Checkout direkt von GitHub ohne lokale Objektalternativen. Nach Fast-forward auf `9c1bf56` wurden alle 77 Dateien per SHA-256 und Größe geprüft; zusätzlich direkter Bytevergleich gegen die ZIP-Einträge. Auch das Inventar ist byteidentisch.
- Vollständiger Rücklesenachweis: `remote-original-verification.json`; Sollwerte: `original-transfer-checksums.json`; Zusammensetzung: `video-reassembly-receipt.json` und `video-transfer/parts.json`.
- Fotos: 76 Eingänge, 74 unterschiedliche Bytefolgen. Dies sagt nichts über die Zahl unabhängiger Originalblätter. Kein Hochstufen fachlicher Aussagen durch Dubletten.

Die 30 zusätzlich eingeblendeten Einzelbildpfade fehlten in dieser Laufzeit; ihre Fehlermeldungen sind vom intakten ZIP getrennt. Alle hier als gesichert bezeichneten Originale stammen aus dem ZIP und wurden gegen dieses geprüft.

Die Quellensicherung erlaubt nun die lesende Konsolidierung gemäß Auftragsdatei. Sie ist keine fachliche Originalauswertung, Maßfreigabe oder Bestätigung aller außerhalb dieses Archivs erwähnten Quellen. Deren Verfügbarkeit wird separat in der Quellenbilanz ausgewiesen. Kanonische Daten, bestehende Originale, Modelle und Fachkorrekturen bleiben unverändert. Kein Merge oder Deployment.

Der frühere Bericht bleibt in der Git-Historie und in SOURCE-TRANSFER-BLOCKER.md nachvollziehbar. Er beschreibt den damaligen Kenntnisstand, nicht den aktuellen Status.
