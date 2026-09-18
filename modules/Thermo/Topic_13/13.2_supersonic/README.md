# 13.2 — Supersonic Compressible Flow (M > 1)

Module 2 of **Topic 13 (Compressible Flow & Gas Dynamics)**.

- **Builds on:** `13.1` (speed of sound, Mach number, stagnation ratios, area–velocity
  relation Eq. 9.45).
- **Feeds into:** `13.3` (a normal shock can stand in the supersonic diverging section).

## Scope
A flow is **supersonic** when `M = V/c > 1`. The area–velocity relation
`dA/A = −(dV/V)(1−M²)` flips sign past `M=1`, so the converging–diverging (C–D) nozzle
and choking enter:

| use | relation | `code/supersonic.py` |
|-----|----------|--------------------|
| area–Mach relation | `A/A* = (1/M)[(2/(k+1))(1+(k−1)/2·M²)]^((k+1)/(2(k−1)))` | `area_mach_ratio` |
| critical (sonic) ratios | `p*/po = (2/(k+1))^(k/(k−1))`, `T*/To = 2/(k+1)` | `critical_pressure_ratio`, `critical_temperature_ratio` |
| choking test | converging nozzle choked when `pB ≤ p*` | `is_choked` |
| invert `p/po → M` | `M = √(2/(k−1)[(po/p)^((k−1)/k)−1])` | `mach_from_pressure_ratio` |
| invert `A/A* → M` | two roots (sub/supersonic) | `mach_from_area_ratio` |

**Key idea:** for `M > 1`, `(1−M²) < 0`, so area and velocity move *together* — a
supersonic flow **accelerates in a diverging** duct (case 2) and **decelerates in a
converging** duct (case 3). `M=1` occurs only at the **throat** (minimum area); reaching
supersonic speed needs a **converging–diverging** nozzle [Moran Sec. 9.13.1].

## Run
```bash
cd code && python3 supersonic.py        # Ex 9.14(a) choking + Ex 9.15(c) supersonic exit
python3 test_supersonic.py              # "All 19 tests passed."
```

## Files
`notes.md`, `code/supersonic.py`, `code/test_supersonic.py`, `problems/problems.md`, `refs.md`.
