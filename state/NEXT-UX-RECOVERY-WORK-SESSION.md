> **Abgelöst am 11.10.2026.** Diese Datei ist kein Arbeitsauftrag mehr. Maßgeblich sind [AGENTS.md](../AGENTS.md), der [Wissenskern](../kern/README.md) und der [Ordnungsplan](../docs/ordnung/PLAN.md). Neue Fachangaben nicht hier anhängen, sondern wie in AGENTS.md beschrieben in `kern/` eintragen.

# NEXT WORK SESSION — UX Evidence-Driven Recovery

Starting point: main after PR #9; consult state/UX-RECOVERY-AUDIT-20261009.md, docs/SEMANTIC-RECONSTRUCTION-CONTRACT-DRAFT.md, docs/HUMAN-UX-QUALITY-CONTRACT.md, and the current Field/Workshop implementation.

Mission: independent screenshot/interaction audit first, then propose a small P1-only patch plan. Preserve original MUX design grammar. No new design direction, new app, geometry, ITER-002 or cinematic work.

1. Confirm current GitHub Pages deployment vs main.
2. Execute browser acceptance on desktop, 768, 390, 320, 200% text and reduced-motion; capture screenshots and reproducible findings. State clearly if a device or browser is unavailable.
3. Audit journeys: discover model, inspect Kumpf source and hypothesis, urgent field task, multiple measurements, original photo references, export/import and offline recovery.
4. Inspect print proofs and grayscale legibility of current A4/A3 PDFs. Check final files not just generator code.
5. Report defects ranked P0/P1/P2 with screenshots, user impact and minimum fixes. Never claim unexecuted checks passed.
6. Propose incremental UI improvements: Discover/Investigate/Document progressive disclosure; field capture-window navigation; partner IDs and before/after provenance; backward-compatible multiple measurements; review statuses.
7. Stop at UX RECOVERY PLAN REVIEW READY. Do not modify production UX until findings are reviewed. Do not merge automatically.

Separate future gate: once real demolition evidence has been secured and reviewed, implement small UX PRs. Semantic contract remains discussion draft.

## Completion checkpoint — 2026-10-09

Executed from PR #10 initial head `1ba1820`, production baseline `1de62e7`. Stop gate reached: **UX RECOVERY PLAN REVIEW READY**, verdict **CONDITIONAL GO for plan review only**. Results: [audit](ux-recovery/20261009/AUDIT.md), [P1 plan](ux-recovery/20261009/RECOVERY-PLAN.md), [evidence](ux-recovery/20261009/EVIDENCE.md), [gate](ux-recovery/20261009/GATE.md).

Do not restart this audit or interpret the checkpoint as implementation permission. Physical Safari/second-device/storage-pressure and daylight print acceptance remain explicit open gates. Review the proposed R1–R4 first. No production UX, geometry or merge performed.
