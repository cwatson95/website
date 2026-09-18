# NE-23 — References

Page-level citations **verified by reading the page text** (poppler `pdftotext`)
in the PDF under `books/library/`. **Printed** = the number on the page;
**PDF** = the viewer page.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, **3rd ed.** (2017) | `NE_Nuclear_Engineering/nuclear_science_shultis_faw.pdf` | PDF = printed **+ 23** |

## Topic → location

| Topic (code symbol) | Section | Printed p. | PDF p. |
|---|---|---|---|
| The fuel cycle; the once-through route | §11.7, Fig. 11.29 | 410–411 | 433–434 |
| Mining, milling, yellowcake (80% U₃O₈), conversion to UF₆ | §11.7 | 410 | 433 |
| **0.720 a% natural abundance**, enrichment to ~3% | §11.7 | 410 | 433 |
| Refuelling: a third of a PWR, a quarter of a BWR | §11.7 | 410–411 | 433–434 |
| **Table 11.7** — annual flows for a 1000 MW(e) PWR (`ANNUAL_FLOWS`) | Table 11.7 | 411 | 434 |
| Recycling cuts lifetime U₃O₈ by ~45%; the proliferation objection | §11.7 | 411–412 | 434–435 |
| Uranium needs: 150 t/y, 4500 t/life; 40 kg for an LMFBR | §11.7.1 | 412 | 435 |
| Uranium availability; 4×10⁶ t under \$130/kg; oceans, shales | §11.7.1 | 412–413 | 435–436 |
| **Enrichment techniques** (`ENRICHMENT_TECHNOLOGIES`) | §11.7.2 | 413–415 | 436–438 |
| Gaseous diffusion; hundreds of stages | §11.7.2 | 413–414 | 436–437 |
| Gas centrifuge; "a few percent of the electrical energy" | §11.7.2 | 414 | 437 |
| Aerodynamic; electromagnetic; laser (49 µeV isotope shift) | §11.7.2 | 414–415 | 437–438 |
| **Waste classification** (`WASTE_CLASSES`) | §11.7.3 | 415–416 | 438–439 |
| Spent fuel; the seven long-lived fission products | §11.7.4 | 416 | 439 |
| **The 1000-year argument**; 10⁻¹⁰ in 1000 y | §11.7.4 | 416 | 439 |
| **Table 11.8** — new and spent fuel composition (`SPENT_FUEL_ATOM_PERCENT`) | Table 11.8 | 417 | 440 |
| Reprocessing; the actinide timescale; the U.S. position | §11.7.4 | 417 | 440 |
| Nuclear propulsion; Rickover, *Nautilus*, *Triton* | §§11.8–11.8.1 | 418–420 | 441–443 |
| Other marine applications; propulsion in space | §§11.8.2–11.8.3 | 420–424 | 443–447 |

## Two things this module adds, both load-bearing

### Separative work
§11.7.2 describes **five** enrichment technologies in detail and never states the
quantity that measures any of them. Without it, "a gas centrifuge needs a few
percent of the electrical energy of a diffusion plant of the same capacity"
(printed 414) has no *capacity* to compare.

The value function and the SWU equation are standard:
$$V(x)=(2x-1)\ln\frac{x}{1-x},\qquad
\mathrm{SWU}=P\,V(x_P)+T\,V(x_T)-F\,V(x_F).$$

Applied to Table 11.7's own numbers — 28 070 kg of product at 2.925%, 121 227 kg
of tails at 0.2%, from 149 297 kg of feed at 0.7114 wt-% — this gives **116.2
tSWU/y**, or 4.14 SWU per kg of product. Both are squarely in the published range
for a 1000 MW(e) PWR, which is the check that the module is computing the same
thing the industry does.

It also makes two things visible that the chapter cannot otherwise say:

- **The tails assay is an economic optimum**, not a constant. At \$50/kg U the
  optimum is 0.30%; at \$250/kg it is 0.14%. Table 11.7's 0.2% corresponds to
  roughly equal uranium and SWU prices. `optimal_tails_assay`.
- **Enrichment work is front-loaded.** Making 1 kg of 90% HEU requires 4.553 kg
  of 20% material, and producing that 20% material is **90.4%** of the total
  separative work. A stock of 20% uranium is nine tenths of the way to weapons
  grade, which is precisely why 20% is the LEU/HEU regulatory line — a fact
  §11.7.2 has all the ingredients for and does not draw.

### Atom-% is not weight-%
§11.7 gives the natural abundance as **0.720 a%** (Appendix A.4 gives 0.7204 a%).
Every enrichment calculation uses **weight** fractions, where the value is
**0.7114 wt-%**.

Substituting one for the other changes the feed-to-product ratio by **1.8%** —
2.7 tonnes of natural uranium a year on a single reactor, and invisible because
both numbers read as "0.72%".

Table 11.7 itself settles which convention it uses: its ²³⁵U balance
$F x_F = P x_P + T x_T$ closes to **0.13%** with 0.7114 wt-% and to **1.4%** with
0.7204 a%. `atom_to_weight_fraction`, and
`test_natural_uranium_is_0_7204_atom_percent_and_0_711_weight_percent`.

## Three checks that establish the tables

Nothing in §§11.7–11.8 was found to be wrong. That conclusion rests on three
independent verifications rather than on reading:

### Table 11.7's enrichment balance closes exactly
$821+27\,249+121\,227=149\,297$ kg — the printed product and tails sum to the
printed feed **to the kilogram**, with no rounding slack. The product assay is
2.9248%, the F/P ratio 5.319 against 5.329 from the balance equations (0.2%), and
the conversion step loses 0.5% of the uranium as it should.

### A mass flow agrees with an energy output to 1%
Table 11.7 reports **873 kg** of fission products a year. At 200 MeV per fission
that mass is 830 000 MWd(t) = **277 full-power days** at 3000 MW(t) — against the
**274 days** the table's own stated 75% capacity factor implies.

These are computed by entirely different routes (a chemical mass flow against a
thermal energy output), and they agree to 1%. It is the strongest single check
available on the table. *`test_the_fission_product_mass_matches_the_energy_produced`.*

### Table 11.8 closes exactly as a heavy-atom balance
Both columns sum to **100.00** atom-%, and the transmutation accounting closes to
two decimals with no adjustment:

| | |
|---|---|
| ²³⁵U consumed 2.49 | = 0.51 captured to ²³⁶U + **1.98 fissioned** |
| ²³⁸U consumed 2.40 | = 0.88 Pu remaining + **1.52 Pu fissioned** |
| total fissions | = 1.98 + 1.52 = **3.50** = the printed fission-product entry |

Two conclusions follow that the book states only qualitatively. **43% of the
fissions came from plutonium** — §11.1's "almost half the power" at end of life,
now with a number. And 3.5% of the heavy atoms fissioned is **33.3 GWd/tU**,
against the **33 GWd/tU** discharge burnup printed in Table 11.2, six chapters
earlier and sourced separately. *`test_table_11_8_closes_exactly_as_a_heavy_atom_balance`,
`test_burnup_from_table_11_8_matches_table_11_2`.*

## A wording note
§11.7's caption to Table 11.7 says the data are "based on an assumed plant
capacity factor of 0.75, i.e., the production of **750 GWy** of electrical
power". A 1000 MW(e) plant at 75% produces 0.75 GW·y of electricity in a year,
not 750 — the intended quantity is presumably 750 MW(e)·y. The tabulated numbers
are consistent with 0.75 GW·y (that is what the 873 kg fission-product check
confirms), so this is a units slip in the caption and not in the data.

## Where the module refuses rather than answering
`feed_per_product` (and everything built on it) raises unless
$0<x_T<x_F<x_P<1$. A cascade cannot enrich below its own feed or leave tails
richer than its feed; outside that ordering the two balance equations have no
positive solution, and the algebra would otherwise return a negative feed ratio
and propagate it silently into a negative SWU.

## Cross-module dependencies
- **`~NE-22`** — the reactor these flows pass through; Table 11.2's burnup is
  independently confirmed here.
- **`~NE-20`** — plutonium buildup is the positive isotopic feedback of §10.8.1,
  quantified here at 43% of the fissions.
- **`~NE-09`** — fission yields; **`~NE-05`/`~NE-06`** — the decay chains behind
  the waste timescales.
- **`~NE-18`** — the dose limits a repository must meet over those timescales.
- **`~NE-24`** — the fusion fuel cycle, which has no mining or enrichment and a
  tritium-breeding problem instead.

## Further reading
- Benedict, Pigford & Levi, *Nuclear Chemical Engineering*, 2nd ed. — the
  standard treatment of cascades, the value function and reprocessing chemistry;
  the source of essentially everything in §11.7.2 done quantitatively.
- Cochran & Tsoulfanidis, *The Nuclear Fuel Cycle: Analysis and Management* —
  fuel-cycle economics, including the tails-assay optimisation.
- NAS/NRC, *Nuclear Wastes: Technologies for Separations and Transmutation*
  (1996) — the actinide-partitioning case §11.7.4 gestures at.
- IAEA INFCIRC/153 and the 20% LEU/HEU definition — the policy consequence of the
  front-loaded SWU curve.
