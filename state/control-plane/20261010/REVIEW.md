# Model Control Plane — review package

Status: MODEL CONTROL PLANE VERTICAL SLICE REVIEW READY. Implementation tested at 51221b9d0e6ad8aed1fb714f7888f1a38bf0e3c5; subsequent evidence-only commit does not change application or tests.

User-authorized independent design grammar; implementation follows EXPERIENCE-ARCHITECTURE.md and DESIGN-SYSTEM.md. Baseline remote HEAD verified as 606908b. Successful deployment run 38033011709 recorded in evidence/baseline-deployment.json. Current live HTTP comparison and CI browser evidence will be recorded separately.

R1: urgent water action visible in control-plane header and field context; original-video and extra measurement guidance available. R4: intrinsic story columns, mobile task-first question, variants behind existing details, explicit component/property deep links and field-step resume. All 21 tasks and v1 storage unchanged.

Local Chromium launch is blocked by environment socket permissions (Operation not permitted before any page loads). Browser validation must run on GitHub Actions; it is not a product WebGL failure. Final expanded Node suite: 40/40; production build and source preservation passed in CI.

Open physical gates: real iPhone/Safari, OS Dynamic Type, actual second-device restore, paper/physical acceptance and field storage pressure. Browser simulations cannot close these. Missing archive video bytes remain outside this task. One measurement object per existing v1 task remains a documented limitation; extra measurements go on labelled photographed sheets. F02/F03 remain unchanged engineering NO-GO.

No merge, no deployment. Executed acceptance and visual review completed; this is a software review milestone, not engineering or field-device release.

## First executed CI findings (c378c1b)

- Field-kit suite passed, including offline export/restore and 200% root text.
- Integration pointer test used document coordinates without scrolling after the new question/navigation chrome moved the canvas. Fix: scroll the canvas into view and assert hit target is actually CANVAS before the same drag/redraw check. No assertion removed.
- Reconstruction default-language gate rejected new arrow glyphs in the field bridge. Fix: plain actionable labels in existing field/workbench chrome, and explicit disclosure for property source internals. Gate unchanged.
- New browser test server mapped an empty root path to a directory and returned 404. Fix the test server root mapping, rerun baseline and after evidence; first root screenshots are not valid product evidence.

## Second executed CI / visual findings (36de9fd)

All five profiles passed page-width checks, but visual inspection caught overflow *within* the desktop rail and adjacent water-path labels at doubled text. The layout now uses intrinsic em-based widths and wrapping working columns; the browser gate additionally checks internal navigation/flow overflow. A cross-route assertion read the server default before module load; the failure screenshot already showed the correct restored component. Await complete route load before checking the same context value. No context expectation relaxed.


## Final acceptance

All checks passed at code HEAD `51221b9d0e6ad8aed1fb714f7888f1a38bf0e3c5`:

- Control Plane: https://github.com/jdistlr/kleines-schaeferrad/actions/runs/38035076111
- Existing four browser journeys: https://github.com/jdistlr/kleines-schaeferrad/actions/runs/38035076012
- Production build (deployment skipped for PR): https://github.com/jdistlr/kleines-schaeferrad/actions/runs/38035076084
- 40 Node tests; Astro check; original evidence verification; all 39 Torsten statements and 21 tasks preserved.
- Desktop 1440, tablet 768, phone 390/320, computed text doubled at 1280: six routes, no horizontal page overflow, no internal control navigation/water-path overflow, no hero overlap or broken images. Visual review confirmed the repaired rail, water layout and mobile entry.
- Keyboard skip/focus and sliders; Reduced Motion; existing 3D manipulation and WebGL fallback; component/property deep links and photo-step resume.
- Original-byte v1 export and fresh-context restore; tampered hash and conflicting response rejected; existing draft protected. Installed service worker field/control offline round trip passed.

R1/R4 accepted within this Chromium/browser scope: immediate water capture, work question before variants, context retained, step return, intrinsic reflow, existing storage semantics. Physical Safari, OS text sizing and actual field use remain unverified.

## Permanent evidence and reproduction

`evidence/before/` contains 15 immutable-baseline screenshots. `evidence/after/` contains 30 route/profile screenshots, active simulation, results, preservation proof and explicitly SYNTHETIC export/negative fixtures. `evidence/screenshots-manifest.json` binds 46 images to SHA-256 and tested revisions. These are Git files, not only expiring Actions artifacts.

Reproduce with `.github/workflows/control-plane.yml`; local commands are `npm ci`, `npm run check`, `node --test tests/*.test.mjs`, `python scripts/verify_evidence.py`, `node scripts/verify-control-preservation.mjs`, `npm run build`, `node tests/browser-control-plane.mjs` with Playwright Chromium installed. Baseline capture uses a separate worktree at 606908b, never a guessed reconstruction.

## Performance and remaining limits

Initial entry JavaScript is 2,390 encoded bytes (navigation/context); water adds 3,416 bytes before explicit simulation loading. Control routes initialize no WebGL canvas. Recorded resource bytes and local-run timings are in results.json; these are not mobile-network benchmarks or Core Web Vitals. Existing large viewer chunk and roughly 132 MB atomic offline package remain limitations; selective evidence caching is deferred to a separate storage-contract change.

The read-only property/model comparison covers five explicit canonical inputs, not the whole mesh. Other properties expose missing evidence without invented certainty. No complete technical drawing or manufacturing release is asserted. ADR and design-system documents define staged migration of construction, evidence and field experiences without changing v1 records or geometry.
