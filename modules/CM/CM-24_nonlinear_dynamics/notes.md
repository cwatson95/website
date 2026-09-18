# CM-24 — Nonlinear Dynamics & Chaos (notes)

Citation key (details in `refs.md`): the dynamical-systems mathematics is `~MA-22`
(Chicone §1.6).

## Mechanics as a flow in phase space
A mechanical system is a flow **ẋ** = **f**(**x**) on phase space (`~CM-19`). Its
**fixed points** (f = 0) and their linear stability — read off the eigenvalues of
the **Jacobian** there — organize the whole portrait. Code: `jacobian`,
`classify_fixed_point` reuses `~MA-22`'s `classify_equilibrium` (saddle / node /
spiral / center).

- **Pendulum** ẋ = (ω, −sin θ − γω): the bottom (0,0) is a **center** when
  undamped and a **stable spiral** when damped; the inverted point (π,0) is a
  **saddle** either way (tests).

## Limit cycles
Nonlinear systems can have isolated closed orbits that attract nearby
trajectories — **limit cycles**, impossible for a linear system. The **van der
Pol** oscillator ẍ − μ(1−x²)ẋ + x = 0 has one: the test integrates from inside and
outside and finds both settle to the *same* amplitude (≈ 2 for μ = 1).

## Chaos
Deterministic systems can show **sensitive dependence on initial conditions** —
nearby trajectories separate exponentially, at a rate set by the **Lyapunov
exponent** λ. The test reuses `~MA-22`: the logistic map at r = 4 is chaotic with
λ = ln 2 > 0, while at r = 2.5 (a stable fixed point) λ < 0. Chaos makes
long-term prediction impossible even though the laws are exact — the modern
descendant of the three-body problem.
