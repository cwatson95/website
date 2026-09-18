# EM-01 — Electrostatics

First module of the **ELECTRICITY & MAGNETISM** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~MA-01` (vector algebra) — used directly (`norm`, `unit`, `dot`).
- **Feeds into:** `~EM-02` (Gauss's law — the flux and divergence of **E**), `~EM-03`
  (potential, since **E** is curl-free), `~EM-05` (multipole expansion), `~EM-06`
  (electrostatic energy & conductors).

## Scope
The starting point of the whole subject: **Coulomb's law**, the **electric field**
**E** as the force-per-unit-charge a source sets up, the **superposition principle**,
and the field of a **continuous charge distribution**. No potentials yet (that is
`~EM-03`) and no flux integrals yet (`~EM-02`).

A field is returned as a **function** `E(x, y, z) -> (Ex, Ey, Ez)` — exactly the
MA-02 convention for vector fields — so MA-02's differential operators act on an
EM field with no glue code. The fact that `curl(E) == 0` everywhere and
`divergence(E) == 0` off the charges is checked here and is the whole content of
`~EM-02`. SI units throughout; a *charge* is a pair `(q, position)`.

## Operations — `code/electrostatics.py`

| call | meaning | reference (printed page) |
|------|---------|--------------------------|
| `point_charge_field(q, source)` | **E** = (1/4πε₀) q/η² **η̂** of one charge | Gr §2.1.3 Eq.2.4 p.61 |
| `coulomb_field(charges)` | superposed **E** of many point charges | Gr §2.1.3 Eq.2.4 p.61 |
| `force_on_charge(Q, E)` | **F** = Q**E** on a test charge | Gr §2.1.3 Eq.2.3 p.61 |
| `field_magnitude(E)` | \|**E**\|(x,y,z) (reuses MA-01 `norm`) | Gr §2.1.2 p.60 |
| `field_line_direction(E)` | **Ê** = **E**/\|**E**\| (reuses MA-01 `unit`) | Gr §2.1.3 p.61 |
| `field_of_distribution(rho, …)` | **E** = (1/4πε₀)∫(**η̂**/η²)ρ dτ' (box) | Gr §2.1.4 Eq.2.8 p.63 |

Constants: `EPS0` (ε₀), `K_E` = 1/4πε₀ ≈ 8.99×10⁹, `ELEM_CHARGE` (e). Here **η** = (field
point) − (source point) is Griffiths' "script-r" separation vector.

## Use
```python
from electrostatics import point_charge_field, coulomb_field, force_on_charge, ELEM_CHARGE, K_E
from vector_calculus import curl, divergence          # ~MA-02, straight onto the field

E = point_charge_field(ELEM_CHARGE)                    # a proton's field, E(x,y,z)
E(5.29e-11, 0, 0)                                      # ~ (5.14e11, 0, 0) V/m at the Bohr radius

pair = coulomb_field([(1e-9, (-0.01, 0, 0)), (1e-9, (0.01, 0, 0))])
pair(0, 0, 0)                                          # (0,0,0): cancels by symmetry

curl(E)(0.4, 0.3, -0.2)                                # ~ (0,0,0): electrostatics is irrotational
divergence(E)(0.4, 0.3, -0.2)                          # ~ 0 in charge-free space (~EM-02)
```

## Run
```bash
cd code
python3 electrostatics.py          # demo: proton field, superposition, curl/div, a charged cube
python3 test_electrostatics.py     # tests  ->  "All 6 tests passed."
```
(`electrostatics.py` imports MA-01/MA-02 by relative path; this becomes
`from physkit… import …` once the shared package exists.)

## Files
- `notes.md` — derivations with inline page citations
- `code/electrostatics.py`, `code/test_electrostatics.py`
- `problems/problems.md` — worked problems (Griffiths Ch. 2)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
