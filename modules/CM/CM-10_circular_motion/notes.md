# CM-10 — Centripetal & Circular Motion (notes)

Citation key (details + PDF pages in `refs.md`): **F** = Fowles & Cassiday 7e.

## Uniform circular motion
A particle on a circle of radius R at angular velocity ω has
**r**(t) = (R cos ωt, R sin ωt, 0), so its speed is v = Rω (constant) and its
acceleration points **inward** with magnitude [F §1.11 p.38]
$$a_c=\frac{v^2}{R}=\omega^2 R.$$
This is the **centripetal acceleration**; the force that supplies it (gravity,
tension, the Coulomb force, …) is F_c = m v²/R. Code: `centripetal_acceleration`,
`centripetal_force`. The period and frequency are T = 2π/ω, f = 1/T.

## Connection to curvature (CM-01)
Fowles derives a_c not as a special case but inside the general plane-polar
kinematics [F §1.11 p.36]: the radial acceleration is r̈ − rθ̇², which for a circle
(r = R fixed) is −Rθ̇² = −v²/R. In `~CM-01` language a circle has **curvature**
κ = 1/R and **normal acceleration** a_N = v²/R, and the full acceleration is
**a** = −ω²**r** (pointing to the centre). The test cross-checks all three —
`speed`, `curvature`, `normal_acceleration` from CM-01 — against the circular-motion
formulas here. The same v²/R reappears as the effective "centrifugal" term in the
rotating-frame treatment `~CM-12`.
