# NE-14 — Charged-particle stopping: range, stopping power, the Bragg peak (notes)

`~NE-11` through `~NE-13` dealt with **neutral** particles, and everything there
followed from one fact: a photon or neutron travels in straight segments past
enormous numbers of atoms, interacts a handful of times, and is removed
probabilistically. Hence $e^{-\mu x}$, and hence **no definite range** — some
fraction always gets through.

Charged particles invert every clause of that sentence, and this module is the
consequences.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed., §7.5,
cited by **printed** page (PDF = printed + 23). Range constants are S&F
Tables 7.2 and 7.3, transcribed into `code/charged_particles.py`.

## 1. Why charged particles are different

They interact **continuously**, with many electrons at once, through the
long-range Coulomb force [S&F §7.5.1]. Thousands of interactions are needed to
stop one, and each costs very little — a 4 MeV alpha can lose at most 2.2 keV to
a single electron (`~NE-08`, Eq. 6.22), 0.05% of its energy.

Two things follow. Because the losses are many and small, slowing down is nearly
**deterministic**: particles of the same mass and initial energy travel almost
the same distance, and stop. Because the alpha is 7000 times heavier than an
electron, it is barely deflected — heavy charged particles travel in **almost
straight lines**.

So a beam of alphas is *not attenuated at all* until near the end of its range,
where it falls off abruptly [S&F Fig. 7.12]. The residual spread is called
**straggling**, and it comes from the statistics of the interaction count plus
occasional large-angle nuclear scattering near the end of the path.

That is the defining contrast, and `figures/fig2` draws the two curves together:

| | neutral | charged |
|---|---|---|
| interactions before stopping | a few to tens | thousands |
| path | straight segments, direction changes | almost straight (heavy) or tortuous (electrons) |
| attenuation | $e^{-\mu x}$, no range | flat, then a cliff |
| shielding question | "how much am I willing to let past?" | "is it thicker than $R$?" |

Three definitions of range coexist [S&F §7.5.2]: the **projected range** $R_p$
(where intensity halves), the **extrapolated range** $R_e$ (tangent at the
inflection, extended to the axis), and the **CSDA range** $R$ (continuous
slowing-down approximation). They differ slightly; CSDA is now standard and is
what this module computes.

**Electrons are the exception to the "straight line" clause.** Having the same
mass as the electrons they scatter from, they suffer large-angle deflections and
produce energetic secondary electrons (**delta rays**) that go on to ionize in
their own right. Their paths are badly tangled [S&F Figs. 7.13–7.14], and the
"range" quoted for an electron is the **path length along that twisting
trajectory** — not a depth. §5 returns to why that distinction matters.

## 2. Stopping power and the Bragg peak

The collisional stopping power has the form [S&F Eq. (7.41)]
$$-\left(\frac{dE}{ds}\right)_{\text{coll}}=\rho\frac{Z}{A}z^2f(I,\beta),$$
with $z$ the projectile charge and $f$ a function of the medium's mean
excitation energy $I$ and the particle's speed. S&F do not write out $f$ — the
Bethe formula — and neither does this module; the range tables of §3 are what the
book provides and what is testable.

Two dependences carry everything:

- **$z^2$** — a doubly charged alpha couples four times as strongly as a proton
  at the same speed. This is why fission fragments ($z\simeq20$) stop in microns.
- **$\rho Z/A$** — per gram, $Z/A\simeq\tfrac12$ for everything, so stopping
  power per unit *mass thickness* is nearly material-independent, exactly as in
  `~NE-12`'s Compton régime.

The crucial behaviour is what happens as the particle slows. $f(\beta)$ **rises**
as $\beta$ falls, so **stopping power increases along the track** and peaks just
before the particle stops. For alphas in water the maximum is at about 0.7 MeV
[S&F Fig. 7.15]. Plotted against depth this is the **Bragg curve**, and its shape
is the reason charged particles matter clinically:

> the dose maximum is deep, it is sharp, and there is essentially nothing beyond
> it.

A photon beam deposits most of its dose near the entrance and exponentially less
thereafter; a proton beam deposits its maximum at a depth you choose by picking
the energy, and zero past it. That is the whole argument for proton and
heavy-ion therapy (`~NE-27`), and the same physics makes an *inhaled* alpha
emitter far more damaging than the same activity outside the body (`~NE-18`).

## 3. Ranges, and the scaling rules

Under the continuous slowing-down approximation [S&F Eq. (7.44)]
$$R=\int_0^{E_0}\frac{dE}{(-dE/ds)_{\text{tot}}}.$$

S&F provide an empirical fit rather than the integral [Eq. (7.47)]:
$$\log_{10}(\rho R)=a+b\log_{10}E+c\left(\log_{10}E\right)^2,$$
with constants in Tables 7.2 (protons, alphas) and 7.3 (electrons), **valid only
for $0.1<E<10$ MeV**. `csda_mass_range` refuses energies outside that window
by default: the fit is a quadratic in $\log E$ with no physical content beyond
its range, and extrapolating it produces confident nonsense rather than a poor
estimate.

The natural unit is **mass thickness** $\rho R$ (g/cm²), and the reason is
rule 1 below. Three rules follow from Eq. (7.46) [S&F §7.5.4]:

1. **$\rho R$ is independent of density.** Air and water differ by 800× in
   density and only 1.2× in $\rho R$.
2. **At the same *speed*, $\rho R\propto m/z^2$.** So a 4 MeV alpha has about the
   same range as a 1 MeV proton — same speed, and $m/z^2=4/4=1$.
3. **Across media at the same speed, $\rho R\propto(m/z^2)(Z/A)$.**

Rule 2 is how S&F's **Example 7.7** gets the range of a 6 MeV triton in water: a
proton of the same speed has $E_p=E_T/3=2$ MeV, look up its range, multiply by
$m/z^2=3$. The answer is 0.021 cm.

S&F warn that **the rules fail below about 1 MeV per nucleon** — a 0.4 MeV alpha
has twice the range this predicts from a 0.1 MeV proton, because at low speed the
particle picks up and loses electrons and its *effective* charge is no longer $z$.

Sample ranges, from the tables:

| particle, energy | in water |
|---|---|
| 4 MeV alpha | 28 μm |
| 4 MeV proton | 235 μm |
| 1 MeV electron | 4.3 mm |
| light fission fragment, 99.9 MeV | ~4 mg/cm² ≈ 15 μm of Al |

**Two errors in the book's own numbers** turned up in checking these, both
documented in `refs.md`: Table 7.2's proton/Pb row is inconsistent with every
other row and is *withheld* rather than used, and Example 7.7 evaluates the water
range with the LiF row's $b$. Neither changes the physics; both would silently
corrupt a calculation.

## 4. Bremsstrahlung

A charged particle deflected by a nucleus radiates. The radiative stopping power
is [S&F Eq. (7.42)]
$$-\left(\frac{dE}{ds}\right)_{\text{rad}}
=\frac{\rho N_A}{A}(E+m_ec^2)Z^2F(E,Z),$$
and the ratio to collisional loss is approximately [Eq. (7.43)]
$$\frac{(-dE/ds)_{\text{rad}}}{(-dE/ds)_{\text{coll}}}
\simeq\frac{EZ}{700}\left(\frac{m_e}{M}\right)^2,\qquad E\ \text{in MeV}.$$

The $(m_e/M)^2$ is decisive. A proton is 1836× heavier, so its radiative fraction
is $3.4\times10^6$ times smaller, and S&F conclude flatly that "all other charged
particles are far too massive to produce significant amounts of bremsstrahlung".
**Bremsstrahlung is an electron problem, full stop.**

Setting the ratio to 1 gives the **crossover energy** $E=700/Z$ MeV
[S&F Example 7.6]: 8.9 MeV in gold, 117 MeV in carbon.

The linear $Z$ has a practical consequence worth carrying: shielding a 2 MeV beta
with **lead** turns 23% of the energy into penetrating bremsstrahlung, against
1.7% in **carbon**. So a beta shield is built low-$Z$ first — plastic, aluminium —
with lead only *behind* it to absorb the photons that get made anyway. Reaching
for lead first makes the problem worse.

## 5. Range is a path length, not a depth

The CSDA range is measured **along the track**. For a heavy particle the track is
nearly straight and the distinction hardly matters. For an electron it matters a
great deal, and S&F quote measured numbers [§7.5.4, from Cross, Freedman & Wong]:

| fraction of the energy | deposited within this fraction of $R$ |
|---|---|
| 80% | 60% |
| 90% | 70% |
| 95% | 80% |
| all of it | 110% |

So an electron's *penetration depth* is roughly 60–80% of its quoted range.
Using the CSDA range as a shielding thickness is conservative; using it as a
depth-of-deposition is not. The book gives a heavy-particle example of the same
effect: 100 keV protons on aluminium have $\rho R=0.26$ mg/cm² but a likely
penetration depth of 0.22, and for 10 keV protons on gold the average depth is
only 20% of the CSDA range.

## Where this goes

- `~NE-17` — dose is energy deposited per unit mass, and §2 is *how* it gets
  deposited; the ranges here decide whether an emitter is an external or an
  internal hazard.
- `~NE-18` — the Bragg peak's dense local deposition is why alpha emitters have a
  radiation weighting factor of 20; LET is stopping power under another name.
- `~NE-15` — a detector must stop the particle to measure it, so §3's ranges set
  the required detector thickness and window thinness.
- `~NE-12` — the photoelectrons, Compton electrons and pairs created there are
  the charged particles dealt with here; photons damage tissue only through them.
- `~NE-09` — fission fragments deposit 168 MeV within microns, which is why the
  fuel gets hot and not the coolant.
- `~NE-27` — proton and heavy-ion therapy is §2 turned into a treatment plan.
