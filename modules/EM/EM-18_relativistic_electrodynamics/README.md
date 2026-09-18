# EM-18 — Relativistic Electrodynamics

Final module of the **ELECTRICITY & MAGNETISM** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~EM-01` (electrostatics — the field **E** and `EPS0`), `~EM-08`
  (magnetostatics — **B** and `MU0`, which together give `C` = 1/√(μ₀ε₀)), `~MA-01`
  (vector algebra — `dot`, reused by the field invariants).
- **Feeds into:** `~RE-08` (covariant formulation of special relativity — the same
  tensors, viewed from the relativity side), `~MA-16` (tensor analysis & index
  notation — the machinery F^{μν} is built from), `~QF-03` (gauge theories / QED —
  where F^{μν} becomes the field strength of the U(1) gauge potential).

## Scope
The payoff of the whole subject: **E** and **B** are not two separate fields but
the six independent components of one **antisymmetric field tensor** F^{μν}
(Gr Eq. 12.118). A **Lorentz boost** mixes them (Eq. 12.109), so a *pure* electric
field in one frame carries a *magnetic* field in another — **magnetism is
electrostatics seen from a moving frame** (§12.3.1), which is the deep reason a
wire that is neutral in the lab can still push on a moving charge.

Two scalar combinations survive every boost: **E·B** and **B²−E²/c²** are
**Lorentz-invariant** (Prob. 12.47). And the four Maxwell equations collapse into
the single **covariant** statement ∂_μF^{μν} = μ₀J^ν (§12.3.4). The tensor
machinery here is `~MA-16`; the covariant viewpoint, shared with the relativity
trunk, is `~RE-08`.

## Operations — `code/relativistic_electrodynamics.py`

| call | meaning | reference (printed page) |
|------|---------|--------------------------|
| `field_tensor(E, B)` | build F^{μν}; F^{0i}=E_i/c, F^{ij}=−ε_ijk B_k | Gr §12.3.3 Eq.12.118 p.562 |
| `fields_from_tensor(F)` | read (**E**, **B**) back off F^{μν} | Gr §12.3.3 Eq.12.118 p.562 |
| `is_antisymmetric(F)` | check F^{μν} = −F^{νμ} (diagonal vanishes) | Gr §12.3.3 p.562 |
| `boost_fields(E, B, beta)` | transform **E**, **B** to a frame at **v** = βc **x̂** | Gr §12.3.2 Eq.12.109 p.553 |
| `field_invariants(E, B)` | (E·B, B²−E²/c²), both boost-invariant | Gr §12.3.3 Prob.12.47 p.562 |
| `gamma(beta)` | Lorentz factor γ = 1/√(1−β²) | Gr §12.1 (Lorentz factor) |

Constants: `C` = 1/√(μ₀ε₀) (built from `EPS0` of `~EM-01` and `MU0` of `~EM-08`).
Fields are plain 3-tuples `(x, y, z)`; F^{μν} is a 4×4 list-of-lists ordered
(ct, x, y, z). The boost is along +**x̂** throughout.

## Use
```python
from relativistic_electrodynamics import (
    field_tensor, fields_from_tensor, boost_fields, field_invariants, gamma)

E = (0.0, 1000.0, 0.0)            # a pure, transverse E field (V/m); no B
B = (0.0, 0.0, 0.0)

F = field_tensor(E, B)            # the 4x4 antisymmetric field tensor F^{mu nu}
fields_from_tensor(F)             # -> ((0,1000,0), (0,0,0)): reads the fields back

gamma(0.6)                        # 1.25  (Lorentz factor for v = 0.6c)
Ep, Bp = boost_fields(E, B, 0.6)  # boost to v = 0.6c x-hat
Bp                                # ~ (0, 0, -2.5e-6) T: a magnetic field has appeared!

field_invariants(E, B)            # (0.0, -1.11e-11):  E.B and B^2 - E^2/c^2
field_invariants(Ep, Bp)          # the same two numbers -- both are boost-invariant
```

## Run
```bash
cd code
python3 relativistic_electrodynamics.py          # demo: build F, a boost makes B, check the invariants
python3 test_relativistic_electrodynamics.py     # tests  ->  "All 7 tests passed."
```
(`relativistic_electrodynamics.py` imports `EPS0` / `MU0` / `dot` from `~EM-01`,
`~EM-08`, `~MA-01` by relative path; this becomes `from physkit… import …` once
the shared package exists.)

## Files
- `notes.md` — derivations with inline page citations
- `code/relativistic_electrodynamics.py`, `code/test_relativistic_electrodynamics.py`
- `problems/problems.md` — worked problems (Griffiths §12.3)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
