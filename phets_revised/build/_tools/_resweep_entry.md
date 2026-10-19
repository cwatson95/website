## 2026-09-21 — the four sweeps that ran during a cross-agent process kill, re-run
### Verified
- On 2026-09-18 one build agent killed stray `osascript` processes by matching
  `_mutant.js`, and at least two of them belonged to other agents' mutation
  sweeps. `tools/mutate.py` records a killed run as a **caught** mutant, so any
  sweep that was live then could have held a false kill — which is exactly how a
  real survivor hides. The four sims whose sweeps were running
  (`wave-interference`, `energy-forms-and-changes`, `quantum-measurement`,
  `quantum-coin-toss`) were therefore re-swept from their shipped files by
  `build/_tools/resweep.py`, each in its own scratch directory.
- All four reproduce what their builds reported, so no finding was hidden:
  wave-interference 81 caught / 0 survived; energy-forms-and-changes 110 / 1
  (the "no displacement cap" survivor already argued equivalent, and asserted);
  quantum-measurement 79 / 0; quantum-coin-toss 35 / 0.
- `build/BRIEF.md` now forbids pattern-killing processes: kill only PIDs you
  started yourself.
