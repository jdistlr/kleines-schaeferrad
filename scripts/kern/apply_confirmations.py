#!/usr/bin/env python3
"""Writes confirmations from the webspace into the knowledge core (kern/angaben.json).

Johannes and Thorsten confirm values in the cockpit while signed in with GitHub (api.php?aktion=confirm).
The return workflow fetches them into evidence/antworten/webspace.json ("bestaetigungen") and runs this
script. The decision is theirs; this script only records it:

  - latest decision "bestaetigt"      -> gueltigkeit "bestaetigt", bestaetigt = {von, am, beleg}
  - latest decision "zurueckgenommen" -> back to "offen", but only if the confirmation came from the webspace

Values that are historical, superseded or rejected are never touched; they are listed instead.
Afterwards the core is validated; on errors nothing is written.

Usage: python scripts/kern/apply_confirmations.py [path/to/webspace.json] [--dry-run]
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pruefe_kern import pruefe  # noqa: E402

CLAIMS = os.path.join(ROOT, "kern", "angaben.json")
WEB_PREFIX = "B-"  # ids of webspace confirmations


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    source = args[0] if args else os.path.join(ROOT, "evidence", "antworten", "webspace.json")
    if not os.path.exists(source):
        print(f"Keine Datei {source}; nichts zu tun.")
        return 0
    with open(source, encoding="utf-8") as f:
        decisions = json.load(f).get("bestaetigungen", [])
    latest = {}
    for d in sorted(decisions, key=lambda x: x.get("am", "")):
        latest[d["ziel"]] = d

    with open(CLAIMS, encoding="utf-8") as f:
        data = json.load(f)
    by_id = {a["id"]: a for a in data["angaben"]}
    confirmed, withdrawn, skipped = [], [], []
    for target, d in latest.items():
        a = by_id.get(target)
        if not a:
            skipped.append(f"{target}: unbekannter Wert")
            continue
        if a["gueltigkeit"] in ("historisch", "ueberholt", "verworfen"):
            skipped.append(f"{target}: ist {a['gueltigkeit']}, wird nicht geändert")
            continue
        if d["aktion"] == "bestaetigt":
            if a["gueltigkeit"] == "bestaetigt":
                continue
            if a["grundlage"] == "muendlich" and not a.get("aussage_von"):
                skipped.append(f"{target}: mündlich ohne bekannte Person (F-007), kann noch nicht bestätigt werden")
                continue
            a["gueltigkeit"] = "bestaetigt"
            a["bestaetigt"] = {"von": d["person"], "am": d["am"][:10], "beleg": d["id"]}
            confirmed.append(f"{target} von {d['person']} am {d['am'][:10]}")
        elif d["aktion"] == "zurueckgenommen":
            beleg = (a.get("bestaetigt") or {}).get("beleg", "")
            if a["gueltigkeit"] == "bestaetigt" and beleg.startswith(WEB_PREFIX):
                a["gueltigkeit"] = "offen"
                a["bestaetigt"] = None  # same shape as before the confirmation
                withdrawn.append(f"{target} (zurückgenommen von {d['person']} am {d['am'][:10]})")
            elif a["gueltigkeit"] == "bestaetigt":
                skipped.append(f"{target}: Bestätigung stammt nicht aus dem Cockpit, Rücknahme bitte von Hand")

    if not confirmed and not withdrawn:
        print("Keine neuen Bestätigungen.")
        for s in skipped:
            print("  übersprungen:", s)
        return 0

    if dry:
        target_dir = None
    else:
        with open(CLAIMS, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        errors = pruefe(os.path.join(ROOT, "kern"), ROOT)[0]
        if errors:
            # Leave the core as it was; the workflow then opens no pull request with a broken core.
            os.system(f'git -C "{ROOT}" checkout -- kern/angaben.json')
            print("Kern wäre ungültig, nichts geschrieben:")
            for e in errors[:20]:
                print("  ", e)
            return 1
        target_dir = CLAIMS
    print(f"Bestätigt: {len(confirmed)}, zurückgenommen: {len(withdrawn)}{' (Probelauf)' if dry else ''}")
    for s in confirmed:
        print("  ✓", s)
    for s in withdrawn:
        print("  ↺", s)
    for s in skipped:
        print("  übersprungen:", s)
    return 0 if target_dir or dry else 1


if __name__ == "__main__":
    sys.exit(main())
