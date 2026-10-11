# Projektvorgaben für alle Agenten

Gilt für jedes KI-Modell und jedes Werkzeug, das in diesem Repository arbeitet: Claude, Astra, Codex, Copilot, Gemini, Cursor und alle anderen. **Diese Datei hat Vorrang** vor allen Übergaben, Arbeitsaufträgen und Statusdateien unter `state/` und `docs/`. Widerspricht eine ältere Übergabe dieser Datei, gilt diese Datei.

Änderungen an diesen Vorgaben nur auf ausdrückliche Anweisung von Johannes (jdistlr).

## Zuerst lesen

1. Diese Datei.
2. [`kern/README.md`](kern/README.md) – wie Wissen abgelegt wird.
3. [`docs/ordnung/PLAN.md`](docs/ordnung/PLAN.md) – in welcher Phase das Projekt steht.

Ältere Übergaben (`state/NEXT-*.md`, `state/CURRENT-STATE.md`, `state/reconstruction-loop/`, `docs/workbench/`) sind Geschichte, keine Arbeitsaufträge.

## Worum es geht

Das Kleine Schäferrad ist ein hölzernes Wasserschöpfrad an der Regnitz. Der Verein baut es jeden Herbst ab und jedes Frühjahr wieder auf. Das Wissen darüber ist überliefert: Skizzen, mündliche Erklärungen, alte Werkzeuge. Am 10.10.2026 wurde das Rad abgebaut; bis zum Frühjahr liegen die Teile einzeln im Lager. Ziel ist eine erste vollständige, überprüfbare Bestandsaufnahme – und daraus später Cockpit, 3D-Modell und Ausstellung.

## Grundregeln

- **Ein Kern.** Fakten stehen ausschließlich im Wissenskern unter [`kern/`](kern/README.md). Befunde, Pläne und Code verweisen mit IDs darauf. Keine Fachangabe nur in Markdown, in Beitragsdateien oder im Code ablegen.
- **Menschen entscheiden.** Thorsten Halsch (`P-THORSTEN`) entscheidet über fachliche Gültigkeit, Johannes Distler (`P-JOHANNES`) über Struktur, Ontologie und Veröffentlichung. Agenten tragen neue Angaben nur mit Gültigkeit `offen` ein und setzen nie `bestaetigt`, `verworfen` oder Quellenautorität.
- **Herkunft benennen.** Jede Angabe nennt ihre Quelle und, wenn mündlich, die Person. Nicht „Nutzer“ schreiben, sondern den Namen.
- **Alles auf Deutsch.** Namen, Eigenschaften, Werte, Hinweise, Commit-Nachrichten und PR-Texte auf Deutsch. Jede Eigenschaft braucht einen deutschen Glossareintrag (`kern/begriffe.json`, Kategorie `eigenschaft`). Fachwörter des Vereins (Krümmling, Schetternbrett, Kumpf, Radstadt) nicht übersetzen oder umbenennen; unklare Wörter mit `python scripts/kern/pruefe_kern.py --begriff <Wort>` nachschlagen.
- **Keine neuen Wahrheitsschichten.** Keine neuen Schemas, Steuerungs- oder Referenzebenen, Iterationsordner, „Truth Models“ oder parallelen Faktenablagen. Neue Dateien im Kern nur mit Freigabe von Johannes.
- **Nichts still löschen.** Überholtes bleibt mit Verweis auf den Nachfolger erhalten.
- **Altdaten eingefroren.** `data/geometry.claims.json`, `data/components.json`, `data/conflicts.json`, `data/knowledge-gaps.json` und `evidence/contributions/` nicht mehr ändern. Sie bleiben nur bis zur Umstellung des Modells für den bestehenden Code.
- **Kein Modellumbau** (Geometrie, Kalibrierung, Modellparameter), bis Phase 2 des Ordnungsplans abgeschlossen ist.

## Neues Fachwissen eintragen

Wenn Thorsten oder jemand aus dem Verein etwas erklärt:

1. Gespräch als Protokoll unter `evidence/raw/<Bauteilordner>/BEFUND.md` festhalten (wörtlich, mit Datum und Person).
2. Das Protokoll als Quelle der Art `aussage` in `kern/quellen.json` eintragen.
3. Jede einzelne Angabe in `kern/angaben.json` mit `aussage_von`, `grundlage: "muendlich"`, `gueltigkeit: "offen"`.
4. Was offen bleibt, als Frage in `kern/fragen.json`.
5. Prüfen, Pull Request öffnen. Thorsten bestätigt.

Nicht mehr: Nachträge an `state/NEXT-ASTRA-WORK-SESSION.md` oder andere Übergabedateien anhängen.

## Branches und Pull Requests

- `main` ist der einzige dauerhafte Arbeitsbranch. **Nie direkt auf `main` committen oder pushen.**
- Arbeit in kurzlebigen Branches mit Präfix nach Zweck: `kern/`, `befund/`, `cockpit/`, `modell/`, `ordnung/`, Datum am Ende (z. B. `befund/radstadt-hoehen-20261012`). Höchstens ein offener Branch pro Thema.
- Jeder Branch endet in einem Pull Request. Der PR nennt die berührten Kern-IDs und was geprüft wurde. Nach dem Merge löscht GitHub den Branch automatisch.

## Veröffentlichung (GitHub Pages)

- Unter https://jdistlr.github.io/kleines-schaeferrad/ liegen zwei Dinge: die **Forschungsseite mit der 3D-Werkstatt** (Astro-Build: `/`, `/feld/`, `/werkstatt/` …) und das **Cockpit** unter `/cockpit/`. Beide kommen ausschließlich vom Branch `gh-pages`.
- `gh-pages` wird **nur** mit `npm run cockpit:pages` geschrieben, und nur aus einem sauberen Stand von `main` nach einem Merge. Das Skript veröffentlicht immer beide Teile zusammen und bricht ab, wenn die Forschungsseite fehlt. Nie von Hand bearbeiten, nie mergen, nie aus einem Arbeitsbranch veröffentlichen.
- Veröffentlichen nur, wenn Johannes es im jeweiligen Auftrag ausdrücklich verlangt.
- Keine weiteren Seiten oder Vorschauen auf Pages legen.
- Das Repository ist öffentlich: keine privaten Daten, Adressen oder Telefonnummern in Kern, Befunde oder Cockpit.

## Keine GitHub Actions

Ausdrückliche Vorgabe vom 11.10.2026: Für dieses Projekt sind keine GitHub Actions gewünscht; Actions sind gesperrt.

- Keine Workflows anlegen, aktivieren, starten oder erneut ausführen. Keine Dateien nach `.github/workflows/`. Historische Definitionen liegen nur unter `docs/archive/github-actions/`.
- Fehlende Actions-Läufe sind kein Grund zu warten. Prüfungen selbst ausführen und das Ergebnis berichten; nicht ausführbare Prüfungen als ungeprüft kennzeichnen.
- Keine automatische Veröffentlichung einrichten.

## Prüfungen vor jedem Commit

```
npm run test:kern            # Kern widerspruchsfrei + Tests
python scripts/verify_evidence.py
```

Die Git-Hooks unter `.githooks/` erzwingen das lokal; `npm install` aktiviert sie. Hooks nie mit `--no-verify` umgehen. Testläufe, die Dateien unter `state/` oder `output/` überschreiben, danach mit `git checkout -- state output` zurücksetzen.
