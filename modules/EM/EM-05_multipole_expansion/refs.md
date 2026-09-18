# EM-05 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |

The offset is the one verified for the whole EM-01..EM-10 sequence (e.g. PDF p.169 carries
printed "151", the start of §3.4). Griffiths is the worked source; Jackson 3e and Schwinger
sit at a higher level (see *See also*).

## Topic → location

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| the $1/r$ expansion, Legendre $P_n$ (`multipole_potential`) | §3.4.1 *Approximate Potentials at Large Distances* (Eq. 3.95) | 151 | 169 |
| quadrupole / $n=2$ term (`quadrupole_moment`) | §3.4.1 ($n=2$ term of Eq. 3.95) | 151 | 169 |
| monopole & dipole moments (`monopole_moment`, `dipole_moment`) | §3.4.2 *The Monopole and Dipole Terms* (Eq. 3.98) | 154 | 172 |
| pure-dipole potential (`dipole_potential`) | §3.4.2 (Eq. 3.99) | 154 | 172 |
| origin-dependence of the moments | §3.4.3 *Origin of Coordinates in Multipole Expansions* | 157 | 175 |
| the dipole field (`dipole_field`) | §3.4.4 *The Electric Field of a Dipole* (Eq. 3.103–3.104) | 158 | 176 |

The explicit **traceless Cartesian tensor** $Q_{ij}=\sum_a q_a(3r_ir_j-r^2\delta_{ij})$
returned by `quadrupole_moment` is the standard packaging of the $n=2$ term of Eq. 3.95
(Griffiths develops it in a §3.4 problem; Jackson §4.1 gives the same tensor). Page 151 is
cited here for the quadrupole **term of the expansion**, which is verified; the tensor's own
equation number is not in the verified map (see flag in the build note).

## See also
- `~EM-01` (`coulomb_field`, `K_E`, `EPS0`) and `~EM-03` (`potential_point_charges`) — the
  exact field and potential the expansion is truncated from and checked against; both are
  imported directly by `multipole.py`.
- `~MA-12` *Special functions* — the Legendre polynomials $P_n$ (and, with the azimuthal
  angle, the spherical harmonics) behind the angular structure of every term; Griffiths
  derives the generating-function expansion of $1/\eta$ in §3.4.1.
- `~EM-09` *Magnetic vector potential* — the magnetic-dipole analogue
  $\mathbf A_{\text{dip}}=(\mu_0/4\pi)\,\mathbf m\times\hat{\mathbf r}/r^2$ (Gr §5.4.3,
  Eq. 5.85, p.252 / PDF 270): the same expansion, the same $3(\cdot)\hat{\mathbf r}-(\cdot)$
  field structure with **p** → **m**.
- Higher-level: Jackson, *Classical Electrodynamics* 3e, **Ch. 4** (multipoles; the
  spherical-harmonic moments $q_{\ell m}$) — `EM/Jackson…SolutionManual…pdf` holds solutions
  only locally; Schwinger, *Classical Electrodynamics* (`EM_Electricity_Magnetism/SchwingerEM.pdf`). Griffiths is
  cited as the worked source.
