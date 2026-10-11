# Prüfliste Fachangaben – Stand 11.10.2026

Zweck: Jede Fachangabe von Thorsten aus den Gesprächen vom 08. bis 11.10.2026 einmal sichtbar machen – mit Quelle und der Frage, ob sie im Faktenregister [`data/geometry.claims.json`](../../data/geometry.claims.json) steht. Grundlage für Phase 1 des [Ordnungsplans](PLAN.md).

Seit der Migration in den [Wissenskern](../../kern/README.md) stehen die fehlenden Angaben als `AN-20261011-*` (Gültigkeit `offen`) und die kritischen Punkte als offene Fragen `F-001` bis `F-011` in [`kern/fragen.json`](../../kern/fragen.json). Die Claim-IDs in dieser Liste gelten im Kern unverändert.

Diese Liste **ändert keine Fakten und kein Modell**. Sie ist die Vorlage für einen gemeinsamen Durchgang mit Thorsten. Erst nach seiner Bestätigung werden Einträge ins Register übernommen oder dort korrigiert.

**Spalte „Register“:**
- ✅ steht im Register, Wert passt
- ⚠️ steht im Register, ist aber veraltet, falsch zugeordnet oder zu grob
- ❌ fehlt im Register; steht nur in Markdown oder einer Beitragsdatei

**Spalte „Thorsten“** bleibt leer, bis er die Angabe bestätigt (✓), korrigiert (Wert eintragen) oder verworfen hat (✗).

## A. Radstadt und landseitiger Lagerbock

| Nr | Angabe | Quelle | Register | Offene Frage / nächster Schritt | Thorsten |
|---|---|---|---|---|---|
| A1 | „Radstadt“ = gesamte Tragkonstruktion, auf der das Rad aufliegt | [Radstadt/BEFUND](../../evidence/raw/Radstadt/BEFUND.md) | ✅ TH-20261009-19 | Ordnerdoppel `Radstadt/` + `Radstatt/` zusammenführen | |
| A2 | Obere Radstadt-Balken vereinfacht 40 × 20 cm (B × H) | Radstadt/BEFUND | ❌ | Als Vereinfachung (nicht Messung) eintragen | |
| A3 | Lichte Weite Land → Wasser **3,40 m** (2,40 m zurückgenommen) | Radstadt/BEFUND | ❌ | Eintragen; Zeichnung 3,84 m Achsmaß − 2 × 0,20 = 3,44 m passt | |
| A4 | Lichte Weite parallel zum Ufer **4,40 m** – von Thorsten selbst angezweifelt | Radstadt/BEFUND, [MASSABGLEICH](../../evidence/raw/Radstadt/MASSABGLEICH.md) | ❌ | **Kritisch:** Drehkreis 4,66–4,96 m. Welche Innenkanten, auf welcher Höhe? Zeichnung zeigt 2,65 + 2,60 = 5,25 m | |
| A5 | Abstand Arme ↔ Radstadt ca. 65 cm | Fachbeitrag 09.10. | ✅ TH-20261009-20 | Messendpunkte festlegen | |
| A6 | Landseitiger Lagerbock: Balken 14 × 14 cm, oberer Querbalken 1,20 m, achsensymmetrisch | [Lagerbock-README](<../../evidence/raw/Lagerboch Landseite/README.md>) | ⚠️ TH-20261009-21…24 | Im Register unter `COMP-TROUGH-SUPPORT` („Trogstütze“). **Identitätsfrage:** Ist Trogstütze = landseitiger Lagerbock der Radstadt? | |
| A7 | Lastfolge **Lagerbock → Rinne → Schöpftrog** | [Auffangtrog/BEFUND](../../evidence/raw/Auffangtrog/BEFUND.md) | ❌ | Als Beziehung eintragen, nicht als Eigenschaft | |

## B. Rinne, A-Bock, Schöpftrog

| Nr | Angabe | Quelle | Register | Offene Frage / nächster Schritt | Thorsten |
|---|---|---|---|---|---|
| B1 | Rinne besteht aus zwei Teilen | [Rinne/BEFUND](../../evidence/raw/Rinne/BEFUND.md) | ✅ TH-20261009-30 | – | |
| B2 | Die Teile **überlappen** (kein stumpfer Stoß) | Rinne/BEFUND | ⚠️ TH-20261009-31 sagt „Stoßstelle“ | TH-31 durch Überlappung ersetzen (alten Wert als überholt behalten) | |
| B3 | A-Bock steht genau unter der Überlappung, Füße auf Gelände | Rinne/BEFUND, [A-Bock/BEFUND](../../evidence/raw/A-Bock/BEFUND.md) | ⚠️ wie B2 | – | |
| B4 | 80 cm Boden → Unterseite Rinnenboden am A-Bock | A-Bock/BEFUND | ✅ TH-20261009-37 | – | |
| B5 | A-Bock: Beine 14 × 14, Aussparung 5 cm, Riegel 4 × 14 × 90 cm, oben/unten verkeilt | A-Bock/BEFUND | ✅ TH-20261009-32…36 | Beinlänge aus Zollstockfotos (TH-38) offen | |
| B6 | Rinne-1-Zeichnung (IMG_6830) entspricht **exakt** dem heutigen Bauteil | [evidence-authority.json](../../data/evidence-authority.json) | ⚠️ CLAIM-0142…0151 noch `historical-drawing`, `as_built_eligible: false` | Claims auf „heute bestätigte Zeichnung“ umstellen | |
| B7 | Trogzeichnung (IMG_6828/6829) entspricht **exakt** dem heutigen Trog | evidence-authority.json | ⚠️ CLAIM-0130…0141 wie B6 | wie B6; Längen 250/(244)/180 klären* | |
| B8 | Grundrisswinkel der Rinne darf plausibel gewählt werden | Auffangtrog/BEFUND | ❌ | Als ausdrücklich erlaubte Annahme kennzeichnen | |

\* Mögliche Lesart (ungeprüft): 180 cm = innere Bodenlänge; + 2 × 30 cm Anstieg bei 45° + 2 × 3 cm × √2 schräge Brettstärke ≈ 248,5 cm ≈ 250 cm außen oben.

## C. Rad: Krümmlinge, Arme, Welle, Kümpfe, Flügelbretter

| Nr | Angabe | Quelle | Register | Offene Frage / nächster Schritt | Thorsten |
|---|---|---|---|---|---|
| C1 | Krümmlinge axial 14 cm (statt 15) | Fachbeitrag 09.10. | ✅ TH-20261009-26 | – | |
| C2 | Lichter Kranzabstand 1,80 m (Innenflächen) | Fachbeitrag 09.10. | ✅ TH-20261009-25, -28, -29 | – | |
| C3 | Landseitige Krümmlinge: je Kumpf 2 zusätzliche Bohrungen; wasserseitige nur Schetternbrett-Bohrungen | [Kruemmlinge/BEFUND](../../evidence/raw/Kruemmlinge/BEFUND.md) | ❌ | Eintragen | |
| C4 | Stoßspalt zwischen Krümmlingen wird verkeilt, Keil verspannt den Kranz über die Schetternägel | Kruemmlinge/BEFUND | ❌ | Eintragen; Spaltweite offen | |
| C5 | Arme 14 × 6,5 cm | Fachbeitrag 09.10. | ✅ TH-20261009-27 | – | |
| C6 | Drei Armtypen je zweimal; **über Aussparungen miteinander verschränkt** (bilden auch ohne Welle einen Stern) | [Arme/ASTRA-HANDOFF](../../evidence/raw/Arme/ASTRA-HANDOFF.md) | ❌ | **Widerspricht dem Modell-Audit:** `audit-candidates.mjs` verlangt, dass die Variante „crossing“ kollidiert. Siehe Plan, Punkt „roter Test“ | |
| C7 | Wellenzeichnung (IMG_6816/6817) ist maßgeblich für Wellenmaße | [Welle/BEFUND](../../evidence/raw/Welle/BEFUND.md) | ⚠️ CLAIM-0001…0009 noch `historical-drawing` | Wie B6 Autorität setzen | |
| C8 | Welle ist Zwölfeck, 37 cm über **Ecken** | Welle/BEFUND | ⚠️ CLAIM-0002 nur „transverse_width 37“ | Präzisieren | |
| C9 | Je Wellenende 2 Metallschellen, zweiteilig verschraubt | Welle/BEFUND | ✅ TH-20261009-14 (Anzahl) | Maße offen, nur Fotoschätzung | |
| C10 | Arme werden mit Wellenkeil + äußeren Keilen gesichert | [wellenkeil-20261011.json](../../evidence/contributions/wellenkeil-20261011.json) | ❌ | Eintragen; Länge ca. 44 cm nur Fotoschätzung | |
| C11 | Kumpf: 12 Dauben, 1 Boden in Nut, 3 Reifen, 2 gebohrte Dauben à 2 Löcher, 2 Kumpfnägel (lang/kurz wegen Überlappung) | [kumpf-20261008.json](../../evidence/contributions/kumpf-20261008.json) | ✅ CLAIM-0356…0368 | Beitragsdatei führt dieselben Angaben unter eigenen IDs (EXPERT-KUMPF-*) – doppelte Ablage auflösen | |
| C12 | Flügelbretter 90° zum Rad | Fachbeitrag 08./09.10. | ⚠️ doppelt: CLAIM-0369, TH-20261009-06, EXPERT-PADDLE-…-ANGLE | Auf einen Eintrag zusammenführen | |
| C13 | Flügelbretter ca. 35 cm breit, landseitig abgeschrägt | Fachbeitrag 09.10. | ✅ TH-20261009-07, -08 | Radialer Überstand über Kranz offen (bestimmt Drehkreis, siehe A4) | |

## D. Frage zur Herkunft

In den Befunden vom 11.10. steht oft „Nutzer“. In `evidence-authority.json` ist die Bestätigung „user / ThorstenHalsch“ zugeordnet. **Für jede Angabe muss eindeutig sein, wer sie gemacht hat** (Thorsten, Johannes, andere Vereinsmitglieder). Bitte beim Durchgang mit festhalten.

## Zusammenfassung

| | Anzahl |
|---|---:|
| Angaben in dieser Liste | 28 |
| ✅ korrekt im Register | 11 |
| ⚠️ im Register, aber veraltet / falsch zugeordnet / doppelt | 8 |
| ❌ fehlen im Register | 9 |
