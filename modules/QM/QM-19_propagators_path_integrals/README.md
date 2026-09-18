# QM-19 — Propagators & path integrals

Part of the **QUANTUM MECHANICS** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~QM-03` (time evolution of $\Psi$, the object the propagator
  evolves), `~QM-02` (Born rule, $|K|^2$ as a probability), `~MA-14` (Green's
  functions / propagators — **imported** here), `~MA-13`/`~CM-13` (calculus of
  variations, for the stationary-phase limit).
- **Feeds into:** `~QF-01` (the path integral is the starting point of quantum
  field theory — forward link), statistical mechanics via Wick rotation, and the
  classical bridge **B1** to `~CM-17` (Lagrangian mechanics, recovered as the
  $\hbar\to0$ limit; not built yet).

## Scope
The **propagator** (kernel) $K(x,t;x',0)=\langle x|e^{-i\hat Ht/\hbar}|x'\rangle$
that turns *any* initial wavefunction into the state at time $t$,
$\Psi(x,t)=\int K(x,t;x',0)\,\Psi(x',0)\,dx'$ — as closed forms you can evaluate
and a sum-over-paths you can build:

1. **The kernel and its eigen-sum** $K=\sum_n\psi_n(x)\psi_n^*(x')e^{-iE_nt/\hbar}$
   (Griffiths Eq. 6.79): completeness at $t=0$, the semigroup law, $|K|^2$ as a
   travel probability.
2. **The free propagator** $K_0=\sqrt{m/2\pi i\hbar t}\,\exp[im(x-x')^2/2\hbar t]$:
   the $\delta$-function initial condition, the composition law, the fact that it
   *solves* the free Schrödinger equation (so it is the retarded Green's function),
   and that it evolves a Gaussian packet to the **same** state as a direct
   split-step FFT integration.
3. **The Feynman path integral** $K=\int\mathcal D[x]\,e^{iS[x]/\hbar}$,
   $S=\int L\,dt$, $L=\tfrac12 m\dot x^2-V$ — the time-sliced sum over paths,
   shown to converge to the closed form, with the classical path as the
   stationary-phase ($\hbar\to0$) limit.
4. **The harmonic oscillator** (Mehler kernel) by its free limit and by solving
   the oscillator Schrödinger equation.
5. **The `~MA-14` connection:** the propagator *is* the time-domain Green's
   function of the Schrödinger operator; its eigen-sum is MA-14's Green's-function
   spectral sum with $1/\lambda_n\to e^{-iE_nt/\hbar}$ (verified for a box).

**House rule for this module:** Griffiths has no path-integral chapter, so nothing
load-bearing is quoted — **every** formula (free $K_0$, Mehler, the delta and
composition laws, the spreading width, the path-integral convergence, the box
eigen-sum, the MA-14 resolvent identity) is checked numerically in
`test_propagator.py` against a closed form, an independent integrator, or imported
MA-14 code. The verification is the code.

## Operations — `code/propagator.py`

| call | meaning | formula |
|------|---------|---------|
| `free_propagator(x, xp, t)` | free kernel $K_0$ | $\sqrt{m/2\pi i\hbar t}\,e^{im(x-x')^2/2\hbar t}$ |
| `free_retarded_propagator(x, xp, t)` | causal $G^R=\theta(t)K_0$ | retarded Green's function |
| `classical_action_free(x, xp, t)` | action of the straight path | $S_{\rm cl}=m(x-x')^2/2t$ |
| `harmonic_propagator(x, xp, t, omega)` | Mehler kernel | see notes §5 |
| `gaussian_packet(x, x0, p0, sigma)` | initial packet | $(2\pi\sigma^2)^{-1/4}e^{-(x-x_0)^2/4\sigma^2+ip_0x}$ |
| `propagate(psi0, xs, t, kernel)` | $\Psi(x,t)=\int K\,\Psi_0\,dx'$ | quadrature on a grid |
| `evolve_free_spectral(psi0, xs, t)` | **independent** TDSE solve | split-step FFT |
| `packet_center_width(psi, xs)` | $\langle x\rangle,\ \sigma_x$ | moments of $|\Psi|^2$ |
| `free_propagator_euclidean` / `harmonic_propagator_euclidean` | Wick-rotated kernels | $t\to-i\tau$ heat kernels |
| `path_integral_realtime_free(x, xp, t, N)` | literal real-time sum-over-paths | $N$ slices, $N\in\{1,2,3\}$ |
| `path_integral_euclidean(xs, tau, N, V, src)` | Trotter sum-over-paths | $(D_{V/2}FD_{V/2})^N$ |
| `box_eigenfunction` / `box_energy` | well states | $\sqrt{2/L}\sin(n\pi x/L)$, $n^2\pi^2\hbar^2/2mL^2$ |
| `box_propagator(x, xp, t, nmax)` | eigen-sum kernel | $\sum_n\psi_n\psi_n^*e^{-iE_nt/\hbar}$ |
| `box_resolvent_static(x, xp, nmax)` | $\langle x|\hat H^{-1}|x'\rangle$ | $\sum_n\psi_n\psi_n^*/E_n$ |

Constants `HBAR`, `MASS` are exported (natural units $\hbar=m=1$).

## Use
```python
import numpy as np
from propagator import (free_propagator, propagate, gaussian_packet,
                        evolve_free_spectral, box_resolvent_static)

# free kernel value
free_propagator(np.array([1.0]), -0.5, 0.8)          # 0.363 + 0.259i

# evolve a Gaussian packet two ways and compare
xs = np.linspace(-40, 40, 4096)
psi0 = gaussian_packet(xs, x0=0.0, p0=2.0, sigma=1.0)
prop = propagate(psi0, xs, 2.0)                       # via the propagator
spec = evolve_free_spectral(psi0, xs, 2.0)            # via direct FFT evolution
np.max(np.abs(prop - spec))                           # ~1e-14: same state

# the box H^{-1} kernel = 2 x MA-14's Green's function
box_resolvent_static(0.3, 0.7, 5000)                 # 0.180 = 2 * 0.3*(1-0.7)
```

## Run
```bash
cd code
python3 propagator.py          # demo: K0, real-time & Wick-rotated path integrals, MA-14 link
python3 test_propagator.py     # tests  ->  "All 15 tests passed."
```

## Files
- `notes.md` — kernel → eigen-sum → Green's function → free → path integral →
  oscillator, with derivations and inline cites
- `code/propagator.py` — the library (numpy; imports `~MA-14`)
- `code/test_propagator.py` — 15 checks: closed forms, FFT cross-check, path-integral
  convergence, MA-14 resolvent identity
- `problems/problems.md` — worked problems (Griffiths 3e Prob. 6.30, 2.21)
- `refs.md` — verified textbook locations + honesty note
