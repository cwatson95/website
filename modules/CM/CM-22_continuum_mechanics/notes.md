# CM-22 — Continuum Mechanics & the Continuity Equation (notes)

Citation keys (details + PDF pages in `refs.md`): **B** = Boas 3e ·
**Gr** = Griffiths 4e.

## The continuity equation
Take a fixed volume; the rate of decrease of the mass inside equals the net
outflow through its surface. Shrinking the volume (the divergence-theorem
argument) gives the **local** statement [B §6.10 p.317]:
$$\boxed{\ \frac{\partial\rho}{\partial t}+\nabla\cdot(\rho\mathbf v)=0\ }$$
with mass flux **j** = ρ**v**. Code: `continuity_residual`. A density bump
advected at constant velocity, ρ = f(x − ct), satisfies it exactly (a test).

## Eulerian vs material form
Using ∇·(ρv) = ρ∇·v + v·∇ρ and the **material derivative**
$$\frac{D}{Dt}=\frac{\partial}{\partial t}+\mathbf v\cdot\nabla$$
(the rate of change *following a fluid element*), continuity is equivalently
$$\frac{D\rho}{Dt}+\rho\,(\nabla\cdot\mathbf v)=0.$$
For **incompressible** flow (∇·v = 0) the density is constant on fluid elements.
Code: `material_derivative`, `divergence_of_velocity`; the test verifies the two
forms agree for a compressible flow.

## Why this is KEY BRIDGE B2
The identical equation, with a different conserved density, is:
- **electric charge** ∂ρ/∂t + ∇·**J** = 0 [Gr §5.1.3 p.222, named there; §8.1.1
  p.356 calls it "the paradigm for all conservation laws"] — `~EM-13`;
- **quantum probability** ∂|Ψ|²/∂t + ∇·**j** = 0 — `~QM-04`.

One conservation law, three densities (mass, charge, probability). With `~EM-14`
now built, the deferred `~QM-04` (probability current) can be filled from this
template.
