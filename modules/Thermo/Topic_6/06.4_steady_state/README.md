# 6.4 — Steady-State Operation

Keystone modeling idealization of **Topic 6 (Processes & Idealizations)** — the
assumption behind almost every flow-device analysis.

- **Builds on:** `6.5` (mass rate balance; steady `Σṁi=Σṁe`), first law / energy
  transport, enthalpy `h`.
- **Feeds into:** turbines, compressors, pumps, nozzles, heat exchangers, throttles
  (Topic 7) and every power/refrigeration cycle (Topics 8–9).

## Scope
At **steady state** nothing accumulates: the storage terms vanish, `dm_cv/dt = 0` and
`dE_cv/dt = 0` [Moran §4.5.1]. The toolkit:

| use | relation | `code/steady_state.py` |
|-----|----------|-------------------------|
| steady mass | `Σṁi = Σṁe` | `steady_mass_residual`, `is_steady` |
| spec. KE change | `(V₂²−V₁²)/2` | `delta_ke` |
| **energy balance → Q̇** | `Q̇=Ẇ+ṁ[(h₂−h₁)+ΔKE+ΔPE]` | `heat_rate_steady` |
| **energy balance → Ẇ** | `Ẇ=Q̇+ṁ[(h₁−h₂)+ΔKE+ΔPE]` | `power_rate_steady` |
| adiabatic turbine | `Ẇ=ṁ(h₁−h₂)` | `turbine_power_adiabatic` |

**Key idea:** with `dE_cv/dt = 0`, the one-inlet/one-exit **steady-state energy rate
balance** (Eq 4.20a) relates only boundary transfers `Q̇`, `Ẇ` to the inlet→exit changes
in `h`, KE, PE — no interior detail is needed. KE/PE are usually small next to `Δh`.

## Run
```bash
cd code && python3 steady_state.py     # Ex 4.4 steam turbine, Q̇cv = -62.3 kW
python3 test_steady_state.py           # "All 12 tests passed."
```

## Files
`notes.md`, `code/steady_state.py`, `code/test_steady_state.py`, `problems/problems.md`, `refs.md`.
