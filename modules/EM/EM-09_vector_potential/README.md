# EM-09 — Magnetic Vector Potential

Ninth module of the **ELECTRICITY & MAGNETISM** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~EM-08` (magnetostatics — the wire and loop **B** fields this
  must reproduce, plus the ∇·**B** = 0 result that makes a potential possible),
  `~MA-02` (`curl` to take **B** = ∇×**A**, `divergence` to test the gauge).
- **Feeds into:** — (no built-out EM module depends on it yet). Cross-links:
  `~EM-05` (the electric-dipole analogue it mirrors term-for-term) and `~QF-03`
  (gauge invariance — the field-theory descendant of the gauge freedom
  **A** → **A** + ∇λ).

## Scope
Magnetostatics (`~EM-08`) closed with two facts about **B**: ∇·**B** = 0 and
∇×**B** = μ₀**J**. The first is the subject here. Because **B** is divergence-free
*everywhere*, it can always be written as the curl of a **vector potential**,
**B** = ∇×**A** (Eq. 5.59) — the magnetic mirror of **E** = −∇V (`~EM-03`). **A**
is not unique: any **A** → **A** + ∇λ leaves **B** unchanged (the **gauge
freedom**), and the **Coulomb gauge** ∇·**A** = 0 spends that freedom to turn
Ampère's law into the vector Poisson equation ∇²**A** = −μ₀**J**.

A vector potential is returned as a **function** `A(x, y, z) -> (Ax, Ay, Az)` —
the same MA-02 vector-field convention `~EM-08` uses for **B** — so MA-02's `curl`
takes **B** = ∇×**A** and `divergence` tests the gauge with no glue code. The
headline object is the magnetic **dipole** **A** = (μ₀/4π) **m**×**r̂**/r² (Eq. 5.85)
of a current loop with moment **m** = I**a** (Eq. 5.86), whose curl reproduces
both the closed-form dipole field *and* — for a straight wire — EM-08's
B = μ₀I/2πs. SI units throughout.

## Operations — `code/vector_potential.py`

| call | meaning | reference (printed page) |
|------|---------|--------------------------|
| `magnetic_dipole_moment(I, area_vector)` | **m** = I**a** (current × oriented area) | Gr §5.4.3 Eq.5.86 p.252 |
| `dipole_vector_potential(m)` | **A** = (μ₀/4π)(**m**×**r̂**)/r² of a dipole at the origin | Gr §5.4.3 Eq.5.85 p.252 |
| `dipole_B_field_closed(m)` | **B** = (μ₀/4π)(1/r³)[3(**m**·**r̂**)**r̂** − **m**] | Gr §5.4.3 p.252 (cf. `~EM-05` Eq.3.104) |
| `B_from_A(A)` | **B** = ∇×**A** (reuses MA-02 `curl`) | Gr §5.4.1 Eq.5.59 p.243 |
| `coulomb_gauge_residual(A, point)` | ∇·**A** check (reuses MA-02 `divergence`), normalized | Gr §5.4.1 p.243 (∇·**A**=0) |
| `wire_vector_potential(I, s0)` | **A** = −(μ₀I/2π)ln(s/s0)**ẑ** of an infinite wire | Gr §5.4.1 p.243 |

Constants: `MU0` (μ₀, the permeability of free space) is imported from `~EM-08`;
the dipole prefactor is μ₀/4π. **r̂** is the unit vector from the dipole (at the
origin) to the field point; s = √(x²+y²) is the cylindrical radius from the wire's
axis.

## Use
```python
import math
from vector_potential import (magnetic_dipole_moment, dipole_vector_potential,
                              dipole_B_field_closed, B_from_A, wire_vector_potential)

m = magnetic_dipole_moment(3.0, (0, 0, math.pi*0.02**2))   # small current loop -> m = I a
A = dipole_vector_potential(m)                             # A(x,y,z), Eq. 5.85
A(0.1, 0.0, 0.0)                                           # ~ (0, +Ay, 0): A circles the m axis

B_from_A(A)(0.1, 0.05, 0.08)                               # B = curl A (MA-02) ...
dipole_B_field_closed(m)(0.1, 0.05, 0.08)                 # ... equals the closed-form dipole field

Aw = wire_vector_potential(10.0)                          # infinite wire on the z-axis
B_from_A(Aw)(0.05, 0.0, 0.0)                              # ~ (0, +By, 0): EM-08's encircling wire field
```

## Run
```bash
cd code
python3 vector_potential.py        # demo: loop -> m, B = curl A vs closed form, gauge, the wire
python3 test_vector_potential.py   # tests  ->  "All 6 tests passed."
```
(`vector_potential.py` reaches `~EM-08` by relative path, which in turn chains
`~MA-01`/`~MA-02`; this becomes `from physkit… import …` once the shared package
exists.)

## Files
- `notes.md` — derivations with inline page citations
- `code/vector_potential.py`, `code/test_vector_potential.py`
- `problems/problems.md` — worked problems (Griffiths Ch. 5)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
