#!/usr/bin/env python3
"""Erzeugt das Cockpit (eine HTML-Seite) aus dem Wissenskern.

Aufruf:
  python scripts/kern/baue_cockpit.py              # schreibt cockpit/index.html (vollständiges Dokument)
  python scripts/kern/baue_cockpit.py --artefakt   # ohne Dokumentrahmen, für die Artifact-Vorschau

Das Cockpit ist nur eine Ansicht. Es wird nie von Hand bearbeitet; Änderungen gehören in kern/.
"""
import json
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HIER, "..", ".."))
sys.path.insert(0, HIER)
from pruefe_kern import lade_kern, pruefe  # noqa: E402


def main():
    kern_dir = os.path.join(ROOT, "kern")
    fehler, _, st = pruefe(kern_dir, ROOT)
    if fehler:
        sys.exit(f"Kern hat {len(fehler)} Fehler; zuerst python scripts/kern/pruefe_kern.py ausführen.")
    d = lade_kern(kern_dir)
    with open(os.path.join(kern_dir, "angaben.json"), encoding="utf-8") as f:
        stand = json.load(f).get("stand")

    daten = {
        "stand": stand,
        "statistik": {k: (dict(v) if hasattr(v, "items") else v) for k, v in st.items()},
        "bauteile": [{**{k: b.get(k) for k in ("id", "name", "begriff", "art", "teil_von", "hinweis")},
                      # Anzahltexte aus den Altdaten sind teils englisch und vage; nur gepflegte zeigen.
                      "anzahl": None if (b.get("herkunft") or {}).get("datei") == "data/components.json" else b.get("anzahl")}
                     for b in d["bauteile"]],
        "begriffe": [{k: b.get(k) for k in ("id", "name", "definition", "aliase")} for b in d["begriffe"]],
        "personen": [{"id": p["id"], "name": p["name"]} for p in d["personen"]],
        "beziehungen": [{k: b.get(k) for k in ("id", "von", "art", "zu", "ueber")} for b in d["beziehungen"]],
        "angaben": [{"id": a["id"], "ziel": a["ziel"], "eig": a["eigenschaft"], "wert": a["wert"], "einheit": a["einheit"],
                     "tol": a.get("toleranz"), "grund": a["grundlage"], "guelt": a["gueltigkeit"],
                     "quellen": [q["quelle"] for q in a["quellen"]]} for a in d["angaben"]],
        "fragen": [{k: f.get(k) for k in ("id", "frage", "betrifft", "blockiert", "haengt_ab_von", "entscheidet", "status", "hinweis", "herkunft")} for f in d["fragen"]],
        "quellen": [{"id": q["id"], "art": q["art"], "pfad": q["pfad"], "titel": q["titel"], "ordner": q["ordner"],
                     "erschlossen": q["erschlossen"], "identisch": bool(q["identisch_mit"])} for q in d["quellen"]],
    }
    with open(os.path.join(HIER, "cockpit", "vorlage.html"), encoding="utf-8") as f:
        vorlage = f.read()
    json_text = json.dumps(daten, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    seite = vorlage.replace("/*__DATEN__*/null", json_text)
    if "--artefakt" in sys.argv:
        ziel = os.path.join(ROOT, "cockpit", "artefakt.html")
    else:
        seite = ('<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n'
                 '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n</head>\n<body>\n'
                 + seite + "\n</body>\n</html>\n")
        ziel = os.path.join(ROOT, "cockpit", "index.html")
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    with open(ziel, "w", encoding="utf-8") as f:
        f.write(seite)
    print(f"Cockpit geschrieben: {os.path.relpath(ziel, ROOT)} ({len(seite) // 1024} KB)")


if __name__ == "__main__":
    main()
