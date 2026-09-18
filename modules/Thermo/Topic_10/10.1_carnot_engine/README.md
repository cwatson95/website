# 10.1 — Carnot Engine

First module of **Topic 10 (Engines)** — the reversible benchmark every real engine
is measured against.

- **Builds on:** `3.3` (second law, Carnot corollaries & ceiling), Topic 3 absolute `T`.
- **Feeds into:** `10.2` (Stirling reaches the same ceiling), and every cycle in
  Topic 9 (`09.1` …) — Otto, Diesel, Brayton, Rankine.

## Scope
The **Carnot cycle** is the reversible power cycle between two reservoirs: four
internally reversible processes — **two isothermals alternated with two isentropics
(adiabatics)** (Moran §5.10). Its thermal efficiency is the *ceiling* for any cycle
between the same reservoirs:

- **Power cycle** (1→2→3→4): isentropic compression `T_C→T_H`, isothermal expansion
  at `T_H` (in: `Q_H`), isentropic expansion `T_H→T_C`, isothermal compression at
  `T_C` (out: `Q_C`). On a **T–s** diagram the cycle is a rectangle.
- Run **in reverse** it is the Carnot refrigerator / heat pump (§5.10.2).

Numerics (`code/carnot_engine.py`):

| quantity | relation | function |
|----------|----------|----------|
| Carnot efficiency | `η_max = 1 − T_C/T_H` (Eq. 5.9) | `carnot_efficiency` |
| efficiency from work | `η = W_cycle/Q_H` (Eq. 2.42) | `thermal_efficiency` |
| efficiency from heat | `η = 1 − Q_C/Q_H` (Eq. 5.4) | `efficiency_from_heats` |
| reversible heat ratio | `(Q_C/Q_H)_rev = T_C/T_H` (Eq. 5.7) | `kelvin_heat_ratio` |
| Carnot heat rejected | `Q_C = Q_H·T_C/T_H` | `carnot_heat_rejected` |
| Carnot net work | `W = η_max·Q_H` | `carnot_work` |
| corollary test | reversible / irreversible / impossible | `cycle_status` |
| max COP (refrig.) | `β_max = T_C/(T_H−T_C)` (Eq. 5.10) | `carnot_cop_refrigerator` |
| max COP (heat pump) | `γ_max = T_H/(T_H−T_C)` (Eq. 5.11) | `carnot_cop_heat_pump` |

**`T` absolute (K or °R).** Carnot is the limit; real cycles fall short.

## Run
```bash
cd code && python3 carnot_engine.py      # Carnot η, Example 5.1, COPs
python3 test_carnot_engine.py            # "All 16 tests passed."
```

## Files
`notes.md`, `code/carnot_engine.py`, `code/test_carnot_engine.py`, `problems/problems.md`, `refs.md`.
