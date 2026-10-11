# Projektvorgaben für Coding-Agenten

## Keine GitHub Actions

Explizite Nutzervorgabe vom 11.10.2026: Für dieses Projekt sind keine GitHub Actions gewünscht. Der Nutzer hat Actions in GitHub gesperrt.

- Keine GitHub-Actions-Workflows anlegen, aktivieren, starten oder erneut ausführen.
- Beim Zusammenführen von Branches keine Workflow-Dateien nach `.github/workflows/` zurückbringen. Historische Definitionen liegen ausschließlich unter `docs/archive/github-actions/`.
- Fehlende, gesperrte oder ausstehende Actions-Läufe sind kein Grund, auf GitHub Actions zu warten oder deren Freischaltung zu verlangen.
- Erforderliche Prüfungen in der verfügbaren Arbeitsumgebung ausführen und deren Ergebnis berichten. Nicht verfügbare Prüfungen als ungeprüft kennzeichnen.
- Builds und Veröffentlichungen bei Bedarf außerhalb von GitHub Actions durchführen; keine automatische Veröffentlichung einrichten.
- Diese Vorgabe nur nach einer ausdrücklichen Änderung durch den Nutzer ändern.

## Ordnungsphase: Faktenbasis zuerst

Gilt ab 11.10.2026 bis zum Abschluss von Phase 2 des [Ordnungsplans](docs/ordnung/PLAN.md). Aufhebung nur durch den Nutzer.

- **Ein Register:** Fakten stehen ausschließlich in `data/geometry.claims.json`. Befunde, Pläne und Code verweisen mit Claim-ID darauf. Fachangaben nicht nur in Markdown oder Beitragsdateien ablegen.
- **Menschen entscheiden:** Thorsten entscheidet über fachliche Gültigkeit, der Nutzer über Struktur. Agenten schlagen Einträge vor, setzen aber keine Gültigkeit („heute gültig“, `as_built_eligible`, Quellenautorität) eigenständig.
- **Keine neuen Wahrheitsschichten:** keine neuen Schemas, Steuerungs- oder Referenzebenen, Iterationsordner oder parallelen Faktenablagen anlegen.
- **Kein Modellumbau:** Geometrie, Kalibrierung und Modellparameter bleiben eingefroren, bis Phase 2 abgeschlossen ist.
- **Nichts still löschen:** Überholte Angaben bleiben mit Verweis auf den Nachfolger erhalten.
- **Herkunft benennen:** Statt „Nutzer“ die Person angeben, die eine Angabe gemacht hat.
- **Arbeit nur über Branches und PRs.** Jeder PR nennt die berührten Claim-IDs.
- **Keine Veröffentlichung auf GitHub Pages** ohne ausdrückliche Freigabe des Nutzers.
