#!/usr/bin/env python3
"""Veröffentlicht Forschungsseite und Cockpit von Hand auf GitHub Pages (Branch gh-pages).

Keine GitHub Actions. Aufbau der veröffentlichten Seite (seit 12.10.2026):
  /            Weiterleitung auf /cockpit/
  /cockpit/    Cockpit aus dem Wissenskern (Arbeitsfassung für Thorsten; Antworten über GitHub-Issues)

Astras Forschungsseite mit 3D-Werkstatt ist archiviert (Branch archiv/astra-forschungsseite-20261011,
docs/ordnung/ARCHIV-FORSCHUNGSSEITE.md). Nur wenn sie ausdrücklich wieder veröffentlicht werden soll:

Die Forschungsseite kommt aus einem fertigen Build:
  --seite <ordner>   bereits gebauter Ordner (z. B. ein entpacktes altes Pages-Artefakt)
  --mit-forschungsseite  npm run build (braucht installierte Abhängigkeiten) und dann dist/
  --ohne-forschungsseite
                     Übergang, solange kein Build der Forschungsseite vorliegt: Unter / steht
                     dann nur eine Weiterleitung auf /cockpit/. Sobald gebaut werden kann,
                     wieder mit --seite oder npm run build veröffentlichen.

Aufruf: python scripts/kern/veroeffentliche_cockpit.py [--seite <ordner>] [--ohne-push]
GitHub Pages: „Deploy from a branch“, Branch gh-pages, Ordner / (root).
"""
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BRANCH = "gh-pages"


WEITERLEITUNG = """<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="0; url=cockpit/"><title>Kleines Schäferrad</title>
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#edf1ec;color:#1c2726;font:17px/1.5 system-ui,sans-serif;padding:16px}
a{color:#2b6a76}p{max-width:34ch}</style></head>
<body><p>Weiter zum <a href="cockpit/">Cockpit des Kleinen Schäferrads</a>. Das Cockpit ist der Arbeitsstand der Bestandsaufnahme.</p></body></html>
"""


def git(*args, cwd=ROOT, check=True):
    return subprocess.run(["git", *args], cwd=cwd, check=check, text=True, capture_output=True)


def main():
    zweig = git("symbolic-ref", "--short", "-q", "HEAD", check=False).stdout.strip()
    if zweig != "main" and "--erlaube-arbeitsbranch" not in sys.argv:
        sys.exit(f"Veröffentlicht wird nur aus main (aktuell: {zweig or 'losgelöst'}). Erst mergen, dann auf main wechseln.")
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "kern", "baue_cockpit.py")], check=True)
    quelle = git("rev-parse", "--short", "HEAD").stdout.strip()
    sauber = not git("status", "--porcelain", "--", "kern", "scripts/kern").stdout.strip()
    if not sauber:
        sys.exit("kern/ oder scripts/kern/ haben ungespeicherte Änderungen. Erst committen, dann veröffentlichen.")

    ohne = "--seite" not in sys.argv and "--mit-forschungsseite" not in sys.argv
    if ohne:
        seite = tempfile.mkdtemp()
        with open(os.path.join(seite, "index.html"), "w", encoding="utf-8") as f:
            f.write(WEITERLEITUNG)
    elif "--seite" in sys.argv:
        seite = os.path.abspath(sys.argv[sys.argv.index("--seite") + 1])
    else:
        subprocess.run(["npm", "run", "build"], cwd=ROOT, check=True)
        seite = os.path.join(ROOT, "dist")
    if not os.path.exists(os.path.join(seite, "index.html")):
        sys.exit(f"Keine Forschungsseite in {seite} (index.html fehlt). Ohne sie würde die bisherige Seite überschrieben.")

    tmp = tempfile.mkdtemp()
    try:
        vorhanden = git("ls-remote", "--heads", "origin", BRANCH).stdout.strip()
        if vorhanden:
            git("fetch", "origin", f"{BRANCH}:refs/remotes/origin/{BRANCH}")
            git("worktree", "add", "--detach", tmp, f"origin/{BRANCH}")
        else:
            git("worktree", "add", "--detach", tmp)
            git("checkout", "--orphan", BRANCH + "-neu", cwd=tmp)
            git("rm", "-rf", "--quiet", ".", cwd=tmp)
        for name in os.listdir(tmp):
            if name != ".git":
                p = os.path.join(tmp, name)
                shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
        shutil.copytree(seite, tmp, dirs_exist_ok=True)
        shutil.copytree(os.path.join(ROOT, "cockpit"), os.path.join(tmp, "cockpit"), dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("artefakt.html", "bilder-paket.json"))
        open(os.path.join(tmp, ".nojekyll"), "w").close()
        git("add", "-A", cwd=tmp)
        if not git("status", "--porcelain", cwd=tmp).stdout.strip():
            print("Keine Änderung gegenüber der veröffentlichten Seite.")
            return
        name = git("config", "user.name", check=False).stdout.strip() or "jdistlr"
        mail = git("config", "user.email", check=False).stdout.strip() or "distler.johannes@gmail.com"
        git("-c", f"user.name={name}", "-c", f"user.email={mail}", "commit", "-m",
            f"Cockpit veröffentlicht (erzeugt aus {quelle})", cwd=tmp)
        if "--ohne-push" in sys.argv:
            print(f"Commit vorbereitet in {tmp}; nicht gepusht.")
            return
        subprocess.run(["git", "push", "origin", f"HEAD:refs/heads/{BRANCH}"], cwd=tmp, check=True,
                       env={**os.environ, "KS_PAGES_VEROEFFENTLICHUNG": "1"})
        print(f"Veröffentlicht auf {BRANCH} (Quelle {quelle}): https://jdistlr.github.io/kleines-schaeferrad/ und …/cockpit/")
    finally:
        if "--ohne-push" not in sys.argv:
            git("worktree", "remove", "--force", tmp, check=False)


if __name__ == "__main__":
    main()
