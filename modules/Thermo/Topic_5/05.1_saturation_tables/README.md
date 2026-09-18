# 5.1 — Saturation Tables (A-2 by T, A-3 by p)

Opening module of **Topic 5 (Property Data: Tables & Diagrams)**.

- **Builds on:** the p–v–T surface and vapor dome (`5.4`); the state principle —
  two independent intensive properties fix a state, *except* inside the two-phase dome
  where `p` and `T` are **not** independent.
- **Feeds into:** `5.2` (superheated vapor A-4), `5.3` (compressed liquid A-5),
  `5.5` (T–s diagram). The quality rule and interpolation defined here are reused
  throughout, and aggregated in `5.EQ`.

## Scope
Inside the liquid–vapor dome, saturation temperature and pressure are paired
(Moran §3.5.2): one table index suffices. The toolkit reads the project steam tables
and evaluates two-phase mixtures:

| use | relation | `code/sat_tables.py` |
|-----|----------|----------------------|
| saturated property by **T** (Table A-2) | interpolate vs `T` | `sat_T` |
| saturated property by **p** (Table A-3) | interpolate vs `p` | `sat_p` |
| linear interpolation | `y = y₁ + (x−x₁)/(x₂−x₁)·(y₂−y₁)` | `linear_interp` |
| two-phase property | `y = yf + x(yg − yf)` | `mixture` |
| quality from `v` | `x = (v − vf)/(vg − vf)` | `quality_from_v` |
| classify a `(p,T)` state | "Finding States" decision tree | `phase_pT` |

**Key idea:** in the dome any specific property `y ∈ {v, u, h, s}` is the same
`x`-weighted blend of its `f` and `g` endpoints (Moran Eq. 3.2, 3.6, 3.7; Eq. 6.4 for `s`).

## Data source
Reads the shared dataset `../../../steam_tables/` (Tables A-2/A-3 as CSV, extracted from
the same Moran 8e appendix) — it does **not** re-key the tables. `vf` is stored ×10³.

## Run
```bash
cd code && python3 sat_tables.py          # Ex 3.2 (rigid two-phase) + phase classification
python3 test_sat_tables.py                # "All 29 tests passed."
```

## Files
`notes.md`, `code/sat_tables.py`, `code/test_sat_tables.py`, `problems/problems.md`, `refs.md`.
