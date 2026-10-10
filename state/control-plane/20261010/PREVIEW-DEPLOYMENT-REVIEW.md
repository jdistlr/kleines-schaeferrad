# MODEL CONTROL PLANE PREVIEW DEPLOYMENT READY

Verified 2026-10-10. PR #18 remains open and unmerged.

## Published review

- [Control Plane](https://jdistlr.github.io/kleines-schaeferrad/review/pr-18/control/)
- [Water dashboard](https://jdistlr.github.io/kleines-schaeferrad/review/pr-18/control/water/)
- [3D viewer](https://jdistlr.github.io/kleines-schaeferrad/review/pr-18/werkstatt/)
- [Evidence](https://jdistlr.github.io/kleines-schaeferrad/review/pr-18/control/evidence/)
- [Field capture](https://jdistlr.github.io/kleines-schaeferrad/review/pr-18/feld/)

## Exact provenance

| Item | Value |
| --- | --- |
| Published and browser-tested application | `c1efd63b66ccb8d9c620f92d2cbbbcd3cbdd5656` |
| Original reviewed application | `51221b9d0e6ad8aed1fb714f7888f1a38bf0e3c5` |
| Original review evidence | `c190647b7fee3ff413c30e0f136b1882d47c7a14` |
| Main infrastructure-only commit | `feb8cd78c70f5966093cf457b27577a677be8134` |
| Preserved production application | `606908bfe8cf1ab0560b337f37d92dd90d320dee` |
| Deployment and live-browser run | [38044650865](https://github.com/jdistlr/kleines-schaeferrad/actions/runs/38044650865) |
| Isolated preflight | [38044428910](https://github.com/jdistlr/kleines-schaeferrad/actions/runs/38044428910) |
| Existing Control Plane acceptance | [38044428920](https://github.com/jdistlr/kleines-schaeferrad/actions/runs/38044428920) |
| Existing field/viewer journeys | [38044428975](https://github.com/jdistlr/kleines-schaeferrad/actions/runs/38044428975) |
| PR build, deployment skipped | [38044429002](https://github.com/jdistlr/kleines-schaeferrad/actions/runs/38044429002) |

The Pages deployment succeeded at 10:25 UTC; the subsequent live-browser gate passed. The evidence-only commit containing this report is not a new deployed application revision. Main changed only `.github/workflows/pages.yml`; PR #18 was not merged. As explicitly authorized after the initial blocker, the single Pages site was republished as a combined package: original production bytes plus the isolated preview subtree. This is not a separate GitHub Pages site.

## Results

- All **195 original production files** match their original SHA-256 hashes, both before and after publication. Composition verifies the same invariant.
- Live Chromium acceptance: five display profiles (desktop, tablet, phone390, phone320, text200), six routes, navigation/deep links, context and step resume, keyboard and reduced motion passed without reported browser errors.
- Water → viewer → field → model → field → control → field passed; simulation context is transferred and playback remains stopped by default.
- Export/import preserves original v1 bytes; tampered hashes and conflicting responses rejected; draft protection passed.
- Original production service worker installed before preview: original session unchanged, preview session separate, preview worker scoped to its subtree, offline reload passed. Reinstallation of the original parent worker preserves the preview cache.
- Preview databases and cache names are independently namespaced. No user production data migration, deletion or cache clearing occurs.
- Astro check, 40 Node tests, evidence checks and preservation passed. All 39 source statements and 21 tasks preserved. No reconstruction, geometry, F02/F03 correction or UX iteration was introduced for deployment.

## Permanent evidence

[Live isolation and production hashes](preview-evidence/live/pages-preview-live/results.json) · [Live complete acceptance](preview-evidence/live/pages-preview-live/acceptance/results.json) · [Production before publication](preview-evidence/live/pages-preview/production-live-before.json) · [Production file manifest](preview-evidence/live/pages-preview/production-sha256.json) · [Composition](preview-evidence/live/pages-preview/composition.json) · [Preflight](preview-evidence/preflight/pages-preview/results.json).

Mobile screenshots from the published URL: [water](preview-evidence/live/water-phone.png), [viewer](preview-evidence/live/viewer-phone.png), [field](preview-evidence/live/field-phone.png).

Live evidence artifact `11666612322` was verified directly from freshly downloaded archive bytes against SHA-256 `232b2884ad8ae9d8bcaefec4965d43bed0f2dbfef0fbcf8046cbbdbd3996ebc2`; the selected committed JSONs and screenshots match the archive entries byte-for-byte. [Verification manifest](preview-evidence/live/archive-verification.json). Full transient Actions artifacts expire; these selected reports and screenshots are committed permanently.

## Operations and limitations

- [Deployment decision and isolation details](PREVIEW-DEPLOYMENT-DECISION.md) supersede the earlier blocker.
- Physical iPhone/Safari, OS Dynamic Type and real device storage pressure remain **unverified**. The public HTTPS URL can be opened directly on an iPhone; phone-width tests here used Chromium, not iOS.
- Same-origin paths are not a security boundary. Isolation is operational (worker scope and namespaced stores), not protection against hostile code on the same origin.
- Production application is deliberately frozen at the original artifact. Future main source changes do not automatically replace it while this temporary workflow remains installed.
- Baseline archive is retained in Actions for 90 days and refreshed by successful workflow runs. Current backup artifact: `11667671706`, expiry `2027-01-08T10:22:07Z`. This is not permanent backup: if all copies expire the workflow fails closed until the exact verified archive is restored.
- Manual rollback: dispatch the Pages workflow on main with `rollback=true`. It publishes the hash-verified original baseline only, without depending on preview build health. Already cached browser content is not remotely erased.
- Existing large offline payload/viewer chunk remain. Field data stays local to this preview; export before any later host migration.
- No server, hosting account, deployment API, framework migration or new UX was added.
