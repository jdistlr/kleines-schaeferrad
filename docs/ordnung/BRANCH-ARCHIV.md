# Branch-Archiv

Stand: 11.10.2026. 22 abgeschlossene Arbeitsbranches werden vom Repository entfernt. **Jeder davon ist vollständig in `main` enthalten** (geprüft am 11.10.2026). Es geht also kein Commit verloren; die Branches sind nur noch Namen für längst übernommene Arbeit.

Löschen in einem Schritt (lokal, mit Schreibrechten):

```
git push origin --delete $(grep -o '^| `[^`]*`' docs/ordnung/BRANCH-ARCHIV.md | tr -d '|` ')
```

Die Tabelle hält jeden Namen mit seinem letzten Commit fest. Ein Branch lässt sich jederzeit wiederherstellen:

```
git push origin <commit>:refs/heads/<branch>
```

Bei Branches mit Pull Request geht es auch über die Schaltfläche „Restore branch“ im jeweiligen PR auf GitHub.

| Branch | Letzter Commit | Datum | Pull Request | Thema |
|---|---|---|---|---|
| `work/github-pages-research-view-20261007` | `dd0cd480a4f5` | 07.10.2026 | – | state: prepare Astra field workbench alpha session |
| `work/pre-disassembly-baseline-20261007` | `dd0cd480a4f5` | 07.10.2026 | – | state: prepare Astra field workbench alpha session |
| `work/field-workbench-alpha-20261007` | `ba6d5d131c43` | 07.10.2026 | #1 | Field Reconstruction Workbench Alpha |
| `work/pre-disassembly-field-kit-20261007` | `d4ef4deb6946` | 07.10.2026 | #2 | Pre-disassembly field kit & MUX UX refinement |
| `work/maintenance-coherence-20261007` | `c709495a817c` | 08.10.2026 | #3 | Maintenance rebuild: coherent UX, visual field guidance, full system context |
| `work/bruteforce-functional-reconstruction-v2-20261008` | `395796a2edad` | 08.10.2026 | #4 | Astra V2: brute-force functional reconstruction & UX recovery |
| `work/baseline-refresh-thorsten-20261008` | `f73ec596f809` | 08.10.2026 | #6 | Baseline V3: Thorsten-Fachwissen in Truth Model übernehmen |
| `work/model-calibration-loop-v3-20261008` | `3b34eebaafc2` | 08.10.2026 | #7 | ITER-001: Baseline V3 model calibration loop |
| `work/iter-001-truth-critic-evidence-gate-20261009` | `6060bc1e81ce` | 09.10.2026 | #8 | ITER-001: Independent Truth Critic & Pre-Disassembly Evidence Gate |
| `work/field-operations-handoff-20261009` | `b3d319ffccc9` | 09.10.2026 | #9 | Field operations handoff: Thorsten Friday, disassembly Saturday, UI follow-up |
| `work/ux-audit-semantic-contract-20261009` | `2c75dbc3afee` | 09.10.2026 | #10 | UX recovery: independent visual audit and P1 plan — review ready |
| `work/astra-abgleich-iter002-20261009` | `6017ba310d4a` | 09.10.2026 | – | docs: complete ITER-002 Astra evidence comparison |
| `work/astra-korrektur-iter003-20261009` | `6999e93146d2` | 09.10.2026 | – | feat: reconcile expert constraints and model geometry in ITER-003 |
| `work/iter003-truth-critic-20261009` | `05b54353211b` | 09.10.2026 | #14 | ITER-003 Truth Critic & Integration Audit — NO-GO |
| `work/iter003-integration-recovery-20261009` | `6a1986864781` | 09.10.2026 | #15 | ITER-003 integration recovery: drawing build, canonical backlinks, provenance |
| `work/holistic-stabilization-audit-20261009` | `129a9a931ec9` | 10.10.2026 | #16 | Holistic stabilization audit — CONDITIONAL GO / review ready |
| `work/state-source-contract-20261010` | `fc6da1a02065` | 10.10.2026 | #17 | Stabilization P0-A/P1-A — state and source contract |
| `work/model-control-plane-20261010` | `c31bf8ae5cdc` | 10.10.2026 | #18 | Model Control Plane: experience architecture and functional vertical slice |
| `design/lab-ordnung-entwurf-20261010` | `704c114a2ba0` | 10.10.2026 | #19 | Entwurf: Laborordnung und exemplarische Wellen-Fallakte |
| `work/evidence-graph-consolidation-20261010` | `3590827705a2` | 10.10.2026 | #20 | Wissenslabor: Referenzbasis und lesende Laboransicht |
| `work/ux-recovery-r1-r4-plan-20261009` | `7e7da93d7b9a` | 11.10.2026 | #11 | Stage UX recovery R1/R4 with field-safe release gate |
| `work/archive-video-evidence-intake-20261009` | `33d2ca394fb4` | 11.10.2026 | #12 | Archive video evidence: timecoded intake and Thorsten capture delta |

## Ab jetzt

- `main` ist der einzige dauerhafte Arbeitsbranch. Daneben gibt es `gh-pages`: Er enthält nur die veröffentlichte Cockpit-Seite, wird ausschließlich von `npm run cockpit:pages` geschrieben und nie gemergt.
- Arbeit läuft in kurzlebigen Branches mit Präfix nach Zweck: `ordnung/`, `kern/`, `modell/`, `cockpit/`, `befund/`. Datum am Ende.
- Jeder Branch endet in einem Pull Request; nach dem Merge löscht GitHub ihn automatisch. Dafür in den Repository-Einstellungen unter *General → Pull Requests* „Automatically delete head branches“ einschalten.
- Höchstens ein offener Branch pro Thema. Aufeinander aufbauende PRs nennen ihre Basis in der Beschreibung.

Thorstens Fork `ThorstenHalsch/kleines-schaeferrad` hat ebenfalls fünf Branches, die alle vollständig in `main` enthalten sind. Sie liegen in seinem Repository; aufräumen kann nur er.
