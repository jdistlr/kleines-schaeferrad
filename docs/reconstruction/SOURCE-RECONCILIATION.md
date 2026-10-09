> **Zusätzliche Fachquelle 09.10.2026:** [Konstruktionsbeitrag](../FACHBEITRAG-KONSTRUKTION-20261009.md), [strukturierte Claims](../../evidence/contributions/thorsten-20261009.json) und [Fotomanifest](../../evidence/contributions/thorsten-20261009-photos.json). Die neueren Korrekturen zu Kranzinnenabstand, Armquerschnitt, Schetternbrettern, U-Bändern, Welle/Lager und A-Bock müssen im nächsten [Astra-Abgleich](../../state/ASTRA-ABGLEICH-20261009.md) property-genau integriert werden. Diese Notiz allein aktualisiert weder Evidenzgraph noch Modell.

# Quellenabgleich vor der Rekonstruktion V2

Ausgangspunkt `45cb32a9c781b506bab1d4ff987e2810da34f378`. Die bisherige primitive Präsentationsgeometrie ist keine Evidenz und wird nicht zur Formbestimmung benutzt.

20 neue Uploads wurden als Originalbytes wiederhergestellt; 19 verschiedene Hashes. Die beiden IMG_6803-Uploads sind bitgleich. `evidence/additions-v2.json` hält Namen, Archivpfade, Hashes und Status getrennt von der unveränderten bisherigen Baseline. EXIF-Rotation ist für die Anzeige zu beachten; Originalbytes werden nicht gedreht oder retuschiert.

## Direkte visuelle Prüfung

- IMG_6798/6799: Historische Armzeichnung mit flachem symmetrischem Knick und mittlerer gerader Zone. Beide Enden liegen auf derselben Seite des Mittelstücks; die alte gegensinnige Kröpfung ist dadurch widerlegt als Wiedergabe dieser Zeichnung. Notationen455 Gesamt,395 innen,50 Mitte,30 Endzone und14 Höhe sind lesbar; Einheiten und heutige Maßgeltung bleiben offen. Eine metrische Kandidatenkonvention muss ausdrücklich gekennzeichnet werden.
- IMG_6792/6793/6794 und6795/6797: Historische Radstattpläne mit Land-/Wasserseite, zwei Rahmenlinien, Lager-/Pfostenabständen und asymmetrischen Maßketten. Perspektive und Faltung begrenzen Ablesegenauigkeit. Historische Seitenbezeichnungen bestimmen nicht automatisch eine aktuelle Fotoorientierung.
- IMG_6800/6801: Welle, axiale Armstaffelung und stationäre Quer-/Diagonalhölzer gemeinsam sichtbar; verdeckte Innenpaarung weiterhin nicht sichtbar.
- IMG_6803/6804/6808: Axiale/halbaxiale Sicht mit Wellenende, Armöffnungen, Keil-/Füllstücken sowie Rahmen und Lagerregion. Keine sichere vollständige Lagerkontaktfläche.
- IMG_6809/6810/6811: Daubenkörper, Metallreifen, überstehende Holzköpfe und Schaufeln; gekoppelter Umfangsaufbau mit Neigung. Keine isoliert eindeutige Erklärung aller Stiftsitze.
- IMG_6812: Gesamtanlage mit Wasser und stationärem Tragwerk als räumliche Systemreferenz.
- IMG_6822: zwei unterschiedlich lange, gekrümmte Holzstifte nebeneinander. IMG_6832: langer Stift mit Kopf in der Hand. Formbeobachtung ist direkt; Funktion als neigungsbestimmendes Paar bleibt Erzählung/Kandidat.

## Externe Konstruktion: Transferregeln

Siehe `data/external-construction-research-v2.json` für einzeln attribuierte Quellen, Bauprinzip, Übertragbarkeit und Vertrauen. Primär genutzt werden Betreiberbeschreibung, historische bebilderte Montagebeschreibung, kommunaler Kontext und museales Objektwissen. Wikipedia war nur Suchweg und ist nicht die technische Belegbasis.

Die Betreiberquelle des Kleinen Schäferrads beschreibt24 Kümpfe; die ältere regionale Montagebeschreibung nennt26. Das ist ausdrücklich ein externer Zählkonflikt, keine Erlaubnis die lokale Baseline zu überschreiben. Gleichfalls belegen Wehrnadeln keine Kumpfnagelfunktion. Gekrümmte Eichenstifte und gekochte Holzbänder eröffnen plausible Material-/Herstellkandidaten; ihre aktuelle Sitzgeometrie braucht lokale Bilder.

Der historische Montagebericht enthält Betriebsbeschreibungen und alte Arbeitspraktiken. Daraus werden Funktionszusammenhänge, keine heutigen Demontageanweisungen übernommen. Reale Reihenfolge und Sicherung verantworten die erfahrenen Personen vor Ort.

## Stylekit

Die reale Referenzseite und ihr ausgeliefertes CSS wurden erneut geladen und inspiziert. Hash/Tokenauszug unter `state/reconstruction/stylekit-inspection.json`. Beibehalten werden Manrope, helle Papier-/Weißhierarchie, feine Linien, ruhige Radien und kurze Bild-/Textkomposition. Die aktuelle Vorgabe hebt die frühere grüne Dominanz auf. Materialfarben gehören in den Modellraum; sie bestimmen nicht die gesamte Oberfläche.


## Baseline-Refresh 2026-10-08 — ThorstenHalsch

Nach der Rekonstruktion V2 wurde PR #5 von `ThorstenHalsch` integriert. Thorsten ist als Wasserrad-Mitinitiator / lokaler Fachkenner einzuordnen. Seine expliziten Korrekturen besitzen für Funktion, Terminologie und lokale Konstruktionslogik höhere Autorität als externe Analogien und unbelegte Modellannahmen. Sie ersetzen jedoch keine direkte metrische Vor-Ort-Messung.

Verbindliche Quellenhierarchie: `data/evidence-authority.json`.

### In die Baseline promoviert

Für den fotografierten Referenz-Kumpf:
- 12 Dauben,
- 1 Kumpfboden,
- Bodenaufnahme in einer Einfräsung/Nut der Dauben,
- 3 Metallbänder,
- 2 speziell gelochte Dauben,
- je 2 Löcher,
- 2 Kumpfnägel: ein langer und ein kurzer,
- Kumpfnägel befestigen den Kumpf durch die gelochten Dauben am Krümmling,
- benachbarte Kümpfe überlappen,
- die Überlappung ist laut Fachauskunft der Grund für die unterschiedlichen Nagellängen.

Diese Aussagen sind als `expert-narrative` in `data/geometry.claims.json` aufgenommen. Exakte Maße, Nagelwege, Loch-Nagel-Zuordnung und Überlappungsmaß bleiben offen.

### Frühere Hypothese herabgestuft

Die frühere Arbeitshypothese, die Lang-/Kurz-Differenz der Kumpfnägel bestimme primär Neigung oder Verdrehung des Kumpfs, ist nicht mehr führend. Die lokale Fachauskunft nennt stattdessen die Überlappung benachbarter Kümpfe als konstruktiven Grund. `data/kumpf-fastener-hypotheses.json` wurde entsprechend neu gerankt.

### Bandvarianten neu interpretiert

Die konkurrierenden historischen Ring-/Bandlängen werden nicht mehr als einfacher Zeichnungswiderspruch behandelt. Die Fachauskunft bestätigt, dass unterschiedliche Derivate mit unterschiedlichen Maßen gefertigt wurden. Offen bleibt die numerische Zuordnung der vorhandenen Längenreihen zum fotografierten Referenz-Kumpf. `CONFLICT-02` ist daher nun `variant-family-confirmed-numeric-mapping-unresolved`.

### Schaufelstellung als Prioritätskorrektur

Thorsten korrigiert die Schaufelstellung auf **90° zum Rad**. Diese Aussage erhält hohe lokale Expertenpriorität. Sie wird noch nicht durch eine blinde 90°-Transformation in Modellgeometrie umgesetzt, weil der genaue geometrische Bezug von „zum Rad“ (Radebene vs lokale radial/tangentiale Orientierung) zunächst explizit definiert werden muss. Dafür existiert `CONFLICT-13` und `GAP-09`; der dedizierte Schaufelscan ist noch zu identifizieren bzw. der vorhandene Radscan gezielt auszuwerten.

### Neue Baseline-Folge

Das Truth Model darf ab jetzt die oben genannten nicht-metrischen Konstruktionsaussagen als lokale Expertenbaseline verwenden. Das Brute-Force-Modell muss seine Kumpf-, Kumpfnagel- und Schaufelkandidaten dagegen neu kalibrieren. Externe Recherche darf diese lokalen Aussagen nicht überstimmen.
