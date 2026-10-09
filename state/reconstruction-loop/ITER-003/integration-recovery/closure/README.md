# ITER-003 recovery continuation — final review evidence

Continued PR #15 from remote `134b2d67b4ddfbfdf3106278a85f81ef9138ea98`; repair commit `f727b8e6b7f05524d46e9128ef74e853112bdc5b`. No reconstruction restart.

## Remaining failure and repair

At the inherited HEAD, production run 37990971132 succeeded. In acceptance run 37990971119, integration, reconstruction and field-kit succeeded; field failed at `browser-field.mjs:28:188`, the **initial storage readiness wait in a second browser context**, before importing. Job 114024718078 and artifact 11644514307 were inspected, including the failure screenshot and JSON. They show an initialized viewer, two canvases and `Lokal gesichert · 0 Einträge` even though the wait timed out. The original artifact remains at https://github.com/jdistlr/kleines-schaeferrad/actions/runs/37990971119/artifacts/11644514307.

The viewer submitted full WebGL frames and recomputed the water simulation on every animation frame even when stopped. Initialization also submitted multiple redundant synchronous renders. This continuously occupied the shared software GPU while another context initialized, delaying frame-based readiness evaluation. The repair coalesces visual changes into one frame, stops drawing an unchanged scene, updates water simulation only in operation mode when needed, and skips hidden-document rendering. Camera damping, dragging, running animation, pause, reset, resize, selection and scan updates still invalidate the view. No timeouts were increased; IndexedDB data semantics and model construction were not changed.

Evidence boundary: the entire old field test passed locally with Chromium 141; the exact Chromium 151 CI timeout was **not reproduced locally**. The baseline's continuous rendering and high software-GPU load were observed. The new regression independently requires an idle scene and paused operation to settle, verifies active animation and orbit redraw, and opens a second context while the first viewer remains alive. Final CI on repair commit f727b8e passes all four journeys with its original Chromium 151 browser version.

## Validation and preserved work

- Full production build, Astro check (0 errors, 0 warnings; four pre-existing hints), 37 Node tests and evidence verification pass locally.
- Integration journey passes: idle/concurrent startup regression, animation and orbit, 13 scene modes, 34 component inspectors, Truth (296 meshes) / Brute (945 meshes), WebGL-unavailable and IndexedDB-denied fallback.
- Field journey passes all four profiles with draft resume, photo bytes, record review, duplicate-safe import, fresh-context import, scan, target sizes and overflow checks.
- Reconstruction and field-kit journeys pass across desktop, 320 px, iPhone emulation and 200% text. Offline reload, draft resume, 28 photo records/attachments, SHA-256 media verification and fresh-context offline import pass.
- PDF formats: 11-page A3 and 2-page A4 outputs; KS-50 is non-empty (12 paths, 305248 bytes), labeled ITER-003. Existing PDF visual evidence from the previous continuation is retained; no new reconstruction/render set was generated.
- `preservation.json` verifies unchanged canonical data, evidence, geometry/calibration/expert/mechanics source, both archived GLBs and all archived view artifacts against the inherited HEAD. All 39 expert claims remain non-as-built. Prior F01/F04/F05 repairs are preserved.
- Local screenshots were inspected for the current workshop and fallback. Browser evidence is simulated Chromium, not physical iPhone/Safari testing or an independent engineering/print sign-off.

## Explicitly retained limitations

F02 remains unresolved (48 nail paths); F03 remains synthetic/unverified. No new dimensions, geometry corrections, source promotions or safety claims.

The legacy `npm run test:reconstruction` command's Node tests pass, but its appended `scripts/audit-candidates.mjs` exits 1: its old LAND-arm/crossing-candidate selector reports zero crossing overlaps after ITER-003's expert geometry replacement, whereas it expects a positive count. This is **not a green result** and is retained in `ks-reconstruction-audit.log`; it must not be presented as certification of the old candidate families. The current 37-test suite and four CI browser journeys are the integration gate. `npm run test:calibration` exits 0; its sampled contact findings are preserved in `ks-calibration-audit.log` and do not close F02/F03. Audit-generated changes to historical ITER-001/reconstruction reports were discarded, preserving their existing evidence rather than overwriting it.

Local runtime: Playwright 1.62.1 with existing Chromium Headless Shell 141.0.7390.37. The Chromium 151 download failed with an invalid ZIP response in this environment; CI uses its pinned Playwright 1.62.1 / Chromium 151. The baseline reproduction used the existing Playwright 1.56.1 / Chromium 141 and is labeled accordingly.

Production CI run 37992432720 and acceptance CI run 37992432907 are successful; all four acceptance jobs pass. See `ci-validation.json`.

**ITER-003 INTEGRATION RECOVERY REVIEW READY.** No merge or deployment. This is an integration-review gate, not a mechanical or human field-use approval.

## Repeat-run test correction

The documentation-only HEAD `04484c9` repeated the CI suites. Run 37992980382 exposed a flaw in the new integration regression: `paused operation keeps rendering`, render count 38 versus 36. The test treated 600 ms of wall-clock silence as settled and then required an unchanged counter over another 400 ms. A software-GPU frame can span that silence; it was not evidence that camera/layout rendering had completed. The original field journey remains successful.

The regression now requires twelve consecutive **animation-frame callbacks** with no redraw. This distinguishes an idle scene from a renderer blocked on a slow frame and still fails an unconditional render loop. The existing 30-second timeout is unchanged. No additional runtime or geometry change was made. The earlier successful CI evidence remains labeled with its tested SHA; the PR records the final follow-up SHA and CI links.
