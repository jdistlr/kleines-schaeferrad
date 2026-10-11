#!/usr/bin/env python3
"""Vergleicht die Parameter des alten 3D-Modells mit dem Wissenskern (nur lesend).

Das alte Modell (src/workbench/) liest seine Maße aus data/hypothesis.parameters.json.
Diese Brücke zeigt für jeden Parameter, welche Kern-Angaben dazu gehören, und ob sie
übereinstimmen. Sie ändert weder Modell noch Kern; sie bereitet Phase 3 vor
(Modell aus dem Kern speisen).

Aufruf: python scripts/kern/modell_bruecke.py   → schreibt docs/ordnung/MODELL-BRUECKE.md
"""
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Parameter des alten Modells → (Kern-Angaben, Umrechnung auf Meter, Bemerkung)
# Umrechnung: Funktion, die aus dem Kernwert den Modellwert macht (z. B. Durchmesser → Radius).
CM = lambda v: v / 100  # Skizzenmaße ohne Einheit in cm
MM = lambda v: v / 1000
M = lambda v: v
HALB_CM = lambda v: v / 200
HALB_M = lambda v: v / 2

BRUECKE = {
    "outerRadius": [("CLAIM-0236", CM, "Außenradius (Notiz)"), ("CLAIM-0234", HALB_CM, "Außendurchmesser (Notiz) / 2")],
    "innerRadius": [("CLAIM-0237", CM, "Innenradius (Notiz)"), ("CLAIM-0235", HALB_CM, "Innendurchmesser (Notiz) / 2")],
    "rimWidth": [("TH-20261009-26", M, "Thorsten"), ("CLAIM-0239", CM, "Skizze"), ("AN-20261012-40", M, "Foto")],
    "ringDistance": [("TH-20261009-28", M, "abgeleitet")],
    "shaftLength": [("CLAIM-0001", CM, "Skizze")],
    "shaftWidth": [("AN-20261011-11", M, "über Ecken"), ("AN-20261012-20", M, "Foto")],
    "armWidth": [("AN-20261012-09", M, "Foto"), ("AN-20261012-06", CM, "Armzeichnung")],
    "armDepth": [("AN-20261012-10", M, "Foto")],
    "vesselRadius": [("CLAIM-0026", lambda v: v / 2000, "Außendurchmesser unten / 2 (Skizze, mm)"), ("CLAIM-0025", lambda v: v / 2000, "Außendurchmesser oben / 2 (Skizze, mm)")],
    "vesselHeight": [("CLAIM-0024", MM, "Skizze, mm"), ("AN-20261012-46", M, "Foto am Neubau-Kumpf")],
    "vesselCount": [("CLAIM-0329", M, "Kontext")],
    "armsPerPlane": [("CLAIM-0326", M, "Kontext"), ("CLAIM-0018", M, "Skizze")],
    "segmentsPerPlane": [("CLAIM-0328", M, "Kontext")],
}

# Kern-Angaben, die das alte Modell noch gar nicht kennt, die ein neues aber braucht.
NEU = ["AN-20261012-30", "AN-20261012-21", "AN-20261012-22", "AN-20261012-19", "AN-20261012-12", "AN-20261012-11",
       "AN-20261012-05", "AN-20261012-03", "AN-20261012-34", "AN-20261011-04", "AN-20261012-28"]


def main():
    hyp = json.load(open(os.path.join(ROOT, "data", "hypothesis.parameters.json"), encoding="utf-8"))["parameters"]
    ang = {a["id"]: a for a in json.load(open(os.path.join(ROOT, "kern", "angaben.json"), encoding="utf-8"))["angaben"]}
    namen = {b["id"]: b["name"] for b in json.load(open(os.path.join(ROOT, "kern", "begriffe.json"), encoding="utf-8"))["begriffe"]}
    zeilen, abweichungen = [], []
    for par, eintrag in hyp.items():
        alt = eintrag.get("value")
        bezuege = BRUECKE.get(par, [])
        if not bezuege:
            zeilen.append(f"| `{par}` | {fmt(alt)} | – | – | noch keine Kern-Angabe |")
            continue
        for kid, umrechnen, wie in bezuege:
            a = ang.get(kid)
            if not a:
                zeilen.append(f"| `{par}` | {fmt(alt)} | {kid} | fehlt | Angabe nicht im Kern |")
                continue
            try:
                neu = umrechnen(float(a["wert"]))
            except (TypeError, ValueError):
                neu = None
            urteil = "–"
            if isinstance(alt, (int, float)) and neu is not None:
                rel = abs(neu - alt) / max(abs(alt), 1e-9)
                urteil = "stimmt" if rel < 0.03 else "weicht ab"
                if urteil == "weicht ab":
                    abweichungen.append(f"- `{par}`: Modell {fmt(alt)}, Kern {kid} ({wie}) {fmt(neu)}")
            zeilen.append(f"| `{par}` | {fmt(alt)} | {kid} ({wie}, {a['gueltigkeit']}) | {fmt(neu)} | {urteil} |")
    neu_z = []
    for kid in NEU:
        a = ang.get(kid)
        if a:
            neu_z.append(f"| {kid} | {namen.get(a['eigenschaft'], a['eigenschaft'])} | {fmt(a['wert'])} {a.get('einheit') or ''} | {a['grundlage']} |")
    text = f"""# Brücke: altes 3D-Modell ↔ Wissenskern

Erzeugt von `scripts/kern/modell_bruecke.py`. Nicht von Hand bearbeiten.

Das alte Modell (`src/workbench/`, Seite `/werkstatt/`) ist vollständig im Repository erhalten. Seine Maße stammen aus `data/hypothesis.parameters.json` und den Kalibrierdateien, nicht aus dem Kern. Diese Tabelle zeigt, wo beide übereinstimmen und wo nicht. Sie ändert nichts; das Umstellen des Modells beginnt erst nach Phase 2 des Ordnungsplans.

## Parameter des alten Modells

| Parameter | Modell | Kern-Angabe | Kern (umgerechnet, m) | Urteil |
|---|---|---|---|---|
{chr(10).join(zeilen)}

## Abweichungen

{chr(10).join(abweichungen) or "Keine."}

## Was das neue Modell zusätzlich braucht

Diese Angaben kennt das alte Modell nicht. Ein aus dem Kern gespeistes Modell kann sie nutzen.

| Kern-ID | Eigenschaft | Wert | Grundlage |
|---|---|---|---|
{chr(10).join(neu_z)}
"""
    ziel = os.path.join(ROOT, "docs", "ordnung", "MODELL-BRUECKE.md")
    with open(ziel, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"geschrieben: {os.path.relpath(ziel, ROOT)}, {len(abweichungen)} Abweichungen")


def fmt(v):
    if isinstance(v, float):
        return f"{v:.3f}".rstrip("0").rstrip(".").replace(".", ",")
    if v is None:
        return "–"
    return json.dumps(v, ensure_ascii=False) if not isinstance(v, (int, str)) else str(v)


if __name__ == "__main__":
    main()
