> **Aktueller Auftrag — 09.10.2026:** Zuerst [ASTRA-ABGLEICH-20261009.md](ASTRA-ABGLEICH-20261009.md) und den [neuen Fachbeitrag](../docs/FACHBEITRAG-KONSTRUKTION-20261009.md) lesen. Neue explizite Maße und Befestigungsbeschreibungen korrigieren die unten erhaltene historische ITER-001-Spezifikation. Die folgende abgeschlossene Iteration nicht erneut als aktuellen Auftrag starten.

# NEXT ASTRA WORK SESSION — Baseline V3 Model Calibration + Perfection Loop

Branch: `work/model-calibration-loop-v3-20261008`
Base: `main@558626019c6f85c6061467727f54122a793b15bd`

Status: **CALIBRATION ITERATION READY FOR TRUTH CRITIC**

Completed: `ITER-001` · 2026-10-08. Handoff: [CRITIQUE-READY.md](reconstruction-loop/ITER-001/CRITIQUE-READY.md). The task below is preserved as the iteration specification. No merge performed.

Read first:
- `state/baseline/BASELINE-V3-THORSTEN.md`
- `data/evidence-authority.json`
- `state/reconstruction-loop/PROTOCOL.md`
- `docs/reconstruction/SOURCE-RECONCILIATION.md`
- `evidence/contributions/kumpf-20261008.json`
- `evidence/contributions/schaufelstellung-20261008.json`
- `data/reconstruction-evidence-map.json`
- `data/assembly.graph.json`
- `data/kumpf-fastener-hypotheses.json`
- `data/knowledge-gaps.json`

Use the currently deployed V2 reconstruction as implementation starting point, but do not protect any geometry that conflicts with Baseline V3.

---

# Mission

Perform the first full **Truth Model ↔ Brute-Force Model calibration iteration** on Baseline V3.

The purpose is not merely to add Thorsten's notes into metadata.

You must:
1. materially correct the serious model where Baseline V3 now constrains it,
2. re-rank and rebuild the Brute-Force model around the new local expert knowledge,
3. deepen the geometry beyond V2 where the new evidence allows it,
4. regenerate technical views where geometry changes,
5. recalibrate water/operation where Kumpf or paddle geometry changes,
6. produce a canonical render package for a separate truth-critic session.

Stop only at:

# **CALIBRATION ITERATION READY FOR TRUTH CRITIC**

---

# A. Reconstruct the reference Kumpf at component level

The reference Kumpf is now a high-priority local construction source.

Mandatory baseline:
- 12 staves,
- 1 base,
- base retained in a groove / Einfräsung in the staves,
- 3 metal hoops,
- 2 drilled staves,
- 2 holes in each drilled stave,
- 2 Kumpfnägel: one long, one short,
- Kumpfnägel fasten the Kumpf to the Krümmling,
- neighboring Kümpfe overlap.

Use the four Thorsten reference photos:
- `evidence/raw/1000046420.jpg`
- `evidence/raw/1000046421.jpg`
- `evidence/raw/1000046422.jpg`
- `evidence/raw/1000046423.jpg`

Do not keep a generic barrel approximation if these images support a more faithful shape.

Extract as much as defensibly possible:
- stave count and angular spacing,
- external profile,
- taper if visible,
- base position,
- groove position,
- hoop positions,
- drilled-stave positions,
- likely hole spacing,
- local asymmetry.

Where scale readout is possible from visible rulers, record the measurement method and uncertainty.
Do not invent unreadable values.

Output:
- improved Truth candidate for the reference Kumpf,
- updated Brute-Force production Kumpf geometry,
- orthographic + section drawings,
- annotated source-photo comparison.

---

# B. Rebuild Kumpfnagel geometry and function

Previous V2 assumptions are no longer equal candidates.

Promote the local expert functional baseline:
- two Kumpfnägel,
- one long + one short,
- attachment through drilled staves to Krümmling,
- unequal length required by neighboring-Kumpf overlap.

Deprioritize:
- “long/short primarily sets tilt/twist”
unless new geometry independently requires it.

Model explicit candidate nail paths through:
- four hole positions,
- two drilled staves,
- Krümmling contact.

Generate several geometrically possible mappings if necessary.

Rank them by:
- source-photo compatibility,
- collision-free insertion,
- overlap compatibility,
- plausible withdrawal during dismantling,
- minimum unsupported assumptions.

Output:
- candidate A/B/C if still ambiguous,
- visible long/short mapping,
- exploded nail/stave/Krümmling detail,
- explicit list of what Saturday must decide.

---

# C. Model neighboring-Kumpf overlap as real topology

Do not treat each Kumpf as an isolated radial duplicate.

Create at least a 3-Kumpf local cluster.

Investigate:
- overlap direction,
- leading/trailing relation,
- long/short nail side,
- whether overlap implies a preferred circumferential assembly direction,
- relation to paddle position.

Keep multiple overlap orientations if current evidence does not determine direction.

Truth Model:
- overlap existence may be treated as local expert-supported topology.

Brute-Force Model:
- select and rank the best directed overlap candidate.

Output:
- 3-Kumpf cluster canonical render,
- exploded overlap view,
- candidate assembly sequence,
- field decision points.

---

# D. Resolve Thorsten's 90° paddle correction properly

This is a priority expert correction.

Do NOT simply rotate paddles by 90°.

First define the geometry:
- wheel/rim plane,
- shaft axis,
- local radial direction,
- local tangent,
- paddle board plane,
- paddle normal.

Then interpret “90° zum Rad” into explicit vector/plane relationships.

Use:
- current photos,
- existing PLY/GLB,
- any identifiable paddle region,
- V2 geometry,
- Thorsten narrative.

If the current code is mathematically perpendicular to the rim plane but visually/functionally still wrong, identify the actual mismatch:
- radial/tangential pitch,
- local rotation,
- axial position,
- front/back orientation,
- connection point,
- phase.

Generate a clear before/after comparison.

If scan evidence is insufficient:
- preserve expert correction as Truth constraint,
- keep exact angular implementation as ranked candidate,
- do not pretend verification.

Output:
- coordinate explanation,
- candidate orientation,
- photo/scan comparison,
- updated paddle technical drawing.

---

# E. Recalibrate the full Kumpf + paddle + rim assembly

After A–D, rebuild the circumference assembly.

Verify:
- Kumpf overlap does not collide,
- nail paths remain possible,
- paddles do not collide with Kümpfe / rims,
- correct partner relation to Krümmling,
- plausible assembly/disassembly path.

Do not assume 24 identical perfect copies if local evidence implies variants.
Retain a canonical repeated family plus variant capability.

---

# F. Recalibrate water function

Only after Kumpf and paddle corrections.

Re-evaluate:
- entry angle into water,
- Kumpf opening orientation,
- approximate fill window,
- lift path,
- retention,
- top discharge window,
- trough interception,
- paddle drag orientation.

This is still a functional visualization, not CFD.

But the animation must now be mechanically consistent with the updated geometry.

Generate:
- slow operating animation/view,
- one full Kumpf cycle,
- water pickup,
- lift,
- discharge into trough,
- trough/rinne continuation.

If a function depends on unresolved orientation, expose a parameter/candidate switch instead of hiding the uncertainty.

---

# G. Refine the serious Truth Model

Apply Baseline V3 changes to the evidence-constrained model.

The serious model should become visibly different from V2 where new evidence justifies it.

Mandatory:
- reference Kumpf structure,
- Kumpfnagel family,
- Kumpf→Krümmling relationship,
- overlap topology,
- paddle orientation constraint,
- updated source/provenance states.

Do not add cinematic site detail to Truth unless supported.

---

# H. Push the Brute-Force model further

After Truth calibration, use the improved constraints to increase synthetic completeness.

Improve where possible:
- all Kumpf instances,
- overlap rhythm,
- nail placement,
- paddle geometry,
- rim relationships,
- frame/contact plausibility,
- trough relation,
- water cycle,
- materials and wet/dry appearance,
- site/water integration,
- lighting and camera composition.

Target visual ambition:
**a convincing digital museum reconstruction of the wheel operating in the Regnitz**, while keeping synthetic status inspectable.

Do not trade mechanical clarity for cinematic appearance.

---

# I. Technical drawing refresh

Regenerate only from updated geometry.

Mandatory updated sheets/details:
- Kumpf section with 12 staves and base groove,
- drilled-stave / 4-hole diagram,
- long/short Kumpfnagel candidate paths,
- 3-Kumpf overlap view,
- Kumpf→Krümmling exploded detail,
- paddle orientation vector/plane diagram,
- Kumpf/paddle/rim local assembly,
- operating path around water/trough.

No primitive symbolic sketches.

Use:
- real-photo overlays when installed context matters,
- geometry-derived orthographic/section/exploded views when construction matters.

---

# J. Canonical render package

Produce all 16 canonical views from `state/reconstruction-loop/PROTOCOL.md`.

For every view:
- Truth Model render,
- Brute-Force render,
- same camera,
- component/status legend,
- iteration identifier.

Add special comparison plates:
1. V2 Kumpf vs Baseline V3 Kumpf
2. old nail hypothesis vs expert-reconciled nail candidates
3. V2 paddle vs corrected paddle candidate
4. isolated Kumpf vs 3-Kumpf overlap cluster
5. old operating cycle vs recalibrated operating cycle

---

# K. Adversarial pass

Before stopping, perform one internal adversarial pass.

Ask:
- Does any V2 assumption survive only because it was already coded?
- Does any external analogy override Thorsten without stronger local evidence?
- Is the Kumpf still too generic compared with the reference photos?
- Are four holes represented?
- Do two nails have a plausible path?
- Does overlap actually explain unequal nail length geometrically?
- Is the paddle visibly/functionally consistent with the expert correction?
- Does the water simulation still rely on the old Kumpf/paddle pose?
- Have any synthetic values accidentally entered Truth?

Correct P0/P1 issues that can be resolved from existing evidence.
Leave evidence-limited issues explicit.

---

# L. Iteration outputs

Write:
- `state/reconstruction-loop/ITER-001/ITERATION-REPORT.md`
- `state/reconstruction-loop/ITER-001/CONSTRAINT-DELTA.json`
- `state/reconstruction-loop/ITER-001/MODEL-DELTA.json`
- `state/reconstruction-loop/ITER-001/SCORECARD.json`
- `state/reconstruction-loop/ITER-001/CRITIQUE-READY.md`
- canonical render set
- updated Truth export
- updated Brute-Force export
- updated technical drawing contact sheet
- remaining Saturday-only questions

Do not merge automatically.

Stop at exactly:

# **CALIBRATION ITERATION READY FOR TRUTH CRITIC**
