# Wissenskern Kleines Schäferrad

Hier steht, was über das Kleine Schäferrad bekannt ist – und nur hier. Cockpit, 3D-Modell, Homepage und Ausstellung lesen aus diesem Kern. Sie sind nie selbst Quelle.

Das Rad ist eine Überlieferung des Vereins: Skizzen, mündliches Wissen und jährlicher Abbau im Herbst und Aufbau im Frühjahr. Der Kern hält dieses Wissen so fest, dass Menschen und KI-Modelle es gleich verstehen.

## Acht Begriffe

| Begriff | Datei | Was es ist | Beispiel |
|---|---|---|---|
| **Bauteil** | `bauteile.json` | Ein Ding im Inventar, im Baum `teil_von` | `COMP-KRUEMMLINGE` Krümmlinge, Teil von `COMP-RIMS` |
| **Beziehung** | `beziehungen.json` | Wie zwei Bauteile zusammengehören | `COMP-TROUGH` *liegt auf* `COMP-RINNE` |
| **Angabe** | `angaben.json` | Ein Wert zu Bauteil, Beziehung oder Quelle | Arme 14 × 6,5 cm, mündlich, Thorsten |
| **Quelle** | `quellen.json` | Foto, Skizze, Scan, Video, Aussage, Kontext | `PHOTO-6816` Wellenskizze |
| **Offene Frage** | `fragen.json` | Was zu entscheiden oder zu messen ist; mit Abhängigkeiten, `kurztitel` (höchstens 40 Zeichen, für Listen und Überschriften) und `klaerung` (wo es sich klären lässt: `wissen`, `radstadt`, `foto`, `rechnen`, `aufbau` – Letzteres ruht bis zum Frühjahr) | `F-001` lichte Weite der Radstadt |
| **Arbeitsschritt** | `arbeitsschritte.json` | Ein Schritt beim Aufbau oder Abbau | `AS-AUF-02` Arme mit Wellenkeil sichern |
| **Wissensträger** | `personen.json` | Wer Wissen beiträgt und bestätigt | `P-THORSTEN` |
| **Begründung** | `begruendungen.json` | Warum es so gebaut wird | `G-001` ungleich lange Kumpfnägel |

Dazu das **Glossar** `begriffe.json`: ein Begriff, eine ID, alle Schreibweisen als Aliase (Radstadt = Radstatt, Schetter = Schetternbrett) und Verwechslungsgefahren (Schetternbrett ≠ Flügelbrett). Begriff nachschlagen:

```
python scripts/kern/pruefe_kern.py --begriff Schetter
```

## Jede Angabe beantwortet drei Fragen

**Woher?** – `grundlage`

| Wert | Bedeutung |
|---|---|
| `messung` | Am Bauteil gemessen (Zollstock, Maßband) |
| `muendlich` | Mündlich überliefert oder von einem Wissensträger gesagt |
| `skizze` | Aus einer Vereinsskizze abgelesen |
| `foto` | Auf einem Foto abgelesen oder beobachtet |
| `scan` | Aus einem 3D-Scan oder dessen Dateieigenschaften |
| `holzliste` | Aus der allgemeinen Holz-/Materialempfehlung, nicht speziell dieses Rad |
| `fremdvorlage` | Aus einer fremden (industriellen) Vorlage |
| `kontext` | Aus Veröffentlichungen oder Projektkontext |
| `ableitung` | Aus anderen Angaben berechnet |
| `annahme` | Bewusst gewählt, z. B. für eine plausible Darstellung |

**Gilt das heute?** – `gueltigkeit`

| Wert | Bedeutung | Wer setzt es |
|---|---|---|
| `offen` | Noch nicht entschieden | Jeder, auch Agenten |
| `bestaetigt` | Gilt für das heutige Rad; braucht `bestaetigt: {von, am}` | **Nur Menschen** aus `personen.json` |
| `historisch` | Dokumentiert eine Unterlage, sagt nichts über das heutige Rad | Jeder |
| `ueberholt` | Durch eine andere Angabe ersetzt; braucht `ersetzt_durch` | Mensch oder bei ausdrücklicher Korrektur |
| `verworfen` | Falsch, bleibt zur Nachvollziehbarkeit erhalten | Mensch |

**Wie genau?** – `toleranz`: `bereich` (von/bis), `plusminus`, `ungefaehr` oder `vereinfachung`. Bei Naturholz ist Toleranz der Normalfall, kein Mangel. Eine bewusste Vereinsvereinfachung wie „obere Balken 40 × 20 cm“ ist eine gültige Angabe mit Toleranz `vereinfachung`.

## Regeln

1. **Fakten nur hier.** Befunde, Pläne und Code verweisen mit IDs auf den Kern.
2. **Nichts löschen.** Falsches wird `verworfen`, Altes `ueberholt` – mit Nachfolger.
3. **Mündliche Angaben brauchen eine Person** (`aussage_von`), bevor sie bestätigt werden können.
4. **Keine neuen Dateien oder Felder** ohne Freigabe von Johannes. Neue Begriffe ins Glossar.
5. **Alles auf Deutsch.** Jede Eigenschaft einer Angabe steht mit deutschem Namen im Glossar (Kategorie `eigenschaft`, Schlüssel in Kleinbuchstaben ohne Umlaute, z. B. `lichte_weite_land_wasser` → „Lichte Weite Land–Wasser“). Die Prüfung lehnt Eigenschaften ohne Glossareintrag ab. Englische Originalwerte aus den Altdaten stehen unter `herkunft`.
6. **Agenten schlagen vor** (per Pull Request, Gültigkeit `offen`). Menschen bestätigen.
7. **Vor jedem Commit prüfen:** `python scripts/kern/pruefe_kern.py` und `python -m unittest tests/test_kern.py`.

## Fotos

Jede Datei steht genau einmal im Kern. Identische Dateien unter anderem Namen sind in der Hauptquelle unter `kopien` zusammengeführt (`python scripts/kern/werkzeuge/kopien_zusammenfuehren.py`); die Prüfung lehnt neue Doppelungen ab. Jedes Foto hat eine `bildart`:

| Bildart | Woran man es erkennt | Wozu es dient |
|---|---|---|
| `messfoto` | Zollstock oder Maßband im Bild | Maße ablesen und als Angabe mit Grundlage `foto` und Toleranz eintragen |
| `konstruktionsfoto` | Nahaufnahme einer Verbindung oder eines Mechanismus | Beziehungen, Arbeitsschritte und offene Fragen belegen |
| `uebersicht` | Gesamtansicht, Umgebung, Kontext | Beleg und Orientierung; muss nichts weiter bewirken |

Ausgewertet werden Fotos von den offenen Fragen her: Welche Messfotos können eine Frage beantworten?

## Neues Wissen eintragen

1. Quelle in `quellen.json` anlegen (Foto, Aussage mit Protokoll-Pfad, …).
2. Angabe in `angaben.json` mit `grundlage`, `quellen`, `aussage_von` und `gueltigkeit: "offen"`.
3. Falls es eine offene Frage beantwortet: Frage auf `beantwortet` setzen und die Angabe unter `antwort` eintragen.
4. Prüfung laufen lassen, Pull Request öffnen. Thorsten bestätigt fachlich.

## Cockpit

`npm run cockpit` (oder `python scripts/kern/baue_cockpit.py`) erzeugt aus dem Kern eine Übersichtsseite unter `cockpit/index.html`: das Rad als anwählbarer Aufriss mit der Akte jedes Bauteils, die offenen Fragen nach dem, was ihre Antwort freischaltet, und die Herkunft des Wissens. Die Seite ist nur eine Ansicht und wird nie von Hand bearbeitet.

**Veröffentlichen** (von Hand, ohne GitHub Actions): `npm run cockpit:pages` baut Forschungsseite und Cockpit und legt beide auf den Branch `gh-pages`. Adressen: https://jdistlr.github.io/kleines-schaeferrad/ (Forschungsseite) und …/cockpit/ (Cockpit). Nach jeder bestätigten Änderung am Kern erneut ausführen; die Seite nennt den Commit, aus dem sie erzeugt wurde.

## Herkunft und Altdaten

Der Kern wurde am 11.10.2026 aus den bisherigen Daten erzeugt (`scripts/kern/migriere_v1.py`). Die Altdateien unter `data/` und `evidence/` bleiben **unverändert und eingefroren**, bis das Modell auf den Kern umgestellt ist (Phase 3 im [Ordnungsplan](../docs/ordnung/PLAN.md)). `migration/v1-zuordnung.json` führt jede Alt-ID auf ihre Kern-ID; die Prüfung stellt sicher, dass keine Alt-Angabe verloren geht. Alte Claim-IDs (`CLAIM-…`, `TH-…`) wurden beibehalten.

Was die Migration geändert hat:
- 20 „conflicting“/„unknown“-Claims, 13 Konflikte und 9 Aufnahmelücken sind jetzt **offene Fragen** statt Pseudo-Fakten.
- 5 zusammengesetzte Subjekte (`COMP-ARMS/COMP-RADSTATT` …) sind jetzt **Beziehungen**.
- Holzlisten-Posten hängen am passenden Bauteil oder sind eigene Listenposten mit offener Zuordnung.
- `COMP-RADSTADT` ist nur noch Schreibvariante von `COMP-RADSTATT`.
- 14 Angaben vom 11.10.2026 aus den Befunden (`AN-20261011-*`) sind nachgetragen, alle `offen`.
- Alle Dateien unter `evidence/raw/` sind als Quellen inventarisiert, inklusive identischer Kopien.
- **Keine Angabe wurde als bestätigt übernommen.** Das ist Aufgabe des Durchgangs mit Thorsten.
