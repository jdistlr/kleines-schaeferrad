# Evidence Ontology Delta

**CONDITIONAL GO für einen additiven Konsistenzplan. Keine Schema-Migration in diesem PR.** Alle 39 Aussagen und Werte erhalten; kein `as_built_eligible` gesetzt. Jede Quellenklasse bleibt sichtbar, Thorstens Auskunft hat Vorrang vor ungestützter Rekonstruktion, ersetzt aber keine unabhängig dokumentierte Ist-Messung.

## Unabhängiger Trace

[CLAIMS-39-TRACE.md](CLAIMS-39-TRACE.md) führt alle 39 Aussagen einzeln durch Originalpfade/Hashes, Kanon, Quellenanalysen, Komponenten, Graph, markierte Meshes und Ansichtszuordnung. [claims-39-trace.json](evidence/claims-39-trace.json) enthält die vollständigen Werte und IDs. UI-Pfad: `src/workbench/data.js` → Komponenten-/Claim-Kontext → `client.js` Inspektor; `assets.mjs` normalisiert Quellen, `build-workbench.mjs` erzeugt Zeichnungen mit ITER-003-Provenienz. Aktuelles ausgeliefertes JS/CSS und KS-50 stimmen mit lokalem Build überein. Kumpf wird als Live-Journey geprüft; kein pauschaler 39-facher Interaktionsnachweis behauptet.

65/65 Thorsten-Dateihashes passen, 63 verschiedene Payloads. Doppelte Bytes mit verschiedenen Originalnamen sind im Manifest erlaubt, keine unabhängigen Bestätigungen. Der bestehende Python-Verifier meldet 43 historische und 4 zusätzliche Originale; die **65 Thorsten-Fotos werden ergänzend** durch den Integrationstest und diesen Hashaudit geprüft. „Alle Quellen verifiziert“ darf diese getrennten Abdeckungen nicht verschweigen. 408 Claims / 117 Quellenanalysen sind vorhandener Umfang, keine Anzahl unabhängiger Beobachtungen.

## Exakte Befunde

| ID | Befund / Fundstelle | Folge und minimaler Änderungsauftrag |
|---|---|---|
| EO-01 | `data/source-analyses.json`, `NARRATIVE-TH-CONSTRUCTION-20261009.claim_ids` enthält nur TH-25..29. Alle 39 Claims nennen diese Quelle; TH-01..24 und TH-30..39 haben dort keinen Rückverweis | Der aktuelle Test verlangt nur irgendeinen Quellenrückverweis. 34 Aussagen bleiben über Fotoanalysen auffindbar, sind nicht verloren. Künftig vollständige narrative Rückverweise herstellen und den Vertrag auf tatsächliche Provenienzkanten beziehen |
| EO-02 | Intake `model_changed:false`, `canonical_data_updated:false`, Status `expert-intake-pending-property-review`; aktuelle Claims tragen weiterhin `intake_status`, daneben ITER-002-Review | Originalbeitrag unverändert lassen. Einen aktuellen Review-/Supersession-Zeiger daneben führen; historische Intakefelder nicht als aktuellen Fortschritt verwenden |
| EO-03 | `COMP-RADSTATT` kanonisch; `COMP-RADSTADT` ist als `terminology-alias` plus erläuternder Notiz vorhanden | Menschlich bereits klargestellt, maschinenlesbare Zielkante fehlt. Additiver Resolver auf bestehende Identität; kein zweites Tragwerk und keine Migration realer IDs |
| EO-04 | `COMP-SCHETTERNBRETTER` ≠ `COMP-PADDLES`; 48 Schetternnägel ≠ 48 Kumpfnägel | 24 Stoßbretter/48 Nägel und 96 Band-Schenkelpfade haben eigene Modellprüfungen. Schettern nie mit Flügelbrettern oder deren U-Bändern verschmelzen |
| EO-05 | TH-20, TH-37, TH-39 ohne explizites Brute-Mesh-Quelltag | TH-20 ist undefinierte 65-cm-Endpunktdistanz, TH-39 Scanverfügbarkeit: keine erzwungene Geometrie. TH-37 wird als lokales 0,8-m-Datum berechnet, aber fehlt als direktes Mesh-Tag: Ableitungsbezug ergänzen, nicht Geometrie verändern |
| EO-06 | 13 Aussagen ohne Graphrelationsreferenz: TH-07/08/10/11/13/20/25/26/27/28/29/38/39 | Kein pauschaler Defekt. Material-/Maß-/Prozess-/Scanattribute sind nicht alle Verbindungen. Pro Aussage „Attribut“, „Ableitung“, „Relation“ oder „offen“ explizit abdecken; keine Scheinrelationen zur Quotenerfüllung |
| EO-07 | 48/48 Kumpfnagelmittellinien schneiden Kranzmaterial; F02. F03 bleibt synthetisch/unregistriert | Modellprobe reproduziert F02; Boden, Keile, Passungen und Lastpfad nicht freigegeben. Nicht durch erfundene Bohrungen, neue Maße oder abgeschwächte Prüfungen schließen |
| EO-08 | PR #12 enthält nur Auftrag; sieben MOV fehlen im geprüften Git-Bestand | Status `SOURCE_TRANSFER_PENDING`, nicht „ausgewertet“. Historische Videos von späteren Demontageaufnahmen trennen; vor jedem Schluss Originalbytes und Metadaten sichern |

TH-25..29 sind im Kanon und in den Komponenten inzwischen rückverknüpft: dieser Teil von F04 ist behoben. EO-01 präzisiert eine verbleibende **andere** Vollständigkeitsgrenze. Keine erneute pauschale Behauptung „F04 unrepariert“.

## Vier Aussagearten und Ableitung

| Art | Beispiel | Zulässige Aussage |
|---|---|---|
| Fachauskunft | TH-26: 14 cm axial; TH-08: etwa 35 cm | Expertenmaß mit Genauigkeits-/Geltungsgrenze, keine eigene Feldmessung |
| Beobachteter Einbauzustand | sichtbare Verbindung auf Originalfoto | Sichtbares Detail zu Zeitpunkt/Objekt; verdeckte Innenform bleibt offen |
| Unabhängige Messung | künftig Endpunkte, Einheit, Werkzeug, Unsicherheit, Zeitpunkt, Instanz, Foto | Nur nach Review als verifiziert für genau diese Eigenschaft/Instanz verwenden |
| Synthetischer Modellwert | A-Bockbein 1,50 m / 12°, Sitzverstärkung 45 mm | Anzeigeannahme, keine Messkarte mit vorausgefülltem Ist-Wert |
| Berechnung | TH-28: 1,80 + (0,14 + 0,14)/2 = 1,94 m; TH-29: 2,08 m | Von Expertenwerten abgeleitet, erbt deren Unsicherheit, keine dritte unabhängige Evidenz |

„Truth“ hat 296 Meshes, enthält Fach-Topologie, lässt stationären Standort und genaue Nagelpfade aus. „Brute“ hat 945 Meshes und zeigt Kandidaten. Beide sind `not as-built`. Die Begriffe dürfen als technische Modi weiterbestehen; die Oberfläche muss ihren Belegumfang verständlich nennen.

## Unveränderlichkeit und minimaler Vertrag

Originalbytes nach SHA-256 adressieren; Dateinamen und Aliasvorkommen erhalten. Korrekturen erzeugen eine neue Analyse-/Claimrevision mit `supersedes`, Autor, Grund, Zeit und betroffenen Eigenschaften. Originalzitat, Interpretation und Entscheidung separat speichern. Ein archiviertes Modell bekommt Eingaberevision, Generatorversion und Hash; sein Review behält den damaligen Stand. Neue Tests schreiben unter neuem Auditpfad, niemals über ITER-001-Nachweise. Hashbezug beweist Unverändertheit, nicht fachliche Richtigkeit.

Keine Promotion durch grünen Test, schöne Darstellung, gehashte Datei, Mehrheitszählung ähnlicher Bilder oder gemessene Pixel in unregistrierten Fotos. Scan-Achsnormalisierung ist keine metrische Registrierung. Quellen- und Komponentenfamilie ist keine reale Teileinstanz. Vor Freigabe von Fachzeichnungen/BOM/Passungen sind Maßregistrierung, Materialzustand, Toleranz, Partner und Expertenentscheid erforderlich.
