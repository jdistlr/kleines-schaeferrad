#!/usr/bin/env python3
"""Baut das Paket für schaeferrad.jdistlr.de: Cockpit (mit api.php als Speicher) plus PHP-Schnittstelle.

Aufruf: python scripts/kern/baue_webspace.py [--ziel <ordner>]      (Standard: dist-webspace/)

- Das Cockpit wird mit --api api.php gebaut, liegt also neben der Schnittstelle (gleiche Herkunft).
- konfig.php entsteht nur, wenn KS_EXPORT_SCHLUESSEL oder KS_CONTROL_PASSWORD gesetzt ist (in der Veröffentlichung aus den Secrets).
- control.php ist die passwortgeschützte Übersicht für Johannes; targets.json (Titel zu Kern-IDs) und
  build.json (veröffentlichter Commit) sind ihre Hilfsdateien.
- impressum.html entsteht nur, wenn KS_IMPRESSUM (HTML, aus dem Secret) gesetzt ist; vorerst keines.
  Das Impressum steht nie im öffentlichen Repository.
- Der Ordner daten/ enthält nur die .htaccess; Antworten auf dem Server werden nie überschrieben.
"""
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def load_list(name, key):
    with open(os.path.join(ROOT, "kern", f"{name}.json"), encoding="utf-8") as f:
        return json.load(f)[key]


def build_targets():
    """Readable titles for every kern ID an answer can point to (used by control.php)."""
    targets = {"VORGEHEN": {"kind": "vorgehen", "title": "Wie wir vorgehen"}}
    for q in load_list("fragen", "fragen"):
        targets[q["id"]] = {"kind": "frage", "title": q.get("frage", "")}
    for c in load_list("bauteile", "bauteile"):
        targets[c["id"]] = {"kind": "bauteil", "title": c.get("name", "")}
    for s in load_list("quellen", "quellen"):
        targets[s["id"]] = {"kind": "quelle", "title": s.get("titel") or s.get("pfad") or ""}
    names = {k: v["title"] for k, v in targets.items()}
    labels = {t["id"]: t["name"] for t in load_list("begriffe", "begriffe")}
    for a in load_list("angaben", "angaben"):
        unit = a.get("einheit") or ""
        title = f"{names.get(a.get('ziel'), a.get('ziel'))}: {labels.get(a.get('eigenschaft'), a.get('eigenschaft', ''))} = {a.get('wert')} {unit}".strip()
        targets[a["id"]] = {"kind": "angabe", "title": title}
    for r in load_list("beziehungen", "beziehungen"):
        targets[r["id"]] = {"kind": "beziehung", "title": f"{names.get(r.get('von'), r.get('von'))} {labels.get(r.get('art'), r.get('art', '')).lower()} {names.get(r.get('zu'), r.get('zu'))}"}
    return targets


def current_commit():
    if os.environ.get("GITHUB_SHA"):
        return os.environ["GITHUB_SHA"]
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def main():
    ziel = os.path.abspath(sys.argv[sys.argv.index("--ziel") + 1]) if "--ziel" in sys.argv else os.path.join(ROOT, "dist-webspace")
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "kern", "baue_cockpit.py"), "--api", "api.php"], check=True)
    if os.path.exists(ziel):
        shutil.rmtree(ziel)
    shutil.copytree(os.path.join(ROOT, "cockpit"), ziel, ignore=shutil.ignore_patterns("artefakt.html", "bilder-paket.json"))
    ws = os.path.join(ROOT, "webspace")
    for name in ("api.php", "control.php", ".htaccess", "datenschutz.html"):
        shutil.copy(os.path.join(ws, name), os.path.join(ziel, name))
    os.makedirs(os.path.join(ziel, "daten"), exist_ok=True)
    shutil.copy(os.path.join(ws, "daten", ".htaccess"), os.path.join(ziel, "daten", ".htaccess"))
    # Impressum nur, wenn KS_IMPRESSUM gesetzt ist (Entscheidung Johannes 12.10.2026: vorerst keines).
    if os.environ.get("KS_IMPRESSUM"):
        with open(os.path.join(ws, "impressum.vorlage.html"), encoding="utf-8") as f:
            impressum = f.read().replace("<!--IMPRESSUM-->", os.environ["KS_IMPRESSUM"])
        with open(os.path.join(ziel, "impressum.html"), "w", encoding="utf-8") as f:
            f.write(impressum)
    with open(os.path.join(ziel, "targets.json"), "w", encoding="utf-8") as f:
        json.dump(build_targets(), f, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(ziel, "build.json"), "w", encoding="utf-8") as f:
        json.dump({"commit": current_commit(), "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}, f)
    config = {}
    if os.environ.get("KS_EXPORT_SCHLUESSEL"):
        config["export_schluessel"] = os.environ["KS_EXPORT_SCHLUESSEL"]
    if os.environ.get("KS_CONTROL_PASSWORD"):
        config["control_password"] = os.environ["KS_CONTROL_PASSWORD"]
    if config:
        with open(os.path.join(ziel, "konfig.php"), "w", encoding="utf-8") as f:
            f.write("<?php return json_decode(<<<'KONFIG'\n" + json.dumps(config) + "\nKONFIG, true);\n")
    # Das Cockpit verlinkt Impressum und Datenschutz im Fuß.
    print(f"Webspace-Paket: {os.path.relpath(ziel, ROOT)}")
    # Danach Cockpit wieder ohne API bauen, damit cockpit/ für GitHub Pages unverändert bleibt.
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "kern", "baue_cockpit.py")], check=True, capture_output=True)


if __name__ == "__main__":
    main()
