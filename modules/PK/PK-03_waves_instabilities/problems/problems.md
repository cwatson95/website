# PK-03 — Problems

Work by hand, then check with `code/plasma_waves.py`. Citations in `../refs.md`;
**M** = Michel, *Introduction to Laser-Plasma Interactions* (section level). The
fiducial plasma below is n = 10¹⁸ m⁻³, T = 10⁴ K, giving ω_p ≈ 5.64×10¹⁰ rad/s and
λ_D ≈ 6.90×10⁻⁶ m.

### P1.  The two scales  *(M §1.2.1–1.2.2)*
From the slab-displacement restoring field, derive ω_p = √(n e²/ε₀m_e), and from
thermal screening derive λ_D = √(ε₀k_BT/n e²). Show the identity λ_D = v_th/ω_p
(one thermal step per plasma period) with v_th = √(k_BT/m). *Check:*
`plasma_frequency(1e18, e, m_e)` ≈ 5.64e10 rad/s; `debye_length(1e18, 1e4, e)` ≈
6.90e-6 m equals `thermal_speed(1e4, m_e)`/ω_p.

**Solution.** Pull a slab of electrons aside by $x$; the exposed surface charge
$\sigma=nex$ makes a parallel-plate field $E=\sigma/\varepsilon_0=nex/\varepsilon_0$, so every
electron feels a linear restoring force,
$$m_e\ddot x=-eE=-\frac{ne^2}{\varepsilon_0}\,x\;\Rightarrow\;\ddot x=-\omega_p^2x,\qquad
\omega_p=\sqrt{\frac{ne^2}{\varepsilon_0 m_e}}.$$
Screening is the static cousin: linearizing Boltzmann electrons
$n=n_0e^{e\phi/k_BT}\approx n_0(1+e\phi/k_BT)$ in Poisson's equation gives
$\nabla^2\phi=\phi/\lambda_D^2$ with
$$\lambda_D=\sqrt{\frac{\varepsilon_0 k_BT}{ne^2}}
=\sqrt{\frac{k_BT}{m}}\Big/\sqrt{\frac{ne^2}{\varepsilon_0 m}}=\frac{v_{th}}{\omega_p}.$$
For $n=10^{18}\,\mathrm{m^{-3}}$ and $T=10^4\,$K this gives
$\omega_p=5.64\times10^{10}\,$rad/s and $\lambda_D=6.90\times10^{-6}\,$m, equal to
$v_{th}/\omega_p$ with $v_{th}=3.89\times10^5\,$m/s — matching `plasma_frequency` and
`debye_length`.

### P2.  Bohm–Gross dispersion  *(M §1.3.1.4)*
Show the warm-electron pressure (1-D adiabatic, γ=3) turns the cold oscillation into
the propagating wave ω² = ω_p² + 3k²v_th² = ω_p²(1+3k²λ_D²). Confirm the cold limit
ω→ω_p as k→0 and that the wave is always above cutoff. *Check:* `bohm_gross` with
k=0.01/λ_D gives ω/ω_p ≈ 1.0001; with k=0.5/λ_D gives ω/ω_p ≈ 1.323; ω(k)² equals
ω_p²+3(k v_th)² exactly.

**Solution.** Linearize the warm-electron fluid about a uniform background: continuity
$\partial_t n_1+n_0\partial_x u=0$, momentum $m n_0\partial_t u=-en_0E-\partial_x p_1$,
and Poisson $\varepsilon_0\partial_x E=-en_1$, closed by the 1-D adiabatic law
$p_1=3k_BT\,n_1$ ($\gamma=3$ for one compressional degree of freedom). Eliminating
$u,E,p_1$ for a plane wave $e^{i(kx-\omega t)}$ collapses them to a single wave equation,
$$-\omega^2n_1=-\omega_p^2n_1-3k^2\frac{k_BT}{m}\,n_1
\;\Rightarrow\;\omega^2=\omega_p^2+3k^2v_{th}^2=\omega_p^2\big(1+3k^2\lambda_D^2\big),$$
using $v_{th}=\omega_p\lambda_D$. As $k\to0$ the pressure term dies and $\omega\to\omega_p$
(the cold cutoff); since $3k^2\lambda_D^2\ge0$ the wave always rides above $\omega_p$.
Numerically $k\lambda_D=0.01$ gives $\omega/\omega_p=\sqrt{1+3(0.01)^2}\approx1.0001$ and
$k\lambda_D=0.5$ gives $\sqrt{1+3(0.25)}=\sqrt{1.75}\approx1.323$, matching `bohm_gross`.

### P3.  Ion-acoustic sound and its saturation  *(M §1.3.1.5)*
Treating electrons as a Boltzmann fluid and ions as inertia, derive
ω = k c_s/√(1+k²λ_D²) with c_s = √(k_BT_e/m_i). Show ω≈k c_s (non-dispersive sound)
for k λ_D≪1, that the phase speed ω/k decreases with k, and that ω saturates at the
ion plasma frequency ω_pi = c_s/λ_D as kλ_D→∞. *Check:* `ion_acoustic` at small
k λ_D gives ω/k = c_s; at large k λ_D it tends to `plasma_frequency(n, e, m_i)` ≈
1.32e9 rad/s.

**Solution.** On the slow ion timescale the light electrons stay Boltzmann-distributed,
$n_{e1}/n_0=e\phi/k_BT_e$, while cold ions carry the inertia. Ion momentum
$m_i(-i\omega)u=-ike\phi$ and continuity $-i\omega n_{i1}+ikn_0u=0$ give
$n_{i1}=n_0ek^2\phi/(m_i\omega^2)$; substituting both densities into Poisson
$-\varepsilon_0k^2\phi=-e(n_{i1}-n_{e1})$ yields
$$\frac{\omega_{pi}^2}{\omega^2}=1+\frac{1}{k^2\lambda_D^2},\qquad
\omega_{pi}^2=\frac{ne^2}{\varepsilon_0 m_i}.$$
Solving for $\omega$ and using $\omega_{pi}\lambda_D=\sqrt{k_BT_e/m_i}=c_s$,
$$\omega=\frac{kc_s}{\sqrt{1+k^2\lambda_D^2}}.$$
For $k\lambda_D\ll1$ this is non-dispersive sound $\omega\simeq kc_s$; the phase speed
$\omega/k=c_s/\sqrt{1+k^2\lambda_D^2}$ falls as $k$ grows; and for $k\lambda_D\gg1$ it
saturates at $\omega\to c_s/\lambda_D=\omega_{pi}$. That ceiling is
`plasma_frequency(n, e, m_i)`$\approx1.32\times10^9\,$rad/s, the large-$k\lambda_D$ limit
that `ion_acoustic` approaches.

### P4.  Landau damping of a Langmuir wave  *(M §1.3.4 / Formulary A.4)*
Argue that particles resonant at v=ω/k exchange energy with the wave, so the rate is
set by ∂f₀/∂v there; a falling Maxwellian (∂_v f₀<0) gives net loss, γ<0. Evaluate
the closed form γ/ω_p = −√(π/8)(kλ_D)⁻³ exp(−1/2(kλ_D)²−3/2) and explain why it is
exponentially weak for kλ_D≪1. *Check:* `landau_damping_rate` gives γ<0 with
γ/ω_p ≈ −0.020, −0.096, −0.151 at kλ_D = 0.3, 0.4, 0.5 (|γ| grows with kλ_D), and
< 10⁻⁴ in magnitude at kλ_D = 0.15.

**Solution.** A particle at the phase velocity $v=\omega/k$ sees a nearly static field
and trades energy resonantly — those just slower than the wave gain, those just faster
lose — so the net rate tracks the slope of $f_0$ there (notes §5),
$\gamma=\tfrac{\pi}{2}(\omega_p^3/k^2)\,\partial_v f_0|_{\omega/k}$. For a Maxwellian
$f_0\propto e^{-v^2/2v_{th}^2}$ the slope $\partial_v f_0=-(v/v_{th}^2)f_0$ is negative, so
$\gamma<0$ — loss. Setting $v=\omega/k$ with the Bohm–Gross
$\omega^2=\omega_p^2(1+3k^2\lambda_D^2)$ puts the exponent at
$-\tfrac{v^2}{2v_{th}^2}=-\tfrac{1}{2(k\lambda_D)^2}-\tfrac32$, and the prefactor collapses
via $\tfrac{\pi}{2}/\sqrt{2\pi}=\sqrt{\pi/8}$ and $\omega_p^4/(k^3v_{th}^3)=\omega_p(k\lambda_D)^{-3}$ to
$$\frac{\gamma}{\omega_p}=-\sqrt{\frac{\pi}{8}}\,\frac{1}{(k\lambda_D)^3}
\exp\!\left(-\frac{1}{2(k\lambda_D)^2}-\frac32\right).$$
It is exponentially weak for $k\lambda_D\ll1$ because the resonance $v\approx v_{th}/k\lambda_D$
then sits far on the tail where almost no particles live. This returns
$\gamma/\omega_p\approx-0.020,-0.096,-0.151$ at $k\lambda_D=0.3,0.4,0.5$ and
$|\gamma|/\omega_p<10^{-4}$ at $k\lambda_D=0.15$, matching `landau_damping_rate`.

### P5.  Two-stream instability band  *(M §1.3.1.3)*
For two cold beams at ±v₀ (each density n/2), write 1 = ½ω_p²[1/(ω−kv₀)²+1/(ω+kv₀)²],
clear to the bi-quadratic ω⁴−(2a+ω_p²)ω²+(a²−ω_p²a)=0 with a=(kv₀)², and show the
lower root ω²<0 (a growing mode) exactly when kv₀<ω_p. *Check:* `two_stream_growth_rate`
is >0 for kv₀ = 0.5ω_p and exactly 0.0 for kv₀ = 1.5ω_p (outside the band).

**Solution.** Multiply through by $(\omega-kv_0)^2(\omega+kv_0)^2=(\omega^2-a)^2$ with
$a=(kv_0)^2$, using $(\omega+kv_0)^2+(\omega-kv_0)^2=2(\omega^2+a)$:
$$(\omega^2-a)^2=\frac{\omega_p^2}{2}\cdot2(\omega^2+a)=\omega_p^2(\omega^2+a)
\;\Rightarrow\;\omega^4-(2a+\omega_p^2)\omega^2+(a^2-\omega_p^2a)=0.$$
This is a quadratic in $\omega^2$ whose discriminant simplifies to $\omega_p^2(8a+\omega_p^2)$:
$$\omega^2=\tfrac12\Big[(2a+\omega_p^2)\pm\omega_p\sqrt{8a+\omega_p^2}\Big].$$
The lower ($-$) root is negative iff $(2a+\omega_p^2)^2<\omega_p^2(8a+\omega_p^2)$, which
reduces to $4a^2<4a\omega_p^2$, i.e. $a<\omega_p^2$ — exactly $kv_0<\omega_p$. There
$\omega^2<0$ makes $\omega=i\gamma$ a purely growing mode. So `two_stream_growth_rate`
is $>0$ at $kv_0=0.5\,\omega_p$ (inside the band) and clips to $0.0$ at $kv_0=1.5\,\omega_p$
(outside).

### P6.  Maximum two-stream growth rate  *(M §1.3.1.3; cf. Ch. 6)*
Maximize the growth rate Im ω = √(−ω²) over k inside the band and show the peak is
γ_max = ω_p/√8 ≈ 0.354 ω_p, reached at kv₀ = √(3/8) ω_p ≈ 0.612 ω_p. Why is the
fastest-growing wavelength comparable to v₀/ω_p (the beam's "Debye-like" scale)?
*Check:* scanning `two_stream_growth_rate` over k, the maximum of Im ω/ω_p is
≈ 0.354 = 1/√8 at kv₀/ω_p ≈ 0.612.

**Solution.** Inside the band the growing root of P5 gives
$\gamma^2=-\omega^2=\tfrac12\big[\omega_p\sqrt{8a+\omega_p^2}-(2a+\omega_p^2)\big]$,
$a=(kv_0)^2$. Maximize over $a$:
$$\frac{d\gamma^2}{da}=\frac12\!\left[\frac{4\omega_p}{\sqrt{8a+\omega_p^2}}-2\right]=0
\;\Rightarrow\;\sqrt{8a+\omega_p^2}=2\omega_p\;\Rightarrow\;a=\tfrac38\omega_p^2,$$
so $kv_0=\sqrt{3/8}\,\omega_p\approx0.612\,\omega_p$. Substituting back,
$$\gamma_{\max}^2=\tfrac12\big[\omega_p(2\omega_p)-(\tfrac34\omega_p^2+\omega_p^2)\big]
=\tfrac12\cdot\tfrac14\omega_p^2=\frac{\omega_p^2}{8}
\;\Rightarrow\;\gamma_{\max}=\frac{\omega_p}{\sqrt8}\approx0.354\,\omega_p.$$
The peak sits at $k\sim\omega_p/v_0$, i.e. wavelength $\lambda\sim v_0/\omega_p$ — the beam's
"Debye-like" length (how far a beam particle drifts in one plasma period): shorter modes
have $kv_0>\omega_p$ and fall outside the band, longer ones couple weakly. Scanning
`two_stream_growth_rate` reproduces $\mathrm{Im}\,\omega/\omega_p\approx0.3536=1/\sqrt8$ at
$kv_0/\omega_p\approx0.612$.

### P7.  One dielectric function, two fates  *(M §1.3.3)*
Both damping and growth come from the same kinetic dielectric function
ε(k,ω) = 1 − (ω_p²/k²)∫_L ∂_v f₀/(v−ω/k) dv = 0, evaluated on the Landau contour
(`~MA-06`). Explain how the *sign of ∂f₀/∂v at the resonance* selects Landau damping
(Maxwellian, falling slope) versus the two-stream instability (counter-streaming
beams, rising slope between them). *(Conceptual — connect the §5 and §6 code: the
beam in P5 is just an f₀ with positive slope where the Maxwellian of P4 has negative
slope.)*

**Solution.** On the Landau contour the resonant denominator splits by the Plemelj rule,
$1/(v-\omega/k)\to\mathrm{P.V.}\,1/(v-\omega/k)-i\pi\,\delta(v-\omega/k)$, so the dielectric
function acquires an imaginary part fixed by the residue at the resonance:
$$\operatorname{Im}\varepsilon(k,\omega)\;\propto\;\frac{\omega_p^2}{k^2}\,
\frac{\partial f_0}{\partial v}\Big|_{v=\omega/k}.$$
Writing $\omega=\omega_r+i\gamma$ and solving $\varepsilon=0$ to first order gives
$\gamma=-\operatorname{Im}\varepsilon/(\partial_\omega\!\operatorname{Re}\varepsilon)\propto
\partial_v f_0|_{\omega/k}$: the growth rate inherits the sign of the slope at $v=\omega/k$.
A single-hump Maxwellian falls for all $v>0$, so the resonance lands on a negative slope
and the wave damps (P4); two counter-streaming beams instead carve a valley at $v=0$ with a
**rising** slope between them, and a mode with $\omega/k$ in that gap meets
$\partial_v f_0>0$ and grows (P5–P6). Same residue, opposite sign — the two-stream $f_0$ is
just the Maxwellian's falling slope flipped upward where the resonant particles sit.
