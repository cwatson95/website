# NE-10 — Problems

Work each by hand, then check with `code/fusion.py`. Citations in `../refs.md`;
**S&F** = Shultis & Faw 3rd ed., cited by printed page. P1–P4 follow the book's
Chapter 6 problems 22–25 (printed 177); P5–P8 are added. Masses from
`../data_tables/B1_atomic_masses.csv`.

### P1.  A glass of water  *(S&F Ch. 6, Prob. 22)*
Estimate the d–d fusion energy in an 8 oz glass of water. How long could it run a
house drawing 10 kW?
*Check:* $2.37\times10^{21}$ deuterons, $4.53\times10^{9}$ J, 5.2 days.

**Solution.** 8 fl oz ≈ 237 mL ≈ 237 g of water. Hydrogen atoms:
$$N_H=\frac{237}{18.015}\times2\times6.022\times10^{23}=1.58\times10^{25}.$$
At S&F's quoted deuterium abundance of 0.015%,
$N_D=2.37\times10^{21}$ deuterons.

Burning deuterium all the way to ⁴He releases 23.85 MeV per *pair* (Example 6.6),
so 11.9 MeV per deuteron:
$$E=2.37\times10^{21}\times11.9\ \text{MeV}\times1.602\times10^{-13}\ \frac{\text{J}}{\text{MeV}}
=\boxed{4.53\times10^{9}\ \text{J}},$$
which at 10 kW is $4.53\times10^{5}$ s = **5.2 days**.

Put the other way: the deuterium in a glass of water is worth about 150 litres of
petrol, and it costs nothing to obtain. It is worth being clear about what this
does and does not show. It shows the *fuel* is free and effectively infinite. It
says nothing about whether the energy can be extracted, which is §3 and §4 of the
notes and the whole of `~NE-24`.

### P2.  The sun, from three angles  *(S&F Ch. 6, Prob. 23)*
The sun radiates $4\times10^{26}$ W. Find (a) the rate at which mass is converted
to energy, (b) the ⁴He production rate, (c) the flux at the earth,
$1.5\times10^{11}$ m away.
*Check:* (a) $4.45\times10^{9}$ kg/s; (b) $9.34\times10^{37}$ s⁻¹;
(c) 1415 W/m² = 0.1415 W/cm².

**Solution.** (a) $\dot m=P/c^2=4\times10^{26}/(2.998\times10^{8})^2
=4.45\times10^{9}$ kg/s.

Four and a half million tonnes a second sounds terminal and is not: over the
sun's 4.6 Gy life so far that is $6.5\times10^{26}$ kg, or **0.03%** of its
$2\times10^{30}$ kg. (The solar wind carries away considerably more.)

(b) Each ⁴He formed releases 26.73 MeV $=4.28\times10^{-12}$ J, so
$$\dot N=\frac{4\times10^{26}}{4.28\times10^{-12}}=9.34\times10^{37}\ \text{s}^{-1}.$$
Equivalently $6.2\times10^{11}$ kg/s of hydrogen consumed — 140 times the mass
actually converted to energy, since only 0.7% of the rest mass is released.

(c) $$F=\frac{P}{4\pi r^2}=\frac{4\times10^{26}}{4\pi(1.5\times10^{11})^2}
=\boxed{1415\ \text{W/m}^2}.$$
The measured solar constant is 1361 W/m²; the 4% gap is S&F's rounding of the
luminosity to $4\times10^{26}$ W (the accepted value is $3.83\times10^{26}$).

### P3.  A supernova against a stellar lifetime  *(S&F Ch. 6, Prob. 24)*
The sun has a lifetime of about $10^{10}$ y. Compare its total energy output with
what a Type Ia supernova releases in a few seconds.
*Check:* $1.26\times10^{44}$ J against $1$–$2\times10^{44}$ J — comparable.

**Solution.** $$E_\odot=4\times10^{26}\ \text{W}\times10^{10}\ \text{y}
\times3.156\times10^{7}\ \frac{\text{s}}{\text{y}}=1.26\times10^{44}\ \text{J}.$$
S&F quote $1$–$2\times10^{44}$ J for a Type Ia (printed 169–170), so the ratio is
0.8 to 1.6: **a supernova releases, in seconds, what the sun takes ten billion
years to radiate.**

That is why one is visible across a galaxy. S&F note the light curve peaks 60
days after collapse at five billion times solar brightness, powered by
$$^{56}\text{Ni}\xrightarrow{6.08\ \text{d}}{}^{56}\text{Co}
\xrightarrow{77.2\ \text{d}}{}^{56}\text{Fe},$$
which is a two-step decay chain of exactly the `~NE-07` kind — the 60-day peak is
the daughter maximum, set by the two half-lives. And the standardisable
brightness that follows from a fixed ⁵⁶Ni mass is what makes Type Ia supernovae
the distance ladder that revealed cosmic acceleration.

Note also the accounting S&F give: **over 90%** of a Type Ia's energy is kinetic
energy of ejecta, ~7% goes to neutrinos, and **less than 1% to visible light**.
The brightest events in the universe are radiating a rounding error.

### P4.  Everything is fusion  *(S&F Ch. 6, Prob. 25)*
Explain how hydroelectric, wind, coal and nuclear power are all indirect
manifestations of stellar fusion.

**Solution.** Trace each back.

**Hydroelectric.** Solar radiation evaporates water and lifts it; it rains at
altitude and runs downhill through turbines. The energy is the gravitational
potential the sun paid for. Fusion, one step removed.

**Wind.** Differential solar heating of the atmosphere and surface drives
pressure gradients. Fusion, one step removed.

**Coal.** Photosynthesis fixed solar energy into carbohydrate in Carboniferous
plants ~300 My ago; burial and heat concentrated it. Fusion, stored for 300
million years — and the chemical bond energy is ~4 eV per atom against fusion's
17.6 MeV per event, so a great deal of sunlight was needed to make a little coal.

**Nuclear fission.** This one is different, and it is the interesting case,
because the energy is *not* from our sun. Uranium is not made by fusion at all —
§6 of the notes shows fusion stops at the iron peak. ²³⁵U and ²³⁸U were built by
**r-process neutron capture** in a supernova (or a neutron-star merger) before
the solar system formed, and the energy stored in them is the gravitational
binding energy of a collapsing stellar core, injected uphill against the
binding-energy curve. So fission is powered by *stellar death* rather than
stellar burning — the ashes of an explosion that predates the sun.

The exceptions worth naming: **geothermal** is mostly the decay heat of ⁴⁰K, ²³²Th
and ²³⁸U in the mantle (also r-process products, plus some primordial accretion
heat), and **tidal** power comes from the earth–moon angular momentum, which is
not fusion at all. So "everything is fusion" is nearly true, and the two
exceptions are both nuclear anyway.

### P5.  Why not D–³He?  *(added)*
D + ³He → ⁴He + p releases **more** energy than D–T (18.35 vs 17.59 MeV) and its
products are both charged, so no neutrons, no activation and direct energy
conversion become possible. Why does no experiment use it?
*Check:* $E_G=4.70$ MeV against D–T's 1.18; at 31 keV the tunnelling probability
is 470 times smaller.

**Solution.** The Q-value is a red herring; the Gamow energy decides.
$$E_G=2\mu c^2(\pi\alpha Z_1Z_2)^2.$$
D–T has $Z_1Z_2=1$ and $\mu=1.2$ u; D–³He has $Z_1Z_2=2$ and $\mu=1.2$ u. The
charge product doubles, so $E_G$ quadruples: 1.175 → 4.700 MeV.

That factor of 4 sits inside $\exp(-\sqrt{E_G/E})$. At $E=31$ keV,
$$\frac{P(\text{D–}^3\text{He})}{P(\text{D–T})}
=\frac{e^{-\sqrt{4.700/0.031}}}{e^{-\sqrt{1.175/0.031}}}
=e^{-12.31+6.16}=2.1\times10^{-3},$$
a factor of 470. Equivalently the Gamow peak moves from 31 to 49 keV, so a
D–³He plasma must run several times hotter to reach comparable rates — and higher
temperature makes confinement harder, radiative losses worse, and the whole
engineering problem sharper.

There is a second problem, which is `~NE-23`'s: **there is essentially no ³He on
earth**. It exists in the lunar regolith at parts-per-billion and in the solar
wind, which is why lunar ³He mining keeps reappearing in speculative energy
plans. D–T needs only lithium, which is a commodity.

The general lesson: **for fusion fuels, $Q$ ranks the prize and $E_G$ ranks the
difficulty, and $E_G$ wins.** p–¹¹B makes the point emphatically: $Q=8.68$ MeV,
fully aneutronic, and $E_G=22.4$ MeV — $10^{16}$ times less likely to tunnel than
D–T at the same energy.

### P6.  The ⁸Be gap  *(added)*
Show that two alpha particles cannot simply fuse, and explain how the universe
makes carbon anyway.
*Check:* $Q(2\alpha\to{}^{8}\text{Be})=-0.092$ MeV;
$Q(3\alpha\to{}^{12}\text{C})=+7.27$ MeV.

**Solution.** From Appendix B,
$$Q=\left[2M(^{4}\text{He})-M(^{8}\text{Be})\right]c^2=-0.0918\ \text{MeV}.$$
**⁸Be is unbound** — barely, by 92 keV, but decisively: it falls apart into two
alphas with a half-life of $7\times10^{-17}$ s. There is no stable nuclide at
$A=8$ at all, and this is a genuine gap in the mass table.

So the alpha-capture ladder cannot start. And yet carbon exists. The resolution
(Hoyle, 1954) is that at the densities and temperatures of a helium-burning core,
$7\times10^{-17}$ s is *long enough*: a small equilibrium population of ⁸Be
persists, and a third alpha can be captured before it decays:
$$3({}^{4}\text{He})\to{}^{12}\text{C},\qquad Q=+7.27\ \text{MeV}.$$

Even that is too slow unless the reaction is **resonant** — which is why Hoyle
predicted, purely from the fact that carbon exists, that ¹²C must have an excited
state near 7.65 MeV. It was found. (`~NE-04` computes the Q-value for reaching
that state; it appears there as the level that closes the ⁹Be(α,n) channel.)

The three-body requirement makes the triple-alpha rate scale as the *square* of
the helium density and as roughly $T^{40}$ near $10^{8}$ K — one of the most
violently temperature-sensitive reactions in nature, and the reason the onset of
helium burning in a degenerate core is explosive (the helium flash).

### P7.  How hot would a classical plasma have to be?  *(added)*
Compare the temperature at which $3kT/2$ equals the D–T Coulomb barrier with the
sun's core and with a tokamak.
*Check:* $3.4\times10^{9}$ K, against 15 MK and ~150 MK.

**Solution.** From `~NE-08`,
$$E_C=1.20\frac{Z_1Z_2}{A_1^{1/3}+A_2^{1/3}}
=\frac{1.20}{2^{1/3}+3^{1/3}}=0.44\ \text{MeV},$$
and setting $3kT/2=E_C$ with $k=8.617\times10^{-11}$ MeV/K gives
$$T=\frac{2\times0.44}{3\times8.617\times10^{-11}}=3.4\times10^{9}\ \text{K}.$$

Against this: the sun's core is $1.5\times10^{7}$ K, a factor of **230** too cold.
ITER aims at roughly $1.5\times10^{8}$ K, still a factor of **23** too cold.

If the classical picture were right, neither would burn. Both do, and the reason
is entirely tunnelling: the Gamow peak sits at 31 keV rather than 440 keV, and it
is populated by the Maxwellian tail. Quantum mechanics is not a correction here —
it is the difference between a universe with stars and one without.

### P8.  Why the sun is not an encouraging precedent  *(added)*
Compute the power density of the sun's core and compare it with a fission reactor
core and with a compost heap.
*Check:* 283 W/m³, against ~$10^{8}$ W/m³ for a PWR core.

**Solution.** S&F give the energy-producing core as 0.1% of the sun's volume.
With $R_\odot=6.96\times10^{8}$ m,
$$V_{\text{core}}=0.001\times\tfrac43\pi R_\odot^3=1.41\times10^{24}\ \text{m}^3,
\qquad
\frac{P}{V}=\frac{4\times10^{26}}{1.41\times10^{24}}=\boxed{283\ \text{W/m}^3}.$$

A compost heap runs at a few hundred W/m³. A human body, at 100 W in 0.07 m³,
manages 1400 W/m³ — **five times the sun's core**. A PWR core producing 3 GW
thermal in ~30 m³ runs at $10^{8}$ W/m³, a factor of 350,000 above the sun.

The sun is luminous because it is $1.4\times10^{27}$ m³ of very feeble reactor,
held together for free by its own weight for ten billion years. This is why the
argument "fusion obviously works, look up" is misleading: a terrestrial reactor
gets none of the sun's advantages (no free confinement, no ten-billion-year
timescale, no room to be a million kilometres across) and must beat its power
density by five or six orders of magnitude to be worth building.

*(A caution on the arithmetic: S&F write that the core is "about 7,000 km in
radius or about 0.1% of the sun's total volume", and those two statements differ
by a factor of 1000 in volume — 0.1% needs 69,600 km. The volume fraction is the
consistent half, as it gives the accepted 283 W/m³; see `../refs.md`.)*
