# CM-22 — Problems

Work by hand, then check with `code/continuum_mechanics.py`. Citations in `../refs.md`.

### P1.  Derive continuity from the divergence theorem  *(Boas 3e §6.10, p.317)*
Equate the rate of mass loss from a fixed volume to the flux through its boundary
and shrink the volume to get ∂ρ/∂t + ∇·(ρv) = 0. *Check:* `continuity_residual`
~0 for an advected density bump ρ = f(x − ct), v = (c,0,0).
*Answer:* $\dfrac{\partial\rho}{\partial t}+\nabla\cdot(\rho\mathbf v)=0$.

**Solution.** Let $\Omega$ be a fixed volume bounded by $\partial\Omega$. Its mass $M=\int_\Omega\rho\,dV$
changes only through flux of $\mathbf j=\rho\mathbf v$ across the surface:
$$\frac{d}{dt}\int_\Omega\rho\,dV=-\oint_{\partial\Omega}\rho\mathbf v\cdot d\mathbf A=-\int_\Omega\nabla\cdot(\rho\mathbf v)\,dV,$$
the last step by the divergence theorem. The volume is fixed, so $d/dt$ passes inside as $\partial/\partial t$,
giving $\int_\Omega\big[\partial_t\rho+\nabla\cdot(\rho\mathbf v)\big]\,dV=0$. Since $\Omega$ is arbitrary the
integrand must vanish pointwise:
$$\frac{\partial\rho}{\partial t}+\nabla\cdot(\rho\mathbf v)=0.$$
For an advected bump $\rho=f(x-ct),\ \mathbf v=(c,0,0)$: $\partial_t\rho=-c f'$ and
$\nabla\cdot(\rho\mathbf v)=\partial_x(cf)=c f'$ cancel, so `continuity_residual` $\approx-1.7\times10^{-11}\approx0$, as reported.

### P2.  Eulerian ↔ material form  *(Boas 3e §6.10, p.317)*
Use ∇·(ρv) = ρ∇·v + v·∇ρ to show continuity is Dρ/Dt + ρ∇·v = 0. *Check:* the two
forms agree numerically for a compressible flow.
*Answer:* $\dfrac{D\rho}{Dt}+\rho\,\nabla\cdot\mathbf v=0$.

**Solution.** Expand the flux divergence with the product rule,
$$\nabla\cdot(\rho\mathbf v)=\rho\,\nabla\cdot\mathbf v+\mathbf v\cdot\nabla\rho,$$
and substitute into the Eulerian form $\partial_t\rho+\nabla\cdot(\rho\mathbf v)=0$:
$$\frac{\partial\rho}{\partial t}+\mathbf v\cdot\nabla\rho+\rho\,\nabla\cdot\mathbf v=0.$$
The first two terms are the material derivative $\dfrac{D\rho}{Dt}=\partial_t\rho+\mathbf v\cdot\nabla\rho$
(the rate of change following a fluid element), leaving $\dfrac{D\rho}{Dt}+\rho\,\nabla\cdot\mathbf v=0$.
The two forms are algebraically identical, which the code confirms: for the compressible test flow the
Eulerian residual equals $D\rho/Dt+\rho\,\nabla\cdot\mathbf v$ to machine precision (demo: $1.39000$ vs $1.39000$).

### P3.  Incompressible flow  *(Boas 3e §6.10, p.316)*
Show that for ∇·v = 0 the density is constant following the flow (Dρ/Dt = 0).
*Check:* `divergence_of_velocity` = 0 and `continuity_residual` = 0 for v = (−y,x,0),
constant ρ.
*Answer:* $\nabla\cdot\mathbf v=0\Rightarrow D\rho/Dt=0$ — density is carried unchanged by the flow.

**Solution.** Begin from the material form (P2), $\dfrac{D\rho}{Dt}+\rho\,\nabla\cdot\mathbf v=0$.
**Incompressible** means $\nabla\cdot\mathbf v=0$, so the second term vanishes and
$$\frac{D\rho}{Dt}=0,$$
i.e. each fluid element keeps its density as it moves. The rigid rotation $\mathbf v=(-y,x,0)$ is
divergence-free, $\nabla\cdot\mathbf v=\partial_x(-y)+\partial_y(x)+\partial_z(0)=0$, so with uniform $\rho$
there is nothing to compress: $\partial_t\rho=0$ and $\nabla\cdot(\rho\mathbf v)=\rho\,\nabla\cdot\mathbf v=0$.
Hence `divergence_of_velocity` $=0$ and `continuity_residual` $=0$, exactly as the test checks.

### P4.  Charge conservation is the same equation  *(Griffiths 4e §8.1.1, p.356)*
Write the continuity equation for electric charge, ∂ρ/∂t + ∇·J = 0, and explain
why it is "the paradigm for all conservation laws" (`~EM-13`).
*Answer:* $\dfrac{\partial\rho}{\partial t}+\nabla\cdot\mathbf J=0$ — the same operator, with charge density and current $\mathbf J=\rho\mathbf v$.

**Solution.** Charge is locally conserved just as mass is. Take $\rho$ to be charge density and
$\mathbf J=\rho\mathbf v$ the current density (charge flux); the identical divergence-theorem argument as
P1 — the charge in $\Omega$ changes only by current through $\partial\Omega$ — gives
$$\frac{\partial\rho}{\partial t}+\nabla\cdot\mathbf J=0.$$
It is "the paradigm for all conservation laws" because it is the **local** statement. Mere global
conservation $\frac{d}{dt}\int\rho\,dV=0$ would still allow charge to vanish here and reappear far away;
continuity forbids that — any change in $\rho$ must be balanced by current through the immediately
surrounding surface. Structurally it is the very operator $\partial_t\rho+\nabla\cdot(\rho\mathbf v)$ that
`continuity_residual` evaluates, with only the conserved density renamed mass $\to$ charge.

### P5.  Probability current  *(→ `~QM-04`)*
State the quantum continuity equation ∂|Ψ|²/∂t + ∇·j = 0 and identify the
probability current j. *(Same structure as mass and charge — the bridge.)*
*Answer:* $\dfrac{\partial|\Psi|^2}{\partial t}+\nabla\cdot\mathbf j=0$ with $\mathbf j=\dfrac{\hbar}{m}\,\mathrm{Im}(\Psi^*\nabla\Psi)$.

**Solution.** Take the conserved density to be the probability density $\rho=|\Psi|^2=\Psi^*\Psi$.
Differentiating in time and using the Schrödinger equation
$i\hbar\,\partial_t\Psi=-\dfrac{\hbar^2}{2m}\nabla^2\Psi+V\Psi$ (with $V$ real) yields a local conservation
law of the now-familiar form
$$\frac{\partial|\Psi|^2}{\partial t}+\nabla\cdot\mathbf j=0,\qquad
\mathbf j=\frac{\hbar}{2mi}\big(\Psi^*\nabla\Psi-\Psi\nabla\Psi^*\big)=\frac{\hbar}{m}\,\mathrm{Im}(\Psi^*\nabla\Psi),$$
where $\mathbf j$ is the **probability current**. This is the same equation as mass continuity (P1) and
charge continuity (P4), now with probability as the conserved density — the reason this module is KEY
BRIDGE B2: one structure $\partial_t\rho+\nabla\cdot\mathbf j$, the operator `continuity_residual` encodes,
carried over to `~QM-04`.
