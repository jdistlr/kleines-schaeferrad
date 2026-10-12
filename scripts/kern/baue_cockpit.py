#!/usr/bin/env python3
"""Erzeugt das Cockpit (eine HTML-Seite) aus dem Wissenskern.

Aufruf:
  python scripts/kern/baue_cockpit.py              # schreibt cockpit/index.html (vollständiges Dokument)
  python scripts/kern/baue_cockpit.py --artefakt   # ohne Dokumentrahmen, für die Arbeitsfassung (Antworten speicherbar)
  python scripts/kern/baue_cockpit.py --api URL    # Antworten über einen eigenen Server (siehe docs/ordnung/ANTWORTEN-SCHNITTSTELLE.md)

Vorschaubilder landen unter cockpit/bilder/ (braucht Pillow) und werden mitveröffentlicht.

Das Cockpit ist nur eine Ansicht. Es wird nie von Hand bearbeitet; Änderungen gehören in kern/.
"""
import json
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HIER, "..", ".."))
sys.path.insert(0, HIER)
from pruefe_kern import lade_kern, pruefe  # noqa: E402


BILDER = os.path.join(ROOT, "cockpit", "bilder")


def vorschau(q):
    """Erzeugt ein verkleinertes Vorschaubild (lange Seite 560 px) und gibt den relativen Pfad zurück."""
    pfad = q.get("pfad") or ""
    if q["art"] not in ("foto", "skizze") or not pfad.lower().endswith((".jpg", ".jpeg", ".png")):
        return None
    ziel = os.path.join(BILDER, q["id"] + ".jpg")
    if not os.path.exists(ziel):
        try:
            from PIL import Image, ImageOps
        except ImportError:
            return None
        os.makedirs(BILDER, exist_ok=True)
        with Image.open(os.path.join(ROOT, pfad)) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            im.thumbnail((560, 560))
            im.save(ziel, "JPEG", quality=70, optimize=True, progressive=True)
    return "bilder/" + q["id"] + ".jpg"


# ---------- Statements: show what was actually said instead of linking to raw files ----------
import re

TEXT_KINDS = ("aussage", "kontext", "ableitung", "dokument")
# Sections written as work orders for agents are not shown to people.
AGENT_NOTE = re.compile(r"Modellparameter|Modellcode|3D-Geometrie|Astra|runtime|Runtime", re.I)
HIDDEN_SECTIONS = re.compile(r"Astra|Modellcode|Arbeitsauftrag|Auftrag für|3D-Umsetzung|Abgrenzung", re.I)


def read_text(path):
    full = os.path.join(ROOT, path or "")
    if not path or not os.path.isfile(full) or os.path.getsize(full) > 60000:
        return None
    with open(full, encoding="utf-8") as f:
        return f.read()


def readable_markdown(text):
    """Protocol as people should read it: without agent work orders, „Nutzer“ named neutrally."""
    out, hide, level = [], False, 0
    for line in text.splitlines():
        m = re.match(r"^(#{2,3}) (.*)", line)
        if m:
            if hide and len(m.group(1)) <= level:
                hide = False
            if not hide and HIDDEN_SECTIONS.search(m.group(2)):
                hide, level = True, len(m.group(1))
        if not hide and not AGENT_NOTE.search(line):
            out.append(line)
    return neutral_names("\n".join(out))


# Who „Nutzer“ was is still open (F-007); until then the person is called neutrally.
NEUTRAL = [("Nutzererklärung im Gespräch", "Erklärung im Gespräch"), ("Nutzerbestätigter", "Im Gespräch bestätigter"), ("Nutzerbestätigte", "im Gespräch bestätigte"), ("Nutzererklärung", "Erklärung im Gespräch"),
           ("Nutzerangabe", "Angabe im Gespräch"), ("Nutzer-Messung", "Messung des Gesprächspartners"), ("vom Nutzer", "im Gespräch"),
           ("des Nutzers", "des Gesprächspartners"), ("laut Nutzer", "laut Gesprächspartner")]


def neutral_names(t):
    for old, new in NEUTRAL:
        t = t.replace(old, new)
    return re.sub(r"\bNutzer\b", "Gesprächspartner", t)


def section_of(text, anchor):
    """Lines of the section whose heading starts with the cited place (e.g. „Lichte Öffnung“)."""
    if not anchor:
        return None
    key = anchor.split(",")[0].strip().lower()
    lines = text.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^(#{2,3}) (.*)", line)
        if m and m.group(2).lower().startswith(key):
            body = []
            for nxt in lines[i + 1:]:
                h = re.match(r"^(#{2,3}) ", nxt)
                if h and len(h.group(1)) <= len(m.group(1)):
                    break
                body.append(nxt)
            return body
    return None


def plain(md_text):
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", md_text)
    return re.sub(r"\*\*|__|`", "", t).strip()


def quote_from_section(body, previous=False):
    """Verbatim quotes (> ...) first; otherwise the first prose paragraph of the section."""
    quotes, block = [], []
    for line in body:
        if line.startswith(">"):
            block.append(line.lstrip("> ").strip())
        elif block:
            quotes.append(" ".join(block)); block = []
    if block:
        quotes.append(" ".join(block))
    # A later correction outranks the verbatim quote it corrects.
    correction = next((plain(line) for line in body if plain(line).startswith("Korrektur")), None)
    if correction and not previous:
        return neutral_names(correction)
    if quotes:
        return neutral_names(plain(quotes[-1] if not previous else quotes[0]))
    para = []
    for line in body:
        if not line.strip() or line.startswith("|"):
            if para:
                break
            continue
        if line.startswith(("#", "!")):
            continue
        para.append(line.strip("- ").strip())
    t = plain(" ".join(para))
    if t.endswith(":"):  # what the sentence introduces belongs to it (next paragraph or list)
        rest, seen, extra = body, False, []
        for line in rest:
            if not seen:
                seen = bool(line.strip()) and plain(line.strip("- ")) and plain(line.strip("- "))[:30] in t
                continue
            if not line.strip():
                if extra:
                    break
                continue
            extra.append(plain(re.sub(r"^\s*(\d+\.|-)\s", "", line)))
        if extra:
            t += " " + " ".join(extra)
    t = neutral_names(t)
    return (t[:420].rsplit(" ", 1)[0] + " …") if len(t) > 420 else t or None


_json_cache = {}


def statement_for(source, anchor):
    path = source.get("pfad") or ""
    if path.endswith(".json"):
        if path not in _json_cache:
            try:
                with open(os.path.join(ROOT, path), encoding="utf-8") as f:
                    _json_cache[path] = json.load(f)
            except (OSError, ValueError):
                _json_cache[path] = {}
        data = _json_cache[path]
        for claim in data.get("claims", []) if isinstance(data, dict) else []:
            if claim.get("id") == anchor and claim.get("statement"):
                return claim["statement"]
        expert = data.get("expert_statement") if isinstance(data, dict) else None
        if isinstance(expert, dict) and expert.get("source_excerpt"):
            return expert["source_excerpt"]
        return None
    text = read_text(path)
    body = section_of(text, anchor) if text else None
    return quote_from_section(body, previous="frühere" in (anchor or "")) if body else None


def source_date(source):
    m = re.search(r"(20\d{2})(\d{2})(\d{2})", source["id"] + " " + (source.get("pfad") or ""))
    return f"{int(m.group(3))}.{int(m.group(2))}.{m.group(1)}" if m else None


def antworten_abzug():
    """Gesicherte Antworten (evidence/antworten/antworten.json), damit das Cockpit sie ohne GitHub-Abfrage zeigt."""
    pfad = os.path.join(ROOT, "evidence", "antworten", "antworten.json")
    if not os.path.exists(pfad):
        return []
    with open(pfad, encoding="utf-8") as f:
        return json.load(f).get("antworten", [])


def figuren():
    """Baut die Figuren aus figuren/figuren.json (helles und dunkles Thema) und legt sie unter cockpit/figuren/ ab.

    Braucht Node. Fehlt es oder scheitert ein Build, bleibt die Figur weg; das Cockpit funktioniert trotzdem.
    """
    import shutil
    import subprocess
    pfad = os.path.join(ROOT, "figuren", "figuren.json")
    if not os.path.exists(pfad):
        return []
    with open(pfad, encoding="utf-8") as f:
        liste = json.load(f)["figuren"]
    ziel = os.path.join(ROOT, "cockpit", "figuren")
    os.makedirs(ziel, exist_ok=True)
    fertig = []
    for fig in liste:
        build = os.path.join(ROOT, fig["build"])
        ordner = os.path.dirname(build)
        ok = True
        for thema, datei in (("--light", fig["id"] + "-hell.html"), (None, fig["id"] + ".html")):
            try:
                subprocess.run(["node", build] + ([thema] if thema else []), cwd=ROOT, check=True, capture_output=True, text=True)
                shutil.copyfile(os.path.join(ordner, datei), os.path.join(ziel, datei))
            except (OSError, subprocess.CalledProcessError) as e:
                print(f"Figur {fig['id']} nicht gebaut: {e}", file=sys.stderr)
                ok = False
                break
        if ok:
            fertig.append({k: fig[k] for k in ("id", "titel", "beschreibung", "fragen", "bauteile")})
    return fertig


def main():
    api = sys.argv[sys.argv.index("--api") + 1] if "--api" in sys.argv else None
    kern_dir = os.path.join(ROOT, "kern")
    fehler, _, st = pruefe(kern_dir, ROOT)
    if fehler:
        sys.exit(f"Kern hat {len(fehler)} Fehler; zuerst python scripts/kern/pruefe_kern.py ausführen.")
    d = lade_kern(kern_dir)
    with open(os.path.join(kern_dir, "angaben.json"), encoding="utf-8") as f:
        stand = json.load(f).get("stand")

    import subprocess
    quellen_by_id = {q["id"]: q for q in d["quellen"]}
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True, capture_output=True).stdout.strip() or None
    daten = {
        "stand": stand,
        "commit": commit,
        "statistik": {k: (dict(v) if hasattr(v, "items") else v) for k, v in st.items()},
        "bauteile": [{k: b.get(k) for k in ("id", "name", "begriff", "art", "teil_von", "anzahl", "hinweis")} for b in d["bauteile"]],
        "begriffe": [{k: b.get(k) for k in ("id", "name", "definition", "aliase")} for b in d["begriffe"]],
        "personen": [{"id": p["id"], "name": p["name"]} for p in d["personen"]],
        "beziehungen": [{k: b.get(k) for k in ("id", "von", "art", "zu", "ueber")} for b in d["beziehungen"]],
        "angaben": [{"id": a["id"], "ziel": a["ziel"], "eig": a["eigenschaft"], "wert": a["wert"], "einheit": a["einheit"],
                     "tol": a.get("toleranz"), "grund": a["grundlage"], "guelt": a["gueltigkeit"],
                     "quellen": [[q["quelle"], q.get("stelle"), statement_for(quellen_by_id[q["quelle"]], q.get("stelle")) if quellen_by_id.get(q["quelle"], {}).get("art") in TEXT_KINDS else None] for q in a["quellen"]],
                     "von": a.get("aussage_von")} for a in d["angaben"]],
        "fragen": [{k: f.get(k) for k in ("id", "frage", "kurztitel", "klaerung", "betrifft", "blockiert", "haengt_ab_von", "entscheidet", "status", "hinweis", "herkunft")} for f in d["fragen"]],
        "quellen": [{"id": q["id"], "art": q["art"], "pfad": q["pfad"], "titel": q["titel"], "ordner": q["ordner"],
                     "bauteil": q.get("bauteil"), "erschlossen": q["erschlossen"], "kopien": len(q.get("kopien", [])),
                     "bildart": q.get("bildart"), "bild": vorschau(q), "person": q.get("person"), "datum": source_date(q),
                     "text": readable_markdown(read_text(q["pfad"])) if q["art"] in TEXT_KINDS and (q.get("pfad") or "").endswith(".md") and read_text(q["pfad"]) else None} for q in d["quellen"]],
        "api": api,
        "impressum": bool(os.environ.get("KS_IMPRESSUM")),
        "figuren": figuren(),
        "antwortenAbzug": antworten_abzug(),
        "vorgehen": open(os.path.join(ROOT, "docs", "ordnung", "VORGEHEN.md"), encoding="utf-8").read() if os.path.exists(os.path.join(ROOT, "docs", "ordnung", "VORGEHEN.md")) else "",
    }
    with open(os.path.join(HIER, "cockpit", "vorlage.html"), encoding="utf-8") as f:
        vorlage = f.read()
    json_text = json.dumps(daten, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    seite = vorlage.replace("/*__DATEN__*/null", json_text)
    if "--artefakt" in sys.argv:
        # Die Arbeitsfassung bekommt die Vorschaubilder als eine Datei (Artefakte veröffentlichen
        # einzelne Dateien nur in begrenzter Zahl); die Seite lädt sie nach dem ersten Bild nach.
        import base64
        from PIL import Image
        import io
        paket = {}
        for q in daten["quellen"]:
            if q["bild"]:
                with Image.open(os.path.join(ROOT, "cockpit", q["bild"])) as im:
                    im.thumbnail((360, 360))
                    puffer = io.BytesIO()
                    im.save(puffer, "JPEG", quality=62, optimize=True)
                paket[q["id"]] = "data:image/jpeg;base64," + base64.b64encode(puffer.getvalue()).decode()
        with open(os.path.join(ROOT, "cockpit", "bilder-paket.json"), "w") as f:
            json.dump(paket, f, separators=(",", ":"))
        daten["bilderPaket"] = "bilder-paket.json"
        json_text = json.dumps(daten, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        seite = vorlage.replace("/*__DATEN__*/null", json_text)
        ziel = os.path.join(ROOT, "cockpit", "artefakt.html")
    else:
        seite = ('<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n'
                 '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n</head>\n<body>\n'
                 + seite + "\n</body>\n</html>\n")
        ziel = os.path.join(ROOT, "cockpit", "index.html")
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    with open(ziel, "w", encoding="utf-8") as f:
        f.write(seite)
    print(f"Cockpit geschrieben: {os.path.relpath(ziel, ROOT)} ({len(seite) // 1024} KB)")


if __name__ == "__main__":
    main()
