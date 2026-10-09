# ITER-003 Integration Recovery — validation handoff

Base: ITER-003 6999e93146d2dc62337f60e9f72e8e84da2619e0. Independent audit: PR #14, 05b54353211bd055b9f5f243c3ccc4162bf7c2d1.

## F01
Replaced spread-argument extrema over unbounded projected edge arrays with streaming extrema in src/workbench/projection.mjs. This directly addresses the observed RangeError. **Full clean production build must still be confirmed by CI**; successful source edit is not a build result.

## F04
Added explicit TH-25..29 source-analysis backlinks to the already cited expert narrative source; no new field measurements. Corrected COMP-PADDLES naming and the plane-reference note. COMP-RADSTADT is explicitly a terminology alias of existing COMP-RADSTATT, not a second physical assembly. Local term Schetter now distinguishes Schetternbretter from Flügelbretter. 39 expert claims retained.

## F05
Updated viewer iteration label, drawing revision and projection iteration to ITER-003; replaced removed bearing ID selector with current TH-JOURNAL-/TH-WOOD-BEARING-/COMP-BEARINGS selectors. Drawing provenance identifies expert claims and no independent as-built measurement. **The generated PDF/SVG/field/offline artifacts require fresh build and visual validation.**

## Non-goals / mechanical gates
F02: all 48 Kumpfnagel paths remain mechanically unresolved; do not add fictitious bores. F03: support/ground/keil contacts remain synthetic or unverified. No geometry edits, no claim of safe assembly, no Truth promotion. No main merge or deployment.

## Acceptance checklist (pending execution)
- Clean checkout npm ci, npm run check, npm run build (prepare workbench, field PDFs, Astro, offline manifest).
- npm run test:workbench, test:field, test:reconstruction, test:calibration; regression for non-spread large edge count.
- Confirm non-empty KS-50 bearing projection, regenerated projection revision/source status, A3/A4 PDFs, offline URLs and page sizes.
- Check all 39 claims, source backlinks, no installedMetric promotion, no new mesh geometry, both GLBs and views intact.
- Independent visual/print and browser review. If unavailable, mark unverified.

Gate is **NOT YET READY** until build, artifact checks and review evidence are attached.