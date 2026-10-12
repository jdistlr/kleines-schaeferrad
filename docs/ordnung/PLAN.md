# Ordnungsplan Kleines Schäferrad

Stand: 11.10.2026 · Verantwortlich: Johannes (Struktur), Thorsten (fachliche Wahrheit)

## Warum

Das Projekt hat in fünf Tagen viel Wissen gesammelt, aber die Wahrheit liegt verstreut:

- **Fakten an vier Orten:** 408 Claims in `data/`, über 120 Einträge in `evidence/contributions/` (nur 39 davon im Register), Markdown-Befunde (Thorstens Angaben vom 11.10. stehen *nur* dort) und rund 114 fest eingetragene Zahlen in `src/workbench/expert-corrections.mjs`.
- **Kein Claim gilt als heutiger Bestand:** alle 408 stehen auf `as_built_eligible: false`, nur 11 sind echte Messungen. Das Modell beruft sich auf nichts, was als wahr markiert ist.
- **Ausfransende Ontologie:** 34 Komponenten, aber 34 weitere Claim-Subjekte außerhalb dieser Liste (zusammengesetzte Subjekte wie `COMP-ARMS/COMP-RADSTATT`, 25 `REF-*`, `PROJECT`, `SITE`).
- **Konkurrierende Wahrheitsschichten**, nacheinander von Agenten eingeführt: Truth Model, Baseline V3, Semantic Reference v1, Control Plane, Evidenzgraph, Laborordnung/Fallakten, 84 Dateien aus Iterationen. 179 Markdown-Dateien, `state/` allein 188 MB.
- **Keine sichtbare Prüfung:** Befunde unter `evidence/raw/` waren für Git Binärdateien (keine Diffs in PRs). `npm run test:reconstruction` ist seit ITER-003 (09.10.) rot, eingecheckte Audits passen nicht mehr zum Code.

## Grundsätze

1. **Ein Kern.** Fakten stehen nur im Wissenskern [`kern/`](../../kern/README.md). Alles andere – Befunde, Pläne, Code – verweist mit Claim-ID darauf.
2. **Jeder Fakt hat drei klare Angaben:**
   - **Quelle:** Messung · heute bestätigte Zeichnung · historische Zeichnung · Fachaussage · Fotobeobachtung · Ableitung · Annahme
   - **Gültigkeit:** heute gültig · historisch · überholt (mit Verweis auf den Nachfolger)
   - **Bestätigt von / am:** Person und Datum
3. **Menschen entscheiden, Agenten schlagen vor.** Thorsten entscheidet fachlich, Johannes strukturell. Agenten (Astra, Claude) dürfen Einträge vorschlagen, aber keine Gültigkeit setzen und keine neuen Wahrheitsschichten anlegen.
4. **Nichts wird still gelöscht.** Überholte Angaben bleiben mit Status „überholt“ erhalten.
5. **Modell folgt Register.** Zahlen im Code kommen aus Claims oder sind ausdrücklich als Annahme gekennzeichnet.

## Phasen

### Phase 0 – Einfrieren (sofort)
- Keine Modell-, Geometrie- oder Kalibrierungsänderungen bis Phase 2 abgeschlossen ist.
- Keine neuen Wahrheits- oder Steuerungsschichten (neue Schemas, „Control Planes“, Iterationsordner).
- Leitplanken in [`AGENTS.md`](../../AGENTS.md) festgehalten.
- Markdown und JSON unter `evidence/raw/` wieder diffbar (`.gitattributes`).

**Fertig, wenn:** dieser PR gemergt ist.

### Phase 1 – Fachangaben sichern (mit Thorsten, ca. 1 Stunde)
- Gemeinsamer Durchgang durch die [Prüfliste](PRUEFLISTE-FACHANGABEN-20261011.md): 28 Angaben, je ✓ / Korrektur / ✗.
- Kritische Fragen zuerst: **A4** (4,40 m vs. Drehkreis), **A6** (Trogstütze = Lagerbock?), **C6** (Armverschränkung vs. Modell-Audit).
- Klären, wer bei „Nutzer“ jeweils gemeint ist.

**Fertig, wenn:** jede Zeile eine Entscheidung von Thorsten hat.

### Phase 2 – Register bereinigen
> **Stand 11.10.2026:** Kernschema, Glossar, Prüfskript und Migration sind umgesetzt ([`kern/`](../../kern/README.md)). Statt das Altregister zu erweitern, gibt es einen neuen Wissenskern mit acht Begriffen; die Altdaten sind vollständig abgebildet und eingefroren. Offen in dieser Phase: Entscheidungen aus Phase 1 eintragen.

- Register-Schema um **Gültigkeit** und **Bestätigt von/am** ergänzen; `as_built_eligible` daraus ableiten statt pauschal `false`.
- Bestätigte Angaben aus Phase 1 eintragen; ⚠️-Einträge korrigieren (alte Werte als „überholt“).
- Beitragsdateien (`evidence/contributions/`) vollständig ins Register überführen; danach sind sie nur noch Quellenbeleg.
- Ontologie: eine Komponentenliste; Beziehungen (`Lagerbock trägt Rinne`) als eigene Einträge statt Subjekte mit „/“; `REF-*` Komponenten zuordnen; `Radstadt`/`Radstatt` zusammenführen.
- `verify_evidence.py` prüft zusätzlich: jedes Subjekt existiert, jeder überholte Eintrag hat einen Nachfolger, jede „heute gültig“-Angabe hat eine bestätigende Person.

**Fertig, wenn:** Register und Prüfliste übereinstimmen und die Prüfung grün ist.

### Phase 3 – Modell an das Register binden
- Feste Zahlen in `expert-corrections.mjs`, `geometry.mjs`, `calibration-v3.json`, `hypothesis.parameters.json` durch Claim-Verweise ersetzen oder als Annahme markieren.
- Ein Test vergleicht Modellmaße mit dem Register.
- **Roter Test:** `audit-candidates.mjs` erwartet, dass sich kreuzende Arme kollidieren. Thorstens Angabe C6 (Arme über Aussparungen verschränkt) spricht genau für diese Variante. Testannahme nach Phase 1 fachlich neu festlegen, nicht einfach anpassen.
- Kollisionsprüfung (`audit-calibration-stationary.mjs`) muss bei Treffern fehlschlagen.
- Audit-Skripte schreiben nicht mehr in historische Iterationsordner.
- Danach erst: Rinne mit Überlappung, Trog nach Zeichnung, Radstadt-Öffnung.

**Fertig, wenn:** alle Tests grün sind und jede Modellzahl eine Herkunft hat.

### Phase 4 – Repository entrümpeln
- `state/` und Iterationsartefakte in einen Archiv-Branch bzw. ein Release-Archiv; im Hauptzweig bleibt eine Statusseite.
- Doppelte Medien entfernen (Video als Ganzes und in Teilen, identische A3-PDFs).
- Defekte Links reparieren, Ordnernamen vereinheitlichen.
- README auf eine Einstiegsseite reduzieren: Was ist sicher, was offen, wo steht es.

**Fertig, wenn:** ein neuer Mitwirkender in fünf Minuten versteht, was wahr ist und wo es steht.

### Phase 5 – Fester Eingangsweg für neues Wissen
- Neue Fachangabe → kurzer Eintrag mit Quelle und Person → Prüfung durch Thorsten → Register.
- Fotos kommen in den Komponentenordner, mit Verweis auf die Claim-IDs, die sie belegen.
- Agenten arbeiten nur auf Branches; jeder PR nennt, welche Claims er berührt.

## Was ausdrücklich nicht passiert
- Kein Löschen von Originalen oder Befunden.
- Keine GitHub Actions (siehe [`AGENTS.md`](../../AGENTS.md)).
- Keine Veröffentlichung auf GitHub Pages ohne ausdrückliche Freigabe.

## Entscheidungen und Vormerkungen

- **12.10.2026 – Hosting:** Johannes erwägt, Cockpit und Forschungsseite von GitHub Pages auf seinen eigenen Webspace mit PHP und MySQL zu übertragen. Dort sollen Antworten und Mehrfachantworten dauerhaft gespeichert werden. Das Cockpit ist darauf vorbereitet (`--api`), die Schnittstelle steht in [ANTWORTEN-SCHNITTSTELLE.md](ANTWORTEN-SCHNITTSTELLE.md). Bis dahin: Arbeitsfassung als Claude-Artefakt, öffentliche Seite nur zum Lesen.

## 12.10.2026 – Vision für das 3D-Modell

Johannes hat [3D-VISION.md](3D-VISION.md) als verbindliche Zielstufe festgelegt (Maximum, darf übertroffen werden). Phase 3 (Modell aus dem Kern) arbeitet auf Stufe 1 „Wahrheit“ hin; „Leben“ und „Erlebnis“ folgen darauf.
