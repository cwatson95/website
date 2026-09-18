# MACRO_EM-04 — References

Page-level citations **verified by extracting the page text** from the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Wilcox & Thron, *Macroscopic Electrodynamics: An Introduction*, **2nd ed.** | `books/macro_electrodynamics_wilcox.pdf` | PDF = printed **+ 23** |

Offset confirmed against the page text (e.g. PDF p.158 carries the Ch. 4
opening "Electrostatics in Cylindrical and Spherical Coordinates" with
printed 135 on the next page; PDF p.203 carries printed "180", the §4.16
Exercises header). The book works in **Gaussian units**. Chapter 4 spans
printed pp. 135–202 (body 135–178, Going Deeper §4.15 p. 179, Exercises
§4.16 pp. 180–202).

## Section map (verified from the section headers)

| § | Title (short) | Printed pp. | PDF pp. |
|---|---|---|---|
| 4.1 | Cylindrical coordinates and Bessel functions | 135–140 | 158–163 |
| 4.2 | Completeness of Bessel functions | 141–142 | 164–165 |
| 4.3 | Zeros and orthogonality | 142–145 | 165–168 |
| 4.4 | Reduced Green function, conducting cylinder | 146–148 | 169–171 |
| 4.5 | Cylinder as a boundary value problem | 148–149 | 171–172 |
| 4.6 | Modified Bessel functions; asymptotics | 149–151 | 172–174 |
| 4.7 | Free-space Green function via Wronskian | 151–155 | 174–178 |
| 4.8 | Conducting wedge | 155–157 | 178–180 |
| 4.9 | Schwinger's construction of $Y_{\ell m}$ | 157–165 | 180–188 |
| 4.10 | Orthogonality of spherical harmonics | 165–166 | 188–189 |
| 4.11 | Coulomb expansion; completeness | 166–169 | 189–192 |
| 4.12 | Green function for concentric spheres | 170–172 | 193–195 |
| 4.13 | Sphere in a uniform field via $G$ | 173–174 | 196–197 |
| 4.14 | Eigenfunction expansions | 175–178 | 198–201 |
| 4.15 | Going Deeper | 179 | 202 |
| 4.16 | Exercises (49) | 180–202 | 203–225 |

## Topic → location (chapter body)

| Topic (code symbol) | Eq. | Printed p. | PDF p. |
|---|---|---|---|
| generating function; Taylor series (`jm_taylor`) | (4.7)–(4.8) | 137 | 160 |
| integral representations (`jn_intrep_413/415/416`) | (4.13), (4.15)–(4.16) | 138 | 161 |
| Bessel recursions incl. $\frac d{dt}[t^{m+1}J_{m+1}]$ (`int_rho_pow_jm`) | (4.24)–(4.28) | 140 | 163 |
| addition theorem / completeness (`addition_j0_series`, `weber_gauss_*`) | (4.37)–(4.39) | 141–142 | 164–165 |
| Dirichlet zeros $x_{mn}$; norms (`J1m_fn`) | (4.44)–(4.58) | 142–144 | 165–167 |
| normalized $\mathcal J_{1m}$; orthogonality/completeness | (4.67), (4.69)–(4.72) | 145–146 | 168–169 |
| Green equation; capped-cylinder kernel (`g_plates_z`-type) | (4.73)–(4.79) | 146–148 | 169–171 |
| top-plate BVP solution | (4.80)–(4.82) | 148 | 171 |
| separation-of-variables rerun | (4.83)–(4.91) | 148–149 | 171–172 |
| $I_\nu$, $K_\nu$, Hankel functions | (4.92)–(4.96) | 150 | 173 |
| asymptotics; zero spacing (4.98) (`bessel_zero_asymptotic`) | (4.97)–(4.107) | 150–151 | 173–174 |
| delta expansion; $z$-reduced free $g$; (4.120) (`coulomb_cylJ`) | (4.108)–(4.120) | 152–153 | 175–176 |
| $\rho$-reduced form; $I_mK_m$ (`g_free_cyl`, `G_cyl_reduced_rho`) | (4.121)–(4.125) | 153–154 | 176–177 |
| Wronskian recipe (`g_in_cyl`, `g_out_cyl`, `g_toroid`) | (4.128)–(4.130) | 155 | 178 |
| wedge: sine expansion, powers, kernels (`wedge_series`) | (4.131)–(4.143) | 155–157 | 178–180 |
| Schwinger construction; $(\vec a\cdot\vec r)^\ell$ identity (`ylm`) | (4.145)–(4.168) | 158–160 | 181–183 |
| Rodrigues; Legendre recursions (`legendre_explicit`) | (4.179)–(4.182) | 162 | 185 |
| explicit $Y_{\ell m}$; tables | (4.185); Tables 4.1–4.3 | 162–164 | 185–187 |
| $Y_{\ell m}$ orthogonality | §4.10 | 165 | 188 |
| Legendre generating function (`test_p27`) | (4.204)–(4.205) | 167 | 190 |
| Coulomb expansion (`sphere_int_coulomb`) | (4.215) | 168 | 191 |
| completeness; addition theorem; resolved expansion | (4.219)–(4.225) | 169 | 192 |
| concentric-sphere radial problem (`gN_shell` analog) | (4.227)–(4.236) | 170–171 | 193–194 |
| image resummations (Kelvin, line image) (`gN_ext_sphere_closed`) | (4.238)–(4.245) | 171–172 | 194–195 |
| sphere in uniform field; $Q_\ell$, $Q_0$ (`Q0_legendre`) | (4.247)–(4.256) | 173–174 | 196–197 |
| eigenfunction orthogonality; completeness (4.267) (`sine_delta_action`) | (4.265)–(4.268) | 176 | 199 |
| 2-D worked examples | (4.273)–(4.283) | 177–178 | 200–201 |
| cylinder eigen-Green function (`G_finite_cyl_eigen`) | (4.286)–(4.287) | 178–179 | 201–202 |

## Exercises §4.16 (all worked in `problems/problems.md`)

| Exercises | Printed p. | PDF p. | Module problems |
|---|---|---|---|
| 4.1.1–4.1.4, 4.2.1 | 180–181 | 203–204 | P1–P5 |
| 4.3.1, 4.4.1 | 181–182 | 204–205 | P6–P7 |
| 4.4.2–4.4.3 | 182–183 | 205–206 | P8–P9 |
| 4.4.4, 4.6.1–4.6.2 | 183–184 | 206–207 | P10–P12 |
| 4.7.1–4.7.2 | 184–185 | 207–208 | P13–P14 |
| 4.7.3–4.7.4 | 185–186 | 208–209 | P15–P16 |
| 4.7.5–4.7.6 | 186–187 | 209–210 | P17–P18 |
| 4.8.1–4.8.3 | 187–189 | 210–212 | P19–P21 |
| 4.8.4–4.8.5 | 189 | 212 | P22–P23 |
| 4.9.1–4.9.2 | 190 | 213 | P24–P25 |
| 4.9.3, 4.11.1–4.11.2 | 191 | 214 | P26–P28 |
| 4.11.3–4.11.5 | 192–193 | 215–216 | P29–P31 |
| 4.11.6, 4.12.1 | 193–194 | 216–217 | P32–P33 |
| 4.12.2–4.12.3 | 195–196 | 218–219 | P34–P35 |
| 4.12.4–4.12.5 | 196 | 219 | P36–P37 |
| 4.12.6, 4.13.1–4.13.2 | 197–198 | 220–221 | P38–P40 |
| 4.13.3–4.13.4 | 198–199 | 221–222 | P41–P42 |
| 4.13.5, 4.14.1–4.14.2 | 200 | 223 | P43–P45 |
| 4.14.3–4.14.6 | 201 | 224 | P46–P49 |

Sections with **no exercises**: §4.5, §4.10, §4.15.

**Erratum noted (numerically settled):** Ex. 4.13.2(b) prints an overall
factor 2 on the odd-$\ell$ series that is inconsistent with the $-2\pi$
source normalization of its own part (a); the Cesàro-summed series equals
$Q_0(\cos\gamma)$ with coefficient $(2\ell+1)/[\ell(\ell+1)]$, no 2 (P40,
`test_p40_sphere_point_electrostatics`). Minor typo in Ex. 4.2.1(a):
$\rho'$ is defined as $|\vec x_\perp|$; it must be $|\vec x'_\perp|$.

Ch. 2–3 anchors used by the solutions: (2.98)/(2.103) Green
representations, printed 53 (PDF 76); (2.106) Neumann BC $-4\pi/S$ and §2.8
non-uniqueness, printed 53–56 (PDF 76–79); (2.115) surface delta, printed 56
(PDF 79); (2.124) 1-D convention, printed 58 (PDF 81); §2.12 capacitance
matrix, printed 63 (PDF 86); (3.30) half-space reduced $g$, printed 92
(PDF 115); §3.9 summation method, printed 109–110 (PDF 132–133); (3.144)
variational bound, printed 112 (PDF 135).

## See also
- `~MACRO_EM-03` — Ch. 3: the reduced-Green-function idea in Cartesian form,
  images (this chapter's numeric cross-checks), the §3.9 summation method
  (P19/P21), Thompson's variational bound (P13/P30).
- `~EM-04` — Griffiths-level separation of variables in these geometries.
- `~MA-11` — Sturm–Liouville orthogonality/completeness (every eigen-sum
  here); `~MA-14` — Green functions and the Wronskian jump construction;
  `~MA-08` — the PDE separation itself; `~MA-06` — the complex/log reading
  of the 2-D kernels.
- Jackson 3e Ch. 3 covers the same cylindrical/spherical expansions
  (SI-Gaussian mixed); Watson, *Theory of Bessel Functions*, for §4.15's
  deeper Bessel theory (Weber's integral, P5/P11); Schwinger et al.,
  *Classical Electrodynamics*, Ch. 18 for the (4.120)-family integrals
  (the book's own pointer in Ex. 4.14.2).
