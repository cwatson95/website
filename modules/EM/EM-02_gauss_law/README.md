# EM-02 — Gauss's Law

Second module of the **ELECTRICITY & MAGNETISM** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~EM-01` (the electric field **E**) and `~MA-02` (`surface_flux`
  for the flux integral; `divergence` for the local form) — both used directly.
- **Feeds into:** `~EM-03` (potential — Gauss becomes Poisson, ∇²V = −ρ/ε₀), `~EM-06`
  (conductors & electrostatic energy), `~EM-07` (Gauss's law for the **D** field in
  dielectrics).

## Scope
The content of Griffiths §2.2. **Gauss's law** says the electric flux of **E** out of
any closed surface equals the enclosed charge over ε₀, ∮**E**·d**a** = Q_enc/ε₀
(integral form), equivalently ∇·**E** = ρ/ε₀ (the local form). With enough symmetry it
hands you the field in one line — the **sphere**, **line**, and **plane** of §2.2.3.
The other half of the electrostatic field, ∇×**E** = 0 (§2.2.4), is established in
`~EM-01` and exploited in `~EM-03`; here it just rounds out the picture.

The organizing computation: feed `~EM-01`'s point-charge field straight into `~MA-02`'s
`surface_flux`, and the inverse-square law makes the flux through **any** enclosing
surface come out to q/ε₀ — independent of the surface's size or shape — while a charge
*outside* nets zero. That surface-independence **is** Gauss's law: no new physics beyond
Coulomb, just the divergence theorem. SI units throughout; a field is the same
`E(x, y, z) -> (Ex, Ey, Ez)` function convention as EM-01/MA-02, so MA-02's operators act
on it with no glue code.

## Operations — `code/gauss_law.py`

| call | meaning | reference (printed page) |
|------|---------|--------------------------|
| `sphere_surface(center, R)` | outward-oriented Gaussian sphere S(u,v) → MA-02 `surface_flux` | Gr §2.2.1 p.66 |
| `flux_through_sphere(E, center, R)` | electric flux ∮**E**·d**a** through that sphere | Gr §2.2.1 Eq.2.13 p.66 |
| `enclosed_charge(E, center, R)` | Q_enc = ε₀ ∮**E**·d**a** (Gauss, read backwards) | Gr §2.2.1 Eq.2.13 p.66 |
| `gauss_residual(E, rho, point)` | local check ∇·**E** − ρ/ε₀ (→ 0) | Gr §2.2.2 Eq.2.16 p.71 |
| `uniform_sphere_field(Q, R, center)` | **E** of a uniformly charged solid sphere (kQ/r² out, kQr/R³ in) | Gr §2.2.3 p.71 |
| `line_charge_field(lam, axis)` | **E** = λ/2πε₀s **ŝ** of an infinite line charge | Gr §2.2.3 p.71 |
| `plane_sheet_field(sigma, normal)` | **E** = σ/2ε₀ **n̂** of an infinite charged sheet | Gr §2.2.3 p.71 |

`uniform_sphere_field`, `line_charge_field`, `plane_sheet_field` are the closed forms
Gauss's law gives instantly for the three classic symmetries (§2.2.3) — spherical
(kQ/r² outside, kQr/R³ inside), cylindrical (λ/2πε₀s), and planar (σ/2ε₀, *uniform* and
discontinuous by σ/ε₀ across the sheet). `EPS0` (ε₀) and `K_E` = 1/4πε₀ are re-exported
from `~EM-01`.

## Use
```python
from gauss_law import (flux_through_sphere, enclosed_charge, gauss_residual,
                       uniform_sphere_field, line_charge_field, plane_sheet_field)
from electrostatics import point_charge_field, field_magnitude, EPS0   # ~EM-01
import math

E = point_charge_field(1e-9)                      # a 1 nC point charge, E(x,y,z)
EPS0 * flux_through_sphere(E, (0,0,0), 0.5)       # ~ 1e-9 C = q  (any enclosing R)
enclosed_charge(E, (0,0,0), 2.0)                  # ~ 1e-9 C: same q, surface-independent

Eout = point_charge_field(1e-9, (3,0,0))          # charge OUTSIDE the sphere
EPS0 * flux_through_sphere(Eout, (0,0,0), 1.0)    # ~ 0: zero net enclosed charge

Es  = uniform_sphere_field(2e-9, 0.1)             # solid sphere, Q=2 nC, R=0.1 m
rho = 2e-9 / ((4/3)*math.pi*0.1**3)               # its uniform volume density
field_magnitude(Es)(0.2, 0, 0)                    # ~ 4.5e2 V/m outside: kQ/r^2
gauss_residual(Es, rho, (0.03, 0, 0))             # ~ 0: div E = rho/eps0 inside (Eq. 2.16)

line_charge_field(2e-9)(0.1, 0, 0)                # ~ (3.6e2, 0, 0): lam/2*pi*eps0*s, radial
plane_sheet_field(1e-9)(0, 0, 0.5)                # ~ (0, 0, 56.5): sigma/2eps0, uniform
```

## Run
```bash
cd code
python3 gauss_law.py          # demo: point-charge flux through spheres, sphere/line/plane fields
python3 test_gauss_law.py     # tests  ->  "All 8 tests passed."
```
(`gauss_law.py` reaches `~EM-01` by relative path — importing it puts MA-01/MA-02 on the
path too; this becomes `from physkit… import …` once the shared package exists.)

## Files
- `notes.md` — derivations with inline page citations
- `code/gauss_law.py`, `code/test_gauss_law.py`
- `problems/problems.md` — worked problems (Griffiths §2.2)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
