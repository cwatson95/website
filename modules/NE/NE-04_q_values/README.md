# NE-04 — Nuclear reactions and Q-values

Fourth module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`). Covers **§§4.4–4.8** (printed pp. 88–94) of Shultis &
Faw, 3rd ed.: reaction notation, the Q-value, the electron-bookkeeping rule for
using atomic masses, and Q-values for excited products.

- **Prerequisites:** `~NE-03` (binding energies and the mass table), `~RE-06`
  ($E=mc^{2}$; rest-mass and kinetic-energy accounting), `~NE-02` (pairing —
  needed to see why capture Q-values alternate along an isotope chain).
- **Cross-links:** `~NE-05` (decay energetics, where the neutral-atom rule breaks
  and each beta mode needs its own electron correction), `~NE-08` (the proper
  kinematic threshold, with recoil), `~NE-09` (the fission Q-value),
  `~NE-10` (fusion Q-values and the Gamow peak), `~NE-13` ($(n,\gamma)$ Q-values
  as compound-nucleus excitation).

## Scope
Conserving total energy including rest mass gives
$$Q=\big[\textstyle\sum(\text{reactant masses})-\sum(\text{product masses})\big]c^{2},$$
positive for exothermic reactions and negative for endothermic ones. The physics
is one line; the bookkeeping is the module. Appendix B holds **atomic** masses,
so a reaction that changes the proton number must be written with every charged
particle replaced by its neutral-atom counterpart (a proton by ¹H, an alpha by
⁴He) — otherwise the electron count does not balance and $Q$ is wrong by exactly
$m_ec^{2}=0.511$ MeV per unbalanced electron. Q is antisymmetric under reversal,
additive along a chain, and equal to $\sum BE(\text{products})-\sum BE(\text{reactants})$,
which makes `~NE-03`'s $B/A$ curve the driver of nuclear energetics. An excited
product costs exactly its excitation energy, $Q^{*}=Q_{\text{gs}}-E^{*}$. And
$Q>0$ never means "easy": a charged projectile still has to cross a Coulomb
barrier of order MeV, which is why reactor physics is built on neutrons.

## Operations — `code/q_values.py`

| call | meaning | reference |
|------|---------|-----------|
| `parse_nuclide(s)`, `format_nuclide(A, Z)` | `'235U'` ↔ `(235, 92)` | §4.4 |
| `parse_reaction(s)` | `'9Be(a,n)12C'` → reactants, products | §4.4 |
| `species_ZA(s)`, `species_mass_u(s)` | shorthand → $(A,Z)$ and mass, with the neutral-atom substitution | Eq. (4.24) |
| `check_conservation(r, p)` | $(\Delta A,\Delta Z)$; must be $(0,0)$ | §4.7 |
| `q_value(r, p)` | $Q=[\sum m_R-\sum m_P]c^{2}$ | **Eq. (4.18)** |
| `q_value_reaction('X(x,y)Y')` | the same, from compact notation | Eq. (4.19) |
| `is_exothermic(r, p)` | $Q>0$? | §4.6 |
| `q_from_binding_energies(r, p)` | $\sum BE_P-\sum BE_R$ — must agree | §4.6 |
| `q_value_excited(r, p, E*)` | $Q_{\text{gs}}-E^{*}$ | §4.8 |
| `threshold_energy_naive(r, p)` | $\lvert Q\rvert$ — a **lower bound**; see `~NE-08` | §4.6 |
| `coulomb_barrier_mev(A1,Z1,A2,Z2)` | $Z_1Z_2e^{2}/4\pi\epsilon_0R$, why exothermic ≠ easy | (preview of §6.3) |

## Use
```python
from q_values import q_value_reaction, q_value, q_value_excited, coulomb_barrier_mev

q_value_reaction("9Be(a,n)12C")     # +5.7011 MeV   (S&F Example 4.4)
q_value_reaction("16O(n,a)13C")     # -2.2156 MeV   endothermic
q_value_reaction("3H(d,n)4He")      # +17.5893 MeV  D-T fusion
q_value(["235U", "n"], ["236U", "g"])   # 6.5448 MeV -- above the 6.2 MeV fission barrier
q_value(["238U", "n"], ["239U", "g"])   # 4.8062 MeV -- below it: 238U is not fissile
q_value_excited(["9Be","a"], ["n","12C"], 7.65)   # -1.9489: the Hoyle channel is closed
coulomb_barrier_mev(2, 1, 3, 1)     # 0.44 MeV -- D-T still needs 1e8 K
```

## Run
```bash
cd code
python3 q_values.py        # demo: Example 4.4, the electron trap, fusion, barriers
python3 test_q_values.py   # tests  ->  "All 15 tests passed."
cd ../figures && python3 make_figures.py
```

Needs `../../data_tables/B1_atomic_masses.csv`.

## Files
- `notes.md` — definition → the electron bookkeeping trap and S&F's substitution
  rule → worked examples → Q from binding energies, antisymmetry and additivity →
  excited products, thresholds and Coulomb barriers, with a "Where this goes" map.
- `code/q_values.py`, `code/test_q_values.py` (stdlib only). Tests reproduce
  Example 4.4, measure the 0.511 MeV cost of the electron mistake, confirm the
  mass and binding-energy routes agree, and check that $(n,\gamma)$ Q equals $S_n$.
- `problems/problems.md` — 8 worked problems (S&F Ch. 4 problems 1 and 5 plus six
  added, including why ²³⁵U is fissile and ²³⁸U is not) with numeric `*Check:*` lines.
- `figures/` — a Q-value survey, capture Q along the actinides against the fission
  barrier, excited-state channels closing, and barrier-vs-Q for five reactions.
- `refs.md` — page-verified citations to S&F §§4.4–4.8.
