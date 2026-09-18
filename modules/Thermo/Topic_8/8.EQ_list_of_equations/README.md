# 8.EQ — List of Equations (Topic 8)

Support module for **Topic 8 (Components & Devices)**: the topic's equations, cited and
**machine-verified**. Parallels `7.EQ`, `9.EQ`.

## What it does
- `equations.md` — the list of equations (form + Moran §/Eq/page + function).
- `code/equations.py` — each equation as a canonical function + a `REGISTRY`.
- `code/test_equations.py` — **verification hub**: checks every equation against a
  book-verified value, then imports all four concept modules (`08.1_compressor`,
  `08.2_condenser`, `08.3_heat_exchanger`, `08.4_heat_pump`) and asserts they compute
  the same things.

## Scope
Mass flow `ṁ = AV/v` (and the ideal-gas form); the one-inlet/one-exit steady CV energy
balance (Eq. 4.20a) and its device specializations — compressor power `ṁ(h1−h2)`,
single-stream (condenser) heat rate `ṁ(h_out−h_in)`, the two-stream heat-exchanger
balance and mass-flow ratio (Eq. 4.18); the isentropic compressor efficiency (Eq. 6.48);
and the vapor-compression cycle relations — `Q̇in/ṁ`, `Ẇc/ṁ`, `Q̇out/ṁ`, `h4 = h3`,
`β`, `γ`, `Q_H = Q_C + W`, and the Carnot ceilings (Eqs. 10.1, 10.3–10.10).

## Run
```bash
cd code
python3 equations.py          # print the cited registry
python3 test_equations.py     # 18 value + 18 cross-module checks -> "All 36 tests passed."
```

## Files
`equations.md`, `code/equations.py`, `code/test_equations.py`, `refs.md`.
