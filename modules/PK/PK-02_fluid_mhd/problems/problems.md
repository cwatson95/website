# PK-02 — Problems

Work by hand, then check with `code/fluid_mhd.py`. Citations in `../refs.md`;
**Mi** = Michel Ch.1 (cited at section level), **Rh** = Rhodes *Excimer Lasers*.
Representative magnetized plasma throughout: n = 10¹⁹ m⁻³, T ≈ 100 eV (1.16×10⁶ K),
B = 1 T, hydrogen (ρ = nm_p), γ = 5/3.

### P1.  Moments of a drifting Maxwellian  *(Mi §1.2.3–1.2.4)*
For f(**v**) = n(m/2πk_BT)^{3/2} exp[−m|**v**−**u**|²/2k_BT], evaluate the first three
velocity moments and show they return ∫f d³v = n (0th), (1/n)∫**v**f d³v = **u** (1st),
and (m/3)∫|**v**−**u**|²f d³v = nk_BT (the scalar pressure, 2nd). Why does the 2nd
central moment give p = nk_BT for *any* drift **u**? *Check:* `moments_of_maxwellian(1e19,
(1e5,0,0), 1e5, M_P)` returns n = 1.0×10¹⁹, u_x = 1.0×10⁵, and p = 13.8 Pa = n·K_B·T.

*Answer:* 0th → $n$, 1st → $\mathbf u$, 2nd central → $p=nk_BT$ (drift-independent).

**Solution.** Shift to the comoving (random) velocity $\mathbf w=\mathbf v-\mathbf u$, where
$f=n(m/2\pi k_BT)^{3/2}e^{-mw^2/2k_BT}$ is an isotropic Gaussian. The **0th** moment is just
the normalized Gaussian,
$$\int f\,d^3v=n\Big(\frac{m}{2\pi k_BT}\Big)^{3/2}\!\int e^{-mw^2/2k_BT}\,d^3w=n,$$
since $\int e^{-mw^2/2k_BT}\,d^3w=(2\pi k_BT/m)^{3/2}$. The **1st** moment splits as
$\mathbf v=\mathbf u+\mathbf w$; the $\mathbf w$ part is an odd integrand and drops, so
$\frac1n\int\mathbf v f\,d^3v=\mathbf u+\langle\mathbf w\rangle=\mathbf u$. The **2nd** central
moment uses the per-axis variance $\langle w_i^2\rangle=k_BT/m$,
$$p=\frac{m}{3}\!\int|\mathbf w|^2 f\,d^3v=\frac{m}{3}\,n\Big(\frac{3k_BT}{m}\Big)=nk_BT.$$
It is drift-independent because the central moment is measured *about* $\mathbf u$ — subtracting
the bulk motion leaves only the thermal spread, which is precisely what pressure is. Hence the
code returns $n=1.0\times10^{19}$, $u_x=1.0\times10^{5}$, and $p=nk_BT=13.8$ Pa.

### P2.  The zeroth moment is continuity  *(Mi §1.2.4.2, Eq. 1.63; → `~CM-22`)*
Integrate the Vlasov equation over **v** and show the force term vanishes (boundary
terms at |**v**|→∞), leaving ∂n/∂t + ∇·(n**u**) = 0. Identify which conserved density
this is in `~CM-22` (mass) and `~QM-04` (probability) — KEY BRIDGE B2. *Check:* for a
rigidly advected bump ρ = exp[−(x−ut)²], `continuity_residual(rho0, rho1, u, dx, dt)`
is ≈ 3×10⁻³, far below the ≈ 0.43 size of ∂ρ/∂t itself.

*Answer:* $\partial_t n+\nabla\cdot(n\mathbf u)=0$; the conserved density is mass in `~CM-22`,
probability in `~QM-04`.

**Solution.** Integrate the Vlasov equation
$\partial_t f+\mathbf v\cdot\nabla_x f+\frac{\mathbf F}{m}\cdot\nabla_v f=0$ over $d^3v$. The first
term is $\int\partial_t f\,d^3v=\partial_t n$. In the second, $\mathbf v$ is an independent
coordinate, so it passes through the spatial gradient,
$\int\mathbf v\cdot\nabla_x f\,d^3v=\nabla\cdot\!\int\mathbf v f\,d^3v=\nabla\cdot(n\mathbf u)$.
The force is divergence-free in velocity ($\nabla_v\cdot(\mathbf E+\mathbf v\times\mathbf B)=0$),
so $\mathbf F\cdot\nabla_v f=\nabla_v\cdot(\mathbf F f)$ is a pure velocity-space divergence and
converts to a surface integral that vanishes as $f\to0$ at infinity,
$$\int\frac{\mathbf F}{m}\cdot\nabla_v f\,d^3v=\frac1m\oint_{|\mathbf v|\to\infty}\!f\,\mathbf F\cdot d\mathbf S_v=0.$$
What survives is the continuity equation,
$$\frac{\partial n}{\partial t}+\nabla\cdot(n\mathbf u)=0.$$
This is the same local law $\partial_t(\text{density})+\nabla\cdot(\text{flux})=0$ carried by mass
in `~CM-22` (density $\rho$) and probability in `~QM-04` (density $|\psi|^2$) — KEY BRIDGE B2;
only the conserved density changes. For the rigid bump $\rho=e^{-(x-ut)^2}$ the finite-difference
residual is $\approx3\times10^{-3}$, far below the $\approx0.43$ size of $\partial\rho/\partial t$
itself.

### P3.  First moment, and the closure problem  *(Mi §1.2.4.2, Eqs. 1.73–1.74)*
Take the **v**-weighted moment to get m n(∂**u**/∂t + **u**·∇**u**) = −∇·**P** +
qn(**E**+**u**×**B**), and explain why the hierarchy never closes (continuity needs **u**,
momentum needs **P**, …). Apply the polytropic closure p = Cρ^γ with γ = (N+2)/N: what
is γ for 1-D adiabatic plasma-wave compression (N = 1), and for a 3-D monatomic plasma?
*Check:* the closure fixes the sound speed; `sound_speed(5/3, 1e19*K_B*1.16e6, 1e19*M_P)`
≈ 1.26×10⁵ m/s (and the pressure input is the p = nk_BT recovered in P1).

*Answer:* $\gamma=3$ for 1-D ($N=1$) compression, $\gamma=5/3$ for a 3-D monatomic ($N=3$) plasma.

**Solution.** Multiply Vlasov by $m\mathbf v$ and integrate. The inertial terms give
$\partial_t(mn\mathbf u)+\nabla\cdot(mn\langle\mathbf{vv}\rangle)$ with
$\langle\mathbf{vv}\rangle=\mathbf u\mathbf u+\mathsf P/(mn)$, and the Lorentz term gives
$qn(\mathbf E+\mathbf u\times\mathbf B)$. Expanding the derivatives and using continuity to cancel
the $\mathbf u\,[\partial_t n+\nabla\cdot(n\mathbf u)]$ piece collapses the inertia to the
convective form,
$$mn\!\left(\frac{\partial\mathbf u}{\partial t}+\mathbf u\cdot\nabla\mathbf u\right)=-\nabla\cdot\mathsf P+qn(\mathbf E+\mathbf u\times\mathbf B).$$
The hierarchy never closes: continuity (for $n$) needs $\mathbf u$, momentum (for $\mathbf u$) needs
the 2nd moment $\mathsf P$, the pressure equation would need the 3rd-moment heat flux $\mathbf q$,
and so on. Truncate polytropically, $p=C\rho^\gamma$ with $\gamma=(N+2)/N$: **1-D** plasma-wave
compression has $N=1\Rightarrow\gamma=3$, a **3-D monatomic** plasma $N=3\Rightarrow\gamma=5/3$.
This $\gamma$ fixes the sound speed; with $\gamma=5/3$ and $p=nk_BT$ from P1,
$$c_s=\sqrt{\frac{\gamma p}{\rho}}=\sqrt{\frac{5}{3}\frac{nk_BT}{nm_p}}\approx1.26\times10^5\ \text{m/s},$$
matching `sound_speed(5/3, 1e19*K_B*1.16e6, 1e19*M_P)` $\approx1.263\times10^5$ m/s.

### P4.  Sound vs Alfvén speed  *(Mi §1.3.1–1.3.2; standard MHD)*
Compute c_s = √(γp/ρ) and v_A = B/√(μ₀ρ) for the plasma above and show c_s ≪ v_A —
the field is far "stiffer" than the gas here. By what factor does v_A change if the
density quadruples? *Check:* `sound_speed(5/3, 1e19*K_B*1.16e6, 1e19*M_P)` ≈ 1.26×10⁵
m/s and `alfven_speed(1.0, 1e19*M_P)` ≈ 6.90×10⁶ m/s (ratio v_A/c_s ≈ 55);
`alfven_speed(1.0, 4*1e19*M_P)` is half of `alfven_speed(1.0, 1e19*M_P)`.

*Answer:* $c_s\approx1.26\times10^5$, $v_A\approx6.90\times10^6$ m/s ($v_A/c_s\approx55$);
quadrupling $\rho$ halves $v_A$.

**Solution.** With $\gamma=\frac53$, $p=nk_BT\approx160$ Pa and
$\rho=nm_p\approx1.67\times10^{-8}$ kg/m³, the two speeds are
$$c_s=\sqrt{\frac{\gamma p}{\rho}}\approx1.26\times10^5\ \text{m/s},\qquad v_A=\frac{B}{\sqrt{\mu_0\rho}}=\frac{1}{\sqrt{(4\pi\times10^{-7})(1.67\times10^{-8})}}\approx6.90\times10^6\ \text{m/s}.$$
Their ratio is $v_A/c_s\approx55$, so $c_s\ll v_A$: magnetic tension is far stiffer than the gas
here — the same verdict as $\beta\ll1$ in P6. Because $v_A\propto\rho^{-1/2}$, quadrupling the
density multiplies $v_A$ by $1/\sqrt4=\tfrac12$. This matches `sound_speed(...)`
$\approx1.26\times10^5$ m/s and `alfven_speed(1.0, 1e19*M_P)` $\approx6.90\times10^6$ m/s
(ratio $\approx55$), with `alfven_speed(1.0, 4*1e19*M_P)` exactly half of
`alfven_speed(1.0, 1e19*M_P)`.

### P5.  Fast magnetosonic speed  *(Mi Ch.1; standard MHD)*
For propagation **k** ⊥ **B**, gas pressure and magnetic pressure restore the wave
together, giving v_fast = √(c_s² + v_A²). Show v_fast ≥ max(c_s, v_A), and that it
reduces to c_s when B → 0 and to v_A when p → 0. *Check:*
`fast_magnetosonic_speed(1.263e5, 6.898e6)` ≈ 6.90×10⁶ m/s = √(c_s²+v_A²), only
marginally above v_A because c_s ≪ v_A here.

*Answer:* $v_{\text{fast}}=\sqrt{c_s^2+v_A^2}\ge\max(c_s,v_A)$; $\to c_s$ as $B\to0$, $\to v_A$ as
$p\to0$.

**Solution.** For $\mathbf k\perp\mathbf B$ a compression squeezes the gas and the field together,
so gas pressure and magnetic pressure restore the wave in parallel and their squared speeds add,
$v_{\text{fast}}=\sqrt{c_s^2+v_A^2}$. Since both terms are non-negative,
$$v_{\text{fast}}^2=c_s^2+v_A^2\ge\max(c_s^2,v_A^2)\ \Rightarrow\ v_{\text{fast}}\ge\max(c_s,v_A),$$
with equality only when the other speed vanishes: $B\to0\Rightarrow v_A\to0\Rightarrow v_{\text{fast}}\to c_s$
(pure sound), and $p\to0\Rightarrow c_s\to0\Rightarrow v_{\text{fast}}\to v_A$ (pure compressional
Alfvén). Numerically
$$v_{\text{fast}}=\sqrt{(1.263\times10^5)^2+(6.898\times10^6)^2}\approx6.90\times10^6\ \text{m/s},$$
only a hair above $v_A$ because $c_s^2/v_A^2\approx(1/55)^2\approx3\times10^{-4}$. This matches
`fast_magnetosonic_speed(1.263e5, 6.898e6)` $\approx6.90\times10^6$ m/s $=\sqrt{c_s^2+v_A^2}$.

### P6.  Magnetic pressure & plasma β  *(Mi Ch.1; standard MHD; Rh for context)*
Define the magnetic pressure P_B = B²/2μ₀ and the plasma β = p/(B²/2μ₀) = nk_BT/(B²/2μ₀).
Compute both for the plasma above; is it magnetically or gas-pressure dominated? How
does β scale with B? (A KrF discharge/e-beam plasma, Rh, is essentially unmagnetized —
β ≫ 1 — so the fluid momentum balance there is pressure- and collision-driven, not
**J**×**B**.) *Check:* `magnetic_pressure(1.0)` ≈ 3.98×10⁵ Pa and `plasma_beta(1e19,
1.16e6, 1.0)` ≈ 4.0×10⁻⁴ ≪ 1 (magnetically dominated); β ∝ 1/B², so doubling B gives
β ≈ 1.0×10⁻⁴.

*Answer:* $P_B\approx3.98\times10^5$ Pa, $\beta\approx4.0\times10^{-4}\ll1$ (magnetically
dominated); $\beta\propto1/B^2$.

**Solution.** The magnetic pressure is
$$P_B=\frac{B^2}{2\mu_0}=\frac{1^2}{2(4\pi\times10^{-7})}\approx3.98\times10^5\ \text{Pa},$$
while the gas pressure is $p=nk_BT\approx160$ Pa. Their ratio is the plasma beta,
$$\beta=\frac{p}{B^2/2\mu_0}=\frac{nk_BT}{B^2/2\mu_0}=\frac{160}{3.98\times10^5}\approx4.0\times10^{-4}\ll1,$$
so the plasma is **magnetically dominated** — the field pressure beats the gas pressure by a factor
$\sim1/\beta\approx2500$. With $p$ fixed and $P_B\propto B^2$, the beta scales as $\beta\propto1/B^2$,
so doubling $B$ drops it to $\beta/4\approx1.0\times10^{-4}$. (A KrF discharge/e-beam plasma, by
contrast, is essentially unmagnetized, $\beta\gg1$, so its momentum balance is set by pressure and
collisions, not $\mathbf J\times\mathbf B$.) This matches `magnetic_pressure(1.0)`
$\approx3.98\times10^5$ Pa and `plasma_beta(1e19, 1.16e6, 1.0)` $\approx4.0\times10^{-4}\ll1$,
with $\beta\approx1.0\times10^{-4}$ after doubling $B$.
