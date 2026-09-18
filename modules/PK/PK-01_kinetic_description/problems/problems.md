# PK-01 — Problems

Work by hand, then check with `code/kinetic_description.py`. Citations in
`../refs.md`; **Mi** = Michel §1.2 / Appendix A.1, **Rh** = Rhodes (ed.) *Excimer
Lasers*, **Pa** = Pathria §6.4. Representative plasma throughout: n = 10¹⁸ m⁻³,
T = 1 eV (= 11604.5 K).

### P1.  Moments of the Maxwellian  *(Mi §1.2.3; Pa §6.4)*
From f_M(v) = n(m/2πk_BT)^{3/2} e^{−mv²/2k_BT}, show the zeroth moment ∫f d³v = n and
the second moment gives the pressure p = (m/3)∫|**v**|²f d³v = n k_BT, hence
⟨½mv²⟩ = (3/2)k_BT (equipartition). Remember the speed Jacobian d³v → 4πv² dv.
*Check:* `maxwellian` integrated against 4πv² returns n, and p = n k_BT
(`test_maxwellian_zeroth_moment_is_number_density`, `test_maxwellian_pressure_and_energy_moments`).

**Solution.** Put $\beta\equiv m/2k_BT$, so $f_M=n(\beta/\pi)^{3/2}e^{-\beta v^2}$ and isotropy turns
$d^3v$ into $4\pi v^2\,dv$. With the Gaussian moment $\int_0^\infty v^2e^{-\beta v^2}\,dv=\tfrac14\sqrt{\pi/\beta^3}$,
the zeroth moment is
$$\int f_M\,d^3v=n\Big(\frac{\beta}{\pi}\Big)^{3/2}4\pi\cdot\tfrac14\sqrt{\frac{\pi}{\beta^3}}=n\Big(\frac{\beta}{\pi}\Big)^{3/2}\frac{\pi^{3/2}}{\beta^{3/2}}=n.$$
The pressure uses $\int_0^\infty v^4e^{-\beta v^2}\,dv=\tfrac38\sqrt{\pi/\beta^5}$:
$$p=\frac{m}{3}\int v^2 f_M\,d^3v=\frac{m}{3}\,n\Big(\frac{\beta}{\pi}\Big)^{3/2}4\pi\cdot\tfrac38\sqrt{\frac{\pi}{\beta^5}}=\frac{m}{2\beta}\,n=nk_BT,$$
since $1/\beta=2k_BT/m$. The energy moment follows at once, $\int\tfrac12 mv^2 f_M\,d^3v=\tfrac32 p=\tfrac32 nk_BT$,
i.e. $\langle\tfrac12 mv^2\rangle=\tfrac32 k_BT$ — equipartition (`~SM-06`). Numerically
$\int f\,d^3v=1.0000\times10^{18}\ \mathrm{m^{-3}}=n$ and $p=1.6022\times10^{-1}\ \mathrm{Pa}=nk_BT$.

### P2.  The Vlasov equation is a continuity equation  *(Mi §1.2.4.1)*
Rewrite the collisionless Boltzmann (Vlasov) equation as
∂ₜf + ∇ₓ·(**v**f) + ∇ᵥ·(**a**f) = 0 and show that whenever ∇ₓ·**v** = 0 and
∇ᵥ·**a** = 0 (true for the Lorentz force) it reduces to df/dt = 0 along orbits —
Liouville's theorem. Identify exactly where the divergence-free property is used.
*Check:* `vlasov_residual` on a free-streamed f is ≈ 7×10⁻⁵, far below the streaming
term v∂ₓf ≈ 0.18 (`test_vlasov_residual_small_under_free_streaming`).

**Solution.** Write the Vlasov equation with $\mathbf a=\mathbf F/m$ and expand each phase-space flux by the product rule:
$$\nabla_{\mathbf x}\!\cdot(\mathbf v f)=(\nabla_{\mathbf x}\!\cdot\mathbf v)\,f+\mathbf v\cdot\nabla_{\mathbf x}f,\qquad \nabla_{\mathbf v}\!\cdot(\mathbf a f)=(\nabla_{\mathbf v}\!\cdot\mathbf a)\,f+\mathbf a\cdot\nabla_{\mathbf v}f.$$
Since $\mathbf x$ and $\mathbf v$ are independent coordinates, $\nabla_{\mathbf x}\!\cdot\mathbf v=0$; and the Lorentz
acceleration $\mathbf a=\tfrac{q}{m}(\mathbf E+\mathbf v\times\mathbf B)$ has $\nabla_{\mathbf v}\!\cdot\mathbf a=0$, because
$\mathbf E$ is independent of $\mathbf v$ and $\partial_{v_i}(\varepsilon_{ijk}v_jB_k)=\varepsilon_{ijk}\delta_{ij}B_k=0$.
Exactly there the two extra terms drop, so the conservative form collapses to the advective one:
$$\partial_t f+\nabla_{\mathbf x}\!\cdot(\mathbf v f)+\nabla_{\mathbf v}\!\cdot(\mathbf a f)=\partial_t f+\mathbf v\cdot\nabla_{\mathbf x}f+\mathbf a\cdot\nabla_{\mathbf v}f=\frac{df}{dt}=0$$
along the orbit $\dot{\mathbf x}=\mathbf v,\ \dot{\mathbf v}=\mathbf a$ — Liouville's theorem. Numerically, on a
free-streamed $f$ the residual $\partial_t f+v\partial_x f\approx7.287\times10^{-5}$ sits far below the streaming
term $v\partial_x f\approx1.814\times10^{-1}$, so phase-space continuity holds to discretization error.

### P3.  Free streaming shears phase space  *(Mi §1.2.4.1)*
For **F** = 0 solve ∂ₜf + v∂ₓf = 0 by characteristics to get f(x,v,t) = f₀(x − vt, v).
Explain why the velocity marginal ∫f dx and the total number ∫∫f dx dv are frozen,
while the density ∫f dv genuinely evolves, and why max f is unchanged (Liouville).
*Check:* `free_stream` conserves the total number and ∫f dx per velocity to machine
precision yet sheares f(x,v) (`test_free_streaming_shears_phase_space_conserving_marginals`).

**Solution.** With $\mathbf F=0$ each orbit conserves its velocity ($\dot v=0$), so the characteristics of
$\partial_t f+v\partial_x f=0$ are the straight lines $x(t)=x_0+vt$ at fixed $v$, along which $f$ is constant:
$$f(x,v,t)=f_0(x-vt,\,v).$$
The substitution $s=x-vt$ at fixed $v$ has unit Jacobian, so per velocity the marginal $\int f\,dx=\int f_0(s,v)\,ds$
is frozen, and with it the total number $\iint f\,dx\,dv$. But $\int f\,dv$ samples different velocities at fixed $x$
and genuinely evolves — that is the shear. And $(x,v)\mapsto(x-vt,v)$ is a measure-preserving shear that only
relabels phase points, so $\max f$ is unchanged — Liouville. Numerically `free_stream` holds
$\iint f\,dx\,dv=2.540050\times10^{3}$ and every per-velocity $\int f\,dx$ to machine precision while $f(x,v)$ visibly shears.

### P4.  Debye shielding  *(Mi §1.2.1)*
Linearize Poisson's equation with a Boltzmann electron response to obtain
∇²φ = φ/λ_D² and the screened potential φ(r) = (q_t/4πε₀r) e^{−r/λ_D}, with
λ_D = √(ε₀k_BT/nq²). Evaluate λ_D for the representative plasma and explain why beyond
λ_D a test charge is invisible. *Check:* `debye_length(1e18, 11604.5)` ≈ 7.4×10⁻⁶ m
and scales as √(T/n) (`test_debye_length_formula_and_scaling`).

**Solution.** Poisson's equation for a test charge $q_t$ in the electron gas is $\nabla^2\phi=-\rho/\varepsilon_0$ with
$\rho=q_t\delta(\mathbf r)+q(n_e-n)$. The electrons Boltzmann-distribute in their own potential; for $q\phi\ll k_BT$ linearize:
$$n_e=n\,e^{-q\phi/k_BT}\approx n\Big(1-\frac{q\phi}{k_BT}\Big)\ \Rightarrow\ q(n_e-n)\approx-\frac{nq^2}{k_BT}\,\phi.$$
Away from the source this is $\nabla^2\phi=\phi/\lambda_D^2$ with $\lambda_D=\sqrt{\varepsilon_0 k_BT/nq^2}$, whose decaying
point-source solution is the screened (Yukawa) potential
$$\phi(r)=\frac{q_t}{4\pi\varepsilon_0 r}\,e^{-r/\lambda_D}.$$
Beyond a few $\lambda_D$ the exponential extinguishes the field: the shielding cloud cancels the bare charge, which is
then invisible. For $n=10^{18}\ \mathrm{m^{-3}}$ and $T=11604.5\ \mathrm{K}$ (with $\lambda_D\propto\sqrt{T/n}$) this gives
`debye_length(1e18, 11604.5)` $\approx7.434\times10^{-6}\ \mathrm{m}\approx7.4\ \mu\mathrm{m}$.

### P5.  λ_D = v_T/ω_p and the plasma parameter  *(Mi §1.2.2; App. A.1)*
Derive the plasma frequency ω_p = √(nq²/ε₀m) (rigid electron displacement) and show
the Debye length equals the distance a thermal electron travels in one plasma period,
λ_D = v_T/ω_p. Evaluate Λ = nλ_D³ and argue the plasma is weakly coupled. *Check:*
`debye_length` equals `thermal_speed`/`plasma_frequency`, and
`plasma_parameter(1e18, 11604.5)` ≈ 411 ≫ 1
(`test_debye_equals_thermal_speed_over_plasma_frequency`, `test_plasma_parameter_weakly_coupled`).

**Solution.** Displace the electron slab rigidly by $\xi$; the bared faces carry surface charge $\sigma=nq\xi$ and set up
a uniform restoring field $E=\sigma/\varepsilon_0=nq\xi/\varepsilon_0$, so each electron obeys
$$m\ddot\xi=-qE=-\frac{nq^2}{\varepsilon_0}\,\xi\ \Rightarrow\ \omega_p=\sqrt{\frac{nq^2}{\varepsilon_0 m}}.$$
Forming the ratio with $v_T=\sqrt{k_BT/m}$, the mass cancels:
$$\frac{v_T}{\omega_p}=\sqrt{\frac{k_BT}{m}\cdot\frac{\varepsilon_0 m}{nq^2}}=\sqrt{\frac{\varepsilon_0 k_BT}{nq^2}}=\lambda_D,$$
so $\lambda_D$ is the distance a thermal electron coasts in one plasma period. Then
$\Lambda=n\lambda_D^3=10^{18}(7.434\times10^{-6})^3\approx411$ particles per Debye sphere, so the nearest-neighbour
Coulomb energy $\ll$ thermal energy — weakly coupled. This matches `debye_length` $=$ `thermal_speed` $/$ `plasma_frequency`
$=7.434\times10^{-6}\ \mathrm{m}$ and `plasma_parameter(1e18, 11604.5)` $\approx410.8\gg1$.

### P6.  When does Vlasov beat Boltzmann?  *(Mi §1.4; Rh Ch.4; ~PK-04)*
The electron–ion collision rate obeys ν_ei/ω_p ∼ lnΛ/Λ. Explain why a large Debye
sphere (Λ ≫ 1) makes the collisionless Vlasov equation the right leading description,
with the collision term — the rare-gas-halide formation/quenching chemistry of the
KrF system (Rh §4.2, §7.2; the KrF/LoKI code, `~PK-04`) — a slow correction. *Check
(conceptual):* `plasma_parameter` ≫ 1 ⇒ ν_ei/ω_p ≪ 1, and `plasma_parameter(n, 4T)` >
`plasma_parameter(n, T)` — a hotter (or thinner) plasma is more ideal.

**Solution.** Two collective rates compete: the mean-field oscillation $\omega_p$ and the Coulomb collision rate
$\nu_{ei}$. Many small-angle deflections across the Debye sphere accumulate to
$$\frac{\nu_{ei}}{\omega_p}\sim\frac{\ln\Lambda}{\Lambda},$$
with $\ln\Lambda$ the Coulomb logarithm (impact parameters from the distance of closest approach out to $\lambda_D$).
When $\Lambda\gg1$ this ratio is $\ll1$: over one plasma period $f$ scarcely feels a collision, so the Boltzmann
right-hand side is negligible and the mean-field **Vlasov** equation is the correct leading description — the collision
term (the rare-gas-halide formation/quenching chemistry and EEDF of the KrF/LoKI system, `~PK-04`) entering only as an
$O(\ln\Lambda/\Lambda)$ correction. Since $\lambda_D\propto\sqrt{T/n}$ gives $\Lambda\propto T^{3/2}/\sqrt{n}$, heating or
thinning raises $\Lambda$. The check bears this out: `plasma_parameter` $\approx411\gg1$ makes
$\nu_{ei}/\omega_p\sim\ln(411)/411\approx0.015\ll1$, and `plasma_parameter(n, 4T)` $=4^{3/2}\Lambda=8\Lambda$ exceeds
`plasma_parameter(n, T)` — a hotter (or thinner) plasma is more ideal.
