# G1 → G2: Vollständige Zuordnung der bestehenden Feldaufgaben und Wissenslücken

Stand 2026-10-10. Lesende Auswertung von `data/field-tasks.json` und `data/knowledge-gaps.json` am Entwurfsbranch. **Keine neuen kanonischen IDs, keine Fachfreigaben.**

## Alle neun Wissenslücken mit vorhandenen Aufgaben

| Lücke | Vorhandene Priorität | Zugeordnete Feldaufgaben (bestehende IDs) | Konfliktverweise |
|---|---|---|---|
| `GAP-01` | P0-before | `TASK-ORIENT`, `TASK-DATUM`, `TASK-POSE`, `TASK-SCAN` | `CONFLICT-03`, `CONFLICT-08`, `CONFLICT-09`, `CONFLICT-10` |
| `GAP-02` | P0-during-first-release | `TASK-ARM-BEFORE`, `TASK-ARM-RELEASE`, `TASK-MORTISE`, `TASK-ARM-PROFILE`, `TASK-KEI` | `CONFLICT-05`, `CONFLICT-06` |
| `GAP-03` | P0-before-and-during | `TASK-KRU-BEFORE`, `TASK-KRU-OPEN` | `CONFLICT-04` |
| `GAP-04` | P0-before-and-during | `TASK-KUM-BEFORE`, `TASK-KUM-VARIANT`, `TASK-HOOPS` | `CONFLICT-01`, `CONFLICT-02`, `CONFLICT-06` |
| `GAP-05` | P0-before | `TASK-COUNT`, `TASK-PAD` | `CONFLICT-07`, `CONFLICT-08` |
| `GAP-06` | P0-before-shaft-lift | `TASK-BEARING` | – |
| `GAP-07` | P0-before | `TASK-ORIENT`, `TASK-WATER` | `CONFLICT-12` |
| `GAP-08` | P0-throughout | `TASK-ARM-RELEASE`, `TASK-PAD`, `TASK-KEI`, `TASK-CRAFT`, `TASK-REGISTER`, `TASK-FINAL` | – |
| `GAP-09` | P0-before | keine direkte Zuordnung | `CONFLICT-13` |

Alle **21 bestehenden Feldaufgaben** sind mindestens einer GAP-ID direkt zugeordnet: ja. Die Zuordnung ist **mehrfach**, weil eine Aufgabe mehrere Lücken bedienen kann; nicht als neue Aufgaben duplizieren.

## Zeitkritische Aufnahmen – Originalreihenfolge beibehalten

- Rang 1: `TASK-WATER` – VOR STILLSETZEN: Wasserübergabe aufnehmen (BEFORE_RELEASE; P0; COMP-TROUGH)
- Rang 2: `TASK-ORIENT` – Blickseiten gemeinsam benennen (BEFORE_RELEASE; P0; COMP-RADSTATT)
- Rang 3: `TASK-DATUM` – Bleibende Referenzen und Kontrollmaß setzen (BEFORE_RELEASE; P0; COMP-RADSTATT)
- Rang 4: `TASK-POSE` – Einbaumaße vor dem Lösen sichern (BEFORE_RELEASE; P0; COMP-RIMS)
- Rang 5: `TASK-COUNT` – Umfangsfolge vor Ausbau sichern (BEFORE_RELEASE; P0; COMP-PADDLES)
- Rang 6: `TASK-KUM-BEFORE` – STOPP: drei Kümpfe und beide Nagelwege (BEFORE_RELEASE; P0; COMP-KUEMPFE)
- Rang 7: `TASK-PAD` – Schaufel: Radbezug und Pitch trennen (DURING_RELEASE; P0; COMP-PADDLES)
- Rang 8: `TASK-SCAN` – Scan-Datei und reale Referenzen zuordnen (BEFORE_RELEASE; P0; COMP-RADSTATT)
- Rang 9: `TASK-ARM-BEFORE` – STOPP: Armzonen vor dem ersten Keilzug (BEFORE_RELEASE; P0++; COMP-ARMS)
- Rang 10: `TASK-BEARING` – STOPP: vor dem Anheben der Welle (BEFORE_RELEASE; P0; COMP-BEARINGS)
- Rang 11: `TASK-KRU-BEFORE` – STOPP: Kranzstoß vor der Trennung (BEFORE_RELEASE; P0; COMP-KRUEMMLINGE)
- Rang 12: `TASK-ARM-RELEASE` – Jeden Keilzug und jede Freigabe festhalten (DURING_RELEASE; P0++; COMP-FASTENERS)
- Rang 13: `TASK-MORTISE` – Geöffnete Wellenzone ohne Deutung aufnehmen (AFTER_RELEASE; P0++; COMP-SHAFT)
- Rang 14: `TASK-KRU-OPEN` – Beide Stoßflächen zusammen dokumentieren (AFTER_RELEASE; P0; COMP-KRUEMMLINGE)
- Rang 15: `TASK-KEI` – Kleinteile behalten ihren Partner (DURING_RELEASE; P0; COMP-KUMPF-NAILS)
- Rang 16: `TASK-REGISTER` – Reales Teil und Lagerplatz eintragen (AFTER_REMOVAL; P0; COMP-FASTENERS)
- Rang 17: `TASK-FINAL` – P0-Lücken und zweite Sicherung prüfen (AFTER_REMOVAL; P0; COMP-RADSTATT)
- Rang 18: `TASK-CRAFT` – Erfahrung direkt am Teil weitergeben (DURING_RELEASE; P0; COMP-ARMS)
- Rang 19: `TASK-KUM-VARIANT` – Referenz-Kumpf: Enden und Maße aufnehmen (AFTER_RELEASE; P0; COMP-KUMPF-STAVES)
- Rang 20: `TASK-HOOPS` – Spannringe und Überlappung vergleichen (AFTER_REMOVAL; P0; COMP-KUMPF-HOOPS)
- Rang 21: `TASK-ARM-PROFILE` – Ausgebauten Arm vollständig erfassen (AFTER_REMOVAL; P0++; COMP-ARMS)

Diese Reihenfolge ist eine **vorhandene Datenpriorisierung**, keine von der Assistenz neu festgelegte fachliche Entscheidung. Ob Aufnahmefenster bereits verstrichen sind, ist nicht unabhängig geprüft. `status:OPEN` ist der Stand des gespeicherten Feldvertrags, kein Live-Nachweis des Baustellenzustands.

## Entscheidungsvorbereitung vs. Feldarbeit

- Thorsten entscheidet fachlich über Quellenauslegung, Konstruktion, konkurrierende Varianten und zulässige Modellannahmen.
- Feldaufträge können als **vorhandene Anweisungen** vorbereitet und zusammengestellt werden, ohne eine neue Fachentscheidung zu fingieren. Durchführung, Sicherheit, Verfügbarkeit und tatsächlicher Fortschritt müssen vor Ort geklärt werden.
- Systemarbeit kann Referenzen, Quellenverfügbarkeit und Abhängigkeiten prüfen, ohne Claims zu korrigieren.

## Offene Datenprüfungen

- Nicht jede Konflikt-ID ist notwendigerweise eine aktuell unaufgelöste Sachkollision; für jeden Eintrag den ursprünglichen Konfliktvertrag lesen.
- Der Bestand nennt `GAP-09` und `CONFLICT-13`, die in bisherigen Kurzlisten leicht übersehen werden: explizit in den Boardentwurf aufnehmen.
- Aufgabenpriorität nicht als Qualitäts- oder Wahrheitsbewertung verwenden.

**Nächster Schritt:** Für einen realen Fall die verlinkten Originale prüfen, den Entscheidungskontext auf Vollständigkeit testen und daraus Desktop-/Smartphone-Entwürfe ableiten. Keine Änderung der 39 Fachkorrekturen, F02/F03, Geometrie, Preview, main oder PR #18.
