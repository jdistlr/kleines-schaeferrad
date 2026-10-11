#!/usr/bin/env python3
"""Verständliche Bauteilnamen und Zuordnung jedes Fotos zu seinem Bauteil (nach Ordner).

Idempotent. Die alten Namen bleiben unter herkunft erhalten.
Aufruf: python scripts/kern/werkzeuge/namen_und_fotozuordnung.py
"""
import json
import os
from collections import OrderedDict

KERN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "kern")

NAMEN = {
    "ANLAGE": "Kleines Schäferrad", "COMP-SHAFT": "Welle", "COMP-ARMS": "Arme", "COMP-RIMS": "Kränze",
    "COMP-HUB-LAND": "Armzone Land", "COMP-HUB-WATER": "Armzone Wasser", "COMP-KUEMPFE": "Kümpfe",
    "COMP-KUMPF-HOOPS": "Kumpfreifen", "COMP-PADDLES": "Flügelbretter", "COMP-FASTENERS": "Keile, Stifte und Bänder",
    "COMP-KUMPF-NAILS": "Kumpfnägel", "COMP-BEARINGS": "Wellenlager", "COMP-RADSTATT": "Radstadt",
    "COMP-TROUGH": "Schöpftrog", "COMP-BEARING-STANDS": "Lagerböcke", "COMP-FRAME-MAIN": "Pfosten und Tragbalken",
    "COMP-FRAME-LOWER": "Untere Rahmenhölzer", "COMP-FRAME-SIDE": "Seitliche Rahmenhölzer",
    "COMP-SCHETTERNBRETTER": "Schetternbretter", "COMP-WOOD-BANDS": "Holzbänder", "COMP-A-BOCK": "A-Bock",
    "COMP-CHANNEL": "Rinne", "COMP-SHAFT-CLAMPS": "Wellenschellen", "COMP-RIM-JOINT-WEDGE": "Stoßkeile",
    "COMP-RINNE": "Rinne 1 (am Trog)", "COMP-RINNE-2": "Rinne 2 (zum Auslass)",
}

ORDNER = {
    "A-Bock": "COMP-A-BOCK", "Arme": "COMP-ARMS", "Auffangtrog": "COMP-TROUGH", "Fluegelbretter": "COMP-PADDLES",
    "Gesamtansichten": "ANLAGE", "Keile": "COMP-FASTENERS", "Kruemmlinge": "COMP-KRUEMMLINGE", "Kumpf": "COMP-KUEMPFE",
    "Lagerboch Landseite": "COMP-TROUGH-SUPPORT", "Lagerbock Wasserseite": "COMP-BEARING-STANDS",
    "Radstadt": "COMP-RADSTATT", "Radstatt": "COMP-RADSTATT", "Rinne": "COMP-CHANNEL",
    "Schetternbretter": "COMP-SCHETTERNBRETTER", "Welle": "COMP-SHAFT",
}


def bearbeite(name, schluessel, f):
    p = os.path.join(KERN, name + ".json")
    with open(p, encoding="utf-8") as h:
        d = json.load(h, object_pairs_hook=OrderedDict)
    for e in d[schluessel]:
        f(e)
    with open(p, "w", encoding="utf-8") as h:
        json.dump(d, h, ensure_ascii=False, indent=2)
        h.write("\n")


def name(b):
    if b["id"] in NAMEN and b["name"] != NAMEN[b["id"]]:
        b.setdefault("herkunft", OrderedDict())
        b["herkunft"].setdefault("name", b["name"])
        b["name"] = NAMEN[b["id"]]


def zuordnung(q):
    if q.get("ordner") in ORDNER and not q.get("bauteil"):
        q["bauteil"] = ORDNER[q["ordner"]]


bearbeite("bauteile", "bauteile", name)
bearbeite("quellen", "quellen", zuordnung)
print("Namen und Fotozuordnung gesetzt.")
