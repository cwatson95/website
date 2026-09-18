# NE-15 — Radiation detectors: gas-filled, scintillation, semiconductor (notes)

S&F open Chapter 8 by saying a detector must do three things: **absorb** the
radiation, produce an **observable phenomenon**, and provide a way to **measure**
it. `~NE-12` and `~NE-14` supplied the first — a detector that does not stop the
particle cannot see it, and the mean free paths and ranges there set how big and
how dense it must be. This module is the second and third.

One quantity organises everything: the **number of information carriers** per
event.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed.,
§§8.1–8.5, cited by **printed** page (PDF = printed + 23). Tables 8.1 and 8.2
are transcribed into `code/detectors.py`.

## 1. Why the carrier count is everything

Deposit energy $E$ in a medium that costs $w$ per carrier (ion pair, electron–hole
pair, photoelectron) and you get
$$N=\frac{E}{w}.$$
That count fluctuates, and the fluctuation is **irreducible** — it is the signal,
not noise added to it. With Gaussian statistics (S&F §8.6.2, and `~NE-16`) the
peak width is
$$\boxed{\;\frac{\text{FWHM}}{E}=2.355\sqrt{\frac{F}{N}}\;}$$
where $F$ is the Fano factor (§4 below).

So resolution improves as $1/\sqrt N$, **and the only lever is $w$.** The entire
history of detector development is a race to make $w$ small:

| detector | $w$ (eV per usable carrier) | carriers at 662 keV | intrinsic FWHM |
|---|---|---|---|
| Ge semiconductor | 2.98 | 222 000 | **0.18%** |
| Si semiconductor | 3.61 | 183 000 | 0.19% |
| Ar gas | 26.4 | 25 000 | 0.67% |
| LaBr₃(Ce) scintillator | ~91 | 7 300 | 2.8% |
| NaI(Tl) scintillator | ~150 | 4 400 | 3.6% |
| BGO scintillator | ~700 | 950 | 7.6% |

Germanium beats sodium iodide by a factor of twenty on resolution, and the reason
is entirely the first column. That is why people put up with liquid nitrogen.

**These are lower bounds, not predictions.** Real detectors add electronic noise,
incomplete charge collection, and — for scintillators — non-proportionality and
light-collection non-uniformity, all adding in quadrature. A real NaI(Tl)
achieves ~6.5% at 662 keV against the 3.6% floor, so *half* the observed width is
not carrier statistics. A real germanium detector achieves ~1.4 keV against a
1.2 keV floor: it nearly attains its limit, which is a statement about how good
the technology is.

## 2. Gas-filled detectors: one equation, four instruments

Radiation ionizes the fill gas; a field sweeps the charge to electrodes. What
happens next depends entirely on the applied voltage, and S&F's Eqs. (8.6)–(8.7)
capture the whole story. If each avalanche multiplies by $f$ and has probability
$\delta$ of triggering another,
$$M=f+\delta f^2+\delta^2f^3+\cdots=\frac{f}{1-\delta f}.$$

The geometric series converges only for $\delta f<1$. The regimes are:

- **Ion chamber** ($M\simeq1$): collect the primary ionization, no gain. Output
  proportional to energy, small signal, used for high dose rates.
- **Proportional counter** ($M\sim10^2$–$10^4$): gas gain, still proportional.
  The workhorse for x-ray spectroscopy and neutron counting (BF₃, ³He — `~NE-13`).
- **Limited proportional**: space charge from slow positive ions begins to
  distort the field; proportionality degrades.
- **Geiger–Müller** ($\delta f\to1$): the avalanche becomes **self-sustaining**,
  propagated along the whole anode by UV photons. Every pulse is the same size
  regardless of the deposited energy — **all spectroscopic information is lost**,
  in exchange for a huge, easy-to-count pulse.

The divergence of Eq. (8.7) at $\delta f=1$ is not a mathematical artefact; *it
is the transition between two instruments*. `gas_multiplication` raises there
rather than returning a negative number.

Note also how steeply $M$ rises near the limit: going from $\delta f=0.8$ to
$0.9$ doubles the gain, and $0.9$ to $0.99$ multiplies it tenfold. Proportional
counters therefore need very stable high-voltage supplies — a 1% drift in voltage
can be a 10% drift in gain.

## 3. Scintillators: the photon count is not the carrier count

A scintillator converts energy to light; a photomultiplier converts light to
photoelectrons and multiplies them. The chain is lossy at every step, and
**the smallest number along it governs the statistics**:

$$\underbrace{38\,000}_{\text{photons/MeV}}
\xrightarrow{\ \sim70\%\ \text{collected}\ }
\underbrace{26\,600}_{\text{at the photocathode}}
\xrightarrow{\ \sim25\%\ \text{QE}\ }
\underbrace{6\,650}_{\text{photoelectrons}}$$

So NaI(Tl)'s effective $w$ is ~150 eV, not the ~26 eV its light yield alone would
suggest. **Quoting the photon yield as though it set the resolution is a standard
error**, and it is off by a factor of six.

S&F's Table 8.1 rewards reading carefully. Its "relative PMT response" column is
*not* the light yield: CsI(Tl) produces 65 000 photons/MeV — 1.7× NaI's — and
delivers **half** NaI's PMT response, because its 540 nm emission is far off a
bialkali photocathode's blue-sensitive peak. Light that the photocathode cannot
convert is light wasted.

The classical materials trade brightness against speed (CsI(Tl) is brightest and
among the slowest; BGO is dense but dim). The cerium-doped modern materials break
the trade: **LaBr₃(Ce) is brighter than NaI *and* fourteen times faster**, which
is why it has displaced NaI wherever the cost is tolerable. Speed matters for
coincidence timing in PET (`~NE-27`) and for high count rates (`~NE-16`'s dead
time).

Organic scintillators (plastics, liquids) go the other way: nanosecond decay at a
third to a half of anthracene's already-modest light. They are for timing and for
fast-neutron pulse-shape discrimination, not spectroscopy.

## 4. Semiconductors, and the Fano factor

A semiconductor is a solid-state ion chamber: an electron–hole pair costs
$w\simeq3\times$ the band gap (Table 8.2), an order of magnitude less than a gas
ion pair and fifty times less than a scintillator photoelectron. Hence §1.

Table 8.2 lays out the trade-off cleanly. **Small band gap → small $w$ → best
resolution**, but also more thermally generated leakage, which is why germanium
($E_g=0.72$ eV) must be cooled while CdTe ($E_g=1.52$ eV) works at room
temperature. And **high $Z$ and high density → better photon stopping**
(`~NE-12`'s $Z^4$), which is why CdTe and HgI₂ exist despite their worse $w$.
Nobody gets both.

**The Fano factor.** S&F never mention it, and the module adds it, because
without it the arithmetic is wrong by a factor of three. Carrier production is
**sub-Poisson**: the total deposited energy is fixed, so a quantum spent creating
one electron–hole pair is unavailable to create another, and the events are
anti-correlated. The variance is suppressed:
$$\sigma_N^2=FN,\qquad F\simeq0.13\ \text{(Ge)},\ 0.115\ \text{(Si)},\ 1\ \text{(scintillators)}.$$

Using $\sqrt N$ instead of $\sqrt{FN}$ overestimates a germanium photopeak width
by $\sqrt{1/0.13}=2.8$ — the difference between predicting 0.50% and the
correct 0.18%, and between a formula that matches measured detectors and one that
does not. Scintillators get no such suppression, because their photoelectron
count is set by a chain of independent lossy steps rather than by a fixed energy
budget.

## 5. What it looks like

⁶⁰Co emits two gammas 159 keV apart (`~NE-05`). At germanium's 0.16% those are
two clean, fully separated lines. At a realistic NaI 6.5% they merge into a
single bump from which neither energy can be read. `figures/fig4` draws both.

That is what a factor of forty in $w$ buys, and it is the practical content of
this entire module.

## Where this goes

- `~NE-16` — the counting statistics behind §1's $\sqrt N$, plus dead time,
  which limits how fast §2's detectors can be read.
- `~NE-12` — the photopeak, Compton edge, backscatter peak and escape peaks that
  populate a spectrum are that module's three processes seen in a detector.
- `~NE-14` — a detector must stop the particle; ranges set window thickness for
  alphas and betas, and detector depth for electrons.
- `~NE-13` — ¹⁰B and ⁶Li line neutron detectors precisely because of their 1/v
  cross sections and charged reaction products.
- `~NE-17` — dosimeters (film, TLD, OSL, pocket chambers) are detectors optimised
  for integrated dose rather than per-event spectroscopy.
- `~NE-27` — PET demands fast, dense scintillators, which is the §3 trade-off
  driving BGO → LSO → LaBr₃.
