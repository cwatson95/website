# MACRO_EM-06 — Magnetostatics (notes)

Compact map of Wilcox & Thron 2e Ch. 6 (printed pp. 267–315; exercises §6.15,
pp. 316–336) — the results the 38 solutions in `problems/problems.md` lean
on. Page numbers are *printed* pages (PDF = printed + 23, verified; see
`refs.md`). **Gaussian units throughout**: Biot–Savart carries $1/c$, forces
carry $I/c$, and $\vec\nabla\times\vec B=\frac{4\pi}{c}\vec J$.
Griffiths-level treatment of the same physics: `~EM-05`. This chapter is the
Green-function/solid-angle upgrade, run deliberately parallel to the
electrostatics of Chs. 2–5.

## §6.1 Analogy to electrostatics (pp. 267–272)
Wire elements $I\,d\vec\ell$ replace point charges (Table 6.1, p. 268):
$d\vec F=\frac{I_1}{c}d\vec\ell_1\times\vec B_2$,
$d\vec B=\frac{I}{c}\frac{d\vec\ell'\times(\vec x-\vec x')}{|\vec x-\vec x'|^3}$.
Element–element forces violate Newton's third law ((6.1)–(6.2), Fig. 6.2) —
harmless, since only closed circuits are physical: the loop–loop force
(6.6),
$\vec F_{12}=-\frac{I_1I_2}{c^2}\oint\!\!\oint\frac{(\vec x_1-\vec x_2)\,d\vec x_1\!\cdot d\vec x_2}{|\vec x_1-\vec x_2|^3}$,
is manifestly antisymmetric. Integrated Biot–Savart (6.7)–(6.9) (three
equivalent forms: direct, gradient-cross, curl-of-integral); loop force
(6.10). Parallel wires both ways ((6.11)–(6.21)): $B=2I/c\rho$ and force per
length $-\frac{2I_1I_2}{c^2\rho}(\hat n_1\cdot\hat n_2)\hat\rho$ — **likes
attract**. Code: `loop_B_3d`, `loop_A_3d`, `wire_B`; P1 (immersed circuit)
is (6.10) plus $\int d\vec x=\vec L$.

## §6.2 General equations (pp. 273–274)
$I\,d\vec x\to\vec J\,d^3x$ (6.22); $\vec B$ from volume currents
(6.24)–(6.26); $\vec\nabla\cdot\vec B=0$ (6.27); force density (6.28) and
the Lorentz force for a moving charge (6.29)–(6.30). Curling (6.26) and
using the magnetostatic consistency condition $\vec\nabla\cdot\vec J=0$
(6.34, from charge conservation with bounded $\rho$):
$\vec\nabla\times\vec B=\frac{4\pi}{c}\vec J$ (6.35). Checked on grids in
`test_div_curl_ampere` (div/curl of the loop field, curl of the uniform-wire
field = $4\pi J/c$).

## §6.3 Ampère's law; vector potentials (pp. 274–276)
Ampère (6.36): $\oint\vec B\cdot d\vec\ell=\frac{4\pi}{c}I_{\rm enc}$ — used
directly by P2 (pinch: $B_\phi=2I\rho/ca^2$ in, $2I/c\rho$ out) and P3
(spinning+sliding cylinder = solenoid $\oplus$ fat wire). $\vec B=\vec\nabla\times\vec A$
(6.37); gauge freedom (6.39); Coulomb gauge $\vec\nabla\cdot\vec A=0$ makes
each component Poisson, $-\nabla^2\vec A=\frac{4\pi}{c}\vec J$ (6.41), solved
in free space by $\vec A=\frac1c\int d^3x'\,\vec J/|\vec x-\vec x'|$ (6.42).
Code: `wire_B_phi`, `pinch_pressure`, `spinning_cylinder_B`.

## §6.4 Surface currents (pp. 276–277)
Jump condition $\hat n\times(\vec B_2-\vec B_1)=\frac{4\pi}{c}\vec K$ (6.43)
shown consistent with the sheet Biot–Savart (6.44) via the solid-angle
density $d\Omega'=-da'\,\hat n\cdot(\vec x-\vec x')/g^3$ (6.46) and the
$\pm2\pi$ near-disk limit (6.48)–(6.49). P4 (infinite sheet
$\vec B=\pm\frac{2\pi K_0}{c}\hat y$) is the cleanest instance. Code:
`sheet_B`, `sheet_B_wires`.

## §6.5 Solid-angle formula for B (pp. 278–280)
The chapter's signature tool. The Stokes transform (6.51) (P5:
$\oint d\vec\ell\times\vec A=\int(d\vec s\times\vec\nabla)\times\vec A$)
turns the loop Biot–Savart into
$$\vec B=\frac Ic\vec\nabla\Omega'(\vec x)+\frac{4\pi I}{c}\int_{S'}d\vec s'\,\delta(\vec x-\vec x')\quad(6.56),$$
$\Omega'$ = solid angle of any spanning surface (choice-independent, p. 283);
the membrane delta restores $\vec\nabla\times\vec B=\frac{4\pi}{c}\vec J$
(6.57) and Ampère's $\pm4\pi I/c$ by linking number (6.58). Off $S'$,
$\vec B=\frac Ic\vec\nabla\Omega$ — a *scalar* potential for a vector
problem. Code: `stokes_transform_lhs/rhs`, `solid_angle_disk_quad`,
`solid_angle_rect` (arctan closed form), and the linking-sign Ampère check.

## §6.6 Circular loop via solid angle (pp. 281–286)
On-axis $\Omega=2\pi(z/\sqrt{z^2+a^2}-\mathrm{sign}\,z)$ (6.60) →
$B_z=\frac{2\pi Ia^2}{c(a^2+z^2)^{3/2}}$ (6.62); far field = dipole
(6.63)–(6.66). Exactly: (6.69) $\Omega=\partial_z\int_{S'}da'/g$ with the
cylindrical Green expansion (6.70) and the disk integral
$\int_0^a\rho'J_0\,d\rho'=\frac akJ_1(ka)$ (6.72) give
$$\Omega=-2\pi a\,\mathrm{sign}(z)\int_0^\infty dk\,J_1(ka)J_0(k\rho)e^{-k|z|}\ (6.73),$$
with the step function $H(\rho)=a\int J_1(ka)J_0(k\rho)dk$ (6.74)–(6.79)
controlling the $\mp2\pi$ disk limits (6.80)–(6.81). Gradient →
$$B_\rho=\frac{2\pi aI}{c}\mathrm{sign}(z)\!\int\!dk\,kJ_1(ka)J_1(k\rho)e^{-k|z|},\quad
B_z=\frac{2\pi aI}{c}\!\int\!dk\,kJ_1(ka)J_0(k\rho)e^{-k|z|}\ (6.83{-}6.84),$$
the sign-derivative delta and the membrane term cancelling (6.85)–(6.94).
These kernels power P6–P10: solenoid inside (P6, $e^{-kd/2}\sinh/\cosh(kz)$
kernels + $1/d^2$ end-correction), spinning disk (P7, $J_2(kR)$ via
$\int\rho^2J_1=R^2J_2/k$), solid rotating cylinder (P8, Weber–Schafheitlin
step), the $I_1K_1$ potential (P9), the spinning cone (P10 — constant
$dB_z/dz$ per slice). Code: `loop_B_bessel`, `solid_angle_disk_bessel`,
`solenoid_*`, `spinning_disk_*`, `spinning_cylinder_solid_*`, `loop_A_IK`,
`cone_Bz_tip`.

## §6.7 Circular loop directly (pp. 286–290)
Coulomb gauge + spherical harmonics: $A_\phi$ from (6.101) with the
Coulomb expansion (6.102) collapses to $m=\pm1$, giving the odd-$\ell$
series (6.113)
$A_\phi=-\frac{\pi Ia}{c}\sum_n\frac{(-1)^n(2n-1)!!}{(n+1)(2n)!!}\frac{r_<^{2n+1}}{r_>^{2n+2}}P^1_{2n+1}$,
and the fields
$$B_r=\frac{2\pi Ia}{cr}\sum\frac{(-1)^n(2n+1)!!}{(2n)!!}\frac{r_<^{2n+1}}{r_>^{2n+2}}P_{2n+1}\ (6.119),\qquad
B_\theta:\ (6.121)\ \text{two-branch}.$$
P11 rebuilds the same physics from the solid angle (Legendre series of
$\Omega$, incl. the sign-split interior form whose constant part is the
Legendre expansion of $\mathrm{sign}(z)$); P12 differentiates it into
(6.119)/(6.121). The $B_\theta$ "discontinuity" at $r=a$ is the spanning
disk's sheet, not physics (p. 290). Rotating spheres: uniform shell → P13
(uniform $\frac{8\pi a\sigma\omega}{3c}\hat z$ inside, dipole
$m=\frac{4\pi\sigma\omega a^4}{3c}$ outside), solid ball → P14 (shell
superposition), $\sigma_0\cos\theta$ shell → P15 (pure $\ell=2$: linear
interior field, quadrupole exterior). Code: `loop_Br_series`,
`loop_Bth_series`, `solid_angle_disk_series(_split)`, `rotating_shell_B`,
`rotating_solid_sphere_B`, `costheta_shell_B` (+ `_quad` twins).

## §6.8 Moments and multipoles (pp. 290–296)
Taylor-expanding (6.42): monopole term vanishes ($\int\vec J=0$, (6.124));
the antisymmetric dipole term defines
$\vec m=\frac1{2c}\int\vec x\times\vec J\,d^3x$ (6.129) —
origin-independent — with $\vec A=\vec m\times\vec x/r^3$ (6.130). For
loops: $\vec m=\frac{I}{2c}\oint\vec x\times d\vec\ell=\frac Ic\vec S$
(directed area, (6.131)–(6.134)) — P18's saddle/bent-loop moments. The
point-dipole field carries a delta:
$\nabla_i\nabla_j\frac1r=\frac{3x_ix_j-r^2\delta_{ij}}{r^5}-\frac{4\pi}{3}\delta_{ij}\delta$
(6.139, box-flux proof pp. 293–294), so
$$\vec B_m=\frac{3\vec x(\vec m\cdot\vec x)-r^2\vec m}{r^5}+\frac{8\pi}{3}\vec m\,\delta(\vec x)\ (6.152),\qquad
\vec J_m=-c\,\vec m\times\vec\nabla\delta\ (6.153)$$
(P19; contrast the electric $-\frac{4\pi}{3}\vec p\delta$ (6.147),
$\rho=-\vec p\cdot\vec\nabla\delta$ (6.150) — the latter is what P30
integrates over a surface). Spherical components (6.154)–(6.156);
$m=I\pi a^2/c$ for the loop (6.157) — P16's solenoid dipole reading.
Exercises push one order further: the cyclic identity, magnetic quadrupole
$m_{ij}=\frac2{3c}\int(\vec x\times\vec J)_ix_j$, $A^{(q)}$ (P20 — note the
book's printed $A^{(q)}$ prefactor carries a redundant $1/c$), and
$B^{(q)}$ with the 5-component symmetric traceless $s_{ij}$ matched to
P15's shell (P21). Code: `circuit_moment`, `saddle_moment`,
`bent_loop_moment`, `gradgrad_1r_box`, `dipole_ball_integral`,
`jm_moment_smeared`, `quad_moment_mij`, `A_quadrupole`, `B_quadrupole`,
`costheta_shell_sij`.

## §6.9 Forces and torques on multipoles (pp. 296–298)
Expanding $\vec F=\frac1c\int\vec J\times\vec B$ with (6.128):
$\vec F=\vec\nabla(\vec m\cdot\vec B)$ (6.170) using only
$\vec\nabla\cdot\vec B=0$; the non-overlap form $(\vec m\cdot\vec\nabla)\vec B$
(6.171) needs $\vec\nabla\times\vec B=0$ too. Potential $U=-\vec m\cdot\vec B$
(6.172) (Stern–Gerlach aside, p. 298); torque $\vec N=\vec m\times\vec B(0)$
(6.177). P22 (dipole beside a wire) and P23 (re-deriving (6.170) from the
loop force via $\oint x_ldx_j=\varepsilon_{ljm}S_m$) exercise both. Code:
`wire_dipole_force/torque`, `small_loop_force/torque`, `force_grad_mB`.

## §6.10 Magnetization and H (pp. 298–303)
Bulk force on magnetized matter from (6.187)–(6.194) splits into volume and
surface effective currents
$$\vec J_{\rm eff}=c\vec\nabla\times\vec M\ (6.195),\qquad
\vec K_{\rm eff}=c\vec M\times\hat n\ (6.196);$$
$\vec H\equiv\vec B-4\pi\vec M$ (6.199) obeys
$\vec\nabla\times\vec H=\frac{4\pi}{c}\vec J_{\rm free}$ (6.200); linear
media $\vec B=\mu\vec H$ (6.202). Para/dia/ferro survey with hysteresis
(pp. 301–303, Fig. 6.13; SI aside $B_i\equiv M/\mu_0$). P24 uses
$\vec K_{\rm eff}$ to *localize* the torque $\vec m\times\vec B_0$ on the
surface (hemisphere: dome only); P25 (dipole in a cavity / permeable
sphere: $C_1=\frac{\mu-1}{2\mu+1}$, $C_2=\frac{3\mu}{2\mu+1}$, and the
$\mu\to1/\mu$ swap) connects its bound current to P13's rotating shell.
Code: `hemisphere_torque(_quad)`, `cavity_C1C2`, `sphere_C1C2`,
`cavity_fields`, `cavity_Kb_coefficient`.

## §6.11 Boundary conditions at interfaces (pp. 303–304)
$(\vec B_2-\vec B_1)\cdot\hat n=0$ (6.204),
$\hat n\times(\vec H_2-\vec H_1)=\frac{4\pi}{c}\vec K_{\rm free}$ (6.205).
With no free currents, magnetostatics **is** electrostatics under
$$\vec B\leftrightarrow\vec D,\qquad\vec H\leftrightarrow\vec E,\qquad\mu\leftrightarrow\epsilon\ (6.210{-}6.211),$$
and $\vec H=-\vec\nabla\Phi_m$. Limits: $\mu\gg1$ pipes B-lines (H-lines meet
the surface normally, "equipotential"); $\mu\to0$ expels them (perfect
diamagnet / Type-1 superconductor — P31's boundary condition). P26
transcribes the dielectric sphere: $\vec B_{\rm in}=\frac{3\mu}{\mu+2}\vec B_0$,
$\vec M=\frac{3}{4\pi}\frac{\mu-1}{\mu+2}\vec B_0$. Code:
`perm_sphere_phim/B/M`.

## §6.12 Image method (pp. 304–310)
Electrostatic warm-up (6.212)–(6.221): $a_E=-\frac{\epsilon-1}{\epsilon+1}$,
$b_E=\frac{2}{\epsilon+1}$. Magnetostatic plane interface, source in vacuum
(6.222)–(6.226): image current $(aJ_\parallel,\,bJ_z)(x,y,-z)$ with
$$a=\frac{\mu-1}{\mu+1}=-b,\qquad \vec J^{**}=\frac{2\mu}{\mu+1}\vec J\ \text{(transmitted)}$$
— P27; embedded source → P28 ($a'=-a$). Worked loop example: $A_\phi$
Laplace kernel (6.227), image loop $I'=\frac{\mu-1}{\mu+1}I$ (6.229), force
$$F_z=-\frac{4\pi^2I^2a^2}{c^2}\frac{\mu-1}{\mu+1}\int_0^\infty dk\,k\,e^{-2kd}J_1^2(ka)\ (6.237)
\;\xrightarrow{d\gg a}\;-\frac{6\pi^2I^2a^4}{c^2(2d)^4}\frac{\mu-1}{\mu+1}\ (6.239),$$
cross-checked as $\vec\nabla(\vec m\cdot\vec B')$ (6.240)–(6.245):
paramagnets attract, diamagnets repel. Exercises extend to the dipole-layer
↔ current-loop dictionary (P29: $\vec B=\frac Ic[\vec\nabla\Omega_{\rm src}
+\frac{\mu-1}{\mu+1}\vec\nabla\Omega_{\rm img}]$), the general Green-function
representation $\Phi_m=\frac Ic\int_{S'}\partial_{n'}G(\vec x,\vec x';\mu)\,da'$
(P30), the superconducting-sphere image $\vec J^*=-(a/r)^5\vec J(a^2/r)$
(P31 — one image ring $I^*=-\frac{r_0}{a}I$ at $a^2/r_0$ kills every
multipole), and the dipole–slab force
$F_z=-\frac{3m^2(1+\cos^2\theta)}{16d^4}\frac{\mu-1}{\mu+1}$ (P32). Code:
`image_coeffs_*`, `interface_BC_residual_*`, `loop_image_force`,
`solid_angle_B`, `greens_phim`, `sphere_image_ring`, `dipole_slab_force`.

## §6.13 Intrinsic/induced magnetization (pp. 311–314)
With $\vec J_{\rm free}=0$, $\vec H=-\vec\nabla\Phi_m$; matching the dipole
field against $-\vec\nabla(d\vec m\cdot\vec x/r^3)$ ((6.246)–(6.253),
delta-weights included) gives
$$\Phi_m(\vec x)=\oint_S\frac{\vec M\cdot\hat n'}{|\vec x-\vec x'|}da'
-\int_V\frac{\vec\nabla'\cdot\vec M}{|\vec x-\vec x'|}d^3x'\ (6.255)$$
— magnetostatics as electrostatics of "magnetic charge"
$\sigma_m=\vec M\cdot\hat n$, $\rho_m=-\vec\nabla\cdot\vec M$. Uniformly
magnetized sphere: $\vec H(0)=-\frac{4\pi}{3}\vec M$ (6.258),
$\vec H=-\frac{4\pi}{3}\vec M$, $\vec B=+\frac{8\pi}{3}\vec M$ everywhere
inside (6.263)–(6.264); outside a perfect dipole
$\vec m=\frac{4\pi a^3}{3}\vec M$ (6.266)–(6.267);
$\vec K_{\rm eff}=cM_0\sin\theta\,\hat e_\phi$ (6.268) ties back to P13.
Exercises: the $\vec A$ volume+surface split (P33), the split-sphere magnet
(P34 — book's $C_n=(-1)^{n+1}2n(2n-3)!!/(2n+2)!!$ exterior is shell $+$
equatorial disk; its printed interior branch misses the disk), bar-magnet
monopole ends $q_m=M_0S$ (P35), $H_z=-M_0\Omega$ and the cube's
$-\frac{4\pi}{3}M_0$ center (P36), the rod magnet's Bessel $\vec H$
harmonized with P6's solenoid ($nI\leftrightarrow cM_0$,
$\vec B=\vec H+4\pi\vec M$; P37), and the normal-magnetized closed shell
($\Phi_m=-4\pi M_A$ inside, $0$ outside, $\vec B\equiv0$; P38). Code:
`A_magnetized_sphere`, `A_magnetization_surface`, `split_sphere_*`,
`bar_H_*`, `cube_Hz*`, `rod_H_*`, `closed_shell_phim_*`.

## §6.14 Going Deeper (p. 315)
Magnetic-materials reading list (Blundell; Coey; Cullity–Graham;
Jiles–Atherton and Preisach/Tellinen hysteresis models; Kittel; Landau–
Lifshitz ECM Chs. V–VI; Spaldin) — background for the μ phenomenology of
§6.10; nothing downstream in this module depends on it.

## Where this goes
- `~EM-05` — the same physics one level down (Griffiths magnetostatics):
  Biot–Savart, Ampère, vector potential, magnetized matter.
- `~MA-11`/`~MA-08` — Legendre/Bessel machinery: every series here
  ((6.113), (6.119), (6.121), P11, P34) and every $J_1J_0$ kernel.
- Within the trunk: Ch. 4's cylindrical/spherical Green expansions ((4.120),
  (4.225), §4.6 modified Bessels) are quoted constantly; Ch. 5 supplies the
  electrostatic twins ((5.106)-(5.107) images, Ex. 5.7.3 sphere) that §§6.11–
  6.12 transcribe; Ch. 7 (MACRO_EM-07) adds time dependence — Faraday,
  monopoles (§7.8 reuses the multivalued $\Omega$), and the $\vec m$ energy
  $-\vec m\cdot\vec B$ revisited (Ex. 7.6.2).
