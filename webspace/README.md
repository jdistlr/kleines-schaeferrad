# Webspace schaeferrad.jdistlr.de

Cockpit plus Antworten-Schnittstelle in PHP, ohne Datenbank. Entscheidungen und Anforderungen: [`docs/ordnung/ANTWORTEN-SCHNITTSTELLE.md`](../docs/ordnung/ANTWORTEN-SCHNITTSTELLE.md).

| Datei | Zweck |
|---|---|
| `api.php` | Antworten speichern (Text, Wert, Name, Fotos, Sprachnachrichten, Antwort auf Antwort), Liste, Namensvorschläge, Dateien, geschützter Export |
| `daten/.htaccess` | verhindert direktes Aufrufen der Rohdateien; Antworten liegen auf dem Server unter `daten/antworten/JJJJ/MM/` |
| `.htaccess` | https erzwingen, kein Verzeichnislisting, `konfig.php` gesperrt |
| `datenschutz.html`, `impressum.vorlage.html` | Datenschutzhinweis; ein Impressum entsteht nur, wenn das Secret `KS_IMPRESSUM` gesetzt ist (vorerst nicht) |
| `konfig.beispiel.php` | Vorlage; die echte `konfig.php` schreibt die Veröffentlichung aus `KS_EXPORT_SCHLUESSEL` |
| `.github/workflows/webspace-veroeffentlichen.yml`, `antworten-zurueckholen.yml` | Hochladen nach jedem Merge, Antworten alle drei Stunden zurückholen (freigegeben am 12.10.2026) |

Paket lokal bauen und testen:

```
python scripts/kern/baue_webspace.py          # → dist-webspace/
cd dist-webspace && php -S 127.0.0.1:8080     # Cockpit unter http://127.0.0.1:8080/
```

## Secrets (GitHub → Settings → Secrets and variables → Actions)

| Name | Inhalt |
|---|---|
| `KS_FTP_HOST` | FTP-Server |
| `KS_FTP_PORT` | 21 (FTPES) |
| `KS_FTP_USER` | FTP-Benutzer |
| `KS_FTP_PASSWORT` | Passwort |
| `KS_FTP_ZIEL` | Zielordner aus Sicht des FTP-Benutzers, meist `/` |
| `KS_EXPORT_SCHLUESSEL` | lange Zufallszeichenfolge für den Export |
| `KS_IMPRESSUM` | optional, vorerst nicht anlegen; später Impressum als HTML |
