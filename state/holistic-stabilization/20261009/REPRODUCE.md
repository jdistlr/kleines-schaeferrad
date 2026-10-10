# Reproduktion und Evidenzindex

Alle Befunde beziehen sich auf Produktstand `118e5f7`, inhaltlich identisch mit Auditstart `7bff823` außerhalb des Arbeitsauftrags. Auditdateien sind additiv. Erhebung 09.10.2026 UTC, Abschluss teilweise 10.10.2026 Europe/Berlin. Lokale Build-Log-Uhrzeit ist Umgebungszeit; GitHub- und Browserzeiten sind ISO/UTC.

## Lokal

Repository am angegebenen Stand auschecken, Node 24 (hier 24.19.0), `npm ci --no-audit --no-fund`, Python mit ReportLab und DejaVu-Schriften. Die konkrete Umgebung wird in `evidence/environment.json` festgehalten. Von Repositorywurzel:

```sh
python scripts/verify_evidence.py
node --test tests/*.test.mjs
npm run check
npm run build
node state/holistic-stabilization/20261009/evidence/probe.mjs
python state/holistic-stabilization/20261009/evidence/canonical-audit.py
node state/holistic-stabilization/20261009/evidence/legacy-domain.mjs
```

Die Modellprobe liest GLBs/Views und Runtime; sie exportiert keine Modelle und erzeugt keine neue Geometrieiteration. `canonical-audit.py` braucht die historischen Remote-Branches für PR #14-Ansichtszuordnung und Branchinventar. `protected-hashes.json` erfasst unveränderte geschützte Eingaben. `preservation-final.json` vergleicht sie und den Git-Diff gegen main.

`npm run test:reconstruction` ist separat mit Exit 1 ausgeführt worden. Der Befehl überschreibt normalerweise `state/reconstruction/candidate-audit.json`. Für diesen Audit wurden die ursprünglichen Bytes vor dem Lauf gesichert und im finally-Pfad wiederhergestellt; das neu erzeugte Ergebnis liegt ausschließlich in `legacy-reconstruction-result.json`. Für eigene Wiederholung eine wegwerfbare Arbeitskopie verwenden. Nicht über historische Auditnachweise schreiben.

## Live-Browser

Playwright 1.62.1 liegt extern zum Repository unter `UX_PLAYWRIGHT`; `KS_CHROMIUM_PATH` zeigt explizit auf vorhandenen Chromium Headless Shell 141.0.7390.37. Die Auditkopien ergänzen nur Browserpfad, konfigurierten Umgebungsproxy und `ignoreHTTPSErrors` in frischen Testkontexten. Keine Produktdatei verändert.

```sh
UX_OUTPUT=state/holistic-stabilization/20261009/evidence/live-browser node state/holistic-stabilization/20261009/evidence/browser-audit.mjs
UX_OUTPUT=state/holistic-stabilization/20261009/evidence/live-followup node state/holistic-stabilization/20261009/evidence/followup.mjs
node state/holistic-stabilization/20261009/evidence/live-compare.mjs
node state/holistic-stabilization/20261009/evidence/offline-diagnostic.mjs
```

Die beiden Browservariablen vorher passend zur eigenen Installation setzen; kein Browserdownload ist implizit Teil dieses Audits. In einer normalen vertrauenswürdigen Netzwerkumgebung ist keine Zertifikatsausnahme erforderlich. Onlinebeobachtung und TLS-/ServiceWorker-Blockade sind getrennt dokumentiert. Alte Fehlversuche werden unter `browser/`, `browser-proxy/` und den jeweiligen Logs bewahrt. Keine erneute Vollmatrix nötig, nur konkrete verbleibende Grenzen gezielt prüfen.

## GitHub-Nachweise

- `github-runs-initial.json`: die 30 zum Abruf neuesten Runs, **keine Vollhistorie** aller 267 Runs.
- `github-jobs.json`: konkrete Schritte/Outcomes für fehlgeschlagene 37987615114 / 37992980382, erfolgreiche #15-Endmatrix 37993441445, initiale #16-Matrix 37995923429, main Build+Deploy 37994601533.
- `ci-job-*-failure-excerpt.log`: ursprünglicher Timeout bzw. Assertion 38/36, keine verallgemeinerte Ursache allein aus Logs behauptet.
- `open-prs-initial.json`, `branches.json`: offene Reviews und alle erfassten Remote-Branches mit SHA/Differenz. Symbolischer origin/HEAD-Zeiger ist kein eigener Arbeitsbranch.

Die Originaldateien der in der Chatnachricht genannten 30 Bilder fehlen an den übergebenen Scratchpfaden. Für diesen Audit wurden **vorhandene versionierte Repositoryoriginale** verwendet und gehasht; kein neuer Intake dieser Anhänge und keine Gleichheit mit den fehlenden Scratchkopien behauptet. Die sieben Archivvideos wurden nicht angesehen; PR #12 enthält dafür nur den noch auszuführenden Auftrag.

## Grenzen

Keine unabhängige Neuinterpretation sämtlicher 65 Fotos/39 Ansichten, sondern Quellen-/Ableitungs-/Hashaudit mit Modellproben und aktuellen UI-Screenshots. Keine physische Safari-, Kamera-, Zweitgeräte-, Speicherdruck-, Papier-, Engineering- oder Hydraulikfreigabe. Die vollständigen Prüfstatus sind im Verdict und in der CI-Matrix ausgewiesen. Bei der schematischen Messkarte wurden keine Bauteilmaße aus Pixeln gewonnen.
