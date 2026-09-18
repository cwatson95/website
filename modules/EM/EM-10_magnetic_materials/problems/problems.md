# EM-10 — Problems

Work by hand, then check with `code/magnetic_materials.py`. Citations in
`../refs.md`; **Gr** = Griffiths 4e (printed pages).

### P1.  A uniformly magnetized cylinder is a solenoid  *(Gr §6.2.1, Ex. 6.1, p.274)*
A long cylinder of radius $R$ is uniformly magnetized along its axis, $\mathbf M = M\,\hat{\mathbf z}$.
Show the interior bound volume current vanishes, $\mathbf J_b=\nabla\times\mathbf M=\mathbf 0$,
while the side wall carries a bound surface current $\mathbf K_b=\mathbf M\times\hat{\mathbf n}=M\,\hat{\boldsymbol\phi}$.
Conclude the cylinder is equivalent to a solenoid with $nI=M$, so the field inside
is $\mathbf B=\mu_0 M\,\hat{\mathbf z}$ (long-solenoid limit). *Check:*
`bound_volume_current(lambda x,y,z:(0,0,M), (0.1,0.2,0))` is $(0,0,0)$, and
`bound_surface_current((0,0,M),(1,0,0))` returns $(0,M,0)=M\hat{\boldsymbol\phi}$ with
`norm` $=M$.

**Solution.** Use the bound currents (Eqs. 6.13–6.14) $\mathbf J_b=\nabla\times\mathbf M$ and
$\mathbf K_b=\mathbf M\times\hat{\mathbf n}$. For $\mathbf M=M\,\hat{\mathbf z}$ uniform, every
derivative of $\mathbf M$ is zero, so $\mathbf J_b=\nabla\times(M\,\hat{\mathbf z})=\mathbf 0$ —
no interior current. On the side wall the outward normal is radial, $\hat{\mathbf n}=\hat{\mathbf s}$,
and with $\hat{\mathbf z}\times\hat{\mathbf s}=\hat{\boldsymbol\phi}$,
$$\mathbf K_b=\mathbf M\times\hat{\mathbf n}=M\,\hat{\mathbf z}\times\hat{\mathbf s}=M\,\hat{\boldsymbol\phi}.$$
This is precisely a solenoid's wall current with $nI=M$, so the long-solenoid result gives
$\mathbf B=\mu_0 nI\,\hat{\mathbf z}=\mu_0 M\,\hat{\mathbf z}$ inside. Numerically the curl returns
$(0,0,0)$ and `bound_surface_current((0,0,M),(1,0,0))` $=(0,M,0)$ with `norm` $=M$.

### P2.  A swirling magnetization carries volume current  *(Gr §6.2.1, Eq. 6.13, p.274)*
Now let the magnetization swirl, $\mathbf M=(-a\,y,\;a\,x,\;0)$ with constant $a$.
Compute the bound volume current $\mathbf J_b=\nabla\times\mathbf M$ and show it is the
uniform axial current $\mathbf J_b=2a\,\hat{\mathbf z}$. Contrast with P1: a *non-uniform*
**M** does feed a real volume current, whereas a uniform **M** does not. *Check:*
`bound_volume_current(lambda x,y,z:(-a*y, a*x, 0), (0.3,0.1,0))` $\approx (0,0,2a)$.

**Solution.** For $\mathbf M=(-a\,y,\;a\,x,\;0)$ the bound volume current (Eq. 6.13) is the curl
$$\mathbf J_b=\nabla\times\mathbf M=\left(\frac{\partial M_z}{\partial y}-\frac{\partial M_y}{\partial z},\;
\frac{\partial M_x}{\partial z}-\frac{\partial M_z}{\partial x},\;
\frac{\partial M_y}{\partial x}-\frac{\partial M_x}{\partial y}\right).$$
The first two components vanish ($M_z=0$ and $M_x,M_y$ have no $z$-dependence); the third is
$\partial_x(a x)-\partial_y(-a y)=a-(-a)=2a$, so
$$\mathbf J_b=2a\,\hat{\mathbf z}.$$
A *non-uniform* $\mathbf M$ thus carries a uniform axial volume current, unlike the uniform $\mathbf M$ of
P1. For $a=5$, `bound_volume_current(...)` returns $(0,0,10)=2a\,\hat{\mathbf z}$.

### P3.  Ampère for H in a filled solenoid  *(Gr §6.3.1, Eq. 6.18 & 6.20, p.279; linear media §6.4.1, p.284)*
A long solenoid ($n$ turns per length, free current $I_f$) is filled with a linear
medium of susceptibility $\chi_m$. Apply $\oint\mathbf H\cdot d\boldsymbol\ell=I_{f,\text{enc}}$
to get $\mathbf H = nI_f\,\hat{\mathbf z}$ **independent of the medium**; then
$\mathbf B=\mu\mathbf H=\mu_0(1+\chi_m)nI_f\,\hat{\mathbf z}$ and $\mathbf M=\chi_m\mathbf H$.
Verify the definition $\mathbf H=\mathbf B/\mu_0-\mathbf M$ reproduces the same **H**.
*Check:* with $H(x,y,z)=(0,0,nI_f)$, `B_linear(chi_m, H)` and `magnetization_linear(chi_m, H)`
and `permeability(chi_m)` give **B**, **M**, μ; feeding **B**, **M** back through
`auxiliary_field_H` returns the original **H**.

**Solution.** Apply Ampère's law for $\mathbf H$ (Eq. 6.20), $\oint\mathbf H\cdot d\boldsymbol\ell=I_{f,\text{enc}}$,
to a rectangular loop with one side of length $\ell$ running along the axis inside the solenoid. Only
free current is enclosed — the $n\ell I_f$ turns it threads — and $\mathbf H$ is axial and uniform inside,
zero outside, so $H\ell=n\ell I_f$ gives
$$\mathbf H=nI_f\,\hat{\mathbf z}\quad(\text{independent of the filling}).$$
Then $\mathbf B=\mu\mathbf H=\mu_0(1+\chi_m)nI_f\,\hat{\mathbf z}$ (Eq. 6.31) and $\mathbf M=\chi_m\mathbf H=\chi_m nI_f\,\hat{\mathbf z}$
(Eq. 6.29). Substituting back into the definition,
$$\mathbf H=\frac{\mathbf B}{\mu_0}-\mathbf M=\big[(1+\chi_m)-\chi_m\big]nI_f\,\hat{\mathbf z}=nI_f\,\hat{\mathbf z},$$
recovering the original field — exactly what feeding `B_linear` and `magnetization_linear` through
`auxiliary_field_H` returns.

### P4.  The magnetized sphere and its demagnetizing field  *(Gr §6.2 Ex. 6.1; H-field §6.3.1, p.279)*
A sphere is uniformly magnetized, $\mathbf M=M\,\hat{\mathbf z}$. Its interior fields are
**uniform**: $\mathbf B_{\text{in}}=\tfrac{2}{3}\mu_0\mathbf M$ and $\mathbf H_{\text{in}}=-\mathbf M/3$.
Verify the defining relation $\mathbf B=\mu_0(\mathbf H+\mathbf M)$ holds inside, and
explain why $\mathbf H_{\text{in}}$ points *against* **M** (the **demagnetizing field**);
the exterior field is a pure dipole. *Check:* `magnetized_sphere_inner_B((0,0,M))`
$=(0,0,\tfrac{2}{3}\mu_0 M)$, `magnetized_sphere_inner_H((0,0,M))` $=(0,0,-M/3)$, and
$B_{\text{in}}=\mu_0(H_{\text{in}}+M)$ to machine precision.

**Solution.** Inside the uniformly magnetized sphere the fields are uniform (Eq. 6.16),
$\mathbf B_{\text{in}}=\tfrac{2}{3}\mu_0\mathbf M$. The auxiliary field follows from its definition (Eq. 6.18):
$$\mathbf H_{\text{in}}=\frac{\mathbf B_{\text{in}}}{\mu_0}-\mathbf M=\tfrac{2}{3}\mathbf M-\mathbf M=-\tfrac{1}{3}\mathbf M.$$
Check the constitutive relation: $\mu_0(\mathbf H_{\text{in}}+\mathbf M)=\mu_0\!\left(-\tfrac13\mathbf M+\mathbf M\right)=\tfrac23\mu_0\mathbf M=\mathbf B_{\text{in}}$. ✓
Because $\mathbf H_{\text{in}}=-\mathbf M/3$ points *against* $\mathbf M$ it is a **demagnetizing** field — sourced
by the effective magnetic charge $-\nabla\cdot\mathbf M$ on the poles. For $\mathbf M=8\times10^5\,\hat{\mathbf z}$ A/m
the code returns $\mathbf B_{\text{in}}=0.6702\,\hat{\mathbf z}$ T and $\mathbf H_{\text{in}}=-2.667\times10^5\,\hat{\mathbf z}$ A/m,
matching `magnetized_sphere_inner_B` and `magnetized_sphere_inner_H`.

### P5.  Classifying media and reading a hysteresis loop  *(Gr §6.4.1, p.284; §6.4.2, p.288)*
**(a)** For $\chi_m=-1.7\times10^{-5}$ (water), $2.5\times10^{-4}$ (paramagnetic metal),
and $5500$ (soft iron), name each class and compute $\mu/\mu_0=1+\chi_m$. **(b)** For a
ferromagnet with saturation $M_s$, coercive scale $H_c$, and loop width $w$, model the
two branches and identify the **remanence** $M_r=|M_\downarrow(0)|>0$ (a permanent
magnet) and the **coercivity** $H_c$ where $M_\downarrow(-H_c)=0$. Explain why an open
loop ($M_\downarrow(0)\neq M_\uparrow(0)$) means **M** depends on history. *Check:*
`classify_material` and `permeability` for (a); `hysteresis_branches`, `remanence`,
`coercivity` for (b) — confirm the descending branch is positive at $H=0$ and crosses
zero at $H=-H_c$.

**Solution.** **(a)** The relative permeability is $\mu/\mu_0=1+\chi_m$ (Eq. 6.33). Reading the sign and
size of $\chi_m$: water $\chi_m=-1.7\times10^{-5}<0$ → **diamagnetic**, $\mu/\mu_0=0.999983$; the metal
$\chi_m=2.5\times10^{-4}$ (small, positive) → **paramagnetic**, $\mu/\mu_0=1.00025$; soft iron $\chi_m=5500$
(large) → **ferromagnetic**, $\mu/\mu_0=5501$. **(b)** The descending branch is
$M_\downarrow(H)=M_s\tanh\!\big((H+H_c)/w\big)$. At $H=0$,
$$M_r=|M_\downarrow(0)|=M_s\tanh(H_c/w)=8\times10^5\tanh(2.5)=7.893\times10^5\ \text{A/m}>0,$$
the remanent (permanent) magnetization, while $M_\downarrow(-H_c)=M_s\tanh 0=0$ fixes the **coercivity**
$H_c=5\times10^3$ A/m. Since $M_\downarrow(0)>0>M_\uparrow(0)$ the loop is *open* — $\mathbf M$ at $H=0$
depends on whether the field was swept down or up, i.e. on history. These match `remanence`
($7.893\times10^5$), `coercivity` ($5\times10^3$), `classify_material` and `permeability`.
