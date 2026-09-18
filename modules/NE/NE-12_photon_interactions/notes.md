# NE-12 — Photon interactions: photoelectric, Compton, pair production (notes)

`~NE-11` treated $\mu$ as a number you look up. This module opens it up. Over the
10 eV – 20 MeV range that matters for shielding and dosimetry, exactly **three**
processes carry essentially the whole of $\mu$, and they divide the energy axis
between them [S&F §7.3, printed p. 191]:

| process | $\sigma$ scales as | dominates |
|---|---|---|
| photoelectric | $Z^4/E^3$ | low energy |
| Compton | $Z/E$ | middle |
| pair production | $Z^2$ | high energy, zero below 1.022 MeV |

Two facts organise everything downstream, and both come from that table.

**The $Z$ exponents are why materials differ.** Compton goes as $Z$ per atom,
i.e. as $Z/A\simeq\tfrac12$ per *gram*, so at MeV energies every material is
about equally good per gram and lead wins only on density (`~NE-11` P2). The
photoelectric $Z^4$ shatters that tie at low energy: per gram, lead beats water
by a factor of **1900** at 100 keV. High-$Z$ shields are for x-rays; sheer mass
is for gammas.

**Only one of the three actually absorbs.** The photoelectric effect destroys the
photon. Compton scattering leaves a degraded photon still travelling, and pair
production hands back two 0.511 MeV annihilation photons. So $\mu$ counts
*interactions* while $\mu_{en}$ counts *energy deposited*, and over most of the
MeV range they differ by more than a factor of two. That gap is what buildup
factors (`~NE-11`) and dose conversion (`~NE-17`) exist to manage.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed., §7.3,
cited by **printed** page (PDF = printed + 23). Coefficients from
`../data_tables/C3_photon_coefficients_*.csv`.

## 1. Photoelectric effect

A photon is absorbed by a **whole atom**, ejecting a bound electron — usually
from the K shell — with [S&F §7.3.1]
$$E_e=E-E_b.$$
The atom recoils but takes essentially none of the energy: by the inverse-mass
split of `~NE-08`, a nucleus thousands of times heavier than the electron gets a
negligible share. This process needs a *bound* electron. A free electron cannot
absorb a photon and conserve both energy and momentum — the atom's role is to
take up the momentum, which is exactly why the cross section climbs so steeply
with $Z$.

**Absorption edges.** As the photon energy falls below a shell's binding energy,
that shell switches off *discontinuously*: the cross section drops abruptly, then
climbs again as $E$ falls further, until the next edge. Lead's K edge sits at
**88 keV** and its L edges at 13–16 keV. The tables carry each edge energy
**twice**, once with the shell closed and once open, and lead's K edge jumps
$\mu_{ph}/\rho$ from 1.547 to 7.320 cm²/g — a factor of 4.7 across zero energy
difference.

This is the sharpest feature in all of photon physics, and it is *useful*.
Iodine ($E_K=33$ keV) and barium ($E_K=37$ keV) are chosen as radiographic
contrast agents precisely because their K edges sit inside the diagnostic x-ray
band, so they absorb far more strongly than tissue at exactly the energies used
(`~NE-27`).

The scaling S&F quote [Eq. (7.32)],
$$\sigma_{ph}\propto\frac{Z^4}{E^3},$$
is explicitly crude: $n\simeq3$ below ~150 keV falling to $n\simeq1$ above 5 MeV,
and $m$ running from 4 at 100 keV to 4.6 at 3 MeV. `photoelectric_scaling` is
therefore named and documented as a *scaling* — dimensionless, useful in ratios,
never a substitute for the table.

**Afterwards.** The vacancy fills, emitting either a characteristic
**fluorescence x-ray** or an **Auger electron**. The K-shell fluorescent yield
runs from 0.005 at $Z=8$ to 0.965 at $Z=90$ — so in light elements the energy
stays put as an Auger electron, and in heavy elements it leaves as an x-ray.

That last point has a consequence visible in the data. Just above lead's K edge,
$\mu$ jumps 4.5-fold but $\mu_{en}$ rises only 1.5-fold, so the deposited
fraction **collapses from 0.90 to 0.29**. More interactions, less deposition: the
photon is absorbed, but a 75–85 keV fluorescence x-ray immediately escapes with
most of the energy. This is the origin of *escape peaks* in high-$Z$ detectors
(`~NE-15`), and `test_K_fluorescence_escape_shows_up_at_the_edge` pins it.

## 2. Compton scattering

A photon scatters off an electron treated as **free and at rest**. The
relativistic kinematics give [S&F Eq. (7.33), from Eq. (2.30)]
$$\boxed{\;E'=\frac{E}{1+(E/m_ec^2)(1-\cos\theta_s)}\;}$$

Look at what is *absent*: the material. Every electron is identical, so $E'$
depends on energy and angle alone. That universality is why a Compton edge lands
at the same energy in every detector, whatever it is made of.

Equivalently, in wavelength,
$$\Delta\lambda=\frac{h}{m_ec}(1-\cos\theta_s),$$
where $h/m_ec=0.02426$ Å is a **constant** — independent of both energy and
material. That was the content of Compton's 1923 experiment and what settled the
question of whether photons carry momentum.

Two features of the spectrum follow, and both are worth memorising:

- **Compton edge**, the maximum electron energy, at $\theta_s=180°$:
  $$E_{\max}=E\,\frac{2E}{m_ec^2+2E}.$$
  For ¹³⁷Cs's 662 keV line, **477 keV**.
- **Backscatter peak**, the photon at $180°$: for ¹³⁷Cs, **184 keV**. As
  $E\to\infty$ it saturates at $m_ec^2/2=0.2555$ MeV, so backscatter peaks always
  cluster near 200–250 keV whatever the source — which is what makes them
  recognisable.

The two sum to $E$, necessarily: one photon's loss is the electron's gain.

Note that the Compton edge is always *below* the photopeak. A Compton event
cannot deposit everything, because the scattered photon always escapes with at
least $m_ec^2/2$ worth. Getting a full-energy peak requires the photoelectric
effect — which is why detectors are made of high-$Z$ material (`~NE-15`).

The total cross section is the **Klein–Nishina** formula [S&F Eq. (7.34)]
$$\sigma_c(E)=\pi Zr_e^2\lambda\left[(1-2\lambda-2\lambda^2)\ln\!\left(1+\frac2\lambda\right)
+\frac{2(1+9\lambda+8\lambda^2+2\lambda^3)}{(\lambda+2)^2}\right],
\qquad\lambda\equiv\frac{m_ec^2}{E},$$
with $r_e=e^2/4\pi\epsilon_0m_ec^2=2.818\times10^{-13}$ cm. It tends to the
Thomson cross section $6.65\times10^{-25}$ cm² as $E\to0$ and falls roughly as
$1/E$ at high energy.

**This is checkable, and checking it is the strongest test in the module.**
Klein–Nishina is an analytic formula; Appendix C.3's Compton column is
independent tabulated data. Computing $\mu_c/\rho=(N_AZ/A)\sigma_{KN}$ reproduces
the table to better than **1%** above 0.5 MeV in all five materials — which
simultaneously validates the formula, $r_e$, the assumed compositions and the
table extraction.

**Where it breaks, and why that is also a check.** S&F note [§7.3.2] that
Eqs. (7.33)–(7.34) "break down when the kinetic energy of the recoil electron is
comparable to its binding energy". The tabulated column is the *bound*-electron
(incoherent) cross section, which is smaller, so free-electron Klein–Nishina must
**over**-predict — more so as energy falls and as $Z$ rises. Both trends hold
quantitatively, and the onset tracks the K edge:

| | 10 keV | 100 keV | 500 keV |
|---|---|---|---|
| water (O K = 0.54 keV) | +38% | +1.3% | +0.03% |
| iron (K = 7.1 keV) | +110% | +6.6% | +0.5% |
| lead (K = 88 keV) | +236% | +19% | +2.3% |

This is physics, not a discrepancy to tune away, and the test asserts the trend
rather than loosening a tolerance.

**Coherent (Rayleigh) scattering** competes — the whole atom recoils, so the
energy loss is slight and the angle small (75% of 1 MeV photons on iron scatter
within 4°). It can exceed incoherent scattering at low energy and high $Z$, but
because it barely changes energy or direction, and because photoelectric
absorption dominates there anyway, it is **deliberately excluded** from the
tabulated total [S&F §7.3.4].

## 3. Pair production

Above a threshold of $2m_ec^2=1.022$ MeV, a photon can vanish in the strong field
near a nucleus, creating an electron–positron pair [S&F §7.3.3]. The nucleus
takes momentum but negligible energy, so [Eq. (7.36)]
$$E_++E_-=E_\gamma-2m_ec^2.$$

The threshold is a **conservation law, not a trend**: below 1.022 MeV the process
is forbidden absolutely, and the `pp` column of Appendix C.3 is identically zero
there and non-zero above. Pair production in the field of an *electron* (triplet
production) is possible but needs $4m_ec^2=2.044$ MeV, because the light recoil
partner must carry real momentum.

The positron's fate matters as much as its creation. It slows to rest and
annihilates, returning **two 0.511 MeV photons back-to-back**. So pair production
does not remove 1.022 MeV from the field — it parks it and hands it back, as two
penetrating photons, somewhere else. That is why $\mu_{en}<\mu$ at high energy,
why 511 keV is the signature of every positron emitter, and why PET works at all
(`~NE-27`).

## 4. Putting them together

The total is the sum [S&F Eqs. (7.37)–(7.38)]
$$\frac{\mu}{\rho}=\frac{\mu_{ph}}{\rho}+\frac{\mu_c}{\rho}+\frac{\mu_{pp}}{\rho},$$
coherent scattering excluded by convention. The **Compton window** — the band
where scattering dominates — is squeezed from below by $Z^4$ and from above by
$Z^2$, so it is wide in light materials and narrow in heavy ones:

| material | photoelectric → Compton | Compton → pair | width |
|---|---|---|---|
| water | 0.028 MeV | > 20 MeV | > 700× |
| concrete | 0.054 MeV | 16.5 MeV | 306× |
| iron | 0.117 MeV | 9.5 MeV | 81× |
| lead | 0.556 MeV | 4.8 MeV | **8.6×** |

In lead the Compton window spans less than one decade. That is the practical
statement of the $Z$ exponents, and it explains a lot of shielding practice: lead
is superb at x-ray energies and merely dense at MeV energies.

Finally, the distinction the whole module builds toward [S&F Eq. (7.39)]:
$$\mu_{en}\simeq\mu f,$$
where $f$ is the fraction of energy actually transferred to the medium rather
than carried off by secondary photons — fluorescence, Compton-scattered photons,
annihilation quanta and bremsstrahlung. **Interacting is not depositing.** In
water at 100 keV, $f=0.15$: an interaction happens, and 85% of the energy leaves.
Every shielding calculation that stops at $e^{-\mu x}$ and every dose calculation
that uses $\mu$ instead of $\mu_{en}$ is wrong by roughly this factor.

## Where this goes

- `~NE-11` — the $\mu$ this module decomposes; buildup factors exist because
  Compton scattering does not remove photons, only degrades them.
- `~NE-14` — the photoelectrons, Compton electrons and pairs created here are
  charged particles, and what they do next is stopping power.
- `~NE-15` — the photopeak, Compton edge, backscatter peak and escape peaks of a
  gamma spectrum are §1–§3 read off an oscilloscope.
- `~NE-17` — dose is $\mu_{en}\phi E/\rho$; the `en` column and the factor $f$
  are exactly what dosimetry needs.
- `~NE-27` — K-edge contrast agents (§1), 511 keV annihilation and PET (§3).
