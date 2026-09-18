# PK-02 — Fluid & MHD Description — Moments, Continuity & Momentum (notes)

A plasma can be followed particle-by-particle (the distribution function $f$ of
`~PK-01`) or as a **fluid** of smooth fields $n(\mathbf r,t)$, $\mathbf u(\mathbf r,t)$,
$p(\mathbf r,t)$. The bridge between the two pictures is **taking velocity moments**
of the kinetic equation: integrate the Vlasov/Boltzmann equation against
$1,\mathbf v,\mathbf v\mathbf v,\dots$ and the infinite phase space collapses onto a
few fluid fields. The $0^\text{th}$ moment is **continuity** (the same conservation
law as mass `~CM-22`, KEY BRIDGE B2); the $1^\text{st}$ is **momentum**; summing over
species gives **ideal MHD**.

Citation key (full details in `refs.md`): **Mi** = Michel, *Introduction to
Laser-Plasma Interactions* (Springer), Ch.1; **Rh** = Rhodes (ed.), *Excimer Lasers*
(Topics in Applied Physics 30). Cited at **section/chapter level** (see `refs.md`).
Michel measures $T$ in energy units ($k_B=1$); below $k_B$ is restored, $p=nk_BT$.

## 1. Velocity moments of the kinetic equation
For species $s$ the moments of $f_s(\mathbf r,\mathbf v,t)$ are the fluid fields
[Mi §1.2.4.2]:
$$
\begin{aligned}
n &= \int f\,d^3v, &
\mathbf u &= \frac{1}{n}\int \mathbf v\,f\,d^3v,\\[2pt]
\mathsf{P} &= m\!\int (\mathbf v-\mathbf u)(\mathbf v-\mathbf u)\,f\,d^3v, &
p &= \tfrac13\,\mathrm{tr}\,\mathsf{P}=\tfrac13 m\!\int|\mathbf v-\mathbf u|^2 f\,d^3v .
\end{aligned}
$$
$n$ is the number density, $\mathbf u$ the mean (fluid) velocity, $\mathsf{P}$ the
pressure tensor and $p$ the scalar pressure. For a (drifting) **Maxwellian** the
distribution is isotropic in the rest frame, so $\mathsf{P}=p\,\mathsf{I}$ and
$$p=n k_B T,\qquad f(\mathbf v)=n\Big(\frac{m}{2\pi k_B T}\Big)^{3/2}
e^{-m|\mathbf v-\mathbf u|^2/2k_B T}.$$
Code: `moments_of_maxwellian` integrates this $f$ and recovers $(n,\mathbf u,nk_BT)$.

## 2. Zeroth moment → continuity
Integrate the Vlasov equation $\partial_t f+\mathbf v\cdot\nabla f
+(\mathbf F/m)\cdot\nabla_{\!v}f=0$ over $d^3v$. The force term integrates to zero
(it is a velocity-divergence, $f\to0$ at $|\mathbf v|\to\infty$), leaving
[Mi Eq. 1.63]:
$$\boxed{\ \frac{\partial n}{\partial t}+\nabla\cdot(n\mathbf u)=0\ }$$
— **local conservation of particles**, with flux $n\mathbf u$. This is exactly the
mass-continuity law of `~CM-22` and the charge/probability laws of `~EM-13`/`~QM-04`
(KEY BRIDGE B2); only the conserved density changes. Code: `continuity_residual`
checks it for a rigidly advected density bump $n=f(x-ut)$.

## 3. First moment → momentum
Multiply the Vlasov equation by $m\mathbf v$ and integrate. The inertial terms give
$\partial_t(mn\mathbf u)+\nabla\cdot(mn\langle\mathbf{vv}\rangle)$, the force term
gives $qn(\mathbf E+\mathbf u\times\mathbf B)$; using continuity to peel off
$\partial_t n$ leaves the **fluid momentum (force) equation** [Mi Eqs. 1.73–1.74]:
$$\boxed{\ m n\!\left(\frac{\partial\mathbf u}{\partial t}
+\mathbf u\cdot\nabla\mathbf u\right)
=-\nabla\cdot\mathsf{P}+qn\,(\mathbf E+\mathbf u\times\mathbf B)\ }$$
The left side is mass density $\times$ acceleration *following the flow*; the right
side is the pressure force plus the Lorentz force. This is Newton's second law for a
fluid element.

## 4. The closure problem
Notice the hierarchy is **not closed**: continuity ($n$) needs $\mathbf u$, momentum
($\mathbf u$) needs $\mathsf{P}$, the pressure equation would need the heat flux
$\mathbf q$, and so on — *each moment couples to the next*. One truncates with an
equation of state. A **polytropic** closure [Mi §1.2.4.2]
$$p=C\rho^{\gamma}\;\Rightarrow\;\nabla p=\gamma k_B T\,\nabla n,
\qquad \gamma=\frac{N+2}{N},$$
turns $\nabla\cdot\mathsf{P}\to\nabla p$: isothermal $\gamma=1$, adiabatic 3-D
$\gamma=5/3$ ($N=3$), 1-D plasma-wave compression $\gamma=3$ ($N=1$). The polytropic
index $\gamma$ is exactly what sets the **sound speed** of §7.

## 5. Two-fluid → one-fluid ideal MHD
Write momentum for electrons and ions, then form total mass density, centre-of-mass
velocity and current,
$$\rho=\sum_s m_s n_s,\qquad
\rho\mathbf u=\sum_s m_s n_s\mathbf u_s,\qquad
\mathbf J=\sum_s q_s n_s\mathbf u_s .$$
Adding the two momentum equations, the $\pm qn\mathbf E$ terms cancel under
**quasineutrality** ($\sum_s q_s n_s\approx0$) and the magnetic terms combine into
$\mathbf J\times\mathbf B$, giving the **ideal-MHD momentum equation**:
$$\boxed{\ \rho\frac{D\mathbf u}{Dt}=-\nabla p+\mathbf J\times\mathbf B\ },
\qquad \frac{D}{Dt}=\frac{\partial}{\partial t}+\mathbf u\cdot\nabla .$$
The light electrons carry the current with negligible inertia; their momentum
equation reduces to the **ideal Ohm's law** $\mathbf E+\mathbf u\times\mathbf B=0$.

## 6. Induction equation & frozen-in flux
Insert Ohm's law into Faraday's law $\partial_t\mathbf B=-\nabla\times\mathbf E$
(`~EM-13`):
$$\boxed{\ \frac{\partial\mathbf B}{\partial t}=\nabla\times(\mathbf u\times\mathbf B)\ }$$
With zero resistivity the magnetic flux through any fluid loop is **conserved** — the
field lines are *frozen into* the plasma and move with it (Alfvén's theorem). Add a
resistive term $\eta\nabla^2\mathbf B/\mu_0$ and the lines diffuse and reconnect.

## 7. Characteristic speeds
Linearizing continuity + momentum (+ closure) gives the wave speeds [Mi §1.3.1–1.3.2;
standard MHD]:
$$c_s=\sqrt{\frac{\gamma p}{\rho}}\quad(\text{sound}),\qquad
v_A=\frac{B}{\sqrt{\mu_0\rho}}\quad(\text{Alfven}),\qquad
v_{\text{fast}}=\sqrt{c_s^{2}+v_A^{2}}\quad(\text{fast magnetosonic},\ \mathbf k\perp\mathbf B).$$
Sound is restored by gas pressure $p$, the **Alfvén** wave by magnetic *tension* on
the frozen-in field, and the perpendicular **fast** wave by gas + magnetic pressure
together (they add in quadrature). Code: `sound_speed`, `alfven_speed`,
`fast_magnetosonic_speed`.

## 8. Magnetic pressure & plasma β
The $\mathbf J\times\mathbf B$ force splits into magnetic **tension** along the lines
and an isotropic **magnetic pressure**; their ratio to the gas pressure is the
**plasma β**:
$$P_B=\frac{B^2}{2\mu_0},\qquad
\boxed{\ \beta=\frac{p}{B^2/2\mu_0}=\frac{n k_B T}{B^2/2\mu_0}\ }.$$
$\beta\ll1$ is a magnetically dominated plasma (the field organizes the flow, e.g. a
tokamak or the solar corona); $\beta\gg1$ is gas-pressure dominated (the flow drags
the field). Code: `magnetic_pressure`, `plasma_beta`.

## Where this goes
- `~PK-01` — the distribution function $f$ and the Vlasov/Boltzmann equation these
  moments are taken of; `~SM-06` — the same moment construction for a neutral gas.
- `~CM-22` — the **identical** continuity equation for mass (KEY BRIDGE B2); `~CM-23`
  — the neutral-fluid Euler/Navier–Stokes limit (drop $\mathbf J\times\mathbf B$).
- `~EM-13` — Maxwell's equations supplying $\mathbf E,\mathbf B$ and Faraday's law for
  the induction equation; `~PK-03` — linearizing these fluid equations gives plasma
  waves and instabilities.
- (→) the KrF/LoKI 0-D kinetics code in this repo is the **continuity (rate) moment**
  taken per species with collisional source terms (Rh, excimer chemistry); the fluid
  picture here is its spatially-resolved generalization.
