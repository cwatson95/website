# RE-10 — The Equivalence Principle

Module of the **RELATIVITY** trunk (see `modules/topic_network.txt`). The hinge
between special and general relativity: how the single fact that *everything falls
the same way* forces gravity to be the **geometry of spacetime** — and how
redshift, light bending and horizons follow with **no field equations**.

- **Prerequisites:** `RE-03` (Lorentz boosts / Doppler), `RE-09` (metric, geodesics).
  Soft: `~CM-11` (Newtonian `GM/r²` field).
- **Feeds into:** `~RE-11` (curvature & geodesic deviation — the tidal field made
  precise), `~RE-14` (Schwarzschild horizons; the Rindler horizon is the local
  seed), `~QF-05` (the Unruh effect on the accelerated observer).

## Scope
The **weak EP** (universality of free fall, `m_inertial = m_grav`, Eötvös tests);
**Einstein's EP** ("the happiest thought" — a uniformly accelerated frame is locally
a uniform gravitational field, and free fall is locally inertial); **gravitational
redshift and time dilation** from the EP alone; the **accelerating-elevator** light-
bending argument (and its famous factor-of-two shortfall); **Rindler observers and
horizons**; and the **tidal field** as the irreducible, non-removable remainder that
*is* spacetime curvature.

## Conventions — a deliberate departure
The rest of the RE trunk sets `c = 1`; **this module keeps `c, g, G` explicit in
SI**, because it is about *realistic gravitational numbers* (a 22.5 m tower, a 1-g
horizon at 0.97 light-years, Earth's tides) whose magnitudes are the whole point.
`c = 2.99792458×10⁸ m/s`, `g = 9.80665 m/s²`, `G = 6.674×10⁻¹¹`. Potentials `Φ` in
J/kg, `Φ→0` at infinity, `Φ<0` deeper in a well.

## The one idea
**A freely falling observer feels no gravity** (Einstein, 1907). A uniformly
accelerated frame is *locally* indistinguishable from a uniform gravitational field,
so free fall *locally removes* gravity. What it cannot remove — the **tidal**
difference between neighbouring free-fallers — is curvature:

```
free fall kills the uniform field  ∂Φ   (the "force")
free fall keeps the tidal tensor   ∂∂Φ   (the curvature)   →  gravity = geometry
```

## Operations — `code/equivalence_principle.py`
| call | meaning |
|------|---------|
| `grav_redshift(delta_phi)` | `Δf/f = −ΔΦ/c²` (climb out ⇒ redshift) |
| `redshift_uniform_field(g, h)` | `−gh/c²` for a photon rising `h` in field `g` |
| `pound_rebka(h=22.5, g=…)` | `|Δf/f| = gh/c²` ≈ `2.45e-15` (Harvard tower) |
| `accelerated_frame_redshift(a, h)` | `−ah/c²` in a rocket — **== field(g=a)** |
| `grav_time_dilation(phi_lower, phi_upper)` | clock-rate ratio `dτ_lo/dτ_up < 1` |
| `rindler_horizon(a)` | `c²/a` — horizon behind an accelerated observer |
| `light_deflection_elevator(g, L)` | `(drop = ½g(L/c)², angle = gL/c²)` |
| `tidal_acceleration(M, r, dr)` | `2GM·dr/r³` — irreducible stretch (curvature) |
| `eotvos_parameter(a1, a2)` | `2|a₁−a₂|/(a₁+a₂)` — WEP figure of merit |

## Use
```python
from equivalence_principle import (
    pound_rebka, accelerated_frame_redshift, redshift_uniform_field,
    rindler_horizon, tidal_acceleration, eotvos_parameter)

pound_rebka()                                  # 2.455e-15  (g·22.5/c²)
accelerated_frame_redshift(9.8, 22.5) == redshift_uniform_field(9.8, 22.5)  # THE equivalence
rindler_horizon(9.80665)                       # 9.17e15 m ≈ 0.97 light-years
tidal_acceleration(5.972e24, 6.371e6, 1.0)     # 3.08e-6 m/s²  (≠ 0: curvature is real)
eotvos_parameter(9.8, 9.8)                      # 0.0  (universality of free fall)
```

## Run
```bash
cd code
python3 equivalence_principle.py        # demo: WEP, redshift, equivalence, horizon, tides
python3 test_equivalence_principle.py   # 11 property-based tests -> "All 11 tests passed."
```

## Files
- `notes.md` — WEP/Eötvös, the happiest thought, redshift & time dilation, light
  bending (the factor of 2), Rindler horizons, tides as curvature, gravity = geometry
- `code/equivalence_principle.py` — the library (pure stdlib `math`; SI units)
- `code/test_equivalence_principle.py` — the equivalence as numerical identity,
  Pound–Rebka value, redshift↔clock consistency, `1/r³` tidal scaling, Eötvös
- `problems/problems.md` — worked problems (Zee §V, Will Ch. 2, Pope notes)
- `refs.md` — verified textbook citations
