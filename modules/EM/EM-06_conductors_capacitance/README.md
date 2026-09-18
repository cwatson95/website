# EM-06 — Conductors & Capacitance

Sixth module of the **ELECTRICITY & MAGNETISM** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~EM-01` (the electric field **E**, plus `field_magnitude`,
  `EPS0`, `K_E`), `~EM-02` (the uniformly-charged-sphere field, reused as the one
  distribution both energy pictures can do in closed form).
- **Feeds into:** `~EM-07` (dielectrics — a capacitor filled with matter, where
  $C\to\kappa C$ and the energy density becomes $\tfrac12\mathbf D\cdot\mathbf E$).

## Scope
The **energy** stored in an electrostatic configuration, computed **two ways that
must agree**, together with the electrostatics of **conductors** and **capacitors**.

Assembling a charge distribution costs work, and that work can be booked either to
the **charges** — $W=\tfrac12\sum_i q_iV_i$ (Gr Eq. 2.42) — or to the **field** —
$W=\tfrac{\varepsilon_0}{2}\int|\mathbf E|^2\,d\tau$ (Gr Eq. 2.45). The two are the
same number; the module pins that down on the distribution both pictures handle
analytically, the uniformly charged sphere, whose field comes straight from `~EM-02`
and whose energy is $\tfrac35\,kQ^2/R$. There is no new physics in the second form,
only a reattribution of the *same* energy from the charges to the field that the
`~EM-01`/`~EM-02` machinery already produces.

A **conductor** is an equipotential: **E** = 0 inside, all net charge on the surface,
**E** just outside normal and of magnitude $\sigma/\varepsilon_0$. That surface
charge feels an outward electrostatic **pressure** $P=\varepsilon_0E^2/2$ (Gr Eq.
2.51). A **capacitor** is a pair of conductors carrying $\pm Q$; the ratio $C=Q/V$
is fixed by geometry alone (Gr Eq. 2.54 for the parallel plate) and stores
$W=\tfrac12CV^2$ — which, written as field energy over the gap, closes the loop back
to Eq. 2.45. SI units throughout.

## Operations — `code/conductors_capacitance.py`

| call | meaning | reference (printed page) |
|------|---------|--------------------------|
| `work_to_assemble(charges)` | W = (1/4πε₀)Σ_{i<j} qᵢqⱼ/rᵢⱼ — assembly energy, charge picture | Gr §2.4.2 Eq.2.42 p.92 |
| `field_energy_density(E)` | u = (ε₀/2)\|**E**\|², energy per unit volume | Gr §2.4.3 Eq.2.45 p.94 |
| `field_energy(E, x0,x1,y0,y1,z0,z1)` | W = (ε₀/2)∫\|**E**\|² dτ over a box (midpoint quadrature) | Gr §2.4.3 Eq.2.45 p.94 |
| `field_energy_spherical(Emag, r0, r1)` | same integral, radial field: ∫(ε₀/2)E²·4πr² dr | Gr §2.4.3 Eq.2.45 p.94 |
| `self_energy_uniform_sphere(Q, R)` | W = (3/5)(1/4πε₀)Q²/R, uniformly charged sphere | Gr §2.4.3 p.94 (Ex. 2.9) |
| `capacitance_parallel_plate(A, d)` | C = ε₀A/d | Gr §2.5.4 Eq.2.54 p.105 |
| `capacitance_isolated_sphere(R)` | C = 4πε₀R | Gr §2.5.4 p.105 |
| `capacitance_spherical(a, b)` | C = 4πε₀ab/(b−a) → 4πε₀a as b→∞ | Gr §2.5.4 p.105 (Ex. 2.11) |
| `capacitance_cylindrical(a, b, L)` | C = 2πε₀L/ln(b/a), coaxial cylinders | Gr §2.5.4 p.105 (Ex. 2.11) |
| `energy_stored(C, V)` | W = ½CV² = ½Q²/C | Gr §2.5.4 Eq.2.55 p.105 |
| `surface_pressure(sigma)` | P = σ²/2ε₀ = (ε₀/2)E², outward | Gr §2.5.3 Eq.2.51 p.103 |

Constants `EPS0` (ε₀) and `K_E` = 1/4πε₀ ≈ 8.99×10⁹ are imported from `~EM-01`; the
worked test field `uniform_sphere_field` comes from `~EM-02`. A *charge* is a pair
`(q, position)`, exactly the `~EM-01` convention.

## Use
```python
from conductors_capacitance import (
    work_to_assemble, self_energy_uniform_sphere, field_energy_spherical,
    capacitance_parallel_plate, energy_stored, surface_pressure,
)
from electrostatics import field_magnitude            # ~EM-01
from gauss_law import uniform_sphere_field            # ~EM-02

# energy two ways for a uniformly charged sphere — they agree
Q, R = 1e-9, 0.05
Emag = lambda r: field_magnitude(uniform_sphere_field(Q, R))(r, 0, 0)
field_energy_spherical(Emag, 0.0, 5000 * R)          # ~1.08e-7 J, the field integral
self_energy_uniform_sphere(Q, R)                     # 1.079e-7 J, the closed form (3/5)kQ²/R

# a parallel-plate capacitor
C = capacitance_parallel_plate(A=0.01, d=1e-3)       # ε₀A/d ~ 8.85e-11 F
energy_stored(C, V=12.0)                             # ½CV² ~ 6.37e-9 J

surface_pressure(1e-6)                               # σ²/2ε₀ ~ 0.056 Pa, outward
```

## Run
```bash
cd code
python3 conductors_capacitance.py        # demo: energy two ways, a capacitor, surface pressure
python3 test_conductors_capacitance.py   # tests  ->  "All 6 tests passed."
```
(`conductors_capacitance.py` imports `~EM-01`/`~EM-02` by relative path; importing
it first puts `electrostatics` and `gauss_law` on `sys.path`, so the `from electrostatics …`
/ `from gauss_law …` lines above resolve. This becomes `from physkit… import …`
once the shared package exists.)

## Files
- `notes.md` — derivations with inline page citations
- `code/conductors_capacitance.py`, `code/test_conductors_capacitance.py`
- `problems/problems.md` — worked problems (Griffiths §2.4–2.5)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
