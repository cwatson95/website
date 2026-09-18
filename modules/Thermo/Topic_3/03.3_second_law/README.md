# 3.3 — Second Law

Third module of **Topic 3 (The Laws)** — the keystone.

- **Builds on:** `3.1` (absolute `T`), `3.2` (first law, cycles `W_cycle=Q_cycle`).
- **Feeds into:** entropy (`4.2`), every cycle's ceiling (Topic 9), refrigerators
  & heat pumps (Topic 8), and exergy (`4.3`).

## Scope
The first law conserves energy; the **second law** gives processes a *direction*
and forbids converting heat fully into work. Two classical statements (Moran §5.2):

- **Clausius:** no cycle can have, as its sole result, heat passing from a cooler
  to a hotter body.
- **Kelvin–Planck:** no cycle exchanging heat with a *single* reservoir delivers
  net work — analytically `W_cycle ≤ 0` (Eq. 5.1/5.3).

Consequences (`code/second_law.py`):

| quantity | relation | function |
|----------|----------|----------|
| Carnot efficiency | `η_max = 1 − T_C/T_H` | `carnot_efficiency` |
| efficiency from heat | `η = 1 − Q_C/Q_H` | `efficiency_from_heat` |
| Kelvin scale | `(Q_C/Q_H)_rev = T_C/T_H` | `kelvin_ratio` |
| max COP (refrig.) | `β_max = T_C/(T_H−T_C)` | `carnot_cop_refrigerator` |
| max COP (heat pump) | `γ_max = T_H/(T_H−T_C)` | `carnot_cop_heat_pump` |

**`T` must be absolute (K or °R).** Carnot is the *ceiling*: real cycles fall short.

## Run
```bash
cd code && python3 second_law.py      # Carnot η (60%, 80%), COPs, Kelvin-Planck
python3 test_second_law.py            # "All 15 tests passed."
```

## Files
`notes.md`, `code/second_law.py`, `code/test_second_law.py`, `problems/problems.md`, `refs.md`.
