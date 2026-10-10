# Source and status contract — stabilization P1-A

This is a small additive contract over existing files, not a new ontology, migration or engineering approval.

## EO-01: reciprocal narrative provenance
- `data/source-analyses.json` source `NARRATIVE-TH-CONSTRUCTION-20261009` now lists `TH-20261009-01` through `TH-20261009-39` as its claim IDs.
- This records **one narrative source**, not 39 independent measurements or 39 distinct witnesses. Preserve individual original-photo provenance edges in parallel.
- Audit finding: the previous narrative backlink list contained only TH-25..29; the other 34 statements were not lost.
- Review check: every listed claim must exist and point back to this narrative source; any mismatch blocks the gate. Check hashes and 39 original expert values independently.

## EO-02: historical intake versus current review
- Historical `intake_status`, `model_changed:false` and `canonical_data_updated:false` describe the intake event. They are **not** today's release or review status.
- Current state is indexed in [CURRENT-STATE.md](CURRENT-STATE.md); source/claim review remains property-scoped and must be recorded with reviewer and revision before promotion.
- `CAPTURED_UNREVIEWED → REVIEWED → ACCEPTED / DISPUTED / UNKNOWN` is a **proposed future property-state contract**, not a claim that existing JSON fields have migrated.
- `EXPERT_REVIEWED` topology does not imply `METRIC_VERIFIED` or `RELEASED`.

## EO-03: terminology alias
- Canonical component identity: `COMP-RADSTATT`.
- Historical/alternate spelling: `COMP-RADSTADT`, **alias of** `COMP-RADSTATT`, not a second structural component.
- This document records the mapping for review; no production alias resolver or component-ID migration is implemented here. Existing IDs and historical citations must remain valid.

## EO-05: derivation, not a new geometric fact
- TH-37 is a locally calculated 0.8 m datum in the candidate model; the audit notes the missing explicit mesh derivation tag.
- Record the derivation against the existing claim and model revision in a future narrowly scoped adapter; **do not invent a direct original-mesh observation** or change geometry to satisfy tag coverage.
- TH-20's 65 cm endpoint definition remains unresolved; TH-39 records scan availability, not a measured mesh.

## Preservation and review boundaries
- No original bytes, photo manifests, claim values, meshes, archived views, workflows, browser UX or model generators are intentionally changed by this contract.
- F02 (48/48 nail centerline intersections) and F03 (stationary supports) remain engineering NO-GO.
- Video source transfer, physical field backup, UX R1/R4 and CI repairs are separately gated.
- Source: [PR #16 audit](https://github.com/jdistlr/kleines-schaeferrad/pull/16), especially EVIDENCE-ONTOLOGY-DELTA and STABILIZATION-ROADMAP at commit `129a9a9`.

## Required evidence before gate
1. Read-back and exact membership check of 39 narrative IDs.
2. Reverse-link check against the actual canonical claim data.
3. Preservation comparison of all 39 expert values and referenced original hashes.
4. CI results for this branch at its final HEAD.
5. Independent review of alias and TH-37 semantics.

Until those are verified, this packet is **REVIEW IN PROGRESS**, not `STATE & SOURCE CONTRACT REVIEW READY`.
