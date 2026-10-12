# Archiv: Astras Forschungsseite mit 3D-Werkstatt

Archiviert am 12.10.2026 auf Anweisung von Johannes. Seitdem steht auf GitHub Pages nur das Cockpit.

## Was archiviert ist

- **Quellstand:** Branch `archiv/astra-forschungsseite-20261011` (Commit `c0c0704`). Das ist der Stand, aus dem Astras letzter Pages-Build am 11.10.2026 um 18:11 Uhr erzeugt wurde (Actions-Lauf 38162778134). Der Code liegt außerdem unverändert in `main` (`src/workbench/`, `src/pages/`); dort wird er aber nicht mehr weiterentwickelt.
- **Gebaute Fassungen** liegen als Actions-Artefakte im Repository (Actions → Lauf → Artifacts). Sie verfallen automatisch:

| Artefakt | Lauf | Größe | verfällt |
|---|---|---|---|
| pages-production-baseline-606908b | 38162747664 / 38162778134 | 125 MB | 09.01.2027 |
| pages-preview-validation | 38162778134 | 15 MB | 09.01.2027 |
| pages-preview-live-evidence | 38162778134 | 29 MB | 09.01.2027 |
| github-pages (letzte Forschungsseite) | 38162778134 | 196 MB | 12.10.2026, 20:21 |

Wer eine gebaute Fassung dauerhaft braucht, lädt `pages-production-baseline-606908b` vor dem 09.01.2027 herunter.

## Neu bauen

```
git checkout archiv/astra-forschungsseite-20261011
npm install
npm run build        # Ergebnis in dist/
```

Wieder veröffentlichen nur auf ausdrücklichen Auftrag von Johannes, dann mit `python scripts/kern/veroeffentliche_cockpit.py --seite dist` aus `main`.

## Warum archiviert

Die Werkstatt rechnet mit eigenen Parametern statt mit dem Wissenskern; Abweichungen stehen in [MODELL-BRUECKE.md](MODELL-BRUECKE.md), Funktionen und Anforderungen an den Nachfolger in [3D-WERKBANK-INVENTAR.md](3D-WERKBANK-INVENTAR.md). Das neue Modell entsteht aus dem Kern.
