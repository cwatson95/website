# QF-02 — Interactions & Feynman Diagrams — Perturbation Theory & the S-matrix

Second module of the **QUANTUM FIELD THEORY** trunk (see `modules/topic_network.txt`):
how interacting fields scatter, order by order in the coupling.

- **Prerequisites:** `~QF-01` (free scalar/Dirac/EM fields and their propagators —
  the lines that get contracted here), `~QM-16` (time-dependent perturbation theory —
  the Dyson series is its field-theory form).
- **Cross-links:** `~QM-18` (non-relativistic scattering / the Born approximation —
  the QM limit, where $\mathcal{M}\to f(\theta)$ and $d\sigma/d\Omega=|f|^2$),
  `~QF-04` (the loop diagrams that diverge → renormalization & the RG), `~QF-03`
  (gauge theories / QED — the same Feynman-rule machinery with spin).

## Scope
Free fields never interact; everything observable comes from the interaction term
and its **perturbative** expansion. The **interaction picture** isolates that term,
the **Dyson series** $S=T\exp(-i\int H_I\,dt)=T\exp(i\int\mathcal{L}_{\mathrm{int}}\,d^4x)$
sums it into the **S-matrix**, and **Wick's theorem** turns each time-ordered product
into a sum over **contractions** — each contraction a **Feynman propagator**
$\widetilde D_F(p)=i/(p^2-m^2+i\epsilon)$, each diagram a term in the amplitude. Read
off the simplest interacting theory, $\phi^4$: the four-point **vertex** is $-i\lambda$,
the tree-level 2→2 amplitude is $i\mathcal{M}=-i\lambda$ (so $|\mathcal{M}|^2=\lambda^2$,
isotropic), and the one-loop correction at $O(\lambda^2)$ diverges (→ `~QF-04`). The
**kinematics** are packaged in the **Mandelstam variables** $s,t,u$ with
$s+t+u=\sum_i m_i^2=4m^2$ and CM energy $\sqrt{s}=E_{\mathrm{cm}}$; the **observable**
is the 2→2 cross section $d\sigma/d\Omega=|\mathcal{M}|^2/(64\pi^2 s)$ (CM, equal
masses), which for $\phi^4$ integrates — with the $\tfrac12$ identical-particle factor
— to the total $\sigma=\lambda^2/(32\pi s)$: positive, $\propto\lambda^2$, and
threshold-gated at $\sqrt{s}\ge 2m$. This is the relativistic, many-body face of the
single-particle scattering of `~QM-18`.

## Operations — `code/feynman.py`  (natural units $\hbar=c=1$, metric $(+,-,-,-)$)

| call | meaning | reference |
|------|---------|-----------|
| `mandelstam(E_cm, theta, m)` | $(s,t,u)$ for 2→2 elastic equal-mass; obeys $s+t+u=4m^2$ | Pe §4.5 |
| `mandelstam_sum(m)` | the identity's RHS, $\sum_i m_i^2 = 4m^2$ | Pe §4.5 |
| `cm_energy(p1, p2)` | $\sqrt{s}=\sqrt{(p_1+p_2)^2}$ from two 4-momenta | Pe §4.5 |
| `cm_momentum(E_cm, m)` | $|\mathbf p|=\tfrac12\sqrt{s-4m^2}$ (0 below threshold) | Pe §4.5 |
| `phi4_amplitude_squared(lam)` | $|\mathcal{M}|^2=\lambda^2$ (tree level, $i\mathcal{M}=-i\lambda$) | Pe §4.4–4.5 |
| `phi4_differential_cross_section(E_cm, lam, m)` | $d\sigma/d\Omega=|\mathcal{M}|^2/(64\pi^2 s)$ | Pe §4.5 (Eq. 4.84) |
| `phi4_cross_section(E_cm, lam, m)` | total $\sigma=\lambda^2/(32\pi s)$ ($\tfrac12$ identical-particle factor) | Pe §4.5 |
| `propagator(p, m, eps)` | $\widetilde D_F(p)=i/(p^2-m^2+i\epsilon)$ | Pe §2.4, §4.3 |
| `minkowski_dot/_square`, `on_shell_energy` | metric $(+,-,-,-)$ helpers; on-shell $p^2=m^2$ | Pe §2.x |

Constant: `MINKOWSKI` ($\mathrm{diag}(+1,-1,-1,-1)$).

## Use
```python
import numpy as np
from feynman import mandelstam, mandelstam_sum, phi4_cross_section, propagator

s, t, u = mandelstam(E_cm=5.0, theta=np.pi/3, m=1.0)
s + t + u, mandelstam_sum(1.0)            # (4.0, 4.0)  -> s + t + u = 4 m^2

phi4_cross_section(5.0, lam=0.3, m=1.0)   # 3.58e-5  (> 0, ∝ λ², ~ 1/s)
phi4_cross_section(1.5, lam=0.3, m=1.0)   # 0.0      (below threshold √s < 2m)

propagator(np.array([np.sqrt(5),2,0,0]), m=1.0, eps=1e-6)   # |D_F| ~ 1/eps : on-shell pole
```

## Run
```bash
cd code
python3 feynman.py          # demo: Mandelstam triple + sum check, σ(√s) for φ⁴, propagator pole
python3 test_feynman.py     # tests  ->  "All 15 tests passed."
```

## Files
- `notes.md` — interaction picture → Dyson series / S-matrix → Wick & the propagator → φ⁴ vertex → Mandelstam → cross section
- `code/feynman.py`, `code/test_feynman.py`
- `problems/problems.md` — worked problems (Peskin Ch. 4; Zee Part I)
- `refs.md` — citation table (Peskin & Schroeder Ch. 4; Zee), section/chapter granularity
