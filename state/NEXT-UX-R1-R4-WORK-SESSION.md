# Next UX Work Session — R1 and R4 implementation only

Base: main after PR #10 merge 36ea5c01d57ee1c0017f99941034a76adbe4790e.
Read: state/ux-recovery/20261009/AUDIT.md, RECOVERY-PLAN.md, GATE.md; docs/HUMAN-UX-QUALITY-CONTRACT.md.

## Scope
- R1: reveal urgent water capture, offer compact capture-window navigation using existing task IDs, make original-video and extra-paper-measurement fallback visible at relevant steps. Deep-link/reload return must preserve task and draft.
- R4: fix 200%-text hero collision via intrinsic wrapping, preserving current visual grammar.
- No R2 measurement schema migration, no R3 workbench redesign, no P2 backlog sweep, no geometry or model changes.
- Preserve task array indices and existing v1 saved records. No changes to source originals or expert authority.

## Timing and release
Real dismantling evidence capture is the operational priority. Implement on this isolated branch, not main. No automatic merge or production deployment until real capture is safely backed up and user reviews results. Current printed field kit/native camera remains fallback.

## Required verification
- Screenshot and interactions at 1440, 768, 390, 320 and 1280 with 200% text.
- R1: water capture in first meaningful view, at most two actions to TASK-WATER, all 21 task IDs and order unchanged, reload/deep-link preserves input step, no false video upload.
- R4: no headline/photo collision at 200% text, no horizontal overflow, keyboard focus intact.
- Existing workbench/field tests, Astro check/build, export/import/offline regression.
- If physical Safari or printer not available, mark as unverified, not passed.
- Document before/after screenshots and rollback, commit/push branch and open review PR. Stop at UX R1+R4 REVIEW READY.
