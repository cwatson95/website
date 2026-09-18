# 13.3 — Normal Shock

Module 3 of **Topic 13 (Compressible Flow & Gas Dynamics)** — the capstone of the
Moran Ch.9 sequence.

- **Builds on:** `13.1` (stagnation ratios), `13.2` (supersonic flow in a C–D nozzle).
- **Feeds into:** the example/homework support modules (`13.EP`, `13.HP`).

## Scope
A **normal shock** is an abrupt, irreversible jump across a plane normal to a
**supersonic** stream: the flow goes from `Mx > 1` to `My < 1`, `p` and `T` rise,
entropy rises (`sy > sx`), stagnation pressure drops, but stagnation temperature is
unchanged (`Tox = Toy`).

| use | relation | `code/shock.py` |
|-----|----------|--------------------|
| downstream Mach | `My² = (Mx²+2/(k−1))/((2k/(k−1))Mx²−1)` | `mach_after_shock` |
| temperature jump | `Ty/Tx = (1+(k−1)/2·Mx²)/(1+(k−1)/2·My²)` | `shock_temperature_ratio` |
| pressure jump | `py/px = (1+kMx²)/(1+kMy²)` | `shock_pressure_ratio` |
| stagnation-p loss | `poy/pox = (Mx/My)[…]^((k+1)/(2(k−1)))` | `stagnation_pressure_ratio_across_shock` |
| sonic-area ratio | `A*x/A*y = poy/pox` | `sonic_area_ratio_across_shock` |

**Key idea:** the second law forces `sy > sx`, so a shock can only turn supersonic flow
subsonic (never the reverse), and the stagnation pressure *always* falls (`poy/pox < 1`)
even though the stagnation temperature is conserved [Moran Sec. 9.13.3 / 9.14.2].

## Run
```bash
cd code && python3 shock.py             # Table 9.3 row (Mx=2.0) + Ex 9.15(d,e)
python3 test_shock.py                   # "All 20 tests passed."
```

## Files
`notes.md`, `code/shock.py`, `code/test_shock.py`, `problems/problems.md`, `refs.md`.
