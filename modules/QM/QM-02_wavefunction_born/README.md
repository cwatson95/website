# QM-02 — The Wavefunction & Born's Rule

Second module of the **QUANTUM MECHANICS** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~QM-01` (the de Broglie matter wave $\lambda=h/p$ is the
  object promoted here to the wavefunction $\Psi$). Helpful: `~MA-19` (probability,
  built) and `~MA-09` (Fourier transforms / momentum space, built).
- **Feeds into:** `~QM-03` (the Schrödinger equation governs $\Psi$), `~QM-04`
  (probability current — *why* $\int|\Psi|^2$ is conserved), `~QM-06` (Born's rule
  becomes the measurement postulate), `~QM-07` (the minimum-uncertainty Gaussian).

## Scope
Born's statistical interpretation, as composable operations on a 1-D grid that you
evaluate and cross-check against closed forms:

1. **The wavefunction** $\Psi(x,t)$ — a complex probability amplitude.
2. **Born's rule** — $|\Psi|^2$ is a probability *density*; $\int_a^b|\Psi|^2dx$ is
   the probability of finding the particle in $[a,b]$.
3. **Normalization** $\int|\Psi|^2dx=1$, **square-integrability** ($\Psi\to0$ at
   $\infty$), and the preservation of the norm in time.
4. **Expectation values** $\langle x\rangle$, $\langle x^2\rangle$, $\langle p\rangle$ and
   the standard deviations $\sigma_x,\sigma_p$, with $\hat p=-i\hbar\,\partial_x$.
5. **The move to momentum space** — $\Phi(p)$ is the Fourier transform of $\Psi$.

**House rule for this module:** nothing is asserted, everything is *checked against
a closed form.* The validation target is the analytic Gaussian wavepacket
$\Psi\propto e^{-(x-x_0)^2/4\sigma^2}e^{ik_0x}$, whose every moment is known in
closed form ($\langle x\rangle=x_0$, $\sigma_x=\sigma$, $\langle p\rangle=\hbar k_0$,
$\sigma_p=\hbar/2\sigma$, $\sigma_x\sigma_p=\hbar/2$, and
$P(|x-x_0|<L\sigma)=\operatorname{erf}(L/\sqrt2)$). The tests confirm each
numerically. (This is the QM-02 analogue of `~QM-01`'s "every constant rederived.")

## Operations — `code/wavefunction.py`

| call | meaning | formula |
|------|---------|---------|
| `prob_density(psi)` | Born density | ρ = \|Ψ\|² |
| `total_probability(psi, x)` | norm integral | ∫\|Ψ\|²dx |
| `normalize(psi, x)` | rescale to unit norm | Ψ / √(∫\|Ψ\|²dx) |
| `prob_between(psi, x, a, b)` | Born probability | ∫ₐᵇ\|Ψ\|²dx |
| `expectation_x` / `expectation_x2` | position moments | ⟨x⟩=∫x\|Ψ\|²dx, ⟨x²⟩ |
| `sigma_x(psi, x)` | position spread | √(⟨x²⟩−⟨x⟩²) |
| `expectation_p(psi, x, hbar)` | momentum (finite diff.) | ∫Ψ*(−iℏ∂ₓ)Ψ dx |
| `expectation_p2` / `sigma_p` | momentum spread | ⟨p²⟩=ℏ²∫\|∂ₓΨ\|²dx, σ_p |
| `gaussian_packet(x, x0, sigma, k0)` | analytic state | (2πσ²)^−¼ e^{−(x−x0)²/4σ²} e^{ik0x} |
| `momentum_space(psi, x, hbar)` | Fourier → Φ(p) | (2πℏ)^−½ ∫Ψ e^{−ipx/ℏ}dx |
| `expectation_p_fft(psi, x, hbar)` | ⟨p⟩ in p-space | ∫p\|Φ\|²dp |
| `free_propagate(psi, x, t, mass, hbar)` | free evolution | IFFT(e^{−iℏk²t/2m}·FFT Ψ) |

`hbar` defaults to 1 (natural units) but is a keyword everywhere.

## Use
```python
import numpy as np
from wavefunction import (gaussian_packet, normalize, prob_between,
                          expectation_x, sigma_x, expectation_p, sigma_p, momentum_space)

x   = np.linspace(-18, 22, 4001)
psi = gaussian_packet(x, x0=2.0, sigma=1.0, k0=5.0)   # already normalized

expectation_x(psi, x)                 # 2.0          (= x0)
sigma_x(psi, x)                       # 1.0          (= sigma)
expectation_p(psi, x)                 # ~5.0         (= hbar*k0)
sigma_x(psi, x) * sigma_p(psi, x)     # 0.5 = hbar/2 (minimum-uncertainty state)
prob_between(psi, x, 1.0, 3.0)        # 0.6827       (= erf(1/sqrt2), the 1-sigma band)
p, phi = momentum_space(psi, x)       # Phi(p) peaks at p = 5 (= hbar*k0)
```

## Run
```bash
cd code
python3 wavefunction.py          # demo: the Gaussian's moments + norm-preserving spreading
python3 test_wavefunction.py     # tests  ->  "All 25 tests passed."
```

## Files
- `notes.md` — the six clusters (wavefunction → Born → normalization → ⟨x⟩ → ⟨p⟩ →
  momentum space), each with its derivation, inline-cited to Griffiths 3e Ch.1
- `code/wavefunction.py` — the library (numpy; trapezoid integrals, FD & FFT momentum)
- `code/test_wavefunction.py` — 25 checks against the closed-form Gaussian moments
- `problems/problems.md` — worked problems (Griffiths 3e §1.3–1.5)
- `refs.md` — verified textbook locations
