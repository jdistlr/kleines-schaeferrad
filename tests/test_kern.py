"""Tests für das Kernmodell: der echte Kern ist gültig, kaputte Varianten werden erkannt.

Aufruf: python -m unittest tests/test_kern.py
"""
import copy
import json
import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts", "kern"))
from pruefe_kern import pruefe  # noqa: E402

KERN = os.path.join(ROOT, "kern")


class KernTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.kern = os.path.join(self.tmp, "kern")
        shutil.copytree(KERN, self.kern)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def aendere(self, name, funktion):
        pfad = os.path.join(self.kern, name + ".json")
        with open(pfad, encoding="utf-8") as f:
            daten = json.load(f)
        funktion(daten)
        with open(pfad, "w", encoding="utf-8") as f:
            json.dump(daten, f, ensure_ascii=False)

    def fehler(self):
        return pruefe(self.kern, ROOT)[0]

    def erwarte_fehler(self, teiltext):
        f = self.fehler()
        self.assertTrue(any(teiltext in x for x in f), f"Erwartet Fehler mit „{teiltext}“, bekam: {f[:5]}")

    def angabe(self, daten, aid):
        return next(a for a in daten["angaben"] if a["id"] == aid)

    # --- der echte Kern ---------------------------------------------------
    def test_echter_kern_ist_gueltig(self):
        fehler, _, statistik = pruefe(KERN, ROOT)
        self.assertEqual(fehler, [])
        self.assertGreater(statistik["angaben"], 400)

    def test_keine_angabe_ist_ohne_mensch_bestaetigt(self):
        with open(os.path.join(KERN, "angaben.json"), encoding="utf-8") as f:
            for a in json.load(f)["angaben"]:
                if a["gueltigkeit"] == "bestaetigt":
                    self.assertIsNotNone(a["bestaetigt"])

    # --- kaputte Varianten -------------------------------------------------
    def frage(self, daten, fid):
        return next(f for f in daten["fragen"] if f["id"] == fid)

    def test_kurztitel_zu_lang(self):
        self.aendere("fragen", lambda d: self.frage(d, "F-001").update(kurztitel="x" * 41))
        self.erwarte_fehler("kurztitel hat 41 Zeichen")

    def test_klaerung_unbekannt(self):
        self.aendere("fragen", lambda d: self.frage(d, "F-001").update(klaerung="irgendwo"))
        self.erwarte_fehler("klaerung irgendwo unbekannt")

    def test_unbekanntes_ziel(self):
        self.aendere("angaben", lambda d: self.angabe(d, "CLAIM-0001").update(ziel="COMP-GIBTESNICHT"))
        self.erwarte_fehler("weder Bauteil, Beziehung noch Quelle")

    def test_bestaetigt_ohne_person(self):
        self.aendere("angaben", lambda d: self.angabe(d, "CLAIM-0001").update(gueltigkeit="bestaetigt"))
        self.erwarte_fehler("bestaetigt.von")

    def test_bestaetigt_mit_person_ist_gueltig(self):
        self.aendere("angaben", lambda d: self.angabe(d, "TH-20261009-26").update(
            gueltigkeit="bestaetigt", bestaetigt={"von": "P-THORSTEN", "am": "2026-10-12"}))
        self.assertEqual(self.fehler(), [])

    def test_muendlich_ohne_aussagende_person_nicht_bestaetigbar(self):
        self.aendere("angaben", lambda d: self.angabe(d, "AN-20261011-02").update(
            gueltigkeit="bestaetigt", bestaetigt={"von": "P-THORSTEN", "am": "2026-10-12"}))
        self.erwarte_fehler("ohne aussage_von")

    def test_ueberholt_ohne_nachfolger(self):
        self.aendere("angaben", lambda d: self.angabe(d, "AN-20261011-03").update(ersetzt_durch=None))
        self.erwarte_fehler("braucht ersetzt_durch")

    def test_alias_doppelt_vergeben(self):
        def f(d):
            next(b for b in d["begriffe"] if b["id"] == "B-FLUEGELBRETT")["aliase"].append("Schetter")
        self.aendere("begriffe", f)
        self.erwarte_fehler("„Schetter“ gehört zu")

    def test_fragen_kreis(self):
        def f(d):
            fr = {x["id"]: x for x in d["fragen"]}
            fr["F-002"]["haengt_ab_von"] = ["F-001"]
        self.aendere("fragen", f)
        self.erwarte_fehler("haengt_ab_von bildet einen Kreis")

    def test_arbeitsschritte_kreis(self):
        def f(d):
            s = {x["id"]: x for x in d["arbeitsschritte"]}
            s["AS-AUF-01"]["nach"] = ["AS-AUF-02"]
        self.aendere("arbeitsschritte", f)
        self.erwarte_fehler("nach bildet einen Kreis")

    def test_unbekannte_beziehungsart(self):
        self.aendere("beziehungen", lambda d: d["beziehungen"][0].update(art="schwebt_ueber"))
        self.erwarte_fehler("Beziehungsart schwebt_ueber")

    def test_teil_von_kreis(self):
        def f(d):
            b = {x["id"]: x for x in d["bauteile"]}
            b["ANLAGE"]["teil_von"] = "COMP-SHAFT"
        self.aendere("bauteile", f)
        self.erwarte_fehler("teil_von bildet einen Kreis")

    def test_altdaten_luecke_wird_erkannt(self):
        pfad = os.path.join(self.kern, "migration", "v1-zuordnung.json")
        with open(pfad, encoding="utf-8") as f:
            z = json.load(f)
        del z["zuordnung"]["CLAIM-0001"]
        with open(pfad, "w", encoding="utf-8") as f:
            json.dump(z, f)
        self.erwarte_fehler("CLAIM-0001 ist im Kern nicht abgebildet")

    def test_eigenschaft_ohne_deutschen_namen(self):
        self.aendere("angaben", lambda d: self.angabe(d, "CLAIM-0001").update(eigenschaft="drawn_overall_length"))
        self.erwarte_fehler("fehlt im Glossar")

    def test_doppelte_datei_wird_abgelehnt(self):
        def f(d):
            foto = next(q for q in d["quellen"] if q["art"] == "foto" and q.get("pfad"))
            kopie = dict(foto, id="DATEI-TEST-KOPIE", kopien=[], alt_ids=[])
            d["quellen"].append(kopie)
        self.aendere("quellen", f)
        self.erwarte_fehler("Kopien zusammenführen")

    def test_unbekannte_bildart(self):
        def f(d):
            next(q for q in d["quellen"] if q["art"] == "foto")["bildart"] = "schnappschuss"
        self.aendere("quellen", f)
        self.erwarte_fehler("Bildart schnappschuss unbekannt")

    def test_angabe_ohne_quelle(self):
        self.aendere("angaben", lambda d: self.angabe(d, "CLAIM-0001").update(quellen=[]))
        self.erwarte_fehler("keine Quelle")


if __name__ == "__main__":
    unittest.main()
