# NEXT WORK SESSION — UX R1/R4 Recovery

**Start condition:** PR #17 reviewed and merged to main **only after** Torsten's annotated photo has been stored with verified SHA-256 and the final CI matrix is green. If the original transfer remains blocked, stop and report `SOURCE TRANSFER PENDING`; do not infer a green evidence gate. Independently confirm current main SHA before work. PR #16 at `129a9a9` is the audit reference, not automatically merged.

## Mission
Implement bounded R1/R4 UX recovery against current main. The goal is a usable, calmer field/workbench experience, **not** a new platform, reconstruction or schema migration.

## Required changes
1. Make urgent water-intake action visible and accessible within two visible actions; link source-video and measurement guidance without implying unavailable archive originals exist.
2. Fix hero/photo collision at 200% computed text size using intrinsic layout/reflow, not hidden content.
3. On 320/390/768 px prioritize task question → selected component → sketch/photo → open property → record observation; progressively disclose technical variants without deleting expert controls.
4. Preserve deep-link/resume and component/property context across discover → inspect → record.
5. Respect existing MUX design grammar; keep all 21 task IDs and order, v1 import semantics, original media and model geometry untouched.

## Verification and evidence
- Baseline screenshots and after screenshots for desktop, 768, 390, 320 and 200% text; keyboard and reduced-motion journeys.
- Exercise field intake, workbench, import/export conflict and tampered hash rejection, return-to-task, WebGL fallback, offline behavior. Label proxy/SSL blockers separately from actual product defects.
- Run build, Node, browser integration/reconstruction/field/field-kit at final HEAD; bind each result to exact SHA.
- Record unresolved real iPhone/Safari, second-device and print/physical acceptance as open; do not fabricate.

## Stop
Open a separate UX PR with reviewable diffs and evidence. Stop at `UX R1+R4 REVIEW READY`. No merge, deployment, new geometry, F02/F03 edits, fabricated measures or source promotion.
