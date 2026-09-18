# QM-01 — Problems

Work them by hand, then check with `code/origins.py`. Sources in `../refs.md`.

### P1.  The UV catastrophe, made quantitative
Show that Rayleigh–Jeans is the $h\nu\ll k_BT$ limit of Planck, and that, unlike
Planck, it has no finite total energy. *(At fixed T, RJ grows without bound while
Planck turns over.)*
*Check:* `rayleigh_jeans_u_nu(1e9, 300)` ≈ `planck_u_nu(1e9, 300)` (classical
regime); at high ν, `planck_u_nu(1e16, 5000) < planck_u_nu(1e15, 5000)` but the
RJ values keep rising. (`test_planck_reduces_to_rayleigh_jeans`,
`test_rayleigh_jeans_diverges_but_planck_does_not`.)

**Solution.** Write Planck with $x=h\nu/k_BT$: $u=\dfrac{8\pi h\nu^3}{c^3}\,\dfrac{1}{e^{x}-1}$.
For $x\ll1$, $e^{x}-1\to x=\dfrac{h\nu}{k_BT}$, so
$$u\to\frac{8\pi h\nu^3}{c^3}\cdot\frac{k_BT}{h\nu}=\frac{8\pi\nu^2}{c^3}\,k_BT,$$
the Rayleigh–Jeans law. At $\nu=10^9,\,T=300$ K, $x\approx1.6\times10^{-4}\ll1$, so the two
agree ($3.8635\times10^{-27}$ vs $3.8632\times10^{-27}$). But RJ $\propto\nu^2$ gives
$\int_0^\infty\nu^2\,d\nu=\infty$ — the UV catastrophe — whereas Planck's $e^{h\nu/k_BT}$
denominator forces an exponential turn-over: $u(10^{16},5000)\approx1.3\times10^{-51}\ll
u(10^{15},5000)\approx4.2\times10^{-17}$, exactly the two `*Check:*` comparisons.

### P2.  Recover σ and b from Planck
Without quoting them, obtain the Stefan–Boltzmann constant and the Wien
displacement constant from Planck's law. *(σ by integrating $x^3/(e^x-1)=\pi^4/15$;
b by solving $x=5(1-e^{-x})$, x≈4.965.)*
*Answer:* σ = 5.6704×10⁻⁸ W m⁻² K⁻⁴, b = 2.898×10⁻³ m K.
*Check:* `stefan_boltzmann_sigma()`, `wien_displacement_b()`.

**Solution.** *σ:* integrate Planck over $\nu$ with $x=h\nu/k_BT$ (so $d\nu=\frac{k_BT}{h}dx$):
$$\int_0^\infty u\,d\nu=\frac{8\pi h}{c^3}\Big(\frac{k_BT}{h}\Big)^4\!\int_0^\infty\frac{x^3}{e^x-1}\,dx
=\frac{8\pi^5k_B^4}{15\,h^3c^3}\,T^4\equiv aT^4,$$
using $\int_0^\infty\frac{x^3}{e^x-1}dx=\Gamma(4)\zeta(4)=\frac{\pi^4}{15}$. With $a=4\sigma/c$,
$\sigma=\frac{2\pi^5k_B^4}{15h^3c^2}=5.6704\times10^{-8}$. *b:* maximizing
$B_\lambda\propto\lambda^{-5}/(e^{hc/\lambda k_BT}-1)$ over $\lambda$ gives, with $x=hc/\lambda k_BT$,
the transcendental $x=5(1-e^{-x})$ (root $x\approx4.965$), so $\lambda_{\max}T=\frac{hc}{k_Bx}=b
=2.898\times10^{-3}$ m K. The code returns $\sigma=5.6704\times10^{-8}$ and $b=2.8978\times10^{-3}$.

### P3.  Why the Sun is (nearly) green
The Sun's surface is ≈5772 K. Where does its spectrum peak?
*Answer:* λ_max = b/T ≈ 502 nm (green; the eye's peak sensitivity sits here — not
a coincidence).
*Check:* `wien_displacement_b()/5772 * 1e9`.

**Solution.** Wien's displacement law puts the spectral peak at $\lambda_{\max}=b/T$. With
$b=2.898\times10^{-3}$ m K and $T=5772$ K,
$$\lambda_{\max}=\frac{2.898\times10^{-3}}{5772}=5.02\times10^{-7}\,\mathrm{m}=502\ \mathrm{nm},$$
which lies in the green, coinciding with the eye's peak photopic sensitivity (not an accident —
the eye evolved under sunlight). `wien_displacement_b()/5772*1e9` returns $502.0$ nm.

### P4.  Photoelectric threshold and Millikan's slope
Sodium has W = 2.28 eV. (a) What is the longest wavelength that ejects electrons?
(b) Show the stopping voltage vs frequency is a line of slope h/e.
*Answer:* (a) λ₀ = c/f₀ ≈ 544 nm. (b) slope = h/e.
*Check:* `threshold_frequency(2.28*e)` → f₀; `c/f0*1e9` ≈ 544;
`test_photoelectric_threshold_and_linearity` verifies `dK_max/df = h`.

**Solution.** (a) The threshold is where $K_{\max}=h\nu-W=0$, i.e. $f_0=W/h$. With
$W=2.28\,\mathrm{eV}=3.65\times10^{-19}$ J,
$$f_0=\frac{3.65\times10^{-19}}{6.626\times10^{-34}}=5.51\times10^{14}\,\mathrm{Hz},\qquad
\lambda_0=\frac{c}{f_0}=544\ \mathrm{nm}.$$
(b) The stopping voltage satisfies $eV_s=K_{\max}=h\nu-W$, so $V_s=\frac{h}{e}\nu-\frac{W}{e}$ —
a straight line of slope $h/e$ (equivalently $dK_{\max}/d\nu=h$, how Millikan measured $h$).
`threshold_frequency(2.28*e)` gives $5.513\times10^{14}$ Hz and $c/f_0\cdot10^9=543.8$ nm.

### P5.  Hydrogen spectral lines
From the Bohr levels, find the Balmer Hα (3→2) and Lyman-α (2→1) wavelengths and
say which part of the spectrum each lands in.
*Answer:* Hα = 656 nm (visible red), Lyman-α = 122 nm (UV).
*Check:* `rydberg_wavelength(2,3)*1e9` ≈ 656.1; `rydberg_wavelength(1,2)*1e9` ≈ 121.6.

**Solution.** The Rydberg formula reads $\frac1\lambda=R\big(\frac1{n_1^2}-\frac1{n_2^2}\big)$ with
$R=1.097\times10^7\,\mathrm{m^{-1}}$. Balmer Hα ($n_2{=}3\to n_1{=}2$):
$$\frac1\lambda=R\Big(\frac14-\frac19\Big)=\frac{5R}{36}\ \Rightarrow\ \lambda=\frac{36}{5R}=656\ \mathrm{nm}
\ \text{(visible red)}.$$
Lyman-α ($2\to1$): $\frac1\lambda=R\big(1-\frac14\big)=\frac{3R}{4}\Rightarrow\lambda=\frac{4}{3R}=121.5\ \mathrm{nm}$
(UV). The code returns `rydberg_wavelength(2,3)*1e9` ≈ $656.1$ and `rydberg_wavelength(1,2)*1e9` ≈ $121.5$.

### P6.  de Broglie — why electron microscopes beat light microscopes  *(Griffiths 3e, Prob. 1.18, p.40)*
A 100 eV electron: what is its de Broglie wavelength, and how does it compare to
visible light (~500 nm)?
*Answer:* λ = h/√(2mE) ≈ 0.123 nm — ~4000× shorter than visible light, so the
diffraction-limited resolution is ~4000× finer.
*Check:* `de_broglie_from_energy(100*e)*1e9` ≈ 0.1226.

**Solution.** Non-relativistically $p=\sqrt{2m_eE}$, so $\lambda=\dfrac{h}{p}=\dfrac{h}{\sqrt{2m_eE}}$.
With $E=100\,\mathrm{eV}=1.602\times10^{-17}$ J,
$$p=\sqrt{2(9.109\times10^{-31})(1.602\times10^{-17})}=5.40\times10^{-24}\ \mathrm{kg\,m/s},\quad
\lambda=\frac{6.626\times10^{-34}}{5.40\times10^{-24}}=0.123\ \mathrm{nm}.$$
This is $\sim\!500/0.123\approx4000\times$ shorter than visible light, so the diffraction-limited
resolution ($\sim\lambda$) is $\sim\!4000\times$ finer — why electron microscopes resolve atoms.
`de_broglie_from_energy(100*e)*1e9` ≈ $0.1226$.

### P7.  Compton — the photon's momentum
Find the maximum wavelength shift when X-rays Compton-scatter off electrons, and
the angle at which it occurs.
*Answer:* Δλ_max = 2λ_C ≈ 4.85 pm, at θ = 180° (back-scatter).
*Check:* `compton_shift(math.pi)*1e12` ≈ 4.853; `compton_shift(0)` = 0.

**Solution.** The Compton shift is $\Delta\lambda=\lambda_C(1-\cos\theta)$ with
$\lambda_C=h/m_ec=2.426$ pm. The factor $(1-\cos\theta)$ is largest at $\cos\theta=-1$, i.e.
$\theta=180^\circ$ (back-scatter):
$$\Delta\lambda_{\max}=\lambda_C\big(1-(-1)\big)=2\lambda_C=4.85\ \mathrm{pm},$$
and it vanishes in the forward direction $\theta=0$ (since $1-\cos0=0$). The X-ray loses momentum
to the recoiling electron, lengthening its wavelength. `compton_shift(math.pi)*1e12` ≈ $4.853$
and `compton_shift(0)` $=0$.
