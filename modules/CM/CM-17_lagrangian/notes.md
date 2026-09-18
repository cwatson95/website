# CM-17 — Lagrangian Mechanics (notes)

Citation keys (details + PDF pages in `refs.md`): **F** = Fowles & Cassiday 7e ·
**G** = Goldstein 3e *(image scan)* · **MT** = Marion & Thornton 5e *(image scan)*.

## Generalized coordinates and the Lagrangian
Choose any convenient **generalized coordinates** q describing the configuration
[F §10.2 p.423; G §1.3]. The dynamics follow from a single scalar, the
**Lagrangian** L = T − V, through **Hamilton's principle**: the actual path makes
the action ∫L dt stationary [G §2.1 p.34]. Stationarity is exactly the
calculus-of-variations problem of `~MA-13`.

## The Euler–Lagrange equation
Stationary action gives, for each coordinate [F §10.4 p.430; G §2.3 p.44]:
$$\frac{d}{dt}\frac{\partial L}{\partial\dot q}-\frac{\partial L}{\partial q}=0.$$
This is Newton's law written in *any* coordinates — no free-body diagrams. Code:
`el_residual` passes the mechanics Lagrangian straight to MA-13's
`euler_lagrange_residual` (t,q,q̇ ↔ x,y,y′); it is ~0 on a true trajectory and
large on a wrong one (a test). The pendulum L = ½l²θ̇² + gl cos θ yields
θ̈ = −(g/l) sin θ, whose integrated trajectory has ~0 residual (a test).

## Momentum and energy
- The **conjugate momentum** p = ∂L/∂q̇ (`generalized_momentum`); if a coordinate
  is **cyclic** (∂L/∂q = 0) its momentum is conserved (`~CM-18`).
- The **Jacobi energy** h = q̇ ∂L/∂q̇ − L equals T + V for L = T − V
  (`jacobi_energy`); it is the Hamiltonian of `~CM-19`, the ancestor being MA-13's
  Beltrami first integral.
