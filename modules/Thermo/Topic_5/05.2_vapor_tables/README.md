# 5.2 — Superheated Vapor Table (A-4)

Topic 5 (Property Data: Tables & Diagrams), single-phase **superheated vapor**.

- **Builds on:** `5.1` — outside the dome, `p` and `T` are again *independent*, so two
  properties fix the state (the state principle in its usual form).
- **Feeds into:** `5.3` (compressed liquid, same two-way table structure), `5.EP`
  (Examples 3.3/3.4 use A-4 reads), `5.EQ`.

## Scope
Above the saturated-vapor line the state needs **two** independent properties, so A-4 is
a two-way table: one block per pressure, listing `v, u, h, s` versus temperature, starting
at the saturated-vapor (`Sat.`) row [Moran §3.5.1, p.105].

| use | how | `code/vapor_tables.py` |
|-----|-----|------------------------|
| superheated property `v,u,h,s` | double interpolation in `(p, T)` | `superheated` |
| linear interpolation | `y = y₁ + (x−x₁)/(x₂−x₁)·(y₂−y₁)` | `linear_interp` |
| list pressure blocks | sorted A-4 pressures | `pressures` |
| `h = u + pv` cross-check | definition of enthalpy | `enthalpy` |

**Key idea:** one off-grid variable → a single interpolation; **both** off-grid →
**double** interpolation (interpolate in `T` inside each bracketing pressure block, then
interpolate those two results in `p`). On a grid pressure, the double form collapses to
the single one.

## Data source
Reads `../../../steam_tables/A4_superheated_water.csv` (24 pressure blocks, 278 rows) —
A-4 specific volume is **direct** m³/kg (unlike A-2/A-3 `vf`, which is ×10³).

## Run
```bash
cd code && python3 vapor_tables.py        # 10 bar/215 °C interpolation + Problem 3.7
python3 test_vapor_tables.py              # "All 15 tests passed."
```

## Files
`notes.md`, `code/vapor_tables.py`, `code/test_vapor_tables.py`, `problems/problems.md`, `refs.md`.
