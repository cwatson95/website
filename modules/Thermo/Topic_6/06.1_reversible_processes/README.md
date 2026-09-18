# 6.1 — Reversible & Internally Reversible Processes

The limiting-ideal idealization of **Topic 6 (Processes & Idealizations)** — the
benchmark against which every real (irreversible) process is measured.

- **Builds on:** the second law (Topic 3, `3.3`), entropy `S`, the T–s diagram.
- **Feeds into:** `6.2` (the σ > 0 irreversible side), `6.3` (adiabatic int. rev. ⇒
  isentropic), and every reversible-cycle analysis in Topics 8–9.

## Scope
A **reversible** process restores system *and* surroundings; an **internally reversible**
process has no irreversibilities *within* the system (a quasi-equilibrium path). For a
closed system the link between heat and entropy is [M §6.6]:

| use | relation | `code/reversible.py` |
|-----|----------|----------------------|
| entropy ↔ heat (int rev) | `dS = (δQ/T)_int rev` | `entropy_change_int_rev` |
| **isothermal heat** | `Q = T(s₂−s₁)` | `heat_int_rev_isothermal` |
| **heat = area under T–s** | `Q = ∫T dS` | `heat_int_rev_area` |
| const-pressure work | `W = p(v₂−v₁)` | `work_const_pressure` |
| entropy production | `σ = 0` | `sigma_internally_reversible` |
| adiabatic int rev ⇒ isentropic | `Q=0 ⇒ dS=0` | `is_isentropic` |
| Carnot η from T–s area | `1 − T_C/T_H` | `carnot_eff_ts` |

**Key idea:** in an internally reversible process the entropy production vanishes (σ = 0)
and the heat transfer is the **area under the path on a T–s diagram** (absolute T). This
is *not* valid for irreversible processes (module `6.2`).

## Run
```bash
cd code && python3 reversible.py        # Ex 6.1 water: W/m=186.38, Q/m=2114.1 kJ/kg
python3 test_reversible.py              # "All N tests passed."
```

## Files
`notes.md`, `code/reversible.py`, `code/test_reversible.py`, `problems/problems.md`, `refs.md`.
