# NE-22 — References

Page-level citations **verified by reading the page text** (poppler `pdftotext`)
in the PDF under `books/library/`. **Printed** = the number on the page;
**PDF** = the viewer page.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, **3rd ed.** (2017) | `NE_Nuclear_Engineering/nuclear_science_shultis_faw.pdf` | PDF = printed **+ 23** |

## Topic → location

| Topic (code symbol) | Section / Eq. | Printed p. | PDF p. |
|---|---|---|---|
| Generations I–IV; the chapter's framing | Ch. 11 opening | 369–370 | 392–393 |
| Nuclear electric power by country | §11.1 | 370–371 | 393–394 |
| **Table 11.1** — 2013 share and capacity (`NUCLEAR_SHARE_2013`) | Table 11.1 | 372 | 395 |
| Electricity from thermal energy; the steam cycle | §11.1.1, Fig. 11.1 | 371 | 394 |
| **Carnot efficiency** (`carnot_efficiency`) | Eq. (11.1), §11.1.2 | 371–373 | 394–396 |
| Typical power reactors; PWR, BWR, HTGR, LMFBR, CANDU | §11.1.3 | 373–378 | 396–401 |
| **Coolant limitations; the 374 °C ceiling** (`coolant_is_liquid`) | §11.1.4 | 378 | 401 |
| Industrial infrastructure | §11.1.5 | 378–379 | 401–402 |
| Evolution of power reactors | §11.1.6 | 379 | 402 |
| Generation II PWRs; the steam cycle | §§11.2–11.2.1, Fig. 11.8 | 379–380 | 402–403 |
| **Table 11.2** — a 1000 MW(e) PWR (`PWR`) | Table 11.2 | 379 | 402 |
| PWR components: vessel, SG, pressuriser, rods | §11.2.2 | 380–385 | 403–408 |
| Generation II BWRs; the direct cycle | §§11.3–11.3.1, Fig. 11.15 | 385–386 | 408–409 |
| **Table 11.3** — a 1000 MW(e) BWR (`BWR`) | Table 11.3 | 386 | 409 |
| BWR components; jet pumps, separators, cruciform rods | §11.3.2 | 386–391 | 409–414 |
| Generation III designs | §11.4 | 391 | 414 |
| ABWR and ESBWR | §11.4.1 | 391–392 | 414–415 |
| **Table 11.4** — BWR/6, ABWR, ESBWR (`GEN_III_BWR`) | Table 11.4 | 391 | 414 |
| System 80+; AP600 and AP1000 | §§11.4.2–11.4.3 | 392–393 | 415–416 |
| **Table 11.5** — AP1000 and EPR (`GEN_III_PWR`) | Table 11.5 | 393 | 416 |
| Other evolutionary LWRs; HWRs; gas-cooled; LMFBRs | §§11.4.4–11.4.7 | 393–396 | 416–419 |
| **Generation IV; the GIF** (`GEN_IV_SYSTEMS`) | §11.5 | 396–402 | 419–425 |
| SCWR, LFR, MSR, GFR, VHTR, SFR | §§11.5.1–11.5.6 | 397–402 | 420–425 |
| Other advanced concepts; small reactors | §11.6 | 402–403 | 425–426 |
| **Table 11.6** — small reactor designs (`SMALL_REACTORS`) | Table 11.6 | 403 | 426 |

## Table 11.3 does not add up

The BWR table gives three quantities that fix each other:

- thermal output **3830 MW**
- fuel loading **168 × 10³ kg U**
- specific power **25.9 kW/kg(U)**

But 25.9 × 168 000 = **4351 MW**, 14% above the printed 3830 MW. Equivalently,
3830 MW over 168 t is **22.8 kW/kg**, and a loading of **148 t** would be needed
to make 25.9 correct.

**The same check passes for Table 11.2 to 0.15%** — 33 kW/kg × 115 t = 3795 MW
against a printed 3800 — which is what isolates this as a defect in Table 11.3
rather than a flaw in the method. Table 11.3's other relations are fine: its core
geometry reproduces its power density to 0.5%, and its output over its electric
power reproduces its efficiency.

Which of the three numbers is wrong cannot be settled from the book alone. For
context, a BWR/4 of this vintage carried roughly 138 t at 3293 MW(t), i.e.
23.9 kW/kg — closer to the derived 22.8 than to the printed 25.9. *Pinned by
`test_table_11_3_does_not_add_up`, which asserts the inconsistency and not a
resolution.*

## "About 40%": §11.1.2 against §11.1.4

§11.1.2 (printed 373): "In modern nuclear power plants, conversion efficiencies
of **about 40%** can be achieved, while fossil-fired units can achieve only
slightly greater efficiencies. However, many older power plants have efficiencies
in the range of 30–35%."

§11.1.4 (printed 378): "This high temperature limit for reactor produced steam
together with normal ambient environmental temperatures **limit the thermal
efficiency for such plants to about 34%**" — and, of gas and liquid-metal
coolants, "permits thermal efficiencies **up to 40%**".

Since essentially every operating power reactor is water-cooled, the 40% belongs
to §11.1.4's second sentence and not to "modern nuclear power plants". The book's
own data agree with §11.1.4:

| plant | η |
|---|---|
| Table 11.2 PWR | 0.342 |
| Table 11.3 BWR | 0.347 |
| Table 11.4 BWR/6 / ABWR / ESBWR | 0.349 / 0.344 / 0.344 |
| Table 11.5 AP1000 | 0.329 |
| Table 11.5 **EPR** | **0.370** |

The EPR is the highest, at 37%, and is the closest any of the book's own
water-cooled entries comes. Recorded rather than corrected: §11.1.2's sentence is
loose rather than wrong, and §11.1.4 states the constraint correctly.

## How the tables were validated

Chapter 11's content is its tables, so each was required to reproduce its own
derived quantities from its own primary ones. Table 11.2 (PWR):

| relation | derived | printed | agreement |
|---|---|---|---|
| π(d/2)²L → power density | 102.2 kW/L | 102 | 0.2% |
| MW(t)/loading → specific power | 33.0 kW/kg | 33 | 0.1% |
| assemblies × rods × L → linear heat rate | 17.9 kW/m | 17.5 | 2.2% |
| q′/(πd) → surface heat flux | 0.586 MW/m² | 0.584 | 0.4% |
| lattice × pitch → assembly width | 21.42 cm | 21.4 | 0.1% |
| 17² − 264 | 25 guide/instrument tubes | — | exact |

Table 11.5's linear heat rates also reproduce from bundle count, 17×17 lattice
and active height to within 4% (AP1000 190.8 vs 187 W/cm; EPR 161.8 vs 156), the
residual being the fraction of lattice positions taken by guide tubes.

The one relation that fails anywhere is Table 11.3's specific power, above.

## Cross-module dependencies
- **`~NE-19`**, **`~NE-21`** — enrichment, k_∞, and the bare-core peaking factor
  of 3.64 that real designs beat.
- **`~NE-20`** — control rods, soluble boron and burnable poisons, which appear
  here as the hardware of Tables 11.2 and 11.3.
- **`~NE-23`** — burnup, enrichment and the back end; the fuel-cycle case for the
  four fast Generation IV systems.
- **`~Thermo-08`**, **`~Thermo-09`** — the Rankine cycle, and why wet steam costs
  turbine efficiency.
- **`~NE-18`** — the dose limits behind containment and the controlled-area
  boundary.

## Further reading
- Todreas, N.E. & Kazimi, M.S., *Nuclear Systems* I–II — the thermal-hydraulics
  behind linear heat rate, critical heat flux and the DNB limits this chapter
  quotes without deriving.
- Lamarsh & Baratta, *Introduction to Nuclear Engineering*, Ch. 4 and 8 — reactor
  types and heat removal at the same level as §11.1.
- GIF, *Technology Roadmap Update for Generation IV Nuclear Energy Systems*
  (2014) — the source S&F's §11.5 follows, including the post-2030 deployment
  statement.
- IAEA PRIS database — the live version of Table 11.1; the 2013 snapshot here is
  already historical, and Japan's 48 units in particular have not all restarted.
