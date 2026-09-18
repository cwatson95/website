# CM-15 — Oscillations

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereqs:** `~CM-02`,
`~MA-07`. **Links:** `~EM-12` (driven RLC), `~CM-16` (normal modes), `~CM-05`
(small oscillations about a minimum).

## Scope
The damped, driven harmonic oscillator x″ + 2γx′ + ω₀²x = F₀cos(ω_d t): simple
harmonic motion, the three damping regimes, the steady-state **resonance** curve,
and the **quality factor** Q. Integrated with MA-07; cross-checked against the
closed forms.

## Operations — `code/oscillations.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `integrate_oscillator(omega0, gamma, x0, v0, …, F0, omega_d)` | integrate the ODE | Fowles §3.2 p.84 |
| `damped_frequency(omega0, gamma)` | ω_d = √(ω₀²−γ²) | Fowles §3.4 p.96 |
| `driven_amplitude(omega0, gamma, F0, omega_d)` | steady-state A(ω) | Fowles §3.6 p.113 |
| `resonance_frequency(omega0, gamma)` | √(ω₀²−2γ²) | Fowles §3.6 p.113 |
| `quality_factor(omega0, gamma)` | Q = ω₀/(2γ) | Fowles §3.6 p.113 |
| `underdamped_solution(omega0, gamma, …)` | closed-form free response | Fowles §3.4 p.96 |

## Use
```python
from oscillations import integrate_oscillator, driven_amplitude, quality_factor
quality_factor(2.0, 0.2)                       # 5.0
driven_amplitude(2.0, 0.2, 1.0, 1.5)           # steady-state amplitude
ts, ys = integrate_oscillator(2.0, 0.2, 0, 0, 0, 100, 20000, F0=1.0, omega_d=1.5)
```

## Run
```bash
cd code
python3 oscillations.py        # demo (SHM, damping, driven resonance)
python3 test_oscillations.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/oscillations.py` · `code/test_oscillations.py` · `problems/problems.md`
