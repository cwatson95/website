# 09.1 — Carnot Cycle

First module of **Topic 9 (Power & Refrigeration Cycles)** — the reversible benchmark.

- **Builds on:** `3.3` (second law, Carnot corollaries), `07.1` (efficiency & COP).
- **Feeds into:** every other cycle in Topic 9 — Otto (`09.2`), Diesel (`09.3`),
  dual (`09.4`), Brayton (`09.5`), Rankine (`09.6`) — as their efficiency ceiling.

## Scope
The **Carnot cycle** is the reversible cycle of *two adiabatic + two isothermal*
processes (Moran §5.10). It delivers the most work — or, reversed, the best COP —
of any cycle between two reservoirs, so it caps all of Topic 9.

| quantity | relation | function |
|----------|----------|----------|
| Carnot efficiency | `η_max = 1 − T_C/T_H` (Eq. 5.9) | `carnot_efficiency` |
| max COP (refrig.) | `β_max = T_C/(T_H−T_C)` (Eq. 5.10) | `carnot_cop_refrigerator` |
| max COP (heat pump) | `γ_max = T_H/(T_H−T_C)` (Eq. 5.11) | `carnot_cop_heat_pump` |
| most work from heat | `W_max = η_max·Q_H` | `max_work_from_heat` |
| ceiling test | `η ≤ η_max` for any cycle | `efficiency_is_possible` |

**`T` must be absolute (K or °R).** Carnot is the ceiling: real cycles fall short.

## Run
```bash
cd code && python3 carnot_cycle.py      # η_max (80%), COPs (9.9, 13.95), the ceiling
python3 test_carnot_cycle.py            # "All 13 tests passed."
```

## Files
`notes.md`, `code/carnot_cycle.py`, `code/test_carnot_cycle.py`, `problems/problems.md`, `refs.md`.
