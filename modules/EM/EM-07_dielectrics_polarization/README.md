# EM-07 — Dielectrics & Polarization

Seventh module of the **ELECTRICITY & MAGNETISM** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~EM-01` (the Coulomb field **E** — reused for the field a free
  charge sets up), `~EM-02` (Gauss's law — the flux integral `flux_through_sphere`),
  `~MA-02` (`divergence`, for the bound volume charge ρ_b = −∇·**P**).
- **Feeds into:** `~EM-10` (magnetic materials) is the step-for-step magnetic analogue —
  magnetization **M** in place of **P**, bound currents in place of bound charge, the
  auxiliary field **H** in place of **D**; `~CMx` (condensed matter) supplies the
  microscopic origin of the susceptibility. **D** itself rejoins **E**, **B**, **H** as
  a field variable in the macroscopic Maxwell equations (`~EM-13`).

## Scope
Matter in an electric field **polarizes**: each atom acquires an induced dipole
**p** = α**E** (Eq. 4.1), and the dipole moment per unit volume is the **polarization**
**P**. A polarized object then carries **bound charge** — perfectly real charge that
sources **E** like any other — with surface density σ_b = **P**·**n̂** (Eq. 4.11) and
volume density ρ_b = −∇·**P** (Eq. 4.12, the divergence taken with `~MA-02`). Folding
the bound charge into Gauss's law isolates the free charge and defines the **electric
displacement** **D** = ε₀**E** + **P** (Eq. 4.21), whose flux reads back the *free*
charge alone, ∮**D**·d**a** = Q_free (Eq. 4.23, reusing `~EM-02`'s flux integral). In a
**linear** dielectric the response is proportional to the field, **P** = ε₀χ_e**E** and
**D** = ε**E** with ε = ε₀(1 + χ_e) (Eq. 4.30–4.34).

A polarization or field is carried as a **function** `P(x, y, z) -> (Px, Py, Pz)` —
the same MA-02 vector-field convention as `~EM-01`'s **E** — so MA-02's `divergence`
lands on **P** and EM-02's `flux_through_sphere` lands on **D** with no glue code. SI
units throughout; a *dielectric* is fixed by its dimensionless dielectric constant
`eps_r` = ε_r = ε/ε₀.

## Operations — `code/dielectrics.py`

| call | meaning | reference (printed page) |
|------|---------|--------------------------|
| `bound_surface_charge(P, normal)` | σ_b = **P**·**n̂**, bound surface density | Gr §4.2.1 Eq.4.11 p.173 |
| `bound_volume_charge(P_field, point)` | ρ_b = −∇·**P** (reuses MA-02 `divergence`) | Gr §4.2.1 Eq.4.12 p.173 |
| `displacement_field(E, P)` | **D** = ε₀**E** + **P** as a field function | Gr §4.3.1 Eq.4.21 p.181 |
| `displacement_point_free_charge(q_free)` | **D** = q_f/4πr² **r̂** of a free point charge | Gr §4.3.1 p.181 |
| `free_charge_enclosed(D, …)` | Q_free = ∮**D**·d**a** (reuses EM-02 flux) | Gr §4.3.1 Eq.4.23 p.181 |
| `permittivity(eps_r)` | ε = ε₀ε_r | Gr §4.4.1 Eq.4.32 p.185 |
| `susceptibility_from_eps_r(eps_r)` | χ_e = ε_r − 1 | Gr §4.4.1 Eq.4.34 p.185 |
| `polarization_linear(eps_r, E)` | **P** = ε₀χ_e**E** in linear media | Gr §4.4.1 Eq.4.30 p.185 |
| `displacement_linear(eps_r, E)` | **D** = ε**E** in linear media | Gr §4.4.1 Eq.4.32 p.185 |
| `capacitance_with_dielectric(C0, eps_r)` | C → ε_r C₀ when a capacitor is filled | Gr §4.4.1 p.185 |
| `polarized_sphere_inner_field(P)` | **E** = −**P**/3ε₀ inside a uniformly polarized sphere | Gr §4.2.1 Ex.4.2 |
| `polarized_sphere_surface_charge(P_mag)` | σ_b(θ) = P cos θ on that sphere | Gr §4.2.1 Eq.4.11 |

Constants `EPS0` (ε₀) and `K_E` = 1/4πε₀ are imported from `~EM-01`; the module adds no
new constants. Here **r̂** is the radial unit vector from the (origin-centred) free charge.

## Use
```python
from dielectrics import (bound_surface_charge, displacement_point_free_charge,
                         free_charge_enclosed, susceptibility_from_eps_r,
                         polarization_linear, displacement_linear, displacement_field,
                         polarized_sphere_inner_field)
from electrostatics import coulomb_field                # ~EM-01, reused directly

# uniformly polarized slab (P along +z): bound charge sits only on the faces
P = (0.0, 0.0, 2e-6)
bound_surface_charge(P, (0, 0, 1))      # +2e-6 C/m^2  (= +P, top face)
bound_surface_charge(P, (0, 0, -1))     # -2e-6 C/m^2  (= -P, bottom face)

# Gauss for D: a free point charge reads back through any sphere, medium-independent
D = displacement_point_free_charge(5e-9)
free_charge_enclosed(D, R=0.2)          # ~ 5e-9 C  (= q_free, via ~EM-02 flux)

# linear dielectric eps_r = 4:  the two faces of D agree,  eps E == eps0 E + P
E = coulomb_field([(5e-9, (0, 0, 0))])
susceptibility_from_eps_r(4.0)          # 3.0   (chi_e = eps_r - 1)
P_lin = polarization_linear(4.0, E)
displacement_linear(4.0, E)(0.1, 0, 0)  # == displacement_field(E, P_lin)(0.1, 0, 0)

# depolarizing field inside a uniformly polarized sphere
polarized_sphere_inner_field((0, 0, 1e-6))[2]   # ~ -3.76e4 V/m  (= -P/3eps0, opposes P)
```

## Run
```bash
cd code
python3 dielectrics.py          # demo: polarized slab, Gauss for D, linear media, sphere
python3 test_dielectrics.py     # tests  ->  "All 7 tests passed."
```
(`dielectrics.py` chains `~EM-01`/`~EM-02` — and through them `~MA-01`/`~MA-02` — onto
`sys.path` by relative path; this becomes `from physkit… import …` once the shared
package exists.)

## Files
- `notes.md` — derivations with inline page citations
- `code/dielectrics.py`, `code/test_dielectrics.py`
- `problems/problems.md` — worked problems (Griffiths Ch. 4)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
