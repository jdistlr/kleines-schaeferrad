# PR #17 — final evidence closure, 2026-10-10

Inherited remote HEAD: `52cf6227b5ff91fd994cd6864c1f23761a3d017a`; baseline main: `118e5f7da51a89eaf04bfe85072169e902f4b532`. All existing commits retained. This supersedes the earlier connector-only review snapshot; it does not rerun reconstruction.

## Fresh verification

Run from the repository root:

```sh
python state/state-source-closure/20261010/verify.py
python scripts/verify_evidence.py
```

[Machine-readable results](state-source-closure/20261010/verification.json) contain every photo and every TH-01..TH-39 claim, its preserved value, and every original-photo provenance edge.

- **65/65 photo paths PASS**, SHA-256, byte length and Git blob SHA match the photo manifest. **63 distinct payloads**; duplicate payloads preserve distinct original names.
- All 65 originals are byte-identical to both baseline and inherited HEAD. The intake document, photo manifest and complete canonical claims document are also byte-identical to both revisions.
- **39/39 expert corrections PASS**: exact ID membership and subject, predicate, value, unit and scope agree with intake. All canonical records remain unchanged.
- **39/39 narrative links reciprocal**, with exactly 39 unique backlinks on `NARRATIVE-TH-CONSTRUCTION-20261009`. Every intake photo source exists, is hashed, is present in canonical provenance and links back to the claim from its source analysis.
- **39/39 `as_built_eligible:false` preserved**. No new metric observation or geometry claim.
- Existing verifier PASS: 43 historical baseline originals, 4 contributed originals, 10 derivatives, 408 claims, 117 source analyses and graph/conflict references. The separate 65-photo check above is necessary: this verifier's contributed-original counter does not cover that photo manifest.

## Torsten's original: SOURCE TRANSFER BLOCKED

Expected file: `5f0dbdce-2f7a-40c3-9b75-c66153bb40fd.jpeg`, previously recorded size 559904 bytes and SHA-256 `048708cdf56fd72025b12c1bc1e0bd4bc8c201dc74654c4fb2c55ed45fe23eb5`.

The original is not among this session's supplied files. SHA-256 search over all 498 accessible JPEG/JPG/PNG files in the checkout and 30 supplied attachments found **zero matches**. This proves absence in the searched scope, not absence from previous conversations or other storage. No reconstruction, re-encoding, annotation recreation, or substitute original was produced. The expected hash and size above remain prior-session evidence, not a fresh hash of an accessible original.

Per the mission's explicit fallback, this blocker is documented for review. It remains a hard blocker before merge / UX start under the existing PR contract. Unblock by transferring the unchanged original to a versioned evidence path and verifying its exact hash.

## Named expert confirmation preserved

[Torsten's attributed review](TORSTEN-FACHREVIEW-20261010.md) retains the quotations and separates them from interpretation:
- Radstatt / Radstadt: synonymous spellings, stable `COMP-RADSTATT` identity; no preferred spelling invented.
- TH-37: ground directly at the A-Bock to the underside of the trough, 0.80 m; Torsten identified the upper endpoint with a red line. No independent as-built measurement or release inferred.

The only modification to that review document is the source-transfer disposition. No statement, canonical value or attribution has been changed.

## CI and gate protocol

Inherited HEAD `52cf622` has successful [build run 38030477655](https://github.com/jdistlr/kleines-schaeferrad/actions/runs/38030477655) and [field acceptance run 38030477673](https://github.com/jdistlr/kleines-schaeferrad/actions/runs/38030477673), including field, field-kit, reconstruction and integration browser journeys. These are **inherited-HEAD results only**.

After committing this evidence packet, inspect every workflow run, job and commit check at the new exact HEAD. Record immutable run URLs, SHA and conclusions in PR #17; do not create another commit merely to insert its own CI result. Only then record `STATE & SOURCE CONTRACT REVIEW READY` as a **review-package gate with SOURCE TRANSFER BLOCKED**, not completed source archival or permission to merge/start UX.

No CI failure was found at inherited HEAD; no production fix, workflow change, test weakening, geometry or UX change is justified. Historical branch-only workflows are not final-HEAD successes. F02/F03 remain engineering NO-GO; physical iPhone/Safari, second-device, paper and live offline acceptance remain open. No merge or deployment.
