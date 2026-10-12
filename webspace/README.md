# Webspace schaeferrad.jdistlr.de

Cockpit plus Antworten-Schnittstelle in PHP, ohne Datenbank. Entscheidungen und Anforderungen: [`docs/ordnung/ANTWORTEN-SCHNITTSTELLE.md`](../docs/ordnung/ANTWORTEN-SCHNITTSTELLE.md).

| Datei | Zweck |
|---|---|
| `api.php` | Antworten speichern (Text, Wert, Name, Fotos, Sprachnachrichten, Antwort auf Antwort), Liste, Namensvorschläge, Dateien, geschützter Export |
| `daten/.htaccess` | verhindert direktes Aufrufen der Rohdateien; Antworten liegen auf dem Server unter `daten/antworten/JJJJ/MM/` |
| `.htaccess` | https erzwingen, kein Verzeichnislisting, `konfig.php` gesperrt |
| `datenschutz.html`, `impressum.vorlage.html` | Rechtliches; das Impressum kommt aus dem Secret `KS_IMPRESSUM`, nie ins Repository |
| `konfig.beispiel.php` | Vorlage; die echte `konfig.php` schreibt die Veröffentlichung aus `KS_EXPORT_SCHLUESSEL` |
| `workflows-entwurf/` | die zwei Workflows, **noch nicht aktiv** |

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
| `KS_IMPRESSUM` | Impressum als HTML, z. B. `<p>Name<br>Anschrift<br>E-Mail</p>` |
