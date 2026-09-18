# MACRO_EM-03 — References

Page-level citations **verified by extracting the page text** from the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Wilcox & Thron, *Macroscopic Electrodynamics: An Introduction*, **2nd ed.** | `books/macro_electrodynamics_wilcox.pdf` | PDF = printed **+ 23** |

Offset confirmed against the page text (e.g. PDF p.110 carries printed "87",
the Ch. 3 opening; PDF p.143 carries printed "120", the §3.13 Exercises
header). The book works in **Gaussian units**. Chapter 3 spans printed
pp. 87–134 (body 87–119, Going Deeper 118–119, Exercises §3.13 120–133).

## Topic → location (chapter body)

| Topic (code symbol) | Section / content | Printed p. | PDF p. |
|---|---|---|---|
| plane image Green functions $G_D$ (3.2), $G_N$ (3.5) (`green_plane`) | §3.1 | 87–88 | 110–111 |
| 2-D line-charge Green functions (3.9)–(3.13) (`green_perp_2d`) | §3.1 | 89 | 112 |
| free $G$ by Fourier transform (3.16)–(3.21) (`gf_regulated`) | §3.2 | 90–91 | 113–114 |
| reduced Green function ODE (3.22)–(3.30) (`g_reduced_halfspace`) | §3.2 | 91–92 | 114–115 |
| Bessel inversion → images (3.31)–(3.36) (`green_halfspace_kspace`) | §3.2 | 92–93 | 115–116 |
| surface delta function (3.37)–(3.42); $\partial_nG=4\pi\sigma$ (3.40) | §3.2 | 93–94 | 116–117 |
| sphere image $q'=-aq/r'$ at $a^2/r'$ (3.43)–(3.48) (`sphere_image`, `green_sphere`) | §3.3 | 94–95 | 117–118 |
| sphere surface gradient (3.50), delta check (3.51)–(3.52) | §3.3 | 95–96 | 118–119 |
| sphere at $V$ (3.53), fixed $Q$ (3.55) (`force_sphere_*`) | §3.3 | 97 | 120 |
| grounded sphere in uniform field (3.56)–(3.61) | §3.3 | 97–98 | 120–121 |
| hemisphere forces (3.62)–(3.68) | §3.4 | 98–99 | 121–122 |
| box separation of variables (3.69)–(3.84) (`box2d_phi`) | §3.5 | 100–101 | 123–124 |
| Fourier sine series & delta expansion (3.86)–(3.89) | §3.6 | 102–103 | 125–126 |
| box reduced Green function (3.92)–(3.97); full $G_D$ (3.98) (`green_box3d`) | §3.6 | 103–104 | 126–127 |
| image-lattice reading (3.102)–(3.107), Figs. 3.9–3.10 | §3.6 | 104–106 | 127–129 |
| Madelung constant (3.108) $=-1.747564594$ (`madelung_*`) | §3.6 | 106 | 129 |
| polar separation (3.109)–(3.118) (`cyl_delta_series`) | §3.7 | 107 | 130 |
| corner/wedge solution (3.119)–(3.123), $\rho^{\pi/\beta-1}$ field (`wedge_phi`) | §3.8 | 108–109 | 131–132 |
| cylindrical halves: series (3.124)–(3.130), closed form (3.131), $\sigma$ (3.132) (`halves_*`) | §3.9 | 109–110 | 132–133 |
| Thompson theorem (general), $W[\sigma]$ (3.136)–(3.143) | §3.10 | 111–112 | 134–135 |
| variational capacitance bound $C^{-1}[\sigma]=2W/Q^2$ (3.144) (`disk_C_variational`) | §3.10 | 112–113 | 135–136 |
| Cauchy–Riemann, $u,v$ harmonic, mapping theorem (3.145)–(3.148) | §3.11 | 113–114 | 136–137 |
| $z=e^w$ strip→half-plane, wedge potential (3.149)–(3.153); $\Phi=V(1-2\phi/\beta)$ (3.152) | §3.11 | 114–115 | 137–138 |
| half-plane Green-function rederivation (3.154)–(3.160) | §3.11 | 115–116 | 138–139 |
| plate-edge fringing via $z=e^w+w$ (3.161)–(3.169) | §3.11 | 116–118 | 139–141 |
| Going Deeper (variational refs; Brown–Churchill et al. for conformal) | §3.12 | 118–119 | 141–142 |

## Exercises §3.13 (all worked in `problems/problems.md`)

| Exercises | Printed p. | PDF p. | Module problems |
|---|---|---|---|
| 3.1.1–3.1.2 | 120–121 | 143–144 | P1–P2 |
| 3.1.3–3.1.5 | 121–122 | 144–145 | P3–P5 |
| 3.2.1–3.2.2 | 122–123 | 145–146 | P6–P7 |
| 3.2.3–3.2.4 | 123–124 | 146–147 | P8–P9 |
| 3.3.1–3.3.3 | 124–125 | 147–148 | P10–P12 |
| 3.3.4–3.3.7 | 125–127 | 148–150 | P13–P16 |
| 3.3.8, 3.5.1 | 127–128 | 150–151 | P17–P18 |
| 3.5.2–3.5.4 | 128–129 | 151–152 | P19–P21 |
| 3.5.5–3.5.6, 3.6.1 | 130–131 | 153–154 | P22–P24 |
| 3.7.1, 3.8.1, 3.9.1 | 131 | 154 | P25–P27 |
| 3.9.2–3.9.5 | 132 | 155 | P28–P31 |
| 3.11.1–3.11.2 | 132–133 | 155–156 | P32–P33 |

Chapter-2 anchors used by the solutions: (2.92) surface charge, printed 50
(PDF 73); (2.98)/(2.103) Green representations, printed 53 (PDF 76);
(2.106) Neumann BC, printed 53; (2.115) surface delta, printed 56 (PDF 79);
(2.170) energy/capacitance, printed 66 (PDF 89); reciprocation theorem
Ex. 2.7.2, printed 77–78 (PDF 100–101); Ex. 2.12.5 (two-sphere lemma),
printed 83–84 (PDF 106–107).

## See also
- `~EM-04` (Griffiths-level boundary-value problems) — first uniqueness
  theorem, the classic plane image, separation in the slot, relaxation; this
  module re-derives those results as Green-function kernels and goes on to
  Robin conditions, image densities, eigenfunction kernels, and conformal
  maps.
- `~MA-08` — separation of variables for the Laplace/Poisson PDE (P18–P23).
- `~MA-11` — Sturm–Liouville orthogonality and completeness: every
  coefficient projection here (3.83), including the non-integer wedge family
  of P26.
- `~MA-14` — Green functions in general: the $-4\pi\delta$ normalization,
  reduced (1-D) Green functions, reciprocity $G(\vec x,\vec x')=G(\vec x',\vec x)$.
- `~MA-06` — complex analysis: Cauchy–Riemann, conformal invariance of
  harmonicity, the $\log$/inversion maps of P32–P33.
- Higher-level parallels: Jackson 3e Ch. 2–3 (images, eigenfunction Green
  functions, variational bounds — same material, SI-Gaussian mixed); Morse &
  Feshbach §4.7 and Brown & Churchill Ch. 10 for the conformal dictionary
  (both are the book's own §3.12 pointers).
