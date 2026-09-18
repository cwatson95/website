# QM-10 — Angular Momentum

Operators, the ladder, and the spherical harmonics (see `modules/topic_network.txt`).

- **Prerequisites:** `~QM-04` (operators, commutators, eigenvalue problems),
  `~MA-04` (linear algebra: Hermitian matrices, simultaneous eigenvectors),
  `~MA-12` (associated Legendre functions / spherical harmonics — **imported by
  this module's code**). The classical object being quantized is `~CM-09`
  (angular momentum `L = r×p`, torque): this is **bridge B3**, which connects when
  CM-09 lands.
- **Feeds into:** `~QM-11` (spin — the half-integer reps built here have matrices
  but no wavefunction), `~QM-12` (the hydrogen atom, whose angular factor *is*
  `Yₗᵐ`), `~QM-13` (addition of two angular momenta), and `~CM-13` (the inertia
  tensor, the classical sibling).

## Scope
Angular momentum is the cleanest illustration of the central quantum move:
**fix the commutation algebra, and the spectrum is forced.** No differential
equation is solved for the eigenvalues — they fall out of `[Lᵢ,Lⱼ]=iℏεᵢⱼₖLₖ`
alone (Griffiths 3e §4.3.1).

1. **The observable** — `L = r×p` promoted to operators by `p → −iℏ∇`
   (Griffiths §4.3).
2. **The algebra** — `[Lₓ,L_y]=iℏL_z` and cyclic; the components are *incompatible*,
   but `L²=Lₓ²+L_y²+L_z²` commutes with each, so `L²` and one component (`L_z`)
   share eigenstates.
3. **The ladder** — `L± = Lₓ ± iL_y` step `m` up/down; the ladder must terminate
   top and bottom, which quantizes everything.
4. **The spectrum** — `L²→ℏ²l(l+1)`, `L_z→ℏm`, `m=−l,…,+l` (so `2l+1` states);
   `l` integer **or half-integer** from the algebra alone.
5. **Position space** — the simultaneous eigenfunctions of `L²` and `L_z=−iℏ∂_φ`
   are the spherical harmonics `Yₗᵐ(θ,φ)` (Griffiths §4.1.2, §4.3.2). These need
   `l` *integer* (single-valued `e^{imφ}`); the half-integer rungs are spin.

**House rule for this module:** nothing about the spectrum is asserted — it is
*built*. The `(2l+1)`-dimensional matrices are constructed from the ladder matrix
elements `ℏ√(l(l+1)−m(m±1))` and the algebra `[Lₓ,L_y]=iℏL_z`, `L²=ℏ²l(l+1)I` is
then verified to **machine precision** (finite-dimensional reps are *exact* — a
clean contrast with `~QM-05`, where `x`,`p` only close on a truncated basis). The
spherical harmonics are checked by integrating over the sphere and against
Griffiths' Table 4.3 closed forms.

## Operations — `code/angular_momentum.py` (ħ = 1, natural units)

| call | meaning | formula |
|------|---------|---------|
| `dim(l)` / `m_values(l)` | rep size; the m-ladder | `2l+1`; `m=l,…,−l` |
| `ladder_coeff(l,m,sign)` | ladder matrix element | `ℏ√(l(l+1)−m(m±1))` |
| `Lz(l)` | z-component (diagonal) | `ℏ·diag(m)` |
| `L_plus(l)` / `L_minus(l)` | raising / lowering | `L±=Lₓ±iL_y` |
| `Lx(l)` / `Ly(l)` | transverse components | `(L₊+L₋)/2`, `(L₊−L₋)/2i` |
| `L_squared(l)` | total (Casimir) | `Lₓ²+L_y²+L_z²=ℏ²l(l+1)I` |
| `casimir_eigenvalue(l)` | the `L²` eigenvalue | `ℏ²l(l+1)` |
| `commutator(A,B)` | `AB−BA` | checks `[Lₓ,L_y]=iℏL_z` |
| `angular_momentum_set(l)` | all five matrices + m | dict |
| `spherical_harmonic(l,m,θ,φ)` | position-space eigenfn | `Yₗᵐ` (Griffiths Eq. 4.32) |
| `sphere_inner_product(l₁,m₁,l₂,m₂)` | overlap on the sphere | `∫Yₗ₁ᵐ¹*Yₗ₂ᵐ² dΩ` |
| `Lz_on_Y(l,m,θ,φ)` | apply `L_z=−iℏ∂_φ` | `→ ℏm·Yₗᵐ` |

`HBAR` is exported (set to `1.0`); the ħ factors are carried symbolically, so
restoring SI is a one-line change.

## Use
```python
import numpy as np
from angular_momentum import Lx, Ly, Lz, L_squared, commutator, spherical_harmonic, sphere_inner_product

np.allclose(commutator(Lx(1), Ly(1)), 1j*Lz(1))      # True  -- [Lx,Ly]=iħLz, exact
np.linalg.eigvalsh(Lz(2)).real                        # [-2,-1,0,1,2]  -- the spectrum
np.allclose(L_squared(1.5), 3.75*np.eye(4))           # True  -- ħ²l(l+1), l=3/2
2*Lx(0.5)                                              # the Pauli matrix σ_x (-> ~QM-11)
sphere_inner_product(2, 1, 2, 1).real                 # 1.0   -- Y_2^1 is normalized
spherical_harmonic(0, 0, 0.7, 1.1)                    # 0.282 = 1/√(4π)
```

## Run
```bash
cd code
python3 angular_momentum.py        # demo: the algebra builds the spectrum
python3 test_angular_momentum.py   # tests  ->  "All 15 tests passed."
```

## Files
- `notes.md` — the algebra-first derivation: commutators → ladder → spectrum → `Yₗᵐ`
- `code/angular_momentum.py` — the library (numpy; `Yₗᵐ` via `~MA-12`)
- `code/test_angular_momentum.py` — 15 checks: exact algebra, spectrum, orthonormality, `L_z` eigenfunctions
- `problems/problems.md` — worked problems (Griffiths 3e)
- `refs.md` — verified textbook locations
