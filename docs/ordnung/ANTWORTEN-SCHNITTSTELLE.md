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

## Entscheidungen vom 12.10.2026 (Johannes): Webspace statt Datenbank

- **Ort:** eigene Subdomain bei UD Media; Cockpit und PHP-Schnittstelle unter derselben Adresse. GitHub Pages bleibt bis zum Umzug als Spiegel.
- **Speicher:** keine Datenbank. Eine JSON-Datei je Antwort, nur anhängen, nie überschreiben (Korrektur = neue Antwort mit Verweis). Schreiben über Zwischendatei und Umbenennen. Fotos und Sprachnachrichten in eigenem Ordner, Fotos beim Hochladen verkleinert. Alles liegt im Webordner der Subdomain (Hobbyprojekt, Entscheidung Johannes); der Datenordner bekommt nur eine einzeilige `.htaccess`, die das direkte Aufrufen der Rohdateien verhindert.
- **Transport:** Hinweg per SFTP nach jedem Merge in `main`; Rückweg: geschützter Export-Endpunkt, regelmäßig abgeholt, landet als Pull Request unter `evidence/antworten/`. Zugangsdaten nur in den GitHub-Secrets. Voraussetzung: Johannes lockert die Actions-Regel in `AGENTS.md` auf genau diese zwei Workflows (noch offen).
- **Wer antwortet:** keine Konten, keine persönlichen Links. Name als **Freitext**, leer lassen erlaubt.
  - Das Gerät merkt sich den zuletzt eingegebenen Namen und füllt ihn vor.
  - Beim Tippen werden bereits verwendete Namen vorgeschlagen, öffentlich nur als **Vorname**. Gibt es denselben Vornamen mehrfach, wird ergänzt: erst Anfangsbuchstabe des Nachnamens („Thorsten H.“), reicht das nicht, weitere Buchstaben oder ein Kürzel.
  - Unordnung ist in Kauf genommen: Beim Einsammeln ordnet Claude Schreibvarianten derselben Person zu (Namensliste neben den Antworten, nicht im Kern); unklare Fälle entscheidet Johannes. Erst danach wird eine Antwort zur Aussage mit Person im Kern.
- **Spamschutz ohne Hürde:** unsichtbares Fangfeld und Begrenzung pro Minute; kein Vereinscode, keine Rätselfrage.
- **Recht:** Impressum und Datenschutzhinweis auf der Subdomain; Hinweis beim ersten Antworten, dass Name und Antwort gespeichert und für die Bestandsaufnahme verwendet werden.
