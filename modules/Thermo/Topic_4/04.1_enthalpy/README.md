# 4.1 — Enthalpy

First module of **Topic 4 (Properties & State Functions)**.

- **Builds on:** `1.3`/`1.4` (properties), `3.2` (first law / `U`), `2.1` (work `pV`).
- **Feeds into:** `4.2` (the 2nd T dS equation uses `h`), `4.3` (exergy's `pV` term),
  control volumes & devices (Topics 6, 8), and every cycle (Topic 9).

## Scope
The recurring combination `U + pV` is named **enthalpy** `H`; per unit mass
`h = u + pv` (Moran Eq. 3.4). Two payoffs:

| use | relation | `code/enthalpy.py` |
|-----|----------|---------------------|
| definition | `h = u + pv` (`H = U + pV`) | `enthalpy` / `enthalpy_total` |
| constant-p heat | `Q = m(h₂−h₁) = ΔH` | `const_pressure_heat` |
| two-phase | `h = hf + x·hfg`, `u = uf + x·ufg` | `enthalpy_from_quality` |
| find quality | `x = (h−hf)/hfg` | `quality_from_enthalpy` |

**Why `h`:** at constant pressure `Q = ΔU + pΔV = Δ(U+pV) = ΔH`, so enthalpy is the
"heat content" for constant-pressure heating (and the energy carried by flowing
mass — Topic 6). At constant *volume* there is no boundary work and `Q = ΔU` instead.

## Run
```bash
cd code && python3 enthalpy.py        # h=u+pv anchor, two-phase h, const-p heat
python3 test_enthalpy.py              # "All 9 tests passed."
```

## Files
`notes.md`, `code/enthalpy.py`, `code/test_enthalpy.py`, `problems/problems.md`, `refs.md`.
