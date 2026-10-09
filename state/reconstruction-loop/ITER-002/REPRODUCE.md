# Nachvollziehbarkeit

Aus Repositorywurzel ausführen. Geprüft mit Node24.19.0, Three0.180.0 aus `vendor/three-0.180.0.tgz`, Python3 sowie NumPy, Pillow und Matplotlib. Kein App-Build oder Export in kanonische Ordner erforderlich.

```bash
node state/reconstruction-loop/ITER-002/scripts/inspect-runtime.mjs
python state/reconstruction-loop/ITER-002/scripts/render-comparison.py
python state/reconstruction-loop/ITER-002/scripts/scan-inspect.py
python state/reconstruction-loop/ITER-002/scripts/write-comparison.py
python state/reconstruction-loop/ITER-002/scripts/write-photo-findings.py
python state/reconstruction-loop/ITER-002/scripts/validate.py
```

`inspect-runtime.mjs` schreibt nur ITER-002-Register sowie temporäre Dreiecksarrays `/tmp/iter002-{brute,truth,nail-reference}.bin`. Keine Kopie eines korrigierten Modells. Renderer benutzt diese unveränderten Dreiecke; Perspektiven und Meshselektionen stehen im Ansichtsmanifest. Die einfachen Tiefensortierungsbilder ersetzen keine Kontaktberechnung.

`write-comparison.py` und `write-photo-findings.py` materialisieren die **manuell visuell erarbeiteten** Befunde; sie führen keine automatische Bildinterpretation durch. Die Kontaktblätter/Crops sind bereits enthalten. `derive-photo-views.py` kann sie erneut aus Originalen erzeugen (Layout/Interpolation können gegenüber der ersten Erzeugung leicht abweichen). `crop-regions.json` definiert Bildregion, Rotation und Vergrößerung; das verändert keine Originaldatei. Pixelregionen in PHOTO-READOUTS beziehen sich auf das EXIF-orientierte Original, nicht auf das Kontaktblatt.

Die historischen Zeichnungsbilder sind zusätzliche Quellen und gehören nicht zu den65 neuen Manifestdateien. Die numerischen Foto-Lesebänder sind keine Feldkalibrierung. Unlesbare oder nicht zuordenbare Endpunkte wurden als null gespeichert.
