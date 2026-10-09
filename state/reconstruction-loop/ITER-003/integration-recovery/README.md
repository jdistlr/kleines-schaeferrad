# ITER-003 Integration Recovery — continuation history

Continuation of PR #15 at remote HEAD `2677758f5671ea0d1d83e4ed90175ec7cfe71c5f`.

Root cause reproduced with local Playwright: `client.js` assumed every evidence asset has `filename` and `archive.path`. 65 Thorsten photographs and the expert narrative instead use `path`. `inspector()` threw `Cannot read properties of undefined (reading 'match')` before `createViewer()` and before `ready=true` / initial persistence. IndexedDB was not the cause. The baseline diagnostic and screenshot are retained here.

Fix: normalize source shapes at the consumer boundary, recognize .jpg, preserve source identity and hashes, publish referenced narrative files in the offline bundle. No timeout increase. Correct the lingering Schetter/Flügelbrett display alias. PDF metadata/footers now derive ITER-003 from projection metadata, explicitly label retained ITER-001 comparison plates, and carry hashes of all six geometry dependencies.

Local checks so far: full production build, 37 Node tests, source verification, four-profile workshop browser journey; model/export fidelity probe confirms Truth 296 / Brute 945 geometries, 39 unchanged view hashes, unchanged input hashes. F02 still 48/48 real nail centrelines intersect rim material; F03 remains open. No geometry iteration or as-built promotion.

Additional field, reconstruction and startup/fallback journeys are being completed. CI now executes all four browser suites, each with diagnostic artifacts. This is the historical continuation record. Current status and validation are in `closure/README.md` and `../INTEGRATION-RECOVERY.md`.

Original CI run 37987615114 job log is retained. Artifact 11643508813 metadata was read; connector download returned a signed file URL, but downloading it twice returned HTTP 403. Its binary diagnostic has not been inspected; local reproduction is separately identified, never passed off as the CI artifact.

Local pinned Playwright 1.62.1 / Chromium 151 download returned an HTML “Site Unavailable” document. Local runs therefore use Chromium Headless Shell 141.0.7390.37, downloaded by Playwright 1.56.1 through its official fallback. CI retains Playwright 1.62.1. No physical iPhone/Safari or engineering safety certification.
