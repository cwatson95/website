# NE-25 — Direct energy conversion: thermoelectric, thermionic, AMTEC, betavoltaic

Twenty-fifth module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`), and the last of Chapter 12. Covers **§§12.5–12.11**
(printed pp. 449–478) of Shultis & Faw, 3rd ed.: thermoelectric and thermionic
generators, AMTEC, Stirling converters, direct radiation conversion and
betavoltaics, radioisotope thermal sources, and space reactors.

- **Prerequisites:** `~NE-05`/`~NE-06` (decay modes and kinetics), `~NE-22` (the
  turbine these replace), `~Thermo-12`/`~SM-11` (thermoelectric materials).
- **Cross-links:** `~NE-23` (where ²³⁸Pu comes from), `~NE-18` (shielding).

## Scope
Converting nuclear heat to electricity **without moving parts** — and the one
application that justifies the efficiency penalty: a spacecraft running for
decades unattended. Four of the five devices are still heat engines bound by
Carnot; only the betavoltaic escapes, and it pays in microwatts. The design
choice is dominated by one trade the chapter tabulates but never combines:
specific power and half-life come from the same decay constant, so the isotope
ranking **inverts** as the mission lengthens.

## Operations — `code/direct_conversion.py`

| call | meaning | reference |
|------|---------|-----------|
| `specific_activity(T½, A)`, `specific_power(Ci/g, MeV)` | the Table 12.2 cross-checks | Table 12.2 |
| `activity_per_watt(...)`, `shielding_needed(nuclide)` | Ci/W; cm of Pb, or None for neutron emitters | Table 12.2 |
| `power_after(y, T½)` | exponential decay of the source | §12.10 |
| `fuel_mass_for_power(W(e), nuclide, η, years)` | grams, sized at **end** of mission | added |
| `mission_sizing(W(e), years)` | all nine ranked by mass | added |
| `carnot_efficiency(T_h, T_c)` | the bound on four of the five | §12.6.1 |
| `thermoelectric_efficiency(ZT, T_h, T_c)` | the relation S&F quote results from | added |
| `zt_for_efficiency(target, ...)` | **refuses a target at or above Carnot** | added |
| `richardson_current(T, φ)` | J = AT²e^{−φ/kT} — why 1400 K | added |
| `thermionic_ideal_efficiency(...)` | refuses φ_collector ≥ φ_emitter | §12.6.1 |
| `betavoltaic_power(Bq, eV, η)` | the one device with no Carnot bound | §12.9.2 |
| `RADIONUCLIDE_SOURCES`, `SNAP_GENERATORS`, `SPACE_REACTORS`, `CONVERTER_TYPES` | Tables 12.1–12.3 | — |

## Use
```python
from direct_conversion import (specific_power, power_after, mission_sizing,
                               fuel_mass_for_power, thermoelectric_efficiency,
                               carnot_efficiency, zt_for_efficiency,
                               richardson_current, betavoltaic_power, CI_TO_BQ)

specific_power(17.1, 5.495)          # 0.557 W/g -- Table 12.2 prints 0.558
power_after(47.0, 87.7)              # 0.69 -- Voyager 1's 238Pu today

mission_sizing(100.0, 0.25)[0]       # ('210Po', 18 g) for a 90-day mission
mission_sizing(100.0, 5.0)[0]        # a different isotope entirely

thermoelectric_efficiency(1.0, 1300.0, 500.0)   # 0.142 -- 23% of Carnot
zt_for_efficiency(0.20, 1300.0, 500.0)          # ZT = 1.78 needed
zt_for_efficiency(0.62, 1300.0, 500.0)          # raises: that is Carnot

richardson_current(800.0, 2.5)       # 1.4e-8 A/cm2 -- nothing
richardson_current(1800.0, 2.5)      # 39 A/cm2 -- hence "in excess of 1400 K"
betavoltaic_power(CI_TO_BQ, 5670.0)  # 6.7e-7 W per curie of tritium
```

## Run
```bash
cd code
python3 direct_conversion.py        # demo: Table 12.2's checks, isotope choice, the converters
python3 test_direct_conversion.py   # tests  ->  "All 10 tests passed."
cd ../figures && python3 make_figures.py
```

## Files
- `notes.md` — everything here is still a heat engine → the ZT penalty → why
  thermionics need 1400 K → the isotope trade → Table 12.2's eighteen internal
  checks → the flight record, with a "Where this goes" map and a note on what the
  module adds.
- `code/direct_conversion.py`, `code/test_direct_conversion.py` (stdlib only).
  `zt_for_efficiency` **refuses** a target at or above Carnot, because no ZT
  reaches it and a bisection would return a plausible-looking bound instead;
  `thermionic_ideal_efficiency` refuses a collector work function above the
  emitter's, which produces no voltage at all.
- `problems/problems.md` — 6 worked problems with numeric `*Check:*` lines.
- `figures/` — specific power against half-life beside the decay curves, the ZT
  penalty against three Carnot limits, the Richardson exponential beside the
  converter landscape, and the space-reactor flight record.
- `refs.md` — page-verified citations; the three relations the chapter needs and
  omits; and the eighteen internal checks that establish Table 12.2.
