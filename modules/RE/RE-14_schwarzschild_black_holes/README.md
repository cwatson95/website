# RE-14 — Schwarzschild Solution & Black Holes

Module of the **RELATIVITY** trunk (see `modules/topic_network.txt`). The first
exact solution of Einstein's equations and the geometry of a black hole: the
horizon, the photon sphere, the ISCO, and the four classic tests of general
relativity.

- **Prerequisites:** `RE-11` (curvature — **imported** for the metric and its
  invariants), `RE-13` (Einstein field equations — the vacuum equation solved
  here); soft `~CM-11` (central-force motion & the effective potential — the
  Newtonian Kepler problem this generalises, *forward-referenced*).
- **Feeds into:** `~RE-15` (FLRW cosmology), `~QF-05` (Hawking/Unruh — the horizon
  thermodynamics begins here). Capstone of the SR→GR line `RE-02 … RE-13`.

## Scope
The Schwarzschild-Droste metric as the **unique** static, spherically symmetric
vacuum solution (Birkhoff); the **event horizon** `r=2M` as a *coordinate*
singularity (curvature `K=48M²/r⁶` finite there, RE-11) versus the real `r=0`
singularity; **gravitational redshift** (exact, → RE-10's `gh/c²` far away, → ∞ at
the horizon); **orbits** from the effective potential `V=(1−2M/r)(1+L²/r²)`, whose
relativistic `−2ML²/r³` term yields the **photon sphere `3M`**, the **ISCO `6M`**,
and **perihelion precession**; and the four **classic tests** — Mercury's
`43″/century`, the Sun's `1.75″` light bending, the Shapiro delay, and the redshift.

## The one idea
Outside any spherical mass the geometry is **one metric**, and every black-hole
phenomenon is one feature of it. The function `f(r)=1−2M/r` vanishing at `r=2M`
is a coordinate artefact (spacetime is smooth there — only the chart fails); the
extra `−2ML²/r³` in the orbital potential, absent from Newton, *is* the photon
sphere, the ISCO, and the `43″` that confirmed the theory.

## Operations — `code/schwarzschild.py` (G = c = 1; imports RE-11)
| call | meaning |
|------|---------|
| `schwarzschild_metric(M)` | the metric `g(x)`, re-exported from RE-11 |
| `horizon_radius/photon_sphere/isco(M)` | the characteristic radii `2M`, `3M`, `6M` |
| `lapse(r,M)`, `kretschmann_formula(r,M)` | `f=1−2M/r`; `K=48M²/r⁶` (finite at `2M`) |
| `effective_potential(r,L,M)` | massive: `(1−2M/r)(1+L²/r²)` |
| `effective_potential_massless(r,L,M)` | light: `(1−2M/r)L²/r²` |
| `circular_orbit_radius(L,M)` | extremum of `V`; roots merge at the ISCO |
| `photon_sphere_from_potential/isco_from_potential(M)` | locate `3M`/`6M` numerically |
| `perihelion_precession(M,a,e)` | `6πM/(a(1−e²))` rad/orbit (Mercury → 43″/cy) |
| `light_deflection(M,b)` | `4M/b` (Sun → 1.75″) |
| `shapiro_delay(r1,r2,b,M)` | radar echo excess delay |
| `gravitational_redshift(r_emit,r_obs,M)` | `√((1−2M/r_obs)/(1−2M/r_emit))−1` |
| `apsides_to_L_E`, `integrate_orbit`, `perihelion_advance` | small RK4: a precessing orbit, from scratch |

## Use
```python
from schwarzschild import (isco, photon_sphere, perihelion_precession,
                           light_deflection, gravitational_redshift,
                           M_SUN, R_SUN, A_MERCURY, E_MERCURY, ARCSEC_PER_RAD)

isco(1.0), photon_sphere(1.0)                       # (6.0, 3.0)  — in units of M
# Mercury: 43" per century from real orbital elements
dphi = perihelion_precession(M_SUN, A_MERCURY, E_MERCURY)        # rad / orbit
dphi * (100*365.25/87.9691) * ARCSEC_PER_RAD        # 42.98  arcsec/century
light_deflection(M_SUN, R_SUN) * ARCSEC_PER_RAD     # 1.751  arcsec (grazing the Sun)
gravitational_redshift(2.0001, 1e9, 1.0)            # 140.4 → diverges at the horizon
```

## Run
```bash
cd code
python3 schwarzschild.py        # demo: the radii, the horizon invariant, the four classic numbers
python3 test_schwarzschild.py   # 16 tests -> "All 16 tests passed."
```
*(Adds `../../RE-11_curvature/code` to `sys.path`; run in place. Imports RE-11
only — orbits are integrated with a self-contained RK4.)*

## Files
- `notes.md` — metric & Birkhoff, horizon vs singularity, redshift, the effective potential (ISCO/photon sphere), the four tests, infall
- `code/schwarzschild.py` — the toolkit (imports RE-11; pure stdlib otherwise)
- `code/test_schwarzschild.py` — vacuum + Kretschmann (via RE-11), `2M/3M/6M` as potential extrema, Mercury `43″`, solar `1.75″`, redshift limits, an integrated precessing orbit
- `problems/problems.md` — worked problems (Zee VI.3 / VII.1–2, cpope §6/§10)
- `refs.md` — verified citations
