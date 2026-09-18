# NE-24 — Fusion reactors: Lawson, the triple product, MCF and ICF (notes)

`~NE-10` showed that fusion releases more energy per nucleon than fission. This
module is about why that has not yet been useful, and the answer is **three
compounding difficulties**, each of which the chapter quantifies.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed.,
§§12.1–12.4, cited by **printed** page (PDF = printed + 23).

## 1. You must make a plasma

The Saha equation [Eq. (12.1)]
$$\frac{f^2}{1-f}=\frac1n\left(\frac{2\pi m_ekT}{h^2}\right)^{3/2}e^{-I/kT}$$
has $I/kT$ in an exponential, and that makes the transition brutally abrupt: at
2×10²¹ m⁻³ the ionised fraction runs 10⁻¹¹⁶ at room temperature, 10⁻⁴ at 5000 K,
and essentially 1 by 20 000 K.

**There is no intermediate regime to work in.** You are in a plasma or nowhere
near one, and everything downstream — confinement, heating, diagnostics — assumes
you are already there.

## 2. It radiates faster than it burns, until it doesn't

A plasma bleeds energy as bremsstrahlung [Eq. (12.6)]:
$$P_{\rm rad}=1.42\times10^{-34}Z^2n_in_e\sqrt{T}\ \ \text{W cm}^{-3}\ (T\text{ in K}).$$

Both this and the fusion power [Eq. (12.5)] go as $n^2$, so **the density cancels
and the crossing point depends only on the fuel**. That crossing is the *critical
ignition temperature*:

| | ignition |
|---|---|
| D-T | 3.1 × 10⁷ K (2.7 keV) |
| D-D | 5.3 × 10⁸ K (46 keV) |

against S&F's Fig. 12.2 values of 3 × 10⁷ and 6 × 10⁸ — 4% and 12% agreement.

**A factor of seventeen.** That gap is the whole reason every serious experiment
burns tritium, despite tritium being radioactive (12.3 y), essentially absent from
nature, and impossible to stockpile.

Note the $Z^2$. A percent of tungsten sputtered off the wall radiates like 5000
hydrogens, which is why plasma-facing materials are a first-order physics problem
and not an engineering detail.

## 3. You must hold it long enough

Lawson's argument [Eqs. (12.8)–(12.10)]: the charged fusion products must supply
at least the energy the plasma loses, so with $\tau_E=3nkT/P_{\rm loss}$,
$$n\tau_E\ \ge\ \frac{12kT}{E_c\langle\sigma v\rangle}\quad\text{(D-T)},
\qquad \frac{6kT}{E_c\langle\sigma v\rangle}\quad\text{(D-D)}.$$

The prefactors differ by exactly two because D-D's reactants are **identical** —
S&F's footnotes 1 and 4 exist because that factor is easy to lose, and the module
tests that the two prefactors stand in the ratio 2.

The modern figure of merit is the **triple product** [Eq. (12.11)]
$$n\tau_ET\ \ge\ \frac{12kT^2}{E_c\langle\sigma v\rangle}$$
because it is nearly independent of density and only weakly dependent on
temperature [Eq. (12.13), $\propto T^{-1/3}$]. Over a factor of three in
temperature around its optimum it moves by under 35%, while $n\tau_E$ itself moves
by a factor of two. **So the triple product measures the confinement scheme, not
the operating point** — which is exactly what you want when comparing a tokamak
with a stellarator.

Its D-T minimum is ~3 × 10¹⁵ keV s cm⁻³ near 15 keV, consistent with S&F's stated
$>2\times10^{15}$ [Eq. (12.14)].

## 4. And then Q = 1 is not the goal

The gain factor [Eq. (12.7)]
$$Q=\frac{P_{\rm fus}}{P_{\rm heat}}=\frac{1}{\eta_{\rm heat}f_{\rm recirc}\eta_{\rm elect}(1-f_c)}$$
gives $Q\approx20$ with S&F's own assumptions (0.7, 0.25, 0.35, 0.2).

**"Break-even" is a milestone, not a destination.** At $Q=1$ the alphas supply
only $3.5/17.6=20\%$ of the plasma heating; a *power plant* must also pay for
converting heat to electricity (~35%) and recirculating a quarter of it. Ignition
— $Q=\infty$ — needs the alphas to supply *all* the heating, a further fivefold
step.

And 80% of D-T's energy leaves as a 14.1 MeV neutron. That single fact is
simultaneously the blanket problem, the tritium-breeding opportunity (lithium
capture regenerates the fuel), and the materials-damage problem.

## 5. Two ways to satisfy Lawson

**Magnetic confinement** takes the $\tau$ route: $n\sim10^{14}$ cm⁻³ and
$\tau_E\sim1$ s. ITER — agreed 2005, construction begun 2013 at Cadarache,
23 000 tonnes, and explicitly *not* an electricity producer — is the first machine
intended to exceed break-even.

**Inertial confinement** takes the $n$ route, because it has no choice.
Eq. (12.15) gives $\tau_E=R\sqrt{m/kT}$, and a millimetre pellet at 10 keV is
confined for **0.8 nanoseconds** — eight orders of magnitude less than a tokamak.
So the density must make up all of it.

Quantitatively: burning a third of the fuel needs an areal density
$\rho R\approx2.6$ g/cm², against ~0.02 for an uncompressed pellet. **A factor of
130 in $\rho R$, i.e. a thousandfold in volume density** — denser than lead, from a
target the size of a peppercorn, in a nanosecond, symmetrically. That is the
entire engineering problem in one number.

## Where this goes

- `~NE-10` — the Gamow peak and stellar burning; why D-T is the easy reaction.
- `~NE-25` — direct conversion, which fusion would also want.
- `~NE-22` — the fission plant whose 34% efficiency fusion must eventually beat.
- `~PK-01`, `~PK-02` — plasma physics proper: confinement, instabilities, transport.
- `~NE-13` — the 14.1 MeV neutron's interactions, which set the blanket design.

## A note on this module's finding, and what it adds

**The correction.** §12.1.1 states the hydrogen ionisation energy as **13.06 eV**.
The accepted value is **13.598 eV** — 13.06 reads as a transposed 13.60. What
makes it more than a typo is that the book's *worked example* (95% ionised at
13 150 K, n = 2 × 10²¹ m⁻³) reproduces to four figures only with 13.06; the
correct value gives 92.4%. The example is internally consistent with the wrong
constant.

**What the module adds.** S&F give Fig. 12.1 as a *graph* and no formula, so
every number in §§12.2–12.3 depends on reading it off. The module supplies fits
for $\langle\sigma v\rangle$ and validates them against the book's own Fig. 12.2
ignition temperatures — a check that exercises the fits, the bremsstrahlung
coefficient and the identical-particle factors simultaneously. The D-D fit
**refuses above 100 keV** and is documented as untrustworthy above 25, which
matters because D-D ignition at 46 keV lies in that degraded band.

Also added: the ICF burn-fraction relation $\phi=\rho R/(\rho R+H_B)$, which turns
§12.3's "only a small portion of the pellet fuel actually fuses" into the factor
of 1000 in compression that the whole approach rests on.

**A garbled sentence, recorded not corrected.** §12.2.6 reads "the estimated
construction cost by the end of **1015** has more than tripled and the completion
date has slipped to **2015** at the earliest" — against a stated original
completion date of 2016. Both years are evidently wrong (2015, and a date after
2016); the intended sense is clear and the numbers are not recoverable from the
text.
