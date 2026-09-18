# CM-02 — Equation of Motion (notes)

Citation key (details + PDF pages in `refs.md`): **F** = Fowles & Cassiday 7e.

## Newton's laws
1. A free body moves at constant velocity (defines inertial frames, `~CM-03`).
2. **F = dp/dt = m a** for constant mass — the equation of motion [F §2.1 p.47].
3. Forces come in equal-and-opposite pairs (→ momentum conservation, `~CM-06`).

## The equation of motion as an ODE
For a particle, [F §4.1 p.144]
$$m\frac{d^2\mathbf r}{dt^2}=\mathbf F(t,\mathbf r,\dot{\mathbf r}).$$
This is a second-order ODE. Writing the state as **y** = [**r**, **v**], it
becomes first order,
$$\frac{d}{dt}\begin{bmatrix}\mathbf r\\ \mathbf v\end{bmatrix}
 =\begin{bmatrix}\mathbf v\\ \mathbf F/m\end{bmatrix},$$
which `trajectory` integrates with **MA-07's RK4** (`~MA-07`). The free-body
principle — net force is the vector sum of the applied forces — is `sum_forces`.

## Worked forces and their motions
- **Constant force / uniform gravity** → parabola (recovers the projectile of `~CM-01`).
- **Spring** F = −k**r** → simple harmonic motion, ω = √(k/m) (`~CM-15`).
- **Linear drag** F = −b**v** added to gravity → exponential approach to the
  terminal velocity v∞ = −mg/b (a test).

These trajectories are the input to the energy and momentum bookkeeping of
`~CM-04`, `~CM-05`, `~CM-06`.
