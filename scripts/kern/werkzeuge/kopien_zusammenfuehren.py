#!/usr/bin/env python3
"""Führt Quellen mit identischem Dateiinhalt zu einer Quelle zusammen.

Identisch heißt: gleicher Git-Blob. Pro Inhalt bleibt eine Hauptquelle; die übrigen
Dateien stehen dort unter `kopien` (Pfad und frühere ID). Alle Verweise im Kern
werden auf die Hauptquelle umgestellt, die früheren IDs bleiben unter `alt_ids`.

Wahl der Hauptquelle: zuerst eine bereits ausgewertete, dann eine im Bauteilordner
(nicht originaltransfer/context), dann die kürzeste ID. Die Art wird „skizze“,
wenn eine der Kopien als Skizze geführt war.

Idempotent. Aufruf: python scripts/kern/werkzeuge/kopien_zusammenfuehren.py
"""
import json
import os
import subprocess
from collections import OrderedDict, defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
KERN = os.path.join(ROOT, "kern")
MEDIEN = {"foto", "skizze", "scan", "video"}


def lade(name):
    with open(os.path.join(KERN, name + ".json"), encoding="utf-8") as f:
        return json.load(f, object_pairs_hook=OrderedDict)


def schreibe(name, daten):
    with open(os.path.join(KERN, name + ".json"), "w", encoding="utf-8") as f:
        json.dump(daten, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    blob = {}
    for zeile in subprocess.check_output(["git", "ls-files", "-s", "evidence/raw"], cwd=ROOT, text=True).splitlines():
        meta, pfad = zeile.split("\t", 1)
        blob[pfad] = meta.split()[1]

    qd = lade("quellen")
    gruppen = defaultdict(list)
    for q in qd["quellen"]:
        q.pop("identisch_mit", None)
        q.setdefault("kopien", [])
        if q["art"] in MEDIEN and q.get("pfad") in blob:
            gruppen[blob[q["pfad"]]].append(q)

    umleitung = {}
    for liste in gruppen.values():
        if len(liste) < 2:
            continue
        rang = lambda q: (not q["erschlossen"], (q.get("ordner") or "").startswith(("originaltransfer", "context")), len(q["id"]), q["id"])
        haupt, *rest = sorted(liste, key=rang)
        if any(q["art"] == "skizze" for q in liste):
            haupt["art"] = "skizze"
        for q in rest:
            umleitung[q["id"]] = haupt["id"]
            haupt["kopien"].append(OrderedDict([("pfad", q["pfad"]), ("id", q["id"])]))
            haupt["kopien"].extend(q.get("kopien", []))
            haupt["alt_ids"] = sorted(set(haupt.get("alt_ids", [])) | {q["id"], *q.get("alt_ids", [])})
            haupt["erschlossen"] = haupt["erschlossen"] or q["erschlossen"]
            if not haupt.get("titel"):
                haupt["titel"] = q.get("titel")
    qd["quellen"] = [q for q in qd["quellen"] if q["id"] not in umleitung]
    schreibe("quellen", qd)

    def um(x):
        return umleitung.get(x, x)

    geaendert = 0
    for name, feld in (("angaben", "angaben"), ("beziehungen", "beziehungen"), ("arbeitsschritte", "arbeitsschritte"),
                       ("begruendungen", "begruendungen"), ("fragen", "fragen")):
        d = lade(name)
        for e in d[feld]:
            for schluessel in ("quellen", "betrifft", "blockiert"):
                if schluessel not in e:
                    continue
                neu = []
                for x in e[schluessel]:
                    if isinstance(x, dict) and "quelle" in x:
                        if x["quelle"] in umleitung:
                            geaendert += 1
                        x["quelle"] = um(x["quelle"])
                        if not any(isinstance(y, dict) and y["quelle"] == x["quelle"] and y.get("stelle") == x.get("stelle") for y in neu):
                            neu.append(x)
                    else:
                        if x in umleitung:
                            geaendert += 1
                        if um(x) not in neu:
                            neu.append(um(x))
                e[schluessel] = neu
        schreibe(name, d)
    print(f"{len(umleitung)} Kopien in {sum(1 for l in gruppen.values() if len(l) > 1)} Hauptquellen zusammengeführt, {geaendert} Verweise umgestellt.")


if __name__ == "__main__":
    main()
