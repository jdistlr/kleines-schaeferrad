# Stabilization Roadmap

**Ziel: weniger gleichzeitige Veränderung, präzisere Freigaben.** Kein neues Modell, Framework, Dashboard-Produkt oder Orchestrierungssystem als Voraussetzung. Aufwand S/M/L bedeutet begrenzte Text-/Mappingarbeit, mehrere gekoppelte Verträge oder mess-/fachabhängige Arbeit; keine Terminzusage. Maximal ein Produktänderungspaket gleichzeitig, daneben Quellenaufnahme. Hannes entscheidet Reihenfolge und Release, Thorsten fachliche Auslegung; technische Ausführung und unabhängige Gegenprüfung werden pro Paket benannt.

## P0 — Aufnahmefenster und eindeutiger Arbeitsstand

| Paket | Ergebnis / Abnahme | Abhängigkeit | Aufwand | Grenze / Rückweg / Stop |
|---|---|---|---|---|
| P0-A Zustandszeiger | Ein aktueller Einstieg verlinkt main, die drei offenen Reviewlinien, F02/F03 und den nächsten Auftrag. PR #14 als historisch, #11/#12 als unerledigt kennzeichnen | Review dieses Plans | S | Nur additive Dokumentation; kein Branch löschen/mergen. `STATE RECONCILIATION REVIEW READY` |
| P0-B Originale sichern | Für sieben Archivvideos Originalbytes, Hash, Metadaten, Archivort und fehlende Quellen einzeln nachweisen. Aktuelle Demontageaufnahmen separat führen | Tatsächlicher Medienzugang; PR #12 | M, transferabhängig | Quelle fehlt → SOURCE TRANSFER BLOCKED. Keine Timecodes erfinden. Kopieren/verifizieren vor Löschen; `ARCHIVE SOURCE INTEGRITY REVIEW READY`, anschließend erst vollständiger #12-Auswertungsauftrag |
| P0-C Praktischer Rückweg | Originalkamera + vorhandener Papierplan; vor Verlust des Einbauzustands Teil/Partner/Endpunkte/Ereignis sichern. Zwei unabhängige Kopien prüfen, nicht nur „gespeichert“ anzeigen | Fachteam und Gerätezugang | M, vor Ort | Keine aus diesem Audit abgeleitete Demontageanweisung. Lokale Erhebung bleibt unreviewed. `FIELD EVIDENCE BACKUP VERIFIED` erst mit Nachweisen |

P0 bezeichnet hier Dringlichkeit der Evidenzsicherung, keinen behaupteten neuen P0-Softwaredefekt. Das reale Aufnahmefenster am 10. Oktober darf nicht von einem UI-Umbau abhängen. Eine Kalendervorgabe beweist nicht, dass Aufnahmen bereits stattgefunden haben.

## P1 — kleinste technische Stabilisierung

| Paket | Ergebnis / Abnahme | Abhängigkeit | Aufwand | Reversible Grenze / Stop |
|---|---|---|---|---|
| P1-A Quellen-/Statusvertrag | EO-01 narrative Rückverweise vollständig; Aliasauflösung Radstadt→Radstatt; Intake-/Reviewstatus getrennt; TH-37 Ableitungsbezug | P0-A, Fachprüfung der Zuordnung | S–M | Keine Änderung der 39 Werte/Originalbytes, keine Ist-Promotion; additive Adapter. `CANONICAL TRACE REVIEW READY` |
| P1-B CI-Verträge | V2-Sampling an V2 binden; aktuellen Modellprüfumfang explizit machen; sechs Gateklassen mit SHA/Status/Scope; Build einmal, Browser gegen dasselbe Artefakt | P0-A; genaue Legacy-Diagnose dieses Audits | M | Bestehende Checks bis freigegebener Ersatz behalten, echte Negativkontrollen, keine Geometrieanpassung für Tests. `CI CONTRACT REVIEW READY` |
| P1-C R1/R4 | Wasser sichtbar, Messblatt-/Originalvideohinweise zugänglich, Deep-Link/Rückkehr, 200%-Text ohne Kollision | #11 neu auf aktuellem main; gesicherter Feldstand vor Veröffentlichung | M | Kein v2-Datenschema, keine Task-Umsortierung. Revert des isolierten UI-Commits möglich; `UX R1+R4 REVIEW READY` |
| P1-D Lesende Control Plane | Revision, Eigenschaftsstatus, offene Maße und Evidenz im bestehenden Inspektor; Kandidatenregler progressiv | P1-A; P1-C zunächst abgeschlossen/reviewt | M | Keine neue persistente Datenbank, keine Statistik ohne Nenner, kein Viewer-Neubau; `CONTROL PLANE READ-ONLY REVIEW READY` |

**Nächster technischer Meilenstein:** P0-A + P1-A als kleiner Quellen-/Zustands-PR. Parallel dürfen Originale aufgenommen werden. P1-C ist als separate begrenzte UX-Arbeit vorbereitet, nicht in denselben Änderungs-PR ziehen. P1-B ist ebenfalls separat zu reviewen: Build-Deduplizierung und korrekter Testvertrag sind zwei nachvollziehbare Änderungen, keine pauschale CI-Bereinigung.

## P2 — nach Stabilisierung und metrischer Grundlage

| Paket | Voraussetzung und Abnahme | Aufwand / Stop |
|---|---|---|
| Mehrfachmessungen / Partnerereignisse | Neuer additiver Messrecord mit stabiler ID, Endpunkten, Einheit, Foto/Instanz; v1 weiterhin lesbar; keine Überschreibung bei Same-ID-Konflikt, Sicherung vor Migration | M; `MEASUREMENT CONTRACT REVIEW READY` |
| F02/F03 gezielt fachlich schließen | Registrierte Endpunkte und Verbindungen, Kumpfnagelweg, stationäre Auflager/Keile/Boden, Materialzustand; begründete Fachentscheidung vor Modellrevision | L, aufnahmeabhängig; eigener neuer Auftrag. **Dieser Plan autorisiert keine Geometrieiteration** |
| Technische Zeichnungen / BOM | Reale Teileidentitäten, freigegebene Eigenschaftsrevision, Toleranzen/Material und Stückzahlstatus | L; `ENGINEERING OUTPUT REVIEW READY` ohne Fertigungsfreigabe bis Unterschrift |
| Montage-/Demontageanimation | Geprüfte Verbindungsabhängigkeiten, reale Freiräume, temporäre Abstützung und sichere Reihenfolge fachlich bestätigt | L; Kinematik bleibt Entwurf, physische Freigabe separat |
| Hydraulik / museale Darstellung | Hydraulik benötigt reale Wasserstände/Bewegung/Mengen und validierten Modellumfang. Museumrealismus bekommt Herkunfts-/Revisionslabel | L; kein Fotorealismus als Beleg. Zurückstellen bis obige Gates geklärt |

## Minimaler Architekturvertrag

Vier Verantwortungsbereiche im vorhandenen Repository, keine vier neuen Dienste:

| Bereich | Liefert | Empfängt / Eigentümerschaft |
|---|---|---|
| Evidence Registry | `source_id`, Originalhash, Originalname/Aliase, Datum/Autor, Ort, Klasse, `review_state`, Revision | Originale und Aufnahmen. Verantwortlich: Intakebearbeitung; menschliche Quellenprüfung |
| Canonical Engineering Knowledge | Familien-/Instanz-ID, eigenschaftsbezogener Claim, Wert/Einheit/Unsicherheit, Endpunkte, Quellenrevision, Aliasziel, Entscheidung / `supersedes` | Nur geprüfte Interpretation mit explizitem Scope. Fachentscheidung Thorsten/benannter Reviewer; kein automatischer Mehrheitsbeschluss |
| Model / Derivation | Eingabe-SHAs, Generatorrevision, Modellhash, Property-/Mesh-Mapping, Annahmen, Prüfdomäne und Grenzen | Kanonrevision plus explizite synthetische Parameter. Technischer Maintainer; abgeleitete Artefakte dürfen Kanon nicht rückwärts ändern |
| Experience / Control Plane | Lesbare Status-/Quellenansicht, Zeichnung/Viewer mit Revision, lokaler Rohbefund mit Export | Ableitung und Kanon als lesende Sichten; Feldbefund kommt zunächst als unreviewed in Evidence zurück |

Zulässiger Übergang: `CAPTURED_UNREVIEWED → REVIEWED → ACCEPTED / DISPUTED / UNKNOWN`, pro Eigenschaft. Fach-Topologie `EXPERT_REVIEWED` ist nicht automatisch `METRIC_VERIFIED`; `RELEASED` verlangt explizite zweckbezogene technische Freigabe. Experience bleibt `SYNTHETIC`, `SOURCE_DERIVED` oder `ENGINEERING_DERIVED` mit Herkunft, auch wenn das Rendering sehr realistisch ist.

Zur Umsetzung reichen zuerst ein Revisionsindex und Adapter über vorhandene JSON-Dateien. Felder werden nur hinzugefügt, wenn sie einen konkreten Befund lösen. Kein pauschales Neuschreiben aller Ontologien. Alte IDs bleiben gültig; neue Revisionen ersetzen niemals Originalbytes oder historische Auditresultate. Auch ein späteres PDF benennt `input_revision`, `generator_revision`, Hash, Prüfumfang und Releasezweck.

## Stop-Regeln

Ein Paket stoppt bei seinem Review-Gate, ungelöster Herkunft, Werteabweichung, unvereinbarer Altimport-Semantik oder geforderter nicht autorisierter Geometrieänderung. Keine Kette „grün → Merge → Deployment → nächste Rekonstruktion“. Neue Fehler werden nach Ursache (Quelle, Vertrag, Anwendung, Engineering, Umgebung) eingeordnet, nicht durch zusätzliche globale Prüfungen überdeckt.
