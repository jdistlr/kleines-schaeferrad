#!/usr/bin/env python3
"""Sammelt Antworten aus dem Cockpit ein (GitHub-Issues mit Antwort-Block) und sichert sie.

Quellen: GitHub-Issues und, falls vorhanden, evidence/antworten/webspace.json (Webspace).
Eine Antwort ist ein Issue, dessen Text einen Block <!-- antwort … --> enthält (Felder ziel, typ, wert).
Das Label „antwort“ setzt GitHub nur bei Mitarbeitern; erkannt wird deshalb der Block.
Kommentare unter dem Issue gehören zur Antwort, angehängte Bilder werden mitgeführt.

Aufruf (braucht die gh-CLI):
  python scripts/kern/antworten_einsammeln.py             # Übersicht je Frage/Bauteil
  python scripts/kern/antworten_einsammeln.py --offen     # nur noch nicht übernommene
  python scripts/kern/antworten_einsammeln.py --sichern   # Abzug nach evidence/antworten/antworten.json

Der Abzug ist eine Sicherung unabhängig von GitHub-Issues und die Datenquelle des Cockpits
(es lädt live nur, was danach dazukam). Übernehmen in den Kern bleibt Handarbeit nach AGENTS.md;
übernommene Antworten bekommen das Label „im-kern“.
"""
import json
import os
import re
import subprocess
import sys

REPO = "jdistlr/kleines-schaeferrad"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ZIEL = os.path.join(ROOT, "evidence", "antworten", "antworten.json")
BILD = re.compile(r'!\[[^\]]*\]\((https?://[^)\s]+)\)|<img[^>]+src="(https?://[^"]+)"')


def gh(pfad):
    """Alle Seiten einer Listen-Abfrage, ein Objekt je Zeile."""
    raus = subprocess.check_output(["gh", "api", "--paginate", pfad, "--jq", ".[] | tojson"], text=True)
    return [json.loads(z) for z in raus.splitlines() if z.strip()]


def bilder(text):
    return [a or b for a, b in BILD.findall(text or "")]


def ohne_bilder(text):
    return BILD.sub("", text or "").strip()


def lesen():
    antworten = []
    for i in gh(f"repos/{REPO}/issues?state=all&per_page=100"):
        if "pull_request" in i:
            continue
        body = i.get("body") or ""
        m = re.search(r"<!--\s*antwort([\s\S]*?)-->", body)
        if not m:
            continue
        f = dict(re.findall(r"^\s*(\w+):\s*(.*)$", m.group(1), re.M))
        text = re.sub(r"<!--[\s\S]*?-->", "", body).replace("_Aus dem Cockpit. Fotos können hier per Ziehen oder Einfügen angehängt werden._", "").strip()
        kommentare = []
        if i.get("comments"):
            for c in gh(f"repos/{REPO}/issues/{i['number']}/comments?per_page=100"):
                kommentare.append({"name": c["user"]["login"], "am": c["created_at"], "text": ohne_bilder(c.get("body")), "bilder": bilder(c.get("body"))})
        antworten.append({
            "nr": i["number"], "link": i["html_url"], "ziel": f.get("ziel", "").strip(), "typ": f.get("typ", "").strip(),
            "wert": f.get("wert", "").strip(), "text": ohne_bilder(text), "bilder": bilder(text),
            "name": i["user"]["login"], "am": i["created_at"], "geaendert": i["updated_at"],
            "uebernommen": any(l["name"] == "im-kern" for l in i["labels"]), "geschlossen": i["state"] == "closed",
            "kommentare": kommentare,
        })
    return sorted(antworten, key=lambda a: a["am"])


def webspace():
    """Antworten vom Webspace (evidence/antworten/webspace.json, vom Workflow „Antworten zurückholen“)."""
    pfad = os.path.join(ROOT, "evidence", "antworten", "webspace.json")
    if not os.path.exists(pfad):
        return []
    liste = json.load(open(pfad, encoding="utf-8")).get("antworten", [])
    for a in liste:
        a.setdefault("kommentare", [])
        a["nr"] = a.get("id")
        a["bilder"] = [f.get("url", f["id"]) for f in a.get("dateien", []) if f.get("art") == "bild"]
    return liste


def main():
    antworten = lesen()
    if "--sichern" not in sys.argv:
        antworten += webspace()
    if "--sichern" in sys.argv:
        os.makedirs(os.path.dirname(ZIEL), exist_ok=True)
        with open(ZIEL, "w", encoding="utf-8") as f:
            json.dump({"hinweis": "Abzug der Cockpit-Antworten (GitHub-Issues). Erzeugt von scripts/kern/antworten_einsammeln.py --sichern. Nicht von Hand bearbeiten.",
                       "antworten": antworten}, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"{len(antworten)} Antworten gesichert: {os.path.relpath(ZIEL, ROOT)}")
        return
    gruppen = {}
    for a in antworten:
        if "--offen" in sys.argv and a["uebernommen"]:
            continue
        gruppen.setdefault(a["ziel"] or "?", []).append(a)
    for ziel, liste in sorted(gruppen.items()):
        print(f"\n## {ziel}")
        for a in liste:
            print(f"- {'#' if isinstance(a['nr'], int) else ''}{a['nr']} {a['name'] or 'ohne Namen'} {a['am'][:10]} [{a['typ']}]{' ' + a['wert'] if a['wert'] else ''}{' (im Kern)' if a['uebernommen'] else ''}"
                  f"{' · ' + str(len(a['bilder'])) + ' Bild(er)' if a['bilder'] else ''}\n  {a['text'][:400]}")
            for k in a["kommentare"]:
                print(f"    ↳ {k['name']} {k['am'][:10]}: {k['text'][:300]}")
    if not gruppen:
        print("Keine Antworten.")


if __name__ == "__main__":
    main()
