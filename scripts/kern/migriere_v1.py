#!/usr/bin/env python3
"""Einmalige Migration der Altdaten in das Kernmodell (kern/).

Liest (unverändert):
  data/geometry.claims.json, data/components.json, data/conflicts.json,
  data/knowledge-gaps.json, data/source-analyses.json, evidence/manifest.json,
  evidence/additions-v2.json, evidence/component-index.json,
  evidence/contributions/*.json und die Dateiliste unter evidence/raw/.

Schreibt:
  kern/bauteile.json, kern/beziehungen.json, kern/angaben.json,
  kern/quellen.json, kern/fragen.json, kern/arbeitsschritte.json,
  kern/begruendungen.json, kern/migration/v1-zuordnung.json

Grundsätze:
  * Altdateien werden nie verändert. Jede Alt-ID ist über `herkunft` bzw. die
    Zuordnungsdatei auffindbar; Rückbau = kern/ löschen.
  * Keine Angabe wird als „bestaetigt“ migriert. Das entscheiden Menschen.
  * Die Nachträge vom 11.10.2026 (Abschnitt NACHTRAEGE) stammen aus den
    Befunden unter evidence/raw/*/BEFUND.md und sind als „offen“ markiert.

Nach dem ersten Lauf ist kern/ die handgepflegte Quelle. Ein erneuter Lauf
überschreibt nur mit --neu.

Aufruf: python scripts/kern/migriere_v1.py [--neu]
"""
import json
import os
import re
import subprocess
import sys
from collections import OrderedDict, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from eigenschaften_de import BAUTEIL_TEXTE, EIG, KONTEXT_TITEL, SCHLUESSEL, WERT, slug  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
KERN = os.path.join(ROOT, "kern")
STAND = "2026-10-11"


def lade(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


def schreibe(rel, daten):
    pfad = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    with open(pfad, "w", encoding="utf-8") as f:
        json.dump(daten, f, ensure_ascii=False, indent=2)
        f.write("\n")


# --------------------------------------------------------------------------
# Feste Zuordnungen (bewusst explizit, damit sie im Review sichtbar sind)
# --------------------------------------------------------------------------

BEGRIFF_JE_KOMPONENTE = {
    "COMP-SHAFT": "B-WELLE", "COMP-HUB-LAND": "B-ARMZONE", "COMP-HUB-WATER": "B-ARMZONE",
    "COMP-ARMS": "B-ARM", "COMP-RIM-LAND": "B-KRANZ", "COMP-RIM-WATER": "B-KRANZ",
    "COMP-RIMS": "B-KRANZ", "COMP-KRUEMMLINGE": "B-KRUEMMLING", "COMP-KUEMPFE": "B-KUMPF",
    "COMP-KUMPF-STAVES": "B-DAUBE", "COMP-KUMPF-BASE": "B-KUMPFBODEN",
    "COMP-KUMPF-HOOPS": "B-KUMPFREIFEN", "COMP-PADDLES": "B-FLUEGELBRETT",
    "COMP-FASTENERS": "B-BEFESTIGUNG", "COMP-KUMPF-NAILS": "B-KUMPFNAGEL",
    "COMP-BEARINGS": "B-LAGER", "COMP-RADSTATT": "B-RADSTADT", "COMP-TROUGH": "B-SCHOEPFTROG",
    "COMP-RINNE": "B-RINNE", "TOOL-BENDING-DIE": "B-BIEGEMATRIZE", "REF-BOARD": "B-VORLAGE",
    "REF-POLYGON": "B-VORLAGE", "REF-CONTACTSTRIPS": "B-VORLAGE",
    "COMP-BEARING-STANDS": "B-LAGERBOCK", "COMP-FRAME-MAIN": "B-RAHMEN",
    "COMP-FRAME-LOWER": "B-RAHMEN", "COMP-FRAME-SIDE": "B-RAHMEN",
    "COMP-SCHETTERNBRETTER": "B-SCHETTERNBRETT", "COMP-WOOD-BANDS": "B-HOLZBAND",
    "COMP-TROUGH-SUPPORT": "B-LAGERBOCK", "COMP-A-BOCK": "B-A-BOCK", "COMP-CHANNEL": "B-RINNE",
    "COMP-SHAFT-CLAMPS": "B-SCHELLE",
}

ART_JE_KIND = {
    "physical-part": "teil", "physical-part-family": "teil", "assembly": "baugruppe",
    "assembly-family": "baugruppe", "fixed-assembly": "baugruppe", "fixed-context-family": "baugruppe",
    "region-of-shaft": "zone", "joint-family": "zone", "manufacturing-tool": "werkzeug",
    "unassigned-reference": "vorlage", "unassigned-industrial-reference": "vorlage",
}

TEIL_VON = {
    "COMP-WHEEL": "ANLAGE", "COMP-RADSTATT": "ANLAGE", "COMP-WATERWAY": "ANLAGE",
    "COMP-SHAFT": "COMP-WHEEL", "COMP-ARMS": "COMP-WHEEL", "COMP-RIMS": "COMP-WHEEL",
    "COMP-KUEMPFE": "COMP-WHEEL", "COMP-PADDLES": "COMP-WHEEL", "COMP-FASTENERS": "COMP-WHEEL",
    "COMP-BEARINGS": "COMP-WHEEL", "COMP-SHAFT-WEDGE": "COMP-WHEEL",
    "COMP-SHAFT-CLAMPS": "COMP-SHAFT", "COMP-HUB-LAND": "COMP-SHAFT", "COMP-HUB-WATER": "COMP-SHAFT",
    "COMP-RIM-LAND": "COMP-RIMS", "COMP-RIM-WATER": "COMP-RIMS", "COMP-KRUEMMLINGE": "COMP-RIMS",
    "COMP-SCHETTERNBRETTER": "COMP-RIMS", "COMP-RIM-JOINT-WEDGE": "COMP-RIMS",
    "COMP-KUMPF-STAVES": "COMP-KUEMPFE", "COMP-KUMPF-BASE": "COMP-KUEMPFE",
    "COMP-KUMPF-HOOPS": "COMP-KUEMPFE", "COMP-KUMPF-NAILS": "COMP-KUEMPFE",
    "COMP-WOOD-BANDS": "COMP-PADDLES",
    "COMP-BEARING-STANDS": "COMP-RADSTATT", "COMP-FRAME-MAIN": "COMP-RADSTATT",
    "COMP-FRAME-LOWER": "COMP-RADSTATT", "COMP-FRAME-SIDE": "COMP-RADSTATT",
    "COMP-TROUGH-SUPPORT": "COMP-RADSTATT", "COMP-RADSTATT-OBERBALKEN": "COMP-RADSTATT",
    "COMP-TROUGH": "COMP-WATERWAY", "COMP-CHANNEL": "COMP-WATERWAY", "COMP-A-BOCK": "COMP-WATERWAY",
    "COMP-RINNE": "COMP-CHANNEL", "COMP-RINNE-2": "COMP-CHANNEL",
    "REF-CONTACTSTRIP-1": "REF-CONTACTSTRIPS", "REF-CONTACTSTRIP-2": "REF-CONTACTSTRIPS",
    "REF-CONTACTSTRIP-3": "REF-CONTACTSTRIPS",
}

NEUE_BAUTEILE = [
    ("ANLAGE", "Kleines Schäferrad (Gesamtanlage)", "B-ANLAGE", "anlage", "eine", "Wurzel des Inventars; nimmt auch Projekt- und Standortangaben auf."),
    ("COMP-WHEEL", "Wasserrad", "B-WASSERRAD", "baugruppe", "eines", None),
    ("COMP-WATERWAY", "Wasserführung", "B-WASSERFUEHRUNG", "baugruppe", "eine", None),
    ("COMP-RINNE-2", "Rinne 2 (zum Auslass)", "B-RINNE", "teil", "eines", "Zweiter Rinnenteil; keine eigene Zeichnung bekannt. COMP-RINNE ist Rinne 1 (hinter Trog)."),
    ("COMP-RADSTATT-OBERBALKEN", "Obere Balken der Radstadt", "B-RAHMEN", "teil", "mehrere; Anzahl offen", None),
    ("COMP-SHAFT-WEDGE", "Wellenkeil", "B-WELLENKEIL", "teil", "mindestens einer; Anzahl offen", None),
    ("COMP-RIM-JOINT-WEDGE", "Stoßkeile der Krümmlinge", "B-STOSSKEIL", "teil", "einer je Krümmlingstoß", None),
    ("REF-MEDIUM-KUMPF", "Kumpf-Größenvariante „mittel“ (Skizze)", "B-VORLAGE", "vorlage", "Skizze", "Größenvariante laut Kumpfskizze; Bezug zum heutigen Kumpf über Frage zu klären."),
    ("REF-SMALL-KUMPF", "Kumpf-Größenvariante „klein“ (Skizze)", "B-VORLAGE", "vorlage", "Skizze", "Größenvariante laut Kumpfskizze; Bezug zum heutigen Kumpf über Frage zu klären."),
    ("REF-CONTACTSTRIP-1", "Kontaktstreifen-Vorlage 1", "B-VORLAGE", "vorlage", "Vorlage", "Industrielle Vorlage; ob sie zum Rad gehört, ist offen."),
    ("REF-CONTACTSTRIP-2", "Kontaktstreifen-Vorlage 2", "B-VORLAGE", "vorlage", "Vorlage", "Industrielle Vorlage; ob sie zum Rad gehört, ist offen."),
    ("REF-CONTACTSTRIP-3", "Kontaktstreifen-Vorlage 3", "B-VORLAGE", "vorlage", "Vorlage", "Industrielle Vorlage; ob sie zum Rad gehört, ist offen."),
]

# Posten der allgemeinen Holzliste: eindeutig zuordenbare gehen auf das Bauteil,
# die übrigen werden eigene Listenposten mit offener Zuordnung.
HOLZLISTE_ZIEL = {
    "REF-Arme": "COMP-ARMS", "REF-Welle": "COMP-SHAFT", "REF-Krümmlinge": "COMP-KRUEMMLINGE",
    "REF-Kumpf": "COMP-KUEMPFE", "REF-Schaufeln": "COMP-PADDLES", "REF-Rinne": "COMP-CHANNEL",
    "REF-Gießtrog": "COMP-TROUGH",
}

ZUSAMMENGESETZT = {
    # Altsubjekt: (von, art, zu, ueber)
    "COMP-A-BOCK/COMP-CHANNEL": ("COMP-CHANNEL", "liegt_auf", "COMP-A-BOCK", []),
    "COMP-ARMS/COMP-KRUEMMLINGE": ("COMP-ARMS", "steckt_in", "COMP-KRUEMMLINGE", []),
    "COMP-ARMS/COMP-RADSTATT": ("COMP-ARMS", "abstand_zu", "COMP-RADSTATT", []),
    "COMP-SHAFT/COMP-BEARINGS": ("COMP-SHAFT", "lagert_in", "COMP-BEARINGS", []),
    "COMP-WOOD-BANDS/COMP-PADDLES/COMP-KRUEMMLINGE": ("COMP-WOOD-BANDS", "befestigt", "COMP-PADDLES", ["COMP-KRUEMMLINGE"]),
}

ZIEL_ALIAS = {"COMP-RADSTADT": "COMP-RADSTATT", "PROJECT": "ANLAGE", "SITE": "ANLAGE"}

EINHEIT = {"m": "m", "cm": "cm", "mm": "mm", "degree": "grad", "deg": "grad",
           "count": "anzahl", "export-unit": "exporteinheit", None: None}


def deutsch(wert):
    if isinstance(wert, str):
        return WERT.get(wert, wert)
    if isinstance(wert, list):
        return [deutsch(x) for x in wert]
    if isinstance(wert, dict):
        return OrderedDict((SCHLUESSEL.get(k, k), deutsch(v)) for k, v in wert.items())
    return wert


def grundlage(klasse, bereich):
    if klasse == "measured":
        return "scan" if bereich == "digital-artifact-only" else "messung"
    if klasse == "historical-drawing":
        if bereich == "generic-stock-recommendation":
            return "holzliste"
        if bereich.startswith("industrial-template"):
            return "fremdvorlage"
        return "skizze"
    if klasse == "observed-current":
        return "scan" if bereich in ("partial-scan-interpretation", "capture-ui-only") else "foto"
    if klasse == "expert-narrative":
        return "muendlich"
    if klasse == "external-context":
        return "kontext"
    if klasse in ("derived", "inferred"):
        return "ableitung"
    raise ValueError(f"Keine Grundlage für {klasse}/{bereich}")


def gueltigkeit_fuer(grund):
    # Holzliste und Fremdvorlagen beschreiben nicht das heutige Rad, sondern
    # dokumentieren eine Unterlage. Alles andere ist offen, bis ein Mensch entscheidet.
    return "historisch" if grund in ("holzliste", "fremdvorlage") else "offen"


# --------------------------------------------------------------------------
# Quellen
# --------------------------------------------------------------------------

def git_dateien():
    out = subprocess.check_output(["git", "ls-files", "-s", "evidence/raw"], cwd=ROOT, text=True)
    dateien = {}
    for zeile in out.splitlines():
        meta, pfad = zeile.split("\t", 1)
        dateien[pfad] = meta.split()[1]
    return dateien


def art_aus_pfad(pfad):
    ext = pfad.rsplit(".", 1)[-1].lower()
    if ext in ("glb", "ply"):
        return "scan"
    if ext == "mp4":
        return "video"
    if "/Arbeitsunterlagen/" in pfad:
        return "skizze"
    return "foto"


KIND_ART = {"historical_document_photo": "skizze", "photo": "foto", "current_photo": "foto",
            "capture_metadata": "scan", "glb": "scan", "ply": "scan", "expert-contribution": "aussage"}


def baue_quellen(dateien, sa):
    quellen = OrderedDict()
    pfad_zu_id = {}
    alias = {}

    def neu(qid, art, pfad=None, titel=None, person=None, hinweis=None):
        if pfad and pfad in pfad_zu_id:
            primaer = pfad_zu_id[pfad]
            if qid != primaer:
                alias[qid] = primaer
                quellen[primaer]["alt_ids"].append(qid)
            return
        if qid in quellen:
            return
        quellen[qid] = OrderedDict([
            ("id", qid), ("art", art), ("pfad", pfad), ("titel", titel),
            ("person", person), ("ordner", pfad.split("/")[2] if pfad and pfad.startswith("evidence/raw/") else None),
            ("erschlossen", False), ("identisch_mit", []), ("alt_ids", []), ("hinweis", hinweis),
        ])
        if pfad:
            pfad_zu_id[pfad] = qid

    vorher = {}
    ci = lade("evidence/component-index.json")["assets"]
    for a in ci:
        if a.get("previous_path"):
            vorher[a["previous_path"]] = a["path"]

    def aktuell(p):
        if not p:
            return None
        p = vorher.get(p, p)
        return p if os.path.exists(os.path.join(ROOT, p)) else None

    man = lade("evidence/manifest.json")
    for a in man["assets"]:
        p = aktuell((a.get("archive") or {}).get("path") or a.get("path"))
        art = KIND_ART.get(a["kind"], "foto")
        if a["id"].startswith("NARRATIVE-"):
            art = "aussage"
        neu(a["id"], art, p, a.get("filename"),
            "P-THORSTEN" if art == "aussage" and "TH" in a["id"] else None)
    for a in man["derived_assets"]:
        neu(a["id"], "ableitung", aktuell(a.get("path")), None)
    for a in man["context_sources"]:
        qid = a["id"]
        quellen.setdefault(qid, OrderedDict([
            ("id", qid), ("art", "kontext"), ("pfad", aktuell(a.get("path"))), ("titel", KONTEXT_TITEL.get(a.get("kind"))),
            ("person", None), ("ordner", None), ("erschlossen", False), ("identisch_mit", []),
            ("alt_ids", []), ("hinweis", None)]))
    for a in lade("evidence/additions-v2.json")["assets"]:
        neu(a["id"], art_aus_pfad(a["archive_path"]), aktuell(a["archive_path"]), a.get("uploaded_name"))
    for a in ci:
        p = aktuell(a["path"])
        if a.get("source_id"):
            neu(a["source_id"], art_aus_pfad(a["path"]), p, a.get("filename"))
    for s in sa:
        sid = s["source_id"]
        if sid in quellen or sid in alias:
            continue
        if sid.startswith("NARRATIVE-"):
            neu(sid, "aussage", None, s.get("title"), "P-THORSTEN" if "-TH-" in sid else None)
        else:
            treffer = [a["path"] for a in ci if a.get("source_id") == sid]
            neu(sid, art_aus_pfad(treffer[0]) if treffer else "foto", aktuell(treffer[0]) if treffer else None, s.get("title"))

    # Restliche Dateien unter evidence/raw (Bilder, Scans, Video), noch ohne ID
    for pfad in sorted(dateien):
        if pfad.endswith((".md", ".json")) or pfad in pfad_zu_id:
            continue
        stamm = re.sub(r"[^A-Za-z0-9]+", "-", pfad[len("evidence/raw/"):].rsplit(".", 1)[0]).strip("-")
        neu("DATEI-" + stamm, art_aus_pfad(pfad), pfad, os.path.basename(pfad))

    # Skizzen anhand der Quellanalyse erkennen
    for s in sa:
        qid = alias.get(s["source_id"], s["source_id"])
        if qid in quellen:
            quellen[qid]["erschlossen"] = True
            if (s.get("document_group") or "").startswith("DOC-") and quellen[qid]["art"] == "foto":
                quellen[qid]["art"] = "skizze"
            if quellen[qid]["titel"] is None:
                quellen[qid]["titel"] = s.get("title")

    # Identische Dateien (gleicher Git-Blob) markieren
    je_blob = defaultdict(list)
    for q in quellen.values():
        if q["pfad"] in dateien:
            je_blob[dateien[q["pfad"]]].append(q["id"])
    for ids in je_blob.values():
        if len(ids) > 1:
            for qid in ids:
                quellen[qid]["identisch_mit"] = [x for x in ids if x != qid]

    return quellen, alias


# --------------------------------------------------------------------------
# Nachträge vom 11.10.2026 (aus den Befunden, alle „offen“)
# --------------------------------------------------------------------------

AUSSAGE_QUELLEN = [
    ("Q-AUSSAGE-20261011-RADSTADT", "evidence/raw/Radstadt/BEFUND.md", "Gesprächsangaben zur Radstadt (Balkenquerschnitt, lichte Weiten)"),
    ("Q-AUSSAGE-20261011-RINNE", "evidence/raw/Rinne/BEFUND.md", "Gesprächsangaben zu Rinne, Überlappung und A-Bock"),
    ("Q-AUSSAGE-20261011-TROG", "evidence/raw/Auffangtrog/BEFUND.md", "Gesprächsangaben zu Schöpftrog und Auflagerfolge"),
    ("Q-AUSSAGE-20261011-KRUEMMLINGE", "evidence/raw/Kruemmlinge/BEFUND.md", "Gesprächsangaben zu Krümmlingbohrungen und Stoßkeil"),
    ("Q-AUSSAGE-20261011-ARME", "evidence/raw/Arme/ASTRA-HANDOFF.md", "Gesprächsangaben zu Armtypen und Verschränkung"),
    ("Q-AUSSAGE-20261011-WELLE", "evidence/raw/Welle/BEFUND.md", "Gesprächsangaben zu Welle, Zwölfeck und Schellen"),
    ("Q-AUSSAGE-20261011-WELLENKEIL", "evidence/contributions/wellenkeil-20261011.json", "Gesprächsangaben zum Wellenkeil"),
]
PERSON_OFFEN = "Im Befund als „Nutzer“ bezeichnet; Person in Frage F-007 klären."


def nachtrag(nr, ziel, eig, wert, einheit, quellen, hinweis=None, grund="muendlich", toleranz=None,
             gueltigkeit="offen", ersetzt_durch=None, begruendung=None):
    return OrderedDict([
        ("id", f"AN-20261011-{nr:02d}"), ("ziel", ziel), ("eigenschaft", eig), ("wert", wert),
        ("einheit", einheit), ("toleranz", toleranz), ("grundlage", grund),
        ("quellen", [{"quelle": q, "stelle": s} for q, s in quellen]),
        ("aussage_von", None), ("gueltigkeit", gueltigkeit), ("bestaetigt", None),
        ("ersetzt_durch", ersetzt_durch), ("begruendung", begruendung),
        ("hinweis", hinweis), ("herkunft", {"datei": "Nachtrag 11.10.2026", "id": None}),
    ])


def nachtraege():
    R, K, A, W, WK, T = ("Q-AUSSAGE-20261011-RADSTADT", "Q-AUSSAGE-20261011-KRUEMMLINGE",
                         "Q-AUSSAGE-20261011-ARME", "Q-AUSSAGE-20261011-WELLE",
                         "Q-AUSSAGE-20261011-WELLENKEIL", "Q-AUSSAGE-20261011-TROG")
    return [
        nachtrag(1, "COMP-RADSTATT-OBERBALKEN", "querschnitt_breite_hoehe", [0.40, 0.20], "m", [(R, "Obere Balken")],
                 "Naturholz: reale Querschnitte variieren.", toleranz={"art": "vereinfachung", "text": "bewusste Vereinsvereinfachung, keine Toleranzzahl angegeben"}),
        nachtrag(2, "COMP-RADSTATT", "lichte_weite_land_wasser", 3.40, "m", [(R, "Lichte Öffnung")],
                 "Korrigiert die zuvor genannten 2,40 m. Zeichnung: 3,84 m Achsmaß − 2 × 0,20 m = 3,44 m."),
        nachtrag(3, "COMP-RADSTATT", "lichte_weite_land_wasser", 2.40, "m", [(R, "Lichte Öffnung, frühere Angabe")],
                 "Vom Aussagenden ausdrücklich als Fehler zurückgenommen.", gueltigkeit="ueberholt", ersetzt_durch="AN-20261011-02"),
        nachtrag(4, "COMP-RADSTATT", "lichte_weite_parallel_ufer", 4.40, "m", [(R, "Lichte Öffnung")],
                 "Vom Aussagenden selbst angezweifelt („möglicherweise vermessen“). Widerspricht Drehkreis 4,66–4,96 m und Zeichnung 5,25 m; siehe F-001."),
        nachtrag(5, "COMP-RIM-LAND", "zusaetzliche_bohrungen_je_kumpf", 2, "anzahl", [(K, "Fachauskunft")],
                 "Bohrungen für die Kumpfbefestigung; nicht auf den Wasserkranz spiegeln."),
        nachtrag(6, "COMP-RIM-WATER", "zusaetzliche_bohrungen_je_kumpf", 0, "anzahl", [(K, "Fachauskunft")],
                 "Wasserseitige Krümmlinge haben nur die Schetternbrett-Bohrungen."),
        nachtrag(7, "COMP-RIM-JOINT-WEDGE", "funktion", "Schließt den Spalt zwischen zwei Krümmlingen und verspannt den Kranz über die Schetternägel.", None,
                 [(K, "Stoßspalt, Keil und Verspannung")], "Spaltweite, Keilmaße und Einsteckrichtung offen.", begruendung="G-003"),
        nachtrag(8, "COMP-SHAFT-WEDGE", "laenge", 0.44, "m", [("PHOTO-WELLENKEIL-IMG20261010124805", "Gesamtansicht mit Zollstock")],
                 "Fotoablesung, perspektivisch begrenzt.", grund="foto", toleranz={"art": "bereich", "von": 0.43, "bis": 0.45}),
        nachtrag(9, "COMP-SHAFT-WEDGE", "endstaerke", 0.055, "m", [(WK, "dimensions")], "Ungefähre Angabe; Gegenende und Keilwinkel offen.",
                 toleranz={"art": "ungefaehr", "text": "ca."}),
        nachtrag(10, "COMP-SHAFT", "querschnittsform", "Zwölfeck", None, [(W, "Bestätigte Grundlagen"), ("PHOTO-6816", "Querschnitt")]),
        nachtrag(11, "COMP-SHAFT", "durchmesser_ueber_ecken", 0.37, "m", [(W, "Bestätigte Grundlagen"), ("PHOTO-6816", "oberes Quermaß")],
                 "Präzisiert CLAIM-0002 (37 ohne Bezug): gemessen über gegenüberliegende Ecken. Abstand über Flächen rechnerisch ≈ 0,357 m."),
        nachtrag(12, "COMP-ARMS", "armtypen", "Drei Armtypen je Armzone: ein gerader Mittelarm und zwei gegensinnig gekröpfte Außenarme; jeder Typ zweimal im Rad.", None,
                 [(A, "Vom Nutzer erklärte Konstruktion")], begruendung="G-004"),
        nachtrag(13, "COMP-SHAFT", "armoeffnung_groesser_als_arm", True, None, [(W, "Bestätigte Grundlagen")],
                 "Öffnung 16 × 9 cm, Arm 14 × 6,5 cm.", begruendung="G-002"),
        nachtrag(14, "COMP-CHANNEL", "grundrisswinkel_frei_waehlbar", True, None, [(T, "Bestätigte Beziehungen")],
                 "Winkel und Lage der Rinne zum Rad dürfen plausibel gewählt werden; gewählte Werte als Annahme kennzeichnen."),
    ]


def neue_beziehungen():
    R, K, A, W, WK, T = ("Q-AUSSAGE-20261011-RINNE", "Q-AUSSAGE-20261011-KRUEMMLINGE",
                         "Q-AUSSAGE-20261011-ARME", "Q-AUSSAGE-20261011-WELLE",
                         "Q-AUSSAGE-20261011-WELLENKEIL", "Q-AUSSAGE-20261011-TROG")
    return [
        ("COMP-RINNE", "liegt_auf", "COMP-TROUGH-SUPPORT", [], [T], "Rinne 1 liegt auf dem oberen Querbalken des landseitigen Lagerbocks; Identität siehe F-004."),
        ("COMP-TROUGH", "liegt_auf", "COMP-RINNE", [], [T], "Schöpftrog liegt im Anschlussbereich auf der Rinne."),
        ("COMP-RINNE", "ueberlappt", "COMP-RINNE-2", [], [R], "Überlappungslänge offen (F-006). Präzisiert den „Stoß“ in TH-20261009-31."),
        ("COMP-ARMS", "verschraenkt_mit", "COMP-ARMS", [], [A], "Die drei Arme einer Armzone greifen über Aussparungen ineinander; siehe F-005."),
        ("COMP-ARMS", "steckt_in", "COMP-SHAFT", [], [WK], None),
        ("COMP-SHAFT-WEDGE", "verkeilt", "COMP-ARMS", ["COMP-SHAFT"], [WK], "Zusammen mit zusätzlichen äußeren Keilen; Lage und Anzahl offen."),
        ("COMP-RIM-JOINT-WEDGE", "verkeilt", "COMP-KRUEMMLINGE", [], [K], None),
        ("COMP-SCHETTERNBRETTER", "verbindet", "COMP-KRUEMMLINGE", [], ["NARRATIVE-TH-CONSTRUCTION-20261009"], "Aus TH-20261009-04/05: je Stoß und Seite ein Schetternbrett, vier Schetternägel."),
        ("COMP-KUMPF-NAILS", "befestigt", "COMP-KUEMPFE", ["COMP-RIM-LAND"], ["NARRATIVE-TH-KUMPF-20261008-02"], "Aus CLAIM-0364."),
    ]


def neue_fragen():
    # schluessel: (frage, betrifft, blockiert, haengt_ab_von[schluessel], entscheidet, hinweis)
    return [
        ("radstadt-oeffnung", "Wie groß ist die lichte Weite der Radstadt parallel zum Ufer wirklich – 4,40 m (Aussage) oder 5,25 m (Zeichnung)? Welche Innenkanten, auf welcher Höhe?",
         ["COMP-RADSTATT", "AN-20261011-04"], ["COMP-RADSTATT", "COMP-WHEEL"], ["schaufel-ueberstand", "achshoehe"], "P-THORSTEN",
         "Drehkreis mit Flügelbrettern 4,66–4,96 m. 4,40 m genügen nur, wenn die Balken mindestens 0,77–1,14 m über oder unter der Achse liegen. Herleitung: evidence/raw/Radstadt/MASSABGLEICH.md."),
        ("schaufel-ueberstand", "Wie weit stehen die Flügelbretter radial über die Kranz-Außenkante hinaus?",
         ["COMP-PADDLES", "COMP-RIMS"], ["COMP-PADDLES"], [], "P-THORSTEN", "Bestimmt den Drehkreis."),
        ("achshoehe", "Wie hoch liegt die Wellenmitte über der Oberkante der Radstadt-Balken, und liegt die Achse mittig?",
         ["COMP-SHAFT", "COMP-RADSTATT", "COMP-BEARINGS"], ["COMP-WHEEL"], ["legacy:CLAIM-0341"], "P-THORSTEN", None),
        ("bock-identitaet", "Ist der „Bock am Rad“ (14 × 14 cm, Querbalken 1,20 m) derselbe Bauteil wie der landseitige Lagerbock der Radstadt?",
         ["COMP-TROUGH-SUPPORT", "COMP-BEARING-STANDS"], ["COMP-TROUGH-SUPPORT"], [], "P-THORSTEN",
         "Befund Auffangtrog nennt dieselben Maße für den landseitigen Lagerbock."),
        ("arm-verschraenkung", "Wie genau greifen die drei Arme einer Armzone ineinander? Das Modell-Audit verlangt bisher, dass sich kreuzende Arme kollidieren.",
         ["COMP-ARMS", "COMP-SHAFT"], ["COMP-ARMS"], ["legacy:CLAIM-0336"], "P-THORSTEN",
         "scripts/audit-candidates.mjs schlägt deshalb seit ITER-003 fehl. Testannahme erst nach dieser Antwort ändern."),
        ("rinne-teile", "Wie lang ist Rinne 2, und wie lang ist die Überlappung der beiden Rinnenteile?",
         ["COMP-RINNE", "COMP-RINNE-2", "COMP-A-BOCK"], ["COMP-CHANNEL", "COMP-A-BOCK"], [], "P-THORSTEN", None),
        ("herkunft-nutzer", "Wer hat die in den Befunden vom 11.10.2026 als „Nutzer“ bezeichneten Angaben gemacht?",
         ["AN-20261011-01", "AN-20261011-02", "AN-20261011-04", "AN-20261011-05", "AN-20261011-12"], [], [], "P-JOHANNES",
         "Ohne Person kann keine dieser Angaben bestätigt werden."),
        ("skizzen-heute", "Gelten die Skizzen von Welle (IMG_6816/6817), Schöpftrog (IMG_6828/6829) und Rinne 1 (IMG_6830) für das heutige Rad?",
         ["PHOTO-6816", "PHOTO-6817", "PHOTO-6828", "PHOTO-6829", "PHOTO-6830"], [], [], "P-THORSTEN",
         "Bestätigung ist in Befunden und evidence-authority.json vermerkt, aber ohne eindeutige Person."),
        ("holzliste", "Zu welchen Bauteilen gehören die Holzlisten-Posten Anwelle, Bänder, Nägel, Fangbaum, Laufsteg, Zwergrinne, Zwergsteg, Landrinne, Pfosten, Rüst- und Landestange und Flügel-Versatz?",
         ["HL-Anwelle", "HL-Bänder", "HL-Nägel", "HL-Fangbaum", "HL-Laufsteg"], [], [], "P-THORSTEN", None),
        ("fluegel-90", "Die Angabe „Flügelbrett 90°“ steht doppelt (CLAIM-0369, TH-20261009-06). Worauf genau beziehen sich die 90°?",
         ["CLAIM-0369", "TH-20261009-06"], ["COMP-PADDLES"], ["legacy:GAP-09"], "P-THORSTEN", None),
        ("werkzeuge", "Welche Werkzeuge werden beim Auf- und Abbau verwendet, und für welchen Schritt?",
         ["COMP-WHEEL"], ["AS-AUF-01", "AS-AUF-02", "AS-AUF-03", "AS-AUF-04", "AS-AUF-05", "AS-AUF-06"], [], "P-THORSTEN",
         "Kern der Überlieferung: alte Werkzeuge sind der Stolz des Vereins."),
    ]


UNBEKANNT_TEXT = {
    "CLAIM-0336": ("Wie sehen die Armöffnungen der Welle innen aus, und welche Arme gehören in welcher Reihenfolge zusammen?", ["CLAIM-0337", "GAP-02"]),
    "CLAIM-0338": ("Wo liegen die beiden Kranzebenen und die festen Bezugspunkte des Rades im Raum?", ["GAP-01"]),
    "CLAIM-0339": ("Wie viele Kümpfe und Flügelbretter hat das Rad, und in welcher Folge sitzen sie am Umfang?", ["CLAIM-0340", "GAP-05"]),
    "CLAIM-0341": ("Wo liegen die Lagermitten, und wie liegt der Dorn im Lager auf?", ["GAP-06"]),
    "CLAIM-0342": ("Wo steht das Wasser im Betrieb relativ zur Achse, und wie liegen Trog und Rinne dazu?", ["GAP-07"]),
    "CLAIM-0343": ("In welcher Reihenfolge wird das Rad abgebaut und aufgebaut?", ["GAP-08"]),
}


KONFLIKT_TEXT = {
    "CONFLICT-01": "Zwei Kumpfskizzen widersprechen sich: Dauben 24 oder 22 mm, Nutdurchmesser 244/264 oder 248/268. Welche gilt für den Referenz-Kumpf?",
    "CONFLICT-02": "Zwei Reihen von Reifenlängen (780/875/968 und 784/880/972). Laut Fachauskunft gibt es Maßvarianten – welche Reihe gehört zum fotografierten Referenz-Kumpf?",
    "CONFLICT-03": "Wellenskizze 370/37 gegen Holzliste 4,50 m / 50 cm (Einbau 40 cm): Beschreibt die Holzliste nur das Rohholz?",
    "CONFLICT-04": "Krümmling 14 cm breit gegen 15 cm Ringdifferenz (213 − 198) in der Skizze.",
    "CONFLICT-05": "Die Zahlen auf der Armskizze (gerade/schräg) und die drei Durchtritte je Armzone lassen sich nicht allen heutigen Armen zuordnen.",
    "CONFLICT-06": "Befestigungsbegriffe waren vermischt. Kumpfnägel sind inzwischen geklärt; welche Funktion haben die übrigen Keile und Bänder?",
    "CONFLICT-07": "Veröffentlicht sind 24 Kümpfe und 24 Flügelbretter; auf den Fotos lassen sie sich nicht vollständig zählen.",
    "CONFLICT-08": "Auf Fotos sichtbare Flächen fehlen im 3D-Scan oder sind lückenhaft. Taugt der Scan für Maße?",
    "CONFLICT-09": "Kranzdurchmesser laut Skizze 4,26 / 3,96 m, der Scan hat eine Ausdehnung von 6,03 / 7,03 / 4,50 Exporteinheiten. Wie sind Scan-Einheiten und Maßstab zu lesen?",
    "CONFLICT-10": "Die beiden Scan-Exporte (PLY und GLB) haben unterschiedliche Ausdehnung und Punktmengen. Welcher ist maßgeblich?",
    "CONFLICT-11": "Industrielle Kontaktstreifen- und Brettvorlagen waren früher als Kumpfbefestigung bzw. Welle eingeordnet. Gehören sie überhaupt zum Rad?",
    "CONFLICT-12": "Die Trogskizze nennt 250 cm Gesamtlänge und daneben 244 cm in Klammern. Welche Kanten sind jeweils gemeint?",
    "CONFLICT-13": "Flügelbretter stehen laut Fachkenner 90° zum Rad. Das Modell stellt sie formal senkrecht zur Kranzebene, Lage und Anstellung können trotzdem falsch sein.",
}


def neue_arbeitsschritte():
    A, WK, K = "Q-AUSSAGE-20261011-ARME", "Q-AUSSAGE-20261011-WELLENKEIL", "Q-AUSSAGE-20261011-KRUEMMLINGE"
    TH = "NARRATIVE-TH-CONSTRUCTION-20261009"
    KU = "NARRATIVE-TH-KUMPF-20261008-02"
    return [
        ("AS-AUF-01", "Arme in die Welle stecken und miteinander verschränken", ["COMP-ARMS", "COMP-SHAFT"], [], [A, WK]),
        ("AS-AUF-02", "Arme mit Wellenkeil und äußeren Keilen sichern", ["COMP-SHAFT-WEDGE", "COMP-ARMS"], ["AS-AUF-01"], [WK]),
        ("AS-AUF-03", "Krümmlinge mittig auf die Armenden setzen und Armsitz verkeilen", ["COMP-KRUEMMLINGE", "COMP-ARMS"], [], [TH]),
        ("AS-AUF-04", "Krümmlingstöße mit Schetternbrettern und Schetternägeln verbinden, Gegenseite verkeilen", ["COMP-SCHETTERNBRETTER", "COMP-KRUEMMLINGE"], [], [TH]),
        ("AS-AUF-05", "Stoßspalte mit Stoßkeilen schließen und den Kranz verspannen", ["COMP-RIM-JOINT-WEDGE", "COMP-KRUEMMLINGE"], ["AS-AUF-04"], [K]),
        ("AS-AUF-06", "Kümpfe mit langem und kurzem Kumpfnagel am landseitigen Kranz befestigen", ["COMP-KUEMPFE", "COMP-KUMPF-NAILS", "COMP-RIM-LAND"], [], [KU]),
        ("AS-AUF-07", "Flügelbretter mit Holzbändern über den Krümmling befestigen und hinten verkeilen", ["COMP-PADDLES", "COMP-WOOD-BANDS", "COMP-KRUEMMLINGE"], [], [TH]),
    ]


def neue_begruendungen():
    return [
        ("G-001", "Ein langer und ein kurzer Kumpfnagel, weil benachbarte Kümpfe überlappen.", ["COMP-KUMPF-NAILS", "CLAIM-0368"], ["NARRATIVE-TH-KUMPF-20261008-03"]),
        ("G-002", "Die Armöffnungen der Welle sind größer als der Armquerschnitt, damit Platz für die Verkeilung bleibt.", ["COMP-SHAFT", "AN-20261011-13"], ["Q-AUSSAGE-20261011-WELLE"]),
        ("G-003", "Der Stoßkeil drückt auf die Schetternägel und verspannt so den ganzen Kranz.", ["COMP-RIM-JOINT-WEDGE", "AN-20261011-07"], ["Q-AUSSAGE-20261011-KRUEMMLINGE"]),
        ("G-004", "Die Außenarme sind gekröpft, damit alle Armenden gemeinsam am jeweiligen Kranz liegen.", ["COMP-ARMS", "AN-20261011-12"], ["Q-AUSSAGE-20261011-ARME"]),
    ]


# --------------------------------------------------------------------------

def main():
    if os.path.exists(os.path.join(KERN, "angaben.json")) and "--neu" not in sys.argv:
        sys.exit("kern/angaben.json existiert bereits. kern/ ist jetzt handgepflegt; Neuaufbau nur mit --neu.")

    claims = lade("data/geometry.claims.json")["claims"]
    comps = lade("data/components.json")["components"]
    conflicts = lade("data/conflicts.json")["conflicts"]
    gaps = lade("data/knowledge-gaps.json")["gaps"]
    sa = lade("data/source-analyses.json")["sources"]
    zuordnung = OrderedDict()

    # Quellen
    quellen, q_alias = baue_quellen(git_dateien(), sa)
    for qid, pfad, titel in AUSSAGE_QUELLEN:
        quellen[qid] = OrderedDict([("id", qid), ("art", "aussage"), ("pfad", pfad), ("titel", titel),
                                    ("person", None), ("ordner", None), ("erschlossen", True),
                                    ("identisch_mit", []), ("alt_ids", []), ("hinweis", PERSON_OFFEN)])
    for alt, neu_id in q_alias.items():
        zuordnung[alt] = {"kern_id": neu_id, "datei": "quellen.json", "art": "quelle-alias"}

    # Bauteile
    bauteile = OrderedDict()
    for c in comps:
        if c["id"] == "COMP-RADSTADT":
            zuordnung[c["id"]] = {"kern_id": "COMP-RADSTATT", "datei": "bauteile.json", "art": "schreibvariante"}
            continue
        anzahl, hinweis = BAUTEIL_TEXTE[c["id"]]
        bauteile[c["id"]] = OrderedDict([
            ("id", c["id"]), ("name", "Rinne 1 (hinter Trog)" if c["id"] == "COMP-RINNE" else c["label"]),
            ("begriff", BEGRIFF_JE_KOMPONENTE[c["id"]]), ("art", ART_JE_KIND[c["kind"]]),
            ("teil_von", TEIL_VON.get(c["id"])), ("anzahl", anzahl),
            ("hinweis", hinweis), ("herkunft", {"datei": "data/components.json", "id": c["id"]}),
        ])
        zuordnung[c["id"]] = {"kern_id": c["id"], "datei": "bauteile.json", "art": "bauteil"}
    for bid, name, begriff, art, anzahl, hinweis in NEUE_BAUTEILE:
        bauteile[bid] = OrderedDict([("id", bid), ("name", name), ("begriff", begriff), ("art", art),
                                     ("teil_von", TEIL_VON.get(bid)), ("anzahl", anzahl), ("hinweis", hinweis),
                                     ("herkunft", {"datei": "Nachtrag 11.10.2026", "id": None})])
    for c in claims:
        s = c["subject"]
        if s.startswith("REF-") and s not in bauteile and s not in HOLZLISTE_ZIEL and s != "REF-CONTACTSTRIPS":
            bid = "HL-" + re.sub(r"[\s-]+", "-", s[4:])
            if bid not in bauteile:
                bauteile[bid] = OrderedDict([("id", bid), ("name", "Holzliste: " + s[4:]), ("begriff", "B-HOLZLISTENPOSTEN"),
                                             ("art", "listenposten"), ("teil_von", None), ("anzahl", None),
                                             ("hinweis", "Posten der allgemeinen Holzliste; Zuordnung offen (F-009)."),
                                             ("herkunft", {"datei": "data/geometry.claims.json", "id": s})])
                zuordnung[s] = {"kern_id": bid, "datei": "bauteile.json", "art": "holzlistenposten"}

    # Beziehungen
    beziehungen = OrderedDict()
    nr = 0
    for alt, (von, art, zu, ueber) in ZUSAMMENGESETZT.items():
        nr += 1
        bid = f"BZ-{nr:03d}"
        beziehungen[bid] = OrderedDict([("id", bid), ("von", von), ("art", art), ("zu", zu), ("ueber", ueber),
                                        ("gueltigkeit", "offen"), ("quellen", []), ("hinweis", None),
                                        ("herkunft", {"datei": "data/geometry.claims.json", "id": alt})])
        zuordnung[alt] = {"kern_id": bid, "datei": "beziehungen.json", "art": "zusammengesetztes-subjekt"}
    for von, art, zu, ueber, qs, hinweis in neue_beziehungen():
        nr += 1
        bid = f"BZ-{nr:03d}"
        beziehungen[bid] = OrderedDict([("id", bid), ("von", von), ("art", art), ("zu", zu), ("ueber", ueber),
                                        ("gueltigkeit", "offen"), ("quellen", qs), ("hinweis", hinweis),
                                        ("herkunft", {"datei": "Nachtrag 11.10.2026", "id": None})])

    # Ziel einer Altangabe bestimmen
    def ziel(subjekt, provenienz):
        if subjekt in ZUSAMMENGESETZT:
            return zuordnung[subjekt]["kern_id"]
        if subjekt in ZIEL_ALIAS:
            return ZIEL_ALIAS[subjekt]
        if subjekt in HOLZLISTE_ZIEL:
            return HOLZLISTE_ZIEL[subjekt]
        if subjekt in bauteile:
            return subjekt
        if subjekt in zuordnung:
            return zuordnung[subjekt]["kern_id"]
        if subjekt == "CAPTURE-01":
            return q_alias.get(provenienz[0], provenienz[0])
        if subjekt in quellen:
            return subjekt
        raise KeyError(subjekt)

    # Angaben und Fragen aus Altdaten
    angaben = OrderedDict()
    frage_quellen = {}  # Alt-ID -> Liste Alt-IDs, die in dieselbe Frage gehen
    for c in claims:
        if c["evidence_class"] in ("conflicting", "unknown"):
            continue
        prov = [p.get("source_id") for p in c["provenance"]]
        grund = grundlage(c["evidence_class"], c["scope"])
        if c["subject"] in HOLZLISTE_ZIEL or (c["subject"].startswith("REF-") and grund == "holzliste"):
            grund = "holzliste"
        hinweise = [x for x in (c.get("note"), ("Ersetzt laut Altdaten: " + c["supersedes"]) if c.get("supersedes") else None) if x]
        person = "P-THORSTEN" if grund == "muendlich" and (c["id"].startswith("TH-") or any("-TH-" in (p or "") for p in prov)) else None
        angaben[c["id"]] = OrderedDict([
            ("id", c["id"]), ("ziel", ziel(c["subject"], prov)), ("eigenschaft", slug(EIG[c["predicate"]])),
            ("wert", deutsch(c["value"])), ("einheit", EINHEIT[c["unit"]]),
            ("toleranz", {"art": "ungefaehr", "text": "ca."} if c.get("approximate") or c["predicate"].endswith("_approx") else None),
            ("grundlage", grund),
            ("quellen", [{"quelle": q_alias.get(p["source_id"], p["source_id"]), "stelle": p.get("region")} for p in c["provenance"]]),
            ("aussage_von", person), ("gueltigkeit", gueltigkeit_fuer(grund)), ("bestaetigt", None),
            ("ersetzt_durch", None), ("begruendung", None), ("hinweis", " ".join(hinweise) or None),
            ("herkunft", {"datei": "data/geometry.claims.json", "id": c["id"], "klasse": c["evidence_class"],
                          "bereich": c["scope"], "sicherheit": c["confidence"], "eigenschaft": c["predicate"],
                          **({"wert": c["value"]} if deutsch(c["value"]) != c["value"] else {})}),
        ])
        zuordnung[c["id"]] = {"kern_id": c["id"], "datei": "angaben.json", "art": "angabe"}
    for a in nachtraege():
        a["eigenschaft"] = slug(EIG[a["eigenschaft"]])
        angaben[a["id"]] = a
    angaben["CLAIM-0368"]["begruendung"] = "G-001"

    # Zweitablagen in Beitragsdateien auf Registereinträge abbilden
    for alt, neu_id in {
        "EXPERT-KUMPF-20261008-STAVE-COUNT": "CLAIM-0356", "EXPERT-KUMPF-20261008-BASE-COUNT": "CLAIM-0357",
        "EXPERT-KUMPF-20261008-BASE-GROOVE": "CLAIM-0358", "EXPERT-KUMPF-20261008-HOOP-COUNT": "CLAIM-0359",
        "EXPERT-KUMPF-20261008-HOOP-VARIANTS": "CLAIM-0360", "EXPERT-KUMPF-20261008-REFERENCE": "CLAIM-0361",
        "EXPERT-KUMPF-20261008-DRILLED-STAVES": "CLAIM-0362", "EXPERT-KUMPF-20261008-HOLES-PER-DRILLED-STAVE": "CLAIM-0363",
        "EXPERT-KUMPF-20261008-NAIL-ATTACHMENT": "CLAIM-0364", "EXPERT-KUMPF-20261008-NAIL-COUNT": "CLAIM-0365",
        "EXPERT-KUMPF-20261008-NAIL-LENGTH-PAIR": "CLAIM-0366", "EXPERT-KUMPF-20261008-VESSEL-OVERLAP": "CLAIM-0367",
        "EXPERT-KUMPF-20261008-NAIL-LENGTH-REASON": "CLAIM-0368", "EXPERT-PADDLE-20261008-ANGLE": "CLAIM-0369",
    }.items():
        zuordnung[alt] = {"kern_id": neu_id, "datei": "angaben.json", "art": "zweitablage"}

    # Fragen
    fragen = OrderedDict()
    schluessel_zu_id = {}

    def neue_frage(schluessel, text, betrifft, blockiert, abh, entscheidet, hinweis, herkunft):
        fid = f"F-{len(fragen) + 1:03d}"
        schluessel_zu_id[schluessel] = fid
        fragen[fid] = OrderedDict([("id", fid), ("frage", text), ("betrifft", betrifft), ("blockiert", blockiert),
                                   ("haengt_ab_von", abh), ("entscheidet", entscheidet), ("status", "offen"),
                                   ("antwort", []), ("hinweis", hinweis), ("herkunft", herkunft)])
        for alt in herkunft:
            zuordnung[alt] = {"kern_id": fid, "datei": "fragen.json", "art": "frage"}
        return fid

    for f in neue_fragen():
        neue_frage(f[0], f[1], f[2], f[3], f[4], f[5], f[6], [])

    claim_by_id = {c["id"]: c for c in claims}
    gap_by_id = {g["id"]: g for g in gaps}
    verwendet = set()
    for cid, (text, weitere) in UNBEKANNT_TEXT.items():
        herkunft = [cid] + weitere
        betrifft = sorted({ziel(claim_by_id[x]["subject"], []) for x in herkunft if x in claim_by_id})
        hinweis = None
        if cid == "CLAIM-0338":
            hinweis = "Teilantwort: lichter Kranzabstand 1,80 m (TH-20261009-25)."
        blockiert = [a[0] for a in neue_arbeitsschritte()] if cid == "CLAIM-0343" else []
        neue_frage("legacy:" + cid, text, betrifft, blockiert, [], "P-THORSTEN", hinweis, herkunft)
        for x in weitere:
            schluessel_zu_id["legacy:" + x] = schluessel_zu_id["legacy:" + cid]
        verwendet.update(herkunft)
    for k in conflicts:
        herkunft = [k["id"]] + ([k["conflict_claim"]] if k.get("conflict_claim") else [])
        betrifft = sorted({ziel(s, k.get("sources") or ["?"]) for s in k["subjects"]})
        hinweis = None
        if k["id"] == "CONFLICT-12":
            hinweis = ("Mögliche Lesart (ungeprüft): 180 cm innere Bodenlänge + 2 × 30 cm Anstieg bei 45° "
                       "+ 2 × 3 cm × √2 schräge Brettstärke ≈ 248,5 cm ≈ 250 cm außen oben.")
        if k["id"] == "CONFLICT-04":
            hinweis = ("Vermutlich kein Widerspruch: 14 cm ist die axiale Breite (entlang der Welle), 15 cm die "
                       "radiale Kranzhöhe (213 − 198). Siehe evidence/raw/Radstadt/MASSABGLEICH.md; Bestätigung offen.")
        text = KONFLIKT_TEXT[k["id"]]
        neue_frage("legacy:" + k["id"], text, betrifft + [x for x in k["claim_ids"] if x in angaben][:12], [], [],
                   "P-THORSTEN", hinweis, herkunft)
        verwendet.update(herkunft)
    for g in gaps:
        if g["id"] in verwendet:
            continue
        text = f"Aufnahmelücke: {g['subject']}"
        hinweis = ("Für die Zeit vor dem Abbau formuliert; das Rad wurde am 10.10.2026 abgebaut. "
                   "Prüfen, ob die Aufnahme vorliegt, sonst beim Frühjahrsaufbau nachholen. "
                   f"Ursprünglich: {g['capture']}")
        neue_frage("legacy:" + g["id"], text, ["COMP-WHEEL"], [], [], "P-JOHANNES", hinweis, [g["id"]])
        verwendet.add(g["id"])
    for c in claims:
        if c["evidence_class"] in ("conflicting", "unknown") and c["id"] not in verwendet:
            raise SystemExit(f"Nicht zugeordnet: {c['id']}")

    for f in fragen.values():
        f["haengt_ab_von"] = [schluessel_zu_id[s] for s in f["haengt_ab_von"]]

    # Arbeitsschritte und Begründungen
    arbeitsschritte = OrderedDict()
    for aid, name, teile, nach, qs in neue_arbeitsschritte():
        arbeitsschritte[aid] = OrderedDict([("id", aid), ("phase", "aufbau"), ("name", name), ("bauteile", teile),
                                            ("werkzeuge", []), ("nach", nach), ("personen", None),
                                            ("grundlage", "muendlich"), ("quellen", qs), ("gueltigkeit", "offen"),
                                            ("hinweis", "Reihenfolge nur dort gesetzt, wo sie ausdrücklich genannt wurde; siehe Frage zur Auf-/Abbaureihenfolge.")])
    begruendungen = OrderedDict()
    for gid, text, betrifft, qs in neue_begruendungen():
        begruendungen[gid] = OrderedDict([("id", gid), ("text", text), ("betrifft", betrifft), ("quellen", qs),
                                          ("gueltigkeit", "offen")])

    # Erschlossen: von Angaben referenziert
    for a in angaben.values():
        for q in a["quellen"]:
            if q["quelle"] in quellen:
                quellen[q["quelle"]]["erschlossen"] = True

    with open(os.path.join(KERN, "begriffe.json"), encoding="utf-8") as f:
        begriffe = json.load(f, object_pairs_hook=OrderedDict)
    eig_namen = OrderedDict()
    for alt, name in EIG.items():
        eig_namen.setdefault(slug(name), name)
    benutzt = {a["eigenschaft"] for a in angaben.values()}
    begriffe["begriffe"] = [b for b in begriffe["begriffe"] if b["kategorie"] != "eigenschaft"] + [
        OrderedDict([("id", k), ("name", n), ("kategorie", "eigenschaft")]) for k, n in sorted(eig_namen.items()) if k in benutzt]
    with open(os.path.join(KERN, "begriffe.json"), "w", encoding="utf-8") as f:
        json.dump(begriffe, f, ensure_ascii=False, indent=2)
        f.write("\n")

    kopf = lambda name, hinweis: OrderedDict([("schema", f"ks-kern-{name}/v1"), ("stand", STAND), ("hinweis", hinweis)])
    hand = "Handgepflegt seit der Migration vom 11.10.2026 (scripts/kern/migriere_v1.py)."
    schreibe("kern/bauteile.json", {**kopf("bauteile", hand), "bauteile": list(bauteile.values())})
    schreibe("kern/beziehungen.json", {**kopf("beziehungen", hand), "beziehungen": list(beziehungen.values())})
    schreibe("kern/angaben.json", {**kopf("angaben", hand), "angaben": list(angaben.values())})
    schreibe("kern/quellen.json", {**kopf("quellen", hand), "quellen": list(quellen.values())})
    schreibe("kern/fragen.json", {**kopf("fragen", hand), "fragen": list(fragen.values())})
    schreibe("kern/arbeitsschritte.json", {**kopf("arbeitsschritte", hand), "arbeitsschritte": list(arbeitsschritte.values())})
    schreibe("kern/begruendungen.json", {**kopf("begruendungen", hand), "begruendungen": list(begruendungen.values())})
    schreibe("kern/migration/v1-zuordnung.json", {
        "schema": "ks-kern-zuordnung/v1", "stand": STAND,
        "hinweis": "Alt-ID → Kern-ID. Altdateien bleiben unverändert; Rückbau: kern/ entfernen.",
        "zuordnung": zuordnung})
    print(f"Bauteile {len(bauteile)}, Beziehungen {len(beziehungen)}, Angaben {len(angaben)}, "
          f"Quellen {len(quellen)}, Fragen {len(fragen)}, Arbeitsschritte {len(arbeitsschritte)}, "
          f"Begründungen {len(begruendungen)}, Zuordnungen {len(zuordnung)}")


if __name__ == "__main__":
    main()
