# QM-15 — Approximation Methods I (Perturbation Theory, Variational Principle, WKB)

A node of the **QUANTUM MECHANICS** trunk (see `modules/topic_network.txt`). The
exactly solvable problems run out fast; this is the time-**independent** toolkit
for everything else, with each method validated against an exact result.

- **Prerequisites:** `~QM-05` (operators, inner products, hermiticity),
  `~QM-09` (the harmonic oscillator — the universal test bed here), `~QM-03`
  (the TISE being approximated). Helpful: `~QM-08` (1-D scattering — its exact
  tunnelling result is imported for cross-validation).
- **Feeds into:** `~QM-16` (time-*dependent* PT, Fermi's golden rule),
  `~QM-18` (the Born approximation = PT for scattering), and across **bridge B1**
  to `~CM-21` (Hamilton–Jacobi / action–angle: WKB is the $\hbar\to0$ limit and
  Bohr–Sommerfeld quantizes the classical action). Cross-links `~MA-21`
  (asymptotic series — a PT expansion is one).

## Scope
The three pillars of time-independent approximation, as code you can run and
check against exact diagonalization / exact spectra:

1. **Perturbation theory** (Griffiths §7.1–7.2). For $H=H^0+\lambda H'$:
   first-order energy $E_n^{(1)}=\langle n|H'|n\rangle$, the first-order state,
   and second-order energy $E_n^{(2)}=\sum_{m\neq n}|\langle m|H'|n\rangle|^2/
   (E_n^0-E_m^0)$. **Degenerate** PT: the splitting is the set of eigenvalues of
   $H'$ in the degenerate subspace. The truncation error is shown to scale as
   $O(\lambda^2)$ (1st order) and $O(\lambda^3)$ (through 2nd order).
2. **Variational principle** (Griffiths Ch.8). $\langle H\rangle\ge E_{gs}$ for
   any trial state; a Gaussian family minimized over its width gives an upper
   bound — *exact* for the oscillator, tight-from-above for a quartic well.
3. **WKB** (Griffiths Ch.9). Bohr–Sommerfeld $\int_{x_1}^{x_2}p\,dx=(n+\tfrac12)
   \pi\hbar$ recovers the oscillator *exactly* and other wells asymptotically;
   tunnelling $T\approx e^{-2\int\kappa\,dx}$ shares the exact exponent of
   `~QM-08`'s barrier.

**House rule for this module:** every approximation is pinned to a *truth*. PT is
checked against exact matrix diagonalization (and its error scaling measured);
the variational bound is checked to lie above an exact finite-difference ground
state; WKB is checked against the analytic oscillator spectrum, Airy-function
zeros, and QM-08's exact transmission. Nothing is asserted that isn't measured.

> **Units.** Natural units $\hbar=m=\omega=1$ throughout (documented in
> `approximations.py`); the oscillator test bed has $E_n=n+\tfrac12$.

## Operations — `code/approximations.py`

| call | meaning | result |
|------|---------|--------|
| **Test-bed operators** | | |
| `ho_energies(D)` | $E_n^0=n+\tfrac12$ | diagonal of $H^0$ |
| `ho_position(D)` / `ho_matrix_power(D,k)` | $x$, $x^k$ in the number basis | tridiagonal / its power |
| **1. Nondegenerate PT** | | |
| `first_order_energy(E0,Hp,n)` | $E_n^{(1)}=\langle n|H'|n\rangle$ | Eq. 7.9 |
| `second_order_energy(E0,Hp,n)` | $E_n^{(2)}=\sum_{m\neq n}\frac{|H'_{mn}|^2}{E_n^0-E_m^0}$ | Eq. 7.15 |
| `first_order_correction(E0,Hp,n)` | $|\psi_n^{(1)}\rangle$ coefficients | Eq. 7.13 |
| `perturbed_energy(E0,Hp,n,lam,order)` | $E_n^0+\lambda E_n^{(1)}+\lambda^2E_n^{(2)}$ | the estimate |
| `exact_energy` / `exact_spectrum(E0,Hp,lam)` | diagonalize $H^0+\lambda H'$ | the truth |
| **1b. Degenerate PT** | | |
| `degenerate_first_order_split(Hp,indices)` | eigenvalues of $H'$ in the subspace | Eq. 7.30/7.33 |
| **2. Variational** | | |
| `gaussian_trial(b,x)` | $(2b/\pi)^{1/4}e^{-bx^2}$ | normalized |
| `variational_energy(psi,x,V)` | $\langle H\rangle$ Rayleigh quotient | $\ge E_{gs}$ |
| `gaussian_ho_energy(b)` | $b/2+1/(8b)$ | closed form |
| `gaussian_variational_min(V,x)` | minimize over $b$ | $(E_{\min},b_{\rm opt})$ |
| `fd_ground_energy` / `fd_level(V,x,n)` | exact FD spectrum | the truth |
| **3. WKB** | | |
| `classical_momentum(E,V)` | $\sqrt{2m(E-V)}$ (0 if forbidden) | array |
| `action_integral(V,E,x_lo,x_hi)` | $\int p\,dx$ | scalar |
| `bohr_sommerfeld_energy(V,n,x_lo,x_hi,gamma)` | solve $\int p\,dx=(n+\gamma)\pi\hbar$ | $E_n$ |
| `barrier_action(V,E,x_lo,x_hi)` | $\gamma=\tfrac1\hbar\int|p|\,dx$ | scalar |
| `tunneling_probability(V,E,x_lo,x_hi)` | $e^{-2\gamma}$ | scalar |
| `tunneling_rectangular(E,V0,a)` | $e^{-2\kappa a}$ | closed form |

The WKB connection-formula constant is `gamma`: $\tfrac12$ (two smooth turning
points, default), $\tfrac34$ (one vertical wall), $1$ (two vertical walls).

## Use
```python
import numpy as np
from approximations import (ho_energies, ho_matrix_power, first_order_energy,
    second_order_energy, degenerate_first_order_split, gaussian_variational_min,
    bohr_sommerfeld_energy, tunneling_rectangular)

E0 = ho_energies(40); X2 = ho_matrix_power(40, 2)        # oscillator + x^2
first_order_energy(E0, X2, 2)                            # 2.5   = n+1/2
second_order_energy(E0, X2, 2)                           # -1.25 = -(n+1/2)/2

Hp = np.array([[.3,.4,0],[.4,-.2,0],[0,0,1.]])           # degenerate states 0,1
degenerate_first_order_split(Hp, [0, 1])                 # eigenvalues of the 2x2 block

x = np.linspace(-12, 12, 6001)
gaussian_variational_min(lambda t: 0.5*t**2, x)[0]       # 0.5  (oscillator, exact)

bohr_sommerfeld_energy(lambda t: 0.5*t**2, 3, -80, 80)   # 3.5  (WKB exact for HO)
tunneling_rectangular(2.0, 10.0, 2.0)                    # 1.1e-07  ~ exp(-2 kappa a)
```

## Run
```bash
cd code
python3 approximations.py        # demo: all three pillars + the cross-checks
python3 test_approximations.py   # tests  ->  "All 21 tests passed."
```
The test imports `~QM-08`'s exact `transmission_barrier` (relative path) to
validate the WKB tunnelling exponent, so run it with the repo layout intact.

## Files
- `notes.md` — the three derivations (PT orders + degenerate W-matrix; the
  variational proof; the WKB wave function, Bohr–Sommerfeld, and tunnelling),
  with the error-scaling and the bridge to action–angle (B1)
- `code/approximations.py` — the library (numpy + scipy; self-contained)
- `code/test_approximations.py` — 21 checks: PT formulae & $O(\lambda^2)/
  O(\lambda^3)$ scaling, degenerate split = subspace eigenvalues, variational
  upper bound, WKB exact-for-HO / Airy / shared tunnelling exponent (imports QM-08)
- `problems/problems.md` — worked problems (Griffiths 3e Ch.7–9)
- `refs.md` — verified textbook locations
