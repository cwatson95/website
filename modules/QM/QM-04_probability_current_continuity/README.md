# QM-04 — Probability Current & Continuity

Fourth module of the **QUANTUM MECHANICS** trunk (see `modules/topic_network.txt`).
This is **KEY BRIDGE B2**: the quantum continuity equation is the *same* local
conservation law as mass (`~CM-22`) and charge (`~EM-14`).

- **Prerequisites:** `~QM-02` (Born rule, ρ = |Ψ|², normalization), `~QM-03`
  (the Schrödinger equation supplies ∂Ψ/∂t).
- **Cross-links:** `~CM-22` (continuity of mass), `~EM-14` (continuity of charge /
  Poynting), `~PK-01` (phase-space continuity / Boltzmann), `~EM-09` (the
  gauge-covariant current with a vector potential), `~QM-07` (Ehrenfest: ⟨v⟩ from **j**).

## Scope
The time-dependent Schrödinger equation implies a **local conservation law** for
probability: ∂ρ/∂t + ∇·**j** = 0, with density ρ = |Ψ|² and **probability current**
**j** = (ℏ/m) Im(Ψ*∇Ψ) = (iℏ/2m)(Ψ∇Ψ* − Ψ*∇Ψ). Integrated over all space it gives
**global conservation** d/dt ∫|Ψ|² dV = 0 — normalization is preserved for all time
(`~QM-02`). Two limits read the current physically: a **travelling wave** e^{ikx}
carries **j** = ρv with v = ℏk/m (probability flows like a fluid, `~CM-22`), while a
**real / standing stationary state** has **j** = 0 everywhere (no net flow). This is
the quantum face of **KEY BRIDGE B2** — one continuity equation, four densities:
mass, charge, probability, phase space.

## Operations — `code/probability_current.py`  (natural units ℏ = m = 1)

| call | meaning | reference |
|------|---------|-----------|
| `prob_density(psi)` | ρ = \|Ψ\|² | Gri §1.4 |
| `prob_current(psi, dx)` | j = (ℏ/m) Im(Ψ* ∂ₓΨ) | Gri §1.5; Sak §2.4 |
| `total_probability(psi, dx)` | ∫\|Ψ\|² dx (conserved) | Gri §1.4 |
| `mean_velocity(psi, dx)` | ⟨v⟩ = ∫j dx / ∫ρ dx (group velocity) | Gri §1.5 |
| `plane_wave(x, k)` | travelling state Ψ = e^{ikx}, j = ρk | Gri §2.4 |
| `gaussian_packet(x, x0, k0, sigma)` | normalized min-uncertainty packet | Gri §1.6 |
| `free_step(psi, dx, dt)` | exact spectral V=0 propagator | — (numerics) |
| `continuity_residual(psi0, psi1, dx, dt)` | ∂ₜρ + ∂ₓj across one step (≈0) | Gri §1.5 |

## Use
```python
import numpy as np
from probability_current import plane_wave, prob_current, prob_density, gaussian_packet, free_step, continuity_residual

x = np.linspace(-40, 40, 2048, endpoint=False); dx = x[1]-x[0]
psi = plane_wave(x, k=1.5)
prob_current(psi, dx).mean() / prob_density(psi).mean()   # ~1.5 = v = k  (j = rho v)

psi0 = gaussian_packet(x, x0=-10, k0=2.0, sigma=2.0)       # a moving packet
psi1 = free_step(psi0, dx, dt=2e-3)                        # one exact free step
np.max(np.abs(continuity_residual(psi0, psi1, dx, 2e-3)))  # ~1e-4 << 0.12  -> continuity holds
```

## Run
```bash
cd code
python3 probability_current.py        # demo: j = rho v, j = 0 for real states, continuity, conserved norm
python3 test_probability_current.py   # tests  ->  "All 7 tests passed."
```

## Files
- `notes.md` — derivation from the Schrödinger equation; the B2 bridge table
- `code/probability_current.py`, `code/test_probability_current.py`
- `problems/problems.md` — worked problems (Griffiths Ch.1; Sakurai Ch.2)
- `refs.md` — citation table (Griffiths, Sakurai; cross-links to CM-22 / EM-14)
