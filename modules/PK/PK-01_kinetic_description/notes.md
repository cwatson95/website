# PK-01 — Kinetic Description — Distribution Functions, Vlasov & Boltzmann (notes)

A plasma sits between two pictures: too many particles to track individually, too
collisionless to treat as a simple thermal fluid. The kinetic description follows
one smooth field — the one-particle distribution function f(x,v,t) in phase space.
Equilibrium fixes f to the Maxwellian (`~SM-06`); its evolution is the Boltzmann
equation, whose collisionless, self-consistent limit — the **Vlasov equation** — is
just the continuity equation for phase-space density (`~CM-22`, `~QM-04`). The
collective scales λ_D, ω_p, Λ say when that mean-field picture is valid.

Citation key (full details in `refs.md`): **Mi** = Michel, *Introduction to
Laser-Plasma Interactions* (§1.2; Appendix A.1); **Rh** = Rhodes (ed.), *Excimer
Lasers*; **Pa** = Pathria 3e.

## 1. The distribution function and its moments
The distribution function counts particles per unit phase-space volume [Mi §1.2.3]:
$$dN=f(\mathbf x,\mathbf v,t)\,d^3x\,d^3v.$$
Its **velocity moments** are the fluid fields — number density, mean (flow)
velocity, and scalar pressure (one third the trace of the pressure tensor
$\mathsf P_{ij}=m\int(v_i-u_i)(v_j-u_j)f\,d^3v$):
$$n=\int f\,d^3v,\qquad \mathbf u=\frac1n\int \mathbf v\,f\,d^3v,\qquad p=\frac{m}{3}\int|\mathbf v-\mathbf u|^2 f\,d^3v.$$
Code: `maxwellian` (and its moments, recovered numerically in the tests).

## 2. The equilibrium Maxwellian
Maximizing entropy at fixed n, momentum and energy gives the drifting Maxwellian;
at rest [Mi §1.2.3; Pa §6.4]:
$$f_M(\mathbf v)=n\Big(\frac{m}{2\pi k_BT}\Big)^{3/2}\exp\!\Big(-\frac{m v^2}{2k_BT}\Big),\qquad v_T=\sqrt{\frac{k_BT}{m}}.$$
Here $v_T$ is the per-component rms velocity. Its moments return §1 with $p=nk_BT$
(ideal gas) and $\langle\tfrac12 m v^2\rangle=\tfrac32 k_BT$ (equipartition, `~SM-06`).
Code: `maxwellian`, `thermal_speed`.

## 3. The Boltzmann equation
Following f along a phase-space trajectory, only collisions create or destroy it
[Mi §1.4; `~SM-06`]:
$$\frac{\partial f}{\partial t}+\mathbf v\cdot\nabla_{\mathbf x} f+\frac{\mathbf F}{m}\cdot\nabla_{\mathbf v} f=\left(\frac{\partial f}{\partial t}\right)_{\!\mathrm{coll}}.$$
The **streaming** term $\mathbf v\cdot\nabla_{\mathbf x}f$ carries f through space; the
**force** term $(\mathbf F/m)\cdot\nabla_{\mathbf v}f$ bends trajectories in velocity;
the right-hand side is the net rate at which short-range collisions scatter
particles in and out of $d^3v$. Code: its collisionless limit is checked by
`vlasov_residual` (§4–5).

## 4. The Vlasov equation: a self-consistent mean field
In a hot, dilute plasma collisions are rare (§7), so drop the right-hand side. The
force is the **self-consistent** Lorentz force built from the *smoothed* charge and
current of f itself [Mi §1.2.4.1]:
$$\boxed{\ \frac{\partial f}{\partial t}+\mathbf v\cdot\nabla_{\mathbf x} f+\frac{q}{m}\big(\mathbf E+\mathbf v\times\mathbf B\big)\cdot\nabla_{\mathbf v} f=0\ }$$
closed by Maxwell's equations with $\rho=q\!\int\! f\,d^3v$ and
$\mathbf J=q\!\int\! \mathbf v f\,d^3v$ — the Vlasov–Maxwell (or, electrostatically,
Vlasov–Poisson) system. The force-free case is in code as `free_stream`.

## 5. Phase-space continuity and Liouville's theorem (B2 / B10)
Write the Vlasov equation as a six-dimensional **continuity equation** for the
phase-space density, with acceleration $\mathbf a=\mathbf F/m$:
$$\frac{\partial f}{\partial t}+\nabla_{\mathbf x}\!\cdot(\mathbf v f)+\nabla_{\mathbf v}\!\cdot(\mathbf a f)=0.$$
Now $\nabla_{\mathbf x}\!\cdot\mathbf v=0$ (x and v are independent coordinates) and
the Lorentz acceleration has $\nabla_{\mathbf v}\!\cdot\mathbf a=0$ — phase-space flow
is **incompressible** — so the divergences open up and the equation collapses to
**Liouville's theorem**: f is constant along orbits [Mi §1.2.4.1]:
$$\boxed{\ \frac{df}{dt}=\frac{\partial f}{\partial t}+\dot{\mathbf x}\cdot\nabla_{\mathbf x} f+\dot{\mathbf v}\cdot\nabla_{\mathbf v} f=0\ }$$
This is **KEY BRIDGE B2**: the identical local conservation law as mass
($\partial_t\rho+\nabla\!\cdot(\rho\mathbf v)=0$, `~CM-22`) and probability
($|\Psi|^2$, `~QM-04`) — only the conserved density changes. The check `vlasov_residual`
advects f one free-streaming step and confirms $\partial_t f+v\,\partial_x f\approx0$
to discretization error (the residual sits far below the streaming term, exactly as
`~QM-04`'s `continuity_residual` does for $|\Psi|^2$). Code: `free_stream`, `vlasov_residual`.

## 6. Debye shielding and the plasma parameter
Each charge is **screened**. Linearizing Poisson's equation with a Boltzmann
electron response $n_e\propto e^{-q\phi/k_BT}\approx 1-q\phi/k_BT$ gives a screened
Coulomb potential decaying over the **Debye length** [Mi §1.2.1]:
$$\nabla^2\phi=\frac{\phi}{\lambda_D^2}\;\Rightarrow\;\phi(r)=\frac{q_t}{4\pi\varepsilon_0 r}\,e^{-r/\lambda_D},\qquad \lambda_D=\sqrt{\frac{\varepsilon_0 k_BT}{n q^2}}.$$
The **plasma parameter** counts the particles cooperating to do that screening — the
population of a Debye sphere [Mi §1.2.1, Eq. A.8]:
$$\Lambda=n\lambda_D^3\gg1.$$
$\Lambda\gg1$ is the defining inequality of a plasma: many particles per Debye sphere,
so screening is a meaningful statistical average and the discrete graininess
(collisions) is weak. Code: `debye_length`, `plasma_parameter`.

## 7. The plasma frequency and why Vlasov closes
Displace the electrons rigidly and the restoring space charge makes them ring at the
**plasma frequency** [Mi §1.2.2, Eq. A.1]; the Debye length is the distance a thermal
electron drifts in one plasma period:
$$\omega_p=\sqrt{\frac{n q^2}{\varepsilon_0 m}},\qquad \lambda_D=\frac{v_T}{\omega_p}.$$
The collision rate compares to this collective rate as
$\nu_{ei}/\omega_p\sim\ln\Lambda/\Lambda\ll1$ when $\Lambda\gg1$ [Mi §1.4, Eq. A.9]:
on the timescale of a plasma oscillation collisions are negligible, the Boltzmann
right-hand side drops, and the mean-field **Vlasov** equation is the correct leading
description. Collisions re-enter as a slow correction — and, fully resolved, become
the excimer rate chemistry and EEDF of `~PK-04` (the KrF/LoKI simulator in this repo).
Code: `plasma_frequency`, and the identity `debye_length` = `thermal_speed`/`plasma_frequency`.

## Where this goes
- `~SM-06` — the Maxwellian and the Boltzmann transport equation this builds on (KEY BRIDGE B10: the stat-mech → kinetic → fluid ladder).
- `~CM-22` / `~QM-04` — the mass and probability faces of the same continuity law (KEY BRIDGE B2); `vlasov_residual` mirrors `~QM-04`'s `continuity_residual`.
- `~PK-02` — taking velocity moments of the Vlasov/Boltzmann equation (as in §1) closes into the fluid / MHD equations.
- `~PK-03` — perturbing the Vlasov equation gives plasma waves and Landau damping; `~PK-04` — the collision term becomes excimer rate kinetics / swarm EEDF (the KrF–LoKI code).
