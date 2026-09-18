# EM-05 — Multipole Expansion

Fifth module of the **ELECTRICITY & MAGNETISM** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~EM-01` (the exact Coulomb field, `coulomb_field`, `K_E`, `EPS0`)
  and `~EM-03` (the exact potential `potential_point_charges`) — the truncated series
  is built from, and checked against, both. `~MA-01` (`norm`, `dot`, `unit`) is reused
  directly.
- **Feeds into:** `~EM-09` (magnetic-dipole analogue): the vector potential repeats this
  whole construction, and the magnetic dipole **A** = (µ₀/4π) **m×r̂**/r² is the
  term-by-term twin of **V** = (1/4πε₀) **p·r̂**/r².
- **Cross-links:** `~MA-12` (the Legendre polynomials `P_n` are the angular pieces of
  the expansion).

## Scope
Seen from far enough away, any **localized** charge cloud looks like a point charge;
look a little closer and the leading correction looks like a dipole, then a quadrupole.
The **multipole expansion** makes this precise: the potential of a bounded distribution
is a power series in $1/r$ (Gr Eq. 3.95, §3.4.1, p.151),
$V=\tfrac{1}{4\pi\varepsilon_0}\!\left[\tfrac{Q}{r}+\tfrac{\mathbf p\cdot\hat{\mathbf r}}{r^{2}}+\tfrac{(\text{quadrupole})}{r^{3}}+\dots\right]$
— the **monopole** ($1/r$, total charge $Q$), **dipole** ($1/r^2$, moment **p**),
**quadrupole** ($1/r^3$), … terms. Each successive term is smaller by one more factor
of $(\text{size}/r)$, so adding a term cuts the truncation error by another power of
$(\text{size}/r)$. For a neutral object ($Q=0$) the monopole vanishes and the **dipole
term dominates** the far field.

The module computes the moments (`monopole_moment`, `dipole_moment`, `quadrupole_moment`),
the pure-dipole potential and field (`dipole_potential`, `dipole_field`), and the
truncated series itself (`multipole_potential`), comparing each against the exact `~EM-03`
potential `potential_point_charges` (and the `~EM-01` field) as $r$ grows. Charges keep
the `~EM-01` convention — a charge is a pair `(q, position)` — and moments are taken about
the coordinate origin. `dipole_potential`/`dipole_field` return field **functions**
`V(x,y,z)` and `E(x,y,z) -> (Ex,Ey,Ez)` in the MA-02 style, so MA-02's `curl`/`divergence`
act on them with no glue code. SI units throughout.

## Operations — `code/multipole.py`

| call | meaning | reference (printed page) |
|------|---------|--------------------------|
| `monopole_moment(charges)` | total charge **Q** = Σ q_a (the n=0 moment) | Gr §3.4.2 p.154 |
| `dipole_moment(charges)` | **p** = Σ q_a **r'**_a (vector moment, Eq. 3.98) | Gr §3.4.2 Eq.3.98 p.154 |
| `quadrupole_moment(charges)` | traceless **Q**_ij = Σ q_a(3 r_i r_j − r²δ_ij) | Gr §3.4.1 p.151 (n=2 term) |
| `dipole_potential(p, source)` | V = (1/4πε₀) **p·r̂**/r² of a pure dipole | Gr §3.4.2 Eq.3.99 p.154 |
| `dipole_field(p, source)` | **E** = (k/r³)[3(**p·r̂**)**r̂** − **p**] | Gr §3.4.4 Eq.3.104 p.158 |
| `multipole_potential(charges, lmax)` | truncated far-field series Σ_{n≤lmax}, with P_n | Gr §3.4.1 Eq.3.95 p.151 |

`K_E` = 1/4πε₀ ≈ 8.99×10⁹ and `EPS0` (ε₀) are imported from `~EM-01`; in the formulas
`k` ≡ `K_E`. A charge is a pair `(q, position)`; `lmax` selects the highest term kept
(0 = monopole, 1 = +dipole, 2 = +quadrupole). Moments are taken about the coordinate
origin — see `notes.md` §3 for why that matters.

## Use
```python
from multipole import (monopole_moment, dipole_moment, dipole_potential,
                       dipole_field, multipole_potential)
from electric_potential import potential_point_charges     # ~EM-03, the exact V

q, a = 1e-9, 0.01
dip = [(q, (0, 0, a/2)), (-q, (0, 0, -a/2))]               # a physical +q,-q dipole

monopole_moment(dip)                                       # 0.0 C   (neutral)
dipole_moment(dip)                                         # (0, 0, q*a) = (0,0,1e-11) C·m

p = dipole_moment(dip)
dipole_potential(p)(0, 0, 100*a)                           # pure-dipole V = k p·r̂/r^2
multipole_potential(dip, lmax=1)(0, 0, 100*a)              # far-field V (monopole+dipole)
potential_point_charges(dip)(0, 0, 100*a)                  # the exact ~EM-03 value -- all three agree

dipole_field(p)(0, 0, 0.1)[2]                              # E_z on axis      =  2kp/r^3
dipole_field(p)(0.1, 0, 0)[2]                              # E_z on bisector  = -kp/r^3
```

## Run
```bash
cd code
python3 multipole.py            # demo: dipole moments, expansion vs exact V, dipole-field 2:1 structure
python3 test_multipole.py       # tests  ->  "All 6 tests passed."
```
(`multipole.py` imports `~EM-01`/`~EM-03` (and `~MA-01`) by relative path; this becomes
`from physkit… import …` once the shared package exists.)

## Files
- `notes.md` — derivations with inline page citations
- `code/multipole.py`, `code/test_multipole.py`
- `problems/problems.md` — worked problems (Griffiths §3.4)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
