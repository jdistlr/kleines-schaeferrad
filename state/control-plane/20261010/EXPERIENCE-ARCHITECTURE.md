# ADR — Model Control Plane vertical slice

Baseline: `606908bfe8cf1ab0560b337f37d92dd90d320dee`, PR #17. Reference: PR #16 at `129a9a9`, especially its UX-CONTROL-PLANE-BRIEF. This new mandate supersedes the earlier narrow R1/R4 scope; it does not merge the audit branch. No reconstruction or F02/F03 changes.

## Product decision

Add an isolated `/control/` workspace to the existing static application. Five connected workspaces share navigation and validated component/property URL context. Overview, Water and Evidence are new routes. Construction and Field use the existing working tools with a reciprocal navigation bridge. The historical entry and existing URLs remain available. This is an incremental app architecture, not five independent dashboards.

The user explicitly removed the requirement to preserve MUX colours/grammar during this session. The control-plane visual grammar is therefore independent: graphite navigation, cool neutral surfaces, water blue for interaction, restrained amber for explicit unknowns. Typography remains locally hosted Manrope because its legibility and weights fit the new layout; this is a design choice, not a MUX obligation. Historical identity comes from originals, local names and source provenance. No invented visual metrics or truth lights.

## Why keep Astro

Astro already compiles the evidence/claim contracts at build time, provides subpath-safe static routes, local fonts and offline assets. The existing stateful viewers and IndexedDB tools are plain client modules. A framework replacement would duplicate tested persistence and introduce migration risk without improving this slice. Route transitions are normal page navigation; URL context plus existing IndexedDB drafts provide continuity. A persistent app shell is a future decision only if observed switching latency warrants it.

## Information and interaction architecture

| Area | Primary job | Contract / next action |
| --- | --- | --- |
| Overview | Understand current revision and next question | ITER-003 from calibration JSON, real count of TH statements, property-specific limitations; enter water/model/field |
| Water & Hydraulics | Compare the functional water path with missing observations | TASK-WATER / GAP-07; same calibratedCycle as viewer, loaded on request; synthetic water/rpm transfer |
| Construction & Digital Twin | Inspect the selected family and its open property | Existing viewer/inspector/capture; Truth/Brute unchanged; synthetic variants progressively disclosed |
| Evidence & Knowledge | Read claims with source and scope | Existing claims rendered directly; original Torsten annotation and PR #17 clarification remain distinct from metric verification |
| Field Capture | Capture one task and preserve original bytes | Existing 21 tasks/order and v1 store; sketch before inputs; current step encoded for reload/return |

Navigation context is deliberately not evidence: `part`, `property`, `from`, `task`, `step` never become a new metric claim. Unknown IDs are rejected; historical Radstadt resolves to Radstatt for navigation only. Existing sources/IDs are not migrated. Workbench navigation refuses to reassign an unfinished draft silently. Normal in-app exits await the existing write queue.

## Hydraulics boundary

The SVG is a nonmetric functional diagram, not new reconstruction geometry. It distinguishes river flow below the wheel from lifted water entering trough and channel. The interactive phase result calls the existing ITER-003 `calibratedCycle` module; no parallel formula or second geometry model. Waterline/rpm ranges equal existing viewer controls. No automatic animation, no inferred discharge quantity, no CFD claim. Its parameter handoff selects operation view and leaves play stopped. F02/F03 remain engineering NO-GO.

## Technical boundaries

No backend, account system, data migration, auto-promotion or new engineering release. Original photos/claims/models remain byte-preserved. TH-37 uses Torsten's later endpoint clarification while preserving the old canonical record and model. Missing archive videos are labelled unavailable, not implied present. All state writes remain in the pre-existing stores.

## Reflection: evidence sufficiency and model update decisions

The follow-up request asks whether accumulated evidence is sufficient to update the models and support complete technical drawings. Source quantity cannot answer this. A part can have expert-confirmed topology while dimensions, tolerances, partner fits and material properties remain open. The UI therefore names the modes “Quellenbasierte Teilgeometrie” and “Rekonstruktionskandidat”; internal truth/brute identifiers remain compatible.

The inspector adds an explicitly limited read adapter: claim → source class and metric limit → existing model input where mapped → missing evidence → existing capture goal. TH-25…29 are mapped to existing reconstruction-constraint inputs. Equality of a number is not a mesh verification or acceptance. Other claims explicitly show that property-level model mapping is absent; no green completeness label is inferred.

A follow-on model delta review should classify each incoming source as supporting, contradicting, clarifying or outside the current property contract, identify affected model inputs, and propose a bounded update only where justified. Geometry changes remain outside this slice. “Absolute knowledge” is not a measurable acceptance gate; use purpose-scoped completeness for documentation, fabrication, assembly and operation separately, with revision, reviewer, uncertainty and unresolved dependencies. No overall readiness percentage is justified without such a reviewed requirement set.
