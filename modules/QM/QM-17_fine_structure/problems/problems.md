# QM-17 — Problems

Work them by hand, then check with `code/fine_structure.py`. Sources in `../refs.md`.

### P1.  The fine-structure constant from scratch  *(Griffiths 3e, Problem 7.14, p.378)*
Assemble $\alpha=e^2/4\pi\varepsilon_0\hbar c$ from the fundamental constants and
show it is the dimensionless number $\approx1/137$. Then show the Bohr energy is
$\mathrm{Ry}=\tfrac12\alpha^2 m_ec^2$, so fine structure (a further $\alpha^2$) is
$\sim10^{-4}$ of the gross spectrum.
*Answer:* $\alpha=7.297\times10^{-3}=1/137.036$; $\tfrac12\alpha^2 m_ec^2=13.606$ eV.
*Check:* `1/fine_structure_constant()` ≈ 137.036; `rydberg_energy_eV()` ≈ 13.606.
(`test_fine_structure_constant`, `test_bohr_energy_from_alpha`.)

**Solution.** The combination $\alpha=e^2/4\pi\varepsilon_0\hbar c$ is a pure number: $e^2/4\pi\varepsilon_0$
carries energy$\times$length, $\hbar$ action, $c$ speed, and the units cancel exactly, leaving
$$\alpha=7.297\times10^{-3}=\frac{1}{137.036}.$$
The Bohr energy is this $\alpha$ *squared* below the rest energy,
$\mathrm{Ry}=\tfrac12\alpha^2 m_ec^2=\tfrac12(7.297\times10^{-3})^2(511\,\mathrm{keV})=13.606$ eV.
Fine structure carries a *further* $\alpha^2\sim5\times10^{-5}$, so it drops from $13.6$ eV to
$\sim10^{-4}$ eV. Matches `1/fine_structure_constant()` → $137.036$ and
`rydberg_energy_eV()` → $13.6057$.

### P2.  The n = 2 fine-structure splitting  *(Griffiths 3e, Problem 7.21, p.387–388)*
The $n=2$ shell splits into $2P_{3/2}$ and $\{2S_{1/2},2P_{1/2}\}$. Using the
$(n,j)$ formula, find the $2P_{3/2}-2P_{1/2}$ interval in eV and in GHz.
*Answer:* $\Delta E=\dfrac{13.6\,\alpha^2}{16}\approx4.53\times10^{-5}$ eV
$\;\Rightarrow\; f=\Delta E/h\approx10.9$ GHz (the measured value, $\sim$10.97 GHz).
*Check:* `(fine_structure_correction_eV(2,1.5)-fine_structure_correction_eV(2,0.5))`
≈ 4.53e-5 eV; `*e/h/1e9` ≈ 10.95. (`test_n2_fine_structure_splitting`.)

**Solution.** With $E^1_{\rm fs}=E_n\dfrac{\alpha^2}{n^2}\!\left[\dfrac{n}{j+\frac12}-\dfrac34\right]$ and
$E_2=-3.4$ eV, the bracket is $2/1-\tfrac34=\tfrac54$ for $j=\tfrac12$ and $2/2-\tfrac34=\tfrac14$ for
$j=\tfrac32$, so
$$\Delta E=E^1_{\rm fs}(\tfrac32)-E^1_{\rm fs}(\tfrac12)=E_2\frac{\alpha^2}{4}\Big(\tfrac14-\tfrac54\Big)
=\frac{13.6\,\alpha^2}{16}=4.53\times10^{-5}\ \mathrm{eV}.$$
Dividing by $h$ gives $f=\Delta E/h\approx10.9$ GHz. This is exactly
`fine_structure_correction_eV(2,1.5)-fine_structure_correction_eV(2,0.5)` → $4.528\times10^{-5}$ eV,
and $\times e/h/10^9$ → $10.95$ GHz (the lab value is $\sim10.97$).

### P3.  Which degeneracies survive fine structure?  *(Griffiths 3e, §7.3.2 / Fig. 7.8, p.387)*
Show that fine structure depends only on $n$ and $j$: the $2S_{1/2}$ ($\ell=0$) and
$2P_{1/2}$ ($\ell=1$) levels stay exactly coincident, while $2P_{1/2}$ and
$2P_{3/2}$ split. Verify the three mechanisms recombine differently for the two
$\ell$ but give the same shift.
*Answer:* $\ell$-degeneracy is **broken**, $j$-degeneracy is **preserved**. For
$2S_{1/2}$: $E_{\rm rel}+E_{\rm Darwin}$ (spin-orbit $=0$); for $2P_{1/2}$:
$E_{\rm rel}+E_{\rm so}$ (Darwin $=0$); both $=-5.66\times10^{-5}$ eV.
*Check:* `fine_structure_correction_eV(2,0.5)` equals the $\ell=0$ and $\ell=1$
decompositions; `< fine_structure_correction_eV(2,1.5)`.
(`test_fine_structure_depends_only_on_n_and_j`, `test_fine_structure_decomposition`.)

**Solution.** The grand result $E^1_{\rm fs}(n,j)$ carries no $\ell$. For $2S_{1/2}$ ($\ell=0$)
spin-orbit vanishes, so the shift is relativistic $+$ Darwin,
$(-1.472+0.906)\times10^{-4}=-5.66\times10^{-5}$ eV; for $2P_{1/2}$ ($\ell=1$) the Darwin term
vanishes, so it is relativistic $+$ spin-orbit, $(-0.264-0.302)\times10^{-4}=-5.66\times10^{-5}$ eV —
**identical**, though assembled from different mechanisms. The $\ell$-degeneracy is therefore broken
only through $j$: $2P_{3/2}$ sits higher at $-1.13\times10^{-5}$ eV. Hence
`fine_structure_correction_eV(2,0.5)` → $-5.660\times10^{-5}$ (matching both $\ell$-decompositions)
$<$ `fine_structure_correction_eV(2,1.5)` → $-1.132\times10^{-5}$.

### P4.  Spin-orbit $\langle\mathbf L\cdot\mathbf S\rangle$ and the center of gravity  *(Griffiths 3e, Eq. 7.65, p.386)*
For a $p$ electron ($\ell=1,s=\tfrac12$) evaluate
$\langle\mathbf L\!\cdot\!\mathbf S\rangle=\tfrac{\hbar^2}{2}[j(j{+}1)-\ell(\ell{+}1)-s(s{+}1)]$
for $j=\tfrac12,\tfrac32$, and confirm the $(2j+1)$-weighted average vanishes.
*Answer:* $p_{1/2}:-\hbar^2$, $p_{3/2}:+\tfrac12\hbar^2$; center of gravity
$2(-\hbar^2)+4(\tfrac12\hbar^2)=0$ — spin-orbit only *redistributes* the level.
*Check:* `LS_coupling(0.5,1)` = −1, `LS_coupling(1.5,1)` = 0.5;
`2*LS_coupling(0.5,1)+4*LS_coupling(1.5,1)` = 0. (`test_LS_coupling_values`.)

**Solution.** From $\langle\mathbf L\!\cdot\!\mathbf S\rangle=\tfrac{\hbar^2}{2}[j(j{+}1)-\ell(\ell{+}1)-s(s{+}1)]$
with $\ell=1,\ s=\tfrac12$ (so $\ell(\ell{+}1)=2,\ s(s{+}1)=\tfrac34$):
$$p_{1/2}:\ \tfrac{\hbar^2}{2}\big[\tfrac34-2-\tfrac34\big]=-\hbar^2,\qquad
p_{3/2}:\ \tfrac{\hbar^2}{2}\big[\tfrac{15}{4}-2-\tfrac34\big]=+\tfrac12\hbar^2.$$
Weighting by the multiplicities $2j+1=2,4$: $2(-\hbar^2)+4(\tfrac12\hbar^2)=0$, so spin-orbit only
*redistributes* the doublet about its center of gravity (it adds no net energy). Matches
`LS_coupling(0.5,1)` $=-1$, `LS_coupling(1.5,1)` $=0.5$, and the weighted sum $=0$ (in units of $\hbar^2$).

### P5.  Landé g-factors of the lowest terms  *(Griffiths 3e, Eq. 7.78, p.390)*
Compute $g_J$ for $^2S_{1/2}$, $^2P_{1/2}$, $^2P_{3/2}$, $^2D_{5/2}$ and explain why
they bracket the orbital ($1$) and spin ($2$) limits.
*Answer:* $2,\ \tfrac23,\ \tfrac43,\ \tfrac65$. $g_J\to1$ when $s=0$ (orbital only),
$g_J\to2$ when $\ell=0$ (spin only); only the projection of $\mathbf S$ on
$\mathbf J$ survives the precession.
*Check:* `lande_g_factor(0.5,0)`=2, `lande_g_factor(0.5,1)`=2/3,
`lande_g_factor(1.5,1)`=4/3, `lande_g_factor(2.5,2)`=6/5.
(`test_lande_g_factor_known_terms`, `test_lande_g_factor_limits`.)

**Solution.** With $g_J=1+\dfrac{j(j{+}1)+s(s{+}1)-\ell(\ell{+}1)}{2j(j{+}1)}$ and $s=\tfrac12$:
$$^2S_{1/2}:1+\tfrac{3/4+3/4-0}{3/2}=2,\quad
{}^2P_{1/2}:1+\tfrac{3/4+3/4-2}{3/2}=\tfrac23,\quad
{}^2P_{3/2}:1+\tfrac{15/4+3/4-2}{15/2}=\tfrac43,\quad
{}^2D_{5/2}:1+\tfrac{35/4+3/4-6}{35/2}=\tfrac65.$$
They bracket $1$ and $2$ because only the projection of $\mathbf S$ on the conserved $\mathbf J$
survives the precession: $s=0$ leaves the orbital value $1$, $\ell=0$ leaves the spin value $2$.
Matches `lande_g_factor` → $2,\ \tfrac23,\ \tfrac43,\ \tfrac65$.

### P6.  Weak vs strong field: where is the crossover?  *(Griffiths 3e, Problem 7.23, p.389)*
The Zeeman shift is $\sim\mu_B B$; the spin-orbit (internal) scale in $n=2$ is the
fine-structure interval of P2. At what external field do they become comparable —
i.e. where does the weak-field (Landé) picture hand over to Paschen–Back?
*Answer:* $\mu_B B\sim\Delta E_{\rm fs}(n{=}2)\Rightarrow B\sim
4.5\times10^{-5}\,\mathrm{eV}/(5.79\times10^{-5}\,\mathrm{eV/T})\approx0.8$ T —
hence "strong" fields in hydrogen mean several tesla.
*Check:* `bohr_magneton_eV_per_T()*1.0` vs the $n{=}2$ splitting are within an order
of magnitude. (`test_zeeman_scale_vs_fine_structure`.) Compare the two regimes:
`zeeman_weak_field_eV(0.5,0,0.5,1.0)` (Landé) vs `zeeman_strong_field_eV(0,0.5,1.0)`
(Paschen–Back).

**Solution.** The internal (spin-orbit) scale in $n=2$ is the P2 interval
$\Delta E_{\rm fs}\approx4.5\times10^{-5}$ eV; the external Zeeman energy is $\mu_B B$ with
$\mu_B=5.79\times10^{-5}$ eV/T. They become comparable when
$$B\sim\frac{\Delta E_{\rm fs}}{\mu_B}\approx\frac{4.5\times10^{-5}}{5.79\times10^{-5}}\approx0.8\ \mathrm{T},$$
so the weak-field Landé picture gives way to Paschen–Back only at *several* tesla. At $B=1$ T both
limits happen to return $\mu_B B$ here: `zeeman_weak_field_eV(0.5,0,0.5,1.0)`$=\mu_B g_J B m_j=\mu_B(2)(\tfrac12)=5.79\times10^{-5}$ eV
and `zeeman_strong_field_eV(0,0.5,1.0)`$=\mu_B B(m_\ell+2m_s)=\mu_B(1)=5.79\times10^{-5}$ eV — both the
order of `bohr_magneton_eV_per_T()*1.0`, confirming the crossover near $1$ T.

### P7.  The 21 cm line  *(Griffiths 3e, Eqs. 7.97–7.99, p.399)*
From the ground-state spin-spin gap
$\Delta E=4g_p\hbar^4/3m_pm_e^2c^2a_0^4$, find the frequency and wavelength of the
hydrogen hyperfine photon, and identify the spectral region.
*Answer:* $\Delta E\approx5.9\ \mu$eV $\Rightarrow f\approx1420$ MHz,
$\lambda\approx21$ cm (microwave / radio). The triplet ($F{=}1$) lies above the
singlet ($F{=}0$); the spin-flip emits the 21 cm line.
*Check:* `hyperfine_splitting_eV()*1e6` ≈ 5.88; `hyperfine_frequency()/1e6` ≈ 1421;
`hyperfine_wavelength()*100` ≈ 21.1; `spin_spin_coupling(1)-spin_spin_coupling(0)`
= 1 ($\hbar^2$). (`test_21cm_line`, `test_spin_spin_triplet_singlet`.)

**Solution.** Evaluating the closed form with CODATA constants,
$$\Delta E=\frac{4g_p\hbar^4}{3m_pm_e^2c^2a_0^4}=5.88\ \mu\mathrm{eV}\ \Rightarrow\
f=\frac{\Delta E}{h}=1420\ \mathrm{MHz},\quad \lambda=\frac cf=21\ \mathrm{cm}$$
(microwave/radio). The gap is the triplet–singlet spin-spin splitting:
$\langle\mathbf S_p\!\cdot\!\mathbf S_e\rangle=\tfrac{\hbar^2}{2}[F(F{+}1)-\tfrac32]$ gives $+\tfrac14\hbar^2$
for $F{=}1$ (triplet, raised) and $-\tfrac34\hbar^2$ for $F{=}0$ (singlet, depressed), a gap of $\hbar^2$.
Matches `hyperfine_splitting_eV()*1e6` → $5.877$, `hyperfine_frequency()/1e6` → $1421$,
`hyperfine_wavelength()*100` → $21.1$, and `spin_spin_coupling(1)-spin_spin_coupling(0)` → $1$ ($\hbar^2$).

### P8.  The hierarchy of corrections  *(Griffiths 3e, Table 7.1, p.378)*
Order the ground-state Bohr energy, fine-structure shift, and hyperfine gap, and
check the step sizes against $\alpha^2$ and $m_e/m_p$.
*Answer:* $13.6\ \mathrm{eV}\gg1.8\times10^{-4}\ \mathrm{eV}\gg5.9\times10^{-6}\ \mathrm{eV}$;
fine/Bohr $\sim\alpha^2$, hyper/fine $\sim m_e/m_p$ (up to $g_p$ and numerical
factors). The Lamb shift ($\sim\alpha^3$) sits between fine and hyperfine and needs
QED (`~QM-22`).
*Check:* `bohr_energy_eV(1)`, `fine_structure_correction_eV(1,0.5)`,
`hyperfine_splitting_eV()` form the ladder. (`test_hierarchy_bohr_fine_hyperfine`.)

**Solution.** The three rungs are
$$|E_1^{\rm Bohr}|=13.6\ \mathrm{eV}\ \gg\ |E^1_{\rm fs}|=1.8\times10^{-4}\ \mathrm{eV}\ \gg\
\Delta E_{\rm hf}=5.9\times10^{-6}\ \mathrm{eV}.$$
The first step is $E^1_{\rm fs}/E_1=\tfrac14\alpha^2\approx1.3\times10^{-5}$ — the $\alpha^2$ of fine
structure; the second, $\Delta E_{\rm hf}/E^1_{\rm fs}\approx0.03$, is $\sim m_e/m_p$
($=5.4\times10^{-4}$) enhanced by $g_p$ and numerical factors. The Lamb shift ($\sim\alpha^3$, QED,
`~QM-22`) sits between fine and hyperfine. The ladder `bohr_energy_eV(1)`,
`fine_structure_correction_eV(1,0.5)`, `hyperfine_splitting_eV()` returns $-13.606$,
$-1.811\times10^{-4}$, $5.877\times10^{-6}$ eV.
