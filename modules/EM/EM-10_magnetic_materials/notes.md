# EM-10 — Magnetic Materials & Magnetization (notes)

Magnetic materials = matter that responds to a magnetic field by developing a net
**magnetization** **M**(**r**), the magnetic dipole moment per unit volume. This
module is the magnetic mirror of the dielectric story in `~EM-07`: where a
polarized object hid **bound charge**, a magnetized object hides **bound current**;
where dielectrics introduced the displacement **D**, magnets introduce the
auxiliary field **H**. Everything is built on `~EM-08` (the magnetostatic **B**,
the constant μ₀, Ampère's law) and the MA-01/MA-02 vector operators.

Citation key (full details + PDF pages in `refs.md`): **Gr** = Griffiths 4e.
Page numbers are the *printed* book pages. SI units: **M** and **H** in A/m,
**B** in tesla, χ_m and μ_r dimensionless, μ in T·m/A.

## 1. Magnetization
The state of a magnetized medium is captured by one vector field (Gr §6.1.4, p.273):
$$\mathbf M\equiv\frac{\text{magnetic dipole moment}}{\text{volume}}.$$
A material acquires **M** in three ways: **paramagnetism** (permanent atomic
moments partially aligning with the field), **diamagnetism** (induced moments
opposing the field, present in all matter), and **ferromagnetism** (cooperative
domain alignment that persists without a field). **M** is the magnetic analogue of
the polarization **P** of `~EM-07`. In code **M** is an ordinary vector-field
function `M(x,y,z) -> (Mx,My,Mz)` (the MA-02 convention), ready for `curl`.

## 2. Bound currents — a magnet is a current distribution
Just as a polarized object hides bound charge, a magnetized object hides **bound
currents** (Gr §6.2.1, Eqs. 6.13–6.14, p.274):
$$\mathbf J_b=\nabla\times\mathbf M\quad(\text{Eq. }6.13),\qquad
  \mathbf K_b=\mathbf M\times\hat{\mathbf n}\quad(\text{Eq. }6.14).$$
The **volume** current is the curl of **M** (code `bound_volume_current`, MA-02
`curl`), so it vanishes wherever **M** is uniform; the **surface** current
**K**_b = **M**×n̂ (code `bound_surface_current`, MA-01 `cross`) wraps the boundary.
For a cylinder uniformly magnetized along its axis, **M** = M ẑ, the interior
carries *no* current but the side wall carries **K**_b = M φ̂ — precisely the
surface current of a **solenoid** with nI = M. A uniformly magnetized cylinder is
magnetically indistinguishable from a solenoid.

The same picture explains the uniformly magnetized **sphere** (Gr §6.2.1, Ex. 6.1):
its surface current **K**_b = M sinθ φ̂ is that of a spinning charged shell, and the
field inside is uniform,
$$\mathbf B_{\text{in}}=\tfrac{2}{3}\mu_0\mathbf M\quad(\text{Eq. }6.16),$$
while outside it is a pure dipole. Code returns these as
`magnetized_sphere_inner_B` and (see §3) `magnetized_sphere_inner_H`.

## 3. The auxiliary field H
Inside matter the total current splits into free and bound parts, **J** = **J**_f +
**J**_b. Ampère's law `∇×B = μ₀J` (from `~EM-08`) then reads
$\nabla\times\mathbf B=\mu_0(\mathbf J_f+\nabla\times\mathbf M)$, which rearranges
into a law for a new field (Gr §6.3.1, Eqs. 6.18, 6.20, p.279):
$$\boxed{\;\mathbf H\equiv\frac{\mathbf B}{\mu_0}-\mathbf M\;}\quad(\text{Eq. }6.18)
  \;\Longrightarrow\;
  \nabla\times\mathbf H=\mathbf J_f,\qquad
  \oint\mathbf H\cdot d\boldsymbol\ell=I_{f,\text{enc}}\quad(\text{Eq. }6.20).$$
**H** is sourced by **free current alone** — the practical payoff, since free
current is what we control in a wire. Code `auxiliary_field_H(B, M)` returns **H**
pointwise from the field functions **B** and **M**. For the magnetized sphere of
§2 this gives the **demagnetizing field**
$\mathbf H_{\text{in}}=\mathbf B_{\text{in}}/\mu_0-\mathbf M=-\mathbf M/3$
(`magnetized_sphere_inner_H`), pointing *against* **M**.

*Caveat (Griffiths' warning).* Unlike **B**, the field **H** is **not** divergence-free:
$\nabla\cdot\mathbf H=-\nabla\cdot\mathbf M$. So ∮**H**·d**l** = I_f,enc is only
*useful* when symmetry kills the contribution of bound surface charge of **M** —
**H** is a bookkeeping convenience, **B** remains the fundamental field.

## 4. Linear media — susceptibility and permeability
For para- and dia-magnets in ordinary fields **M** tracks **H** linearly
(Gr §6.4.1, Eqs. 6.29, 6.31, 6.33, p.284):
$$\mathbf M=\chi_m\mathbf H\quad(\text{Eq. }6.29),$$
with χ_m the dimensionless **magnetic susceptibility** — small and *negative* for
diamagnets, small and *positive* for paramagnets. Substituting into **H** = **B**/μ₀ − **M**,
$$\mathbf B=\mu_0(\mathbf H+\mathbf M)=\mu_0(1+\chi_m)\mathbf H\equiv\mu\mathbf H
  \quad(\text{Eq. }6.31),\qquad
  \mu=\mu_0(1+\chi_m)\quad(\text{Eq. }6.33),$$
where μ is the **permeability** and μ_r = μ/μ₀ = 1 + χ_m the relative permeability.
Code: `magnetization_linear` (**M** from **H**), `B_linear` (**B** from **H**),
`permeability` (μ), and `classify_material`, which reads the sign and size of χ_m
(χ_m < 0 → diamagnetic; small χ_m > 0 → paramagnetic; large/nonlinear →
ferromagnetic). This is the exact mirror of `~EM-07`'s ε = ε₀(1 + χ_e).

## 5. Ferromagnetism and hysteresis
Ferromagnets break linearity. Exchange coupling aligns spins into **domains**, and
the magnetization depends on the **history** of the applied field, not just its
present value (Gr §6.4.2, p.288). Sweeping **H** up, down, and back traces a
**hysteresis loop**. Two markers characterize it:
- **remanence** M_r: the magnetization left at **H** = 0 (a permanent magnet);
- **coercivity** H_c: the reverse field needed to drive **M** back through zero.

Code models the loop with a two-branch tanh: `hysteresis_branches(Ms, Hc, width)`
returns (M_up, M_down), the ascending branch shifted to +H_c and the descending to
−H_c, so $M_\downarrow(0)>0>M_\uparrow(0)$ — an **open** loop, the signature of
history dependence. Then `remanence` = $|M_\downarrow(0)|$ and `coercivity` = H_c
(where $M_\downarrow(-H_c)=0$); both saturate to ±M_s at large $|H|$. Heated above
the **Curie temperature** the domain order melts and the ferromagnet reverts to an
ordinary paramagnet.

## 6. The electric ↔ magnetic analogy (~EM-07)
Griffiths develops dielectrics (Ch. 4) and magnets (Ch. 6) in deliberate parallel.
The dictionary, term for term:

| electric — `~EM-07` (Ch. 4) | magnetic — EM-10 (Ch. 6) |
|---|---|
| polarization **P** | magnetization **M** |
| ρ_b = −∇·**P**  (Eq. 4.12) | **J**_b = ∇×**M**  (Eq. 6.13) |
| σ_b = **P**·n̂  (Eq. 4.11) | **K**_b = **M**×n̂  (Eq. 6.14) |
| **D** = ε₀**E** + **P**  (Eq. 4.21) | **H** = **B**/μ₀ − **M**  (Eq. 6.18) |
| ∮**D**·d**a** = Q_f,enc  (Eq. 4.23) | ∮**H**·d**l** = I_f,enc  (Eq. 6.20) |
| **P** = ε₀χ_e**E**  (Eq. 4.30) | **M** = χ_m**H**  (Eq. 6.29) |
| **D** = ε**E**, ε = ε₀(1+χ_e) | **B** = μ**H**, μ = μ₀(1+χ_m) |

The analogy is close but **not exact**. On the electric side the bound source is a
*charge* (a divergence) and the auxiliary field **D** is built *from* **E**; on the
magnetic side the bound source is a *current* (a curl) and **H** is built *from*
**B**. The roles of "fundamental" and "auxiliary" therefore swap — **E** is
fundamental with **D** auxiliary, but **B** is fundamental with **H** auxiliary —
because there are no magnetic monopoles (∇·**B** = 0 always, whereas
∇·**D** = ρ_f). A direct consequence: **D** is divergence-sourced by free charge,
while **H** is curl-sourced by free current but is *not* divergence-free
(∇·**H** = −∇·**M**), which is why Ampère-for-**H** needs symmetry to be useful (§3).

## Where this goes
- `~EM-11` (induction) leaves statics behind: a changing **B** drives an EMF —
  the static-magnetism arc `~EM-08` → `~EM-09` → EM-10 closes here.
- `~EM-13` (Maxwell) carries **H** and the constitutive relations into the full set,
  ∇×**H** = **J**_f + ∂**D**/∂t.
- The dia/para/ferro classification and domain physics open onto condensed matter
  (`~CMx`): magnetic ordering, exchange, and the Curie transition.
- Read alongside `~EM-07` (the **D** field): together they are "fields in matter."
