# CM-11 — Central-Force Motion (notes)

Citation keys (details + PDF pages in `refs.md`): **F** = Fowles & Cassiday 7e ·
**MT** = Marion & Thornton 5e *(image scan)*.

## Reduction to a 1-D radial problem
A central force **F** = f(r)**r̂** conserves angular momentum **L** (no torque,
`~CM-09`), so the motion stays in a plane and L = μr²θ̇ is constant. Energy
conservation then reads [F §6.9 p.251]
$$E=\tfrac12\mu\dot r^2+\underbrace{U(r)+\frac{L^2}{2\mu r^2}}_{U_{\rm eff}(r)},$$
a single particle of **reduced mass** μ (`~CM-07`) moving in the **effective
potential** U_eff. The L²/(2μr²) term is the centrifugal barrier. Code:
`effective_potential`.

## Circular orbits and Kepler's laws
For the attractive inverse-square potential U = −k/r [F §6.5 p.229; MT Ch.8 p.287]:
- **Circular orbit** at the minimum of U_eff: r₀ = L²/(μk) (`circular_orbit_radius`);
- **Kepler I** — bound orbits (E < 0) are ellipses [F §6.5];
- **Kepler II** — equal areas in equal times (constant L, `~CM-09`);
- **Kepler III** — T² ∝ a³, with T = 2π√(μa³/k) (`kepler_period`) [F §6.3 p.225].

The test integrates a circular orbit (radius constant) and a bound ellipse
(E < 0), checking that **both E and L are conserved** along the trajectory, and
that T²/a³ is the same for every orbit. This 1/r potential is one of the KEY
BRIDGES: the same algebra is the hydrogen atom (`~QM-12`) and, with corrections,
the Schwarzschild orbit (`~RE-14`).
