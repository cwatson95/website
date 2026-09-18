# NE-15 — Problems

Work each by hand, then check with `code/detectors.py`. Citations in `../refs.md`;
**S&F** = Shultis & Faw 3rd ed., cited by printed page. P1–P6 follow the book's
Chapter 8 problems 1, 3, 4, 5, 6, 8 and 9 (printed 268–269); P7 is added.
Chapter 8 problems 2 and 7 are counting statistics and belong to `~NE-16`.

### P1.  Three changes to a proportional counter  *(S&F Ch. 8, Prob. 1)*
What happens if (a) the anode wire diameter increases, (b) the fill-gas pressure
increases, (c) the wall's atomic number increases?

**Solution.** All three act through Eq. (8.7), $M=f/(1-\delta f)$, but by
different routes.

**(a) Thicker anode wire → *less* gas gain.** The field near a cylindrical anode
is $E(r)=V/[r\ln(b/a)]$ [S&F Eq. (8.2)], so a larger anode radius $a$ *lowers*
the peak field at the wire surface. Avalanche multiplication happens only within
a few wire radii, where the field exceeds the ionization threshold, so a thicker
wire means a smaller $f$ and a much smaller $M$. Proportional counters use very
fine wires (25 μm is typical) for exactly this reason.

**(b) Higher pressure → *less* gain at fixed voltage, but more stopping power.**
More gas means shorter mean free paths between ionizing collisions, so an
electron gains less energy between collisions and multiplies less — $f$ falls, and
the voltage must be raised to compensate. The compensating benefit is that a
denser gas stops more radiation, raising *efficiency*. Pressure trades gain for
efficiency.

**(c) Higher wall $Z$ → more efficiency for photons, and a harder wall effect.**
By `~NE-12`'s $Z^4$, a high-$Z$ wall photo-absorbs far more strongly, and the
photoelectrons it emits enter the gas and are counted. That raises gamma
efficiency substantially — gas alone is nearly transparent to MeV photons. The
cost is that the response now depends on the wall material rather than the gas,
which spoils the detector as a tissue-equivalent dosimeter.

### P2.  Waiting for the light  *(S&F Ch. 8, Prob. 3)*
NaI(Tl) fluorescence has a mean lifetime of 230 ns. How long to collect 90% of
the photons?
*Check:* 530 ns.

**Solution.** Scintillation light decays exponentially, so the fraction collected
by time $t$ is $1-e^{-t/\tau}$ — the same mathematics as `~NE-06`, with $\tau$ in
place of the mean life:
$$t=-\tau\ln(1-0.90)=230\times\ln10=\boxed{530\ \text{ns}}.$$

For reference: 50% arrives in 159 ns, 99% takes 1.06 μs.

This is why NaI is a *slow* scintillator. A counting system must integrate for
roughly 500 ns per event to capture the charge, which sets a floor on the pulse
pair resolving time and hence on the achievable count rate (`~NE-16`'s dead
time). LaBr₃(Ce), at 16 ns, needs only 37 ns for the same 90% — and that is why
it, not NaI, goes into time-of-flight PET (`~NE-27`).

### P3.  Scintillation efficiency of anthracene  *(S&F Ch. 8, Prob. 4)*
1 MeV deposited in anthracene produces 20 000 photons at 447 nm. What is the
scintillation efficiency?
*Check:* 5.5%.

**Solution.** Each photon carries
$$E_\gamma=\frac{hc}{\lambda}=\frac{1239.84\ \text{eV·nm}}{447\ \text{nm}}=2.774\ \text{eV},$$
so the light energy is $20\,000\times2.774=55\,500$ eV and
$$\eta=\frac{55\,500}{10^6}=\boxed{5.5\%}.$$

**94.5% of the deposited energy never becomes light at all** — it ends as lattice
vibrations. That is typical: even NaI(Tl), one of the best, manages only ~11%
(38 000 photons at 415 nm). LaBr₃(Ce) reaches ~21%.

Equivalently, anthracene costs $w=50$ eV per *photon* — and after collection and
photocathode conversion, several hundred eV per *photoelectron*. Set that against
germanium's 2.98 eV and §1 of the notes needs no further argument.

### P4.  Air in an ion chamber but not a proportional counter  *(S&F Ch. 8, Prob. 5)*
Why?

**Solution.** An ion chamber only has to **collect** the primary charge; a
proportional counter has to **multiply** it, and multiplication is fragile.

Air contains ~21% O₂, and oxygen is strongly **electronegative**: it captures
drifting free electrons to form O₂⁻. A negative molecular ion is thousands of
times heavier than an electron, drifts thousands of times more slowly, and — the
fatal part — **cannot be accelerated to ionizing energies in the avalanche
region.** Every electron captured is an electron removed from the multiplication
chain, so $f$ becomes erratic and $M$ loses any stable relation to the deposited
energy. Proportionality is destroyed.

In an ion chamber none of this matters much: the negative ion still carries its
charge to the electrode, just more slowly, and the *total* collected charge is
unchanged. Slow collection is tolerable because ion chambers are usually operated
in current mode over long integration times.

Hence proportional counters use scrupulously electronegative-free fills — P-10
(90% Ar, 10% methane), pure argon, BF₃, ³He — while ion chambers can be open to
the atmosphere, which is a great convenience for a survey instrument that must be
tissue-equivalent anyway.

### P5.  FWHM from a quoted resolution  *(S&F Ch. 8, Prob. 6)*
A NaI(Tl) detector has 8% energy resolution. What is the FWHM for ¹³⁷Cs?
*Check:* 53 keV.

**Solution.** Resolution is *defined* as FWHM/E, so
$$\text{FWHM}=0.08\times662\ \text{keV}=\boxed{53\ \text{keV}},$$
and $\sigma=\text{FWHM}/2.355=22.5$ keV.

Two things follow. Since resolution is quoted at a *stated energy* and scales as
$1/\sqrt E$, "8%" alone is meaningless — the same detector is ~11% at 300 keV and
~5.8% at 1.25 MeV. Always state the line.

And 53 keV is wider than the 159 keV separating ⁶⁰Co's two gammas is large: two
peaks 53 keV wide, 159 keV apart, overlap substantially. This is the calculation
behind `figures/fig4`.

Note the 8% is a *measured* figure. This module's statistical floor for NaI at
662 keV is 3.6%, so about $\sqrt{8^2-3.6^2}=7.1\%$ of the width comes from
elsewhere — chiefly non-proportionality of the light yield with energy, and
non-uniform light collection across the crystal.

### P6.  Choosing a scintillator for the job  *(S&F Ch. 8, Prob. 8)*
Inorganic or organic, for γ rays, fast neutrons, β particles?

**Solution.**

**γ rays → inorganic.** Photon detection needs photoelectric absorption, whose
cross section goes as $Z^4$ (`~NE-12`). NaI ($Z=53$ for iodine), BGO
($Z=83$ for bismuth) and LaBr₃ all contain heavy elements and are dense; organic
scintillators are hydrogen, carbon and oxygen ($Z\le8$) at ~1 g/cm³, and are
nearly transparent to MeV gammas. Inorganics also give more light, hence better
resolution — and for gammas one usually wants a *spectrum*, not just a count.

**Fast neutrons → organic.** Detection proceeds by elastic scattering off nuclei
and then detecting the recoil (`~NE-08`). The recoil energy fraction is
$1-\alpha=4A/(A+1)^2$, which is **1.0 for hydrogen** and falls off fast — so a
hydrogen-rich medium is required, and organics are ~50% hydrogen by atom count.
A heavy inorganic barely transfers any energy to its recoils. Organics also allow
**pulse-shape discrimination**: proton recoils and electrons produce different
decay-time profiles, letting a neutron signal be separated from a gamma
background. EJ-301/BC-501A exists for exactly this.

**β particles → organic, usually plastic.** Betas are stopped in millimetres
(`~NE-14`), so density is not needed; low $Z$ is actively *wanted*, because it
minimises the bremsstrahlung that would escape and the backscatter that would
distort the spectrum. Thin plastic sheets are cheap, machinable to any shape, and
can be made large. (For β *spectroscopy* rather than counting, a Si detector does
better.)

### P7.  HPGe against Si(Li)  *(S&F Ch. 8, Prob. 9)*
Why do both exist?

**Solution.** Table 8.2 has the answer in two columns.

**HPGe** — $Z=32$, $\rho=5.33$ g/cm³, $w=2.98$ eV, $E_g=0.72$ eV.
*Advantages:* the smallest $w$ of any practical material, hence the best
resolution available (~0.16% at 1.3 MeV); high $Z$ and density give real
photopeak efficiency at MeV energies. It is **the** gamma spectrometer.
*Disadvantages:* the 0.72 eV band gap means enormous thermal carrier generation
at room temperature, so it **must** be cooled to 77 K — a dewar, or a mechanical
cooler, forever. It is also expensive and physically fragile.

**Si(Li)** — $Z=14$, $\rho=2.33$ g/cm³, $w=3.61$ eV, $E_g=1.12$ eV.
*Advantages:* the larger gap tolerates warmer operation, and the low $Z$ is a
*virtue* for x-ray and charged-particle spectroscopy — less backscatter, and a
photopeak that is not dominated by escape peaks. It excels below ~30 keV, where
silicon's photoelectric cross section is still adequate.
*Disadvantages:* at $Z=14$ it is nearly transparent to MeV gammas, so photopeak
efficiency collapses above a few hundred keV.

**They do not compete; they cover different energies.** Si(Li) for x-rays and
low-energy photons, HPGe for gamma spectroscopy. The choice is set by `~NE-12`'s
$Z$ dependence, not by anything in the detector physics of this chapter.
