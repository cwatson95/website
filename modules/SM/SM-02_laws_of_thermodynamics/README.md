# SM-02 — Laws of Thermodynamics

Second module of the **STATISTICAL MECHANICS & THERMODYNAMICS** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~SM-01` (Boltzmann entropy S = k ln Ω, `K_B`).
- **Feeds into:** `~SM-03` (the canonical ensemble computes these potentials from a partition function).

## Scope
The four laws and the machinery they generate. **Temperature** is not assumed — it
*emerges* from entropy as 1/T = (∂S/∂U). The first law dU = T dS − P dV + µ dN is
energy conservation; the **second law** says total entropy never decreases; the
third sends S → 0 as T → 0. From U one builds the other **thermodynamic potentials**
by Legendre transforms — enthalpy H = U + PV, Helmholtz F = U − TS, Gibbs
G = U − TS + PV — each natural for a different control variable, and each pair of
second derivatives gives a **Maxwell relation**. The **Carnot** engine sets the
efficiency ceiling η = 1 − T_c/T_h.

## Operations — `code/laws_of_thermodynamics.py`

| call | meaning | reference |
|------|---------|-----------|
| `enthalpy(U, P, V)` | H = U + PV | Sch Ch.5 (image-only) |
| `helmholtz_free_energy(U, T, S)` | F = U − TS | Sch Ch.5; Pa §3.3 p.50 |
| `gibbs_free_energy(U, T, S, P, V)` | G = U − TS + PV = H − TS | Sch Ch.5 (image-only) |
| `temperature_from_entropy(S_of_U, U)` | 1/T = (∂S/∂U) (relative-step derivative) | Pa §1.2 p.3 |
| `pressure_from_helmholtz(F_of_V, V)` | P = −(∂F/∂V)_T | Sch Ch.5 (image-only) |
| `maxwell_relation_residual(S_TV, P_TV, T, V)` | (∂S/∂V)_T = (∂P/∂T)_V | Sch Ch.5 (image-only) |
| `carnot_efficiency(Tc, Th)` | η = 1 − Tc/Th | Sch Ch.4 (image-only) |
| `carnot_cop_refrigerator` / `carnot_cop_heat_pump` | Tc/(Th−Tc) ; Th/(Th−Tc) | Sch Ch.4 (image-only) |
| `entropy_change_heat(Q, T)` | dS = Q/T | Pa §1.3 p.6 |
| `total_entropy_change_heat_flow(Q, Th, Tc)` | Q(1/Tc − 1/Th) > 0 (2nd law) | Pa §1.3 p.6 |

Constant: `K_B` (re-exported from `~SM-01`).

## Use
```python
from laws_of_thermodynamics import carnot_efficiency, gibbs_free_energy, total_entropy_change_heat_flow

carnot_efficiency(300.0, 600.0)               # 0.5  (max efficiency of any engine)
gibbs_free_energy(100.0, 300.0, 0.2, 1e5, 1e-3)   # 140.0 J  (= H - TS)
total_entropy_change_heat_flow(1.0, 600.0, 300.0) # 1.67e-3 J/K > 0: heat flows hot->cold
```

## Run
```bash
cd code
python3 laws_of_thermodynamics.py          # demo: temperature from S(U), potentials, Maxwell, Carnot, 2nd law
python3 test_laws_of_thermodynamics.py     # tests  ->  "All 7 tests passed."
```

## Files
- `notes.md` — derivations with inline page citations
- `code/laws_of_thermodynamics.py`, `code/test_laws_of_thermodynamics.py`
- `problems/problems.md` — worked problems (Pathria Ch.1, §3.3; Schroeder Ch.1/3/4/5)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
