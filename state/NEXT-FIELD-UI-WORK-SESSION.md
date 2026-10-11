> **Abgelöst am 11.10.2026.** Diese Datei ist kein Arbeitsauftrag mehr. Maßgeblich sind [AGENTS.md](../AGENTS.md), der [Wissenskern](../kern/README.md) und der [Ordnungsplan](../docs/ordnung/PLAN.md). Neue Fachangaben nicht hier anhängen, sondern wie in AGENTS.md beschrieben in `kern/` eintragen.

# Next Field UI Work Session — Evidence Capture Reliability

Base: main after PR #8. Do not start ITER-002.

Mission: support real capture on 09–10 October 2026. Do not reimplement existing field tasks, change existing task IDs/order or claim browser acceptance without real execution.

1. Read truth-critic/GATE.md, CAPTURE-PLAN.md, the existing Field Mode and PDF outputs.
2. Validate published Pages route, deployment and real-device behavior; record observed results and blockers.
3. Improve field UI incrementally: time-window entry screen (before shutdown, before removal, during exposure, before departure); clear hold-point cards and offline fallback; capture of object/partner IDs, before/after, multiple measurements with units and source photo references; export/restore integrity.
4. Preserve all existing IndexedDB drafts and task identifiers. No migration without explicit backwards-compatibility tests.
5. Add focused tests, verify on 320px and mobile Safari if physically available; never substitute emulator for physical acceptance.
6. Preserve evidence authority and unreviewed state. No new geometry, scan transforms or model truth promotion.
7. Work in a separate PR, no automatic merge. Stop at FIELD UI CAPTURE RELIABILITY REVIEW READY.
