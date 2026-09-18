# NE-20 — Reactor kinetics: point kinetics, delayed neutrons, feedback, Xe poisoning

Twentieth module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`). Covers **§§10.7–10.9** and **Addenda 2–3
(§§10.11–10.12)** (printed pp. 339–365) of Shultis & Faw, 3rd ed.: the point
reactor kinetics equations, delayed neutrons, reactivity units, power transients,
reactivity feedback, and the ¹³⁵Xe and ¹⁴⁹Sm fission-product poisons.

- **Prerequisites:** `~NE-19` (the six factors whose changes are the reactivity),
  `~NE-09` (fission-product yields), `~MA-11` (coupled linear ODEs).
- **Cross-links:** `~NE-21` (spatial flux; xenon oscillations), `~NE-22`
  (control as engineering), `~NE-23` (burnup reactivity loss).

## Scope
A reactor is controllable only because 0.65% of the fission neutrons arrive
seconds to minutes late. That fraction β sets the natural unit of reactivity —
the **dollar** — and at 1\$ the prompt neutrons alone sustain the chain and the
period collapses three orders of magnitude. The same physics run backwards gives
a **shutdown speed limit** of −80 s per e-fold, set by the longest-lived
precursor. Feedback then decides whether a reactor regulates itself, and ¹³⁵Xe —
the largest thermal absorption cross section of any nuclide — creates a poison
that *grows for 11 hours after shutdown* and can lock a reactor out for a day.

## Operations — `code/reactor_kinetics.py`

| call | meaning | reference |
|------|---------|-----------|
| `DELAYED_GROUPS`, `beta_total`, `relative_yields`, `decay_constants` | Table 10.9, three nuclides | Table 10.9 |
| `mean_precursor_lifetime()` | τ = Σ a_i/λ_i = 12.95 s | §10.7.4 |
| `reactivity`, `keff_from_reactivity`, `dollars`, `keff_from_dollars`, `pcm` | ρ, k(\$), pcm | Eq. (10.30) |
| `prompt_generation_time` / `effective_generation_time` | ℓ₀/k **vs** ℓ₀+βτ — *two* quantities S&F both call ℓ | Eqs. (10.83), (10.31) |
| `simple_period(δk, ℓ₀)` | the prompt-only model, kept to show how wrong it is | Eq. (10.28) |
| `small_insertion_period(k$)` | τ/k(\$); **refuses beyond 0.3\$** | Eq. (10.33) |
| `prompt_critical_period(k$, ℓ₀)` | (ℓ₀/β)/(k(\$)−1); refuses below 1\$ | Eq. (10.36) |
| `inhour(ω, ℓ₀)`, `asymptotic_period(k$, ℓ₀)` | the exact root, no approximation | Eq. (10.39) |
| `one_group_omegas`, `step_response`, `prompt_jump_factor` | Addendum 3; jump = 1/(1−k(\$)) | Eqs. (10.96)–(10.108) |
| `solve_point_kinetics(ρ(t), ℓ₀, t_end)` | six-group RK4 integration | Eqs. (10.86) |
| `poison_reactivity(σ_a, N/Σ_f)` | ρ_p ≈ −0.6 σ_a N_p/Σ_f | Eq. (10.45) |
| `iodine_xenon_equilibrium(φ)`, `xenon_transient`, `xenon_reactivity` | the ¹³⁵I/¹³⁵Xe system | Eqs. (10.46)–(10.51) |
| `time_to_poison(φ, available_ρ)` | when restart becomes impossible | §10.9.1 |
| `promethium_samarium_equilibrium`, `samarium_transient` | ¹⁴⁹Pm/¹⁴⁹Sm; equilibrium is flux-independent | Eqs. (10.52)–(10.55) |
| `temperature_coefficient`, `is_self_regulating` | α_T, and the sign that matters | §10.8.2 |

## Use
```python
from reactor_kinetics import (keff_from_dollars, small_insertion_period,
                              asymptotic_period, prompt_jump_factor,
                              solve_point_kinetics, iodine_xenon_equilibrium,
                              xenon_reactivity, time_to_poison,
                              promethium_samarium_equilibrium, BETA)

keff_from_dollars(0.1)             # 1.00065 -- S&F Example 10.11
small_insertion_period(0.1)        # 129.5 s (the book's 128 s)
asymptotic_period(0.1, 1e-4)       #  98.1 s -- the exact inhour value
small_insertion_period(1.5)        # raises: the formula does not survive prompt critical
asymptotic_period(1.5, 1e-4)       # 0.030 s -- the cliff

asymptotic_period(-100.0, 1e-4)    # -80.4 s: the shutdown speed limit
prompt_jump_factor(-1.0)           # 0.5 -- a -1$ scram halves the power at once

xenon_reactivity(11*3600, 0.0, 1e14) / xenon_reactivity(0, 0.0, 1e14)   # 4.53x
time_to_poison(1e14, 0.10) / 3600  # 2.5 h before restart becomes impossible
promethium_samarium_equilibrium(1e15)[1] == promethium_samarium_equilibrium(1e13)[1]
```

## Run
```bash
cd code
python3 reactor_kinetics.py        # demo: Examples 10.11-10.12, the cliff, xenon, samarium
python3 test_reactor_kinetics.py   # tests  ->  "All 16 tests passed."
cd ../figures && python3 make_figures.py
```

## Files
- `notes.md` — why 0.65% of the neutrons decide everything → the prompt-critical
  cliff → the shutdown speed limit → point kinetics and the ℓ notation collision
  → feedback and self-regulation → xenon and samarium, with a "Where this goes"
  map and a note on the module's three corrections.
- `code/reactor_kinetics.py`, `code/test_reactor_kinetics.py` (stdlib only,
  including an RK4 integrator for the six-group equations). Two functions
  **refuse**: `small_insertion_period` beyond 0.3\$, because Eq. (10.33) returns
  a comfortable-looking 8.6 s at 1.5\$ where the truth is 0.03 s; and
  `prompt_jump_factor` at or above 1\$, where it diverges.
- `problems/problems.md` — 7 worked problems (S&F Ch. 10 problems 24–27, 30–33)
  with numeric `*Check:*` lines.
- `figures/` — the two models of a 0.1% insertion side by side, the period cliff
  beside the shutdown floor, six-group transients beside the prompt jump, and the
  iodine reservoir beside the post-shutdown xenon peak with the lockout window.
- `refs.md` — page-verified citations; **three printed slips this module
  corrects**; the ℓ notation collision and its factor of 840; and the
  quantified accuracy of Eq. (10.33) where the book applies it.
