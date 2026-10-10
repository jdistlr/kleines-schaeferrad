# CI Contract Matrix

**Anwendung integriert; technische Freigabe weiterhin NO-GO.** Der Audit ändert keinen Workflow und deaktiviert keinen Test. Status gilt immer für SHA, Daten-/Modellrevision, Testvertrag und Laufumgebung. Rohdaten: [Runs](evidence/github-runs-initial.json), [Jobs](evidence/github-jobs.json), [37 Einzeltests](evidence/test-inventory.json).

## Tatsächliche Workflow-Landschaft

| YAML | Tatsächlicher Trigger | Geprüfter Vertrag | Aktueller Stellenwert |
|---|---|---|---|
| `pages.yml` | main-Push, alle PRs, manuell | Node 24 / Python 3.12, `npm install`, check, vollständiger Build; Deploy nur Nicht-PR auf main | Aktiv. PR-Build ist kein Deploy. Erfolgreicher main-Lauf 37994601533 mit Build **und** Deploy bereits vor diesem Audit |
| `field-workbench.yml` | alle PRs; Push nur alter Field-Branch; manuell | Vier Matrixjobs field / field-kit / reconstruction / integration; jeder installiert, führt 37 Node-Tests, Python-Verifier, check/build und Browser aus | Aktiv. Hohe Wiederholung derselben Vorarbeit; neue Dokumentations-PRs lösen vollen Lauf aus |
| `pre-disassembly-field-kit.yml` | zwei historische Branches, manuell | Build/check, Workbench/Field-Unit-Tests, Quellen, Field-Kit-Browser | Branchgebundener älterer Vertrag; kein automatischer main-/PR-Gate |
| `reconstruction-v2.yml` | V2-Branch, manuell | Zusätzlich `test:reconstruction` einschließlich altem Kandidatenaudit und `prepare:model` | V2-Vertrag nicht als aktuelles ITER-003-Signal übernehmen; kann historische Berichte/Exporte schreiben |
| `ux-recovery-audit.yml` | alter UX-Auditbranch + Pfadfilter, manuell | Playwright 1.56.1, Live-Folgebeobachtung, kein Build/Deploy | Beobachtungssammlung. Erfolgreiche Ausführung bedeutet nicht fehlerfreie UX |

Die Matrix trennt YAML-Trigger von erforderlichen Merge-Checks; kein Gate wurde umbenannt.

## Tests, Modellrevision und Befund

| Prüfung | Bindung / Abdeckung | Resultat dieses Audits | Was sie nicht belegt |
|---|---|---|---|
| `verify_evidence.py` | aktuelle Manifest-/Claim-/Graphreferenzen; Klassen inkl. `derived`, Confidence inkl. `qualified` | PASS; 43 historische, 4 Zusatzoriginale, 10 Derivate, 408 Claims, 117 Analysen | Keine visuelle Wahrheit aller Fotos; separater Thorsten-Hashcheck nötig |
| `integration-recovery.test.mjs` | 65 normalisierte Thorsten-Fotos, Narrative, 39 Claims mit mindestens einem Rückverweis | PASS | Vollständige Reziprozität **aller** Provenienzkanten nicht geprüft: EO-01 |
| `expert-corrections.test.mjs` | ITER-003 Maße als Expertenbedingungen, Armsitze, Schettern, U-Bänder, Welle, Kanal/Truth-Grenze | PASS | Schaftendpunkt am Kranz ist keine kollisionsfreie Nagelverbindung; F02 bleibt |
| `workbench.test.mjs` | Modellfamilien, Varianten, Beobachtungsverträge und Import | PASS | Keine reale Teilevollständigkeit, kein Hardware-Speicherdruck |
| `field-kit.test.mjs` | 21 Aufgaben, Identitäten, Scan-Achsnormalisierung, Aufnahmevalidierung, PDF-Manifest | PASS | Kein realer Scanmaßstab, keine physische Papier-/Handschuhabnahme |
| `calibration.test.mjs` | aktuelle Runtime + synthetische Referenzkumpf-/Zyklusfixtures | PASS | Keine Hydraulik-/Festigkeitsfreigabe |
| `mechanics.test.mjs` | analytische Wasser-/Registrierungsfixtures | PASS | Registrierungscode funktioniert an Fixtures; reale Transformation weiterhin null |
| `reconstruction-geometry.test.mjs` | Ontologiefamilien, Quellen, 66 historische/erwartete Slots | PASS | Erwartete Slots sind keine bestätigten eingebauten Instanzen |
| `npm run check`, `npm run build` | main-Anwendung einschließlich SVG/PDF/Offline-Artefakte | PASS; 0 Fehler, 0 Warnungen, vier Hinweise; 193 Offline-URLs, 130.999.689 lokale Bytes | Keine UX-Vollabnahme oder Fertigungsfreigabe |
| PR #15 Browsermatrix | `6a19868`, Playwright 1.62.1, CI Chromium 151 | PASS verifiziert, Lauf 37993441445 | Diese Evidenz nicht als lokal erneut getesteten Chromium 151 ausgeben |
| initialer PR #16 Browsermatrix | `7bff823`, unverändertes Produkt | PASS, Lauf 37995923429 | Dokumentation kann grün sein, während mechanische/UX-Befunde offen sind |
| unabhängige Modellprobe | aktuelle Runtime gegen eingefrorene ITER-003 GLBs/Ansichten | PASS Exportfidelität, 39 Hashes; **FAIL** Nagelpfade 48/48 | 96 freie Bandmittellinien und 12 freie Armstiftlinien belegen keine volle Volumenfreiheit/Pressung |
| `npm run test:reconstruction` | Node-Tests plus V2-`audit-candidates.mjs` gegen heutige Runtime | **FAIL exit 1**, reproduziert | Kein Beweis einer neu entstandenen Geometriekollision; siehe Diagnose |
| physischer Field-/Engineering-Gate | reales Rad, iPhone/Safari, zweites Gerät, Papier, Fachteam | **NOT RUN / OPEN** | Nicht „N/A“, wenn tatsächliche Freigabe beabsichtigt ist |

## Legacy-Diagnose und echter Fehlerverlauf

[audit-candidates.mjs](../../../scripts/audit-candidates.mjs) selektiert korrekt drei LAND-Arme je Kandidat. Es sampelt jedoch fest `x ∈ [-0,65; -0,05] m`, `y,z ∈ [-0,22; 0,22] m`. Beim Crossing-Modell reicht jeder selektierte Arm in X nur ungefähr von −1,04 bis −0,68 m. Kein Arm berührt den Prüfkasten. Der erwartete positive Crossing-Overlap kann folglich nicht auftreten. Staggered/Independent schneiden den Kasten höchstens mit einem Arm: auch dort ist Null-Overlap keine aussagekräftige Bestätigung. [Bounds und Auswahl](evidence/legacy-domain.json), [vollständiger Lauf/Exit](evidence/legacy-reconstruction-result.json).

Dies korrigiert die unpräzise geerbte Erklärung „LAND-Selector passt nicht“: **Auswahl erfolgreich, räumliche Gültigkeit des Prüfvertrags falsch**. Vorschlag: historischen V2-Vertrag an historische Revision binden; zukünftigen ITER-003-Probenbereich aus dokumentierten Referenzen ableiten und mit Positiv-/Negativkontrolle belegen. Bis Review bleibt der bestehende Befehl rot. Kein grünes Label durch Entfernen der Assertion, Verschieben der Geometrie oder neues Timeout.

Historisch unterschiedliche Fehler nicht als einen „immer komplexeren CI-Fehler“ zusammenzählen:

- Frühe #15-Reparaturen betreffen Manifestvarianten, `qualified` und `derived` (Commits `8455d21`, `f1563da`, `3ff008e`). Semantische Schemaabdeckung, keine neue Ist-Wahrheit.
- Lauf 37987615114: tatsächlicher 60-s-Starttimeout in `browser-field.mjs`, Job 114013410401; Logauszug archiviert.
- `f727b8e`: bedarfsgesteuertes Rendern statt durchgehender GPU-Belegung; Ergebnis in #15 bereits geprüft. Exakter alter CI-Timeout lokal nicht reproduziert, keine nachträgliche Behauptung.
- Lauf 37992980382: Integrationstest `38 !== 36`, falsches Wandzeitkriterium für Ruhe; andere drei Jobs grün. `6a19868` bewertet zwölf abgeschlossene Frames; endgültige Matrix erfolgreich.

## Empfohlene sechs Gates

| Gate | PASS | FAIL | NOT APPLICABLE / Offen |
|---|---|---|---|
| Source integrity | Originalbytes + Quellen-ID/Hash prüfbar | fehlende oder geänderte referenzierte Bytes | unveränderte Dokumentation: referenzierte Baseline nutzen; angekündigte fehlende Videos explizit BLOCKED |
| Canonical consistency | gültige, typisierte, vollständige Kanten; Ableitungen/Status nachvollziehbar | dangling IDs, falsche Klasse, unzulässige Promotion | Eigenschaft ohne Relation: begründetes N/A, nicht Dummy-Kante |
| Model integrity | Exporte/Inputs stimmen; begrenzte Geometrieconstraints erfüllt | beschädigter Export, verletzte explizite Modellbedingung | fachlich nicht modellierbarer offener Wert: OPEN, keine erfundene Geometrie |
| Application | Build, Storage, Import/Export, Offline, Browser-Journeys | technische Regression | keine Produktänderung: Baseline + gezielte Integritätsprüfung erst nach Review einer Pfadregel |
| Engineering | registrierte Maße, Toleranz, Material/Passung, Last-/Montageprüfung und fachliche Freigabe | konkrete Unvereinbarkeit; F02/F03 verhindern Freigabe | für reinen Dokumentations-PR N/A; für Konstruktion BLOCKED, niemals automatisch PASS |
| Physical field acceptance | reales Gerät, Backup/Restore, Unterbrechung, Papier unter Praxisbedingungen | Evidenzverlust oder unbrauchbarer Ablauf | aktuell NOT RUN; bleibt Pflicht vor Field-Freigabe |

Ein Checkrecord braucht nur `scope`, Commit/Inputrevision, Toolversion, Befehl, Exit, Status, Artefaktpfad und Grenze. Keine neue Orchestrierungsplattform. Nach Review einmal zentral Build/Unit/Source prüfen, die vier Browserjobs dasselbe **unveränderliche** Buildartefakt konsumieren lassen; Browser parallel nur mit isolierten Kontexten/Ressourcen. Lockfile-Verwendung vereinheitlichen (`npm ci` auch Pages), Laufzeiten vorher/nachher messen. Required Checks/Branchprotection wurden nicht administrativ ausgelesen: diese YAML-Inventur behauptet keine Kenntnis der Merge-Regeln.
