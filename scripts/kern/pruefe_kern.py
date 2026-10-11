#!/usr/bin/env python3
"""Prüft das Kernmodell unter kern/ auf Vollständigkeit und Widerspruchsfreiheit.

Ohne externe Abhängigkeiten. Exit-Code 1 bei Fehlern.

Aufruf:
  python scripts/kern/pruefe_kern.py            # Prüfung + Kurzbericht
  python scripts/kern/pruefe_kern.py --begriff Schetter   # Begriff nachschlagen
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

GRUNDLAGEN = {"messung", "muendlich", "skizze", "foto", "scan", "holzliste", "fremdvorlage",
              "kontext", "ableitung", "annahme"}
GUELTIGKEIT = {"offen", "bestaetigt", "historisch", "ueberholt", "verworfen"}
EINHEITEN = {None, "m", "cm", "mm", "grad", "anzahl", "exporteinheit"}
BAUTEIL_ARTEN = {"anlage", "baugruppe", "teil", "zone", "werkzeug", "vorlage", "listenposten"}
QUELLEN_ARTEN = {"foto", "skizze", "scan", "video", "aussage", "kontext", "ableitung", "dokument"}
FRAGE_STATUS = {"offen", "beantwortet", "verworfen"}
PHASEN = {"aufbau", "abbau", "pflege"}
TOLERANZ_ARTEN = {"bereich", "plusminus", "ungefaehr", "vereinfachung"}
KATEGORIEN = {"kernbegriff", "bauteil", "werkzeug", "ort", "beziehungsart"}
DATUM = re.compile(r"^\d{4}-\d{2}-\d{2}$")

DATEIEN = {
    "begriffe": "begriffe", "personen": "personen", "bauteile": "bauteile",
    "beziehungen": "beziehungen", "angaben": "angaben", "quellen": "quellen",
    "fragen": "fragen", "arbeitsschritte": "arbeitsschritte", "begruendungen": "begruendungen",
}


def lade_kern(kern_dir):
    daten = {}
    for name, schluessel in DATEIEN.items():
        with open(os.path.join(kern_dir, name + ".json"), encoding="utf-8") as f:
            inhalt = json.load(f)
        if inhalt.get("schema") != f"ks-kern-{name}/v1":
            raise ValueError(f"{name}.json: schema muss ks-kern-{name}/v1 sein")
        daten[name] = inhalt[schluessel]
    return daten


def zyklen(kanten):
    """Gibt einen Knoten zurück, der in einem Zyklus liegt, sonst None."""
    farbe = {}

    def besuche(k):
        farbe[k] = 1
        for n in kanten.get(k, []):
            if farbe.get(n) == 1:
                return n
            if n not in farbe:
                r = besuche(n)
                if r:
                    return r
        farbe[k] = 2
        return None

    for k in list(kanten):
        if k not in farbe:
            r = besuche(k)
            if r:
                return r
    return None


def pruefe(kern_dir, root=ROOT, altdaten=True):
    fehler, warnungen = [], []
    F = fehler.append
    W = warnungen.append
    d = lade_kern(kern_dir)

    # Eindeutige IDs über alle Dateien
    alle = {}
    for name, eintraege in d.items():
        for e in eintraege:
            i = e.get("id")
            if not i:
                F(f"{name}: Eintrag ohne id")
                continue
            if i in alle:
                F(f"ID doppelt: {i} in {alle[i]} und {name}")
            alle[i] = name
    ids = lambda name: {e["id"] for e in d[name]}
    begriffe = {b["id"]: b for b in d["begriffe"]}
    personen = {p["id"]: p for p in d["personen"]}
    bauteile = {b["id"]: b for b in d["bauteile"]}
    beziehungen = {b["id"]: b for b in d["beziehungen"]}
    angaben = {a["id"]: a for a in d["angaben"]}
    quellen = {q["id"]: q for q in d["quellen"]}
    fragen = {f["id"]: f for f in d["fragen"]}
    schritte = {s["id"]: s for s in d["arbeitsschritte"]}
    begruendungen = {g["id"]: g for g in d["begruendungen"]}
    referenzierbar = set(alle)

    # Glossar
    namen = {}
    for b in begriffe.values():
        if b.get("kategorie") not in KATEGORIEN:
            F(f"{b['id']}: unbekannte Kategorie {b.get('kategorie')}")
        if not b.get("definition"):
            F(f"{b['id']}: Definition fehlt")
        for wort in [b["name"]] + b.get("aliase", []):
            key = wort.casefold()
            if key in namen and namen[key] != b["id"]:
                F(f"Glossar: „{wort}“ gehört zu {namen[key]} und {b['id']}")
            namen[key] = b["id"]
        for n in b.get("nicht_verwechseln_mit", []):
            if n not in begriffe:
                F(f"{b['id']}: nicht_verwechseln_mit verweist auf unbekannten Begriff {n}")
    beziehungsarten = {k for k, b in begriffe.items() if b["kategorie"] == "beziehungsart"}
    werkzeugbegriffe = {k for k, b in begriffe.items() if b["kategorie"] == "werkzeug"}

    def person_ok(p, wo):
        if p is not None and p not in personen:
            F(f"{wo}: unbekannte Person {p}")

    def bestaetigung(e, wo):
        g, b = e.get("gueltigkeit"), e.get("bestaetigt")
        if g not in GUELTIGKEIT:
            F(f"{wo}: Gültigkeit {g} unbekannt")
        if g == "bestaetigt":
            if not isinstance(b, dict) or b.get("von") not in personen or not DATUM.match(str(b.get("am", ""))):
                F(f"{wo}: „bestaetigt“ braucht bestaetigt.von (Person) und bestaetigt.am (JJJJ-MM-TT)")
            elif not personen[b["von"]].get("darf_bestaetigen"):
                F(f"{wo}: {b['von']} darf nicht bestätigen")
        elif b:
            F(f"{wo}: bestaetigt gesetzt, aber Gültigkeit ist {g}")

    def quellen_ok(liste, wo):
        for q in liste:
            qid = q["quelle"] if isinstance(q, dict) else q
            if qid not in quellen:
                F(f"{wo}: unbekannte Quelle {qid}")

    # Personen
    for p in personen.values():
        if not p.get("name"):
            F(f"{p['id']}: Name fehlt")

    # Bauteile
    for b in bauteile.values():
        if b["art"] not in BAUTEIL_ARTEN:
            F(f"{b['id']}: Art {b['art']} unbekannt")
        if b.get("begriff") not in begriffe:
            F(f"{b['id']}: Begriff {b.get('begriff')} fehlt im Glossar")
        elif begriffe[b["begriff"]]["kategorie"] not in ("bauteil", "werkzeug"):
            F(f"{b['id']}: Begriff {b['begriff']} ist kein Bauteil- oder Werkzeugbegriff")
        if b.get("teil_von") and b["teil_von"] not in bauteile:
            F(f"{b['id']}: teil_von {b['teil_von']} unbekannt")
        if b["art"] in ("teil", "baugruppe", "zone") and not b.get("teil_von"):
            F(f"{b['id']}: {b['art']} ohne teil_von hängt nicht im Inventarbaum")
    z = zyklen({k: [b["teil_von"]] for k, b in bauteile.items() if b.get("teil_von")})
    if z:
        F(f"Bauteile: teil_von bildet einen Kreis bei {z}")

    # Beziehungen
    for r in beziehungen.values():
        for feld in ("von", "zu"):
            if r[feld] not in bauteile:
                F(f"{r['id']}: {feld} {r[feld]} ist kein Bauteil")
        for u in r.get("ueber", []):
            if u not in bauteile:
                F(f"{r['id']}: ueber {u} ist kein Bauteil")
        if r["art"] not in beziehungsarten:
            F(f"{r['id']}: Beziehungsart {r['art']} fehlt im Glossar")
        if r.get("gueltigkeit") not in GUELTIGKEIT:
            F(f"{r['id']}: Gültigkeit {r.get('gueltigkeit')} unbekannt")
        quellen_ok(r.get("quellen", []), r["id"])
        if r["art"] == "zusammenhang":
            W(f"{r['id']}: Beziehungsart noch unbestimmt")

    # Angaben
    for a in angaben.values():
        wo = a["id"]
        if a["ziel"] not in bauteile and a["ziel"] not in beziehungen and a["ziel"] not in quellen:
            F(f"{wo}: Ziel {a['ziel']} ist weder Bauteil, Beziehung noch Quelle")
        if a["grundlage"] not in GRUNDLAGEN:
            F(f"{wo}: Grundlage {a['grundlage']} unbekannt")
        if a.get("einheit") not in EINHEITEN:
            F(f"{wo}: Einheit {a.get('einheit')} unbekannt")
        t = a.get("toleranz")
        if t is not None:
            if t.get("art") not in TOLERANZ_ARTEN:
                F(f"{wo}: Toleranzart {t.get('art')} unbekannt")
            if t.get("art") == "bereich" and not (isinstance(t.get("von"), (int, float)) and isinstance(t.get("bis"), (int, float)) and t["von"] <= t["bis"]):
                F(f"{wo}: Toleranzbereich braucht von ≤ bis")
        if not a.get("quellen"):
            F(f"{wo}: keine Quelle")
        quellen_ok(a.get("quellen", []), wo)
        person_ok(a.get("aussage_von"), wo)
        bestaetigung(a, wo)
        if a["gueltigkeit"] == "bestaetigt" and a["grundlage"] == "muendlich" and not a.get("aussage_von"):
            F(f"{wo}: mündliche Angabe kann ohne aussage_von nicht bestätigt werden")
        if a["gueltigkeit"] == "ueberholt":
            if a.get("ersetzt_durch") not in angaben:
                F(f"{wo}: „ueberholt“ braucht ersetzt_durch mit existierender Angabe")
        elif a.get("ersetzt_durch"):
            F(f"{wo}: ersetzt_durch gesetzt, aber Gültigkeit ist {a['gueltigkeit']}")
        if a.get("begruendung") and a["begruendung"] not in begruendungen:
            F(f"{wo}: Begründung {a['begruendung']} unbekannt")
    z = zyklen({k: [a["ersetzt_durch"]] for k, a in angaben.items() if a.get("ersetzt_durch")})
    if z:
        F(f"Angaben: ersetzt_durch bildet einen Kreis bei {z}")

    # Quellen
    for q in quellen.values():
        if q["art"] not in QUELLEN_ARTEN:
            F(f"{q['id']}: Art {q['art']} unbekannt")
        if q.get("pfad") and not os.path.exists(os.path.join(root, q["pfad"])):
            F(f"{q['id']}: Pfad {q['pfad']} existiert nicht")
        person_ok(q.get("person"), q["id"])
        for x in q.get("identisch_mit", []):
            if x not in quellen:
                F(f"{q['id']}: identisch_mit {x} unbekannt")

    # Fragen
    for f in fragen.values():
        wo = f["id"]
        if f["status"] not in FRAGE_STATUS:
            F(f"{wo}: Status {f['status']} unbekannt")
        for feld in ("betrifft", "blockiert"):
            for x in f.get(feld, []):
                if x not in referenzierbar:
                    F(f"{wo}: {feld} {x} unbekannt")
        for x in f.get("haengt_ab_von", []):
            if x not in fragen:
                F(f"{wo}: haengt_ab_von {x} ist keine Frage")
        person_ok(f.get("entscheidet"), wo)
        if f["status"] == "beantwortet" and not f.get("antwort"):
            F(f"{wo}: beantwortet, aber keine Antwort-Angabe")
        for x in f.get("antwort", []):
            if x not in angaben:
                F(f"{wo}: Antwort {x} ist keine Angabe")
    z = zyklen({k: f.get("haengt_ab_von", []) for k, f in fragen.items()})
    if z:
        F(f"Fragen: haengt_ab_von bildet einen Kreis bei {z}")

    # Arbeitsschritte
    for s in schritte.values():
        wo = s["id"]
        if s["phase"] not in PHASEN:
            F(f"{wo}: Phase {s['phase']} unbekannt")
        for x in s["bauteile"]:
            if x not in bauteile:
                F(f"{wo}: Bauteil {x} unbekannt")
        for x in s.get("werkzeuge", []):
            if x not in werkzeugbegriffe and not (x in bauteile and bauteile[x]["art"] == "werkzeug"):
                F(f"{wo}: Werkzeug {x} unbekannt")
        for x in s.get("nach", []):
            if x not in schritte:
                F(f"{wo}: nach {x} ist kein Arbeitsschritt")
        if s.get("grundlage") not in GRUNDLAGEN:
            F(f"{wo}: Grundlage {s.get('grundlage')} unbekannt")
        if s.get("gueltigkeit") not in GUELTIGKEIT:
            F(f"{wo}: Gültigkeit {s.get('gueltigkeit')} unbekannt")
        quellen_ok(s.get("quellen", []), wo)
    z = zyklen({k: s.get("nach", []) for k, s in schritte.items()})
    if z:
        F(f"Arbeitsschritte: nach bildet einen Kreis bei {z}")

    # Begründungen
    for g in begruendungen.values():
        for x in g["betrifft"]:
            if x not in referenzierbar:
                F(f"{g['id']}: betrifft {x} unbekannt")
        quellen_ok(g.get("quellen", []), g["id"])

    # Altdaten vollständig abgebildet
    if altdaten:
        with open(os.path.join(kern_dir, "migration", "v1-zuordnung.json"), encoding="utf-8") as f:
            zuordnung = json.load(f)["zuordnung"]

        def alt_ids(rel, schluessel, feld="id"):
            with open(os.path.join(root, rel), encoding="utf-8") as f:
                return [e[feld] for e in json.load(f)[schluessel]]

        pflicht = (alt_ids("data/geometry.claims.json", "claims") + alt_ids("data/components.json", "components")
                   + alt_ids("data/conflicts.json", "conflicts") + alt_ids("data/knowledge-gaps.json", "gaps"))
        for alt in pflicht:
            if alt not in zuordnung:
                F(f"Altdaten: {alt} ist im Kern nicht abgebildet")
            elif zuordnung[alt]["kern_id"] not in referenzierbar:
                F(f"Altdaten: {alt} → {zuordnung[alt]['kern_id']} existiert nicht mehr")

    statistik = {
        "bauteile": len(bauteile), "beziehungen": len(beziehungen), "angaben": len(angaben),
        "quellen": len(quellen), "fragen_offen": sum(f["status"] == "offen" for f in fragen.values()),
        "arbeitsschritte": len(schritte), "begruendungen": len(begruendungen),
        "gueltigkeit": Counter(a["gueltigkeit"] for a in angaben.values()),
        "grundlage": Counter(a["grundlage"] for a in angaben.values()),
        "quellen_unerschlossen": sum(not q["erschlossen"] for q in quellen.values()),
    }
    return fehler, warnungen, statistik


def begriff_nachschlagen(wort, kern_dir):
    d = lade_kern(kern_dir)
    w = wort.casefold()
    treffer = [b for b in d["begriffe"] if w in b["name"].casefold() or any(w in a.casefold() for a in b.get("aliase", []))]
    for b in treffer:
        print(f"{b['id']}  {b['name']}  [{b['kategorie']}]")
        print(f"  {b['definition']}")
        if b.get("aliase"):
            print(f"  auch: {', '.join(b['aliase'])}")
        if b.get("nicht_verwechseln_mit"):
            print(f"  nicht verwechseln mit: {', '.join(b['nicht_verwechseln_mit'])}")
        teile = [x["id"] for x in d["bauteile"] if x["begriff"] == b["id"]]
        if teile:
            print(f"  Bauteile: {', '.join(teile)}")
    if not treffer:
        print(f"Kein Begriff zu „{wort}“. Neue Begriffe in kern/begriffe.json eintragen.")
        return 1
    return 0


def main():
    kern_dir = os.path.join(ROOT, "kern")
    if "--begriff" in sys.argv:
        sys.exit(begriff_nachschlagen(sys.argv[sys.argv.index("--begriff") + 1], kern_dir))
    fehler, warnungen, s = pruefe(kern_dir)
    for w in warnungen:
        print("Hinweis:", w)
    for f in fehler:
        print("FEHLER:", f)
    print(f"Kern: {s['bauteile']} Bauteile, {s['beziehungen']} Beziehungen, {s['angaben']} Angaben, "
          f"{s['quellen']} Quellen ({s['quellen_unerschlossen']} unerschlossen), {s['fragen_offen']} offene Fragen, "
          f"{s['arbeitsschritte']} Arbeitsschritte, {s['begruendungen']} Begründungen")
    print("Gültigkeit:", ", ".join(f"{k} {v}" for k, v in s["gueltigkeit"].most_common()))
    print("Grundlage:", ", ".join(f"{k} {v}" for k, v in s["grundlage"].most_common()))
    if fehler:
        print(f"{len(fehler)} Fehler.")
        sys.exit(1)
    print("Kern widerspruchsfrei.")


if __name__ == "__main__":
    main()
