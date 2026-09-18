# QM-18 — Scattering Theory

The scattering amplitude, partial waves, the optical theorem, and the Born
approximation (see `modules/topic_network.txt`).

- **Prerequisites:** `~QM-10` (angular momentum — Legendre $P_\ell$ / partial
  waves; its `legendre` from `~MA-12` is **imported by this module's code**),
  `~QM-03`/`~QM-04` (the Schrödinger equation and the radial equation for a
  central potential), `~MA-12` (spherical Bessel / Legendre special functions).
  The classical sibling is `~CM-08` (collisions, cross-sections, Rutherford) —
  **bridge** to classical mechanics, already built.
- **Feeds into:** `~QM-12` (the hydrogen radial equation reuses the spherical
  Bessel radiation-zone forms), `~QM-15` (the Born approximation **is** first-order
  perturbation theory), and forward to `~QF-01` (field-theory scattering, where
  $f$ becomes an S-matrix element — connects when it lands).

## Scope
How a beam reveals a potential. One complex function, the **scattering amplitude**
$f(\theta)$, sits between the potential and the detector; there are two
complementary ways to compute it (Griffiths 3e Ch. 10).

1. **Amplitude & cross-sections** — the asymptotic wave $e^{ikz}+f(\theta)e^{ikr}/r$;
   the differential cross-section $d\sigma/d\Omega=|f|^2$; the total cross-section
   $\sigma=\int|f|^2d\Omega$ (Griffiths §10.1, p.477–481).
2. **Partial-wave analysis** — for a central potential, expand in $P_\ell(\cos\theta)$;
   each $\ell$ scatters independently with a real **phase shift** $\delta_\ell$:
   $f=\frac1k\sum(2\ell+1)e^{i\delta_\ell}\sin\delta_\ell\,P_\ell$,
   $\sigma=\frac{4\pi}{k^2}\sum(2\ell+1)\sin^2\delta_\ell$ (§10.2–10.3, p.482–491).
3. **The optical theorem** — $\sigma_{\rm tot}=\frac{4\pi}{k}\operatorname{Im}f(0)$,
   an exact identity (probability conservation; §10.3 / Problem 10.19, p.504).
4. **The Born approximation** — for weak $V$, $f=-\frac{m}{2\pi\hbar^2}\!\int
   e^{i\mathbf q\cdot\mathbf r}V\,d^3r$ (the Fourier transform of $V$); the Yukawa
   potential gives $f=-2m\beta/[\hbar^2(\mu^2+q^2)]$, whose $\mu\to0$ limit is
   Rutherford (§10.4, p.493–501).

**House rule for this module:** nothing is asserted — every formula is checked
against a closed form or an independent computation. Hard-sphere $\delta_0=-ka$ and
$\sigma\to4\pi a^2$ are recovered from the spherical-Bessel boundary condition; the
square-well phase shift from log-derivative matching is checked against its s-wave
closed form; the **two** cross-section formulas (sum-of-$\sin^2$ and the optical
theorem) are verified to agree to machine precision; and the Born Yukawa amplitude
is checked by doing the radial integral numerically and recovering the classical
`~CM-08` Rutherford $d\sigma/d\Omega$ in the screened limit.

## Operations — `code/scattering.py` ($\hbar=2m=1$, so $E=k^2$)

| call | meaning | formula |
|------|---------|---------|
| `momentum_transfer(theta,k)` | momentum transfer | $q=2k\sin(\theta/2)$ |
| `P_l(l,x)` | Legendre polynomial (via `~MA-12`) | $P_\ell(x)$ |
| `hard_sphere_phase_shift(l,k,a)` | hard-sphere $\delta_\ell$ | $\tan\delta_\ell=j_\ell(ka)/n_\ell(ka)$ |
| `square_well_phase_shift(l,k,a,V0)` | square-well $\delta_\ell$ | log-derivative match at $r=a$ |
| `phase_shifts_hard_sphere/_square_well` | arrays $[\delta_0,\dots,\delta_{\ell_{\max}}]$ | — |
| `partial_wave_amplitude(theta,k,deltas)` | amplitude | $\frac1k\sum(2\ell+1)e^{i\delta_\ell}\sin\delta_\ell P_\ell$ |
| `differential_cross_section(theta,k,deltas)` | $d\sigma/d\Omega$ | $\lvert f\rvert^2$ |
| `partial_cross_section(l,k,delta_l)` | one partial wave | $\frac{4\pi}{k^2}(2\ell+1)\sin^2\delta_\ell$ |
| `total_cross_section(k,deltas)` | total | $\frac{4\pi}{k^2}\sum(2\ell+1)\sin^2\delta_\ell$ |
| `optical_theorem_sigma(k,deltas)` | total, the other way | $\frac{4\pi}{k}\operatorname{Im}f(0)$ |
| `born_amplitude_yukawa(theta,k,beta,mu)` | Born, Yukawa | $-2m\beta/[\hbar^2(\mu^2+q^2)]$ |
| `born_amplitude_radial(theta,k,V_func)` | Born, any central $V$ | $-\frac{2m}{\hbar^2 q}\!\int rV\sin(qr)dr$ |
| `rutherford_cross_section(theta,k,beta)` | Coulomb $\mu\to0$ | $(2m\beta/\hbar^2)^2/q^4$ |

## Use
```python
import math
from scattering import (phase_shifts_hard_sphere, phase_shifts_square_well,
                        total_cross_section, optical_theorem_sigma,
                        born_amplitude_yukawa, rutherford_cross_section)

a = 1.0; k = 0.01/a                              # low-energy hard sphere
ds = phase_shifts_hard_sphere(k, a, lmax=8)
total_cross_section(k, ds) / (math.pi*a**2)      # ~4.0   -- four times the shadow!
ds[0] + k*a                                       # ~0     -- s-wave delta_0 = -ka

k = 1.5; ds = phase_shifts_square_well(k, a, 4.0, lmax=8)
total_cross_section(k, ds), optical_theorem_sigma(k, ds)   # equal -> optical theorem

born_amplitude_yukawa(math.pi/3, k=2, beta=1, mu=0.7)      # forward-peaked amplitude
rutherford_cross_section(math.pi/3, k=1, beta=1)*math.sin(math.pi/6)**4  # const (Rutherford)
```

## Run
```bash
cd code
python3 scattering.py          # demo: factor-4 hard sphere, optical theorem, Born/Rutherford
python3 test_scattering.py     # tests  ->  "All 18 tests passed."
```

## Files
- `notes.md` — amplitude → partial waves → phase shifts → optical theorem → Born
- `code/scattering.py` — the library (numpy/scipy; $P_\ell$ via `~MA-12`, spherical Bessel via scipy)
- `code/test_scattering.py` — 18 checks: $\delta_0=-ka$, $\sigma\to4\pi a^2$, optical theorem, Born vs radial integral, Rutherford limit
- `problems/problems.md` — worked problems (Griffiths 3e Ch. 10)
- `refs.md` — verified textbook locations
