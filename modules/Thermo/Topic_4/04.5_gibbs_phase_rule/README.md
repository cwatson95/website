# 4.5 — Gibbs phase rule

Module of **Topic 4 (Properties & State Functions)**.

- **Builds on:** `4.1` (enthalpy), `4.2` (entropy) — the rule rests on the Gibbs
  function `g = h − Ts` and chemical potential.
- **Feeds into:** `4.4` (it explains *why* quality is needed in the vapor dome),
  combustion / chemical equilibrium (Topic 12).

## Scope
For a nonreacting equilibrium system with `N` components in `P` phases, the number of
intensive properties you may independently specify is

> **`F = 2 + N − P`**  (Moran Eq. 14.68; classic form `F = C − P + 2`).

| case | `code/gibbs_phase_rule.py` |
|------|----------------------------|
| general `F = 2+N−P` | `gibbs_phase_rule(N, P)` |
| single component `F = 3−P` | `single_component_dof(P)` |
| max coexisting phases `P = N+2` | `max_phases(N)` |

**Why it matters here:** a pure substance in the two-phase dome has `N=1, P=2 → F=1`,
so `T` and `p` are *dependent* — which is exactly why the **quality** `x` is needed as
the second property (`4.4`). A pure substance's triple point has `F=0` (fully fixed);
at most 3 phases can coexist.

## Run
```bash
cd code && python3 gibbs_phase_rule.py    # F for vapor, two-phase, triple point, mixtures
python3 test_gibbs_phase_rule.py          # "All 17 tests passed."
```

## Files
`notes.md`, `code/gibbs_phase_rule.py`, `code/test_gibbs_phase_rule.py`, `problems/problems.md`, `refs.md`.
