# Fachliche Entscheidungshoheit und Thorsten-Review

Stand: 2026-10-10. Verbindliche Prozessleitplanke für den Entwurf; keine Änderung kanonischer Daten.

## Rollen
- **Thorsten**: alleinige fachliche Beurteilung, Entscheidung und Bestätigung von Bauweisen, Ist-Maßen, Quelleninterpretationen, Widersprüchen, Rekonstruktionsannahmen und technischer Freigabe im Projekt. Falls eine formale Sicherheits-/Fertigungszulassung nötig ist, sind darüber hinaus gesetzlich oder organisatorisch vorgeschriebene befugte Prüfer erforderlich; Thorstens Fachentscheidung ersetzt diese nicht automatisch.
- **Johannes**: Auftraggeber und Entscheider über Zweck, Bedienbarkeit, Priorisierung und Systemgestaltung. Keine fachliche Ersatzfreigabe.
- **Assistenz**: Quellen und bestehende Entscheidungen aufbereiten, Alternativen und Unsicherheit kenntlich machen, Nachweisketten prüfen, Entwurfs- und Korrekturvorschläge erstellen. Keine fachliche Selbstfreigabe.

## Entscheidungspaket je Frage
1. Eindeutiger Gegenstand und **konkrete** Frage, mit bestehenden IDs.
2. Sämtliche zugeordneten erreichbaren Originalskizzen, Fotos, Messprotokolle und Fachauskünfte samt exakter Fundstelle, Zeitpunkt, Herkunft und Integritätsstatus; fehlende Originale explizit kennzeichnen.
3. Bereits getroffene Entscheidungen mit Originalwortlaut, Entscheider, Zeitpunkt und Geltungsgrenze. Fachauskunft nicht automatisch als Freigabe deuten.
4. Stützende, widersprechende und abhängige Aussagen; unterschiedliche Zeitstände, Bezugsflächen, Einheiten und Messunsicherheiten.
5. Aktuelle Modellumsetzung, verwendete Approximationen, Alternativhypothesen und Auswirkungen auf angrenzende Bauteile.
6. Entscheidungsoptionen: bestätigen, begrenzt bestätigen, korrigieren, widersprechen, nicht entscheidbar, neue Untersuchung beauftragen.
7. Benötigte zusätzliche Nachweise und konkrete Aufnahmehandlung, insbesondere bei drohendem Verlust durch Demontage.
8. Entscheidungserfassung: Thorstens dokumentierter Originalentscheid, Datum, Bezug, Geltungsgrenze, Begründung, offene Punkte, betroffene Claim-/Modell-IDs. Kein stillschweigendes Umschreiben bestehender Aussagen.

## Schutz vor Scheinsicherheit
- Quellenvollständigkeit nicht behaupten, solange Register-/Originalprüfung unvollständig ist.
- Zwei Fotos desselben Blattes nicht als unabhängige Bestätigungen zählen.
- Historisches Entwurfsmaß, aktuelle menschliche Messung, Fachauskunft und Modellparameter getrennt ausweisen.
- Fehlender Beleg ist kein Gegenbeweis; Modellübernahme ist keine unabhängige Bestätigung.
- »Nicht entscheidbar« ist ein gültiges fachliches Ergebnis.
- Eine UI-/Systemabnahme durch Johannes ist keine Fachfreigabe.
- Fachliche Korrekturen zunächst als Änderungsvorschläge mit Abhängigkeitsanalyse; Umsetzung erst nach dokumentierter Thorsten-Entscheidung und separatem Implementierungsauftrag.

## Auswirkungen auf die Gates
G1: read-only Daten-/Quellenprüfung; keine fachliche Entscheidung.
G2: echte Fallakte mit ausgewogenen Entscheidungsgrundlagen und Originalzugänglichkeit.
G3: Entwürfe zeigen Thorstens Entscheidungsakte, Quellenvergleich, Modellbezug und Feldauftrag; keine simulierten Freigaben.
G4a: Johannes prüft System/UX und Vollständigkeit der Entscheidungsdarstellung.
G4b: Thorsten prüft fachliche Aussagen und trifft explizite Entscheidungen. G4a ersetzt G4b nicht.

Keine Änderung von PR #18, main, Preview, Geometrie, F02/F03, 39 Fachkorrekturen oder kanonischen Daten.
