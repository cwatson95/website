# MACRO_EM-06 — References

Page-level citations **verified by extracting the page text** from the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Wilcox & Thron, *Macroscopic Electrodynamics: An Introduction*, **2nd ed.** | `books/macro_electrodynamics_wilcox.pdf` | PDF = printed **+ 23** |

Offset confirmed against the page text (e.g. PDF p.290 carries printed
"267", the Ch. 6 opening; PDF p.339 carries printed "316", the §6.15
Exercises header). The book works in **Gaussian units**. Chapter 6 spans
printed pp. 267–336 (body 267–314, Going Deeper 315, Exercises §6.15
316–336).

## Topic → location (chapter body)

| Topic (code symbol) | Section / content | Printed p. | PDF p. |
|---|---|---|---|
| wire-element force/field table; Biot–Savart (6.7)–(6.10) (`loop_B_3d`) | §6.1 | 268–270 | 291–293 |
| loop–loop force symmetric form (6.6); parallel wires (6.11)–(6.21) | §6.1 | 270–272 | 293–295 |
| volume currents (6.22)–(6.26); $\nabla\cdot B=0$ (6.27); Lorentz force (6.30) | §6.2 | 273 | 296 |
| $\nabla\cdot J=0$ (6.34); $\nabla\times B=4\pi J/c$ (6.35) | §6.2 | 274 | 297 |
| Ampère's law (6.36) (`wire_B_phi`) | §6.3 | 275 | 298 |
| gauge freedom (6.39); Coulomb gauge (6.41); $A=\frac1c\int J/g$ (6.42) (`loop_A_3d`) | §6.3 | 275–276 | 298–299 |
| surface-current jump (6.43); sheet consistency, $\pm2\pi K/c$ (6.44)–(6.50) (`sheet_B`) | §6.4 | 276–278 | 299–301 |
| Stokes transform (6.51) (`stokes_transform_*`) | §6.5 | 278 | 301 |
| $B=\frac Ic\nabla\Omega'$ + membrane delta (6.52)–(6.56) | §6.5 | 279 | 302 |
| $\nabla\times B$ restored (6.57); Ampère by linking (6.58) | §6.5 | 280 | 303 |
| on-axis loop $\Omega$ (6.59)–(6.60); $B_z$ (6.62); far field (6.63)–(6.66) (`loop_Bz_axis`, `solid_angle_disk_axis`) | §6.6 | 281–282 | 304–305 |
| $\Omega$ definition (6.67)–(6.69); surface independence (`solid_angle_disk_quad`) | §6.6 | 283 | 306 |
| cylindrical Green expansion (6.70); disk integral (6.72); $\Omega$ Bessel form (6.73) (`solid_angle_disk_bessel`) | §6.6 | 283–284 | 306–307 |
| step function $H(\rho)$ (6.74)–(6.81) | §6.6 | 284–285 | 307–308 |
| loop $B_\rho,B_z$ Bessel integrals (6.83)–(6.84) (`loop_B_bessel`); delta bookkeeping (6.85)–(6.94) | §6.6 | 285–286 | 308–309 |
| $A_\phi$ in spherical harmonics (6.95)–(6.113) | §6.7 | 286–289 | 309–312 |
| loop $B_r$ series (6.119); radial derivative (6.120); $B_\theta$ (6.121) (`loop_Br_series`, `loop_Bth_series`) | §6.7 | 289–290 | 312–313 |
| multipole expansion of $A$ (6.122)–(6.123); $\int J=0$ (6.124) | §6.8 | 290–291 | 313–314 |
| $m=\frac1{2c}\int x\times J$ (6.129); $A=m\times x/r^3$ (6.130); loops (6.131) (`circuit_moment`) | §6.8 | 291–292 | 314–315 |
| directed area $m=\frac IcS$ (6.133)–(6.134) (`saddle_moment`) | §6.8 | 292–293 | 315–316 |
| $\nabla_i\nabla_j\frac1r$ delta identity (6.139), box proof (6.140)–(6.146) (`gradgrad_1r_box`) | §6.8 | 293–294 | 316–317 |
| electric dipole delta field (6.147); $\rho=-p\cdot\nabla\delta$ (6.150) | §6.8 | 294–295 | 317–318 |
| magnetic dipole $B_m$ with $\frac{8\pi}3m\delta$ (6.152); $J_m$ (6.153) (`dipole_B`, `dipole_ball_integral`) | §6.8 | 295 | 318 |
| dipole spherical components (6.154)–(6.156); $m=I\pi a^2/c$ (6.157) | §6.8 | 295–296 | 318–319 |
| force expansion (6.162)–(6.169); $F=\nabla(m\cdot B)$ (6.170); $(m\cdot\nabla)B$ (6.171) (`force_grad_mB`) | §6.9 | 296–297 | 319–320 |
| $U=-m\cdot B$ (6.172); Stern–Gerlach aside; torque (6.174)–(6.177) | §6.9 | 297–298 | 320–321 |
| bulk force split (6.187)–(6.194); $J_{\rm eff},K_{\rm eff}$ (6.195)–(6.196) | §6.10 | 300 | 323 |
| $H\equiv B-4\pi M$ (6.199); $\nabla\times H$ (6.200); $B=\mu H$ (6.202)–(6.203) | §6.10 | 301 | 324 |
| para/dia/ferro, domains, hysteresis (Fig. 6.13) | §6.10 | 301–303 | 324–326 |
| boundary conditions (6.204)–(6.207); $B\leftrightarrow D$, $H\leftrightarrow E$, $\mu\leftrightarrow\epsilon$ (6.210)–(6.211) | §6.11 | 303 | 326 |
| $\mu\gg1$ piping, $\mu\to0$ expulsion (superconductors); $H=-\nabla\Phi_m$ | §6.11 | 304 | 327 |
| electrostatic image warm-up (6.212)–(6.221) | §6.12 | 305–306 | 328–329 |
| magnetostatic image ansatz (6.222)–(6.225); coefficients (6.226) (`image_coeffs_vacuum_source`) | §6.12 | 307–308 | 330–331 |
| loop $A_\phi$ Laplace form (6.227); image loop (6.228)–(6.229) (`loop_A_bessel`) | §6.12 | 308–309 | 331–332 |
| image force on loop (6.230)–(6.237) (`loop_image_force`); $d\gg a$ limit (6.238)–(6.239); dipole check (6.240)–(6.245) | §6.12 | 309–310 | 332–333 |
| $d\Phi_m=dm\cdot x/r^3$ (6.246)–(6.253) | §6.13 | 311–312 | 334–335 |
| $\Phi_m$ surface+volume form (6.255) (`disk_phim_quad`) | §6.13 | 312 | 335 |
| magnetized sphere: $H(0)$ (6.256)–(6.259); interior $H,B$ (6.260)–(6.264) (`A_magnetized_sphere`) | §6.13 | 312–314 | 335–337 |
| exterior dipole (6.265)–(6.267); $K_{\rm eff}=cM_0\sin\theta\,\hat e_\phi$ (6.268) | §6.13 | 314 | 337 |
| Going Deeper: magnetic-materials references | §6.14 | 315 | 338 |

## Exercises §6.15 (all worked in `problems/problems.md`)

| Exercises | Printed p. | PDF p. | Module problems |
|---|---|---|---|
| 6.1.1, 6.3.1 | 316–317 | 339–340 | P1–P2 |
| 6.3.2, 6.4.1 | 317–318 | 340–341 | P3–P4 |
| 6.5.1, 6.6.1 | 318–319 | 341–342 | P5–P6 |
| 6.6.2–6.6.3 | 319–320 | 342–343 | P7–P8 |
| 6.6.4–6.6.5 | 320–321 | 343–344 | P9–P10 |
| 6.7.1–6.7.2 | 321 | 344 | P11–P12 |
| 6.7.3–6.7.4 | 322 | 345 | P13–P14 |
| 6.7.5, 6.8.1, 6.8.2 | 323 | 346 | P15–P17 |
| 6.8.3 | 324 | 347 | P18 |
| 6.8.4–6.8.5 | 325–326 | 348–349 | P19–P20 |
| 6.8.6, 6.9.1, 6.9.2 | 326–327 | 349–350 | P21–P23 |
| 6.10.1 | 327–328 | 350–351 | P24 |
| 6.10.2 | 328 | 351 | P25 |
| 6.11.1, 6.12.1 | 329–330 | 352–353 | P26–P27 |
| 6.12.2–6.12.3 | 330–331 | 353–354 | P28–P29 |
| 6.12.4–6.12.5 | 331–332 | 354–355 | P30–P31 |
| 6.12.6, 6.13.1 | 332–333 | 355–356 | P32–P33 |
| 6.13.2 | 333–334 | 356–357 | P34 |
| 6.13.3–6.13.4 | 334–335 | 357–358 | P35–P36 |
| 6.13.5–6.13.6 | 335–336 | 358–359 | P37–P38 |

(No exercises attach to §6.2 or §6.14; §6.15 numbering runs 6.1.1, then
6.3.1 onward.)

Cross-chapter anchors used by the solutions: cylindrical free Green
expansion (4.120) and Coulomb expansion (4.225) (quoted at (6.70)/(6.102));
modified Bessel functions §4.6 (P9); Legendre derivative identities
(4.181)–(4.183), Ex. 4.12.1 and the $P_\ell(0)$/derivative values of
Ex. 4.9.1 (P11, P34); the dielectric plane-image coefficients
(5.106)–(5.107) (quoted at (6.221)); the dielectric sphere Ex. 5.7.3 (P26);
the electrostatic sphere-image density Ex. 3.3.3 (P31's $(a/r)^5$ twin);
uniform-cone charge Ex. 2.4.4 (P10's geometry).

## Book-text caveats found while transcribing

- **Ex. 6.6.2** (P7): the far-field limit line reads "$|z|\gg\rho,a,b$" —
  the disk problem has no $a,b$; read $|z|\gg\rho,R$.
- **Ex. 6.6.3** (P8): "$H(R)$" denotes the step function in $\rho$ at $R$
  (1 for $\rho<R$, 0 for $\rho>R$), argument notation loose.
- **Ex. 6.8.5(c)** (P20): with $m_{ij}$ as defined in part (b) (which
  already carries $1/c$), the printed $A^{(q)}$ prefactor $-1/(2cr^5)$ has a
  redundant $1/c$ (dimensional check against $A=m\times x/r^3$); harmless in
  the module's $c=1$ code.
- **Ex. 6.13.2** (P34): the printed $r_<^{2n}/r_>^{2n+1}$ form with the
  stated $C_n$ is correct **outside** only; the literal interior branch
  omits the equatorial-disk source $\sigma_m=-2M_0$ (e.g. it gives
  $\Phi_m(0)=0$ instead of $-2\pi M_0a$). The corrected interior expansion
  is derived in P34 and verified by quadrature.

## See also
- `~EM-05` (Griffiths-level magnetostatics) — Biot–Savart, Ampère, vector
  potential, magnetized matter; this module re-derives that material through
  solid angles, Bessel kernels, image currents and scalar potentials.
- `~MA-08`/`~MA-11` — the special-function machinery (Legendre/Bessel
  series, orthogonality) used by every expansion here.
- `~MACRO_EM-04` — the cylindrical/spherical Green-function expansions this
  chapter consumes; `~MACRO_EM-05` — the electrostatic dielectric twins
  (images, sphere in a field) transcribed by §§6.11–6.12; `~MACRO_EM-07` —
  time dependence, Faraday, and the monopole use of the multivalued
  $\Omega$ (§7.8).
- Higher-level parallels: Jackson 3e Ch. 5 (magnetostatics, images,
  magnetized sphere — SI/Gaussian mixed); Landau–Lifshitz ECM Chs. V–VI
  (the book's own §6.14 pointer) for magnetic materials.
