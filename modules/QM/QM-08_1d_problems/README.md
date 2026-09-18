# QM-08 — One-dimensional problems: wells, step & barrier, tunnelling

Module of the **QUANTUM MECHANICS** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~QM-03` (the time-independent Schrödinger equation — every
  problem here is the TISE on a different potential), and `~QM-02` (the Born rule:
  $|\psi|^2$ a probability density, $R$ and $T$ as probabilities). `~MA-04`
  (eigenvalue problems) underlies the matrix eigensolver.
- **Feeds into:** `~QM-09` (the harmonic well — the *smooth* bound-state problem,
  next), `~QM-15` (WKB: tunnelling through a general barrier), and `~QM-18`
  (scattering theory in 3-D). Cross-links `~MA-09` (Fourier / wave packets) and
  `~MA-08` (the Schrödinger equation as a PDE).

## Scope
The handful of 1-D potentials that can be solved exactly, and that fix the whole
vocabulary of QM — quantization, parity, tunnelling, resonance — as **functions
you can evaluate**:

1. **Infinite square well** — the cleanest bound-state ladder
   $E_n = n^2\pi^2\hbar^2/2mL^2$; recovered here numerically by a finite-difference
   eigensolver that works for *any* potential.
2. **Finite square well** — a finite number of bound states (counted from the
   transcendental/graphical condition) sitting below the well top.
3. **Delta-function well** — exactly **one** bound state, $E=-m\alpha^2/2\hbar^2$,
   recovered as the zero-width limit of a finite well.
4. **Free particle / wave packets** — the dispersive relation $\omega=\hbar k^2/2m$,
   group vs phase velocity, and the spreading of a Gaussian packet.
5. **Scattering** — the **step** ($R+T=1$, current-weighted) and the **rectangular
   barrier**: tunnelling ($T>0$ for $E<V_0$) and over-barrier resonances
   ($T=1$ at $k a=n\pi$).

**House rule for this module:** the analytic scattering coefficients are not just
quoted — each is independently reproduced by a **transfer-matrix** solve of the
same piecewise-constant potential, and the bound-state spectra come from a
finite-difference eigensolver checked against the closed forms. The tests are the
verification.

## Operations — `code/one_dim.py`  (natural units $\hbar=m=1$)

| call | meaning | formula |
|------|---------|---------|
| `bound_states(V, x)` | TISE eigensolver for any `V(x)` | $-\tfrac{\hbar^2}{2m}\psi''+V\psi=E\psi$ |
| `infinite_well_energy(n, L)` | exact well ladder | $E_n=n^2\pi^2\hbar^2/2mL^2$ |
| `finite_square_well_bound_count(V0, a)` | how many bound states | $\lceil 2z_0/\pi\rceil,\ z_0=\tfrac{a}{\hbar}\sqrt{2mV_0}$ |
| `delta_well_energy(alpha)` | the one bound state | $E=-m\alpha^2/2\hbar^2$ |
| `transmission_barrier(E, V0, a)` | barrier $T(E)$ | $[1+\tfrac{V_0^2\sinh^2\kappa a}{4E(V_0-E)}]^{-1}$ ($E<V_0$) |
| `reflection_barrier(E, V0, a)` | barrier $R(E)$ | $1-T$ |
| `step_RT(E, V0)` | step reflection/transmission | $R=(\tfrac{k_1-k_2}{k_1+k_2})^2,\ T=\tfrac{4k_1k_2}{(k_1+k_2)^2}$ |
| `scatter_piecewise(E, V_list, x_list)` | transfer-matrix $T,R$ for any step-stack | $[A_0,B_0]^T=M\,[t,0]^T$ |
| `free_particle_omega(k)` / `phase_velocity` / `group_velocity` | dispersion | $\omega=\hbar k^2/2m,\ v_g=2v_p=\hbar k/m$ |
| `gaussian_packet_sigma(t, sigma0)` | packet spreading | $\sigma_0\sqrt{1+(\hbar t/2m\sigma_0^2)^2}$ |

Constants `HBAR`, `MASS` (both 1.0) are exported so the formulae read dimensionally.

## Use
```python
import numpy as np
from one_dim import (bound_states, infinite_well_energy,
                     transmission_barrier, step_RT, finite_square_well_bound_count)

# infinite well: finite differences recover n^2 pi^2 / 2L^2
x = np.linspace(0, 1, 2001)
E, psi = bound_states(np.zeros_like(x), x, n_states=3)
E[0], infinite_well_energy(1, 1.0)        # (4.9348, 4.9348)  ground state

# tunnelling: nonzero transmission through a classically impassable barrier
transmission_barrier(E=5.0, V0=10.0, a=1.0)   # 0.00714  (E < V0, yet T > 0)

# a step you can't get over reflects everything; one you can lets most through
step_RT(0.5, 1.0)                          # (1.0, 0.0)   total reflection, E < V0
step_RT(4.0, 1.0)                          # (0.0052, 0.9948)  R + T = 1

finite_square_well_bound_count(15.0, 1.0)  # 4   bound states
```

## Run
```bash
cd code
python3 one_dim.py          # demo: well ladder, tunnelling vs width, resonances, step
python3 test_one_dim.py     # tests  ->  "All 18 tests passed."
```

## Files
- `notes.md` — the five problems, each derived and tied to the failure/feature it isolates
- `code/one_dim.py` — the library (FD eigensolver, analytic + transfer-matrix scattering)
- `code/test_one_dim.py` — 18 checks: well ladders, bound-state counts, tunnelling, resonances, $R+T=1$
- `problems/problems.md` — worked problems (Griffiths 3e)
- `refs.md` — verified textbook locations
