# NE-08 — Binary reaction kinematics, thresholds and the Coulomb barrier

Eighth module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`). Covers **§§6.1–6.5** (printed pp. 136–153) of Shultis
& Faw, 3rd ed.: the compound nucleus, two-body energy/momentum conservation, the
kinematic threshold, the Coulomb barrier and the overall threshold, heavy-particle
scattering from an electron, and elastic neutron scattering with its
moderation consequences.

- **Prerequisites:** `~NE-04` (Q-values — this module supplies the threshold that
  `threshold_energy_naive` deliberately gets wrong), `~NE-03` (masses and binding
  energy), `~CM-06` / `~RE-06` (two-body kinematics and frame transformations).
- **Cross-links:** `~NE-09` (fission is the compound-nucleus reaction of §6.1
  taken to its extreme), `~NE-10` (the barrier of §6.3 is what stars tunnel
  through), `~NE-13` (cross sections turn "allowed" into "at this rate"; lethargy
  is the variable §6.5 makes inevitable), `~NE-14` (the 2.2 keV maximum transfer
  to an electron is the input to Bethe stopping power), `~NE-19`/`~NE-22` (ξ and
  the collision count decide moderator choice and the thermal/fast split),
  `~NE-24` (Lawson criterion).

## Scope
A positive Q-value says a reaction is *allowed*, not that it *happens*. Momentum
conservation forces the products to carry the centre-of-mass motion, so an
endoergic reaction needs $E_x^{th}=-Q(1+m_x/m_X)$, always more than $|Q|$ — 0.4%
more for a neutron on ²³⁸U, 100% more for a deuteron on a deuteron. Independently,
a charged projectile must reach the nuclear surface against Coulomb repulsion,
$E_x^C\simeq1.20Z_xZ_X/(A_x^{1/3}+A_X^{1/3})$ MeV, **whatever the sign of Q**; the
reaction needs $\max(E_x^C,E_x^{th})$. That barrier is zero for neutrons at every
target and 28 MeV for an alpha on uranium — one line of algebra that explains why
reactor physics is neutron physics and why fusion needs a star. Specialising the
same kinematics to elastic neutron scattering gives $E'/E\in[\alpha,1]$ with
$\alpha=((A-1)/(A+1))^2$, hence the energy-independent logarithmic decrement
$\xi=1+\alpha\ln\alpha/(1-\alpha)$ and a collision count $n=\xi^{-1}\ln(E_1/E_2)$:
18 collisions in hydrogen, 115 in graphite, 2172 in uranium.

## Operations — `code/binary_kinematics.py`

| call | meaning | reference |
|------|---------|-----------|
| `q_value_masses(m_x, m_X, m_y, m_Y)` | $[(m_x+m_X)-(m_y+m_Y)]c^2$ | Eqs. (6.4)–(6.6) |
| `threshold_energy(Q, m_x, m_y, m_Y)` | $-Q(m_y+m_Y)/(m_y+m_Y-m_x)$, exact | Eq. (6.14) |
| `threshold_energy_approx(Q, m_x, m_X)` | $-Q(1+m_x/m_X)$ | Eq. (6.15) |
| `cm_kinetic_energy(E, m_x, m_X)`, `cm_velocity_fraction` | $E\,m_X/(m_x+m_X)$; $m_x/(m_x+m_X)$ | §6.2 |
| `coulomb_barrier(Z_x, A_x, Z_X, A_X)` | $1.20Z_xZ_X/(A_x^{1/3}+A_X^{1/3})$ MeV | Eq. (6.19) |
| `closest_approach(E, Z_x, Z_X)` | $Z_xZ_Xe^2/4\pi\epsilon_0E$ | Eq. (6.17) |
| `overall_threshold(...)` | $\max(E_x^C,E_x^{th})$ | Eq. (6.20) |
| `minimum_product_energy(...)` | $Q+(E_x^{th})_{\min}$ | Example 6.1 |
| `electron_recoil_energy(E, M, θ)`, `max_electron_recoil_energy` | $4(m_e/M)E\cos^2\theta$ | Eqs. (6.21)–(6.22) |
| `scattering_energy(A, E, θ_s, Q, branch)` | full Eq. (6.25), incl. the inelastic double-energy region | Eq. (6.25) |
| `elastic_scattering_energy_ratio(A, θ_s)` | $E'/E$ for elastic scattering ($Q=0$) | Eq. (6.25) |
| `alpha_collision(A)`, `max_fractional_energy_loss(A)` | $\alpha=((A-1)/(A+1))^2$; $1-\alpha$ | Eq. (6.27) |
| `mean_energy_after_collision(A, E)` | $\tfrac12(1+\alpha)E$ | Eq. (6.28) |
| `average_log_energy_decrement(A)` | $\xi=1+\alpha\ln\alpha/(1-\alpha)$ | Eq. (6.29) |
| `collisions_to_thermalize(A, E1, E2)` | $\xi^{-1}\ln(E_1/E_2)$ | Eq. (6.30) |
| `recoil_energy(A, E, θ_s)`, `max_lab_scattering_angle(m_x, m_X)` | struck-nucleus energy; angular limit | §6.5.1 |
| `load_atomic_masses()`, `atomic_mass(A, Z)` | Appendix B masses (2931 nuclides) | Table B.1 |

## Use
```python
from binary_kinematics import (threshold_energy, threshold_energy_approx, coulomb_barrier,
                               overall_threshold, minimum_product_energy, alpha_collision,
                               average_log_energy_decrement, collisions_to_thermalize,
                               max_electron_recoil_energy, atomic_mass, M_N_U, q_value_masses)

Q = q_value_masses(1.0078250321, atomic_mass(7, 3), M_N_U, atomic_mass(7, 4))
Q                                       # -1.6442 MeV  -- 7Li(p,n)7Be
threshold_energy_approx(Q, 1.00783, atomic_mass(7, 3))   # 1.8803 MeV, not 1.6442
coulomb_barrier(1, 1, 3, 7)             # 1.236 MeV  -- the book's §6.4.2 value

coulomb_barrier(0, 1, 92, 235)          # 0.0  -- neutrons climb nothing
coulomb_barrier(2, 4, 92, 238)          # 28.36 MeV

alpha_collision(1), alpha_collision(238)             # 0.0, 0.9833
average_log_energy_decrement(12)                     # 0.1578
collisions_to_thermalize(12, 2.0, 0.025)             # 115.3  -- S&F Table 6.1
max_electron_recoil_energy(4.0, 4.0026) * 1e3        # 2.19 keV from a 4 MeV alpha
```

## Run
```bash
cd code
python3 binary_kinematics.py        # demo: thresholds, barriers, the moderator table
python3 test_binary_kinematics.py   # tests  ->  "All 29 tests passed."
cd ../figures && python3 make_figures.py
```

Needs `../../data_tables/B1_atomic_masses.csv`.

## Files
- `notes.md` — the compound nucleus → where the threshold comes from, via the
  centre-of-mass split → the Coulomb barrier and the overall threshold, with S&F
  Example 6.1 reproduced → heavy particle on an electron → elastic neutron
  scattering, α, ξ and Table 6.1, with a "Where this goes" map.
- `code/binary_kinematics.py`, `code/test_binary_kinematics.py` (stdlib only).
  Tests reproduce **both** of the chapter's published tables — Example 6.1
  (three reactions × five columns) and Table 6.1 (six materials × three columns) —
  plus the §6.4.1 detection-reaction energies, the §6.4.2 Coulomb threshold and
  Example 6.2's 2.2 keV. One test asserts that the §6.4.2 kinematic threshold
  does **not** match the printed 1.875 MeV; see `refs.md`.
- `problems/problems.md` — 8 worked problems (S&F Ch. 6 problems 5, 6, 8, 9, 10,
  11, 12 and 15) with numeric `*Check:*` lines.
- `figures/` — the threshold penalty against mass ratio, the barrier landscape
  against target Z for four projectiles, the elastic-scattering energy band, and
  the moderator comparison reproducing Table 6.1.
- `refs.md` — page-verified citations, the $R_o=1.2$ fm convention (back-solved
  from Eq. (6.19) and confirmed against three of the authors' worked values), a
  0.3% erratum in the §6.4.2 threshold, and a typo in Problem 5.
