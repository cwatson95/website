# NE-19 — The neutron life cycle: four- and six-factor formulas, k_eff (notes)

A reactor is a bookkeeping problem. Follow one generation of fission neutrons
round the cycle, count what happens to them, and the ratio of the next generation
to this one is $k_{\rm eff}$. S&F define six factors:

| | | |
|---|---|---|
| $\varepsilon$ | fast fission factor | the bonus from ²³⁸U fissioning above ~1 MeV |
| $p$ | resonance escape probability | surviving ²³⁸U's resonances while slowing down |
| $f$ | thermal utilization | absorbed by *fuel* rather than by everything else |
| $\eta$ | thermal fission factor | fast neutrons produced per thermal absorption in fuel |
| $P^f_{NL}$ | fast non-leakage | |
| $P^{th}_{NL}$ | thermal non-leakage | |

$$\boxed{k_\infty=\varepsilon p f\eta}\qquad
\boxed{k_{\rm eff}=\varepsilon p f\eta\,P^f_{NL}P^{th}_{NL}}$$

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed.,
§§10.1–10.6, cited by **printed** page (PDF = printed + 23).

> **The printed Eqs. (10.16) and (10.17) omit $\varepsilon$**, and Eq. (10.17)
> calls the three-factor product $\eta p f$ "the four-factor formula". The book's
> own Tables 10.5 and 10.8 include it — Table 10.5's water row is 0.888, which is
> $\varepsilon\eta pf$ and not $\eta pf$ (0.845). See §6 below.

## 1. Thermal neutrons, and two cross-section tables that disagree on purpose

Neutrons thermalise into a Maxwellian [Eq. (10.1)]
$$\phi_M(E,T)\propto E\,e^{-E/kT},$$
**linear in $E$, not $\sqrt E$.** The *density* spectrum is the familiar
Maxwell–Boltzmann $\sqrt E\,e^{-E/kT}$; the flux is that times the speed, and
$v\propto\sqrt E$ supplies the extra factor. So the flux peaks at $kT$ and
averages $2kT$, where the density peaks at $kT/2$ and averages $\tfrac32 kT$.
Using $\tfrac32kT$ is a 33% error in a reaction rate.

At S&F's room temperature (293.61 K) $kT=0.0253$ eV — the energy of a 2200 m/s
neutron, and the reference for every thermal cross section.

Averaging a $1/v$ cross section over that spectrum gives [Eq. (10.5)]
$$\bar\sigma_a=\frac{\sqrt\pi}{2}g_a(T)\sqrt{\frac{T_0}{T}}\,\sigma_a(E_0),$$
where $\sqrt\pi/2=0.886$ and $g_a$ is the **Westcott non-1/v factor**, 1 for
light nuclei.

**This is why Tables 10.1 and 10.2 disagree, and mixing them is a systematic
few-percent error.** Table 10.1 is thermal-*averaged*; Table 10.2 is at 0.0253 eV.
For ²³⁸U — a clean $1/v$ absorber — the ratio is 0.888, within 0.3% of $\sqrt\pi/2$.
For ²³⁵U it is 0.867, so $g_a=0.978$: the deviation the Westcott factor exists to
describe. (S&F's own Example 10.3 mixes them, taking $\nu$ from Table 10.2 and
$\sigma_f,\sigma_a$ from Table 10.1.)

## 2. $\eta$ — the only factor that belongs to the fuel alone

$$\eta=\nu\frac{\Sigma_f^F}{\Sigma_a^F}\qquad\text{[Eq. (10.12)]}$$

Nothing you do to the moderator, coolant or control rods changes it. Two
thresholds matter: $\eta>1$ for a chain reaction, $\eta>2$ for **breeding** (one
neutron to continue the chain, one to convert a fertile atom).

Natural uranium gives $\eta=1.339$ — comfortably above 1, hopelessly below 2. Of
the fissile nuclides only ²³³U reaches 2.30, which is why the thorium cycle is the
only credible *thermal* breeder; ²³⁹Pu manages 2.11 thermally but exceeds 3 above
a few hundred keV, which is why plutonium breeders are **fast** reactors.

## 3. $f$ — and how a control rod works

$$f=\frac{\sigma^F_a}{\sigma^F_a+\sigma^{NF}_a(N^{NF}/N^F)}\qquad\text{[Eq. (10.11)]}$$

A control rod does one thing: it lowers $f$. That is the entire mechanism.

In natural uranium, ²³⁵U is 0.72% of the atoms and supplies **64%** of the
absorption, because its cross section is 250× ²³⁸U's.

## 4. $p$ — and why dilution helps twice over

$$p=\exp\left[-\frac{N_A I}{10^{24}\xi\Sigma_p}\right],\qquad
I=a\left(\frac{\Sigma_{sM}10^{24}}{N_A}\right)^c\qquad\text{[Eqs. (10.7), (10.8)]}$$

Two effects compound. Diluting the absorber obviously reduces $N_A$; less
obviously it *raises* the effective resonance integral $I$ ($c=0.486$ for ²³⁸U),
because more scattering per absorber atom carries a neutron across each resonance
in fewer, larger lethargy steps. Each absorber atom becomes individually more
effective — and the net still favours dilution, since the $N_A^{1-c}$ in the
exponent wins.

## 5. Leakage

$$P^{th}_{NL}=\frac{1}{1+L_T^2B_c^2},\qquad P^f_{NL}=e^{-B_c^2\tau_T}
\qquad\text{[Eqs. (10.13), (10.15)]}$$

with $L_T^2=L_M^2(1-f)$ [Eq. (10.14)]: fuel soaks up thermal neutrons, so
adding it *shortens* the diffusion length — in graphite at $f=0.81$, from 3070 to
570 cm².

The Fermi age $\tau_T$ is one sixth the mean square crow-flight distance from
birth to thermalisation, and it is the parameter that sets reactor *size*:
graphite's 368 cm² against water's 27. A graphite core must be metres across; a
water core need not be.

## 6. Putting it together — and the missing $\varepsilon$

The tension is the whole subject. **Adding moderator raises $p$ and lowers $f$**,
so $k_\infty$ has an interior maximum, and Table 10.5 gives it for natural
uranium:

| moderator | $(N_M/N_U)_{\rm opt}$ | $\varepsilon$ | $\eta$ | $f$ | $p$ | $k_\infty$ |
|---|---|---|---|---|---|---|
| H₂O | 1.70 | 1.051 | 1.338 | 0.869 | 0.727 | **0.888** |
| D₂O | 291 | 1.000 | 1.338 | 0.956 | 0.917 | **1.173** |
| Be | 191 | 1.000 | 1.338 | 0.822 | 0.708 | **0.779** |
| C | 417 | 1.000 | 1.338 | 0.823 | 0.709 | **0.781** |

**Only heavy water clears 1.** That single line is why enrichment plants exist,
and why the only natural-uranium power reactor in commercial service is the
CANDU. D₂O wins not on $f$ but on *being allowed to have a lot of moderator*: its
absorption cross section is 560× smaller than light water's, so it can be piled on
until $p$ is high without killing $f$.

Notice also that the water row is the **only** one with $\varepsilon\neq1$ — and
it is exactly the row that discriminates between the printed Eq. (10.17) and the
tables. $1.338\times0.869\times0.727=0.845$; the table says 0.888. The
$\varepsilon$ is there. `four_factor_formula_as_printed` reproduces the printed
version so the difference can be measured rather than argued about.

## 7. Lumping the fuel — how CP-1 worked

Break the homogeneity and $p$ roughly doubles. Neutrons then slow down in
moderator containing *no ²³⁸U at all*, and only those reaching a resonance energy
near a lump are in danger [Eq. (10.18)]:
$$p=\exp\left[-\frac{N_F V_F I}{\xi_M\Sigma_{sM}V_M}\right],\qquad
I=A+\frac{C}{\sqrt{r\rho}}.$$

That $1/\sqrt{r\rho}$ is a surface-to-volume statement: resonance capture in a
lump happens in a thin skin, so a fatter rod hides more of its own ²³⁸U.

$f$ falls slightly in return, because the thermal flux is depressed inside the
rod — the Wigner–Seitz calculation of §10.5, where the square cell is replaced by
an equal-area cylinder ($b=a/\sqrt\pi$) and
$$\frac1f=\frac{\Sigma_{aM}V_M}{\Sigma_{aF}V_F}F(x)+E(y,z).$$

The net, for S&F's 1.25 cm natural-uranium rods in graphite (Table 10.8): $p$
rises from 0.45 to 0.90, $f$ falls from ~0.98 to 0.905, and **$k_\infty$ reaches
1.118 at a 20 cm pitch** where the homogeneous mixture peaks at 0.781. That is
how Fermi's CP-1 went critical on natural uranium.

**A note on reading Eq. (10.25).** The series for $E(y,z)$ is
$$E=1+\frac{z^2}{2}\left[\frac{z^2}{z^2-y^2}\ln\frac zy-\frac34+\frac{y^2}{4z^2}\right],$$
and the grouping matters: $z^2/(z^2-y^2)$ multiplies *only the logarithm*, with
$z^2/2$ outside the whole bracket. In the printed two-dimensional layout the two
leading fractions sit side by side and read naturally as a single
$z^2/[2(z^2-y^2)]$ prefactor — which gives 1.736 instead of 1.031 and would turn
Example 10.9's $f=0.905$ into 0.553. The module implements both the series and
the exact Bessel form of Eq. (10.22) and tests them against each other.

## Where this goes

- `~NE-13` — the elastic-scattering kinematics and $\xi$ that make moderation work.
- `~NE-09` — $\nu$ and the fission cross sections $\eta$ is built from.
- `~NE-20` — what happens when $k_{\rm eff}\neq1$, and the feedbacks that fight it.
- `~NE-21` — where the buckling $B_c^2$ actually comes from.
- `~NE-22`, `~NE-23` — enrichment and lattice design as engineering choices.

## A note on this module's corrections

Five printed results in §§10.1–10.6 are contradicted by the book's own numbers,
and one prose claim is not reproduced by its own fit. All are pinned by tests.

1. **Eqs. (10.16)–(10.17)** omit $\varepsilon$ — settled by Table 10.5's water row
   and every row of Table 10.8.
2. **Table 10.3** gives heavy water $\sigma_{sM}=0.509$ b, a duplicate of its own
   $\xi$ column. Table 10.7's $\xi\Sigma_{sM}=0.178$ cm⁻¹ requires 10.6 b — and
   the same cross-check reproduces graphite to four figures.
3. **Example 10.1** displays the fraction with 6.206 immediately after computing
   6.639 and immediately before substituting 6.639 again.
4. **Example 10.3** writes $k_\infty=\eta f=2.4367\times0.8143$, but 2.4367 is
   $\nu$; $\eta=2.080$ was computed two lines above, and $2.080\times0.8143$ is
   the printed 1.6939.
5. **Example 10.4** writes $L^2=3500(1-0.8143)=570.1$. Table 10.4 gives 3070, and
   $3070\times0.1857=570.1$ exactly; 3500 gives 650.
6. **Example 10.9** writes $z=11.8284/55.4=0.20368$ two lines after computing
   $b=11.284$ cm. $11.284/55.4=0.20368$.

Recorded but *not* corrected: §10.4.1 says the heterogeneous $\varepsilon$ is
"5–10% higher" than the homogeneous one, while Eq. (10.6)'s own fitted constants
give at most **1.2%** anywhere in their range. And that fit tends to
$a-c=0.99934$ at infinite dilution — marginally below 1, which $\varepsilon$
cannot be, since it counts fissions *added*.
