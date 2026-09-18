# QM-16 — Approximation Methods II: Time-Dependent Perturbation Theory & Fermi's Golden Rule

Part of the **QUANTUM MECHANICS** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~QM-15` (the time-*independent* counterpart — perturbing the
  energy levels of a static Hamiltonian), `~QM-05` (Hilbert space, Hermitian
  operators), `~QM-06` (the Born rule — what turns $|c_f(t)|^2$ into a *measured*
  transition probability). Helpful: `~QM-11` (two-level / spin language),
  `~MA-04` (eigendecomposition; the engine for $e^{-iHt}$).
- **Feeds into:** `~QM-17` (selection rules — *which* transitions have a nonzero
  matrix element), and bridges to `~QO-03` (laser physics: absorption,
  stimulated and spontaneous emission — **not yet built**; the bridge connects
  when it lands).

## Scope
What makes a quantum system **jump** from one state to another: a
*time-dependent* term in the Hamiltonian. Static potentials only give stationary
states with constant occupation probabilities (`~QM-03`); transitions require
$H'(t)$. As evaluable formulae and honest dynamics (Griffiths 3e Ch. 11):

1. **First-order transition amplitude.** Start in $|i\rangle$; to first order in
   a small perturbation the amplitude to be found in $|f\rangle$ is
   $c_f^{(1)}(t)=-\tfrac{i}{\hbar}\int_0^t\langle f|H'(t')|i\rangle\,
   e^{i\omega_{fi}t'}\,dt'$, and $P_{i\to f}=|c_f^{(1)}|^2$.
2. **Two-level system & Rabi oscillations.** The *exact* solvable case: a
   constant coupling drives complete sinusoidal flopping between two levels, the
   **generalized Rabi formula**
   $P=\frac{\Omega_R^2}{\Omega_R^2+\delta^2}\sin^2\!\big(\tfrac12\sqrt{\Omega_R^2+\delta^2}\,t\big)$
   — full inversion on resonance ($\delta=0$), capped below 1 off resonance.
3. **Sinusoidal perturbations & resonance.** A drive $H'=V\cos\omega t$ produces
   a $\mathrm{sinc}^2$ resonance line: $P(\omega)$ peaks sharply at
   $\omega=\omega_{fi}$, with peak $\propto t^2$ and width $\propto 1/t$.
4. **Fermi's golden rule.** A discrete state coupled to a *continuum* of density
   $\rho(E_f)$ decays at a **constant rate**
   $\Gamma=\frac{2\pi}{\hbar}|\langle f|H'|i\rangle|^2\rho(E_f)$.
5. **Emission/absorption & selection rules** — a word on how light drives atoms
   (absorption, stimulated and spontaneous emission), and why most matrix
   elements vanish (the bridge to `~QM-17`).

**House rule for this module:** nothing is asserted, everything is *checked* —
the Rabi formula against the exact $2\times2$ evolution, first-order PT against
the honest time-dependent Schrödinger equation (no RWA, no weak-coupling
assumption), and the golden-rule rate against both the linear-in-$t$ derivation
and the exponential decay of an $(N{+}1)$-level band model.

## Operations — `code/tdpt.py`

| call | meaning | formula |
|------|---------|---------|
| `evolve(H, psi0, t)` | exact unitary evolution (static $H$) | $\|\psi(t)\rangle=e^{-iHt}\|\psi_0\rangle$ |
| `evolve_tdse(H_of_t, psi0, t)` | honest TDSE integration (driven $H(t)$) | $i\,\partial_t\|\psi\rangle=H(t)\|\psi\rangle$ |
| `first_order_amplitude(me, w_fi, t)` | first-order amplitude | $c_f^{(1)}=-\tfrac{i}{\hbar}\!\int\! \langle f\|H'\|i\rangle e^{i\omega_{fi}t'}dt'$ |
| `first_order_probability(...)` | first-order transition prob. | $P=\|c_f^{(1)}\|^2$ |
| `two_level_H(delta, Omega_R)` | rotating-frame 2-level $H$ | $\tfrac12(\Omega_R\sigma_x+\delta\sigma_z)$ |
| `rabi_probability(t, Omega_R, delta)` | **exact** Rabi formula | $\frac{\Omega_R^2}{\Omega_R^2+\delta^2}\sin^2\!\frac{\sqrt{\Omega_R^2+\delta^2}\,t}{2}$ |
| `generalized_rabi_frequency(Omega_R, delta)` | flopping frequency | $\sqrt{\Omega_R^2+\delta^2}$ |
| `two_level_exact_probability(t, delta, Omega_R)` | Rabi from the *dynamics* | $\|\langle f\|e^{-iHt}\|i\rangle\|^2$ |
| `sinusoidal_probability(t, w, w_fi, V_fi)` | resonance line (Eq. 11.35) | $\|V_{fi}\|^2\frac{\sin^2[(\omega_{fi}-\omega)t/2]}{(\omega_{fi}-\omega)^2}$ |
| `make_driven_H(w, w_fi, V_fi)` | lab-frame driven $H(t)$ | $H_0+V_{fi}\cos(\omega t)\,\sigma_x$ |
| `golden_rule_rate(V, rho)` | Fermi's golden rule | $\Gamma=\tfrac{2\pi}{\hbar}\|V\|^2\rho$ |
| `band_hamiltonian(N, dE, V)` | discrete state + band | Wigner–Weisskopf "star" $H$ |
| `band_first_order_probability(N, dE, V, t)` | first-order decay into band | $\sum_k\|c_k^{(1)}\|^2\to\Gamma t$ |
| `survival_probability(H, times)` | exact survival of $\|i\rangle$ | $P_i(t)=\|\langle i\|e^{-iHt}\|i\rangle\|^2$ |
| `extract_rate(times, P)` | decay constant from $P(t)$ | plateau of $-d\ln P/dt$ |

Convention: $i$ = initial state, $f$ = final state; **natural units $\hbar=1$**
(energies are angular frequencies, rates are $1/\text{time}$). $\delta=\omega-\omega_{fi}$
is the detuning; $\Omega_R$ the Rabi frequency; $\rho$ the density of final states.

## Use
```python
import numpy as np
from tdpt import (rabi_probability, two_level_exact_probability,
                  sinusoidal_probability, golden_rule_rate,
                  band_hamiltonian, survival_probability, extract_rate)

# Rabi: full inversion on resonance, capped off resonance
rabi_probability(np.pi, 1.0, 0.0)        # 1.0   -> complete population inversion
rabi_probability(np.pi, 1.0, 3.0)        # 0.0936 (capped at 1/(1+9)=0.1)
two_level_exact_probability(2.1, 0.7, 1.0)   # 0.6166  (== the formula, from e^{-iHt})

# sinusoidal drive: resonance peaks at w = w_fi
ws = np.linspace(0.7, 1.3, 4001)
ws[np.argmax(sinusoidal_probability(40.0, ws, 1.0, 0.01))]   # 1.0000 (resonance)

# Fermi's golden rule: a discrete state decaying into a band
V, dE, N = 0.0309, 0.02, 375
G = golden_rule_rate(V, 1/dE)            # 0.3000  (= 2*pi*V^2*rho)
H = band_hamiltonian(N, dE, V)
t = np.linspace(0.5/G, 2.5/G, 60)
extract_rate(t, survival_probability(H, t))  # 0.3084  (~3%: finite-band)
```

## Run
```bash
cd code
python3 tdpt.py            # demo: Rabi inversion, resonance line, golden-rule decay
python3 test_tdpt.py       # tests  ->  "All 12 tests passed."
```

## Files
- `notes.md` — the derivations: $c_f^{(1)}$, the exact two-level/Rabi solution,
  the $\mathrm{sinc}^2$ resonance, and the golden rule, each tied to its code + test
- `code/tdpt.py` — the library (numpy + scipy; exact evolution, TDSE integrator,
  Rabi, resonance, golden-rule band model) and a `_demo()`
- `code/test_tdpt.py` — 12 checks: unitarity, the $c_f^{(1)}$ closed form, Rabi vs
  exact dynamics, weak/short-time PT, the resonance line shape, PT vs honest TDSE,
  and the golden-rule rate (linear-in-$t$, $V^2$/$\rho$ scaling, exponential decay)
- `problems/problems.md` — worked problems (Griffiths 3e Ch. 11)
- `refs.md` — verified textbook locations
