#!/usr/bin/env python3
"""Baut das Paket für schaeferrad.jdistlr.de: Cockpit (mit api.php als Speicher) plus PHP-Schnittstelle.

Aufruf: python scripts/kern/baue_webspace.py [--ziel <ordner>]      (Standard: dist-webspace/)

- Das Cockpit wird mit --api api.php gebaut, liegt also neben der Schnittstelle (gleiche Herkunft).
- konfig.php entsteht nur, wenn KS_EXPORT_SCHLUESSEL gesetzt ist (in der Veröffentlichung aus dem Secret).
- impressum.html entsteht nur, wenn KS_IMPRESSUM (HTML, aus dem Secret) gesetzt ist; vorerst keines.
  Das Impressum steht nie im öffentlichen Repository.
- Der Ordner daten/ enthält nur die .htaccess; Antworten auf dem Server werden nie überschrieben.
"""
import json
import os
import shutil
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def main():
    ziel = os.path.abspath(sys.argv[sys.argv.index("--ziel") + 1]) if "--ziel" in sys.argv else os.path.join(ROOT, "dist-webspace")
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "kern", "baue_cockpit.py"), "--api", "api.php"], check=True)
    if os.path.exists(ziel):
        shutil.rmtree(ziel)
    shutil.copytree(os.path.join(ROOT, "cockpit"), ziel, ignore=shutil.ignore_patterns("artefakt.html", "bilder-paket.json"))
    ws = os.path.join(ROOT, "webspace")
    for name in ("api.php", ".htaccess", "datenschutz.html"):
        shutil.copy(os.path.join(ws, name), os.path.join(ziel, name))
    os.makedirs(os.path.join(ziel, "daten"), exist_ok=True)
    shutil.copy(os.path.join(ws, "daten", ".htaccess"), os.path.join(ziel, "daten", ".htaccess"))
    # Impressum nur, wenn KS_IMPRESSUM gesetzt ist (Entscheidung Johannes 12.10.2026: vorerst keines).
    if os.environ.get("KS_IMPRESSUM"):
        with open(os.path.join(ws, "impressum.vorlage.html"), encoding="utf-8") as f:
            impressum = f.read().replace("<!--IMPRESSUM-->", os.environ["KS_IMPRESSUM"])
        with open(os.path.join(ziel, "impressum.html"), "w", encoding="utf-8") as f:
            f.write(impressum)
    schluessel = os.environ.get("KS_EXPORT_SCHLUESSEL", "")
    if schluessel:
        with open(os.path.join(ziel, "konfig.php"), "w", encoding="utf-8") as f:
            f.write("<?php return json_decode(<<<'KONFIG'\n" + json.dumps({"export_schluessel": schluessel}) + "\nKONFIG, true);\n")
    # Das Cockpit verlinkt Impressum und Datenschutz im Fuß.
    print(f"Webspace-Paket: {os.path.relpath(ziel, ROOT)}")
    # Danach Cockpit wieder ohne API bauen, damit cockpit/ für GitHub Pages unverändert bleibt.
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "kern", "baue_cockpit.py")], check=True, capture_output=True)


if __name__ == "__main__":
    main()
