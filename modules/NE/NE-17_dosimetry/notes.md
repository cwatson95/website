# NE-17 — Dosimetry: kerma, absorbed dose, equivalent & effective dose (notes)

`~NE-11` and `~NE-12` said how much radiation is there. This module says how much
it matters — and the honest answer takes **four** quantities, not one, each a
correction to the last:

| | | |
|---|---|---|
| **kerma** $K$ | energy handed to charged particles per unit mass | Eq. (9.2) |
| **absorbed dose** $D$ | energy actually deposited per unit mass | Eq. (9.1) |
| **equivalent dose** $H=QF\cdot D$ | weighted by how densely the track deposits it | Eq. (9.10) |
| **effective dose** $E=\sum_T w_T H_T$ | whole-body risk from a partial-body exposure | Eq. (9.12) |

They are not interchangeable, and the gaps between them are the physics.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed.,
§§9.1–9.4, cited by **printed** page (PDF = printed + 23).

## 1. Energy imparted, dose, and kerma

The **absorbed dose** is the limit of mean energy imparted per unit mass
[Eq. (9.1)],
$$D=\lim_{\Delta m\to0}\frac{\Delta\bar\varepsilon}{\Delta m},$$
in grays (1 Gy = 1 J/kg; the old rad is 0.01 Gy). It is the physically
meaningful quantity, and it is awkward to calculate, because "imparted here"
depends on where the secondary electrons went.

**Kerma** sidesteps that [Eq. (9.2)]: it counts the kinetic energy *released* to
charged particles per unit mass at the point of interaction, and never asks where
that energy ends up. It is defined only for uncharged radiation, and it is the
quantity a fluence calculation gives you directly:
$$\boxed{\;K=1.602\times10^{-10}\,E\,\frac{\mu_{tr}}{\rho}\,\Phi\;}\qquad\text{[Eq. (9.5)]}$$
with $E$ in MeV, $\mu_{tr}/\rho$ in cm²/g, $\Phi$ in cm⁻², $K$ in Gy.

**The two agree under charged-particle equilibrium** — for every charged particle
leaving the volume, an identical one enters. Replacing $\mu_{tr}$ by $\mu_{en}$
gives the dose [Eq. (9.6)]:
$$D=1.602\times10^{-10}\,E\,\frac{\mu_{en}}{\rho}\,\Phi.$$

That prefactor is not a physical constant. It is $1.602\times10^{-13}$ J/MeV
times 1000 g/kg, and `test_the_two_prefactors_are_derivable_not_magic` re-derives
it rather than trusting it.

**The residual gap $K>D$ is bremsstrahlung.** $\mu_{tr}$ counts energy handed to
electrons; $\mu_{en}$ subtracts what those electrons radiate back out. In iron at
5 MeV the two are 0.02112 and 0.01983 cm²/g — a **6.5% gap** — so even in perfect
equilibrium the kerma overstates the dose. Below about 1 MeV the gap vanishes and
the words are interchangeable; in a high-Z shield at MeV energies they are not.

## 2. Exposure, and the conversion the book omits

**Exposure** $X$ predates all of this and is still how survey meters are
calibrated. It is charge liberated per unit mass **of air**, and only for photons
[§9.2.5]. One roentgen is exactly $2.58\times10^{-4}$ C/kg. In the same fluence
notation [Eq. (9.9)],
$$X\,(\mathrm{R})=1.835\times10^{-8}\,E\,\frac{\mu_{en}}{\rho}\bigg|_{\rm air}\Phi.$$

Every ingredient of that $1.835\times10^{-8}$ is bookkeeping too, ending with a
division by $W=33.85$ eV per ion pair.

S&F define $D$ and $X$ in adjacent sections and **never connect them**, which is
a gap worth closing, because a survey meter reads in mR/h and a dose limit is
written in mSv:
$$\boxed{\;1\ \mathrm{R}=(2.58\times10^{-4}\ \mathrm{C/kg})(33.85\ \mathrm{J/C})
=8.73\ \mathrm{mGy}\ \text{in air}\;}$$
which is exactly the ratio of the two prefactors — an independent derivation, and
that is how the test checks it. A survey meter reading 10 mR/h is delivering
87 µGy/h to air, and roughly 10% more than that to tissue.

## 3. Neutron kerma

For fast neutrons the energy goes to recoiling nuclei. For isotropic elastic
scattering in the CM frame, the mean fraction transferred is [Eq. (9.7), from
Eq. (6.28)]
$$f_s=\tfrac12(1-\alpha)=\frac{2A}{(A+1)^2},$$
so $K=1.602\times10^{-10}E\,(f_s\mu_s/\rho)\,\Phi$.

This is the *same* algebra that makes light nuclei good moderators in `~NE-13`,
read as a dose statement. The consequence for tissue is stark: in water,
**hydrogen is 11% of the mass and carries 97% of the fast-neutron kerma**
($f_H=0.5$ against $f_O=0.11$, and $\sigma_s^H$ is 3.7× larger). Tissue is a
hydrogen target as far as fast neutrons are concerned.

For slow and thermal neutrons this is simply wrong — the kerma there comes from
capture reactions, chiefly ¹⁴N(n,p)¹⁴C and ¹H(n,γ)²H — and S&F say so without
computing it. `neutron_kerma` documents the restriction rather than extrapolating
past it.

## 4. Quality factor: one gray is not one gray

Equal energy deposited by an alpha particle and by a gamma ray does unequal
biological damage, because the alpha lays its energy down thousands of times more
densely. Radiobiologists measure this as **RBE** [§9.2.6]; radiation protection
replaces RBE with a coarse, prescriptive surrogate, the **quality factor**
[Table 9.1]:

| radiation | QF |
|---|---|
| x, γ, β (any energy) | 1 |
| neutrons < 10 keV | 5 |
| 10–100 keV | 10 |
| **0.1–2 MeV** | **20** |
| 2–20 MeV | 10 |
| > 20 MeV | 5 |
| protons > 2 MeV | 5 (ICRP) / 2 (NCRP) |
| alpha particles | 20 |

$H=QF\times D$ [Eq. (9.10)], in sieverts.

Two things are worth noticing. **The neutron peak sits exactly on the fission
spectrum** — 0.1–2 MeV — so a reactor's neutron field is weighted at the maximum.
And **the span is a factor of twenty**, which is why `quality_factor` refuses an
unrecognised radiation instead of returning 1. A default of 1 is not a
conservative fallback; it is a twentyfold understatement in the two cases where
being wrong is expensive.

## 5. Effective dose: risk arithmetic

Organs differ in radiosensitivity, and a real exposure is never uniform. The
effective dose weights each organ's equivalent dose by a tissue factor
[Eqs. (9.11), (9.12)]:
$$E=\sum_T w_T H_T,\qquad \sum_T w_T=1.$$

The constraint $\sum w_T=1$ is what makes $E$ comparable with a whole-body dose;
without it the whole framework leaks. `effective_dose` therefore **refuses an
organ it cannot weight** — silent omission returns a number that still looks like
an effective dose and is always too *low*, i.e. it errs toward declaring an
exposure safe.

**The weights are a risk estimate, and risk estimates move.** S&F print two sets
(Table 9.2, ICRP 1977; Table 9.3, ICRP 1991); the module carries the current
ICRP-103 (2007) set as well, because the drift is the lesson:

| organ | 1977 | 1991 | 2007 |
|---|---|---|---|
| gonads | 0.25 | 0.20 | **0.08** |
| breast | 0.15 | 0.05 | **0.12** |
| bone marrow | 0.12 | 0.12 | 0.12 |

The gonad weight fell threefold as the hereditary-risk estimate came down
(`~NE-18` §2); the breast weight went down and then back up. An effective dose is
only ever quoted with respect to one vintage of these numbers, and comparing
across vintages without saying so is a real error.

## 6. Internal dose, and the natural yardstick

An ingested nuclide keeps irradiating you after you swallow it, so the meaningful
quantity is the **committed** effective dose equivalent: the whole integral of
what one intake will ever deliver, conventionally truncated at 50 years [§9.3.1].
The ICRP model behind it (§9.3.3) is a compartment model — a transfer
compartment, first-order biological elimination with constant $\lambda_b$
alongside $\lambda_r$ — and the output is Table 9.4, a coefficient in Sv/Bq per
nuclide. Doses from different nuclides simply add.

Table 9.4 is printed twice, in Sv/Bq and rem/Ci, related by exactly
$3.7\times10^{12}$. That redundancy makes the table check itself, and all 68 rows
pass.

Finally, **the yardstick** [Tables 9.5, 9.6]:

| | annual effective dose |
|---|---|
| world average, natural | **2.4 mSv** (range 1–10) |
| U.S. average, natural | 3.0 mSv |
| U.S. man-made | 0.65 mSv (18% of the total) |

**Half the world figure and two thirds of the U.S. figure is inhaled radon.** The
dominant human radiation exposure is a decay product of uranium in soil. Every
number in `~NE-18` is measured against this.

## Where this goes

- `~NE-12` — the $\mu_{tr}$ / $\mu_{en}$ distinction this module spends; the
  Appendix C.3 tables are the same ones.
- `~NE-13` — $f_s=2A/(A+1)^2$ is the moderation result, reused as dose.
- `~NE-16` — a dose measurement is a count, with all of its propagation.
- `~NE-18` — takes $E$ and turns it into a probability of harm; the 2.4 mSv
  background is its unit of comparison.
- `~NE-27` — imaging and therapy are dosimetry problems with a target.
- `~ST-09` — the statistics behind every measured dose.

## A note on this module's four corrections

Four printed results in this chapter are contradicted by the book's own numbers.
None was found by reading; all were found by recomputing.

1. **Example 9.3** reports 10.5 µSv from an expression whose own factors give
   0.105 µSv — a clean factor of 100. (It also says "5 minutes" while using
   600 s.)
2. **Example 9.5** reports "7.1 mrem". The number is right and the *unit* is
   wrong: Table 9.4 gives 7.1 **rem** = 71 mSv, thirty times a year's background.
   The printed intermediates reproduce neither, giving 16.6 mrem.
3. **Problem 9.1** calls tritium's average beta energy 5.37 **MeV**. A tritium
   beta cannot exceed 18.6 keV; the book's own Appendix D says 5.67 keV.
4. **Solution manual, Problem 9.4(a)** tabulates 0.08931 where its own factors
   give 0.06931 — and Problem 9.5(a), on the same line of the same nuclide, uses
   0.06931. The neighbouring problem proves the typo.
