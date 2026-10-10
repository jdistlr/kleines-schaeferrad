# Control Plane Preview Deployment — BLOCKED

Stand: 2026-10-10. Ergebnis: **MODEL CONTROL PLANE PREVIEW DEPLOYMENT BLOCKED**.
**MODEL CONTROL PLANE PREVIEW DEPLOYMENT READY ist nicht erreicht.**

## Verifizierter Ausgangspunkt

- Repository: `jdistlr/kleines-schaeferrad`.
- PR [#18](https://github.com/jdistlr/kleines-schaeferrad/pull/18) ist offen und nicht gemergt.
- Geprüfter PR-HEAD: `c190647b7fee3ff413c30e0f136b1882d47c7a14`.
- Getesteter Anwendungscode: `51221b9d0e6ad8aed1fb714f7888f1a38bf0e3c5`.
- Remote-main: `606908bfe8cf1ab0560b337f37d92dd90d320dee`.
- Bestehender Produktionslauf [38033011709](https://github.com/jdistlr/kleines-schaeferrad/actions/runs/38033011709): completed/success, main 606908b; aktueller Status dieses konkreten Laufs erneut abgefragt. Keine Behauptung über sämtliche späteren Läufe.
- Preview-Deploymentlauf: **keiner gestartet**.
- Veröffentlichte Preview-URL: **keine**.
- Diese Sitzung ändert ausschließlich diese Dokumentation; weder Anwendung, Geometrie, Evidenzen, Fachkorrekturen noch produktive Deploymentkonfiguration wurden geändert.

## Pages-Prüfung und Entscheidung

[pages.yml am geprüften main](https://github.com/jdistlr/kleines-schaeferrad/blob/606908bfe8cf1ab0560b337f37d92dd90d320dee/.github/workflows/pages.yml) baut PRs, veröffentlicht sie jedoch nicht. Der Deploy-Job ist auf Nicht-PR-Ereignisse und `refs/heads/main` beschränkt. Er verwendet `actions/deploy-pages@v4` und das Environment `github-pages`. Ein isoliertes zweites Hostingziel ist nicht konfiguriert.

Die Repository-Pages-Settings konnten über den verfügbaren GitHub-Connector nicht gelesen werden: GET `/repos/jdistlr/kleines-schaeferrad/pages` wurde als nicht unterstützter Endpoint abgewiesen. Das ist eine Zugriffsbeschränkung dieses Connectors, kein Nachweis einer fehlenden Pages-Installation. Die Beurteilung beruht auf Workflow, Konfiguration, Produktionslauf und offiziellen Plattformangaben.

Die [offizielle deploy-pages-Dokumentation](https://github.com/actions/deploy-pages#inputs-) bezeichnet den Preview-Eingang weiterhin als nicht öffentlich verfügbare Alpha. Eine bloße Umbenennung des GitHub-Environments schafft kein nachgewiesenes unabhängiges Pages-Hostingziel. Daher wurde kein solcher Versuch gestartet.

Ein gemeinsames Pages-Artefakt mit Produktion plus Preview-Unterordner müsste das produktive Pages-Deployment erneut veröffentlichen. Dies widerspricht dem ausdrücklichen Verbot eines produktiven Deployments. Ein zweites GitHub-Repository wäre außerhalb des ausdrücklich erlaubten Repositoryumfangs.

## Tatsächliche Isolationsrisiken

Am unveränderten PR-HEAD geprüft:

| Stelle | Befund | Konsequenz |
| --- | --- | --- |
| `astro.config.mjs` | Site und Base per Umgebungsvariable; Standard-Base `/kleines-schaeferrad` | Astro allein lässt sich umstellen, aber nicht sämtliche Offline-Pfade |
| `scripts/build-offline.mjs` | Base fest `/kleines-schaeferrad/` | Eine andere Base erfordert zusätzliche Anpassung |
| `public/manifest.webmanifest` | ID, Start, Scope und Icon unter derselben festen Base | Ein reiner Astro-Base-Wechsel genügt nicht |
| `src/field/store.js` | IndexedDB `ks-pre-disassembly`, Version 1 | Gleiche Origin teilt Daten auch bei anderem URL-Pfad |
| `src/workbench/records.js` | IndexedDB `ks-field-workbench`, Version 1 | Zweiter originweiter gemeinsamer Datenspeicher |
| `scripts/build-offline.mjs` | Aktivierung löscht andere Caches mit Präfix `ks-field-` | Preview und Produktion könnten gegenseitig Offline-Caches entfernen |
| `src/field/client.js` | Registrierung von SW und Scope anhand der Base | Pfad-Scope isoliert allein weder IndexedDB noch CacheStorage |

Eine **eigene HTTPS-Origin** ist hier die kleinste robuste Isolation: Sie trennt Service Worker, CacheStorage und IndexedDB durch den Browser, ohne Migration oder Änderungen am Fachmodell.

## Verfügbare Alternative und verbleibender Blocker

Der verfügbare Sites-Host wurde anhand seiner verbindlichen Anleitung geprüft. Er kann eine eigenständige Site veröffentlichen, verlangt jedoch ein zusätzliches verwaltetes Quellrepository mit synchronisiertem Commit. Das würde über die Vorgabe „Arbeite ausschließlich in jdistlr/kleines-schaeferrad“ hinausgehen. Deshalb wurde keine Site und kein zweites Repository angelegt. Die Anforderung einer separaten Hostingumgebung wurde nicht stillschweigend als Aufhebung dieser Repositorygrenze behandelt.

Für einen statischen Direct-Upload-Host, der das vorhandene Build-Artefakt ohne zweites Quellrepository ausliefert, steht in dieser Sitzung kein eingerichtetes Deploymentziel mit passenden Zugangsmöglichkeiten bereit. Es wurden keine Zugangsdaten gesucht oder neue Hostingkonten angelegt.

**Konkreter Fortsetzungsweg innerhalb der Repositorygrenze:** ein separates statisches Direct-Upload-Projekt, beispielsweise Cloudflare Pages, mit eigener Provider-Origin bereitstellen und den Deploymentzugang verbinden. Danach das vorhandene geprüfte Artefakt deployen, nicht die Anwendung neu entwickeln.

**Alternative mit kleiner Umfangserweiterung:** die obligatorische Sites-Quellkopie ausdrücklich zulassen; jdistlr/kleines-schaeferrad bleibt dabei kanonische Quelle. Dies ist eine Scope-Entscheidung, keine fehlende allgemeine Veröffentlichungserlaubnis: Die öffentliche Preview selbst ist bereits autorisiert.

## Vorhandenes geprüfte Build-Artefakt

Der [erfolgreiche Acceptance-Lauf 38035076111](https://github.com/jdistlr/kleines-schaeferrad/actions/runs/38035076111) stellt ein verwendbares statisches Build bereit:

- Name: `control-plane-review-site`
- Artifact-ID: `11663835871`
- ZIP-Größe laut GitHub: `103257354` Bytes
- ZIP-Digest laut GitHub: `sha256:7e8388f94678294df591157504303101a6f2f5480772811a231a9df6ebf007d6`
- Herkunft: Anwendungscode `51221b9d0e6ad8aed1fb714f7888f1a38bf0e3c5`
- Beim Abruf nicht abgelaufen; Ablauf laut GitHub: `2027-01-08T07:37:44Z`

Diese Sitzung hat das Artefakt weder heruntergeladen noch seinen Digest unabhängig neu berechnet. GitHub-Actions-Artefaktlinks sind keine öffentlich nutzbaren Review-Websites.

Der kleinste Veröffentlichungsweg ist, die entpackten Dateien auf einer eigenen Origin unter `/kleines-schaeferrad/` zu hosten. Dadurch bleiben die vorhandenen Base-, Manifest- und Offline-Pfade erhalten. Der Review-Einstieg wäre dort `/kleines-schaeferrad/control/`. Das ist ein geplanter Pfad, keine bereits existierende URL.

## Abnahme nach Bereitstellung des isolierten Hosts

1. ZIP-Digest prüfen; Deployment-ID, tatsächliche Origin und zugehörigen Commit dokumentieren.
2. Direkte Aufrufe und Reloads von `control/`, `control/water/`, `control/evidence/`, `werkstatt/` und `feld/` unter der bestehenden Base prüfen.
3. Browser-Netzwerkfehler, Asset-/Font-MIME-Typen, GLB-Ladevorgänge, Navigation und Query-Deep-Links prüfen; insbesondere Wasser → 3D → Feldaufnahme.
4. SW-Scope und Cache-URLs gegen die Preview-Origin prüfen; Offline-Installation und Reload verifizieren.
5. Synthetische Testaufnahme, Export/Import und Wiederladen auf der Preview prüfen. Keine produktiven Nutzerdaten verwenden.
6. Mobile Viewports und Browserprüfungen gegen die tatsächlich veröffentlichte URL ausführen; physisches iPhone/Safari separat ausweisen, falls nicht getestet.
7. Dauerhafte GitHub-Evidenz mit URL, Deploymentlauf, Commit, Screenshots, Ergebnissen und Grenzen ergänzen.

In dieser Sitzung fanden **keine Live-Preview-Browserprüfungen** statt, da keine Preview veröffentlicht wurde. Vorherige PR-Browsertests ersetzen diese Prüfung nicht.

## Abschluss

Kein Merge, kein produktives Deployment, kein neues Hostingprojekt, keine Rekonstruktions- oder UX-Änderung. Der Auftrag stoppt am ausdrücklich vorgesehenen dokumentierten Blocker; die READY-Marke wird nicht verwendet.
