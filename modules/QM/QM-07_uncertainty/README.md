# QM-07 — Uncertainty Principle & Ehrenfest's Theorem

Module of the **QUANTUM MECHANICS** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~QM-05` (Hilbert space, operators, **commutators** — the
  right-hand side of the bound) and `~MA-09` (Fourier transforms — $x$ and $p$ are
  conjugate variables). Light contact with `~QM-03` (Schrödinger equation, for the
  time evolution) helps.
- **Feeds into:** `~QM-09` (the harmonic-oscillator ground state **is** the
  minimum-uncertainty Gaussian packet) and, in the classical limit, `~CM-19`
  (Hamilton's equations — what Ehrenfest's theorem reduces to). The bridge to
  `~CM-19` connects when that module lands.

## Scope

The position–momentum uncertainty relation, its generalization to any pair of
observables, the state that saturates it, and the theorem that pulls classical
mechanics back out — all as **quantities you compute and check against closed
forms**:

1. **Position–momentum** $\sigma_x\sigma_p\ge\hbar/2$ for states on a 1-D grid,
   with $\hat p=-i\hbar\,d/dx$ applied spectrally (FFT).
2. **Generalized (Robertson)** $\sigma_A\sigma_B\ge\tfrac12|\langle[\hat A,\hat B]\rangle|$
   for Hermitian $A,B$, verified on finite matrices (spin-$\tfrac12$) — with the
   **Schwarz inequality derived step by step** (notes §2.1) and every link of
   the proof chain checked separately (`test_uncertainty_chain_stepwise`).
3. **Minimum-uncertainty packet** — the Gaussian saturates the bound exactly;
   the oscillator eigenstates give $\sigma_x\sigma_p=(n+\tfrac12)\hbar$.
4. **Ehrenfest's theorem** $d\langle x\rangle/dt=\langle p\rangle/m$,
   $d\langle p\rangle/dt=-\langle V'(x)\rangle$, by time-evolving a packet in free
   space and a harmonic well; the SHO centre traces the classical oscillation.

**House rule for this module:** nothing is asserted, everything is *measured on a
state*. Every bound is checked numerically against its analytic value — the
Gaussian's $\hbar/2$, the oscillator's $n+\tfrac12$, spin's $(\hbar/2)|\langle S_z\rangle|$,
and the two Ehrenfest rates against the recorded $\langle p\rangle$ and the mean
force. **Natural units $\hbar=m=1$.**

## Operations — `code/uncertainty.py`

| call | meaning | formula |
|------|---------|---------|
| `gaussian_packet(x, x0, sigma, p0)` | minimum-uncertainty state | $(2\pi\sigma^2)^{-1/4}e^{-(x-x_0)^2/4\sigma^2}e^{ip_0x/\hbar}$ |
| `ho_eigenstate(x, n)` | oscillator eigenstate | $\propto H_n(x)e^{-x^2/2}$ |
| `sigma_x(psi, x, dx)` / `sigma_p(psi, dx)` | standard deviations | $\sqrt{\langle x^2\rangle-\langle x\rangle^2}$, etc. |
| `apply_p(psi, dx)` | momentum operator | $\hat p\psi=-i\hbar\,d\psi/dx$ via FFT |
| `uncertainty_product(psi, x, dx)` | the product | $\sigma_x\sigma_p\ (\ge\hbar/2)$ |
| `spin_ops()` | spin-$\tfrac12$ operators | $S_i=\hbar\,\sigma_i/2$ |
| `commutator(A, B)` | the RHS source | $[A,B]=AB-BA$ |
| `std(A, psi)` | spread of an observable | $\sqrt{\langle A^2\rangle-\langle A\rangle^2}$ |
| `generalized_bound(A, B, psi)` | Robertson bound | $\tfrac12\lvert\langle[A,B]\rangle\rvert$ |
| `inner(f, g, dx=None)` | inner product (ket or grid) | $\langle f\vert g\rangle$ |
| `schwarz_gap(f, g, dx=None)` | Schwarz slack ($\ge0$) | $\langle f\vert f\rangle\langle g\vert g\rangle-\lvert\langle f\vert g\rangle\rvert^2$ |
| `schwarz_residual_identity(f, g, dx=None)` | the proof's identity | gap $=\langle f\vert f\rangle\langle h\vert h\rangle$, $h\perp f$ |
| `split_step_evolve(psi0, x, V, dt, n, dVdx)` | time evolution | split-step Fourier; records $\langle x\rangle,\langle p\rangle,\langle-V'\rangle$ |
| `classical_sho(t, x0, p0, omega)` | classical limit | $x_0\cos\omega t+\tfrac{p_0}{m\omega}\sin\omega t$ |

Also exported: `HBAR`, `M`, `grid`, `normalize`, `mean_x`, `mean_p`, `apply_p2`,
`expval`, `variance`, the Pauli matrices `PAULI_X/Y/Z`.

## Use
```python
from uncertainty import (grid, gaussian_packet, ho_eigenstate,
                         uncertainty_product, spin_ops, std, generalized_bound,
                         split_step_evolve, classical_sho)

x, dx = grid(L=40.0, N=2048)
uncertainty_product(gaussian_packet(x, sigma=1.3), x, dx)   # 0.5000  (= hbar/2, saturated)
uncertainty_product(ho_eigenstate(x, 2), x, dx)            # 2.5000  (= n + 1/2)

Sx, Sy, Sz = spin_ops()
up = [1.0, 0.0]                                             # spin up along z
std(Sx, up) * std(Sy, up), generalized_bound(Sx, Sy, up)   # (0.25, 0.25) -> saturates

# Ehrenfest: a packet in a harmonic well follows the classical oscillation
t, xs, ps, Fs, _ = split_step_evolve(gaussian_packet(x, x0=3.0),
                                     x, V=0.5*x**2, dt=0.01, nsteps=628,
                                     dVdx=lambda xx: xx)
max(abs(xs - classical_sho(t, 3.0, 0.0, 1.0)))             # ~6e-5  (classical limit)
```

## Run
```bash
cd code
python3 uncertainty.py          # demo: saturation, the spin bound, Ehrenfest
python3 test_uncertainty.py     # tests  ->  "All 20 tests passed."
```

## Files
- `notes.md` — the four results, each with its **full stepwise derivation**: the
  Schwarz inequality from the inner-product axioms (§2.1, five steps), the
  Robertson proof (§2.2, six steps), and the closed forms the code checks
- `code/uncertainty.py` — the library (numpy; spectral $\hat p$ and split-step evolver)
- `code/test_uncertainty.py` — 20 checks: saturation, $n+\tfrac12$, the spin bound,
  the Schwarz identity / saturation and the stepwise proof chain,
  both Ehrenfest rates, the classical SHO limit, norm conservation
- `problems/problems.md` — worked problems (Griffiths 3e)
- `refs.md` — verified textbook locations
