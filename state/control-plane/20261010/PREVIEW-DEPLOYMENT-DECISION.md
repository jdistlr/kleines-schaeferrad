# Pages combined deployment — authorized 2026-10-10

The earlier blocker is superseded by the user's explicit approval to republish the Pages package while preserving all existing production files and adding PR #18 under `/kleines-schaeferrad/review/pr-18/`. PR #18 must remain unmerged. A narrowly scoped main deployment workflow update is authorized. No geometry or factual correction changes are authorized.

## Frozen production

Original production: commit `606908bfe8cf1ab0560b337f37d92dd90d320dee`, Actions run `38033011709`, artifact `11662297630`. The downloaded ZIP contains `artifact.tar`, SHA-256 `9a31ad078b177153348e4d5ce0915f83c1d60d97f17abba00fec816bd58e4f5f`.

The combined package copies 195 original files unchanged and adds a previously absent `review/pr-18` directory. No rebuilt production file is substituted. File hashes are checked after composition, against live production before publishing, and against live production after publishing. The baseline archive is re-uploaded with 90-day retention; it is not permanent storage. If all retained copies expire, deployment must fail closed until the exact verified archive is restored. A local downloaded copy also exists during this work session, but is not durable storage.

While this temporary workflow is installed, main source changes do NOT automatically become new production application builds: production is deliberately frozen. A future production release must explicitly replace this policy and decide whether to retain the preview. Rollback publishes the verified baseline alone. Preview removal may still leave browser-cached copies until their service workers/caches are removed; rollback is not remote deletion of browser data.

## Preview isolation

Preview base: `/kleines-schaeferrad/review/pr-18/`. IndexedDB names: `ks-preview-pr18-pre-disassembly` and `ks-preview-pr18-field-workbench`. Cache prefix: `ks-preview-pr18-cache-` (deliberately NOT `ks-field-`). The preview worker has its own subtree scope and deletes only its own cache prefix. Manifest paths use the same base.

No automatic copying or migration of production field records occurs. The v1 schemas, import/export and storage operations remain unchanged; preservation checks normalize only the explicitly authorized database-name selection lines. Production workers and data are not unregistered, deleted or changed in user browsers.

Same-origin paths are not a security boundary. A previously installed parent worker may handle the first preview navigation; the original parent worker fetches cache misses from the network. Tests install the real original parent worker first, exercise preview storage and offline navigation, then reinstall the original parent worker to test cache cleanup in the reverse order. Browser tests use fresh synthetic contexts, never a user's existing field records.

## Validation policy

Local build and all 40 Node tests passed during preparation. Local browser startup was denied by the execution environment (socket permission), so GitHub Actions must run the browser gates before publication. The final remote gate reuses the full existing Control Plane acceptance suite against the actual HTTPS preview URL and separately verifies production byte preservation and storage isolation. Physical iPhone/Safari testing is not claimed.

Status at creation of this decision: preparation; no preview published yet. Final deployment IDs, pinned source commit, result and remaining limits must be appended to the PR after the live gate.
