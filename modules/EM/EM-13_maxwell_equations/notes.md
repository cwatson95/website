# EM-13 — Maxwell's Equations (notes)

Maxwell's equations are the four local laws that govern **all** of classical
electromagnetism. Three of them — Gauss's law, the no-monopole law, and Faraday's law —
are already in hand from `~EM-01`, `~EM-08`, and `~EM-11`. The fourth, Ampère's law, is
*almost* right: Maxwell's one correction, the **displacement current**, closes the set,
makes it self-consistent under time variation, and — for free — predicts light.

Citation key (full details + PDF pages in `refs.md`): **Gr** = Griffiths 4e. Page numbers
are the *printed* book pages. Vectors are bold; ε₀ = `EPS0` (from `~EM-01`), μ₀ = `MU0`
(from `~EM-08`).

## 1. How Maxwell fixed Ampère's law — the displacement current
Magnetostatics gave Ampère's law $\nabla\times\mathbf B=\mu_0\mathbf J$. Take its
divergence (Gr §7.3.2, p.334): the left side vanishes identically,
$\nabla\cdot(\nabla\times\mathbf B)=0$, so the law *demands*
$$\nabla\cdot\mathbf J=0 .$$
That is true for **steady** currents but false the moment charge piles up anywhere: the
continuity equation (§5 below) says $\nabla\cdot\mathbf J=-\partial\rho/\partial t$. Maxwell's
remedy is to add the **displacement current density** (Gr §7.3.2, Eq. 7.38, p.334)
$$\boxed{\;\mathbf J_d\equiv\varepsilon_0\,\frac{\partial\mathbf E}{\partial t}\;}$$
to the source. Using Gauss's law $\nabla\cdot\mathbf E=\rho/\varepsilon_0$,
$$\nabla\cdot(\mathbf J+\mathbf J_d)=\nabla\cdot\mathbf J+\varepsilon_0\frac{\partial}{\partial t}(\nabla\cdot\mathbf E)
=\nabla\cdot\mathbf J+\frac{\partial\rho}{\partial t}=0 ,$$
so the corrected Ampère–Maxwell law is divergence-consistent for *any* fields. Physically:
between the plates of a **charging capacitor** there is no conduction current, yet a magnetic
field circulates — it is fed entirely by $\mathbf J_d$, the changing **E** acting as a source.
Code: `displacement_current_density(dE_dt)` returns $\varepsilon_0\,d\mathbf E/dt$.

## 2. The four equations
In differential form, with all sources present (Gr §7.3.3, Eqs. 7.39–7.42, p.337):
$$\nabla\cdot\mathbf E=\frac{\rho}{\varepsilon_0}\qquad\text{(Gauss, 7.39)}$$
$$\nabla\cdot\mathbf B=0\qquad\text{(no magnetic monopoles, 7.40)}$$
$$\nabla\times\mathbf E=-\frac{\partial\mathbf B}{\partial t}\qquad\text{(Faraday, 7.41)}$$
$$\nabla\times\mathbf B=\mu_0\mathbf J+\mu_0\varepsilon_0\frac{\partial\mathbf E}{\partial t}\qquad\text{(Ampère–Maxwell, 7.42)}$$
Each line is a **single divergence or curl**, so each maps onto exactly one MA-02 operator.
Code computes a *normalized* residual for each — `gauss_E_residual`, `gauss_B_residual`,
`faraday_residual`, `ampere_maxwell_residual` — by freezing the field at time $t$ and applying
MA-02's `divergence`/`curl` to the spatial slice (the time derivatives come from `partial_t`).
Dividing each residual by the local derivative scale makes it dimensionless, so "the equation
holds" reads as a residual ≈ 0 regardless of units. These four equations fix the **fields**;
the **Lorentz force** $\mathbf F=q(\mathbf E+\mathbf v\times\mathbf B)$ (from `~EM-08`) is the
separate fifth ingredient that says what the fields *do* to charges.

## 3. Maxwell's equations in matter
Inside a medium one bundles the bound charge and bound current into two auxiliary fields,
the displacement **D** and the **H** field (Gr §7.3.5, p.340):
$$\mathbf D=\varepsilon_0\mathbf E+\mathbf P,\qquad
  \mathbf H=\frac{1}{\mu_0}\mathbf B-\mathbf M ,$$
with **P** the polarization (`~EM-07`) and **M** the magnetization (`~EM-10`). In terms of the
**free** charge ρ_f and free current **J**_f the four equations keep their shape:
$$\nabla\cdot\mathbf D=\rho_f,\quad \nabla\cdot\mathbf B=0,\quad
  \nabla\times\mathbf E=-\frac{\partial\mathbf B}{\partial t},\quad
  \nabla\times\mathbf H=\mathbf J_f+\frac{\partial\mathbf D}{\partial t}.$$
The displacement current is now $\partial\mathbf D/\partial t$. Matching **E**, **B**, **D**, **H**
across an interface gives the **boundary conditions** (Gr §7.3.6, p.342) that `~EM-15` and
`~EM-16` use at reflecting surfaces and waveguide walls.

## 4. The wave that pops out — c from the constants
In vacuum (ρ = 0, **J** = 0) take the curl of Faraday's law and substitute Ampère–Maxwell:
$$\nabla\times(\nabla\times\mathbf E)=-\frac{\partial}{\partial t}(\nabla\times\mathbf B)
=-\mu_0\varepsilon_0\frac{\partial^2\mathbf E}{\partial t^2}.$$
The identity $\nabla\times(\nabla\times\mathbf E)=\nabla(\nabla\cdot\mathbf E)-\nabla^2\mathbf E$
collapses to $-\nabla^2\mathbf E$ because $\nabla\cdot\mathbf E=0$ in vacuum, leaving a **wave
equation**
$$\nabla^2\mathbf E=\mu_0\varepsilon_0\frac{\partial^2\mathbf E}{\partial t^2},
\qquad c=\frac{1}{\sqrt{\mu_0\varepsilon_0}}\approx 2.998\times10^8\ \mathrm{m/s}.$$
That two *static* constants, measured in electrostatics and magnetostatics, combine into the
speed of light was Maxwell's punchline: **light is an electromagnetic wave.** Code: `C_SI` is
exactly $1/\sqrt{\mu_0\varepsilon_0}$; `plane_wave_fields(E0, k, c)` builds the simplest
solution
$$\mathbf E=E_0\cos(kz-\omega t)\,\hat{\mathbf x},\qquad
  \mathbf B=\frac{E_0}{c}\cos(kz-\omega t)\,\hat{\mathbf y},\qquad \omega=ck,$$
and `verify_vacuum_plane_wave` confirms it kills all four residuals — **but only when ω = ck**
(`test_wrong_dispersion_breaks_ampere` mismatches the speed and watches Faraday/Ampère blow up).
The check is done in natural units (c a free parameter, set to 1) so the finite-difference
$\partial_t$ stays well conditioned; the SI value lives in `C_SI`. The full theory of these
waves — polarization, energy, media, reflection — is `~EM-15`.

## 5. Continuity — the conservation law underneath (KEY BRIDGE B2)
The consistency Maxwell exploited in §1 is itself the statement of **local charge conservation**
(Gr §8.1.1, Eq. 8.4, p.356):
$$\frac{\partial\rho}{\partial t}+\nabla\cdot\mathbf J=0 .$$
It is not an extra postulate — it is *forced* by the four equations: take the divergence of
Ampère–Maxwell (7.42) and use Gauss (7.39). The identical equation governs **mass** in fluids
(`~CM-22`), **probability** in quantum mechanics (`~QM-04`), and **phase-space density** in
kinetic theory (`~PK-02`) — one law, different densities (**KEY BRIDGE B2**). Promoting it from
charge to *energy* density gives Poynting's theorem, the gateway to `~EM-14`.

## Where this goes
- `~EM-14` — Poynting's theorem, field energy & momentum, the stress tensor: the conservation
  laws that follow from the four equations.
- `~EM-15` — the electromagnetic waves these equations predict; speed c in vacuum, c/n in media.
- `~CM-22` / `~QM-04` / `~PK-02` — the continuity equation, the same law for mass / probability /
  phase space (**KEY BRIDGE B2**).
- `~EM-18` — all four equations collapse into one covariant statement $\partial_\mu F^{\mu\nu}=\mu_0 J^\nu$.
