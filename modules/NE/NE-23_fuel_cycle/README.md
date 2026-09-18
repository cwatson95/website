# NE-23 — The nuclear fuel cycle: enrichment & SWU, burnup, spent fuel, waste

Twenty-third module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`), and the last of Chapter 11. Covers **§§11.7–11.8**
(printed pp. 410–424) of Shultis & Faw, 3rd ed.: the fuel cycle, uranium supply,
enrichment techniques, radioactive waste, spent fuel, and nuclear propulsion.

- **Prerequisites:** `~NE-22` (the reactor these flows pass through), `~NE-09`
  (fission yields), `~NE-05`/`~NE-06` (decay).
- **Cross-links:** `~NE-20` (plutonium buildup as feedback), `~NE-18` (the dose
  limits a repository must meet), `~NE-24` (the fusion fuel cycle, for contrast).

## Scope
Follow the material: 150 t of natural uranium a year in, 26 t of spent fuel out,
and a waste problem measured in hundreds of thousands of years. Four fifths of
the mined uranium never enters a reactor — it leaves the enrichment plant as
depleted tails. The module adds the two things S&F leave out and everything
downstream needs: **separative work**, the unit all five enrichment technologies
are measured in, and the **atom-% / weight-%** distinction that silently shifts a
feed requirement by 1.8%.

## Operations — `code/fuel_cycle.py`

| call | meaning | reference |
|------|---------|-----------|
| `atom_to_weight_fraction(a)` | 0.7204 a% → 0.7114 wt-% | §11.7 + added |
| `value_function(x)` | V = (2x−1)ln[x/(1−x)] | added |
| `separative_work(P, x_f, x_p, x_t)` | SWU; 116 tSWU/y for Table 11.7 | added |
| `feed_per_product`, `tails_per_product` | the cascade balance; **refuses impossible cascades** | added |
| `optimal_tails_assay(x_f, x_p, $U, $SWU)` | the tails assay as an economic optimum | added |
| `ANNUAL_FLOWS` | Table 11.7's flowsheet | Table 11.7 |
| `natural_uranium_per_year`, `lifetime_uranium` | 150 t/y, 4500 t/life | §11.7.1 |
| `NEW_FUEL_ATOM_PERCENT`, `SPENT_FUEL_ATOM_PERCENT` | Table 11.8 | Table 11.8 |
| `plutonium_fission_fraction()` | 43% of the fissions | Table 11.8 |
| `burnup_from_fissioned_fraction(3.5)` | 33.3 GWd/tU, = Table 11.2's 33 | Table 11.8 |
| `fission_energy_from_mass(873)` | 830 000 MWd = 277 full-power days | Table 11.7 |
| `fission_product_activity_fraction`, `years_to_ore_activity` | the 1000-year argument | §11.7.4 |
| `WASTE_CLASSES`, `LONG_LIVED_FISSION_PRODUCTS`, `ENRICHMENT_TECHNOLOGIES` | the classifications | §§11.7.2–11.7.3 |

## Use
```python
from fuel_cycle import (atom_to_weight_fraction, value_function, separative_work,
                        feed_per_product, optimal_tails_assay,
                        plutonium_fission_fraction, burnup_from_fissioned_fraction,
                        fission_energy_from_mass, years_to_ore_activity,
                        U235_WEIGHT_FRACTION)

atom_to_weight_fraction(0.007204)          # 0.007114 -- not the same number
separative_work(28070, U235_WEIGHT_FRACTION, 0.029249, 0.002) / 1e3   # 116.2 tSWU/y
optimal_tails_assay(U235_WEIGHT_FRACTION, 0.045, 250.0, 100.0)[0]     # 0.0014 -- dear U

plutonium_fission_fraction()               # 0.434 -- 43% of the energy
burnup_from_fissioned_fraction(3.5)        # 33.3 GWd/tU = ~NE-22's Table 11.2
fission_energy_from_mass(873) / 3000       # 277 full-power days, vs 274 implied

years_to_ore_activity(1e-10)               # 997 y for fission products
years_to_ore_activity(1e-10, 24000.0)      # 798 000 y for 239Pu

feed_per_product(0.00711, 0.03, 0.03)      # raises: a cascade cannot do that
```

## Run
```bash
cd code
python3 fuel_cycle.py        # demo: the flowsheet, SWU, tails economics, Table 11.8, waste
python3 test_fuel_cycle.py   # tests  ->  "All 12 tests passed."
cd ../figures && python3 make_figures.py
```

## Files
- `notes.md` — the atom-%/weight-% trap → the mass balance and its
  mass-against-energy check → separative work, the optimal tails assay and the
  proliferation arithmetic → spent fuel and where the energy came from → the two
  waste timescales → uranium supply and propulsion, with a "Where this goes" map.
- `code/fuel_cycle.py`, `code/test_fuel_cycle.py` (stdlib only). `feed_per_product`
  **refuses** a cascade with x_t ≥ x_f or x_p ≤ x_f: the balance equations have no
  positive solution there, and the formula would otherwise return a negative feed
  ratio without complaint.
- `problems/problems.md` — 6 worked problems with numeric `*Check:*` lines.
- `figures/` — the annual mass flow with the tails stream drawn to scale, the
  value function beside the tails-assay optimum, Table 11.8's before/after
  composition beside which nucleus actually fissioned, and the two waste
  timescales on one log axis.
- `refs.md` — page-verified citations; the two things this module adds and why
  they are load-bearing; and the three independent checks that establish
  Tables 11.7 and 11.8 as trustworthy.
