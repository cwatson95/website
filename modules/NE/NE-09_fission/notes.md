# NE-09 — Fission: fissile nuclides, fragments, neutrons and the energy budget (notes)

`~NE-08` ended with a neutron that faces no Coulomb barrier and can be absorbed
by any nucleus at any energy. Fission is what happens next when the absorbing
nucleus is heavy enough. The compound nucleus, excited by the binding energy the
neutron releases on arrival, oscillates; if the excitation exceeds a barrier of
about 6 MeV, one of those oscillations stretches it into a dumbbell whose two
ends repel Coulombically harder than the short-ranged strong force can hold them,
and it snaps. Scission takes about $10^{-20}$ s.

The whole of reactor engineering is downstream of four numbers, and this module
computes all four.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed.,
§§6.5.3–6.6, cited by **printed** page (PDF = printed + 23). Masses from
`../data_tables/B1_atomic_masses.csv`.

## 1. Fissile or merely fissionable: one pairing term

The compound nucleus is excited to [S&F §6.6, p. 153]
$$E^{*}=S_n+E_n,$$
the neutron separation energy of the *product* nucleus plus whatever kinetic
energy the neutron brought (`excitation_energy`; recoil is negligible). Note
which nucleus $S_n$ belongs to: absorbing a neutron on ²³⁵U makes ²³⁶U, and it is
²³⁶U's neutron binding energy that is released.

Compare $E^{*}$ with the ~6.2 MeV barrier and the actinides split cleanly:

| target | $N$ | compound | $E^{*}$ at $E_n=0$ | verdict |
|---|---|---|---|---|
| ²³³U | 141 | ²³⁴U | 6.844 | **fissile** |
| ²³⁵U | 143 | ²³⁶U | 6.545 | **fissile** |
| ²³⁹Pu | 145 | ²⁴⁰Pu | 6.533 | **fissile** |
| ²⁴¹Pu | 147 | ²⁴²Pu | 6.309 | **fissile** |
| ²⁴⁰Pu | 146 | ²⁴¹Pu | 5.242 | fissionable |
| ²³⁸U | 146 | ²³⁹U | 4.806 | fissionable |
| ²³²Th | 142 | ²³³Th | 4.786 | fissionable |

Read the $N$ column. **Every fissile nuclide has an odd neutron number and every
merely fissionable one has an even number**, without exception. The cause is the
pairing term of `~NE-02`: adding a neutron to an odd-$N$ target completes a pair
and releases about 1.5 MeV more than adding one to an already-paired even-$N$
target. That single term — worth $\sim11.2/\sqrt{A}\simeq0.7$ MeV on each side of
the comparison — is the entire difference between a fuel and a blanket, and
`test_fissile_and_fissionable_split_on_the_pairing_term` checks that the two
groups do not overlap.

The consequence for ²³⁸U is quantitative: it is 1.39 MeV short, so a neutron must
*bring* that much. The fission spectrum of §4 peaks at 0.70 MeV and averages
1.99 MeV, so some fission neutrons qualify and most do not — fast fission of ²³⁸U
is real and worth a few percent of a PWR's power, but it can never sustain a
chain on its own (`~NE-19`).

**Fertile** nuclides are the fissionable ones that *become* fissile on capture
[S&F p. 152]:
$$^{232}\text{Th}(n,\gamma)^{233}\text{Th}\xrightarrow[22\,\text{m}]{\beta^-}
{}^{233}\text{Pa}\xrightarrow[27\,\text{d}]{\beta^-}{}^{233}\text{U},$$
$$^{238}\text{U}(n,\gamma)^{239}\text{U}\xrightarrow[24\,\text{m}]{\beta^-}
{}^{239}\text{Np}\xrightarrow[56\,\text{h}]{\beta^-}{}^{239}\text{Pu}.$$
Two beta decays raise $Z$ by 2 and $N$ by $-1$ — turning an even-$N$ target into
an odd-$N$ one, which is the pairing argument run in reverse. Breeding
(`~NE-23`) is nothing more than this observation industrialised: 99.3% of natural
uranium is ²³⁸U, and a breeder converts it into fuel rather than discarding it.

A few nuclides fission **spontaneously**, without any neutron at all — a
tunnelling process competing with alpha decay (S&F Table 6.2, `~NE-05`). Almost
always it is a tiny branch, but it matters twice over: ²⁵²Cf, fissioning in 3.09%
of decays, emits $2.3\times10^{12}$ n/(g·s) and is the standard laboratory
neutron source, and ²⁴⁰Pu's 920 n/(g·s) is why reactor-grade plutonium
pre-initiates and cannot be used in a gun-type weapon.

**Two of the 26 rows in Table 6.2 are typos**, found by checking each row against
its own other columns; see `refs.md`. That the table can be checked at all is
because it is over-determined: half-life, fission probability, alphas per fission
and neutron emission rate are four numbers constrained by two relations.

## 2. Fragments, and why the energy spectrum is bimodal

Conservation is exact and simple [S&F Eq. (6.34)]:
$$A_L+A_H+\nu_p=A_{\text{target}}+1,\qquad Z_L+Z_H=Z_{\text{target}}$$
— `conserve_fission`. What is *not* simple is which pair forms. Thermal fission
is strongly **asymmetric**: $A\simeq94$ and $A\simeq140$ appear in about 6.5% of
fissions each, while a symmetric $A\simeq118$ split appears in 0.01% — a
peak-to-valley ratio of about 650 [S&F Fig. 6.6, p. 155]. Raise the incident
energy and the asymmetry washes out (about 100 at 14 MeV, a single central peak
at 90 MeV), which is a hint that the asymmetry is a shell effect and not a
liquid-drop one.

The fragments fly apart with equal and opposite momenta, so [S&F Eqs. (6.40)–(6.41)]
$$\frac{E_L}{E_H}=\frac{m_H}{m_L},\qquad
E_L=E_{\text{ff}}\frac{m_H}{m_L+m_H}$$
— `fragment_energy_split`. **The lighter fragment carries more energy**, and
because the mass distribution is bimodal the *energy* distribution is bimodal
too, peaking at 99.2 MeV (light) and 68.1 MeV (heavy) rather than showing a
single line at their average [S&F Fig. 6.7, p. 157].

Both fragments start with the parent's neutron-to-proton ratio, $144/92=1.57$,
against the 1.2–1.4 that is stable at $A\sim100$. They are therefore
grossly neutron-rich and beta-decay down an **isobaric chain** at constant $A$
(`~NE-07`). Four chains carry most of the history and practice of the subject:
$$^{140}\text{Xe}\to{}^{140}\text{Cs}\to{}^{140}\text{Ba}\to{}^{140}\text{La}
\to{}^{140}\text{Ce (stable)},$$
the chain whose barium and lanthanum Hahn, Strassmann and Meitner detected in
1939 and thereby discovered fission;
$$^{147}\text{Nd}\to{}^{147}\text{Pm}\to{}^{147}\text{Sm},$$
which produces promethium, an element with no stable isotope;
$$^{99}\text{Sr}\to\cdots\to{}^{99}\text{Mo}\to{}^{99\text{m}}\text{Tc}
\to{}^{99}\text{Tc}\to{}^{99}\text{Ru},$$
the source of the ⁹⁹ᵐTc used in most nuclear-medicine scans (`~NE-27`), and the
generator whose 22.9 h milking interval `~NE-07` computed; and
$$^{135}\text{Sb}\to{}^{135}\text{Te}\to{}^{135}\text{I}\to{}^{135}\text{Xe}
\to{}^{135}\text{Cs}\to{}^{135}\text{Ba},$$
containing ¹³⁵Xe, which has the largest thermal-neutron absorption cross section
of any nuclide and can poison a reactor into shutdown (`~NE-20`).

## 3. The energy: 200 MeV, and where it goes

The estimate is a one-liner from `~NE-03`. Binding energy per nucleon is about
8.4 MeV near $A\simeq100$ and 7.5 MeV near uranium, so splitting 236 nucleons and
gaining 0.9 MeV each releases $236\times0.9\simeq200$ MeV.

The exact value for a specific split comes from the mass deficit
[S&F Example 6.4]:
$$E_p=\left[M(^{235}\text{U})+m_n-\sum M(\text{fragments})-\nu_pm_n\right]c^2$$
— `prompt_energy_release`. For $^{235}$U$(n,f)\to{}^{139}$Xe$+^{95}$Sr$+2n+7\gamma$
this gives **183.6 MeV**, of which 5.2 MeV is in the neutrons and 6.7 MeV in the
gammas, leaving $E_{\text{ff}}=171.7$ MeV for the fragments — 101.9 MeV to the
light one and 69.8 MeV to the heavy one.

Then the fragments decay. Seven beta decays take ¹³⁹Xe to ¹³⁹La and ⁹⁵Sr to
⁹⁵Mo, releasing [S&F Example 6.5]
$$E_d=\left[M(^{139}\text{Xe})+M(^{95}\text{Sr})-M(^{139}\text{La})-M(^{95}\text{Mo})\right]c^2
=24.2\ \text{MeV}.$$
Note what does **not** appear: an electron-mass correction. Seven $\beta^-$
particles leave, but seven ambient electrons are absorbed to keep the atoms
neutral, so neutral-atom masses give the answer directly — unlike the $\beta^+$
and EC cases of `~NE-05`, where the corrections are the entire subtlety.

$183.6+24.2=207.8$ MeV, which is the "about 200 MeV" of every introduction and
within 1 MeV of Table 6.5's average over all outcomes:

| component | produced (MeV) | recoverable (MeV) |
|---|---|---|
| fission fragment kinetic energy | 168 | 168 |
| prompt neutrons | 5 | 5 |
| prompt gammas | 7 | 7 |
| capture gammas | — | 3–9 |
| delayed betas | 8 | 8 |
| delayed gammas | 7 | 7 |
| **neutrinos** | **12** | **0** |
| total | 207 | 198–204 |

Two lines carry the engineering. The fragments' 168 MeV is 81% of the total and
is deposited within a fraction of a millimetre of where it is created — the fuel
pellet gets hot, not the coolant, and the whole thermal-hydraulic design of
`~NE-22` follows from that locality. And the 12 MeV of neutrino energy is gone:
neutrinos pass through the reactor, the planet and the solar system without
interacting, so a reactor is intrinsically ~6% less efficient than its mass
deficit suggests. (It is also detectable — reactor antineutrinos are how
Reines and Cowan first observed the neutrino, and are now proposed for
safeguards monitoring.)

## 4. The neutrons: $\nu$, $\beta$, and the spectrum

Between 0 and about 8 neutrons boil off the excited fragments within $10^{-17}$ s.
Averaged over outcomes [S&F Table 6.3, p. 158]:

| nuclide | $\bar\nu$ (thermal) | $\beta$ | $\bar\nu$ (fast) | $\beta$ |
|---|---|---|---|---|
| ²³⁵U | 2.43 | 0.0065 | 2.57 | 0.0064 |
| ²³³U | 2.48 | 0.0026 | 2.62 | 0.0026 |
| ²³⁹Pu | 2.87 | 0.0021 | 3.09 | 0.0020 |
| ²⁴¹Pu | 3.14 | 0.0049 | — | — |
| ²³⁸U | — | — | 2.79 | 0.0148 |
| ²³²Th | — | — | 2.44 | 0.0203 |

$\bar\nu>2$ for every fissile nuclide, which is the necessary condition for a
chain reaction with margin left over for leakage and parasitic capture
(`~NE-19`). Fast fission gives more neutrons than thermal, because a hotter
compound nucleus boils off more.

The important column is $\beta$, the **delayed neutron fraction** — neutrons
emitted not at scission but seconds to minutes later, by the beta decay of a few
dozen precursor fission products. It is under 1% everywhere, and it is the reason
reactors can be controlled by human beings and mechanical rods. A reactor held
just subcritical on prompt neutrons alone responds on the $\sim10^{-4}$ s prompt
neutron lifetime; held critical *only with* the delayed contribution, its period
is set by the precursors' seconds-to-minutes half-lives instead. Everything in
`~NE-20` lives in that gap. Note also that ²³⁹Pu's $\beta$ is a third of ²³⁵U's:
a plutonium-heavy core has correspondingly less reactivity margin before prompt
criticality, which is a real constraint on MOX loading (`~NE-23`).

The prompt neutrons are born **fast**, with the Watt distribution
[S&F Eq. (6.42), p. 159]
$$\chi(E)=\frac{e^{-(E+E_w)/T_w}}{\sqrt{\pi E_wT_w}}
\sinh\!\left(\frac{\sqrt{4E_wE}}{T_w}\right)
\;\equiv\;ae^{-E/b}\sinh\sqrt{cE}$$
— `watt_spectrum`, with Table 6.4's parameters. It **peaks at 0.70 MeV and
averages 1.99 MeV**: broad and strongly right-skewed, so the mode and the mean
differ by a factor of three and quoting one for the other is a standard error.
Since a thermal neutron has 0.025 eV, every fission neutron must be slowed by
about eight decades — the 18 hydrogen or 115 graphite collisions of `~NE-08` —
before it is efficient at causing the next fission. A reactor is, structurally,
a machine for doing that slowing down cheaply.

## 5. Macroscopic consequences

At 200 MeV recoverable per fission [S&F p. 162],
$$1\ \text{W}=3.1\times10^{10}\ \text{fissions/s},\qquad
1\ \text{MWd}=1.05\ \text{g of }^{235}\text{U fissioned}.$$
But only 85% of thermal neutrons absorbed by ²³⁵U cause fission; the other 15%
give $(n,\gamma)$ ²³⁶U. So the **consumption** rate is higher [S&F p. 163]:
$$\boxed{1\ \text{MWd}=1.24\ \text{g of }^{235}\text{U consumed}}$$
— `grams_per_mwd(fission_fraction=0.85)`. Equivalently 1 g of ²³⁵U yields
0.95 MWd = 82 GJ, against coal's 12 GJ per **tonne**: a factor of nearly seven
million, and the only reason any of this is worth the trouble.

Finally, **decay heat**. The fission products keep radiating after shutdown
[S&F Eqs. (6.44)–(6.45), valid $10\ \text{s}<t<10^5$ s]:
$$F_\gamma(t)=1.4\,t^{-1.2},\qquad F_\beta(t)=1.26\,t^{-1.2}
\quad\text{MeV s}^{-1}\text{ fission}^{-1}.$$
The functional form is the point. This is a **power law**, not an exponential,
because it is the superposition of hundreds of decay chains with half-lives
spread over ten decades — so it has no characteristic time and never really
switches off. A decade in time buys only a factor $10^{1.2}\simeq16$ in power. A
shut-down core sits at roughly 7% of full power the instant the rods drop and is
still of order 1% an hour later — megawatts in a large reactor. Every
loss-of-coolant accident in history — Three Mile Island, Fukushima — is a story
about this curve, and it is why a reactor cannot simply be switched off
(`~NE-22`, `~NE-23`).

## Where this goes

- `~NE-10` — fusion, the other side of the binding-energy curve of `~NE-03`.
- `~NE-13` — the cross sections that decide how *often* fission happens, and the
  1/v and resonance structure that makes moderation worth the trouble.
- `~NE-19` — the neutron life cycle: $\nu$, the fast-fission factor from §1, and
  the resonance-escape probability assemble into $k_\infty$ and $k_{\text{eff}}$.
- `~NE-20` — point kinetics: $\beta$ from §4 is the parameter the whole theory
  turns on, and the ¹³⁵Xe chain of §2 is the poisoning transient.
- `~NE-22`, `~NE-23` — the 1.24 g/MWd of §5 sizes the fuel cycle, the decay-heat
  curve sizes the emergency cooling, and the fission-product chains of §2 are the
  waste inventory.
- `~NE-27` — ⁹⁹ᵐTc, a fission product turned into the most-used diagnostic
  radionuclide in medicine.
