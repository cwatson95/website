# 6.5 — Conservation of Mass Flow

Foundational module of **Topic 6 (Processes & Idealizations)** — the bookkeeping every
control-volume analysis starts from.

- **Builds on:** `1.x` (control volume, specific volume `v`), one-dimensional flow.
- **Feeds into:** `6.4` (steady-state energy balance reuses `Σṁi=Σṁe`), and every flow
  device in Topics 7–9 (turbines, compressors, nozzles, heat exchangers, cycles).

## Scope
The **mass rate balance** says mass in a control volume changes only by what flows in
minus what flows out [Moran Eq. 4.2]. The toolkit:

| use | relation | `code/mass_conservation.py` |
|-----|----------|------------------------------|
| mass flow rate (specific vol.) | `ṁ = AV/v` | `mass_flow_rate` |
| mass flow rate (density) | `ṁ = ρAV` | `mass_flow_rate_rho` |
| from volumetric flow | `ṁ = (AV)/v` | `mdot_from_volumetric` |
| invert for velocity | `V = ṁv/A` | `velocity_from_mdot` |
| **mass rate balance** | `dm_cv/dt = Σṁi − Σṁe` | `dmcv_dt` |
| steady-state check | `Σṁi = Σṁe` | `steady_mass_residual`, `is_steady_mass` |

**Key idea:** `ṁ = ρAV = AV/v` (Eqs 4.4a/4.4b) couples geometry (`A`), kinematics (`V`),
and state (`v`); at **steady state** `dm_cv/dt = 0`, so total mass in equals total mass
out (Eq 4.6) — but steady state and one-dimensional flow are *independent* idealizations.

## Run
```bash
cd code && python3 mass_conservation.py    # Ex 4.1 feedwater heater, Ex 4.2 barrel
python3 test_mass_conservation.py          # "All 13 tests passed."
```

## Files
`notes.md`, `code/mass_conservation.py`, `code/test_mass_conservation.py`, `problems/problems.md`, `refs.md`.
