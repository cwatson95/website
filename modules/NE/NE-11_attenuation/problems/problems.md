# NE-11 — Problems

Work each by hand, then check with `code/attenuation.py`. Citations in
`../refs.md`; **S&F** = Shultis & Faw 3rd ed., cited by printed page. P1–P7
follow the book's Chapter 7 problems 1, 2, 4, 5, 8, 10 and 11 (printed 218–219);
P8 is added. Coefficients from `../data_tables/C3_photon_coefficients_*.csv` and
`../data_tables/C1_thermal_neutron_cross_sections.csv`.

### P1.  Measuring μ from a transmission experiment  *(S&F Ch. 7, Prob. 1)*
A broad beam of neutrons is normally incident on a 6 cm homogeneous slab; 40% is
transmitted without interacting. Find (a) $\mu_t$ and (b) the mean distance a
neutron travels before interacting.
*Check:* (a) 0.1527 cm⁻¹; (b) 6.55 cm.

**Solution.** Invert Eq. (7.4):
$$0.40=e^{-\mu_t(6)}\;\Rightarrow\;
\mu_t=\frac{-\ln0.40}{6}=\frac{0.9163}{6}=\boxed{0.1527\ \text{cm}^{-1}},$$
and by Eq. (7.8) the mean free path is $1/\mu_t=\boxed{6.55\ \text{cm}}$.

This is how interaction coefficients are actually *measured* — the definition in
Eq. (7.1) is a limit and cannot be used directly. Note the slab is only 0.92 mfp
thick, which is what makes the measurement good: much thinner and the
transmitted fraction is indistinguishable from 1, much thicker and it is
indistinguishable from 0. Transmission experiments are most precise near 1 mfp.

One caution the problem glosses over: it says *broad beam*, and Eq. (7.4)
describes a **narrow** beam. In a broad-beam geometry scattered neutrons reach
the detector too, so the measured transmission is $B\times e^{-\mu t}$ and the
inferred $\mu$ is an **underestimate**. Real measurements use collimation to
approximate the narrow-beam condition.

### P2.  Half-thicknesses at 1 MeV  *(S&F Ch. 7, Prob. 2)*
Using Appendix C, find the half-thickness for 1 MeV photons in water, iron and
lead.
*Check:* 9.81 cm, 1.48 cm, 0.898 cm.

**Solution.** $x_{1/2}=\ln2/\mu$ with $\mu=\rho(\mu/\rho)$:

| | $\mu/\rho$ (cm²/g) | $\rho$ (g/cm³) | $\mu$ (cm⁻¹) | $x_{1/2}$ (cm) |
|---|---|---|---|---|
| water | 0.07066 | 1.00 | 0.0707 | **9.81** |
| iron | 0.05951 | 7.874 | 0.4686 | **1.48** |
| lead | 0.06803 | 11.35 | 0.7721 | **0.898** |

Look at the first column. At 1 MeV the three mass coefficients agree within 15%,
while the half-thicknesses span a factor of 11. **The entire difference is
density.** At MeV energies photons interact almost exclusively by Compton
scattering off electrons, and every material has roughly the same number of
electrons per gram ($Z/A\simeq0.5$, except hydrogen's 1.0). Lead is a good
gamma shield because it packs those electrons into less space, not because lead
atoms are individually better at stopping MeV photons.

That stops being true below ~0.5 MeV, where the photoelectric effect and its
steep $Z$ dependence take over and lead genuinely does become special
(`~NE-12`).

### P3.  Working backwards from a tenth-thickness  *(S&F Ch. 7, Prob. 4)*
A material has a tenth-thickness of 2.6 cm for 1.25 MeV gammas. Find (a) $\mu$,
(b) $x_{1/2}$, (c) the mean free path.
*Check:* 0.8856 cm⁻¹, 0.783 cm, 1.129 cm.

**Solution.** (a) $\mu=\ln10/x_{1/10}=2.3026/2.6=\boxed{0.8856\ \text{cm}^{-1}}$.

(b) $x_{1/2}=\ln2/\mu=\boxed{0.783\ \text{cm}}$.

(c) $\ell=1/\mu=\boxed{1.129\ \text{cm}}$.

The three lengths are fixed multiples of each other and carry no independent
information:
$$x_{1/2}:\ell:x_{1/10}=\ln2:1:\ln10=0.693:1:2.303.$$
So a tenth-thickness is always **3.32 half-thicknesses** — never "ten
half-thicknesses", which is the mistake the ratio is there to prevent.

(For context, $\mu=0.886$ cm⁻¹ at 1.25 MeV is denser than lead's 0.66 cm⁻¹ at
that energy, so this hypothetical material is heavier than lead — depleted
uranium or tungsten territory.)

### P4.  Two slabs in series  *(S&F Ch. 7, Prob. 5)*
Two adjacent slabs have thicknesses $t_1,t_2$ and coefficients $\mu_1,\mu_2$.
Find the probability a gamma ray (a) first interacts in slab 1, (b) first
interacts in slab 2, (c) penetrates both.

**Solution.** (a) Interacting somewhere in slab 1 is Eq. (7.5):
$$P_1=1-e^{-\mu_1t_1}.$$

(b) To interact first in slab 2 the photon must cross slab 1 *and then* interact
in slab 2. The two are independent, so the probabilities multiply:
$$P_2=e^{-\mu_1t_1}\left(1-e^{-\mu_2t_2}\right).$$

(c) $$P_{\text{through}}=e^{-\mu_1t_1}e^{-\mu_2t_2}=e^{-(\mu_1t_1+\mu_2t_2)}.$$

Check: $P_1+P_2+P_{\text{through}}=1$, as it must be — the photon does exactly
one of these three things.

Two things to take from this. The survival probability depends only on
$\sum_i\mu_it_i$, the **total optical thickness**, so for the transmitted beam
the slab **order does not matter** (`test_layered_shields_add_in_mean_free_paths`).
But $P_1$ and $P_2$ separately *do* depend on order, which is why real shields
are layered deliberately — a high-$Z$ layer first to stop photons, a low-$Z$
layer behind it to catch the secondary electrons and bremsstrahlung, and the
reverse arrangement works far worse.

Generalising to $N$ slabs [Prob. 6]:
$$P_i=\left[\exp\left(-\sum_{j<i}\mu_jt_j\right)\right]\left(1-e^{-\mu_it_i}\right),
\qquad P_{\text{through}}=\exp\left(-\sum_{j=1}^{N}\mu_jt_j\right).$$

### P5.  Natural uranium  *(S&F Ch. 7, Prob. 8)*
Natural uranium is 0.720% ²³⁵U, 0.0055% ²³⁴U and the rest ²³⁸U by atom. Using
Table C.1, find the total macroscopic cross section and the macroscopic fission
cross section for thermal neutrons.
*Check:* $\Sigma_t=0.828$ cm⁻¹, $\Sigma_f=0.204$ cm⁻¹.

**Solution.** Uranium metal has $\rho=19.05$ g/cm³ and $A=238.03$, so
$$N=\frac{19.05\times6.022\times10^{23}}{238.03}=0.0482\times10^{24}\ \text{cm}^{-3}.$$

From Table C.1, $\sigma_t$ = 700 b (²³⁵U), 116 b (²³⁴U), 12.2 b (²³⁸U):
$$\bar\sigma_t=0.00720(700)+0.000055(116)+0.99275(12.2)=17.18\ \text{b},$$
$$\Sigma_t=0.0482\times17.18=\boxed{0.828\ \text{cm}^{-1}}.$$

For fission, $\sigma_f$ = 587 b (²³⁵U), 0.465 b (²³⁴U), $1.2\times10^{-5}$ b (²³⁸U):
$$\bar\sigma_f=0.00720(587)=4.23\ \text{b},\qquad
\Sigma_f=\boxed{0.204\ \text{cm}^{-1}}.$$

Now read the numbers. ²³⁵U is 0.72% of the atoms and supplies **essentially
100%** of the thermal fission and **29%** of the total interaction — a nuclide
present at one part in 139 dominating the reactor physics, because its cross
section exceeds ²³⁸U's by a factor of 57. This is the same
abundance-times-cross-section arithmetic as Example 7.3, with the opposite
conclusion: there the rare isotope was negligible, here it is everything.

Note also $\Sigma_f/\Sigma_t=0.25$: only a quarter of thermal-neutron
interactions in natural uranium are fissions. The rest are mostly capture in
²³⁸U, which is why natural uranium cannot go critical in a light-water reactor
and why enrichment exists (`~NE-19`, `~NE-23`).

### P6.  Mean free path in graphite  *(S&F Ch. 7, Prob. 10)*
Using Appendices A.3 and C.1, find the mean free path of a thermal neutron in
graphite.
*Check:* $\Sigma_t=0.404$ cm⁻¹, mfp = 2.48 cm (for $\rho=1.7$ g/cm³).

**Solution.** Reactor graphite has $\rho\simeq1.7$ g/cm³ and $A=12.011$:
$$N=\frac{1.7\times6.022\times10^{23}}{12.011}=0.0852\times10^{24}\ \text{cm}^{-3}.$$
Table C.1 gives $\sigma_t(^{12}\text{C})=4.74$ b, so
$$\Sigma_t=0.0852\times4.74=0.404\ \text{cm}^{-1},\qquad
\ell=1/\Sigma_t=\boxed{2.48\ \text{cm}}.$$

The answer is sensitive to the density assumed, and graphite's varies from
~1.6 g/cm³ (nuclear grade, deliberately porous) to 2.26 (ideal crystal) — so
quote the density with the answer.

The physics worth noticing: almost all of that 4.74 b is **scattering**, not
absorption ($\sigma_\gamma=0.0034$ b). Carbon interacts with neutrons readily and
consumes them almost never, which is precisely the combination a moderator needs
— many collisions to slow the neutron down (115 of them, from `~NE-08`), each
costing essentially no neutrons. The 2.48 cm mfp times 115 collisions is why a
graphite-moderated core is metres across.

### P7.  Flux density is not particle density  *(S&F Ch. 7, Prob. 11)*
At a point the flux density is $4\times10^{12}$ cm⁻² s⁻¹. Find the particle
density if the particles are (a) photons, (b) thermal neutrons (2200 m/s).
*Check:* (a) 133 cm⁻³; (b) $1.82\times10^{7}$ cm⁻³.

**Solution.** Invert Eq. (7.14), $n=\phi/v$:

(a) Photons travel at $c=3.00\times10^{10}$ cm/s:
$$n=\frac{4\times10^{12}}{3.00\times10^{10}}=\boxed{133\ \text{cm}^{-3}}.$$

(b) Thermal neutrons travel at $2.2\times10^{5}$ cm/s:
$$n=\frac{4\times10^{12}}{2.2\times10^{5}}=\boxed{1.82\times10^{7}\ \text{cm}^{-3}}.$$

**The same flux density corresponds to particle densities differing by 136,000.**
That is the whole reason flux density, and not particle density, is the working
variable. Reaction rate is $\mu\phi$, not $\mu n$: what matters is how much
*track length* the particles lay down per second, and a fast particle lays down
more track per unit density than a slow one.

The neutron figure is also a useful sanity check on how empty a reactor is:
$1.8\times10^{7}$ neutrons/cm³ against $\sim10^{22}$ atoms/cm³ of fuel is one
neutron per $10^{15}$ atoms. A reactor core is, by number, almost entirely not
neutrons.

### P8.  Why shielding beats standoff  *(added)*
A 1 Ci point source emits 1 MeV photons. Compare (a) retreating from 1 m to 10 m
with (b) staying at 1 m behind 10 cm of lead. Then find how much lead matches a
retreat to 100 m.
*Check:* (a) ×100; (b) ×2250; (c) about 15 cm.

**Solution.** From Eq. (7.26), $\phi^o=S_pe^{-\mu t}/4\pi r^2$ with
$\mu_{\text{Pb}}=0.7721$ cm⁻¹.

(a) Geometric attenuation is a power law: $(10)^2=\boxed{100}$.

(b) Material attenuation is exponential:
$e^{0.7721\times10}=e^{7.721}=\boxed{2250}$.

So 10 cm of lead — a slab you can lift — outperforms a 9 m retreat by a factor of
22, and it does so in a room rather than a field.

(c) Retreating to 100 m buys $10^4$. Matching that needs
$$t=\frac{\ln10^4}{0.7721}=\frac{9.21}{0.7721}=\boxed{11.9\ \text{cm}},$$
so 12 cm of lead equals a 100 m standoff, and 24 cm equals 10 km. The exponential
never runs out of leverage; the inverse square always does.

This asymmetry is why radiation protection is taught as **time, distance,
shielding** — cheapest first — but why every serious installation ends up
relying on the third. It also shows the limit of the argument: the calculation
above is *uncollided* flux, and at 12 cm (9.2 mfp) of lead the buildup factor is
substantial, so the real dose reduction is well short of $10^4$. Deep shields are
where §2's warning bites hardest.
