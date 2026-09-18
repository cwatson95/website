# EM-07 — Dielectrics & Polarization (notes)

A **dielectric** is an insulator: its charges are not free to wander, but in an
external field they *shift* slightly, and the material **polarizes**. The new field
variable is the **polarization** **P**(**r**), the dipole moment per unit volume; its
companion is the **displacement** **D**. Everything here is built from the `~EM-01`
Coulomb field and the `~EM-02` flux law by carefully accounting for the **bound charge**
that a polarized object carries.

Citation key (full details + PDF pages in `refs.md`): **Gr** = Griffiths 4e. Page
numbers are the *printed* book pages. **n̂** is the outward surface normal; **r̂** the
radial unit vector.

## 1. Induced dipoles and the polarization
Put a neutral atom in a field **E**: the nucleus and electron cloud pull apart until the
restoring force balances, leaving an **induced dipole** proportional to the field
(Gr §4.1.2, Eq. 4.1, p.167):
$$\mathbf p=\alpha\,\mathbf E,$$
with α the atomic **polarizability**. For a chunk of material, the relevant quantity is
the dipole moment *per unit volume*, the **polarization** (Gr §4.1.4, p.172):
$$\mathbf P=\frac{\text{dipole moment}}{\text{volume}}
   =\lim_{\Delta\tau\to0}\frac{1}{\Delta\tau}\sum_{i\in\Delta\tau}\mathbf p_i .$$
**P** is the object we track; the field it produces is the whole content of this module.

## 2. Bound charge — the field of a polarized object
Inside a uniformly polarized block the head of each little dipole sits against the tail of
the next, so the interior stays neutral; only at the **surfaces** (and wherever **P**
*varies*) does the cancellation fail. Griffiths shows the field of a polarized object is
*exactly* that of two ordinary charge densities (Gr §4.2.1, Eqs. 4.11–4.12, p.173):
$$\sigma_b=\mathbf P\cdot\hat{\mathbf n},\qquad
  \rho_b=-\nabla\cdot\mathbf P .$$
This **bound charge** is real charge — it sources **E** just like free charge. Code:
`bound_surface_charge` returns `dot(P, n̂)`; `bound_volume_charge` returns
`-divergence(P)` straight from `~MA-02`. A *uniform* **P** gives ρ_b = 0, putting all the
bound charge on the surface.

**Uniformly polarized sphere** (Gr §4.2.1, Ex. 4.2). Take **P** = P **ẑ**. With **n̂** = **r̂**
the surface charge is
$$\sigma_b=\mathbf P\cdot\hat{\mathbf r}=P\cos\theta,$$
which integrates to zero net charge. The field *inside* is uniform and opposes **P**:
$$\boxed{\;\mathbf E_{\mathrm{in}}=-\frac{\mathbf P}{3\varepsilon_0}\;}$$
the classic **depolarizing field**. Code: `polarized_sphere_surface_charge`,
`polarized_sphere_inner_field`. This is the *electric twin* of the uniformly **magnetized**
sphere in `~EM-10`, whose interior carries a uniform **B** built the same way from bound
currents.

## 3. The displacement field and Gauss's law for D
Split the total charge into bound and free, ρ = ρ_b + ρ_f, and feed it to the differential
Gauss law of `~EM-02`:
$$\nabla\cdot\mathbf E=\frac{\rho}{\varepsilon_0}
  =\frac{\rho_f-\nabla\cdot\mathbf P}{\varepsilon_0}
  \;\Longrightarrow\;
  \nabla\cdot\!\big(\varepsilon_0\mathbf E+\mathbf P\big)=\rho_f .$$
The combination in parentheses is the **electric displacement** (Gr §4.3.1, Eq. 4.21, p.181):
$$\mathbf D\equiv\varepsilon_0\mathbf E+\mathbf P,\qquad
  \nabla\cdot\mathbf D=\rho_f,\qquad
  \oint\mathbf D\cdot d\mathbf a=Q_{f,\mathrm{enc}}\quad(\text{Eq. 4.23}).$$
The payoff: **D** is sourced by **free charge alone** — the charge you actually deposit and
control. Given symmetry you extract **D** from Q_free exactly as `~EM-02` extracts **E**
from Q_enc, then recover **E** = (**D** − **P**)/ε₀. Code: `displacement_field` forms
ε₀**E** + **P** pointwise; `displacement_point_free_charge` gives the free point charge's
**D** = q_f/4πr² **r̂** (*medium-independent*); `free_charge_enclosed` runs EM-02's
`flux_through_sphere` on **D** and reads back q_f. One caveat Griffiths stresses: in general
∇×**D** = ∇×**P** ≠ **0**, so **D** is *not* the gradient of a potential — the symmetry trick
is its only general handle.

## 4. Linear dielectrics — susceptibility, permittivity, dielectric constant
For most materials in modest fields the polarization is simply proportional to the field
(Gr §4.4.1, Eq. 4.30, p.185):
$$\mathbf P=\varepsilon_0\chi_e\,\mathbf E,$$
with χ_e the (dimensionless) **electric susceptibility**. Then **D** collapses to a constant
times **E** (Eq. 4.32):
$$\mathbf D=\varepsilon_0\mathbf E+\mathbf P=\varepsilon_0(1+\chi_e)\,\mathbf E
  \equiv\varepsilon\,\mathbf E,$$
defining the **permittivity** ε = ε₀(1 + χ_e) and the **dielectric constant** (relative
permittivity) (Eq. 4.34):
$$\varepsilon_r=\frac{\varepsilon}{\varepsilon_0}=1+\chi_e .$$
Code: `susceptibility_from_eps_r` (χ_e = ε_r − 1), `permittivity` (ε = ε₀ε_r),
`polarization_linear` (**P** = ε₀χ_e**E**), `displacement_linear` (**D** = ε**E**). The two
expressions for **D** — ε**E** and ε₀**E** + **P** — are identically equal, and the tests
check it. Filling a capacitor with a linear dielectric multiplies its capacitance by ε_r
(`capacitance_with_dielectric`): at fixed free charge **D** is unchanged, so **E** = **D**/ε
and hence V drop by ε_r while Q holds, and C = Q/V rises by ε_r.

## Where this goes
- `~EM-10` is the magnetic mirror image of this entire module: magnetization **M** plays the
  role of **P**, the **bound currents** J_b = ∇×**M**, K_b = **M**×**n̂** play the role of
  bound charge, and the auxiliary field **H** = **B**/μ₀ − **M** plays the role of **D**,
  sourced by *free current*. The uniformly polarized sphere ↔ the uniformly magnetized sphere.
- `~CMx`: α and χ_e are *outputs* of microscopic physics — the **Clausius–Mossotti** relation
  ties χ_e to the atomic polarizability and number density, and condensed-matter theory
  computes the frequency-dependent ε(ω).
- **D** joins **E**, **B**, **H** as a field variable in the **macroscopic Maxwell equations**
  (`~EM-13`), where ∂**D**/∂t is the displacement current.
- The bookkeeping "field = vacuum term + material response," **D** = ε₀**E** + **P**, is the
  same move as **H** = **B**/μ₀ − **M** — one idea, two chapters.
