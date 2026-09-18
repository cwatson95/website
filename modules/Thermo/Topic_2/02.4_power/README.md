# 2.4 — Power

Topic 2 (*Energy & Work*) module; see `modules/Thermo/list.txt`.

- **Builds on:** `2.1` work (power is its time-rate).
- **Feeds into:** steady-state device analysis (`1.1`, `6.4`), turbines/compressors
  (`8`), and the cycles in group `9` (rated in kW).

## Scope
Power is the **rate of energy transfer by work**, `Ẇ = δW/dt` (Moran §2.2.2). Each
work mode of `2.1` has a power:

| | expression | `code/power.py` |
|---|-----------|-----------------|
| force on a moving point | `Ẇ = F·V` | `power_force_velocity` |
| rotating shaft | `Ẇ = τ ω` | `shaft_power` |
| electrical | `Ẇ = V I` | `electric_power` |
| from work / to energy | `Ẇ = W/dt`, `W = Ẇ·dt` | `power_from_work`, `energy_from_power` |

`rpm_to_rad_s` converts shaft speed. Same sign convention (`Ẇ>0` out).

## Run
```bash
cd code && python3 power.py          # one of each
python3 test_power.py                # "All 7 tests passed."
```

## Files
`notes.md`, `code/power.py`, `code/test_power.py`, `problems/problems.md`, `refs.md`.
