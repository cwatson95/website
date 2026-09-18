# 1.5 — Quasiequilibrium Processes

Topic 1 (*Foundations*) module; see `modules/Thermo/list.txt`.

- **Prerequisite for:** `1.2` closed-system `∫p dV` work, `2` expansion/compression
  work, and any process drawn on a `p–V` or `T–S` diagram (`5`).

## Scope
A **quasiequilibrium** (quasistatic) process is so slow that the system stays
infinitesimally close to equilibrium throughout — so a single `p` is defined at
every step, the process is a continuous **path** of equilibrium states on a `p–V`
diagram, and the boundary work is the **area under that path**, `W = ∫p dV`.

The headline result the code makes concrete: **work is path-dependent**. Between
the *same* end states, different quasiequilibrium paths enclose different areas
and deliver different work — so `W` (like `Q`) is a path function, not a property.

## Operations — `code/quasiequilibrium.py`

| call | meaning |
|------|---------|
| `pdv_work(p_of_V, V1, V2)` | `∫p dV` along any path `p(V)` (numerical) |
| `constant_pressure_work(p, V1, V2)` | `p(V₂−V₁)` |
| `constant_volume_work(...)` | `0` (no boundary work) |
| `polytropic_work(p1, V1, V2, n)` | `∫p dV` for `pVⁿ=const` |
| `path_work(segments)` | total `W` over a sequence of legs |

## Run
```bash
cd code && python3 quasiequilibrium.py   # demo: 3 paths, same end states, 3 works
python3 test_quasiequilibrium.py         # "All 8 tests passed."
```
Demo output: `A=(100 kPa,2 m³)→B=(200 kPa,1 m³)` gives `W = −138.63 / −100 / −200 kJ`
for the isothermal, const-p-then-V, and const-V-then-p paths.

## Files
`notes.md` (derivation + cites), `code/quasiequilibrium.py`,
`code/test_quasiequilibrium.py`, `problems/problems.md`, `refs.md`.
