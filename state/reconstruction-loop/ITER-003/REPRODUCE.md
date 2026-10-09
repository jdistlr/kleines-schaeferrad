# Reproduktion

Vom Repository-Root, Node >=22.12, Python mit numpy/Pillow/moderngl und EGL:

```sh
npm ci --ignore-scripts
node --test tests/*.test.mjs
node state/reconstruction-loop/ITER-003/scripts/export.mjs
python state/reconstruction-loop/ITER-003/scripts/render.py
node state/reconstruction-loop/ITER-003/scripts/audit.mjs
./node_modules/.bin/astro build
```

export.mjs erzeugt komprimierte GLBs und Metadaten in models sowie temporäre Dreiecksdaten unter /tmp/ks-iter003. render.py benutzt diese Daten. GLBs mit gzip entpacken; mechanische Z-Achse wird im glTF zu Y-up gedreht. Keine Standortregistrierung in dieser Rotation.

scripts/reconcile.py dokumentiert die initiale kanonische Migration. Es ist kein allgemeiner Buildschritt; nachfolgende Anpassungen an reconstruction-constraints.json dürfen nicht dadurch überschrieben werden. ITER-001/002 bleiben archivierte Vergleichszustände.
