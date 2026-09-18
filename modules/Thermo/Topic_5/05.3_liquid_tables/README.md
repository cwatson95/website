# 5.3 — Compressed Liquid Table (A-5) + Saturated-Liquid Approximation

Topic 5 (Property Data: Tables & Diagrams), single-phase **compressed (subcooled) liquid**.

- **Builds on:** `5.1` (the `f` data the approximation leans on) and `5.2` (A-5 has the
  same two-way `(p,T)` table format as A-4).
- **Feeds into:** `5.EP` (compressed-liquid checks), `5.EQ` (Eqs. 3.11–3.14).

## Scope
For a compressed liquid the state is fixed by `p` and `T`. Table A-5 lists `v, u, h, s`
versus `(p, T)`, but exists only for water on a coarse grid [Moran §3.5.1, p.105]. Because
liquid `v` and `u` barely change with pressure at fixed `T`, Moran's **saturated-liquid
approximations** [§3.10.1, p.123] usually suffice:

| use | relation | `code/liquid_tables.py` |
|-----|----------|-------------------------|
| compressed liquid from A-5 | double interpolation in `(p,T)` | `compressed` |
| saturated-liquid reference (`f` at `T`) | read A-2 | `sat_liquid` |
| `v(T,p) ≈ vf(T)` (Eq. 3.11) | sat-liquid volume | `v_approx` |
| `u(T,p) ≈ uf(T)` (Eq. 3.12) | sat-liquid energy | `u_approx` |
| `h(T,p) ≈ hf(T) + vf(T)[p − psat(T)]` (Eq. 3.13) | pressure-corrected | `h_approx` |
| `h(T,p) ≈ hf(T)` (Eq. 3.14) | drop the small term | `h_approx_simple` |

**Key idea:** evaluate liquid properties at the **saturated-liquid state for the given
temperature**. `v` and `u` lose almost nothing; `h` keeps a small `vf·(p − psat)`
pressure correction (Eq. 3.13) that can itself be dropped (Eq. 3.14) when small.

## Data source
Reads `../../../steam_tables/` : A-5 for the table, A-2 for the `f` reference values.
A-5 `v` and A-2 `vf` are tabulated **×10³** (divide by 1000 for m³/kg).

## Run
```bash
cd code && python3 liquid_tables.py       # 100 bar/100 °C: A-5 vs approximations + Problem 3.13
python3 test_liquid_tables.py             # "All 19 tests passed."
```

## Files
`notes.md`, `code/liquid_tables.py`, `code/test_liquid_tables.py`, `problems/problems.md`, `refs.md`.
