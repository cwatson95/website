# MACRO_EM-05 — References

Page-level citations **verified by extracting the page text** from the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Wilcox & Thron, *Macroscopic Electrodynamics: An Introduction*, **2nd ed.** | `books/macro_electrodynamics_wilcox.pdf` | PDF = printed **+ 23** |

Offset confirmed against the page text (PDF p.226 carries printed "203", the
Ch. 5 opening; PDF p.265 carries printed "242", the §5.13 Exercises header).
The book works in **Gaussian units**. Chapter 5 spans printed pp. 203–266
(body 203–240, Going Deeper 241, Exercises §5.13 242–266).

## Topic → location (chapter body)

| Topic (code symbol) | Section / content | Printed p. | PDF p. |
|---|---|---|---|
| Taylor expansion (5.2)–(5.11); moments $q,\vec p,Q_{ij}$ (5.12), traceless (5.13) (`moments_point_charges`) | §5.1 | 203–205 | 226–228 |
| ideal charge/dipole/quadrupole fields (5.14)–(5.16); prolate/oblate | §5.1 | 205–206 | 228–229 |
| spherical moments $\rho_{\ell m}$ (5.17)–(5.20) (`rho_lm`) | §5.1 | 207 | 230 |
| charge–multipole energy (5.21)–(5.25) (`quad_energy_in_potential`) | §5.2 | 207–209 | 230–232 |
| dipole–dipole (5.27), dipole–quadrupole (5.28)/(5.29) | §5.2 | 209 | 232 |
| separable configs, $W=\sum(\rho_<)^*(\rho_>)$ (5.30)–(5.37); $\vec p$ vs $(\rho)_{1m}$ (5.38)–(5.39) (`sphere_image_W_*`) | §5.2 | 210–211 | 233–234 |
| force expansion (5.40)–(5.52); alternate form (5.53) (`force_multipole`) | §5.3 | 211–214 | 234–237 |
| $\vec P=n\vec p$ (5.56); $\rho^d_{\rm eff}$, $\sigma^d_{\rm eff}$ (5.58)–(5.59); quadrupole density (5.60) (`quad_density_check`) | §5.4 | 214–215 | 237–238 |
| $\vec D$ (5.64)–(5.65); $\chi,\epsilon$ (5.66)–(5.70) | §5.4 | 215–216 | 238–239 |
| dielectric Green theory (5.71)–(5.78): representation (5.77), symmetry (5.78) | §5.5 | 217–218 | 240–241 |
| slab reduced problem + BCs (5.79)–(5.87) (`g_halfspace_dielectric`) | §5.6 | 218–219 | 241–242 |
| half-space solution (5.88)–(5.104); image forms (5.105)–(5.107) (`two_halfspace_phi`) | §5.6 | 219–221 | 242–244 |
| $\sigma_{\rm bound}$ (5.108)–(5.111), surface delta (5.112)–(5.113); $\epsilon\to\infty,0,1$ limits | §5.6 | 222 | 245 |
| sphere radial systems (5.114)–(5.135) (`sphere_gl_solve`) | §5.7 | 223–224 | 246–247 |
| sphere kernels (5.136)–(5.141) (`sphere_G_in/out`) | §5.7 | 225 | 248 |
| induced dipole (5.142)–(5.144); interior screening (5.145)–(5.146) (`sphere_uniform_field_phi`) | §5.7 | 225–226 | 248–249 |
| $\delta W=\frac1{4\pi}\int\vec E\cdot\delta\vec D$ (5.147)–(5.159) | §5.8 | 226–227 | 249–250 |
| $W=\frac1{8\pi}\int\vec E\cdot\vec D$ for symmetric $\epsilon_{ij}$ (5.160)–(5.164); $W=\frac12\int\!\!\int\rho G_D\rho$ (5.165)–(5.168) | §5.8 | 227–228 | 250–251 |
| introducing a dielectric: $\Delta W$ (5.169)–(5.173) (`slab_deltaW`) | §5.8 | 229 | 252 |
| fixed-$Q$ vs fixed-$V$ forces (5.174)–(5.179) (`capacitor_force_fixed_*`) | §5.9 | 230 | 253 |
| bulk force, average-field rule (5.180)–(5.185) (`surface_force_from_*`) | §5.9 | 231–232 | 254–255 |
| leading-log model (5.186)–(5.194); confinement bound (5.195)–(5.197) (`leading_log_*`) | §5.10 | 232–235 | 255–258 |
| sphere–charge force, three ways (5.198)–(5.221); (5.201)/(5.202) (`sphere_charge_*`) | §5.11 | 235–239 | 258–262 |
| fluid-rise capacitor (5.222)–(5.229) | §5.11 | 239–240 | 262–263 |
| Going Deeper: dielectric materials reading list | §5.12 | 241 | 264 |

## Exercises §5.13 (all worked in `problems/problems.md`)

| Exercises | Printed p. | PDF p. | Module problems |
|---|---|---|---|
| 5.1.1–5.1.5 | 242–243 | 265–266 | P1–P5 |
| 5.1.6, 5.2.1 | 243–244 | 266–267 | P6–P7 |
| 5.2.2 | 244–245 | 267–268 | P8 |
| 5.2.3, 5.3.1 | 245 | 268 | P9–P10 |
| 5.4.1–5.4.3 | 246–247 | 269–270 | P11–P13 |
| 5.4.4–5.4.5 | 247–249 | 270–272 | P14–P15 |
| 5.6.1 | 249 | 272 | P16 |
| 5.6.2–5.6.3 | 249–251 | 272–274 | P17–P18 |
| 5.6.4–5.6.5 | 251–252 | 274–275 | P19–P20 |
| 5.6.6, 5.7.1 | 252–253 | 275–276 | P21–P22 |
| 5.7.2–5.7.3 | 253–254 | 276–277 | P23–P24 |
| 5.7.4–5.7.6 | 255 | 278 | P25–P27 |
| 5.7.7–5.7.8 | 255–256 | 278–279 | P28–P29 |
| 5.7.9–5.7.10 | 256–257 | 279–280 | P30–P31 |
| 5.7.11–5.7.12 | 257–258 | 280–281 | P32–P33 |
| 5.8.1 | 258–259 | 281–282 | P34 |
| 5.9.1 | 259 | 282 | P35 |
| 5.9.2–5.9.4 | 260–261 | 283–284 | P36–P38 |
| 5.9.5 | 261–262 | 284–285 | P39 |
| 5.9.6–5.9.8 | 262–263 | 285–286 | P40–P42 |
| 5.9.9–5.9.10 | 263–264 | 286–287 | P43–P44 |
| 5.10.1 | 264 | 287 | P45 |
| 5.11.1–5.11.3 | 265 | 288 | P46–P48 |
| 5.11.4 | 266 | 289 | P49 |

Cross-chapter anchors used by the solutions: §2.9 1-D Green function
$G=x_<(1-x_>/L)$ (2.136), printed 58–59 (PDF 81–82); §2.11 conductor
pressure $2\pi\sigma^2$; §3.1–§3.3 images and 2-D $-2\ln\rho$ Green function;
§3.2 reduced-$g$ technique; Ex. 4.2.1 Bessel addition theorem
$J_0(kD)=\sum_mJ_mJ_m e^{im\Delta\phi}$, printed 180–181 (PDF 203–204);
Ex. 4.9.1 $P_\ell(0)=(-1)^{\ell/2}(\ell-1)!!/\ell!!$, printed 190 (PDF 213);
Eq. (4.240) exterior grounded-sphere kernel, printed 172 (PDF 195);
Ex. 4.12.1 split-sphere capacitance, printed 194 (PDF 217);
Ex. 4.13.4 $C_{11},C_{12}=\frac a4\sum(\pm1)^\ell(2\ell+1)^2[\int_0^1P_\ell]^2$,
printed 199 (PDF 222).

## Errata (verified against the PDF text and numerically)

- **Ex. 5.2.2** (printed 244): interaction energy sign — printed $-\frac9{16}$,
  correct $+\frac9{16}$ (microscopic check in `test_p08_quad_quad_energy`).
- **Ex. 5.7.12** (printed 258): printed $2a^3(\epsilon-1)/(3+2\epsilon)$ —
  dimensional analysis and the bound-charge quadrature give $a^5$
  (`test_p33_induced_quadrupole`).
- Fig. 5.24 caption (printed 247): "magnetic field" → electric field.
- Fig. 5.32 caption (printed 253): credited to Exercise 5.9.10; it is the
  geometry of Exercise 5.7.1 (5.9.10 reuses it).
- Ex. 5.9.9 (printed 263): text says "Figure 5.39"; the referenced drawing is
  Fig. 5.43.

## See also
- `~EM-05`, `~EM-07`-adjacent modules — Griffiths-level multipole expansion,
  polarization, bound charge, D-field, and linear dielectrics; this module is
  the Green-function and force-calculus upgrade.
- `~MACRO_EM-03` — images, reduced Green functions, uniqueness (the methods
  §5.6 extends to dielectric interfaces).
- `~MACRO_EM-04` — cylindrical/spherical eigenfunctions, Bessel identities,
  Legendre integrals: the direct inputs of P22–P23, P30–P31.
- `~MA-11` (orthogonal expansions), `~MA-14` (Green functions) — the
  mathematics under every kernel here.
- Higher-level parallels: Jackson 3e Ch. 4 (multipoles, dielectrics,
  Clausius–Mossotti, energy in dielectrics) and Landau–Lifshitz ECM Ch. II
  (thermodynamic forces in dielectrics — the book's own §5.12 pointer).
