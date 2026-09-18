# NE-12 — Problems

Work each by hand, then check with `code/photon_interactions.py`. Citations in
`../refs.md`; **S&F** = Shultis & Faw 3rd ed., cited by printed page. P1–P3
follow the book's Chapter 7 problems 12, 14 and 15 (printed 219); P4–P8 are
added. Coefficients from `../data_tables/C3_photon_coefficients_*.csv`.

### P1.  Interactions and positrons in water  *(S&F Ch. 7, Prob. 12)*
A beam of 3 MeV photons with intensity $10^8$ cm⁻² s⁻¹ irradiates water.
(a) How many photon–water interactions occur per second per cm³? (b) How many
positrons are produced?
*Check:* (a) $3.97\times10^{6}$; (b) $1.13\times10^{5}$.

**Solution.** This is `~NE-11`'s $R=\mu\phi$ with the right subscript.

(a) $\mu(3\ \text{MeV, water})=0.03968$ cm⁻¹, so
$$R=\mu\phi=0.03968\times10^{8}=\boxed{3.97\times10^{6}\ \text{cm}^{-3}\text{s}^{-1}}.$$

(b) One positron per pair-production event, and
$\mu_{pp}=0.001131$ cm⁻¹:
$$R_{pp}=\boxed{1.13\times10^{5}\ \text{cm}^{-3}\text{s}^{-1}},$$
which is only **2.85%** of all interactions. At 3 MeV in water, Compton
scattering still does 97% of the work — pair production has been open since
1.022 MeV but is still feeble, because water is low-$Z$ and the cross section
goes as $Z^2$. In lead at the same energy the pair fraction is nearly ten times
larger.

Each of those $1.13\times10^{5}$ positrons then annihilates, producing
$2.26\times10^{5}$ photons per cm³ per second at exactly 0.511 MeV. A "3 MeV
beam" therefore generates a 511 keV field wherever it goes, which no
uncollided-flux calculation would ever show.

### P2.  A ⁶⁰Co source in a water tank  *(S&F Ch. 7, Prob. 14)*
A 2 mCi ⁶⁰Co source sits at the centre of a water-filled iron tank, inside
diameter 20 cm, wall thickness 1 cm. Find the uncollided flux density at the
outer surface nearest the source.
*Check:* $3.40\times10^{4}$ cm⁻² s⁻¹.

**Solution.** ⁶⁰Co emits **two** gammas per decay, 1.1732 and 1.3325 MeV
(`~NE-05`), so treat them separately and add. Each has source strength
$S=2\times10^{-3}\times3.7\times10^{10}=7.40\times10^{7}$ s⁻¹.

The path from centre to outer surface is 10 cm of water plus 1 cm of iron, so
$r=11$ cm, and Eq. (7.27) gives
$$\phi^o=\frac{S}{4\pi r^2}\exp\!\left[-(\mu_{H_2O}t_{H_2O}+\mu_{Fe}t_{Fe})\right].$$

| $E$ (MeV) | $\mu_{H_2O}$ | $\mu_{Fe}$ | optical thickness | $\phi^o$ |
|---|---|---|---|---|
| 1.1732 | 0.06524 | 0.43257 | 1.085 | $1.64\times10^{4}$ |
| 1.3325 | 0.06114 | 0.40601 | 1.017 | $1.76\times10^{4}$ |
| | | | **total** | $\boxed{3.40\times10^{4}}$ |

Two things worth noticing. The 1 cm of iron contributes 0.43 mean free paths
against the 10 cm of water's 0.65 — **a centimetre of iron is worth seven
centimetres of water**, which is the density argument of `~NE-11` P2 in
miniature. And the total optical thickness is only about 1 mfp, so this is
exactly the regime where the buildup factor is *not* negligible: the true flux at
that surface is perhaps twice the uncollided value computed here.

### P3.  Maximum Compton transfer at three energies  *(S&F Ch. 7, Prob. 15)*
Find the maximum Compton-electron energy and the corresponding minimum scattered
photon energy for (a) 100 keV, (b) 1 MeV, (c) 10 MeV photons.
*Check:* (a) 28.1 / 71.9 keV; (b) 796.5 / 203.5 keV; (c) 9750.9 / 249.1 keV.

**Solution.** Both at $\theta_s=180°$:
$$E_{\max}=E\frac{2E}{m_ec^2+2E},\qquad E'_{\min}=\frac{E}{1+2E/m_ec^2}.$$

| $E$ | $E_{\max}$ (edge) | $E'_{\min}$ (backscatter) | fraction transferred |
|---|---|---|---|
| 100 keV | 28.1 keV | 71.9 keV | 28% |
| 1 MeV | 796.5 keV | 203.5 keV | 80% |
| 10 MeV | 9750.9 keV | 249.1 keV | 97.5% |

The trend is the point. At 100 keV a *head-on* Compton collision — the most
violent available — still leaves 72% of the energy in the photon. At 10 MeV it
takes 97.5%. **Compton scattering is a poor absorber at low energy and an
efficient one at high energy**, and the backscattered photon converges on
$m_ec^2/2=255$ keV from below in every case.

This is also why the deposited fraction $f=\mu_{en}/\mu$ has a *minimum* in the
Compton region rather than falling monotonically: at low energy the
photoelectric effect absorbs outright, at high energy Compton transfers nearly
everything, and in between neither does.

### P4.  Why lead is two different shields  *(added)*
Compare lead and water per gram at 100 keV and at 1 MeV, and explain the
difference.
*Check:* photoelectric ratio 1896 at 100 keV; total ratio 0.963 at 1 MeV.

**Solution.** Per gram, from Appendix C.3:

| | 100 keV | 1 MeV |
|---|---|---|
| $(\mu_{ph}/\rho)_{Pb}/(\mu_{ph}/\rho)_{H_2O}$ | **1896** | 4916 |
| $(\mu/\rho)_{Pb}/(\mu/\rho)_{H_2O}$ | **32.3** | **0.963** |

At 1 MeV lead is, per gram, *very slightly worse than water*. All of its
reputation comes from being 11.35 times denser.

The reason is the $Z$ exponents. At 1 MeV essentially every interaction is
Compton, whose cross section per gram is $(N_A Z/A)\sigma_{KN}$ — and
$Z/A\simeq0.5$ for nearly everything, so per gram all materials are equivalent.
Lead's $Z/A=0.396$ is actually the *worst* of the five tabulated materials,
because heavy nuclei are neutron-rich (`~NE-02`) and neutrons contribute mass
without contributing electrons.

At 100 keV the photoelectric effect is available, its cross section goes as
$Z^4$, and lead's $Z=82$ against water's effective $\simeq7.4$ gives
$(82/7.4)^4\approx1.5\times10^{4}$ — the right order for the observed 1900 once
the $Z^4$ is diluted by $A$ in the per-gram conversion.

**The practical rule:** for x-rays, choose high $Z$; for MeV gammas, choose mass
and take whatever is cheap. Concrete shields reactors not because it is good but
because it is cheap and there can be a lot of it.

### P5.  The K edge and contrast agents  *(added)*
Lead's K edge multiplies $\mu_{ph}$ by 4.7 at 88 keV. Why are iodine ($E_K=33$
keV) and barium ($E_K=37$ keV) used as radiographic contrast agents rather than
lead?
*Check:* diagnostic x-rays run 30–120 keV.

**Solution.** A contrast agent must absorb far more strongly than tissue *at the
energies actually used*. Diagnostic x-ray tubes produce a bremsstrahlung
continuum from ~30 to ~120 keV, peaking well below the endpoint.

An element's photoelectric cross section is largest **just above** its K edge, so
the useful element is one whose edge sits at the *bottom* of the working band —
iodine's 33 keV and barium's 37 keV are ideally placed, giving maximum
absorption across most of the spectrum.

Lead's edge at 88 keV is too high: over most of the diagnostic band lead is
*below* its K edge, where the K shell contributes nothing. Lead would still
absorb well (its L edges are at 13–16 keV and $Z^4$ is enormous), but it is also
toxic and, more to the point, iodine can be made into a water-soluble compound
that circulates in blood. The physics and the chemistry have to agree.

The same edge logic runs backwards for detection: a material with a K edge just
*below* the photon energy of interest makes a good detector, which is part of why
NaI(Tl) (iodine again, $Z=53$) is the workhorse gamma scintillator (`~NE-15`).

### P6.  Klein–Nishina against the table  *(added)*
Verify Eq. (7.34) against Appendix C.3 for water at 1 MeV, then explain the
disagreement for lead at 10 keV.
*Check:* water agrees to 0.1%; lead at 10 keV is 236% high.

**Solution.** For water, $Z/A=0.55509$. Klein–Nishina at 1 MeV gives
$\sigma_{KN}=2.112\times10^{-25}$ cm²/electron, so
$$\frac{\mu_c}{\rho}=N_A\frac{Z}{A}\sigma_{KN}
=6.022\times10^{23}\times0.55509\times2.112\times10^{-25}=0.07060\ \text{cm}^2/\text{g},$$
against the tabulated 0.07066 — **0.1%**.

For lead at 10 keV the same calculation is 236% too high, and this is *expected*.
Klein–Nishina assumes a **free electron at rest**. At 10 keV the recoil energy is
comparable to — indeed below — lead's K binding energy of 88 keV, so the K
electrons cannot recoil freely and simply do not participate. The tabulated
column is the *bound*-electron (incoherent) cross section, which is smaller.

The approximation fails exactly where S&F say it should [§7.3.2], and the failure
is ordered: worse at lower energy, worse at higher $Z$, and negligible once
$E\gtrsim5E_K$. Water is within 1.3% at 100 keV because oxygen's K edge is only
0.54 keV.

Turning this around gives a useful trick: **above a few MeV, where binding is
irrelevant, the tabulated Compton column can be solved for $Z/A$.** Doing so
returns the standard NIST values for air, water, iron and lead to 0.3% — and
reveals that S&F's concrete is ANSI/ANS-6.4.3 standard concrete, not NIST
"ordinary concrete" (see `../refs.md`).

### P7.  Fluorescence escape at the K edge  *(added)*
Just above lead's K edge, $\mu$ jumps by 4.5× but $\mu_{en}$ rises only 1.5×, so
the deposited fraction *falls* from 0.90 to 0.29. Explain.
*Check:* $f=1.482/1.647=0.900$ below, $2.160/7.420=0.291$ above.

**Solution.** Below the edge, absorption is by L-shell electrons; the resulting L
vacancy fills with low-energy emissions that are reabsorbed locally, so nearly
all the energy stays put.

Above the edge, the K shell opens and dominates. But filling a K vacancy in lead
emits a **75–85 keV characteristic x-ray**, and S&F give the K fluorescent yield
as 0.965 at $Z=90$ — so almost every K photoabsorption is followed by a hard
x-ray. That x-ray has a mean free path of centimetres in lead and **escapes**,
taking most of the energy with it.

So crossing the edge upward, lead becomes far better at *stopping* photons and
substantially worse at *absorbing their energy*. More interactions, less
deposition.

Two consequences. In dosimetry, using $\mu$ where $\mu_{en}$ belongs overestimates
dose by a factor of 3 right above the edge. In spectroscopy, the escaping x-ray
produces **escape peaks** — a full-energy peak accompanied by a satellite
displaced downward by the fluorescence energy — which is a routine feature of
germanium and NaI spectra and a routine source of misidentified lines
(`~NE-15`).

### P8.  Why a gamma spectrum looks the way it does  *(added)*
Sketch and explain the features of a ¹³⁷Cs spectrum measured in a small NaI
detector.
*Check:* photopeak 662 keV, Compton edge 477 keV, backscatter peak 184 keV.

**Solution.** Every feature is one of §1–§3 read off an oscilloscope.

- **Photopeak, 662 keV.** Photoelectric absorption of the full-energy photon.
  Requires §1, which is why detectors want high $Z$ — in a low-$Z$ detector this
  peak is weak and the spectrum is nearly useless for identification.
- **Compton continuum, 0 → 477 keV.** The recoil electron is stopped and
  measured, but the scattered photon escapes the small detector. Every scattering
  angle contributes, so the result is a continuum, not a line.
- **Compton edge, 477 keV.** Its sharp upper end, at $\theta_s=180°$. The gap
  between edge and photopeak — 185 keV here — is $E'_{\min}$, the energy the
  backscattered photon necessarily carries away.
- **Backscatter peak, 184 keV.** Photons that Compton-scattered through ~180° in
  the shielding or the source *outside* the detector and then entered it. Same
  kinematics, opposite bookkeeping: here the scattered photon is what gets
  measured.
- **511 keV**, if anything nearby emits positrons (§3), and **x-ray escape
  peaks** displaced by the iodine K fluorescence at ~29 keV (P7).

A large detector suppresses the continuum relative to the photopeak, because a
scattered photon has more chance to interact again before escaping and so still
deposits the full energy. That is the entire argument for building big
germanium detectors, and it is `~NE-15`'s subject.
