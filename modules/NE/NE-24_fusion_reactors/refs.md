# NE-24 — References

Page-level citations **verified by reading the page text** (poppler `pdftotext`)
in the PDF under `books/library/`. **Printed** = the number on the page;
**PDF** = the viewer page.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, **3rd ed.** (2017) | `NE_Nuclear_Engineering/nuclear_science_shultis_faw.pdf` | PDF = printed **+ 23** |

## Topic → location

| Topic (code symbol) | Section / Eq. | Printed p. | PDF p. |
|---|---|---|---|
| Fusion reactors; the chapter's framing | §12.1 | 429–430 | 452–453 |
| **The Saha equation** (`saha_ionization_fraction`) | Eq. (12.1), §12.1.1 | 430 | 453 |
| **D-T and D-D reactions** (`REACTIONS`) | Eqs. (12.2)–(12.3) | 430 | 453 |
| Maxwellian-averaged ⟨σv⟩; Fig. 12.1 | Eq. (12.4) | 430–431 | 453–454 |
| **Fusion power density** (`fusion_power_density`) | Eq. (12.5) | 431 | 454 |
| The identical-particle ½ for D-D | footnote 1 | 431 | 454 |
| **Bremsstrahlung** (`bremsstrahlung_power_density`) | Eq. (12.6) | 431–432 | 454–455 |
| **Critical ignition temperature**; Fig. 12.2 | §12.2 | 432 | 455 |
| **The gain factor Q** (`gain_factor`) | Eq. (12.7), §12.2.1 | 432–433 | 455–456 |
| Break-even; the 20% alpha fraction | §12.2.1 | 433 | 456 |
| **Confinement time** (`energy_confinement_time`) | Eq. (12.8), §12.2.2 | 433 | 456 |
| **Lawson's criterion** (`lawson_n_tau`) | Eqs. (12.9)–(12.10) | 433 | 456 |
| The D-D prefactor and E_c | footnote 4 | 433 | 456 |
| **The triple product** (`triple_product`) | Eqs. (12.11)–(12.14), §12.2.3 | 434–435 | 457–458 |
| Fig. 12.3 — F and kTF against temperature | Fig. 12.3 | 434 | 457 |
| Plasma heating: ohmic, neutral beam, RF | §12.2.4 | 435–437 | 458–460 |
| History of MCF; tokamaks, stellarators | §12.2.5 | 437–439 | 460–462 |
| **ITER** (`ITER`) | §12.2.6 | 439–443 | 462–466 |
| **Inertial confinement** (`icf_confinement_time`) | §12.3, Eq. (12.15) | 443–446 | 466–469 |
| History of ICF; NIF | §12.3.1 | 446–449 | 469–472 |
| ICF technical problems | §12.3.2 | 449–450 | 472–473 |
| The Z machine; spherical tokamak; stellarator revival | §§12.4–12.4.3 | 450–454 | 473–477 |
| Prospects for commercial fusion | §12.4.4 | 454–455 | 477–478 |

## The ionisation energy in §12.1.1

The text reads: "for hydrogen isotopes **I = 13.06 eV** and with n = 2 × 10²¹,
95% of the atoms are ionized at T = 13,150 K."

Hydrogen's ionisation energy is **13.598 eV**. 13.06 reads as a transposed 13.60.

What makes this more than a typo is that **the worked example is internally
consistent with the wrong value**. Solving Eq. (12.1) at n = 2 × 10²¹ m⁻³ and
13 150 K gives

| I | ionised fraction |
|---|---|
| 13.06 eV (printed) | **0.9498** |
| 13.598 eV (correct) | 0.9237 |

So the "95%" was computed *with* 13.06 eV; the constant and the example stand or
fall together. With the correct value the same conditions give 92.4%, and 95%
ionisation is reached at about 13 600 K. *Verified:
`test_the_saha_example_needs_the_wrong_ionization_energy`.*

**Could not reproduce:** the same paragraph states that at room temperature the
ionised fraction is "a ridiculously small 1.5 × 10⁻¹⁰⁶". With I = 13.06 eV the
module gets 3.7 × 10⁻¹¹¹ at 293 K and 1.6 × 10⁻¹⁰⁸ at 300 K; 1.5 × 10⁻¹⁰⁶ needs
about 312 K. The exponent is hypersensitive to the assumed room temperature (five
decades between 293 K and 312 K), so this is recorded as *could-not-check* rather
than as an error. The qualitative point — "ridiculously small" — is unaffected by
five orders of magnitude either way.

## What this module adds: a usable ⟨σv⟩

S&F present the Maxwellian-averaged reactivity as **Fig. 12.1, a graph**, and give
no formula. Every quantitative statement in §§12.2–12.3 — the ignition
temperatures, Lawson's criterion, the triple product — therefore depends on
reading values off a log plot.

The module supplies two standard fits:

$$\langle\sigma v\rangle_{DT}=9.10\times10^{-16}\exp\!\left[-0.572\left|\ln\frac{T}{64.2}\right|^{2.13}\right]\ \text{cm}^3/\text{s}$$
$$\langle\sigma v\rangle_{DD}=2.72\times10^{-14}\,T^{-2/3}e^{-18.76\,T^{-1/3}}\ \text{cm}^3/\text{s}$$

with $T$ in keV, and validates them against the book itself rather than against
an outside table:

| check | module | S&F |
|---|---|---|
| D-T ⟨σv⟩ peak | 64.2 keV | the D-T cross-section peak |
| D-T ignition | 3.12 × 10⁷ K | Fig. 12.2: ~3 × 10⁷ K |
| D-D ignition | 5.29 × 10⁸ K | Fig. 12.2: ~6 × 10⁸ K |

The ignition check is the valuable one: it exercises the fits, the
bremsstrahlung coefficient of Eq. (12.6), the Q-values of Eqs. (12.2)–(12.3) and
the identical-particle factors of footnote 1 **all at once**, and it agrees to 4%
and 12%.

**Where the D-D fit is refused, and why it is allowed as far as it is.** The
Gamow form assumes the rate is set by barrier penetration alone, which fails once
the cross section turns over; at 100 keV it is roughly a factor of two low. The
module allows it to 100 keV — not 25 — precisely because **D-D ignition at 46 keV
sits in the untrustworthy band**, and refusing there would hide the fact. The
docstring records which way the error runs: the fit is low, so the D-D fusion
power is understated and the returned ignition temperature is an over-estimate.

## Two other things added
- **The ICF burn fraction.** §12.3 says only that "in practice, only a small
  portion of the pellet fuel actually fuses". The standard relation
  $\phi=\rho R/(\rho R+H_B)$ with $H_B\approx6$ g/cm² turns that into a number:
  burning a third needs $\rho R=2.6$ g/cm² against ~0.02 for an uncompressed
  millimetre pellet, i.e. the thousandfold compression the whole approach rests
  on. `areal_density_for_burn`.
- **A units note.** Eq. (12.6)'s result is labelled "W cm⁻³ s⁻¹". A watt is
  already a joule per second; the quantity is a power density, W cm⁻³. The
  numerical value and its use in §12.2 are unaffected.

## A garbled sentence in §12.2.6
"Construction was to have been completed in 2016, but … the estimated
construction cost by the end of **1015** has more than tripled and the completion
date has slipped to **2015** at the earliest."

Both years are evidently wrong: 1015 for 2015, and a completion date that has
"slipped" to *earlier* than the original 2016. The intended sense is clear and the
intended numbers are not recoverable from the text, so this is recorded rather
than corrected.

## Cross-module dependencies
- **`~NE-10`** — fusion Q-values, the Coulomb barrier and the Gamow peak; why D-T
  is the easy reaction and p-¹¹B is not.
- **`~NE-13`** — the 14.1 MeV neutron carries 80% of D-T's energy; its
  interactions set the blanket, the tritium breeding and the materials damage.
- **`~NE-22`** — the 34%-efficient fission plant fusion must eventually beat.
- **`~NE-25`** — direct conversion, which a fusion plant would also want.
- **`~PK-01`, `~PK-02`** — confinement, instabilities and transport, which this
  chapter treats descriptively.

## Further reading
- Lawson, J.D., *Proc. Phys. Soc. B* **70** (1957) 6 — the original criterion,
  four pages, and still the clearest statement of it.
- Bosch, H.-S. & Hale, G.M., *Nucl. Fusion* **32** (1992) 611 — the definitive
  ⟨σv⟩ parametrisations the fits here approximate.
- Freidberg, J.P., *Plasma Physics and Fusion Energy* — the systems argument of
  §12.2 done properly, including where the recirculating-power fraction comes from.
- Atzeni, S. & Meyer-ter-Vehn, J., *The Physics of Inertial Fusion* — the burn
  fraction, the H_B parameter, and the compression requirement in full.
