# Figuren

Erklärende isometrische Figuren, gebaut mit dem Anatomie-Skill (`.claude/skills/anatomy/`). Regeln stehen in `AGENTS.md`, Abschnitt „Figuren mit dem Anatomie-Skill“.

- Jede Figur liegt in einem eigenen Ordner mit `build.mjs`. Das Skript liest alle Maße aus `kern/` und nennt die Kern-IDs in Anzeige und Bildunterschrift.
- `figuren.json` sagt, bei welchen Fragen und Bauteilen das Cockpit die Figur zeigt.
- Gebaute Seiten (`*.html`) und Prüfbilder (`shots/`) werden nicht versioniert. `python scripts/kern/baue_cockpit.py` baut die Figuren mit und legt sie unter `cockpit/figuren/` ab.

| Figur | Inhalt | Fragen |
|---|---|---|
| `armtypen` | Mittelarm mit Hals und zwei gekröpfte Außenarme, wie beim Abbau am 10.10.2026 vermessen; ein Zollstock zeigt die Maße | F-005, F-034 |
| `wellenlager` | Wellenende mit Dorn im offenen Schlitz des landseitigen Lagerklotzes; Herleitung der Achshöhe | F-003, F-015, F-001 |

Bauen und prüfen:

```
npm run figuren     # alle Figuren: Audit und helles Thema
node .claude/skills/anatomy/scripts/lines.mjs figuren/armtypen/armtypen-hell.html   # jede Linie endet auf etwas
```
