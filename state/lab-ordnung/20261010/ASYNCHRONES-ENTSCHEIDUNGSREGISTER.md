# Asynchrones Entscheidungs- und Untersuchungsregister – Entwurf

Stand 2026-10-10. **Nur Dokumentation; keine Fachentscheidung, kein neues kanonisches Datenmodell.**

## Zweck
Thorsten erhält gebündelte, entscheidungsreife Dossiers; er muss nicht synchron an der Laborentwicklung teilnehmen. Johannes entscheidet über System/UX, nicht über Konstruktion. Assistenz kann Unterlagen, Nachweislücken und Alternativen vorbereiten, nicht freigeben.

## Drei Registeransichten über bestehende IDs
1. **Fachentscheidungen für Thorsten:** eine Frage je Eintrag, referenzierte Claims, Quellen, bereits dokumentierte Aussagen, Widersprüche, Modellbezug, Entscheidungsoptionen und konkrete Folgen.
2. **Aufnahmen/Messungen:** vorhandene `TASK-*`/`GAP-*`, Zeitpunkt, Endpunkte, Einheit, Werkzeug, Fotoanforderung, Verlustfenster, ausführende Person noch offen.
3. **System-/Modellnachweise:** Referenzauflösung, Quellzugänglichkeit, Parametermapping, Vergleichs- und Visualisierungsaufgaben, ohne fachliche Freigabe.

Keine neue Parallelontologie: Die Register sind vorläufige **Sichten und Arbeitslisten** auf vorhandene `data/`-Verträge; etwaige neue Identifikatoren sind Dokument-IDs, keine kanonischen Claim-IDs.

## Reifegrad einer Entscheidungsfrage (keine Wahrheitsskala)
- **Vorbereitung:** Quellen sammeln/Originale prüfen, keine Entscheidung verlangen.
- **Klärung erforderlich:** zusätzliche Messung/Beobachtung oder Kontext fehlt.
- **Vorlage bereit:** erreichbare Quellen, abweichende Aussagen, Annahmen und Geltungsgrenzen transparent; Thorsten kann entscheiden oder ausdrücklich zurückstellen.
- **Von Thorsten beantwortet:** Originalantwort, Zeitpunkt, konkrete Geltungsgrenze und Nachweise dokumentiert; nicht automatisch in kanonische Daten übertragen.
- **Umsetzung gesondert beauftragt:** erst nach geprüftem Änderungsantrag und Freigabe der Systemarbeit.

## Startbestand – noch keine versandfertigen Entscheidungen

| Arbeits-ID | Frage/Auftrag | Bestehende Anker | Nächste Vorbereitung |
|---|---|---|---|
| ENT-WELLE-01 | Geltungsbereich und Einheiten der historischen Wellenmaße 370/37 | `COMP-SHAFT`, `CLAIM-0001`, `CLAIM-0002`, `PHOTO-6816`, `PHOTO-6817` | Originale neu prüfen; Endpunkte dokumentieren |
| ENT-WELLE-02 | Handelt es sich bei abweichenden Wellenangaben um echten Widerspruch oder verschiedene Gegenstände? | `CLAIM-0346`, `PHOTO-6816`, `PHOTO-6827` | Originalvergleich und Quelle der allgemeinen Empfehlung prüfen |
| ENT-WELLE-03 | Welche Teile der Wellen-/Armverbindung sind aus bisherigen Fachauskünften tatsächlich geklärt? | `TH-20261009-13`, `TH-20261009-14`, `CLAIM-0336` | Originalauskunft, Bilder, Aussagegrenzen und Varianten bündeln |
| MESS-WELLE-01 | Mortisen/Keile und Partnerbezüge beim Lösen dokumentieren | `GAP-02`, `TASK-ARM-BEFORE` | Aus bestehendem Feldauftrag vollständige Checkliste und Verlustfenster ableiten |
| MESS-WELLE-02 | Lager-/Zapfenbezüge vor Wellenanhebung sichern | `GAP-06` | passende bestehende Feldaufgaben und Aufnahmevorgaben zuordnen |
| SYS-WELLE-01 | Claim-zu-Modellparameter-Nachweis prüfen | `src/control/property-readiness.mjs`, `data/reconstruction-constraints.json:shaft` | explizit vorhandene und fehlende Zuordnungen kennzeichnen |

Diese Liste ist **kein vollständiger Projektbestand**. Die Erweiterung erfolgt erst nach systematischer read-only Zuordnung aller vorhandenen 21 Feldaufgaben, neun Lücken, Konflikte und fachlichen Aussagen; keine erfundenen Entscheidungsstände.

## Priorisierung
Zuerst drohender irreversibler Informationsverlust, dann konstruktive Abhängigkeiten, dann Entscheidungsvoraussetzungen und Aufwand. Bereits dokumentierte P0-/Timing-Felder aus `data/field-tasks.json` übernehmen, nicht durch neue Fantasiescores ersetzen. Eine Entscheidung kann auf eine Messung warten, während andere Dossiers vorbereitet werden.

## Übergabe an Thorsten
Ein gebündeltes, später exportierbares Paket je Gegenstand: knappe Frage, Originalbelege und genaue Bildregionen, Vorentscheidungen im Originalwortlaut, widersprechende/abhängige Aussagen, Modellannahmen, fehlende Nachweise, klare Antwortoptionen inklusive »nicht entscheidbar«, und Platz für seine Begründung. Antworten dürfen nicht automatisch zu Freigaben oder Datenmigration führen.

## Grenzen
Keine Anfrage an Thorsten gesendet, keine fachliche Antwort erfunden, kein Merge/Deployment, keine Veränderung von PR #18, main, Preview, F02/F03, 39 Fachkorrekturen, Geometrie, kanonischen Daten oder lokalen Aufnahmen.
