# QF-05 — Problems

Work each by hand, then check with `code/curved_spacetime.py`. Citations in
`../refs.md`; **BD** = Birrell & Davies (chapter-level), **Ful** = Fulling.
All numbers are SI.

### P1.  Bogoliubov normalization and the squeezed vacuum  *(BD §2.2; Ful)*
From a′_j = Σ_k(α*_{jk} a_k − β*_{jk} a_k†) and the demand that
[a′_j, a′_{j′}†] = δ_{jj′}, derive the normalization Σ_k(|α_{jk}|² − |β_{jk}|²) = 1.
Then specialize to a single squeezed mode, α = cosh r, β = sinh r, and show the
rotated vacuum holds ⟨N⟩ = sinh²r particles. *Check:* `squeeze_to_bogoliubov(1.3)`
then `bogoliubov_check(...)` = 1.0 and `particle_number(beta)` = sinh²(1.3) ≈ 2.884.

**Solution.** Expand the adjoint $a_{j'}^{\prime\dagger}=\sum_l(\alpha_{j'l}\,a_l^\dagger-\beta_{j'l}\,a_l)$ and
commute it against $a'_j$ using $[a_k,a_l^\dagger]=\delta_{kl}$ (all other commutators vanish):
$$[a'_j,a_{j'}^{\prime\dagger}]=\sum_k\big(\alpha_{jk}^*\alpha_{j'k}-\beta_{jk}^*\beta_{j'k}\big).$$
Setting this to $\delta_{jj'}$ and taking $j=j'$ gives the normalization
$\sum_k(|\alpha_{jk}|^2-|\beta_{jk}|^2)=1$. A single squeezed mode $\alpha=\cosh r,\ \beta=\sinh r$
satisfies it automatically, $\cosh^2 r-\sinh^2 r=1$. Its rotated vacuum holds
$\langle N\rangle=\lVert a'|0\rangle\rVert^2$; since $a'|0\rangle=(\alpha^*a-\beta^*a^\dagger)|0\rangle=-\beta^*|1\rangle$,
$$\langle N\rangle=|\beta|^2=\sinh^2 r.$$
At $r=1.3$, $(\cosh r,\sinh r)=(1.971,1.698)$, so `bogoliubov_check`$=1.971^2-1.698^2=1.0$ and
`particle_number`$=\sinh^2 1.3\approx2.884$.

### P2.  The Unruh temperature scale  *(BD §4.5)*
Starting from T_U = ℏa/2πck_B, confirm it is **linear** in the proper acceleration
and estimate the acceleration needed to reach T_U = 1 K (a ≈ 2.5×10²⁰ m/s²). Why is
the Unruh effect undetectable for everyday accelerations? *Check:*
`unruh_temperature(1e20)` ≈ 0.4055 K, `unruh_temperature(9.81)` ≈ 3.98×10⁻²⁰ K, and
`unruh_temperature(2e20)/unruh_temperature(1e20)` = 2.0.

**Solution.** In $T_U=\dfrac{\hbar a}{2\pi c\,k_B}$ every factor but $a$ is a constant, so $T_U\propto a$ exactly:
$a\mapsto\lambda a$ sends $T_U\mapsto\lambda T_U$ (the check is $\lambda=2$). Invert for the acceleration that reaches $1\,$K,
$$a=\frac{2\pi c\,k_B}{\hbar}\,T_U=\big(2.47\times10^{20}\,\mathrm{m\,s^{-2}\,K^{-1}}\big)\times(1\,\mathrm K)\approx2.5\times10^{20}\,\mathrm{m/s^2}.$$
The prefactor $2\pi c\,k_B/\hbar\approx2.47\times10^{20}$ is enormous (because $\hbar$ is tiny and $c$ huge), so even $1\,$K
demands an acceleration $\sim10^{19}g$ — hopelessly large. Hence $T_U(10^{20})=10^{20}/2.47\times10^{20}\approx0.405\,$K, while
everyday $g=9.81$ gives $T_U=9.81/2.47\times10^{20}\approx4.0\times10^{-20}\,$K, undetectable. These match
`unruh_temperature(1e20)`$\approx0.4055$ and `unruh_temperature(9.81)`$\approx3.98\times10^{-20}$, with the ratio $2.0$.

### P3.  The accelerated vacuum is thermal  *(BD §4.5)*
For a Rindler mode of frequency ω the Bogoliubov coefficients satisfy
|β_ω|²/|α_ω|² = e^{−2πcω/a}. Combine this with |α_ω|² − |β_ω|² = 1 to show
⟨n_ω⟩ = |β_ω|² = 1/(e^{ℏω/k_BT_U} − 1) — a Planck spectrum. *Check:* for a = 10²⁰,
`unruh_occupation(w, a)` equals `bose_occupation(w, unruh_temperature(a))` to machine
precision (e.g. 0.582 at w = a/2πc), and `unruh_beta_ratio(w, a)` = ⟨n⟩/(⟨n⟩+1).

**Solution.** Write $R\equiv|\beta_\omega|^2/|\alpha_\omega|^2=e^{-2\pi c\omega/a}$. The norm
$|\alpha_\omega|^2-|\beta_\omega|^2=1$ becomes $|\alpha_\omega|^2(1-R)=1$, so
$$\langle n_\omega\rangle=|\beta_\omega|^2=R\,|\alpha_\omega|^2=\frac{R}{1-R}=\frac{1}{e^{2\pi c\omega/a}-1}.$$
The exponent is exactly the Boltzmann factor at $T_U$, since
$\dfrac{\hbar\omega}{k_BT_U}=\hbar\omega\cdot\dfrac{2\pi c\,k_B}{k_B\,\hbar a}=\dfrac{2\pi c\omega}{a}$; thus
$\langle n_\omega\rangle=1/(e^{\hbar\omega/k_BT_U}-1)$, a Planck spectrum. And since $|\alpha|^2=|\beta|^2+1$,
$R=|\beta|^2/|\alpha|^2=\langle n\rangle/(\langle n\rangle+1)$. At $\omega=a/2\pi c$ the exponent is $1$: $\langle n\rangle=1/(e-1)=0.582$
and $R=e^{-1}=0.368=0.582/1.582$. So `unruh_occupation(w, a)` equals `bose_occupation(w, unruh_temperature(a))` and
`unruh_beta_ratio(w, a)`$=\langle n\rangle/(\langle n\rangle+1)$.

### P4.  Hawking temperature from surface gravity  *(BD Ch. 8)*
Using r_s = 2GM/c² and κ = c²/2r_s = c⁴/4GM, show T_H = ℏκ/2πck_B = ℏc³/8πGM k_B,
and evaluate it for the Sun. Why is an astrophysical black hole effectively
*absorbing* (compare T_H to the 2.7 K CMB)? *Check:* `schwarzschild_radius(M_SUN)` ≈
2953 m, `surface_gravity(M_SUN)` ≈ 1.52×10¹³ m/s², and `hawking_temperature(M_SUN)` ≈
6.17×10⁻⁸ K (equal to ℏ·`surface_gravity`/2πck_B).

**Solution.** From $r_s=2GM/c^2$, the surface gravity is
$\kappa=\dfrac{c^2}{2r_s}=\dfrac{c^2}{2}\cdot\dfrac{c^2}{2GM}=\dfrac{c^4}{4GM}$. Hawking's temperature is the Unruh formula
evaluated at the horizon's acceleration $a\to\kappa$:
$$T_H=\frac{\hbar\kappa}{2\pi c\,k_B}=\frac{\hbar}{2\pi c\,k_B}\cdot\frac{c^4}{4GM}=\frac{\hbar c^3}{8\pi G M\,k_B}.$$
For the Sun, $r_s\approx2953\,$m and $\kappa=c^2/2r_s\approx1.52\times10^{13}\,$m/s$^2$, giving $T_H\approx6.17\times10^{-8}\,$K.
This is $\sim8$ orders of magnitude below the $2.7\,$K CMB, so the hole absorbs far more radiation than it emits — effectively
*absorbing*, it grows rather than evaporates. Matches `schwarzschild_radius(M_SUN)`$\approx2953$,
`surface_gravity(M_SUN)`$\approx1.52\times10^{13}$, and `hawking_temperature(M_SUN)`$\approx6.17\times10^{-8}=\hbar\cdot$`surface_gravity`$/2\pi c\,k_B$.

### P5.  A one-kilogram black hole  *(BD Ch. 8)*
Since T_H ∝ 1/M, small holes are hot. Compute T_H for M = 1 kg and its horizon radius
r_s, and comment on why such an object would radiate explosively. *Check:*
`hawking_temperature(1.0)` ≈ 1.23×10²³ K and `schwarzschild_radius(1.0)` ≈
1.5×10⁻²⁷ m (sub-nuclear).

**Solution.** Since $T_H=\hbar c^3/8\pi GM\,k_B\propto1/M$, scale off the solar value:
$$T_H(1\,\mathrm{kg})=T_H(M_\odot)\,\frac{M_\odot}{1\,\mathrm{kg}}=6.17\times10^{-8}\times1.989\times10^{30}\approx1.23\times10^{23}\,\mathrm K.$$
Its horizon is $r_s=2G/c^2\approx1.49\times10^{-27}\,$m — about twelve orders below a proton radius. At $k_BT_H$ of order
$10^{23}\,$K the thermal quanta exceed every Standard-Model rest mass, so the hole pours out radiation; and because
$\dot M\propto-1/M^2$, shedding mass only raises $T_H$ — a runaway ending in an explosive final burst. Matches
`hawking_temperature(1.0)`$\approx1.23\times10^{23}$ K and `schwarzschild_radius(1.0)`$\approx1.5\times10^{-27}$ m (sub-nuclear).

### P6.  Evaporation lifetime ∝ M³  *(BD Ch. 8)*
Equate the Stefan–Boltzmann luminosity L = σA T_H⁴ (with A = 4πr_s²) to −c² dM/dt and
integrate to get τ = 5120πG²M³/ℏc⁴. Show τ ∝ M³ and evaluate it for M_⊙. Which
primordial mass would be evaporating *now* (τ ~ the age of the universe)? *Check:*
`evaporation_lifetime(M_SUN)` ≈ 6.6×10⁷⁴ s ≈ 2.1×10⁶⁷ yr, and
`evaporation_lifetime(2*M_SUN)/evaporation_lifetime(M_SUN)` = 8.0.

**Solution.** Both factors scale with mass: $A=4\pi r_s^2=4\pi(2GM/c^2)^2\propto M^2$ and $T_H^4\propto M^{-4}$, so
$L=\sigma A T_H^4\propto M^{-2}$. With every constant collected, the balance $L=-c^2\dot M$ reads
$$\frac{dM}{dt}=-\frac{\hbar c^4}{15360\,\pi G^2}\frac{1}{M^2}\quad\Longrightarrow\quad M^2\,dM=-\frac{\hbar c^4}{15360\,\pi G^2}\,dt.$$
Integrating from $M$ down to $0$ with $\int_0^M M'^2\,dM'=M^3/3$,
$$\tau=\frac{15360\,\pi G^2}{\hbar c^4}\cdot\frac{M^3}{3}=\frac{5120\,\pi G^2 M^3}{\hbar c^4}\ \propto\ M^3,$$
so $\tau(2M)=8\,\tau(M)$. For $M_\odot$, $\tau\approx6.6\times10^{74}\,$s$\,\approx2.1\times10^{67}\,$yr, dwarfing the
$\sim1.4\times10^{10}\,$yr age of the universe; setting $\tau$ equal to that age inverts to $M\sim10^{11}\,$kg — the
primordial holes expiring now. Matches `evaporation_lifetime(M_SUN)`$\approx6.6\times10^{74}$ s and the ratio $8.0$.

### P7.  Bosons versus fermions in the thermal spectrum  *(BD Ch. 4)*
The horizon spectrum builder is |β_ω|² = 1/(e^{ℏω/k_BT} ∓ 1) — minus for bosons, plus
for fermions. Argue that at fixed (ω, T) a thermal *fermion* mode is always less
occupied than a *boson* mode, and that fermion occupation never exceeds ½. *Check:*
`thermal_beta_squared(w, T, 'bose')` equals `bose_occupation(w, T)` and exceeds
`thermal_beta_squared(w, T, 'fermi')` for every w; `fermi_occupation` is bounded in
(0, ½].

**Solution.** Let $x=\hbar\omega/k_BT>0$ for any real mode at $T>0$. The two builders are $n_B=1/(e^x-1)$ and
$n_F=1/(e^x+1)$. Because $e^x-1<e^x+1$, the bosonic denominator is the smaller one, so
$$n_B=\frac{1}{e^x-1}>\frac{1}{e^x+1}=n_F\qquad\text{for every }\omega,$$
bosons pile up while Pauli exclusion throttles fermions. Moreover $e^x+1>2$ for all $x>0$, hence
$$n_F=\frac{1}{e^x+1}<\tfrac12,$$
rising toward $\tfrac12$ as $x\to0^+$ and falling to $0$ as $x\to\infty$, i.e. $n_F\in(0,\tfrac12]$. For instance at
$x\approx0.076$, $n_B=12.6\gg n_F=0.481<\tfrac12$, and $n_F(x\to0)=\tfrac12$. So `thermal_beta_squared(w, T, 'bose')`
$=$ `bose_occupation(w, T)` exceeds `thermal_beta_squared(w, T, 'fermi')` for every $w$, with `fermi_occupation`
bounded in $(0,\tfrac12]$.
