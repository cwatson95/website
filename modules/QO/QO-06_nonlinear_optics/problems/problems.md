# QO-06 — Problems

Work by hand, then check with `code/nonlinear_optics.py`. Citations in
`../refs.md`; **Boyd** = Boyd, *Nonlinear Optics* 4e (chapter-level); **SZ** =
Scully & Zubairy.

### P1.  Orders of magnitude of χ⁽ⁿ⁾  *(Boyd Ch. 1)*
From P = ε₀(χ⁽¹⁾E + χ⁽²⁾E² + χ⁽³⁾E³ + …), argue that the ratio of successive
terms is ~E/E_at with the atomic field E_at ≈ 5×10¹¹ V/m, hence χ⁽²⁾ ~ pm/V and
χ⁽³⁾ ~ 10⁻²² m²/V². Why does χ⁽²⁾ vanish in a centrosymmetric medium? *Check:*
`chi_polarization(E, chi1)` reduces to the linear ε₀χ⁽¹⁾E; the χ⁽²⁾-only term
scales as E² (doubling E multiplies it by **4**).

**Solution.** Compare adjacent terms of $P=\varepsilon_0(\chi^{(1)}E+\chi^{(2)}E^2+\chi^{(3)}E^3+\cdots)$:
$$\frac{\chi^{(n+1)}E^{n+1}}{\chi^{(n)}E^{n}}=\frac{\chi^{(n+1)}}{\chi^{(n)}}\,E\sim\frac{E}{E_{\rm at}},$$
since this expansion of the bound-electron response only breaks down when $E$ nears the atomic field $E_{\rm at}\sim10^{11}$–$10^{12}$ V/m that binds the electron. Thus $\chi^{(n+1)}/\chi^{(n)}\sim1/E_{\rm at}$, and with $\chi^{(1)}\sim1$: $\chi^{(2)}\sim1/E_{\rm at}\sim$ pm/V, $\chi^{(3)}\sim1/E_{\rm at}^2\sim10^{-22}\ \text{m}^2/\text{V}^2$. In a centrosymmetric medium, inversion sends $E\to-E$ and $P\to-P$; but the $\chi^{(2)}$ term gives $\chi^{(2)}(-E)^2=+\chi^{(2)}E^2$, which can equal the required $-\chi^{(2)}E^2$ only if $\chi^{(2)}=0$ (every even order dies; odd $\chi^{(3)}$ survives). So `chi_polarization(E, chi1)` is the pure linear $\varepsilon_0\chi^{(1)}E$, while the $\chi^{(2)}$-only term $\varepsilon_0\chi^{(2)}E^2$ quadruples ($\times4$) when $E$ doubles.

### P2.  SHG phase matching and the first null  *(Boyd Ch. 2)*
Integrate the undepleted-pump coupled-wave equation to get
η ∝ L² sinc²(ΔkL/2), with Δk = k(2ω) − 2k(ω). Show the efficiency peaks at
Δk = 0 and that its **first null is at ΔkL = 2π**. *Check:*
`shg_efficiency(0.0, L)` = **1.0** (normalized peak); `shg_efficiency(2π/L, L)`
≈ **0** while `shg_efficiency(π/L, L)` > 0.

**Solution.** In the undepleted-pump, slowly-varying-envelope limit the harmonic amplitude obeys $dA_2/dz=i\kappa A_1^2e^{-i\Delta k\,z}$ with $A_1$ fixed. Integrating over the crystal,
$$A_2(L)=i\kappa A_1^2\int_0^Le^{-i\Delta k\,z}dz=i\kappa A_1^2\,L\,e^{-i\Delta kL/2}\,\operatorname{sinc}\!\Big(\frac{\Delta kL}{2}\Big),\qquad\operatorname{sinc}x=\frac{\sin x}{x}.$$
The efficiency is $\eta\propto|A_2(L)|^2\propto L^2\operatorname{sinc}^2(\Delta kL/2)$. It is largest at $\Delta k=0$, where $\operatorname{sinc}0=1$ and every slice adds in phase ($\eta\propto L^2$); its first zero is where the argument first hits $\pi$, i.e. $\Delta kL/2=\pi\Rightarrow\Delta kL=2\pi$. Hence `shg_efficiency(0.0, L)`$=1.0$ (normalized peak), `shg_efficiency(2π/L, L)`$\approx0$, while at the half-way point `shg_efficiency(π/L, L)`$=\operatorname{sinc}^2(\pi/2)=(2/\pi)^2\approx0.405>0$.

### P3.  Coherence length from dispersion  *(Boyd Ch. 2; ~EM-15)*
Using k = nω/c, show Δk = (4π/λ)(n(2ω) − n(ω)) and L_c = π/|Δk|. For a 0.030
index split at λ = 1.064 µm, find L_c and explain why L_c is the half-period of
back-and-forth conversion. *Check:* `shg_phase_mismatch(1.50, 1.53, 1.064e-6)`
≈ **3.54×10⁵ m⁻¹**, and `coherence_length` of that ≈ **8.9 µm**; the sinc² curve
nulls at L = 2L_c.

**Solution.** With $k=n\omega/c$ and the harmonic at $2\omega$,
$$\Delta k=k(2\omega)-2k(\omega)=\frac{2\omega}{c}\big(n(2\omega)-n(\omega)\big)=\frac{4\pi}{\lambda}\big(n(2\omega)-n(\omega)\big),$$
using $\omega=2\pi c/\lambda$ so that $2\omega/c=4\pi/\lambda$. The coherence length is the run over which the relative phase $\Delta k\,z$ accumulates $\pi$, $L_c=\pi/|\Delta k|$. For an index split $\Delta n=0.030$ at $\lambda=1.064\,\mu$m, $\Delta k=4\pi(0.030)/(1.064\,\mu\text{m})\approx3.54\times10^5\ \text{m}^{-1}$ and $L_c=\pi/\Delta k\approx8.9\,\mu$m. Beyond $L_c$ the harmonic is $\pi$ out of phase and power flows *back* to the fundamental, so conversion oscillates with spatial period $2L_c$ and $L_c$ is its half-period — exactly the $L=2L_c$ null of the §2 $\operatorname{sinc}^2$ curve. This is `shg_phase_mismatch(1.50, 1.53, 1.064e-6)`$\approx3.54\times10^5\ \text{m}^{-1}$ with `coherence_length`$\approx8.9\,\mu$m.

### P4.  Manley–Rowe and the parametric step  *(Boyd Ch. 2; ~QO-05)*
For ω₃ = ω₁ + ω₂ show d(I₁/ω₁) = d(I₂/ω₂) = −d(I₃/ω₃), i.e. one pump photon
makes one signal + one idler photon, and deduce ΔI₁ + ΔI₂ + ΔI₃ = 0. Identify
the idler wavelength when a 532 nm pump seeds an 800 nm signal. *Check:*
`manley_rowe_check(...)` returns equal `dPhi_signal` = `dPhi_idler` = −`dPhi_pump`
(= **10²⁴**), `energy_residual` ≈ **0**, and an idler at λ ≈ **1588 nm**.

**Solution.** The photon flux in beam $i$ is $\Phi_i=I_i/\hbar\omega_i$. A lossless $\chi^{(2)}$ step destroys one pump photon ($\omega_3$) to make one signal ($\omega_1$) and one idler ($\omega_2$), so $d\Phi_1=d\Phi_2=-d\Phi_3$, i.e.
$$\frac{d}{dz}\frac{I_1}{\omega_1}=\frac{d}{dz}\frac{I_2}{\omega_2}=-\frac{d}{dz}\frac{I_3}{\omega_3}.$$
Writing $\Delta I_i=\hbar\omega_i\,\Delta\Phi_i$ with $\Delta\Phi_1=\Delta\Phi_2=-\Delta\Phi_3\equiv\Delta\Phi$, energy balance follows: $\Delta I_1+\Delta I_2+\Delta I_3=\hbar(\omega_1+\omega_2-\omega_3)\Delta\Phi=0$ because $\omega_3=\omega_1+\omega_2$. For $\lambda_p=532$ nm and $\lambda_s=800$ nm the idler obeys $1/\lambda_i=1/\lambda_p-1/\lambda_s=(800-532)/(532\cdot800\ \text{nm})$, giving $\lambda_i\approx1588$ nm. Hence `manley_rowe_check(...)` returns `dPhi_signal`$=$`dPhi_idler`$=-$`dPhi_pump`$=10^{24}$, `energy_residual`$\approx0$, and an idler at $\approx1588$ nm.

### P5.  Self-phase modulation / the B-integral  *(Boyd Ch. 4/7)*
From n = n₀ + n₂I derive the nonlinear phase φ_NL = (2π/λ)n₂IL acquired by a
beam modulating itself. Evaluate it for fused silica (n₂ = 2.6×10⁻²⁰ m²/W) at
I = 10¹⁵ W/m² over L = 1 cm at λ = 1.064 µm, and say why a B-integral of order 1
threatens a laser chain. *Check:* `kerr_phase(2.6e-20, 1e15, 1e-2, 1.064e-6)`
≈ **1.54 rad**, linear in both I and L.

**Solution.** A wave traversing length $L$ accumulates phase $\phi=(2\pi/\lambda)nL$; with the Kerr index $n=n_0+n_2I$ the intensity-dependent part is the self-phase modulation
$$\phi_{\rm NL}=\frac{2\pi}{\lambda}\,n_2 I\,L,$$
the beam phase-modulating itself. For fused silica $n_2=2.6\times10^{-20}\ \text{m}^2/\text{W}$ at $I=10^{15}\ \text{W/m}^2$ over $L=10^{-2}$ m at $\lambda=1.064\,\mu$m,
$$\phi_{\rm NL}=\frac{2\pi}{1.064\times10^{-6}}(2.6\times10^{-20})(10^{15})(10^{-2})\approx1.54\ \text{rad}.$$
The accumulated $B=\int(2\pi/\lambda)n_2I\,dz$ is the "B-integral"; once $B\gtrsim1$ the brightest filaments pick up $\sim1$ rad of extra phase, the wavefront self-focuses, and the beam breaks up — damaging a high-power chain (`~PK-04`), so designers hold $B$ below order unity. Linear in both $I$ and $L$, this is `kerr_phase(2.6e-20, 1e15, 1e-2, 1.064e-6)`$\approx1.54$ rad.

### P6.  SBS gain spectrum and the Brillouin shift  *(Boyd Ch. 9; → SBS_Project)*
A pump scattering off a backward acoustic wave is downshifted by
ν_B = 2 n v_a/λ_p. Sketch the Stokes gain as a Lorentzian of FWHM Γ_B centered at
Ω_B, and find where the gain falls to half its peak. *Check:*
`brillouin_shift(1.33, 1480, 532e-9)` ≈ **7.4 GHz** (water); `brillouin_gain`
gives **g₀** at line center and **g₀/2** at Ω_B ± Γ_B/2 — the lineshape
`SBS_Project` fits to data.

**Solution.** Backscattered Stokes light beats with the pump to drive a sound wave; phase matching for a reflected wave ($\mathbf k_S\approx-\mathbf k_p$) needs phonon wavevector $q\approx2k_p=4\pi n/\lambda_p$, and for a linear sound branch $\Omega_B=v_a q$, so
$$\nu_B=\frac{\Omega_B}{2\pi}=\frac{v_a\,q}{2\pi}=\frac{2 n v_a}{\lambda_p}.$$
The Stokes gain is the Lorentzian $g(\Omega)=g_0(\Gamma_B/2)^2/[(\Omega-\Omega_B)^2+(\Gamma_B/2)^2]$, peaking at $g_0$ when $\Omega=\Omega_B$ and falling to $g_0/2$ where $(\Omega-\Omega_B)^2=(\Gamma_B/2)^2$, i.e. at $\Omega_B\pm\Gamma_B/2$ — the two half-maximum points a full $\Gamma_B$ apart. For water, $\nu_B=2(1.33)(1480)/(532\times10^{-9})\approx7.4$ GHz. So `brillouin_shift(1.33, 1480, 532e-9)`$\approx7.4$ GHz, and `brillouin_gain` returns $g_0$ at line center and $g_0/2$ at $\Omega_B\pm\Gamma_B/2$ — the lineshape `SBS_Project` fits.

### P7.  Brillouin vs. Raman  *(Boyd Ch. 9–10)*
Both stimulated-scattering gains are Lorentzians of the same form; contrast the
two by phonon type (acoustic vs. optical/vibrational) and therefore by the
**size** of the shift. Why is the Raman shift orders of magnitude larger than the
Brillouin shift? *Check:* `raman_gain(Ω_R, Ω_R, γ_R)` peaks at **g₀** just like
SBS, but at a Raman shift Ω_R (~10¹⁴ rad/s, THz) ≫ the Brillouin shift (~GHz).

**Solution.** Both gains are the identical Lorentzian $g(\Omega)=g_0(\Gamma/2)^2/[(\Omega-\Omega_0)^2+(\Gamma/2)^2]$; they differ only in which excitation the optical beat drives. Brillouin scatters off an **acoustic** phonon, $\Omega=v_a q$, gapless and linear in $q$; at the backscatter wavevector $q\approx2k$ this is
$$\Omega_B=v_a\cdot\frac{4\pi n}{\lambda}\sim\frac{v_a}{c}\,\omega\sim10^{-5}\,\omega\sim\text{GHz},$$
because $v_a/c\sim10^{-5}$. Raman scatters off an **optical/vibrational** phonon whose frequency is set by intramolecular bond stiffness, nearly $q$-independent, with $\hbar\Omega_R\sim0.1$ eV $\Rightarrow\Omega_R\sim10^{14}\ \text{rad/s}$ (tens of THz). The ratio $\Omega_R/\Omega_B\sim10^4$–$10^5$ is large precisely because acoustic-branch frequencies vanish as $q\to0$ while optical-branch frequencies sit at a finite bond-stiffness gap. So `raman_gain(Ω_R, Ω_R, γ_R)` peaks at $g_0$ exactly like SBS, but at $\Omega_R\sim10^{14}$ rad/s $\gg$ the GHz Brillouin shift.
