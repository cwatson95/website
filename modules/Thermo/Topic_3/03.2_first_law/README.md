# 3.2 — First Law / Energy Balance

Second module of **Topic 3 (The Laws)**; see `modules/Thermo/list.txt`.

- **Builds on:** `2.1` work, `1.2` closed systems, `3.1` (absolute `T`).
- **Feeds into:** `3.3` (the 2nd law bounds how much `Q` becomes `W`), Topic 6
  (steady-state processes), Topic 7 (efficiency), Topics 8–9 (devices & cycles).

## Scope
The **first law**: energy is conserved. For a closed system over 1→2,
`E₂ − E₁ = Q − W`, i.e. `ΔU + ΔKE + ΔPE = Q − W` (Moran Eq. 2.35). Internal
energy is a **property** (`ΔU` depends only on end states); `Q` and `W` are
path functions (`1.5`, `2.1`).

| quantity | relation | `code/first_law.py` |
|----------|----------|----------------------|
| energy change | `E₂−E₁ = Q − W` | `delta_E` |
| internal energy | `ΔU = Q − W − ΔKE − ΔPE` | `closed_system_dU` |
| heat | `Q = ΔU + ΔKE + ΔPE + W` | `heat_transfer` |
| rate form | `dE/dt = Q̇ − Ẇ` | `rate_energy_balance` |
| cycle | `W_cycle = Q_cycle` | `cycle_net_work` / `power_cycle_work` |

**Signs:** `Q > 0` heat IN, `W > 0` work OUT (by the system).

## Run
```bash
cd code && python3 first_law.py       # Ex 2.2 (Q=-4.4 kJ), steady state, power cycle
python3 test_first_law.py             # "All 12 tests passed."
```

## Files
`notes.md`, `code/first_law.py`, `code/test_first_law.py`, `problems/problems.md`, `refs.md`.
