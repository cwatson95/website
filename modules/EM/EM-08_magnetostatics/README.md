# EM-08 — Magnetostatics

Eighth module of the **ELECTRICITY & MAGNETISM** trunk (see `modules/topic_network.txt`) —
where the magnetic field **B** enters, the steady-current counterpart of EM-01's
electrostatics.

- **Prerequisites:** `~MA-01` (vector algebra) — `cross` is the heart of every magnetic
  formula (`dot`, `norm` too); `~MA-02` (vector calculus) — `line_integral` for the
  Ampère circulation, `divergence` for ∇·**B** = 0.
- **Feeds into:** `~EM-09` (magnetic vector potential — because ∇·**B** = 0, **B** = ∇×**A**),
  `~EM-10` (magnetic materials — bound currents and the **H** field); later `~EM-11`
  (induction) and `~EM-13` (Maxwell) add the time dependence.

## Scope
The magnetic field **B** enters through the force it exerts. The magnetic force on a
charge $Q$ moving with velocity **v** is **F** = Q(**v**×**B**) (Eq. 5.1), and on a
current-carrying wire **F** = ∫I d**l**×**B** (Eq. 5.16) — both **cross products**
(MA-01 `cross`), so the magnetic force is always perpendicular to the motion and **does
no work**. The sources are **steady currents**: the **Biot–Savart law** (Eq. 5.39) gives
**B** of any steady current, the magnetic analogue of Coulomb's law in `~EM-01`.

The structure of **B** is the magnetostatic half of Maxwell's equations: ∇·**B** = 0
(Eq. 5.50 — no magnetic monopoles) and ∇×**B** = μ₀**J** (Eq. 5.56), whose integral form
is **Ampère's law** ∮**B**·d**l** = μ₀I_enc (Eq. 5.57). A field is returned as a function
`B(x, y, z) -> (Bx, By, Bz)` — exactly the MA-02 convention for vector fields — so MA-02's
`divergence` confirms ∇·**B** = 0 with no glue code and `line_integral` runs the Ampère
circulation directly. SI units throughout; a current is a scalar $I$ with a geometry (a
path or an axis).

## Operations — `code/magnetostatics.py`

| call | meaning | reference (printed page) |
|------|---------|--------------------------|
| `lorentz_force(Q, v, B)` | **F** = Q(**E** + **v**×**B**); magnetic part Q **v**×**B** (MA-01 `cross`) | Gr §5.1.2 Eq.5.1 p.212 |
| `force_on_wire(I, dl, B)` | **F** = I(d**l**×**B**) on a current element | Gr §5.1.3 Eq.5.16 p.216 |
| `biot_savart(I, path, a, b)` | **B** = (μ₀I/4π)∫(d**l'**×**η̂**)/η² along a curve | Gr §5.2.2 Eq.5.39 p.224 |
| `circular_loop_field(I, R)` | **B** of a circular current loop (Biot–Savart, numeric) | Gr §5.2.2 Eq.5.39 p.224 |
| `loop_axis_field_closed(I, R, z)` | B_z = μ₀IR²/2(R²+z²)^{3/2} on the axis | Gr §5.2.2 Eq.5.41 p.224 |
| `infinite_wire_field(I)` | \|**B**\| = μ₀I/2πs, azimuthal (**φ̂**, right-hand rule) | Gr §5.2.2 Eq.5.36 p.224 |
| `ampere_circulation(B, s)` | ∮**B**·d**l** = μ₀I_enc round a circle (MA-02 `line_integral`) | Gr §5.3.3 Eq.5.57 p.233 |
| `div_B_residual(B, point)` | local ∇·**B** = 0 check (MA-02 `divergence`) | Gr §5.3.2 Eq.5.50 p.231 |

Constant: `MU0` (μ₀ ≈ 1.257×10⁻⁶ T·m/A ≈ 4π×10⁻⁷), the permeability of free space. As in
EM-01, **η** = (field point) − (source point) is Griffiths' "script-r" separation vector.
The on-axis loop (Eq. 5.41) lives in §5.2.2; the citation map fixes that section at p.224.

## Use
```python
from magnetostatics import (lorentz_force, infinite_wire_field, ampere_circulation,
                            circular_loop_field, loop_axis_field_closed, MU0)
from vector_calculus import divergence              # ~MA-02, straight onto the field

lorentz_force(1.602e-19, (1e6, 0, 0), (0, 0, 0.5))  # ~ (0,-8.0e-14,0): along -y, perp to v
                                                     # (magnetic force does no work)

B = infinite_wire_field(10.0)                        # 10 A along z; B(x,y,z) azimuthal
B(0.05, 0, 0)                                         # ~ (0, 4.0e-5, 0) T at s = 5 cm
ampere_circulation(B, 0.03)                           # ~ mu0*10: Ampère, independent of radius
divergence(B)(0.04, 0.02, 0.0)                        # ~ 0: no magnetic monopoles (div B = 0)

loop = circular_loop_field(5.0, 0.1)                  # 5 A loop, R = 10 cm (Biot–Savart)
loop(0, 0, 0)[2]                                       # ~ mu0*5/(2*0.1): matches the closed form
loop_axis_field_closed(5.0, 0.1, 0.0)                 #   mu0 I / 2R at the centre
```

## Run
```bash
cd code
python3 magnetostatics.py          # demo: Lorentz force, infinite wire + Ampère, loop on axis
python3 test_magnetostatics.py     # tests  ->  "All 7 tests passed."
```
(`magnetostatics.py` chains MA-01/MA-02 onto `sys.path` by relative path; this becomes
`from physkit… import …` once the shared package exists.)

## Files
- `notes.md` — derivations with inline page citations
- `code/magnetostatics.py`, `code/test_magnetostatics.py`
- `problems/problems.md` — worked problems (Griffiths Ch. 5)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
