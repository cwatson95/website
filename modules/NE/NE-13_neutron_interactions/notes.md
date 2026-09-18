# NE-13 — Neutron interactions: the 1/v law, resonances, activation (notes)

`~NE-12` decomposed the photon coefficient into three processes with smooth,
predictable dependences on $Z$ and $E$. Neutron cross sections are the opposite
in every respect, and that contrast is the point of this module.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed., §7.4,
cited by **printed** page (PDF = printed + 23). Cross sections from
`../data_tables/C1_thermal_neutron_cross_sections.csv` and
`../data_tables/C2_activation_radionuclides.csv`.

## 1. Why there is no theory to fit

Neutrons interact with the **nucleus**, not the electrons. So none of `~NE-12`'s
scalings survive: no $Z^4$, no $Z/A\simeq\tfrac12$, no smooth trend at all.
S&F are unusually blunt [§7.4, p. 196]:

> fundamental theories which can be used to predict neutron cross-section
> variations in any accurate way are still lacking. As a result, all
> cross-section data are empirical in nature, with little guidance available for
> interpolation between different energies or isotopes.

The tables make the point better than any argument. Thermal absorption:

| | $\sigma_a$ (b) | | ratio |
|---|---|---|---|
| ¹H | 0.333 | ²H 0.000506 | **658×** |
| ¹⁰B | 3840 | ¹¹B 0.00553 | **694 000×** |
| ²³⁵U $\sigma_f$ | 587 | ²³⁸U $\sigma_f$ 1.2×10⁻⁵ | **5×10⁷** |

These are **isotopes of the same element** — same chemistry, same electron
cloud, one neutron apart. Nothing in the periodic table predicts them. This is
why the module tabulates and interpolates only where behaviour is regular, and
raises rather than extrapolating elsewhere.

Two regularities do exist, and between them they carry most of reactor physics.

## 2. The 1/v law

Below about 1 keV, for light and some magic-number nuclei, S&F give
[Eq. (7.40), p. 199]
$$\sigma_t=\sigma_1+\frac{\sigma_2}{\sqrt{E}}.$$
Two terms with different origins: $\sigma_1$ is elastic scattering, nearly
energy-independent down here, and $\sigma_2/\sqrt{E}$ is radiative capture.
Since $E\propto v^2$, the second term is **$\propto1/v$** — the neutron spends
longer in the vicinity of the nucleus, and the capture probability rises in
proportion to the time available.

The consequence is the single most important fact in thermal reactor design:

| neutron energy | $\sigma_a$ relative to thermal |
|---|---|
| 1 keV | 0.005 |
| 1 eV | 0.159 |
| 0.0253 eV (thermal) | 1.000 |
| 0.001 eV | 5.03 |

**Slowing a neutron from 1 keV to thermal multiplies its capture cross section
by 199.** For ²³⁵U fission the gain from fission-spectrum energies is larger
still — roughly 600×. That is what buys the 115 graphite collisions of `~NE-08`:
moderation is not free, and it pays for itself several hundred times over.

Everything in Appendix C.1 is quoted at one reference point — **0.0253 eV,
2200 m/s, 293.6 K** — and `test_2200_metres_per_second_is_0_0253_eV` checks all
three agree. (A caution the module encodes: the *nominal* 2200 m/s is 0.02525 eV,
0.2% from 0.0253. Mixing the two as reference points introduces a small
systematic error, so `one_over_v_cross_section` anchors on the energy.)

Eq. (7.40) is stated for $E<1$ keV, and `light_nucleus_total_cross_section`
**raises above that** rather than extrapolating. The reason is not caution but
physics: above 1 keV resonances appear, and no smooth form describes them at all.

## 3. Resonances

A resonance is an energy at which the neutron plus target matches a level of the
compound nucleus (`~NE-08`), and the cross section can rise by four orders of
magnitude over a fraction of an eV. Their character shifts systematically with
mass [S&F §7.4.1, p. 199]:

| class | $A$ | resonance energies | widths |
|---|---|---|---|
| light | < 25 | keV to MeV | keV to MeV, sparse |
| intermediate | 25–150 | 100 eV to several keV | intermediate |
| heavy | > 150 | **eV region** | **< 1 eV**, unresolved above a few keV |

The trend has one cause: heavier nuclei have denser level schemes, so their
resonances come lower, closer together and narrower. **Only hydrogen and
deuterium have no resonances at all** — for both, the cross section is nearly
constant from 1 eV to the MeV region.

Now put the two vertical markers of `figures/fig3` together. A fission neutron
is born at ~2 MeV, above almost every resonance. To become useful it must be
slowed to 0.025 eV — straight down through the heavy-nuclide resonance forest,
where ²³⁸U's narrow capture resonances are waiting. The probability of getting
through without being captured is the **resonance escape probability**, and it
is one of the four factors of `~NE-19`. It is also why fuel is lumped rather
than dissolved: a neutron slowing down inside a fuel lump sees the resonances,
one slowing down in the moderator between lumps does not.

Below about 0.01 eV in solids there are **Bragg cutoffs** — energies below which
coherent scattering from crystal planes is no longer possible. S&F note them and
omit them from the figures; they matter for cold-neutron work and not for
reactors.

## 4. What actually happens, by energy

S&F's Table 7.1 lists what a shielding calculation needs, and the division is by
energy:

**Above 1 eV** — elastic scattering dominates. Inelastic scattering opens once
the neutron energy exceeds the first excited state of the scatterer (`~NE-08`'s
double-energy region), and above ~8 MeV multi-particle reactions like $(n,2n)$
become possible. Absorption is small: over the fission spectrum the $(n,\gamma)$
cross section "seldom exceeds 200 mb for the heavy elements".

**Below 1 eV** — absorption takes over, following §2, and fission for the
fissile nuclides.

Two exceptions worth carrying. **$(n,2n)$ thresholds are anomalously low for
deuterium (3.3 MeV) and beryllium (1.84 MeV)**, and neither has inelastic
scattering to compete. Beryllium's threshold sits *below* the 2 MeV mean fission
energy, which makes it a genuine **neutron multiplier** — the reason it appears
in fusion blankets (`~NE-10`, `~NE-24`) and as a reflector. And $(n,p)$ and
$(n,\alpha)$ matter for light elements: in the MeV region the $(n,\alpha)$ cross
sections for Be, N and O are appreciable fractions of the total, which is why
`~NE-11`'s Example 7.3 needed ¹⁷O's $(n,\alpha)$ channel rather than its capture
channel.

## 5. Activation

A neutron absorbed by a stable nuclide often leaves a radioactive one. For a
thin sample in a uniform flux [S&F Example 7.5, p. 204]
$$R=\frac{mN_A}{A}\sigma_\gamma\phi,$$
and the activity that builds up follows the saturation law of `~NE-07`:
$$A(t)=R\left[1-e^{-\lambda t}\right]\xrightarrow[t\to\infty]{}R.$$

**Example 7.5** irradiates 2 g of ⁵⁵Mn ($\sigma_\gamma=13.3$ b) for 2 minutes at
$10^{13}$ cm⁻² s⁻¹ and gets **2.609×10¹⁰ Bq**. The book states its assumption
explicitly — "the irradiation time is very small compared to the half-life" — and
so uses the linear form $A\simeq\lambda Rt$.

The exact form gives **2.598×10¹⁰ Bq**. The two differ by 0.45%, which is
exactly $\lambda t/2$, the leading term of the expansion. Both are checked, and
`activation_activity` **requires the half-life to be passed explicitly** so the
approximation is a choice rather than a silent default. The example sits 0.9% up
the saturation curve, which is why the shortcut is safe there and would not be
for a longer irradiation.

Foil activation is how neutron flux is actually *measured*: irradiate a foil of
known mass and cross section, count its activity, and invert the formula. The
practical constraint is finding a nuclide whose product half-life suits the
irradiation and the counting.

(A small caution the tables encode: Appendix C.2 lists ⁹⁹ᵐTc with **no**
activation cross section, and that blank is meaningful. Its parent ⁹⁹Mo is a
*fission product* (`~NE-09`), reached by decay rather than by capture on a stable
target, so no activation cross section applies. The loader returns `None` rather
than a zero that would silently produce a wrong rate.)

## 6. Fission cross sections, and what actually has to exceed one

S&F §7.4.2 restates the fissile/fissionable split of `~NE-09` in cross-section
terms. The thermal fission cross sections separate the two groups by four orders
of magnitude, so the classification is robust:

| | $\sigma_f$ (b) | $\sigma_\gamma$ (b) | $\alpha=\sigma_\gamma/\sigma_f$ | $\eta$ |
|---|---|---|---|---|
| ²³³U | 529 | 46 | 0.087 | **2.28** |
| ²³⁵U | 587 | 99 | 0.169 | 2.08 |
| ²³⁹Pu | 749 | 271 | 0.362 | 2.11 |
| ²⁴¹Pu | 1015 | 363 | 0.358 | — |
| ²³⁸U | 1.2×10⁻⁵ | 2.73 | — | — |

Two derived quantities do the work.

**$\alpha=\sigma_\gamma/\sigma_f$**, the capture-to-fission ratio. Every capture
is simultaneously a neutron that did not cause fission *and* a heavier actinide
created. ²³⁹Pu's 0.362 against ²³⁵U's 0.169 is a large part of why plutonium
recycling is harder than the energy content suggests (`~NE-23`).

**$\eta=\nu\sigma_f/\sigma_a$**, neutrons produced per neutron **absorbed** — as
distinct from $\nu$, neutrons per **fission**. It is $\eta$, not $\nu$, that must
exceed 1 for a chain reaction, and the gap between them is parasitic capture: 15%
even in ²³⁵U. Note that **²³³U has the highest $\eta$ despite the lowest $\nu$**,
purely because its capture-to-fission ratio is lowest — which is the entire
technical case for the thorium fuel cycle. $\eta$ is the first of the four
factors in `~NE-19`.

## Where this goes

- `~NE-19` — $\eta$ opens the four-factor formula; the resonance escape
  probability of §3 is another factor, and lumping is why it is not worse.
- `~NE-20` — ¹³⁵Xe, whose absorption cross section is the largest of any nuclide,
  poisons a reactor via the §3 mechanism at the §2 energies.
- `~NE-21` — the diffusion equation propagates the flux that §5 takes as given.
- `~NE-11` — the macroscopic machinery ($\Sigma=\sigma N$, mean free path,
  $R=\Sigma\phi$) restated here for neutrons.
- `~NE-08` — the elastic-scattering kinematics that make moderation possible, and
  the compound nucleus behind every resonance.
- `~NE-26` — neutron activation analysis is §5 used as a measurement technique.
