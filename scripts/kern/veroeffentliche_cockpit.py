#!/usr/bin/env python3
"""Veröffentlicht das Cockpit von Hand auf GitHub Pages (Branch gh-pages).

Keine GitHub Actions: Das Skript baut die Seite lokal, legt sie als einzigen
Inhalt auf den Branch gh-pages und pusht ihn. GitHub Pages muss einmalig auf
„Deploy from a branch“, Branch gh-pages, Ordner / (root) eingestellt sein.

Aufruf: python scripts/kern/veroeffentliche_cockpit.py [--ohne-push]
"""
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BRANCH = "gh-pages"


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
        shutil.copy(os.path.join(ROOT, "cockpit", "index.html"), os.path.join(tmp, "index.html"))
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
        print(f"Veröffentlicht auf {BRANCH} (Quelle {quelle}): https://jdistlr.github.io/kleines-schaeferrad/")
    finally:
        if "--ohne-push" not in sys.argv:
            git("worktree", "remove", "--force", tmp, check=False)


if __name__ == "__main__":
    main()
