# NE-08 — References

Page-level citations **verified by reading the page text** (poppler `pdftotext`)
in the PDF under `books/library/`. **Printed** = the number on the page;
**PDF** = the viewer page.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, **3rd ed.** (2017) | `NE_Nuclear_Engineering/nuclear_science_shultis_faw.pdf` | PDF = printed **+ 23** |
| Shultis & Faw, *Problem Solution Manual*, 3rd ed. (2016) | `NE_Nuclear_Engineering/nuclear_science_sol_shultis_faw.pdf` | indexed by chapter/problem |

## Topic → location

| Topic (code symbol) | Section / Eq. | Printed p. | PDF p. |
|---|---|---|---|
| Binary reactions; $X(x,y)Y$ notation | §6.1, Eq. (6.1) | 136–137 | 159–160 |
| The compound nucleus | §6.1.1, Eq. (6.2) | 137 | 160 |
| Kinematics of binary two-product reactions | §6.2 | 138 | 161 |
| Energy/mass conservation; $Q=(m_x+m_X-m_y-m_Y)c^2$ (`q_value_masses`) | §6.2.1, Eqs. (6.4)–(6.6) | 139 | 162 |
| Conservation of energy and linear momentum | §6.2.2, Eqs. (6.7)–(6.10) | 139–140 | 162–163 |
| **The master equation** — quadratic in $\sqrt{E_y}$ | Eq. (6.11) | 140 | 163 |
| Exoergic limit $E_y\to Q$ at vanishing beam energy | Eq. (6.12) | 141 | 164 |
| Reaction threshold energy | §6.3 | 142 | 165 |
| Kinematic threshold | §6.3.1, Eq. (6.13) | 142 | 165 |
| **Exact threshold** $-Q(m_y+m_Y)/(m_y+m_Y-m_x)$ (`threshold_energy`) | Eq. (6.14) | 142 | 165 |
| **Approximate threshold** $-Q(1+m_x/m_X)$ (`threshold_energy_approx`) | Eq. (6.15) | 142 | 165 |
| Coulomb barrier threshold; the repulsive force | §6.3.2, Eq. (6.16) | 143 | 166 |
| Work done against the Coulomb field (`closest_approach`) | Eq. (6.17) | 143 | 166 |
| Touching radii $b=R_o(A_x^{1/3}+A_X^{1/3})$ | Eq. (6.18) | 144 | 167 |
| **Barrier** $E_x^C\simeq1.20Z_xZ_X/(A_x^{1/3}+A_X^{1/3})$ MeV (`coulomb_barrier`) | Eq. (6.19) | 144 | 167 |
| Barrier energy is recovered in the products | §6.3.2 (closing ¶) | 144 | 167 |
| **Overall threshold** $\max(E_x^C,E_x^{th})$ (`overall_threshold`) | §6.3.3, Eq. (6.20) | 144 | 167 |
| **Example 6.1** — the $^{15}$N\* table (`minimum_product_energy`) | Example 6.1 | 144–145 | 167–168 |
| Applications of binary kinematics | §6.4 | 145 | 168 |
| $^{3}$He(n,p)$^{3}$H, the neutron-detection reaction | §6.4.1 | 145 | 168 |
| $^{7}$Li(p,n)$^{7}$Be, a neutron-production reaction ($E^C=1.236$ MeV; $E^{th}$ — see below) | §6.4.2 | 146 | 169 |
| Heavy particle scattering from an electron (`electron_recoil_energy`) | §6.4.3, Eq. (6.21) | 146 | 169 |
| $(E_e)_{\max}=4(m_e/M)E_M$ (`max_electron_recoil_energy`) | Eq. (6.22) | 147 | 170 |
| **Example 6.2** — 2.20 keV from a 4 MeV alpha | Example 6.2 | 147 | 170 |
| Reactions involving neutrons | §6.5, Eq. (6.23) | 147 | 170 |
| Neutron scattering; $A\equiv M/m_n$ | §6.5.1, Eq. (6.24) | 147 | 170 |
| **Scattered-neutron energy** (`scattering_energy`, `elastic_scattering_energy_ratio`) | Eq. (6.25) | 148 | 171 |
| Scattering angle from $E$ and $E'$ | Eq. (6.26) | 148 | 171 |
| **Example 6.3** — min/max energy; no backscatter from $A=1$ | Example 6.3 | 148 | 171 |
| $E'_{\min}=\alpha E$, $E'_{\max}=E$ (`alpha_collision`) | Eq. (6.27) | 149 | 172 |
| Average energy loss $\tfrac12(1-\alpha)E$ (`mean_energy_after_collision`) | Eq. (6.28) | 149 | 172 |
| **$\xi=1+\alpha\ln\alpha/(1-\alpha)$** (`average_log_energy_decrement`) | Eq. (6.29) | 149 | 172 |
| Collisions to slow down, $n=\xi^{-1}\ln(E_1/E_2)$ (`collisions_to_thermalize`) | Eq. (6.30) | 149 | 172 |
| **Table 6.1** — slowing of neutrons by various materials | Table 6.1 | 150 | 173 |
| Thermal neutrons; 0.025 eV, 2200 m/s at 293 K | §6.5.1 (closing) | 149–150 | 172–173 |
| Neutron capture reactions | §6.5.2 | 150 | 173 |
| Nuclear radius $R=R_oA^{1/3}$ (the source of $R_o$) | Eq. (1.7) | 9 | 32 |
| Atomic masses (`load_atomic_masses`) | Table B.1 | 570–587 | 593–610 |

## Problems (verified, S&F 3rd ed. Ch. 6)
Chapter 6's problem set begins on printed **174** (PDF 197). Problems **1–15**
belong to this module; **16–21** are fission (`~NE-09`) and **22–25** are fusion
and stellar energy (`~NE-10`).

- **Probs. 1–4** — compound-nucleus tables: $Q$, threshold, minimum product
  energy for every entry/exit channel of $^{7}$Li, $^{10}$B, $^{19}$F and
  $^{15}$N\* — printed 174–175, PDF 197–198.
- **Prob. 5** — derive Eq. (6.15) — printed 175, PDF 198. *(See the caution
  below: the stated starting point is a typo.)*
- **Prob. 6** — verify the table of Example 6.1 — printed 175, PDF 198.
- **Prob. 7** — derive Eq. (6.21) from Eq. (6.11) — printed 175, PDF 198.
- **Prob. 8** — 2 MeV neutron elastically scattered by $^{12}$C at 45° — printed 175, PDF 198.
- **Prob. 9** — inelastic scattering from the 4.439 MeV level of $^{12}$C — printed 175, PDF 198.
- **Prob. 10** — $^{16}$O(n,p)$^{16}$N, the reactor-coolant activation reaction — printed 175, PDF 198.
- **Prob. 11** — $^{18}$F from Li₂CO₃ via tritons — printed 175–176, PDF 198–199.
- **Prob. 12** — $^{18}$O(p,n)$^{18}$F, the PET cyclotron reaction — printed 176, PDF 199.
- **Prob. 13** — neutron energies from 5.5 MeV alphas on $^{7}$Li and $^{9}$Be — printed 176, PDF 199.
- **Prob. 14** — derive the inelastic min/max scattered energies — printed 176, PDF 199.
- **Prob. 15** — collisions to slow 2 MeV to 1 eV in $^{16}$O and $^{56}$Fe — printed 176, PDF 199.

Worked solutions for most chapter problems are in the authors' solution manual,
`nuclear_science_sol_shultis_faw.pdf`, indexed by chapter and problem number.

## Two conventions worth pinning down

**The nuclear-radius coefficient.** S&F write the barrier both ways — as
$Z_xZ_Xe^2/4\pi\epsilon_0 b$ with $b=R_o(A_x^{1/3}+A_X^{1/3})$ [Eqs. (6.17)–(6.18)],
and as the numerical form $E_x^C\simeq1.20Z_xZ_X/(A_x^{1/3}+A_X^{1/3})$ MeV
[Eq. (6.19)], without stating $R_o$ at the point of use. Back-solving,
$$R_o=\frac{e^2/4\pi\epsilon_0}{1.20\ \text{MeV}}=\frac{1.43996}{1.20}=1.200\ \text{fm},$$
the value of Eq. (1.7). This module therefore uses `R0_FM = 1.2`, and
`test_barrier_matches_the_books_1_20_mev_form` checks the two forms agree and
reproduces the authors' own worked values (1.994, 2.111 and 1.236 MeV). Using the
1.4 fm sometimes quoted for the nuclear-force radius would make every barrier 17%
low and break Example 6.1. `~NE-04`'s `coulomb_barrier_mev` was corrected to match.

**$E_x^C$ is a laboratory energy.** Eq. (6.17) is derived as the work done by the
projectile against a target treated as fixed, so $E_x^C$ is what the *beam* must
carry, and Eq. (6.20) compares it directly with the laboratory threshold
$E_x^{th}$. That is what `overall_threshold` implements. A more careful treatment
would require the *centre-of-mass* energy to reach the barrier, raising the
laboratory requirement by $(1+m_x/m_X)$ — a 50% increase for $\alpha+^{9}$Be. The
book does not take that step, and neither does this module, so that the published
Example 6.1 values are reproduced exactly; the refinement matters when the
projectile is not light compared with the target.

## An erratum: the $^{7}$Li(p,n)$^{7}$Be threshold

S&F §6.4.2 (printed 146) states that for $^{7}$Li(p,n)$^{7}$Be "the kinematic and
Coulombic-barrier threshold energies are, respectively, **1.875** and 1.236 MeV".
The Coulomb value checks out exactly ($1.20\times3/(1+7^{1/3})=1.2359$). The
kinematic one does not. Using the book's own Appendix B masses,
$$Q=(1.0078250+7.0160040)-(1.0086649+7.0169292)\,\text{u}\times931.494=-1.6442\ \text{MeV},$$
which is the $-1.644$ MeV the same paragraph quotes, and then
$$E_p^{th}=1.6442\left(1+\frac{1.0078250}{7.0160040}\right)=1.8804\ \text{MeV}$$
from Eq. (6.15) — and 1.8803 MeV from the exact Eq. (6.14), so the discrepancy is
not the approximation. Recovering 1.875 would need $Q=-1.6395$ MeV.

**1.880 MeV is the correct figure**, and independently so: the $^{7}$Li(p,n)
threshold is one of the standard calibration points for proton-beam energy in
neutron metrology, accepted at 1.8804 MeV. The book's 1.875 is a slip of 0.3%.
`test_known_thresholds` asserts 1.8803 rather than the printed value.

The reaction is also a good illustration of Eq. (6.20) in the opposite sense to
Example 6.1: here the *kinematic* threshold (1.880) exceeds the Coulomb one
(1.236), so the barrier never binds.

## A typo in Problem 5

The book asks the reader to "start with **Eq. (6.17)** and derive Eq. (6.15)".
Eq. (6.17) is the Coulomb work integral $W_C=Z_xZ_Xe^2/4\pi\epsilon_0b$ and has no
bearing on the kinematic threshold. The intended starting point is **Eq. (6.14)**,
the exact threshold, from which Eq. (6.15) follows in one substitution
($m_y+m_Y\simeq m_x+m_X$). `problems/problems.md` P1 does it that way and flags
the discrepancy.

## Cross-module dependencies
- **`~NE-04`** — $Q$-values, including `threshold_energy_naive`, which returns
  $|Q|$ and is deliberately named; this module supplies the correction.
- **`~NE-03`** — binding and separation energies behind the masses used here.
- **`~CM-06`**, **`~RE-06`** — two-body kinematics and frame transformations;
  the centre-of-mass split of §6.2 is the classical-mechanics result applied.
- **`../data_tables/`** — `B1_atomic_masses.csv` (2931 nuclides) for every mass.

## Further reading
- Krane, *Introductory Nuclear Physics*, §11.2 — the same kinematics with the
  relativistic corrections retained, and the invariant-mass route to the
  threshold, which is cleaner than eliminating $E_Y$ by hand.
- Mayo, *Introduction to Nuclear Concepts for Engineers* (1998) — S&F's cited
  source for the derivation of $\xi$ [Eq. (6.29)].
- Lamarsh & Baratta, *Introduction to Nuclear Engineering*, §3.5 — the moderating
  ratio $\xi\Sigma_s/\Sigma_a$, the figure of merit that $\xi$ alone is not.
- Eisberg & Resnick, *Quantum Physics* (1985) — S&F's cited source on barrier
  tunnelling, the effect that makes fusion possible below the classical barrier
  (`~NE-10`).
