# Antworten im Cockpit: Speicher und Schnittstelle

Stand: 12.10.2026

Im Cockpit kann jede offene Frage beantwortet und jedes Bauteil ergänzt werden. Mehrere Antworten zur selben Sache sind ausdrücklich erlaubt; nichts wird überschrieben. Antworten sind **Vorschläge**: Johannes übernimmt sie als Angaben (Gültigkeit `offen`) per Pull Request in den Wissenskern, Thorsten bestätigt sie dort. Übernommene Antworten werden mit `uebernommen: true` markiert.

## Wo Antworten heute gespeichert werden

| Fassung | Speicher | Antworten möglich |
|---|---|---|
| Arbeitsfassung (Claude-Artefakt, geteilt mit Thorsten als „Contributor“) | Datenspeicher des Artefakts, Sammlung `antworten` | ja |
| Öffentliche Seite (GitHub Pages) | keiner | nein, nur lesen |
| Später: eigener Webspace (PHP/MySQL) | Datenbank über die Schnittstelle unten | ja |

Die Seite wählt den Speicher selbst: Ist beim Bauen `--api <URL>` angegeben, spricht sie mit dem Server; sonst nutzt sie den Artefakt-Speicher, wenn vorhanden; sonst ist sie nur zum Lesen.

## Datensatz „Antwort“

| Feld | Typ | Bedeutung |
|---|---|---|
| `id` | Text | vom Speicher vergeben |
| `ziel` | Text | Kern-ID der Frage (`F-…`) oder des Bauteils (`COMP-…`) |
| `typ` | Text | `stimmt`, `stimmt_nicht`, `genauer` (bei Fragen); `ergaenzung`, `korrektur` (bei Bauteilen) |
| `text` | Text | Erklärung in eigenen Worten |
| `wert` | Text | optional, ein Maß wie „4,40 m“ (frei geschrieben, wird bei der Übernahme geprüft) |
| `von` / `name` | Text | Artefakt: Nutzer-ID der Plattform; Server: eingegebener Name oder Login |
| `am` | ISO-Zeit | Zeitpunkt der Antwort |
| `uebernommen` | ja/nein | in den Wissenskern übernommen |

## Schnittstelle für den eigenen Server (PHP/MySQL)

Ein einziger Endpunkt, z. B. `https://<webspace>/schaeferrad/api.php`:

- `GET api.php?aktion=liste` → JSON-Liste aller Antworten (Felder wie oben), sortiert nach `am`.
- `POST api.php?aktion=speichern` mit JSON-Körper `{ziel, typ, text, wert, name, am, uebernommen}` → `201` mit `{id}`.
- Fehler als HTTP-Status mit `{fehler: "…"}`.

Empfehlungen für die spätere Umsetzung:

- Tabelle `antworten` mit den Feldern oben, `id` als Auto-Increment, Index auf `ziel`.
- Schreiben nur für angemeldete Vereinsmitglieder (z. B. HTTP-Basic-Auth oder Sitzung), Lesen für die öffentliche Seite optional.
- Prepared Statements, Längenbegrenzung für `text` (z. B. 4.000 Zeichen), keine Ausführung von Inhalten.
- Gleiche Herkunft wie die Seite, dann ist kein CORS nötig.
- Ein Export `GET api.php?aktion=export` für die Übernahme in den Kern.
