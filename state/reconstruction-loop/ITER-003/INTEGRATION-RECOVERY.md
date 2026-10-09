# ITER-003 INTEGRATION RECOVERY REVIEW READY

Continuation: PR #15, branch `work/iter003-integration-recovery-20261009`, inherited HEAD `134b2d6`; runtime repair `f727b8e6b7f05524d46e9128ef74e853112bdc5b`.

This gate means ready for integration review, not mechanical release, merge permission or deployment.

## Completed integration scope

- F01: streaming projection extrema retained; clean production build succeeds, including drawings, field PDFs and atomic offline bundle.
- F04: all 39 Thorsten statements and canonical source backlinks retained; none promoted to confirmed as-built dimensions.
- F05: ITER-003 provenance and current bearing selectors retained; KS-50 contains actual projection paths, A3/A4 dimensions verified. Prior PDF visual evidence remains available.
- Remaining field-workbench startup failure: replace unconditional idle WebGL rendering with coalesced rendering on change; preserve active animation, controls and fallbacks. New browser regression covers idle/pause, orbit, animation and concurrent context startup. No timeout increase.
- Current local validation: Astro check, production build, all 37 Node tests, source verification and all four browser journeys pass. Offline capture, media integrity and fresh-context import pass.
- Preservation check: canonical inputs, geometry source, both model archives and all view artifacts unchanged against inherited HEAD. No reconstruction rerun.

CI on repair commit: [production build 37992432720](https://github.com/jdistlr/kleines-schaeferrad/actions/runs/37992432720) and [four browser journeys 37992432907](https://github.com/jdistlr/kleines-schaeferrad/actions/runs/37992432907). Final outcomes are recorded in `integration-recovery/closure/ci-validation.json`.

Evidence, screenshots, runtime versions, exact failure boundary and limitations: [closure report](integration-recovery/closure/README.md). Earlier continuation evidence and repairs remain intact.

## Open boundaries, not silently declared green

F02: 48 Kumpfnagel paths remain unresolved; no fictitious bores. F03: support/ground/wedge contacts remain synthetic or unverified. Neither finding was modified or closed.

The old appended candidate audit in `npm run test:reconstruction` exits 1 because its old LAND-arm/crossing selector is no longer applicable to the expert-replaced geometry. Its Node tests pass, but the whole legacy command is explicitly **not passed**. The exact result is retained in `integration-recovery/closure/ks-reconstruction-audit.log`; no geometry or historical audit evidence was rewritten to make it green. `npm run test:calibration` exits 0 but does not certify mechanics.

Physical iPhone/Safari, independent human print review and engineering sign-off remain outside the automated evidence. The local old-browser baseline passed; the exact original CI timeout was not reproduced locally. The final CI result supplies the original-browser acceptance evidence.

No merge. No deployment. No new measurements or geometry iteration.
