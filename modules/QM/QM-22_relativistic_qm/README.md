# QM-22 — Relativistic Quantum Mechanics: Klein–Gordon & Dirac

The capstone of the **QUANTUM MECHANICS** trunk (see `modules/topic_network.txt`):
making quantum mechanics compatible with special relativity, and discovering — as
a *consequence* — spin, the antiparticle, and the on-ramp to quantum field theory.

- **Prerequisites:** `~QM-03` (the Schrödinger equation this generalizes),
  `~QM-05` (operators / matrix QM), `~QM-10`/`~QM-11` (angular momentum & spin, the
  algebra spin-$\tfrac12$ obeys), `~MA-18` (Clifford / gamma-matrix algebra). The
  energy–momentum relation belongs to `~RE-06` — **skipped** in the RE trunk
  (waits on `~CM-06`) — so it is stated inline here.
- **Feeds into:** `~QF-01` (second quantization: fields resolve the negative-energy
  / indefinite-density problems and reinterpret them as antiparticles),
  `~QM-17` (fine structure = the non-relativistic expansion of the Dirac equation).

## Scope
The relativistic energy–momentum relation $E^2=p^2c^2+m^2c^4$ (stated inline; home
module `~RE-06` not built), and the two equations got by quantizing it:

1. **Klein–Gordon** (spin 0): $(\Box+m^2)\phi=0$; a plane wave $e^{-ip\cdot x}$
   solves it **iff** $E^2=\vec p^{\,2}+m^2$ (both signs → negative-energy modes);
   and its two flaws — negative energies and an **indefinite** probability density.
2. **Dirac** (spin $\tfrac12$): $(i\gamma^\mu\partial_\mu-m)\psi=0$; the gamma
   matrices and the **Clifford algebra** $\{\gamma^\mu,\gamma^\nu\}=2g^{\mu\nu}$;
   why Dirac "square-roots" Klein–Gordon ($\text{Dirac}^2=\text{KG}$); 4-spinors;
   the 4 plane-wave solutions (2 positive-, 2 negative-energy).
3. **Non-relativistic limit** → the **Pauli equation** with the correct $g=2$ and
   spin–orbit coupling: **spin and its $g=2$ emerge automatically** from the Dirac
   structure; the leading energy $E\approx m+p^2/2m$.

**House rule (per the weak-coverage rule):** Griffiths 3e is non-relativistic —
"Klein–Gordon" appears **nowhere** in 644 pages, and the Dirac equation only *in
passing* (fine-structure remarks, p.388 & p.415, both verified). The physics here
is standard and done correctly anyway; **the verification is the code**, exactly
as in `~QM-01_origins`. Every identity is checked numerically against a closed form.

## Operations — `code/relativistic.py`  (natural units $\hbar=c=1$)

| call | meaning | formula |
|------|---------|---------|
| `metric()` / `minkowski_dot(a,b)` | $g_{\mu\nu}=\mathrm{diag}(1,-1,-1,-1)$; invariant product | $a\cdot b=a^0b^0-\vec a\cdot\vec b$ |
| `pauli(i)` | Pauli matrices (built locally) | $\sigma_1,\sigma_2,\sigma_3$ |
| `dirac_gamma(mu)` / `gamma5()` | gamma matrices, Dirac rep | $\gamma^0,\gamma^i$ from Pauli blocks; $\gamma^5=i\gamma^0\gamma^1\gamma^2\gamma^3$ |
| `clifford(mu,nu)` | Clifford anticommutator | $\{\gamma^\mu,\gamma^\nu\}=2g^{\mu\nu}\mathbb1_4$ |
| `kg_energy(p,m,sign)` | on-shell energy (both signs) | $E=\pm\sqrt{\vec p^{\,2}+m^2}$ |
| `box_fd` / `kg_operator_fd` | $\Box$ and $(\Box+m^2)\phi$ numerically | $\Box=\partial_t^2-\nabla^2$ |
| `kg_eigenvalue(p,m)` | KG operator eigenvalue on $e^{-ip\cdot x}$ | $-(p\cdot p-m^2)$ |
| `p_slash(p4)` / `dirac_matrix(p4,m)` | $\not{\!p}=\gamma^\mu p_\mu$; Dirac operator | $\not{\!p}-m$ |
| `dirac_determinant(p4,m)` | when solutions exist | $\det(\not{\!p}-m)=(p\cdot p-m^2)^2$ |
| `dirac_squared(p4,m)` | "Dirac² = Klein–Gordon" | $(\not{\!p}-m)(\not{\!p}+m)=(p\cdot p-m^2)\mathbb1$ |
| `u_spinor` / `v_spinor` / `dirac_solutions` | the 4 plane-wave spinors | $(\not{\!p}-m)u=0$, $(\not{\!p}+m)v=0$ |
| `nonrel_energy` / `energy_expansion` | NR limit | $E=m+\tfrac{p^2}{2m}-\tfrac{p^4}{8m^3}+\cdots$ |
| `sigma_dot_pi_squared` / `dirac_g_factor` | Pauli term, $g$-factor | $(\vec\sigma\cdot\vec\pi)^2=\vec\pi^2-q\vec\sigma\cdot\vec B\Rightarrow g=2$ |

`HBAR`, `C` (both `1.0`) and `I2`, `I4` are exported; reinsert $\hbar,c$ for SI.

## Use
```python
from relativistic import (dirac_gamma, clifford, metric, four_momentum,
                          dirac_determinant, dirac_squared, dirac_solutions,
                          dirac_matrix, p_slash, I4, dirac_g_factor)
import numpy as np

# Clifford algebra holds for every pair:
np.allclose(clifford(0, 0),  2*metric()[0,0]*I4)     # True: (gamma^0)^2 = +I
np.allclose(clifford(1, 1),  2*metric()[1,1]*I4)     # True: (gamma^1)^2 = -I

p4 = four_momentum([0.3, 0.4, 0.0], m=1.0)           # on-shell electron
abs(dirac_determinant(p4, 1.0))                      # ~0: solutions exist iff E^2=p^2+m^2
np.allclose(dirac_squared(p4, 1.0), 0)               # True: Dirac^2 = Klein-Gordon (=0 on shell)

u = dirac_solutions([0.3, 0.4, 0.0], 1.0)["u0"]
np.allclose(dirac_matrix(p4, 1.0) @ u, 0)            # True: spinor solves the Dirac equation

dirac_g_factor()                                     # (2.0, ~1e-15): g=2 emerges from Dirac
```

## Run
```bash
cd code
python3 relativistic.py          # demo: Clifford algebra, KG/Dirac dispersion, g=2
python3 test_relativistic.py     # tests  ->  "All 18 tests passed."
```

## Cross-links
- `~RE-06` (relativistic dynamics / 4-momentum / $E=mc^2$) — the home of
  $E^2=p^2c^2+m^2c^4$; **skipped** in the RE trunk pending `~CM-06`. Stated inline
  here; the bridge connects when RE-06 lands.
- `~QF-01` (canonical field quantization) — **forward**: re-reads $\phi,\psi$ as
  fields, turning the negative-energy / indefinite-density problems into
  antiparticles and conserved charges. The single-particle theory ends here.
- `~QM-11` (spin) — spin-$\tfrac12$ is *derived* here (the 4-spinor), not posited.
- `~QM-17` (fine structure) — the relativistic + spin–orbit corrections are the
  non-relativistic expansion of this equation (Griffiths p.388/p.415).
- `~MA-18` (group theory / Clifford & gamma algebra) — the algebra of the $\gamma^\mu$;
  the test cross-checks `pauli()` against MA-18 (the only inter-module import).

## Files
- `notes.md` — derivations (KaTeX): the energy–momentum relation, Klein–Gordon and
  its problems, the Dirac equation / Clifford algebra / spinors, and the $g=2$ limit
- `code/relativistic.py` — the library (numpy; gammas, KG & Dirac operators, spinors, $g$-factor)
- `code/test_relativistic.py` — 18 checks against closed forms (incl. the MA-18 cross-check)
- `problems/problems.md` — worked problems, each with a code *Check:*
- `refs.md` — verified textbook locations + the weak-coverage honesty note
