# 10.2 — Stirling Engine

Second module of **Topic 10 (Engines)** — a *regenerative*, externally-heated reversible
engine whose ideal efficiency reaches the **Carnot** ceiling.

- **Builds on:** `10.1` (Carnot engine — the same `1 − T_C/T_H` bound) and the isothermal
  ideal-gas work of Topic 2.
- **Related:** the Stirling *cycle* is treated in Moran §9.8.4 (Ericsson & Stirling cycles).

## Scope
Four internally-reversible processes — two **isothermals** (at `T_H`, `T_C`) alternating with
two constant-**volume** regenerative processes (Moran §9.8.4):

| process | type | external heat |
|---|---|---|
| 1–2 | isothermal compression at `T_C` | rejects `Q_12 = R T_C ln r` |
| 2–3 | constant-V heating `T_C→T_H` | from the **regenerator** |
| 3–4 | isothermal expansion at `T_H` | adds `Q_34 = R T_H ln r` |
| 4–1 | constant-V cooling `T_H→T_C` | to the **regenerator** |

With **100 % regeneration** the two constant-volume transfers `c_v(T_H−T_C)` cancel, so all
external heat exchange is isothermal and `η = 1 − T_C/T_H` (Carnot). Remove the regenerator and
that heat becomes external, collapsing `η` far below Carnot.

| quantity | relation | function |
|---|---|---|
| ideal efficiency | `η = 1 − T_C/T_H` | `stirling_efficiency` |
| isothermal heat | `Q = R T ln r` | `isothermal_heat`, `stirling_heat_added/_rejected` |
| net work | `W = R(T_H−T_C) ln r` | `stirling_net_work` |
| regenerator duty | `Q = c_v(T_H−T_C)` | `regenerator_heat` |
| efficiency, no regenerator | `W/(Q_34 + c_v(T_H−T_C))` | `stirling_efficiency_no_regen` |
| regenerator effectiveness | `(h_x−h_2)/(h_4−h_2)` (Eq. 9.27) | `regenerator_effectiveness` |

`T` absolute (K or °R).

## Run
```bash
cd code && python3 stirling_engine.py    # ideal η = Carnot; with/without regenerator
python3 test_stirling_engine.py          # "All 14 tests passed."
```

## Files
`notes.md`, `code/stirling_engine.py`, `code/test_stirling_engine.py`, `problems/problems.md`, `refs.md`.
