# SM-05 — Phase Transitions & Critical Phenomena

Fifth module of the **STATISTICAL MECHANICS & THERMODYNAMICS** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~SM-01` (`K_B`, the counting/entropy picture); the canonical ensemble of `~SM-03`.
- **Cross-links:** `~QF-04` (the renormalization group as a field theory).

## Scope
A phase transition is a non-analyticity in the free energy as a control parameter
crosses a critical value. The workhorse is the **Ising model**. In the **mean-field
(Weiss)** approximation each spin feels the average of its neighbors, giving the
self-consistency
m = tanh[(T_c/T) m + b], with T_c = qJ/k — a continuous (second-order) transition
with a nonzero **spontaneous magnetization** below T_c and the **critical exponent
β = ½**. The **exact 1-D Ising** chain has *no* transition at any T > 0. **Landau
theory** expands the free energy F = a(T−T_c)m² + bm⁴, whose double well below T_c
reproduces the same m ~ (T_c − T)^{1/2}.

## Operations — `code/phase_transitions.py`

| call | meaning | reference |
|------|---------|-----------|
| `critical_temperature(q, J)` | mean-field T_c = qJ/k | Pa §12.5 p.420 |
| `mean_field_magnetization(T, Tc, b)` | solve m = tanh[(Tc/T)m + b] (bisection) | Pa §12.5 p.420 |
| `mean_field_residual(m, T, Tc, b)` | m − tanh[(Tc/T)m + b] (≈0 at a solution) | Pa §12.5 p.420 |
| `spontaneous_magnetization(T, Tc)` | zero-field m: >0 below Tc, 0 above | Pa §12.5 p.420 |
| `ising_1d_magnetization(T, J, h)` | exact 1-D chain; m = 0 at h = 0, ∀ T>0 | Pa §13.2 p.476 |
| `landau_free_energy(m, T, Tc, a, b)` | F = a(T−Tc)m² + bm⁴ | Pa §12.10 p.442 |
| `landau_equilibrium_magnetization(T, Tc, a, b)` | m₀ = √(a(Tc−T)/2b), else 0 | Pa §12.10 p.442 |
| `critical_exponent_beta(Tc, model)` | β in m ~ (Tc−T)^β (= ½ mean field) | Pa §12.7 p.435 |

Constant: `K_B` (re-exported).

## Use
```python
from phase_transitions import spontaneous_magnetization, critical_exponent_beta, ising_1d_magnetization, K_B

spontaneous_magnetization(150.0, 300.0)        # 0.957: ferromagnet well below Tc
spontaneous_magnetization(330.0, 300.0)        # 0.0:   paramagnet above Tc
critical_exponent_beta(300.0, "meanfield")     # 0.5  (mean-field universality)
ising_1d_magnetization(50.0, 100*K_B, 0.0)     # 0.0: no spontaneous order in 1-D
```

## Run
```bash
cd code
python3 phase_transitions.py          # demo: mean-field m(T), beta=1/2, 1-D Ising, Landau double well
python3 test_phase_transitions.py     # tests  ->  "All 8 tests passed."
```
(Solving m = tanh[(Tc/T)m] uses **bisection**, not fixed-point iteration — near Tc
the map's slope → 1 and naive iteration suffers critical slowing down.)

## Files
- `notes.md` — derivations with inline page citations
- `code/phase_transitions.py`, `code/test_phase_transitions.py`
- `problems/problems.md` — worked problems (Pathria Ch.12–14; Schroeder Ch.8)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
