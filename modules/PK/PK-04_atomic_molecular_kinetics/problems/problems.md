# PK-04 — Problems

Work by hand, then check with `code/molecular_kinetics.py`. Citations in `../refs.md`;
**Rh** = Rhodes (ed.) *Excimer Lasers*, **Mi** = Michel. Cited at chapter/section level;
the Maxwellian ⟨σv⟩ derivation is `~SM-06`.

### P1.  Coupled rate equations and timescales  *(Mi, atomic-processes ch.)*
Write the rate equations for the 0-D cartoon (pump → Kr\*, harpoon Kr\* + F₂ → KrF\* + F,
radiative KrF\* → Kr + F + hν, F₂ quench). Identify the limiting reagent, and argue that
KrF\* is **quasi-steady**, n(KrF\*) ≈ R₂/(A + k_q n(F₂)), so it tracks the formation rate
and rises to a peak then decays once the pump (and Kr\*) drain away. *Check:* `simulate_krf()`
gives `peak_KrFs` ≈ 1.45×10²² m⁻³ at `peak_time` ≈ 54 ns, with KrF\* at the final time
< 10 % of the peak; `excimer_rhs` is literally production − loss.

**Solution.** With $r_1=k_{\rm pump}\,g(t)\,n_{\rm Kr}$ (pump), $r_2=k_h\,n_{\rm Kr^*}n_{\rm F_2}$
(harpoon), $r_3=A\,n_{\rm KrF^*}$ (radiative) and $r_4=k_q\,n_{\rm KrF^*}n_{\rm F_2}$
(quench), the ledger $\dot n_i=$ production $-$ loss is
$$\dot n_{\rm Kr^*}=r_1-r_2,\quad \dot n_{\rm KrF^*}=r_2-(r_3+r_4),\quad \dot n_{\rm F_2}=-r_2,\quad \dot n_{\rm F}=r_2+r_3+r_4 .$$
$\mathrm{F_2}$ is the limiting reagent: it starts at $2\times10^{23}\ \mathrm{m^{-3}}$ (vs $10^{24}$ for
Kr), is consumed by harpooning and never refilled. KrF\* has a fast total loss rate
$A+k_q n_{\rm F_2}\sim10^{8}\ \mathrm{s^{-1}}$ (an effective lifetime of tens of ns), much
faster than the pump envelope, so it sits in quasi-steady state:
$$\dot n_{\rm KrF^*}\approx0\ \Rightarrow\ n_{\rm KrF^*}\approx\frac{r_2}{A+k_q n_{\rm F_2}},$$
tracking the instantaneous formation rate $r_2\propto g(t)\,n_{\rm Kr^*}$. While the Gaussian
pump fills Kr\*, $r_2$ climbs; once the pump passes and Kr\* drains, $r_2$ collapses and
KrF\* follows it down. So KrF\* rises to a peak then decays — `simulate_krf()` gives
`peak_KrFs` $\approx1.45\times10^{22}\ \mathrm{m^{-3}}$ at `peak_time` $\approx54$ ns, with the
final KrF\* far below 10 % of the peak, and `excimer_rhs` is literally production minus loss.

### P2.  The Maxwellian rate coefficient  *(Mi; `~SM-06`)*
From the 3-D Maxwellian and ε = ½mv², derive
k = ⟨σv⟩ = √(8/πm) (kT)^{−3/2} ∫₀^∞ σ(ε) ε e^{−ε/kT} dε. For a step cross-section
σ = σ₀ for ε ≥ E_th, integrate to get k = σ₀⟨v⟩(1 + E_th/kT) e^{−E_th/kT}. *Check:*
`rate_coefficient_maxwellian(T, 3e-20, 12.0)` equals `rate_coefficient_step_closed_form(...)`
to < 10⁻⁵ relative, and the coefficient increases with T (`test_rate_coefficient_matches_closed_form`).

**Solution.** Average the flux $\sigma v$ over the Maxwellian
$f(\mathbf v)=(m/2\pi kT)^{3/2}e^{-mv^2/2kT}$; for an isotropic cross-section
$d^3v=4\pi v^2\,dv$, so
$$k=\langle\sigma v\rangle=\int\sigma v\,f\,d^3v=4\pi\Big(\frac{m}{2\pi kT}\Big)^{3/2}\!\int_0^\infty\sigma(v)\,v^3 e^{-mv^2/2kT}\,dv .$$
Substituting $\varepsilon=\tfrac12 mv^2$ (so $v^3\,dv=2\varepsilon\,d\varepsilon/m^2$) collapses
the prefactor to $\sqrt{8/\pi m}\,(kT)^{-3/2}$:
$$k=\sqrt{\frac{8}{\pi m}}\,(kT)^{-3/2}\!\int_0^\infty\sigma(\varepsilon)\,\varepsilon\,e^{-\varepsilon/kT}\,d\varepsilon .$$
For the step $\sigma=\sigma_0$ above $E_{\rm th}$ the integral runs from $E_{\rm th}$, and
$\int_{E_{\rm th}}^\infty\varepsilon\,e^{-\varepsilon/kT}\,d\varepsilon=(kT)^2(1+E_{\rm th}/kT)e^{-E_{\rm th}/kT}$,
so with $\langle v\rangle=\sqrt{8kT/\pi m}$
$$k(T)=\sigma_0\,\langle v\rangle\Big(1+\frac{E_{\rm th}}{kT}\Big)e^{-E_{\rm th}/kT}.$$
This closed form reproduces the numeric energy integral: `rate_coefficient_maxwellian(T, 3e-20, 12.0)`
equals `rate_coefficient_step_closed_form(...)` to $\sim10^{-8}$ (well under $10^{-5}$)
relative, both rising with $T$.

### P3.  Threshold becomes activation energy  *(Mi; `~SM-06`)*
Show that the apparent Arrhenius activation energy E_a = −d(ln k)/d(1/kT) of the step-σ
result is ≈ E_th − ½kT, i.e. just below the threshold, so k(T) is Arrhenius-like
k ∝ e^{−E_th/kT}. *Check:* for E_th = 15 eV, the slope of ln k between 12 000 and 14 000 K
gives an apparent E_a of 0.85–1.0 × E_th (`test_rate_coefficient_apparent_activation_energy`);
`arrhenius(T, A, Ea)` recovers its input Ea exactly from any two temperatures.

**Solution.** Take the log of the closed form and differentiate with respect to
$\beta\equiv1/kT$. Since $k=\sigma_0\sqrt{8/\pi m}\,(kT)^{1/2}(1+E_{\rm th}/kT)e^{-E_{\rm th}/kT}$,
$$\ln k=\text{const}-\tfrac12\ln\beta+\ln(1+E_{\rm th}\beta)-E_{\rm th}\beta .$$
The apparent activation energy is
$$E_a=-\frac{d\ln k}{d(1/kT)}=-\frac{d\ln k}{d\beta}=\frac{kT}{2}-\frac{E_{\rm th}}{1+E_{\rm th}/kT}+E_{\rm th}.$$
For $E_{\rm th}\gg kT$ the middle term $\to kT$, leaving
$$E_a\approx E_{\rm th}-\tfrac12 kT,$$
just below threshold — so $k\propto e^{-E_{\rm th}/kT}$ is Arrhenius with $E_a\simeq E_{\rm th}$.
Numerically, for $E_{\rm th}=15$ eV the slope of $\ln k$ between 12 000 and 14 000 K gives
$E_a\approx14.5$ eV $=0.97\,E_{\rm th}$ (inside the 0.85–1.0 band), while `arrhenius(T, A, Ea)`
returns its input $E_a$ exactly because $\ln\!\big(Ae^{-E_a/kT}\big)$ is exactly linear in $1/kT$.

### P4.  Saha equation from detailed balance  *(Mi, ionization ch.)*
Balance ionization A → A⁺ + e against recombination A⁺ + e → A to derive the Saha relation
n_e n_i/n₀ = (2g_i/g₀)(2πm_e kT/h²)^{3/2} e^{−E_ion/kT}. With n_e = n_i and n₀ = n_tot − n_i,
solve the quadratic for the ionization fraction x = n_i/n_tot. *Check:* `saha_ionization_fraction(T, 1e24, 14.0)`
rises from ≈ 0.02 (10⁴ K) to ≈ 0.99 (3×10⁴ K), → 1 when hot and → 0 when cold
(`test_saha_fraction_bounded_and_monotonic`); the factor 2 is the electron spin.

**Solution.** Detailed balance equates the ionization rate $A\to A^++e$ with the
recombination rate $A^++e\to A$; in equilibrium the populations obey the Saha relation
$$\frac{n_e n_i}{n_0}=\frac{2g_i}{g_0}\Big(\frac{2\pi m_e kT}{h^2}\Big)^{3/2}e^{-E_{\rm ion}/kT}\equiv S ,$$
where $(2\pi m_e kT/h^2)^{3/2}$ is the electron quantum concentration (inverse
thermal-de-Broglie volume) and the factor $2$ counts the two electron spin states. Put
$n_e=n_i$, $n_0=n_{\rm tot}-n_i$, and let $x=n_i/n_{\rm tot}$, $R=S/n_{\rm tot}$:
$$\frac{x^2}{1-x}=R\ \Longrightarrow\ x^2+Rx-R=0\ \Longrightarrow\ x=\frac{-R+\sqrt{R^2+4R}}{2}.$$
As $T\to0$, $S\to0$ so $x\to0$ (neutral); as $T\to\infty$, $S\to\infty$ so $x\to1$ (fully
ionized), rising monotonically between. Hence `saha_ionization_fraction(T, 1e24, 14.0)`
climbs from $\approx0.02$ at $10^4$ K to $\approx0.99$ at $3\times10^4$ K.

### P5.  The KrF\* excimer and bound–free emission  *(Rh, rare-gas-halide kinetics ch.)*
Sketch the KrF potential curves: a bound ionic B/C upper state and a **repulsive**
(Kr + F) lower state. Explain why this guarantees a population inversion without any
pumping cleverness, and compute the band-centre photon energy. *Check:* `photon_energy_eV(248)`
≈ 4.999 eV (the code's E_{hν}); `simulate_krf()` accumulates a monotonically increasing
`photons` count (`test_excimer_photons_and_reservoir`). The gain/emission machinery is `~QO-03`.

**Solution.** The upper $B/C$ state is ionic, $\mathrm{Kr^+F^-}$, Coulomb-bound with a well a
few eV deep; the lower state correlates to ground-state $\mathrm{Kr}+\mathrm{F}$ and is
**repulsive** (no chemical bond). A vertical $B\to X$ photon therefore lands on the repulsive
wall and the lower-state pair flies apart in $\sim$ps, so its population is pinned near zero.
The inversion is then automatic — the instant any KrF\* exists,
$$\Delta N=n_{\rm KrF^*}-n_{\rm lower}\approx n_{\rm KrF^*}>0,$$
with no lower-level depletion scheme needed (an effectively empty-lower-level laser). The
band-centre photon energy is
$$E_\gamma=\frac{hc}{\lambda}=\frac{1239.84\ \text{eV}\cdot\text{nm}}{248\ \text{nm}}=4.999\ \text{eV}.$$
So `photon_energy_eV(248)` $\approx4.999$ eV, and since every radiative event adds one
bound–free photon, `simulate_krf()` accumulates a monotonically increasing `photons` count
(the gain/Einstein-coefficient side is `~QO-03`).

### P6.  What is (and is not) conserved  *(this module §6)*
Show the closed reactions conserve the Kr-atom inventory n(Kr) + n(Kr\*) + n(KrF\*) and the
F-atom inventory 2n(F₂) + n(F) + n(KrF\*). Which quantity is *not* conserved, and why?
(The raw particle count: dissociative emission KrF\* → Kr + F splits one particle into two.)
*Check:* `simulate_krf()` keeps `kr_nuclei` and `f_nuclei` constant to < 10⁻⁶ relative across
the pulse (`test_excimer_atom_conservation`), while the total particle count grows.

**Solution.** Add the rate equations with the right stoichiometric weights. Every Kr nucleus
sits in exactly one of {Kr, Kr\*, KrF\*}, so (using the code's channels, with quench
returning Kr + F)
$$\frac{d}{dt}\big(n_{\rm Kr}+n_{\rm Kr^*}+n_{\rm KrF^*}\big)=(-r_1+r_3+r_4)+(r_1-r_2)+(r_2-r_3-r_4)=0 .$$
$\mathrm{F_2}$ carries two F atoms, F and KrF\* one each, so
$$\frac{d}{dt}\big(2n_{\rm F_2}+n_{\rm F}+n_{\rm KrF^*}\big)=2(-r_2)+(r_2+r_3+r_4)+(r_2-r_3-r_4)=0 .$$
Both vanish because each reaction merely **relabels** atoms. What is *not* conserved is the
raw particle count: the dissociative emission $\mathrm{KrF^*}\to\mathrm{Kr}+\mathrm{F}+h\nu$
splits one heavy particle into two, so $\sum_i n_i$ grows ($\approx+4\%$ here). Accordingly
`simulate_krf()` keeps `kr_nuclei` and `f_nuclei` constant to $<10^{-6}$ relative across the
pulse while the total particle count grows.

### P7.  Maxwellian vs. the real (LoKI) EEDF  *(Mi; `~PK-01`)*
The rate coefficients above assume a Maxwellian EEDF. Verify it is normalized and has
mean energy 3/2 kT, then explain why a *discharge* EEDF is generally **non-Maxwellian**
(field-driven tail depletion/enhancement) and must be solved from the electron kinetic
equation. *Check:* `maxwell_energy_pdf` integrates to 1 with ⟨ε⟩ = 3/2 kT
(`test_maxwell_eedf_normalized_and_mean_energy`); in `phantom11` the Maxwellian is replaced
by LoKI Monte-Carlo tables read at E/N = `CHOW_EN_TD_DEFAULT` = 51 Td (`loki_tables.py`).

**Solution.** The energy-space Maxwellian is
$F(\varepsilon)=\frac{2}{\sqrt\pi}(kT)^{-3/2}\sqrt\varepsilon\,e^{-\varepsilon/kT}$. With
$\int_0^\infty\varepsilon^{s-1}e^{-\varepsilon/kT}\,d\varepsilon=\Gamma(s)(kT)^s$ and
$\Gamma(\tfrac32)=\tfrac{\sqrt\pi}{2}$, $\Gamma(\tfrac52)=\tfrac{3\sqrt\pi}{4}$,
$$\int_0^\infty F\,d\varepsilon=\frac{2}{\sqrt\pi}(kT)^{-3/2}\,\Gamma(\tfrac32)(kT)^{3/2}=\frac{2}{\sqrt\pi}\cdot\frac{\sqrt\pi}{2}=1 ,$$
$$\langle\varepsilon\rangle=\int_0^\infty\varepsilon\,F\,d\varepsilon=\frac{2}{\sqrt\pi}(kT)^{-3/2}\,\Gamma(\tfrac52)(kT)^{5/2}=\frac{2}{\sqrt\pi}\cdot\frac{3\sqrt\pi}{4}\,kT=\tfrac32 kT .$$
A *discharge* EEDF is generally **not** Maxwellian: the reduced field $E/N$ feeds energy into
the electrons while inelastic thresholds (excitation, ionization) drain the high-energy tail,
so $F(\varepsilon)$ develops a depleted/enhanced tail no single $T$ can fit — it must be
solved from the electron kinetic (Boltzmann) equation (`~PK-01`). That is why
`maxwell_energy_pdf` integrates to 1 with $\langle\varepsilon\rangle=\tfrac32 kT$ here, whereas
phantom11 replaces the Maxwellian with LoKI Monte-Carlo tables read at $E/N=$
`CHOW_EN_TD_DEFAULT` $=51$ Td.
