# Quellenzugriff: Originalarchiv lesbar, Remote-Sicherung blockiert

Stand: 2026-10-10. **EVIDENCE SOURCE ACCESS BLOCKED — REVIEW READY**

## Verifizierter Eingang

- ZIP: `SCHAEFERRAD-ORIGINALTRANSFER-76-FOTOS-1-VIDEO(1).zip`, 64.916.510 Bytes.
- ZIP-SHA-256: `0402a328404f7121b0679aaae0648f556197060a1a288a7d56d46efe10ac6ad9`.
- ZIP-CRC vollständig fehlerfrei; 78 Einträge: 76 JPEG, 1 MP4, 1 JSON-Inventar.
- Alle 76 JPEGs vollständig mit Pillow dekodiert; Video vollständig mit `ffmpeg -v error -i IMG_6857.mp4 -f null -` dekodiert, Exit 0, keine Fehlerausgabe.
- SHA-256 und Bytegrößen aller 77 Originaldateien stimmen mit `manifest/quelleninventur.json` überein. Maschinenlesbarer Nachweis: `original-transfer-checksums.json`.
- 74 unterschiedliche Foto-Bytefolgen: die Paare IMG_6829(1)/(2) und IMG_6838(1)/(2) sind bereits im Eingangsmanifest als byteidentisch ausgewiesen. Alle 76 Dateien bleiben erhalten. Keine Aussage über die Zahl unabhängiger Originalblätter.
- Fehlende separat angehängte JPEG-Pfade verhindern diese Archivprüfung nicht. Die separaten Anhänge wurden nicht als zusätzlich verifiziert ausgegeben.

## Repository und Erhaltung

PR #20 geprüft: offen, Draft, Head `665d8be543a276082826c212f16cfd5c231f9bcf`, Branch `work/evidence-graph-consolidation-20261010`, Basis `design/lab-ordnung-entwurf-20261010`. PR #19 geprüft: offen, Draft, Head `704c114a2ba0cd43db8e121df83b1981c7e9cace`. Git-ls-remote bestätigt den PR-20-Head vor und nach dem fehlgeschlagenen Upload.

Auftragsdatei und Evidence-README sowie Attribute und Deployment-Auslöser gelesen. Im Checkout und seinen Workspace-Vorfahren keine AGENTS.md gefunden. Separater Checkout schützt einen vorhandenen älteren Checkout mit uncommitteten Änderungen. Keine dieser Änderungen angefasst; die bisherige Branch-Historie bleibt erhalten. Der historische Transferblockadebericht wird nicht überschrieben.

## Tatsächliche Transfergrenze

Alle 77 Originale und das unveränderte Inventar wurden lokal unter `evidence/raw/originaltransfer-20261010/` abgelegt. Lokaler Sicherungscommit: `46184fe6d1aa2a5d3759affb62687b6222629d6f` (nicht auf GitHub).

Der autorisierte Git-Push auf genau diesen Branch scheitert mit:

```
fatal: could not read Username for 'https://github.com': No such device or address
```

Öffentliches Git-Lesen funktioniert; authentifiziertes Git-Schreiben ist in dieser Laufzeit nicht eingerichtet. Der GitHub-Connector kann Textberichte schreiben, bietet aber keinen direkten Upload lokaler Binärdateien. Sein Blob-Aufruf erwartet einen Inhaltsstring. Die Auftragsdatei verbietet ausdrücklich die Text-API als Ersatz für den Originaltransfer; deshalb keine Base64-Textumgehung. Dies ist keine fehlende Nutzerfreigabe und keine automatische Approval-Ablehnung.

**Die Originale sind weiterhin NICHT als auf GitHub gesichert bestätigt.** Dieser Bericht und die Prüfsummen sind keine Ersatzsicherung der Bild-/Videobytes. Ein SHA-256-Abgleich rückgelesener GitHub-Originale ist noch nicht möglich. Q0–Q3 und Stabilisierungsplan wurden deshalb nicht begonnen.

## Konkrete Fortsetzung

Benötigt wird eine Laufzeit mit authentifiziertem Git-Schreibzugriff auf `jdistlr/kleines-schaeferrad` und Zugriff auf das bereits bereitgestellte Archiv. Keine erneute Fotoaufnahme oder fachliche Entscheidung erforderlich. Archiv ist im aktuellen Anhang vorhanden; lokaler Commit ist nur ein temporärer Wiederaufnahmepunkt.

1. Aktuellen Remote-HEAD und etwaige neue Arbeit übernehmen, keinen Force-Push verwenden.
2. Originale aus dem unveränderten Archiv unter dem oben genannten separaten Pfad aufnehmen, vorhandene Originale nicht überschreiben. Mitgeliefertes Inventar unverändert mitführen.
3. Größen und SHA-256 gegen `original-transfer-checksums.json` prüfen; alle 77 Originale committen und auf den bestehenden Branch pushen.
4. Einen unabhängigen frischen Checkout von GitHub anlegen (nicht vom lokalen Repository, keine lokalen alternates). Dort das beiliegende `verify-original-transfer.py` ausführen. Commit-ID und vollständiges Ergebnis als Remote-Prüfartefakt sichern.
5. Erst nach 77/77 Remote-Übereinstimmungen Konsolidierung laut `state/NEXT-EVIDENCE-GRAPH-CONSOLIDATION-SESSION.md` fortsetzen.

Keine kanonischen Datenänderungen, keine Geometrieiteration, kein Merge, kein Deployment und keine Fachfreigabe. Die Sicherung von Originalbytes allein wäre noch keine fachliche Originalauswertung.
