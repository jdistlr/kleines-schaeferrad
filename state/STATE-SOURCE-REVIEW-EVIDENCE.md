# P0-A / P1-A review evidence — 2026-10-10

Branch `work/state-source-contract-20261010`, baseline main `118e5f7`. Audit authority: PR #16 `129a9a9`. This is a **connector read-back and audit-trace cross-check**, not a fresh local execution of the original media verifier.

## Verified
- PR #17 patch lists exactly three changed files: `data/source-analyses.json`, `state/CURRENT-STATE.md`, `state/SOURCE-STATUS-CONTRACT.md`. No original media, model, generator, test, workflow or UI file is in the PR diff.
- Parsed the narrative source on the PR branch and all 39 rows of `claims-39-trace.json` from audit `129a9a9`.
- 39 distinct IDs, 39 narrative backlinks, and 39 canonical claim provenance links to `NARRATIVE-TH-CONSTRUCTION-20261009`: **39/39 reciprocal**.
- Audit trace records `intake_value_equal: true` for **39/39**; `as_built_eligible: false` for **39/39**.
- Every original-source occurrence in the archived trace reports `hash_matches: true`. These are **previously captured audit results**, not rehashed raw bytes in this review.
- Source title/review wording updated to avoid implying 39 independent field measurements.

## Open, do not relabel as PASS
- Live raw-byte rehash and independent verification of all 65 Thorsten paths at final branch HEAD: **NOT RUN here**. Diff-level preservation verified; original audit contains the hash evidence.
- CI on final PR HEAD `617a024178a2c9cdde019b9bceb8fcf7f0985e3f`: initially **IN PROGRESS**, runs `38028563084` and `38028563128`. Re-query before any gate decision.
- Human semantic signoff: `COMP-RADSTADT → COMP-RADSTATT` alias, TH-37 local 0.8 m derivation and review-status language: **OPEN**. No runtime alias adapter implemented.
- F02/F03 remain **ENGINEERING NO-GO**; real iPhone/Safari, paper, second-device and offline acceptance **OPEN**.

## Decision
**CONDITIONAL REVIEW / NOT YET GATE-COMPLETE.** Do not merge, deploy, change geometry, or promote source-derived values to as-built. Stop at review after CI and expert decisions are recorded.
