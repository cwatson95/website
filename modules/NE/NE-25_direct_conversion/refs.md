# NE-25 — References

Page-level citations **verified by reading the page text** (poppler `pdftotext`)
in the PDF under `books/library/`. **Printed** = the number on the page;
**PDF** = the viewer page.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, **3rd ed.** (2017) | `NE_Nuclear_Engineering/nuclear_science_shultis_faw.pdf` | PDF = printed **+ 23** |

## Topic → location

| Topic (code symbol) | Section | Printed p. | PDF p. |
|---|---|---|---|
| Thermoelectric generators; the Seebeck effect | §12.5 | 449–451 | 472–474 |
| p- and n-type semiconductors; the thermopile | §12.5 | 449–450 | 472–473 |
| Tellurides and selenides; "up to 10 percent" | §12.5 | 450 | 473 |
| Radionuclide thermoelectric generators (RTGs) | §12.5.1 | 451–455 | 474–478 |
| **Table 12.1** — the SNAP series (`SNAP_GENERATORS`) | Table 12.1 | 452 | 475 |
| Thermionic generators | §12.6 | 455–457 | 478–480 |
| **Conversion efficiency; the Carnot bound; 1400 K** | §12.6.1 | 456–457 | 479–480 |
| In-pile thermionic generators | §12.6.2 | 457–458 | 480–481 |
| AMTEC conversion | §12.7 | 458–461 | 481–484 |
| Stirling converters | §12.8 | 461–464 | 484–487 |
| Direct conversion of nuclear radiation | §12.9 | 464–466 | 487–489 |
| **Betavoltaic batteries** (`betavoltaic_power`) | §12.9.2 | 466–468 | 489–491 |
| Radioisotopes for thermal power sources | §12.10 | 468–470 | 491–493 |
| **Table 12.2** — the nine practical sources (`RADIONUCLIDE_SOURCES`) | Table 12.2 | 469 | 492 |
| Space reactors; the U.S. and Russian programmes | §§12.11–12.11.2 | 470–478 | 493–501 |
| **Table 12.3** — space power reactors (`SPACE_REACTORS`) | Table 12.3 | 477 | 500 |
| COSMOS-954 and the BUK disposal system | §12.11.2 | 477–478 | 500–501 |

## Table 12.2 passes eighteen internal checks

The table gives four numeric properties for nine nuclides — half-life,
recoverable energy per decay, specific activity, specific power — and **only two
of the four are independent**. Both derived rows reproduce:

| check | worst case | agreement |
|---|---|---|
| W/g from (Ci/g) × (MeV/dec) | ¹⁴⁴Ce | **0.1%** |
| Ci/g from ln2/T½ × N_A/A | ⁹⁰Sr | **1.3%** |
| Ci/W from the two above | all nine | 0.5% |

⁹⁰Sr is the only entry above 0.5%, plausibly because its row is quoted in secular
equilibrium with ⁹⁰Y (as the caption states for its recoverable energy) while the
specific-activity calculation here uses ⁹⁰Sr alone. Nothing else in the table
needs an explanation.

Eighteen passing internal checks is what makes a table usable rather than merely
printed. *Verified: `test_table_12_2_is_fully_self_consistent`.*

## Three relations this module adds

Nothing in §§12.5–12.11 was found to be wrong. Three things are absent, and each
is what turns a described device into a designed one.

### The thermoelectric efficiency
§12.5 reports "conversion efficiencies up to 10 percent" and never gives the
relation that produces them:
$$\eta=\eta_{\rm Carnot}\,\frac{\sqrt{1+Z\bar T}-1}{\sqrt{1+Z\bar T}+T_c/T_h}.$$

Without it there is no way to see that **ZT is the binding parameter**, nor what
improving it would buy. At ZT = 1 the second factor is 0.23, so a 61%-Carnot
temperature pair yields 14% and a real RTG lands at 5–7%. A 20% device would need
ZT = 1.78. `thermoelectric_efficiency`, `zt_for_efficiency`.

### The Richardson law
§12.6.1 states that emitter temperatures "typically in excess of 1400 K" are
needed, as a fact rather than a consequence. $J=AT^2e^{-\phi/kT}$ makes it a
consequence: for a 2.5 eV emitter the current density is $1.4\times10^{-8}$ A/cm²
at 800 K and 39 A/cm² at 1800 K — **ten orders of magnitude for a factor of 2.25
in temperature**. It also explains caesium coatings: 2.5 eV → 1.8 eV is a factor
of 200. `richardson_current`.

### Mission sizing
§12.10 lists nine isotopes with their properties and never combines them into
"how many grams for this mission". Doing so is the point of the table, because
**the ranking inverts with mission length**: ²¹⁰Po is lightest for 90 days and
useless past a year. `fuel_mass_for_power`, `mission_sizing`.

## What the mass ranking hides
By mass alone, ²⁴²Cm and ²⁴⁴Cm beat ²³⁸Pu at every mission length. Neither has
flown, and Table 12.2 says why in a row easy to skim past: their shielding
entries read **"neut."** — both are strong spontaneous-fission neutron emitters,
against which the lead thicknesses tabulated for the gamma emitters are useless.
⁶⁰Co is the mirror image: plentiful and cheap, and needing **18 cm of lead**, the
most of any entry by a factor of 2.4.

²³⁸Pu wins because it is a near-pure alpha emitter with an 87.7-year half-life —
0.558 W/g, negligible shielding, and 69% of its power remaining after Voyager 1's
47 years. *Verified: `test_why_every_deep_space_mission_flew_plutonium_238`.*

## Where the module refuses
- **`zt_for_efficiency` above Carnot.** No value of ZT reaches the Carnot limit;
  the bracketing search would otherwise run to its upper bound and return a
  plausible-looking figure.
- **`thermionic_ideal_efficiency` with φ_collector ≥ φ_emitter.** The output
  voltage is a *difference* of work functions, so such a cell produces no
  electricity at all rather than a small amount.

## Cross-module dependencies
- **`~NE-22`** — the turbine these devices replace, and the 34% they are measured
  against; Table 12.3's space reactors run an order of magnitude below it.
- **`~NE-23`** — ²³⁸Pu is made by irradiating ²³⁷Np, a reprocessing product; the
  supply failure follows directly from the U.S. decision not to reprocess.
- **`~NE-05`, `~NE-06`** — decay modes and the exponential behind §4 of the notes.
- **`~NE-18`** — the dose basis for Table 12.2's shielding rows (10 rad/h at 1 m).
- **`~Thermo-12`, `~SM-11`** — thermoelectric materials and the solid-state
  physics of ZT.

## Further reading
- Rowe, D.M. (ed.), *CRC Handbook of Thermoelectrics* — where the efficiency
  relation and the ZT figure of merit come from.
- Angelo, J.A. & Buden, D., *Space Nuclear Power* — the SNAP series and the space
  reactor programmes in full, including COSMOS-954.
- Bennett, G.L. et al., "Mission of Daring: The General-Purpose Heat Source RTG"
  (AIAA 2006-4096) — the GPHS-RTG that flew on Galileo, Ulysses, Cassini and New
  Horizons, and the ²³⁸Pu supply problem.
- Hagelstein, P.L. et al., *Introductory Applied Quantum and Statistical
  Mechanics*, Ch. on thermionic emission — the Richardson law derived.
