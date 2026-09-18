# NE-10 — Fusion and nucleosynthesis

Tenth module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`), and the last of Chapter 6. Covers **§6.7** (printed
pp. 163–173) of Shultis & Faw, 3rd ed.: the candidate fusion fuels, thermonuclear
temperatures and the three confinement schemes, D–T and tritium breeding, the
proton–proton chain and the CNO cycle, helium and advanced burning up to the iron
peak, stellar death, and nucleosynthesis by the s- and r-processes. The **Gamow
peak** is added — `list_NE.txt` puts it in scope and S&F do not derive it.

- **Prerequisites:** `~NE-08` (the Coulomb barrier, which is the entire
  difficulty), `~NE-03` (the binding-energy curve and its ⁶²Ni peak), `~NE-05`
  (the β⁺ mass correction, needed throughout stellar hydrogen burning),
  `~NE-09` (the other slope of the same curve).
- **Cross-links:** `~NE-24` (fusion reactors — the Lawson criterion is this
  module made quantitative), `~NE-13` (cross sections turn the Gamow peak into
  ⟨σv⟩), `~NE-14` (whether the alpha deposits its 3.5 MeV before leaving),
  `~NE-07` (the ⁵⁶Ni→⁵⁶Co→⁵⁶Fe chain behind a Type Ia light curve), `~NE-02`
  (the shell effects the r- and s-process abundance peaks reveal).

## Scope
Fusion beats fission per nucleon by a factor of four — D–T gives 17.6 MeV from
five nucleons — and the fuel is free and effectively infinite. The obstacle is
entirely the Coulomb barrier: small in absolute terms but payable by *every*
reacting pair, and the only scalable currency is heat. Classically that means
$3\times10^{9}$ K, two hundred times the sun's core. Fusion happens anyway
because the reactants **tunnel**: the rate is the product of a falling Maxwellian
and a rising Gamow factor, peaked at $E_0=[E_G(kT)^2/4]^{1/3}$ — 31 keV for D–T
at a 10 keV plasma, a tenth of the barrier. Since $E_G\propto(Z_1Z_2)^2$ sits
inside a square root inside an exponential, charge is punished ferociously, which
is why every experiment runs D–T despite having to breed its own tritium. Stars
solve confinement by being enormous and slow: the sun's p–p bottleneck is
weak-force-mediated, its core power density is 283 W/m³ — less than a compost
heap — and it lasts ten billion years. Fusion builds elements to the iron peak
and stops; everything heavier is neutron capture, s- and r-process.

## Operations — `code/fusion.py`

| call | meaning | reference |
|------|---------|-----------|
| `q_value(reactants, products, table, n_positrons)` | Q from neutral-atom masses, with the β⁺ correction | §6.7, `~NE-05` |
| `FUSION_REACTIONS`, `TRITIUM_BREEDING` | the seven candidate fuels; ⁶Li and ⁷Li breeding | p. 163–164 |
| `reaction_product_energies(Q, m1, m2)` | inverse-mass split — D–T gives 3.54 / 14.05 MeV | Eq. (6.46) |
| `thermal_energy(T)`, `mean_thermal_energy(T)`, `temperature_for_energy(E)` | $kT$, $3kT/2$, and the inverse | §6.7.1 |
| `barrier_temperature(Z1, A1, Z2, A2)` | where $3kT/2$ = the Coulomb barrier — $3\times10^{9}$ K | §6.7 + `~NE-08` |
| `gamow_energy(Z1, A1, Z2, A2)` | $E_G=2\mu c^2(\pi\alpha Z_1Z_2)^2$ | added — see `refs.md` |
| `tunnelling_probability(E, ...)` | $\exp(-\sqrt{E_G/E})$ | added |
| `gamow_peak_energy(T, ...)`, `gamow_peak_width(T, ...)` | $E_0=[E_G(kT)^2/4]^{1/3}$; $\Delta=(4/\sqrt3)\sqrt{E_0kT}$ | added |
| `PP_CHAIN`, `PP_MULTIPLICITY`, `pp_chain_energy(include_annihilation)` | 24.69 MeV nuclear / 26.73 MeV with annihilation | Eq. (6.47) |
| `CNO_CYCLE` | the catalytic route, same net Q | Eq. (6.48) |
| `HELIUM_BURNING`, `ADVANCED_BURNING` | triple-alpha and the ladder to silicon | pp. 168–169 |
| `energy_per_deuteron()` | 11.9 MeV — d–d burned fully to ⁴He | Example 6.6 |
| `SUN`, `solar_mass_loss_rate`, `solar_helium_rate`, `radiant_flux`, `core_power_density` | 4.45e9 kg/s, 9.3e37 He/s, 1415 W/m², 283 W/m³ | §6.7.2 |
| `deuterium_atoms(g)`, `fusion_energy_of_water(g)` | the fuel supply | §6.7.1 |
| `BOOK_Q_ERRATA`, `SUN_ERRATA` | two corrected printed values | see `refs.md` |

## Use
```python
from fusion import (q_value, gamow_energy, gamow_peak_energy, tunnelling_probability,
                    barrier_temperature, temperature_for_energy, reaction_product_energies,
                    pp_chain_energy, energy_per_deuteron, core_power_density,
                    fusion_energy_of_water, atomic_mass, M_N_U)

q = q_value([(2,1), (3,1)], [(4,2), (1,0)])        # 17.589 MeV  -- D + T
reaction_product_energies(q, atomic_mass(4,2), M_N_U)   # (3.54, 14.05) -- only 20% stays

q_value([(1,1), (1,1)], [(2,1)], n_positrons=1)    # 0.420 MeV, not 1.442 -- see NE-05
pp_chain_energy(include_annihilation=False)        # 24.687 MeV (nuclear)
pp_chain_energy()                                  # 26.731 MeV (S&F's 26.72)

T = temperature_for_energy(0.010)                  # a 10 keV plasma
barrier_temperature(1, 2, 1, 3)                    # 3.4e9 K  -- classically hopeless
gamow_peak_energy(T, 1, 2, 1, 3) * 1e3             # 30.9 keV -- where it actually happens
gamow_energy(1, 1, 5, 11) / gamow_energy(1, 2, 1, 3)    # 19x  -- why p-11B is hard

core_power_density()                               # 283 W/m3 -- less than a compost heap
fusion_energy_of_water(236.6) / 1e4 / 86400        # 5.2 days of a 10 kW house
```

## Run
```bash
cd code
python3 fusion.py        # demo: fuels, Gamow peaks, the pp chain, the sun
python3 test_fusion.py   # tests  ->  "All 27 tests passed."
cd ../figures && python3 make_figures.py
```

Needs `../../data_tables/B1_atomic_masses.csv`.

## Files
- `notes.md` — the fuels and why D–T wins → the 20/80 energy split → tunnelling
  and the Gamow peak → three confinement schemes → the pp chain, its two traps
  and its absurd bottleneck → building elements and the three reasons it stops at
  iron → s- and r-process → the fuel supply, with a "Where this goes" map.
- `code/fusion.py`, `code/test_fusion.py` (stdlib only). Tests recompute **every**
  Q-value printed in §6.7 from Appendix B (19 of 20 agree to <3 keV), pin the β⁺
  correction and the two pp-chain conventions, and check the stellar-burning
  ladder, the ⁸Be gap and the photodisintegration threshold.
- `problems/problems.md` — 8 worked problems (S&F Ch. 6 problems 22–25 plus four
  added: why not D–³He, the ⁸Be gap, the classical temperature, and the sun's
  power density) with numeric `*Check:*` lines.
- `figures/` — the Gamow peak as Maxwellian × tunnelling, the fuels ranked by Q
  against E_G, the alpha-capture ladder to iron, and fusion vs fission per
  nucleon with the D–T split.
- `refs.md` — page-verified citations; **two errata** (p+¹¹B's Q-value, printed
  8.08 vs 8.68; the solar core radius, internally inconsistent by 10×); the
  pp-chain convention switch; the Gamow-peak sources; and one statement about
  inertial confinement overtaken by events in 2022.
