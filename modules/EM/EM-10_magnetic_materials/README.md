# EM-10 — Magnetic Materials & Magnetization

Tenth module of the **ELECTRICITY & MAGNETISM** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~EM-08` (magnetostatics — supplies `MU0` and Ampère's law
  `∇×B = μ₀J`), `~MA-01` (vector algebra — `cross`, `norm`), `~MA-02` (vector
  calculus — `curl`).
- **Feeds into:** — (this closes the static-magnetism arc `~EM-08` → `~EM-09` →
  EM-10; `~EM-11` onward turns to time-varying fields, and the **H** field +
  constitutive relations reappear in `~EM-13` Maxwell).

## Scope
The magnetic analogue of dielectrics (`~EM-07`). A **magnetized** object —
described by its magnetization **M**, the magnetic dipole moment per unit volume —
carries **bound currents**: a volume current **J**_b = ∇×**M** (Eq. 6.13, via the
MA-02 `curl`) and a surface current **K**_b = **M**×n̂ (Eq. 6.14, via the MA-01
`cross`). These are the magnetic mirror of `~EM-07`'s bound charge. A uniformly
magnetized cylinder, **M** = M ẑ, has no interior current (∇×**M** = 0) but a side
current **K**_b = M φ̂ — it is a **solenoid**.

Folding the bound current into Ampère's law isolates the free current behind an
**auxiliary field H = B/μ₀ − M** (Eq. 6.18), whose circulation reads the free
current alone: ∮**H**·d**l** = I_free,enc (Eq. 6.20). For **linear** media **M** is
proportional to **H**, **M** = χ_m**H** (Eq. 6.29), so **B** = μ**H** with
μ = μ₀(1+χ_m) (Eqs. 6.31, 6.33) — the magnetic permeability. Ferromagnets are
*not* linear: **M** depends on the history of **H**, tracing a **hysteresis** loop
with remanence and coercivity. Like `~EM-01`/`~EM-08`, **M**, **B**, **H** are
returned as field functions `(x,y,z) -> (·,·,·)`, so MA-02 operators act on them
directly. SI units throughout (**M**, **H** in A/m; **B** in T; χ_m, μ_r
dimensionless).

## Operations — `code/magnetic_materials.py`

| call | meaning | reference (printed page) |
|------|---------|--------------------------|
| `bound_volume_current(M_field, point)` | **J**_b = ∇×**M**, bound volume current (reuses MA-02 `curl`); 0 where **M** is uniform | Gr §6.2.1 Eq.6.13 p.274 |
| `bound_surface_current(M, normal)` | **K**_b = **M**×n̂, bound surface current (reuses MA-01 `cross`) | Gr §6.2.1 Eq.6.14 p.274 |
| `auxiliary_field_H(B, M)` | **H** = **B**/μ₀ − **M**, sourced by free current alone | Gr §6.3.1 Eq.6.18 p.279 |
| `magnetization_linear(chi_m, H)` | **M** = χ_m**H** (linear medium) | Gr §6.4.1 Eq.6.29 p.284 |
| `permeability(chi_m)` | μ = μ₀(1+χ_m) | Gr §6.4.1 Eq.6.33 p.284 |
| `B_linear(chi_m, H)` | **B** = μ**H** (linear medium) | Gr §6.4.1 Eq.6.31 p.284 |
| `classify_material(chi_m)` | dia- / para- / ferromagnetic from sign & size of χ_m | Gr §6.4.1–6.4.2 p.284, 288 |
| `magnetized_sphere_inner_B(M)` | uniform **B** = ⅔μ₀**M** inside a uniformly magnetized sphere | Gr §6.2.1 Ex.6.1 p.274 † |
| `magnetized_sphere_inner_H(M)` | uniform **H** = −**M**/3 inside (the demagnetizing field) | Gr §6.3.1 Eq.6.18 p.279 |
| `hysteresis_branches(Ms, Hc, width)` | two-branch tanh model of an open hysteresis loop | Gr §6.4.2 p.288 |
| `remanence(Ms, Hc, width)` | remanent \|**M**\| left at **H** = 0 | Gr §6.4.2 p.288 |
| `coercivity(Ms, Hc, width)` | coercive field H_c that returns **M** to zero | Gr §6.4.2 p.288 |

Constant: `MU0` (μ₀, vacuum permeability) is imported from `~EM-08`
(`magnetostatics.MU0`). `chi_m` is the dimensionless magnetic susceptibility;
**M**, **B**, **H** are field functions `(x,y,z) -> (·,·,·)` — the MA-02
vector-field convention, so `curl` acts on **M** with no glue code.

† Ex. 6.1 (the uniformly magnetized sphere, **B**_in = ⅔μ₀**M**, the code's
Eq. 6.16) sits just past the §6.2.1 heading; the citation map verifies the section
anchor (p.274), not the example's own page — see `refs.md`.

## Use
```python
from magnetic_materials import (
    bound_volume_current, bound_surface_current, auxiliary_field_H,
    permeability, classify_material, magnetized_sphere_inner_B,
)
from magnetostatics import MU0                          # ~EM-08, chained onto the path

M = lambda x, y, z: (0.0, 0.0, 1e4)                     # uniformly magnetized along z
bound_volume_current(M, (0.1, 0.2, 0.0))               # ~ (0,0,0): J_b = curl M = 0 (uniform)
bound_surface_current((0, 0, 1e4), (1, 0, 0))          # (0, 1e4, 0): K_b = M phi-hat -> a solenoid

classify_material(-1.7e-5)                              # 'diamagnetic'  (chi_m < 0)
permeability(5500.0) / MU0                             # ~ 5501: mu/mu0 for soft iron

Bin = magnetized_sphere_inner_B((0, 0, 8e5))           # (0,0,0.670): B = (2/3) mu0 M, uniform inside
H = auxiliary_field_H(lambda x, y, z: Bin, lambda x, y, z: (0, 0, 8e5))
H(0, 0, 0)                                              # (0,0,-2.67e5) = -M/3, the demagnetizing field
```

## Run
```bash
cd code
python3 magnetic_materials.py          # demo: magnetized cylinder, linear media, sphere, hysteresis
python3 test_magnetic_materials.py     # tests  ->  "All 7 tests passed."
```
(`magnetic_materials.py` adds `~EM-08`'s `code/` to `sys.path`, which in turn
chains MA-01/MA-02; this collapses to `from physkit… import …` once the shared
package exists.)

## Files
- `notes.md` — derivations with inline page citations
- `code/magnetic_materials.py`, `code/test_magnetic_materials.py`
- `problems/problems.md` — worked problems (Griffiths Ch. 6)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
