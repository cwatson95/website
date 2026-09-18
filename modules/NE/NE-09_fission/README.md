# NE-09 — Fission: fissile nuclides, fragments, neutrons and the energy budget

Ninth module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`). Covers **§§6.5.3–6.6** (printed pp. 150–163) of
Shultis & Faw, 3rd ed.: fissile vs fissionable vs fertile, spontaneous fission,
the fission process and fragment kinematics, fission-product decay chains and
mass yields, prompt and delayed neutrons and their spectrum, the ~200 MeV energy
budget, decay heat, and the macroscopic conversion factors.

- **Prerequisites:** `~NE-08` (the neutron reaction that starts it), `~NE-03`
  (binding energy — the 0.9 MeV/nucleon that fission harvests), `~NE-02` (the
  pairing term, which decides fissile vs fissionable), `~NE-07` (the isobaric
  decay chains the fragments fall down).
- **Cross-links:** `~NE-13` (cross sections — how *often*, not just whether),
  `~NE-19` (ν and fast fission assemble into k_eff), `~NE-20` (β is the whole of
  point kinetics; ¹³⁵Xe is the poisoning transient), `~NE-22`/`~NE-23` (1.24
  g/MWd sizes the fuel cycle; the decay-heat curve sizes emergency cooling),
  `~NE-27` (⁹⁹ᵐTc), `~NE-05` (spontaneous fission as a decay branch).

## Scope
A neutron absorbed by a heavy nucleus excites the compound nucleus by
$E^*=S_n+E_n$. Compare that with the ~6.2 MeV fission barrier and the actinides
split into **fissile** (²³³U, ²³⁵U, ²³⁹Pu, ²⁴¹Pu — all odd-$N$) and merely
**fissionable** (²³⁸U, ²³²Th, ²⁴⁰Pu — all even-$N$), because adding a neutron to
an odd-$N$ target completes a pair and releases ~1.5 MeV more. The fragments fly
apart with equal momenta, so the lighter one takes more energy (99.2 vs 68.1 MeV
on average) and the energy spectrum is bimodal; both are neutron-rich and
beta-decay down isobaric chains that include ⁹⁹ᵐTc and ¹³⁵Xe. About 200 MeV is
released — 168 in fragment kinetic energy deposited within a millimetre, 12 lost
forever to neutrinos — along with $\bar\nu\simeq2.4$ neutrons born on a Watt
spectrum peaking at 0.70 MeV and averaging 1.99 MeV. Under 1% of those neutrons
arrive late, and that fraction is the only reason a reactor is controllable.
Afterwards, decay heat falls as $t^{-1.2}$ — a power law, so it never switches
off.

## Operations — `code/fission.py`

| call | meaning | reference |
|------|---------|-----------|
| `separation_energy_n(A, Z)` | $S_n=[M(A-1,Z)+m_n-M(A,Z)]c^2$ | §6.6 |
| `excitation_energy(A_t, Z_t, E_n)` | $E^*=S_n+E_n$ of the compound nucleus | §6.6 |
| `is_fissile(A, Z)` | $E^*(E_n{=}0)>$ barrier | §6.5.3 |
| `FISSILE`, `FISSIONABLE`, `FERTILE`, `BREEDING` | the classification and the two breeding chains | §6.5.3 |
| `conserve_fission(...)`, `partner_fragment(...)` | $A_L+A_H+\nu_p=A_t+1$, $Z_L+Z_H=Z_t$ | Eq. (6.34) |
| `fragment_energy_split(E, m_L, m_H)` | $E_L/E_H=m_H/m_L$ | Eqs. (6.40)–(6.41) |
| `prompt_energy_release(...)` | $E_p$ from the mass deficit | Example 6.4 |
| `delayed_energy_release(...)` | $E_d$ down the beta chains | Example 6.5 |
| `total_neutrons(nuc, spec)`, `delayed_fraction`, `delayed_neutrons` | $\bar\nu$, $\beta$, $\bar\nu_d$ | Table 6.3 |
| `watt_spectrum(E, nuc, spec)` | $\chi(E)$, normalised | Eqs. (6.42)–(6.43) |
| `watt_peak_energy()`, `watt_mean_energy()` | 0.70 MeV mode, 1.99 MeV mean | §6.6.2 |
| `FISSION_ENERGY_MEV`, `fission_energy(recoverable)` | 207 MeV produced, 201 recoverable | Table 6.5 |
| `decay_heat_gamma/beta/total(t)` | $1.4t^{-1.2}$, $1.26t^{-1.2}$ MeV/s | Eqs. (6.44)–(6.45) |
| `fissions_per_second(P)`, `grams_per_mwd(...)`, `mwd_per_gram`, `burnup_energy` | 3.1e10 /W; 1.05 g fissioned, 1.24 g consumed per MWd | pp. 162–163 |
| `SPONTANEOUS_FISSION`, `neutrons_per_gram_second`, `spontaneous_fission_rate` | 26 spontaneously fissioning nuclides | Table 6.2 |
| `TABLE_6_2_ERRATA`, `BETA_BRANCH_PERCENT` | two corrected typos; the caption's beta branches | see `refs.md` |
| `load_atomic_masses()`, `atomic_mass(A, Z)` | Appendix B masses (2931 nuclides) | Table B.1 |

## Use
```python
from fission import (excitation_energy, is_fissile, conserve_fission,
                     prompt_energy_release, delayed_energy_release, fragment_energy_split,
                     total_neutrons, delayed_fraction, watt_peak_energy, watt_mean_energy,
                     grams_per_mwd, decay_heat_total, neutrons_per_gram_second)

excitation_energy(235, 92)          # 6.545 MeV  -- over the 6.2 MeV barrier
excitation_energy(238, 92)          # 4.806 MeV  -- 1.39 MeV short
is_fissile(235, 92), is_fissile(238, 92)          # True, False

conserve_fission(235, 92, 95, 38, 2)              # (139, 54) -- 139Xe
prompt_energy_release(235, 92, [(139, 54), (95, 38)], 2)      # 183.6 MeV
delayed_energy_release([(139, 54), (95, 38)], [(139, 57), (95, 42)])   # 24.2 MeV

total_neutrons("235U"), delayed_fraction("235U")  # 2.43, 0.0065
watt_peak_energy(), watt_mean_energy()            # 0.70, 1.99 MeV

grams_per_mwd(fission_fraction=0.85)              # 1.238 g of 235U per MWd
decay_heat_total(3600.0)                          # 1.4e-4 MeV/s per fission, an hour on
neutrons_per_gram_second("252Cf")                 # 2.3e12
```

## Run
```bash
cd code
python3 fission.py        # demo: the fissile split, Examples 6.4/6.5, the budget
python3 test_fission.py   # tests  ->  "All 24 tests passed."
cd ../figures && python3 make_figures.py
```

Needs `../../data_tables/B1_atomic_masses.csv`.

## Files
- `notes.md` — the pairing term that decides fissile vs fissionable → fragments,
  the bimodal energy spectrum and the four famous decay chains → the 200 MeV
  budget from both examples → ν, β and the Watt spectrum → 1.24 g/MWd and the
  decay-heat power law, with a "Where this goes" map.
- `code/fission.py`, `code/test_fission.py` (stdlib only). Tests reproduce
  Examples 6.4 and 6.5 and Tables 6.3, 6.4 and 6.5, and check Table 6.2's 26 rows
  against themselves through two relations the book never prints — which is how
  the two typos below were found.
- `problems/problems.md` — 8 worked problems (S&F Ch. 6 problems 16–21 plus two
  added) with numeric `*Check:*` lines.
- `figures/` — the fissile/fissionable split against the barrier, the 200 MeV
  budget produced vs recoverable, the Watt spectrum with mode and mean marked,
  and decay heat on log-log axes.
- `refs.md` — page-verified citations, and **two errata in Table 6.2** (²³⁷Np's
  fission probability, off by 100; ²⁴⁸Cm's neutron emission rate, off by 10⁵),
  each forced by the row's own other columns.
