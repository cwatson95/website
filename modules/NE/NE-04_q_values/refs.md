# NE-04 — References

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
| Nuclear reactions, notation $X(x,y)Y$ (`parse_reaction`) | §4.4 | 88 | 111 |
| Examples of binary reactions; multiple reaction outcomes | §4.5, §4.5.1 | 88–89 | 111–112 |
| Energy conservation including rest mass | Eq. (4.16) | 90 | 113 |
| **Definition** $Q$ = (KE of products) − (KE of reactants) | Eq. (4.17) | 90 | 113 |
| **Q from rest masses** (`q_value`, `q_value_reaction`) | Eq. (4.18) | 91 | 114 |
| Exothermic ($Q>0$) vs endothermic ($Q<0$); endothermic reactions need a threshold (`is_exothermic`, `threshold_energy_naive`) | §4.6 | 91 | 114 |
| Binary reaction $x+X\to Y+y$ | Eq. (4.19) | 91 | 114 |
| Q-values for radioactive decay | §4.6.2 | 91 | 114 |
| **Charge conservation and the electron trap**; $^{16}$O$(n,p)^{16}$N done wrong | Eqs. (4.22)–(4.23) | 91–92 | 114–115 |
| The neutral-atom substitution rule (`PARTICLES`, `species_mass_u`) | Eqs. (4.24)–(4.25) | 92 | 115 |
| **Example 4.4** — $^{9}$Be$(\alpha,n)^{12}$C and $^{16}$O$(n,\alpha)^{13}$C, with mass tables | Ex. 4.4 | 92 | 115 |
| Special case for changes in the proton number | §4.7.1 | 93 | 116 |
| Q-value for reactions producing **excited** nuclei (`q_value_excited`) | §4.8 | 93 | 116 |
| Measured atomic masses (`load_atomic_masses`) | App. B | 570–587 | 593–610 |

## Problems (verified, S&F 3rd ed. Ch. 4)
Chapter 4's problem set begins on printed **94** (PDF 117); problems 1–4 are on
that page and 5 onward on printed 95 (PDF 118). The ones belonging to this module:

- **Prob. 1** — complete four reactions by conservation of nucleons: $^{238}$U$(n,?)$, $^{14}$N$(n,?)^{}+p$, $^{226}$Ra$\to(?)+\alpha$, $(?)\to{}^{230}$Th$+\alpha$ — printed 94, PDF 117.
- **Prob. 5** — net energy released by $^2$H$(d,n)^3$He and $^2$H$(t,n)^4$He — printed 95, PDF 118.

Problems 2, 3, 4, 6, 7, 8, 9 and 10 concern binding and separation energies and
belong to `~NE-03`.

Worked solutions for most chapter problems are in the authors' solution manual,
`nuclear_science_sol_shultis_faw.pdf`, indexed by chapter and problem number.

## A note on scope
This module computes Q-values for reactions in which **neutron and proton numbers
are separately conserved**, which is where S&F's neutral-atom substitution rule
applies cleanly. Beta decay, electron capture and positron emission change the
proton number without a matching free charged particle, and each needs its own
electron-mass correction; they are handled in `~NE-05` (S&F §5.4).

The threshold returned by `threshold_energy_naive` is deliberately the naive
$|Q|$. The true kinematic threshold includes the recoil that momentum
conservation forces on the products and is larger by roughly $(1+m_x/m_X)$;
it is derived in `~NE-08` (S&F §6.3).

## Cross-module dependencies
- **`~NE-03`** — binding energies; `q_from_binding_energies` is the same Q-value
  computed as $\sum BE(\text{products})-\sum BE(\text{reactants})$, and the
  $(n,\gamma)$ Q-value *is* the product's neutron separation energy.
- **`~NE-02`** — the pairing term, which is why $S_n$ and hence the capture
  Q-value alternates between even-$A$ and odd-$A$ actinide targets, and therefore
  why $^{235}$U is fissile and $^{238}$U is not.
- **`../data_tables/`** — `B1_atomic_masses.csv` for every mass used here;
  `C1_thermal_neutron_cross_sections.csv` for the cross sections that decide
  whether an energetically allowed reaction actually happens.

## Further reading
- Krane, *Introductory Nuclear Physics*, §11.2 — Q-values and reaction kinematics,
  including the threshold derivation S&F defers to Ch. 6.
- Lamarsh & Baratta, *Introduction to Nuclear Engineering*, §3.4 — the same
  neutral-atom bookkeeping, worked for the decay modes of `~NE-05`.
