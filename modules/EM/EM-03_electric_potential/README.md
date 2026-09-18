# EM-03 — Electric Potential

Third module of the **ELECTRICITY & MAGNETISM** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~EM-01` (the field **E** this module integrates and reproduces) and
  `~MA-02` (`line_integral` for V = −∫**E**·d**l**, `gradient` for **E** = −∇V, `laplacian`
  for ∇²V). The curl-free structure proved in `~EM-02` is what makes the potential exist.
- **Feeds into:** `~EM-04` (boundary-value problems — solving ∇²V = −ρ/ε₀ with boundary
  data), `~EM-05` (multipole expansion of V), `~EM-06` (electrostatic energy W = ½∫ρV).
  Cross-links: `~MA-08` (the Laplace/Poisson PDE) and `~MA-14` (Green's functions).

## Scope
Because the electrostatic field is **curl-free** (∇×**E** = 0, the closing result of
`~EM-02`), it is the gradient of a single scalar — the **potential** V. This module
builds V and shows that the three MA-02 operators connecting V and **E** are exact
inverses: integrate the field to get the potential, **V = −∫E·dl** (`line_integral`,
Eq. 2.21); differentiate the potential to recover the field, **E = −∇V** (`gradient`,
Eq. 2.23); and in vacuum the potential obeys **Laplace's equation ∇²V = 0**
(`laplacian`, Eq. 2.25), with Poisson's ∇²V = −ρ/ε₀ (Eq. 2.24) where charge sits.
Because V is a *scalar*, superposition is ordinary addition — the easier road to the
field of `~EM-01`.

V is returned as a scalar field function `V(x, y, z) -> float` — exactly the MA-02
convention for scalar fields — so `gradient` and `laplacian` act on it with no glue
code, and an EM-01 field `E(x,y,z) -> (Ex,Ey,Ez)` drops straight into `line_integral`.
The round trips are checked here: `field_from_potential(potential_of_charge(q))`
reproduces the exact EM-01 Coulomb field, and `potential_from_field(point_charge_field(q))`
recovers the potential difference *path-independently* (the curl-free property is exactly
what licenses the straight-line path). SI units throughout; a *charge* is a pair
`(q, position)`.

## Operations — `code/electric_potential.py`

| call | meaning | reference (printed page) |
|------|---------|--------------------------|
| `potential_of_charge(q, source)` | V = (1/4πε₀) q/η of one charge (0 at ∞) | Gr §2.3.4 Eq.2.29 p.84 |
| `potential_point_charges(charges)` | superposed **scalar** V of point charges | Gr §2.3.4 Eq.2.29 p.84 |
| `potential_from_field(E, reference, n)` | V = −∫_ref^r **E**·d**l** (reuses MA-02 `line_integral`) | Gr §2.3.1 Eq.2.21 p.78 |
| `field_from_potential(V)` | **E** = −∇V (MA-02 `gradient`, negated) | Gr §2.3.1 Eq.2.23 p.78 |
| `poisson_residual(V, rho, point)` | ∇²V + ρ/ε₀, normalized (Poisson / Laplace) | Gr §2.3.3 Eq.2.24–2.25 p.83 |

Imported from `~EM-01`: `EPS0` (ε₀), `K_E` = 1/4πε₀ ≈ 8.99×10⁹, and the fields
`point_charge_field`/`coulomb_field` this module integrates and reproduces; from
`~MA-02`: `line_integral`, `gradient`, `laplacian`. Here **η** = \|**r** − **r'**\| is
Griffiths' "script-r" separation distance. Note `potential_of_charge` sets V = 0 at
infinity, while `potential_from_field` sets V = 0 at its finite `reference`, so the
latter returns a potential *difference*.

## Use
```python
from electric_potential import (
    potential_of_charge, potential_point_charges,
    potential_from_field, field_from_potential, poisson_residual,
)
from electrostatics import point_charge_field, K_E        # ~EM-01: the field to recover

q = 2e-9
V = potential_of_charge(q)                                # scalar V(x,y,z) = k q / r, zero at infinity
V(0.5, 0, 0)                                              # ~ 35.95 V   (= k q / 0.5)

E = field_from_potential(V)                               # E = -grad V   (~MA-02 gradient, negated)
E(0.5, 0, 0)                                              # ~ (71.9, 0, 0) V/m = point_charge_field(q) here

Vback = potential_from_field(point_charge_field(q))       # V = -int E.dl   (~MA-02 line_integral)
Vback(0.5, 0, 0)                                          # ~ 34.15 V = V(0.5,0,0) - V(ref): the two invert

poisson_residual(V, 0.0, (0.5, 0.2, -0.3))                # ~ 0: Laplace's equation holds in vacuum

Vd = potential_point_charges([(q, (-0.05, 0, 0)), (-q, (0.05, 0, 0))])
Vd(0.0, 0.3, 0.1)                                         # ~ 0: the midplane of a +q,-q pair is at V=0
```

## Run
```bash
cd code
python3 electric_potential.py          # demo: point-charge V, E=-grad V vs Coulomb, V=-int E.dl, Laplace, dipole
python3 test_electric_potential.py     # tests  ->  "All 6 tests passed."
```
(`electric_potential.py` adds `~EM-01` to the path and imports `electrostatics` plus
MA-02's `vector_calculus` by relative path; this becomes `from physkit… import …`
once the shared package exists.)

## Files
- `notes.md` — derivations with inline page citations
- `code/electric_potential.py`, `code/test_electric_potential.py`
- `problems/problems.md` — worked problems (Griffiths §2.3)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
