#!/usr/bin/env python3
"""Sammelt Antworten aus dem Cockpit ein (GitHub-Issues mit dem Antwort-Block; das Label „antwort“ setzt GitHub nur bei Mitarbeitern) und listet sie je Frage/Bauteil.

Nur lesend. Übernehmen in den Kern bleibt Handarbeit nach AGENTS.md („Neues Fachwissen eintragen“);
übernommene Antworten bekommen danach das Label „im-kern“.

Aufruf: python scripts/kern/antworten_einsammeln.py [--offen]   (braucht die gh-CLI)
"""
import json
import re
import subprocess
import sys

REPO = "jdistlr/kleines-schaeferrad"


def main():
    roh = subprocess.check_output(["gh", "api", f"repos/{REPO}/issues?state=all&per_page=100"], text=True)
    gruppen = {}
    for i in json.loads(roh):
        m = re.search(r"<!--\s*antwort([\s\S]*?)-->", i.get("body") or "")
        if not m:
            continue
        f = dict(re.findall(r"^\s*(\w+):\s*(.*)$", m.group(1), re.M))
        im_kern = any(l["name"] == "im-kern" for l in i["labels"])
        if "--offen" in sys.argv and im_kern:
            continue
        text = re.sub(r"<!--[\s\S]*?-->", "", i.get("body") or "").strip()
        gruppen.setdefault(f.get("ziel", "?"), []).append((i["number"], i["user"]["login"], i["created_at"][:10], f.get("typ", ""), f.get("wert", ""), text, im_kern))
    for ziel, liste in sorted(gruppen.items()):
        print(f"\n## {ziel}")
        for nr, wer, am, typ, wert, text, im_kern in liste:
            print(f"- #{nr} {wer} {am} [{typ}]{' ' + wert if wert else ''}{' (im Kern)' if im_kern else ''}\n  {text[:400]}")
    if not gruppen:
        print("Keine Antworten.")


if __name__ == "__main__":
    main()
