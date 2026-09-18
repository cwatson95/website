# MACRO_EM-06 — Problems (Wilcox Ch. 6, all 38 exercises)

Every exercise of Wilcox & Thron 2e §6.15 (printed pp. 316–336), worked in
full. Statements are paraphrased (all given data kept); the book prints no
solutions — everything below is module-authored and machine-checked in
`code/magnetostatics.py` / `code/test_magnetostatics.py`. Sources in
`../refs.md`.

**Conventions (the book's, Gaussian units).** Biot–Savart
$\vec B=\frac{I}{c}\oint\frac{d\vec x'\times(\vec x-\vec x')}{|\vec x-\vec x'|^3}$ (6.7);
force $\vec F=\frac{I}{c}\oint d\vec x\times\vec B$ (6.10);
$\vec\nabla\cdot\vec B=0$ (6.27), $\vec\nabla\times\vec B=\frac{4\pi}{c}\vec J$ (6.35);
Coulomb-gauge potential $\vec A=\frac1c\int d^3x'\,\vec J/|\vec x-\vec x'|$ (6.42);
solid angle $d\Omega'=da'\,\hat n'\cdot(\vec x'-\vec x)/|\vec x-\vec x'|^3$
(6.67), so $\Omega=\partial_z\int_{S'}da'/|\vec x-\vec x'|$ (6.69) and
$\vec B=\frac{I}{c}\vec\nabla\Omega$ off the spanning surface (6.61);
moment $\vec m=\frac1{2c}\int\vec x\times\vec J\,d^3x$ (6.129), $=\frac{I}{c}S\hat n$
for a planar loop (6.134); $\vec J_{\rm eff}=c\vec\nabla\times\vec M$,
$\vec K_{\rm eff}=c\vec M\times\hat n$ (6.195–6.196); $\vec H=\vec B-4\pi\vec M$
(6.199) with $\vec\nabla\times\vec H=\frac{4\pi}{c}\vec J_{\rm free}$ (6.200) and
$\vec B=\mu\vec H$ in linear media (6.202); interface conditions
$(\vec B_2-\vec B_1)\cdot\hat n=0$, $\hat n\times(\vec H_2-\vec H_1)=\frac{4\pi}{c}\vec K_{\rm free}$
(6.204–6.205). Code sets $c=1$ (constant `C`) but keeps every $1/c$ explicit.
Griffiths-level background: `~EM-05`.

---

### P1.  Exercise 6.1.1 — Planar circuit partly immersed in a field  *(Wilcox 2e §6.15, p.316)*
An irregular planar circuit carries current $I>0$. A uniform field $\vec B$
points perpendicular to the circuit's plane, but only within a bounded
(crosshatched) region that the circuit partially enters (the book's
Fig. 6.22). Show that the net force on the circuit is
$$\vec F=\frac{I}{c}\,\vec L\times\vec B,$$
with $\vec L$ the chord vector joining the two points where the circuit
crosses the field boundary (from one field-free side to the other).
*Answer:* as stated; the immersed arc's shape is irrelevant — only its
endpoint-to-endpoint displacement $\vec L$ enters.
*Check:* `circuit_force_partial` (segment-by-segment $d\vec l\times\vec B$ sum
over two different irregular immersed arcs with the same crossing points)
equals `chord_force` to $10^{-12}$ and is unchanged under path refinement
(`test_p1_partial_circuit_force`).

**Solution.** Only the immersed portion feels a force, so from (6.10)
$$\vec F=\frac{I}{c}\int_{\rm in}d\vec x\times\vec B .$$
Since $\vec B$ is one constant vector throughout the region, it factors out
of the integral:
$$\vec F=\frac{I}{c}\Bigl(\int_{\rm in}d\vec x\Bigr)\times\vec B
=\frac{I}{c}\,\vec L\times\vec B,$$
because $\int d\vec x$ along any path is just the endpoint displacement —
here from the entry point (current entering the field region) to the exit
point. All the wiggles of the immersed arc cancel telescopically. With
$\vec B$ perpendicular to the circuit plane and $\vec L$ in the plane,
$\vec F$ lies in the plane, perpendicular to the chord, with magnitude
$ILB/c$. (Had the *whole* circuit been immersed, $\vec L=0$ — a closed loop
in a uniform field feels no net force, only a torque.)

### P2.  Exercise 6.3.1 — Magnetic pinch pressure in a straight wire  *(Wilcox 2e §6.15, pp.316–317)*
A long straight wire of radius $a$ carries total current $I$, uniformly
distributed over its cross-section (Fig. 6.23). Starting from
$$\frac{dP(\rho)}{d\rho}=\frac{1}{A(\rho)}\frac{dF_\rho}{d\rho}$$
($F_\rho$ = radial force on a coaxial tube of radius $\rho$, $A(\rho)$ = its
lateral area), find the radial pressure $P(\rho)$ everywhere. Inward or
outward?
*Answer:* $P(\rho)=\dfrac{I^2}{\pi c^2a^2}\Bigl(1-\dfrac{\rho^2}{a^2}\Bigr)$
for $\rho\le a$, zero outside; the pressure is **inward** (the pinch), maximal
on the axis, $P(0)=I^2/\pi c^2a^2$.
*Check:* closed form vs the integrated $dP/d\rho=-JB_\phi/c$ quadrature
($10^{-10}$), monotone decrease, $P(a)=0$; Ampère's law for $B_\phi$ verified
at $\rho\lessgtr a$ (`test_p2_pinch_pressure`).

**Solution.** The current density is $J=I/\pi a^2$. Ampère's law (6.36) on a
coaxial circle: $2\pi\rho B_\phi=\frac{4\pi}{c}I_{\rm enc}$ with
$I_{\rm enc}=I\rho^2/a^2$ inside, $I$ outside, so
$$B_\phi=\frac{2I\rho}{ca^2}\ (\rho\le a),\qquad B_\phi=\frac{2I}{c\rho}\ (\rho\ge a).$$
The force density is $\vec f=\frac1c\vec J\times\vec B
=\frac1c J\hat z\times B_\phi\hat e_\phi=-\frac{JB_\phi}{c}\hat\rho$ — radially
inward. A shell $(\rho,\rho+d\rho)$ of unit length feels
$dF_\rho=-\frac{JB_\phi}{c}\,2\pi\rho\,d\rho$, and with $A(\rho)=2\pi\rho$
per unit length the book's relation gives
$$\frac{dP}{d\rho}=-\frac{J\,B_\phi(\rho)}{c}=-\frac{2I^2\rho}{\pi c^2a^4}.$$
Each shell's inward squeeze is borne by the material beneath it, so
integrating in from the free surface ($P(a)=0$):
$$P(\rho)=\int_\rho^a\frac{2I^2\rho'}{\pi c^2a^4}d\rho'
=\frac{I^2}{\pi c^2a^2}\Bigl(1-\frac{\rho^2}{a^2}\Bigr),$$
and $P\equiv0$ for $\rho>a$ (no current, no body force). The pressure is
compressive (inward): parallel current filaments attract (§6.1) — this is
the classic $z$-pinch profile.

### P3.  Exercise 6.3.2 — Spinning, sliding charged cylinder by Ampère's law  *(Wilcox 2e §6.15, p.317)*
An infinite hollow cylinder of radius $R$ carries uniform surface charge
density $\sigma$ (Fig. 6.24). It spins about its axis ($z$) at angular
velocity $\omega$ *and* translates along $z$ with speed $v_0$. Use Ampère's
law to find $\vec B$ inside and outside.
*Answer:* inside: $\vec B=\dfrac{4\pi\sigma\omega R}{c}\hat z$ (uniform);
outside: $\vec B=\dfrac{4\pi\sigma R v_0}{c\rho}\hat e_\phi$. The rotation
acts as an infinite solenoid, the translation as a fat straight wire.
*Check:* both closed forms vs direct Biot–Savart superposition (a sinh-graded
stack of current loops for $K_\phi$, a ring of long straight wires for
$K_z$), agreement $2\times10^{-3}$ with the complementary components
consistent with zero (`test_p3_spinning_sliding_cylinder`).

**Solution.** The moving surface charge is the superposition of two surface
currents: rotation gives $K_\phi=\sigma v_\phi=\sigma\omega R$ (a solenoid
sheet), translation gives $K_z=\sigma v_0$ (an axial sheet).
*Solenoid part.* By symmetry $\vec B=B_z(\rho)\hat z$; $B_z(\infty)=0$ and a
rectangular Ampère loop straddling the sheet with legs parallel to $z$ picks
up only the sheet current: $B_z^{\rm in}-B_z^{\rm out}=\frac{4\pi}{c}K_\phi$,
while a loop entirely inside (or outside) shows $B_z$ is constant in each
region. Hence $B_z^{\rm out}=0$ and
$B_z^{\rm in}=\frac{4\pi}{c}\sigma\omega R$.
*Wire part.* By symmetry $\vec B=B_\phi(\rho)\hat e_\phi$; a coaxial circular
Ampère loop encloses $I_{\rm enc}=K_z\cdot2\pi R=2\pi R\sigma v_0$ when
$\rho>R$ and nothing when $\rho<R$:
$$B_\phi(\rho>R)=\frac{4\pi\sigma R v_0}{c\rho},\qquad B_\phi(\rho<R)=0 .$$
Superpose: uniform axial field inside, azimuthal wire field outside. (Each
part also satisfies the jump condition (6.43) across the sheet.)

### P4.  Exercise 6.4.1 — Field of an infinite current sheet  *(Wilcox 2e §6.15, pp.317–318)*
A plane sheet (the $y$–$z$ plane, Fig. 6.25) carries constant surface current
density $\vec K=K_0\hat z$. Find $\vec B$ on both sides.
*Answer:* $\vec B=\pm\dfrac{2\pi K_0}{c}\,\hat y$ for $x\gtrless0$ — uniform,
parallel to the sheet, perpendicular to the current, antisymmetric across the
sheet, with jump $\hat n\times(\vec B_2-\vec B_1)=\frac{4\pi}{c}\vec K$.
*Check:* closed form vs a sinh-graded superposition of infinite straight
wires ($10^{-6}$); the jump condition verified exactly
(`test_p4_current_sheet`).

**Solution.** Think of the sheet as a stack of parallel wires along $z$ at
$(0,y')$, each carrying $dI=K_0\,dy'$. The wire at $y'$ produces
$d\vec B=\frac{2\,dI}{c\,d}\hat e_\phi$ with $d=\sqrt{x^2+(y-y')^2}$. By the
$y'\to2y-y'$ mirror symmetry the components along $\hat x$ cancel pairwise
and the $\hat y$ components add:
$$B_y(x)=\frac{2K_0}{c}\int_{-\infty}^{\infty}\frac{x\,dy'}{x^2+y'^2}
=\frac{2K_0}{c}\,\pi\,\mathrm{sign}(x).$$
So $\vec B=\frac{2\pi K_0}{c}\mathrm{sign}(x)\,\hat y$: uniform on each side
(the sheet has no length scale), tangential, and odd in $x$. Consistency with
(6.43), $\hat n=\hat x$:
$\hat x\times[\vec B(0^+)-\vec B(0^-)]=\hat x\times\frac{4\pi K_0}{c}\hat y
=\frac{4\pi K_0}{c}\hat z=\frac{4\pi}{c}\vec K$ ✓. (This is the magnetostatic
twin of the charged sheet's $\pm2\pi\sigma$ field, cf. §6.4's
$\pm\frac{2\pi}{c}K$ disk argument (6.48)–(6.49).)

### P5.  Exercise 6.5.1 — The Stokes transform $\oint d\vec\ell\times\vec A$  *(Wilcox 2e §6.15, p.318)*
Transform Stokes' theorem
$\oint_C\vec A\cdot d\vec\ell=\int_S da\,\hat n\cdot(\vec\nabla\times\vec A)$
into ($d\vec s=da\,\hat n$)
$$\oint_C d\vec\ell\times\vec A=\int_S(d\vec s\times\vec\nabla)\times\vec A .$$
*Answer:* identity proved below; in components the right side is
$\int_S\bigl[\sum_i ds_i\vec\nabla A_i-d\vec s\,(\vec\nabla\cdot\vec A)\bigr]$
— the form (6.51) used to build the solid-angle representation of $\vec B$
(§6.5) and the directed-area moment formula (6.133).
*Check:* both sides computed for a smooth non-trivial $\vec A$ over the unit
circle spanned two ways — a flat disk and a paraboloidal cap —
agreeing to $10^{-5}$ (surface independence included)
(`test_p5_stokes_transform`).

**Solution.** Let $\hat c$ be an arbitrary *constant* vector and apply
ordinary Stokes' theorem to the field $\vec A\times\hat c$:
$$\oint_C(\vec A\times\hat c)\cdot d\vec\ell
=\int_S d\vec s\cdot\bigl[\vec\nabla\times(\vec A\times\hat c)\bigr].$$
Left side: the cyclic identity
$d\vec\ell\cdot(\vec A\times\hat c)=\hat c\cdot(d\vec\ell\times\vec A)$ gives
$\hat c\cdot\oint d\vec\ell\times\vec A$.
Right side: for constant $\hat c$,
$\vec\nabla\times(\vec A\times\hat c)=(\hat c\cdot\vec\nabla)\vec A-\hat c\,(\vec\nabla\cdot\vec A)$,
so
$$d\vec s\cdot[\cdots]=\sum_{i,j}ds_j\,c_i\partial_iA_j-(d\vec s\cdot\hat c)(\vec\nabla\cdot\vec A)
=\hat c\cdot\Bigl[\sum_j ds_j\vec\nabla A_j-d\vec s\,(\vec\nabla\cdot\vec A)\Bigr].$$
Since $\hat c$ is arbitrary, the vectors multiplying it are equal:
$$\oint_C d\vec\ell\times\vec A
=\int_S\Bigl[\sum_i ds_i\,\vec\nabla A_i-d\vec s\,(\vec\nabla\cdot\vec A)\Bigr]
=\int_S(d\vec s\times\vec\nabla)\times\vec A,$$
where the last equality is the $\varepsilon$-identity
$[(d\vec s\times\vec\nabla)\times\vec A]_k
=\sum_i ds_i\partial_kA_i-ds_k\sum_i\partial_iA_i$ (expand
$\varepsilon_{kij}\varepsilon_{ilm}=\delta_{jl}\delta_{km}-\delta_{jm}\delta_{kl}$
— the operator BAC–CAB rule, with $\vec\nabla$ acting only on $\vec A$).

### P6.  Exercise 6.6.1 — Finite solenoid: interior Bessel form and outside falloff  *(Wilcox 2e §6.15, pp.318–319)*
(a) Building on the loop fields (6.83)–(6.84), show that a tightly wound
solenoid (radius $a$, length $d$, $n$ turns per unit length, current $I$,
origin at its center; Fig. 6.26) has, for $-d/2<z<d/2$,
$$B_\rho=\frac{4\pi anI}{c}\int_0^\infty dk\,J_1(ka)J_1(k\rho)\,e^{-kd/2}\sinh(kz),$$
$$B_z=\frac{4\pi nI}{c}H(\rho)-\frac{4\pi anI}{c}\int_0^\infty dk\,J_1(ka)J_0(k\rho)\,e^{-kd/2}\cosh(kz),$$
where $H(\rho)=1$ for $\rho<a$, $0$ for $\rho>a$ (the first term is the
infinite-solenoid field; the second is the finite-length correction).
(b) Show the correction term at the center falls off like $1/d^2$ for
$d\gg\rho,a$.
*Answer:* (a) as stated; (b) correction $\to 8\pi a^2nI/(cd^2)$.
*Check:* Bessel forms vs a brute-force stack of elliptic-integral loops
($2\times10^{-6}$) and the exact on-axis form
(`test_p6_solenoid_bessel_inside`); $d^2\times$correction $\to8\pi a^2nI/c$
monotonically, to $5\times10^{-4}$ at $d=80a$
(`test_p6_correction_term_falloff`).

**Solution.** (a) Superpose loops: the turns in $dz_0$ at height $z_0$ carry
$nI\,dz_0$, so replace $I\to nI\,dz_0$, $z\to z-z_0$ in (6.83)–(6.84) and
integrate $z_0\in(-d/2,d/2)$. Both integrals factor through
$$\int_{-d/2}^{d/2}dz_0\,k\,e^{-k|z-z_0|}\,
\begin{Bmatrix}\mathrm{sign}(z-z_0)\\1\end{Bmatrix}.$$
For $|z|<d/2$ split at $z_0=z$:
$$\int k e^{-k|z-z_0|}dz_0=2-e^{-k(d/2+z)}-e^{-k(d/2-z)}=2\bigl[1-e^{-kd/2}\cosh kz\bigr],$$
$$\int \mathrm{sign}(z-z_0)\,k e^{-k|z-z_0|}dz_0
=e^{-k(d/2-z)}-e^{-k(d/2+z)}=2\,e^{-kd/2}\sinh kz .$$
The $\sinh$ line inserted into (6.83) gives $B_\rho$ directly. For $B_z$,
(6.84) produces
$$B_z=\frac{4\pi anI}{c}\int_0^\infty dk\,J_1(ka)J_0(k\rho)
-\frac{4\pi anI}{c}\int_0^\infty dk\,J_1(ka)J_0(k\rho)e^{-kd/2}\cosh kz,$$
and the first ($d$-independent) integral is exactly the step function
identity (6.74): $a\int_0^\infty J_1(ka)J_0(k\rho)\,dk=H(\rho)$ — the
infinite-solenoid term $\frac{4\pi nI}{c}H(\rho)$. ✓
(b) At $\rho=0$, $z=0$ the correction is
$\Delta=\frac{4\pi anI}{c}\int_0^\infty dk\,J_1(ka)e^{-kd/2}$. For $d\gg a$
the exponential confines $k\lesssim2/d\ll1/a$, where $J_1(ka)\simeq ka/2$:
$$\Delta\simeq\frac{4\pi anI}{c}\cdot\frac{a}{2}\int_0^\infty k\,e^{-kd/2}dk
=\frac{2\pi a^2nI}{c}\cdot\frac{4}{d^2}=\frac{8\pi a^2nI}{c\,d^2}\;\propto\;\frac1{d^2}.$$
So the *outside* return field near the middle of a long solenoid dies as
$1/d^2$ (each end looks like a monopole-pair aperture; cf. P16 for the
$|z|\gg d$ dipole regime).

### P7.  Exercise 6.6.2 — Spinning charged disk  *(Wilcox 2e §6.15, p.319)*
A thin disk of radius $R$ in the $z=0$ plane carries uniform surface charge
$\sigma$ and spins at $\omega$ about its axis. Show
$$B_\rho=\mathrm{sign}(z)\,\frac{2\pi\omega\sigma R^2}{c}\int_0^\infty dk\,e^{-k|z|}J_2(kR)J_1(k\rho),\qquad
B_z=\frac{2\pi\omega\sigma R^2}{c}\int_0^\infty dk\,e^{-k|z|}J_2(kR)J_0(k\rho).$$
Extra: show $B_z\to\dfrac{\pi\sigma\omega}{2c}\dfrac{R^4}{|z|^3}$ for
$|z|\gg\rho,R$ and read off the disk's magnetic moment $m_z$.
(The book's limit line lists "$\rho,a,b$"; the disk's only scales are $\rho$
and $R$.)
*Answer:* as stated; $m_z=\pi\sigma\omega R^4/(4c)$ (so
$B_z\to2m_z/|z|^3$ on axis).
*Check:* Bessel forms vs ring superposition ($5\times10^{-6}$), $B_\rho$ odd
in $z$ (`test_p7_spinning_disk`); far-field $B_z$ matches
$\frac{2m}{z^3}(1-R^2/z^2)$ to $2\times10^{-3}$ — the exact axis expansion —
and $m$ matches the direct moment integral (`test_p7_disk_far_field_moment`).

**Solution.** The annulus $(\rho_0,\rho_0+d\rho_0)$ is a loop of current
$dI=\sigma\,(\omega\rho_0)\,d\rho_0$ (charge per length $\sigma d\rho_0$
passing at speed $\omega\rho_0$). Insert $a\to\rho_0$, $I\to dI$ in
(6.83)–(6.84) and integrate. Both components need
$$\int_0^R\rho_0^2\,J_1(k\rho_0)\,d\rho_0=\frac{R^2}{k}J_2(kR),$$
which follows from the Bessel recursion $\frac{d}{dx}[x^2J_2(x)]=x^2J_1(x)$
(the $m=2$ member of the family that gave (6.72)). Then, e.g.,
$$B_z=\frac{2\pi\sigma\omega}{c}\int_0^\infty dk\,k\,J_0(k\rho)e^{-k|z|}
\int_0^R \rho_0^2 J_1(k\rho_0)d\rho_0
=\frac{2\pi\omega\sigma R^2}{c}\int_0^\infty dk\,J_2(kR)J_0(k\rho)e^{-k|z|},$$
and identically for $B_\rho$ with $J_1(k\rho)$ and the loop field's
$\mathrm{sign}(z)$. ✓
*Far field.* On axis ($\rho=0$, $J_0=1$), $e^{-k|z|}$ confines
$k\lesssim1/|z|\ll1/R$ where $J_2(kR)\simeq(kR)^2/8$:
$$B_z\simeq\frac{2\pi\omega\sigma R^2}{c}\,\frac{R^2}{8}\int_0^\infty k^2e^{-k|z|}dk
=\frac{2\pi\omega\sigma R^4}{8c}\,\frac{2}{|z|^3}
=\frac{\pi\sigma\omega R^4}{2c\,|z|^3}.$$
Matching the on-axis dipole field $B_z=2m_z/|z|^3$ (6.154):
$$m_z=\frac{\pi\sigma\omega R^4}{4c}
\;\Bigl(=\frac1{2c}\int(\vec x\times\vec K)_z\,da
=\frac{1}{2c}\int_0^R\rho_0\,\sigma\omega\rho_0\,2\pi\rho_0\,d\rho_0\ \checkmark\Bigr).$$

### P8.  Exercise 6.6.3 — Spinning solid charged cylinder  *(Wilcox 2e §6.15, pp.319–320)*
A solid cylinder (radius $R$, length $d$, uniform charge density $\rho_0$)
spins at $\omega$ about its axis; origin at the center. Show that for
$|z|<d/2$
$$B_z(\rho,z)=\frac{2\pi\rho_0\omega}{c}\bigl(R^2-\rho^2\bigr)H(R-\rho)
-\frac{4\pi\rho_0\omega R^2}{c}\int_0^\infty\frac{dk}{k}\,e^{-kd/2}\cosh(kz)\,J_2(kR)J_0(k\rho),$$
with $H$ the unit step (the book writes it "$H(R)$", meaning the step in
$\rho$ at $R$). [Hint: use Exercise 6.6.1 or 6.6.2.]
*Answer:* as stated — an infinite-cylinder parabolic profile plus a
finite-length correction.
*Check:* Bessel form vs a doubly split stack of spinning disks (each a ring
superposition), $3\times10^{-4}$; the Weber–Schafheitlin integral
$\int_0^\infty J_2(kR)J_0(k\rho)\,dk/k=(R^2-\rho^2)/2R^2\,H(R-\rho)$ behind
the step term verified by direct quadrature
(`test_p8_spinning_solid_cylinder`).

**Solution.** Slice the cylinder into disks of thickness $dz_0$: each is a
spinning disk (P7) of surface density $\rho_0\,dz_0$. Integrate P7's $B_z$
with $z\to z-z_0$:
$$B_z=\frac{2\pi\rho_0\omega R^2}{c}\int_0^\infty dk\,J_2(kR)J_0(k\rho)
\int_{-d/2}^{d/2}dz_0\,e^{-k|z-z_0|}.$$
The inner integral (P6's split) is $\frac2k[1-e^{-kd/2}\cosh kz]$, so
$$B_z=\frac{4\pi\rho_0\omega R^2}{c}\int_0^\infty\frac{dk}{k}J_2(kR)J_0(k\rho)
-\frac{4\pi\rho_0\omega R^2}{c}\int_0^\infty\frac{dk}{k}e^{-kd/2}\cosh(kz)J_2(kR)J_0(k\rho).$$
The first, $d$-independent integral is the Weber–Schafheitlin closed form
$$\int_0^\infty\frac{dk}{k}\,J_2(kR)J_0(k\rho)=\frac{R^2-\rho^2}{2R^2}\,H(R-\rho)$$
(at $\rho=0$ it is $\int J_2(x)dx/x=1/2$ ✓), turning the leading term into
$\frac{2\pi\rho_0\omega}{c}(R^2-\rho^2)H(R-\rho)$ — precisely the infinite
spinning cylinder: nested solenoid sheets $K_\phi=\rho_0\omega\rho'\,d\rho'$
give $B_z(\rho)=\frac{4\pi}{c}\int_\rho^R\rho_0\omega\rho'\,d\rho'
=\frac{2\pi\rho_0\omega}{c}(R^2-\rho^2)$ inside and $0$ outside. ✓

### P9.  Exercise 6.6.4 — Loop potential as a modified-Bessel integral  *(Wilcox 2e §6.15, p.320)*
The thin circular loop of radius $a$ in the $z'=0$ plane carrying current $I$
has volume current
$\vec J(\vec x')=I\,a\,\frac{\delta(\rho'-a)}{\rho'}\,\delta(z')\,\hat e_{\phi'}$,
with $\hat e_{\phi'}=-\sin\phi'\,\hat x+\cos\phi'\,\hat y$. Show that its
vector potential can be evaluated as
$$\vec A(\rho,z)=\frac{4Ia}{c}\,\hat e_\phi\int_0^\infty dk\,\cos(kz)\,
I_1(k\rho_<)\,K_1(k\rho_>),$$
where $\rho_<$ ($\rho_>$) is the lesser (greater) of $\rho$ and $a$
(modified Bessel functions as in §4.6).
*Answer:* as stated — the $\rho$-stacked twin of the $z$-stacked form (6.227).
*Check:* `loop_A_IK` $=$ `loop_A_bessel` (6.227) $=$ direct Biot–Savart line
integral `loop_A_3d`, to $2\times10^{-6}$ at points inside and outside $\rho=a$
(`test_p9_loop_A_IK`).

**Solution.** (The given $\vec J$ integrates over a half-plane
cross-section to $I$ ✓.) By symmetry $\vec A=A_\phi(\rho,z)\hat e_\phi$, and
evaluating at $\phi=0$ (where $\hat e_\phi=\hat y$) as in (6.100)–(6.101),
$$A_\phi=\frac{Ia}{c}\int_0^{2\pi}d\phi'\,\frac{\cos\phi'}{|\vec x-\vec x'|}
\Big|_{\rho'=a,\,z'=0}.$$
Now insert the *other* cylindrical expansion of the free Green function —
Fourier in $z$, modified Bessel in $\rho$ (the §4.6 companion of (6.70)):
$$\frac1{|\vec x-\vec x'|}=\frac2\pi\sum_{m=-\infty}^{\infty}
\int_0^\infty dk\,e^{im(\phi-\phi')}\cos\bigl(k(z-z')\bigr)\,I_m(k\rho_<)K_m(k\rho_>).$$
The $\phi'$ integral $\int_0^{2\pi}\cos\phi'\,e^{-im\phi'}d\phi'=\pi(\delta_{m,1}+\delta_{m,-1})$
keeps only $m=\pm1$, each contributing equally ($I_{-1}K_{-1}=I_1K_1$), so with
$z'=0$ and $\phi=0$:
$$A_\phi=\frac{Ia}{c}\cdot\frac2\pi\cdot2\pi\int_0^\infty dk\,\cos(kz)\,I_1(k\rho_<)K_1(k\rho_>)
=\frac{4Ia}{c}\int_0^\infty dk\,\cos(kz)\,I_1(k\rho_<)K_1(k\rho_>). \checkmark$$
Here $\rho_<=\min(\rho,a)$, $\rho_>=\max(\rho,a)$ because the source sits at
$\rho'=a$. This form is manifestly regular on the axis ($I_1\to0$) and decays
for $\rho\to\infty$ ($K_1\to0$); the numeric check confirms it agrees with
the $e^{-k|z|}J_1J_1$ representation (6.227) everywhere off the wire.

### P10.  Exercise 6.6.5 — Spinning truncated cone: field at the tip  *(Wilcox 2e §6.15, pp.320–321)*
A truncated cone of half-opening angle $\alpha$ has its axis along $z$ and
its (virtual) apex at the origin; the surface extends from axial distance
$L_1$ to $L_2$ (Fig. 6.27). It carries uniform surface charge $\sigma$ (cf.
Ex. 2.4.4) and spins at $\omega$, so $\vec K=\sigma\omega\rho\,\hat e_\phi$.
Using the on-axis loop field (6.62), sum the ring currents to get $B_z$ at
the origin.
*Answer:* $B_z(0)=\dfrac{2\pi\sigma\omega}{c}\,(L_2-L_1)\,
\dfrac{\sin^3\alpha}{\cos\alpha}$.
*Check:* closed form vs direct ring quadrature ($10^{-10}$); the
$\propto\alpha^3$ small-angle scaling verified
(`test_p10_cone_tip_field`).

**Solution.** Slice the cone into rings by axial position $z\in(L_1,L_2)$.
The ring at $z$ has radius $\rho(z)=z\tan\alpha$; its width measured *along
the slant* is $d\ell=dz/\cos\alpha$, so it carries
$$dI=K\,d\ell=\sigma\omega\,\rho(z)\,\frac{dz}{\cos\alpha}
=\frac{\sigma\omega\tan\alpha}{\cos\alpha}\,z\,dz .$$
The on-axis loop formula (6.62), with the field point a distance $z$ below
the ring's plane, gives
$dB_z=\frac{2\pi\,dI}{c}\frac{\rho^2}{(\rho^2+z^2)^{3/2}}$. With
$\rho^2+z^2=z^2/\cos^2\alpha$:
$$dB_z=\frac{2\pi}{c}\,\frac{\sigma\omega\tan\alpha}{\cos\alpha}\,z\,
\frac{z^2\tan^2\alpha\,\cos^3\alpha}{z^3}\,dz
=\frac{2\pi\sigma\omega}{c}\,\frac{\sin^3\alpha}{\cos\alpha}\,dz,$$
which is *independent of $z$* — every slice contributes equally (the
$1/z^2$ geometric dilution exactly cancels the growth of ring radius and
current). Hence
$$B_z(0)=\frac{2\pi\sigma\omega}{c}\,\frac{\sin^3\alpha}{\cos\alpha}\,(L_2-L_1).$$
Limits: $\alpha\to0$ kills the field as $\alpha^3$ (thin needle);
$\alpha\to\pi/2$ diverges (the cone flattens into an infinite sheet-like
annulus whose inner edge approaches the origin).

### P11.  Exercise 6.7.1 — Legendre series for the disk solid angle  *(Wilcox 2e §6.15, p.321)*
Evaluate the solid angle (6.69) of a flat disk of radius $a$ (in the $x$–$y$
plane, axis $\hat z$, oriented as the current-loop spanning surface of
§§6.6–6.7) with the spherical-coordinate Coulomb expansion (4.225). Show
$$\Omega(\vec x)=-2\pi\sum_{n\ge0}\Bigl(\frac ar\Bigr)^{2n+2}
\frac{(-1)^n(2n+1)!!}{(2n+2)!!}\,P_{2n+1}(\cos\theta)\qquad(r\ge a),$$
$$\Omega(\vec x)=-2\pi\sum_{n\ge0}\frac{(-1)^n(2n-1)!!}{(2n)!!}
\Bigl[\frac{4n+3}{2n+2}-\Bigl(\frac ra\Bigr)^{2n+1}\Bigr]P_{2n+1}(\cos\theta)\qquad(r\le a),$$
the two agreeing at $r=a$; and show the interior form can be re-organized as
$$\Omega(\vec x)=-2\pi\,\mathrm{sign}(z)+2\pi\sum_{n\ge0}
\frac{(-1)^n(2n-1)!!}{(2n)!!}\Bigl(\frac ra\Bigr)^{2n+1}P_{2n+1}(\cos\theta).$$
[Hints: (4.181)–(4.183), Ex. 4.12.1, and
$\partial_z=\cos\theta\,\partial_r+\frac{\sin^2\theta}{r}\partial_{\cos\theta}$.]
*Answer:* as stated. The sign-split form isolates the disk discontinuity: the
constant part of the interior series is exactly the Legendre expansion of
$\mathrm{sign}(\cos\theta)$.
*Check:* exterior series vs quadrature and the Bessel form (6.73) to
$2\times10^{-6}$; split interior form to $10^{-6}$ (geometric convergence);
plain interior branch converges $\sim1/N$ to the same values (conditionally
convergent constant part); termwise $r=a$ branch agreement; on-axis closed
form (6.60) reproduced (`test_p11_solid_angle_series`).

**Solution.** *Exterior.* Start from (6.69),
$\Omega=\partial_z\int_{S'}da'/|\vec x-\vec x'|$. Every source point has
$r'=\rho'\le a<r$ and sits at polar angle $\pi/2$, so the $m=0$ (azimuthally
averaged) Coulomb expansion gives
$$\int_{S'}\frac{da'}{|\vec x-\vec x'|}
=2\pi\sum_\ell P_\ell(0)\,P_\ell(\cos\theta)\,\frac{1}{r^{\ell+1}}\int_0^a\rho'^{\,\ell+1}d\rho'
=2\pi\sum_\ell\frac{P_\ell(0)\,a^{\ell+2}}{(\ell+2)\,r^{\ell+1}}P_\ell(\cos\theta).$$
$P_\ell(0)$ kills odd $\ell$; for $\ell=2n$, $P_{2n}(0)=(-1)^n\frac{(2n-1)!!}{(2n)!!}$.
Now apply the hinted derivative. Acting on $f_\ell(r)P_\ell(\cos\theta)$ with
$f_\ell=r^{-(\ell+1)}$, the two pieces combine via the derivative identities
(4.181)–(4.183) into the pure $P_{\ell+1}$ ladder
$$\partial_z\Bigl[\frac{P_\ell(\cos\theta)}{r^{\ell+1}}\Bigr]
=-(\ell+1)\frac{P_{\ell+1}(\cos\theta)}{r^{\ell+2}}$$
(the textbook identity $\partial_z[r^{-(\ell+1)}P_\ell]$: both
$\cos\theta\,\partial_r$ and the angular term produce
$P_{\ell+1}$-content only, by
$(\ell+1)P_{\ell+1}=(2\ell+1)xP_\ell-\ell P_{\ell-1}$ and
$(1-x^2)P'_\ell=\ell(P_{\ell-1}-xP_\ell)$; Ex. 4.12.1). Hence
$$\Omega=2\pi\sum_n\frac{(-1)^n(2n-1)!!}{(2n)!!}\frac{a^{2n+2}}{2n+2}
\bigl[-(2n+1)\bigr]\frac{P_{2n+1}(\cos\theta)}{r^{2n+2}}
=-2\pi\sum_n\frac{(-1)^n(2n+1)!!}{(2n+2)!!}\Bigl(\frac ar\Bigr)^{2n+2}P_{2n+1},$$
using $(2n+1)(2n-1)!!=(2n+1)!!$ and $(2n+2)(2n)!!=(2n+2)!!$. ✓
*Interior.* For $r\le a$ split the radial integral at $\rho'=r$:
$$\int_0^a\frac{\rho'^{\,\ell+1}\,d\rho'}{r_>^{\ell+1}}\,r_<^\ell\Big/\rho'^{\,\ell}\ \text{bookkeeping}
\;\Rightarrow\;
\int_0^r\frac{\rho'^{\,\ell+1}}{r^{\ell+1}}d\rho'+r^\ell\!\int_r^a\frac{d\rho'}{\rho'^{\,\ell}}
=\frac{r}{\ell+2}+\frac{r}{\ell-1}\Bigl[1-\Bigl(\frac ra\Bigr)^{\ell-1}\Bigr]$$
(for $\ell\ge2$; the $\ell=0$ term is $a-r/2$, and only its $-r/2$ piece
survives $\partial_z$). Applying the same $\partial_z$ ladder — now also to
the growing solutions, via
$\partial_z[r^{\ell}P_\ell]=\ell\,r^{\ell-1}P_{\ell-1}$ — and collecting
coefficients of $P_{2n+1}$ produces the stated interior branch; at $r=a$ it
matches the exterior branch *termwise* because
$\frac{(2n-1)!!}{(2n)!!}\bigl[\frac{4n+3}{2n+2}-1\bigr]
=\frac{(2n-1)!!}{(2n)!!}\frac{2n+1}{2n+2}=\frac{(2n+1)!!}{(2n+2)!!}$.
*Sign split.* The $r$-independent part of the interior series is
$-2\pi\sum_n(-1)^n\frac{(2n-1)!!}{(2n)!!}\frac{4n+3}{2n+2}P_{2n+1}(\cos\theta)$.
Since $\int_0^1P_{2n+1}(x)\,dx=(-1)^n\frac{(2n-1)!!}{(2n+2)!!}$, the Legendre
coefficients of $\mathrm{sign}(x)$ are
$c_{2n+1}=(4n+3)\int_0^1P_{2n+1}=(-1)^n\frac{(2n-1)!!(4n+3)}{(2n+2)!!}$ —
exactly the numbers above. So that constant part *is*
$-2\pi\,\mathrm{sign}(\cos\theta)$, and pulling it out leaves the stated
geometric-convergent power series. The sign term carries the whole
$\Omega=\mp2\pi$ jump across the disk ((6.80)–(6.81)); the remaining series
is continuous through $z=0$.

### P12.  Exercise 6.7.2 — Loop $B_r$, $B_\theta$ from the solid angle  *(Wilcox 2e §6.15, p.321)*
Using P11's solid-angle series in $\vec B=\frac{I}{c}\vec\nabla\Omega$,
recover the current-loop fields (6.119) and (6.121) for both $r>a$ and
$r<a$:
$$B_r=\frac{2\pi Ia}{cr}\sum_{n\ge0}\frac{(-1)^n(2n+1)!!}{(2n)!!}
\frac{r_<^{2n+1}}{r_>^{2n+2}}P_{2n+1}(\cos\theta),$$
$$B_\theta=-\frac{\pi Ia^2}{c}\sum_{n\ge0}\frac{(-1)^n(2n+1)!!}{(n+1)(2n)!!}
P^1_{2n+1}(\cos\theta)\times
\begin{cases}\dfrac{1}{r^3}\bigl(\tfrac ar\bigr)^{2n}, & r>a,\\[1ex]
-\dfrac{2n+2}{2n+1}\dfrac1{a^3}\bigl(\tfrac ra\bigr)^{2n}, & r<a.\end{cases}$$
*Answer:* as stated (Condon–Shortley $P^1_\ell$).
*Check:* both series vs the elliptic-integral loop field converted to
spherical components, $10^{-8}$ at interior and exterior points
(`test_p12_loop_field_series`).

**Solution.** $B_r=\frac{I}{c}\partial_r\Omega$ and
$B_\theta=\frac{I}{c}\frac1r\partial_\theta\Omega$ (6.82-analog in
spherical form).
*Exterior $B_r$:* $\partial_r(a/r)^{2n+2}=-(2n+2)(a/r)^{2n+2}/r$, so
$$B_r=\frac{2\pi I}{c}\sum(-1)^n\frac{(2n+1)!!}{(2n+2)!!}(2n+2)\frac{a^{2n+2}}{r^{2n+3}}P_{2n+1}
=\frac{2\pi Ia}{cr}\sum(-1)^n\frac{(2n+1)!!}{(2n)!!}\frac{a^{2n+1}}{r^{2n+2}}P_{2n+1},$$
i.e. (6.119) with $r_<=a$, $r_>=r$.
*Interior $B_r$:* use the sign-split form (the $\mathrm{sign}(z)$ term is
$r$-independent on either side, so $\partial_r$ kills it):
$$B_r=\frac{2\pi I}{c}\sum(-1)^n\frac{(2n-1)!!}{(2n)!!}\frac{(2n+1)\,r^{2n}}{a^{2n+1}}P_{2n+1}
=\frac{2\pi Ia}{cr}\sum(-1)^n\frac{(2n+1)!!}{(2n)!!}\frac{r^{2n+1}}{a^{2n+2}}P_{2n+1},$$
the same formula with $r_<=r$, $r_>=a$: $B_r$ is one continuous expression. ✓
*$B_\theta$:* $\frac{\partial}{\partial\theta}P_\ell(\cos\theta)
=-\sin\theta\,P'_\ell(\cos\theta)=P^1_\ell(\cos\theta)$ in the
Condon–Shortley convention. Exterior:
$$B_\theta=-\frac{2\pi I}{c}\sum(-1)^n\frac{(2n+1)!!}{(2n+2)!!}
\frac{a^{2n+2}}{r^{2n+3}}P^1_{2n+1}
=-\frac{\pi Ia^2}{c}\sum\frac{(-1)^n(2n+1)!!}{(n+1)(2n)!!}\frac{(a/r)^{2n}}{r^3}P^1_{2n+1},$$
since $(2n+2)!!=2(n+1)(2n)!!$. Interior (split form again):
$$B_\theta=\frac{2\pi I}{c}\sum(-1)^n\frac{(2n-1)!!}{(2n)!!}\frac{r^{2n}}{a^{2n+1}}P^1_{2n+1}
=-\frac{\pi Ia^2}{c}\sum\frac{(-1)^n(2n+1)!!}{(n+1)(2n)!!}
\Bigl[-\frac{2n+2}{2n+1}\Bigr]\frac{(r/a)^{2n}}{a^3}P^1_{2n+1},$$
matching the stated $r<a$ branch. The *apparent* jump of $B_\theta$ across
$r=a$ is the book's point: on the sphere $r=a$ the two branches disagree
termwise, but the sums only actually differ at $\theta=\pi/2$ — the wire
itself — because the discarded $\mathrm{sign}(z)$ term contributes the
compensating $\delta$-sheet on the spanning disk ($\frac1r\partial_\theta$
of $-2\pi\,\mathrm{sign}(\cos\theta)$), cf. (6.85)–(6.94). Off the wire the
full field is continuous — the numeric check hits points on both sides
against the elliptic closed form.

### P13.  Exercise 6.7.3 — Rotating uniformly charged shell  *(Wilcox 2e §6.15, p.322)*
A spherical shell of radius $a$ with uniform surface charge $\sigma$ spins at
constant $\omega$ about $\hat z$ (Fig. 6.28). Via the vector potential, show
$$\vec B=\begin{cases}
\dfrac{8\pi a\sigma\omega}{3c}\,\hat z, & r<a,\\[1ex]
\dfrac{3\vec x(\vec m\cdot\vec x)-r^2\vec m}{r^5}, & r>a,
\end{cases}
\qquad \vec m=\frac{4\pi\sigma\omega a^4}{3c}\hat z:$$
uniform inside, a perfect dipole outside. (Identical to the uniformly
magnetized sphere of §6.13 with $M_0=\sigma\omega a/c$.)
*Answer:* as stated.
*Check:* closed forms vs Biot–Savart ring quadrature over the shell at
interior and exterior points, $10^{-6}$ (`test_p13_rotating_shell`).

**Solution.** The surface current is
$\vec K=\sigma\vec v=\sigma\omega a\sin\theta'\,\hat e_{\phi'}$. In
$\vec A=\frac1c\oint K\,da'/|\vec x-\vec x'|$ expand the Green function in
spherical harmonics (6.102). Because
$K\propto\sin\theta'=-P^1_1(\cos\theta')$, the $\hat e_{\phi'}$ projection
picks out *only* the $\ell=1$, $m=\pm1$ terms (the same bookkeeping as
(6.101)–(6.113), where now the $\theta'$ integral
$\int P^1_\ell P^1_1\sin\theta'\,d\theta'\propto\delta_{\ell1}$). The result
must therefore be of the pure $\ell=1$ form
$$A_\phi=\frac{4\pi\sigma\omega a}{3c}\sin\theta\times
\begin{cases}r, & r<a\\ a^3/r^2, & r>a\end{cases}$$
(the coefficient fixed by the $\ell=1$ radial factor
$\frac{4\pi}{3}\frac{r_<}{r_>^2}\,a^2\cdot\frac{\sigma\omega a}{c}$, continuous
at $r=a$). Then $\vec B=\vec\nabla\times(A_\phi\hat e_\phi)$:
$$B_r=\frac{1}{r\sin\theta}\partial_\theta(\sin\theta A_\phi),\qquad
B_\theta=-\frac1r\partial_r(rA_\phi).$$
Inside ($A_\phi\propto r\sin\theta$, i.e. $\vec A=\frac12\vec B_0\times\vec x$):
$B_r=\frac{8\pi\sigma\omega a}{3c}\cos\theta$,
$B_\theta=-\frac{8\pi\sigma\omega a}{3c}\sin\theta$, which is the uniform
field $\frac{8\pi a\sigma\omega}{3c}\hat z$. ✓ Outside
($A_\phi=\frac{m\sin\theta}{r^2}$ with $m=\frac{4\pi\sigma\omega a^4}{3c}$):
$B_r=\frac{2m\cos\theta}{r^3}$, $B_\theta=\frac{m\sin\theta}{r^3}$ — exactly
the point dipole (6.154)–(6.155). The magnetization-sphere identification:
$K_{\rm eff}=cM_0\sin\theta\,\hat e_\phi$ (6.268) matches
$K=\sigma\omega a\sin\theta\,\hat e_\phi$ at $M_0=\sigma\omega a/c$, and then
$B_{\rm in}=\frac{8\pi}{3}M_0$ ✓, $m=\frac{4\pi a^3}{3}M_0$ ✓ ((6.259),
(6.267)).

### P14.  Exercise 6.7.4 — Rotating uniformly charged solid sphere  *(Wilcox 2e §6.15, p.322)*
A solid sphere of radius $a$, uniform charge density $\rho$, spins at
$\omega$ about $\hat z$.
(a) Show the exterior field is a perfect dipole with
$m=4\pi a^5\omega\rho/(15c)$.
(b) Show the interior field is an $r$-dependent dipole field with
$m(r)=4\pi r^5\omega\rho/(15c)$ plus a $\hat z$-directed field that vanishes
at $r=a$.
*Answer:* (a) as stated; (b) the extra term is
$\frac{4\pi\rho\omega}{3c}(a^2-r^2)\hat z$.
*Check:* closed forms vs exact-shell superposition (P13 per shell, radially
split quadrature), $10^{-8}$; exterior equals `dipole_B`; continuity across
$r=a$ (`test_p14_rotating_solid_sphere`).

**Solution.** Slice into shells of radius $r'$, surface density
$\sigma_{\rm eff}=\rho\,dr'$, and superpose P13.
*Outside* ($r>a$): every shell is a dipole,
$$m=\int_0^a\frac{4\pi(\rho\,dr')\,\omega r'^4}{3c}
=\frac{4\pi\rho\omega}{3c}\,\frac{a^5}{5}=\frac{4\pi a^5\omega\rho}{15c}. \checkmark$$
*Inside* ($r<a$): shells with $r'<r$ act as dipoles, accumulating
$m(r)=4\pi r^5\omega\rho/(15c)$ — the same integral cut at $r$; shells with
$r'>r$ each contribute their uniform interior field
$\frac{8\pi r'(\rho\,dr')\omega}{3c}\hat z$, summing to
$$\int_r^a\frac{8\pi\rho\omega r'}{3c}dr'\,\hat z
=\frac{4\pi\rho\omega}{3c}\,(a^2-r^2)\,\hat z,$$
which indeed vanishes at $r=a$, where the total field joins the exterior
dipole continuously (no surface current at the outer boundary: $\vec K$ is a
volume effect here). So
$\vec B_{\rm in}=\vec B_{\rm dip}\bigl(m(r)\bigr)+\frac{4\pi\rho\omega}{3c}(a^2-r^2)\hat z$. ✓

### P15.  Exercise 6.7.5 — Rotating shell with $\sigma=\sigma_0\cos\theta$: pure quadrupole  *(Wilcox 2e §6.15, p.323)*
The rotating shell of P13 (radius $a$, frequency $\omega$) now has
$\sigma(\theta)=\sigma_0\cos\theta$, giving surface current
$\vec K=\omega a\,\sigma(\theta)\sin\theta\,\hat e_\phi$. Show that
$$\vec B=\begin{cases}
\dfrac{4\pi\sigma_0\omega}{5c}\,(-x\,\hat x-y\,\hat y+2z\,\hat z), & r<a,\\[1ex]
\dfrac{4\pi\sigma_0 a^5\omega}{5c\,r^7}\,
\bigl[x(5z^2-r^2)\hat x+y(5z^2-r^2)\hat y-z\bigl(5(x^2{+}y^2)-2r^2\bigr)\hat z\bigr], & r>a.
\end{cases}$$
*Answer:* as stated — a linear (harmonic) interior field and a pure
quadrupole exterior (see P21c for its $s_{ij}$).
*Check:* both branches vs Biot–Savart ring quadrature, $2\times10^{-6}$;
exterior $1/r^4$ falloff exact (`test_p15_costheta_shell`).

**Solution.** Now $K_\phi=\omega a\sigma_0\cos\theta\sin\theta
=-\frac{\omega a\sigma_0}{3}P^1_2(\cos\theta)$ (Condon–Shortley
$P^1_2=-3\cos\theta\sin\theta$): a *pure $\ell=2$* current, so the same
projection as P13 leaves only the $\ell=2$ radial pair. The regular/decaying
combination continuous at $r=a$ is
$$A_\phi=\frac{4\pi\omega a\sigma_0}{5c}\cdot\Bigl(-\frac{P^1_2(\cos\theta)}{3}\Bigr)\times
\begin{cases}r^2/a, & r<a\\ a^4/r^3, & r>a\end{cases}
=\frac{4\pi\omega a\sigma_0}{5c}\,\cos\theta\sin\theta\times
\begin{cases}r^2/a\\ a^4/r^3\end{cases}$$
(coefficient from the $\ell=2$ kernel $\frac{4\pi}{5}\frac{r_<^2}{r_>^3}$
and the projection integral
$\int_0^\pi P^1_2P^1_2\sin\theta\,d\theta=\frac{2\cdot4!}{5\cdot2!\cdot... }
=\frac{12}{5}$, folded with the $a^2$ area factor). Taking
$B_r=\frac{1}{r\sin\theta}\partial_\theta(\sin\theta A_\phi)$,
$B_\theta=-\frac1r\partial_r(rA_\phi)$:
*inside* $A_\phi\propto r^2\sin\theta\cos\theta$ gives
$B_r=\frac{4\pi\sigma_0\omega}{5c}\,r\,(3\cos^2\theta-1)$,
$B_\theta=-\frac{4\pi\sigma_0\omega}{5c}\,3r\sin\theta\cos\theta$; converting
with $x=r\sin\theta\cos\phi$ etc. gives exactly
$\frac{4\pi\sigma_0\omega}{5c}(-x,-y,2z)$ — divergence-free and curl-free
(a harmonic $\ell=2$ interior field, the magnetostatic analog of a uniform
field gradient). *Outside* the same derivatives of $a^4/r^3$ produce the
quoted Cartesian quadrupole, falling as $1/r^4$ — no net moment: the shell's
dipole $\propto\int\sigma_0\cos\theta\cdot\sin^2\theta\,(\dots)$ integrates
to zero, so the leading multipole is $\ell=2$. Both branches agree at $r=a$
except for the $K$-sheet jump in $B_\theta$, as they must.

### P16.  Exercise 6.8.1 — Solenoid outside field and its dipole reading  *(Wilcox 2e §6.15, p.323)*
(a) Following P6 but for $|z|>d/2$, show the solenoid's axial field is
$$B_z=\frac{4\pi anI}{c}\int_0^\infty dk\,J_1(ka)J_0(k\rho)\,e^{-k|z|}\sinh(kd/2).$$
(b) For $|z|\gg d,\rho,a$, show
$B_z\simeq\dfrac{2\pi a^2IN}{c}\dfrac{1}{|z|^3}$, $N\equiv nd$ the total
number of turns.
(c) Recover (b) by treating the solenoid as a point dipole.
*Answer:* as stated; the dipole moment is $m=NI\pi a^2/c$.
*Check:* Bessel form vs the loop stack ($2\times10^{-6}$); far-field ratio to
$2\pi a^2IN/(c|z|^3)$ and to `dipole_B` with $m=\pi a^2IN/c$ within the
expected $O((d/z)^2)$ corrections (`test_p16_solenoid_outside_dipole`).

**Solution.** (a) Same superposition as P6, but with $|z|>d/2$ the field
point is outside the $z_0$ range and $|z-z_0|=|z|-z_0\,\mathrm{sign}(z)$
never changes branch:
$$\int_{-d/2}^{d/2}k\,e^{-k|z-z_0|}\,dz_0
=e^{-k|z|}\bigl(e^{kd/2}-e^{-kd/2}\bigr)=2\,e^{-k|z|}\sinh(kd/2),$$
which in (6.84) gives the stated $B_z$ (and the matching
$B_\rho\propto J_1(k\rho)$ form with the same kernel). ✓
(b) On axis, $e^{-k|z|}$ confines $k\lesssim1/|z|$, small enough that
$J_1(ka)\simeq ka/2$, $J_0\simeq1$, $\sinh(kd/2)\simeq kd/2$:
$$B_z\simeq\frac{4\pi anI}{c}\,\frac{a}{2}\,\frac{d}{2}\int_0^\infty k^2e^{-k|z|}dk
=\frac{\pi a^2 n d\,I}{c}\,\frac{2}{|z|^3}=\frac{2\pi a^2IN}{c\,|z|^3}. \checkmark$$
(c) Each turn is a loop of moment $I\pi a^2/c$ (6.157); $N$ turns give
$m=NI\pi a^2/c$ along $\hat z$. On the axis of a dipole (6.154),
$B_z=2m/|z|^3=2\pi a^2IN/(c|z|^3)$ — the multipole expansion reproduces the
$k\to0$ limit of the exact kernel: the three factors $ka/2$, $kd/2$, $k$ in
(b) are precisely the loop area, the turn count and the dipole differentiation.

### P17.  Exercise 6.8.2 — Shaved magnet slab $\equiv$ rim current $I=cM_0d$  *(Wilcox 2e §6.15, pp.323–324)*
An extremely thin flat wafer of thickness $d$ is shaved off the end of a
permanent magnet (Fig. 6.29); inside it $\vec M=M_0\hat n$, uniform and
perpendicular to its faces. Show its field is that of a wire circuit along
its outer boundary $C$ carrying $I=cM_0d$ — i.e.
$$\vec A=M_0d\oint_C\frac{d\vec\ell'}{|\vec x-\vec x'|}$$
(cf. (6.42), (6.22); flatness is unnecessary as long as $\vec M$ stays
perpendicular to the wafer).
*Answer:* as stated.
*Check:* $\vec B$ of the wafer (magnetic-charge picture: two disks
$\sigma_m=\pm M_0$) vs Biot–Savart of the rim loop with $I=cM_0d$: relative
deviation $<2\times10^{-4}$ at $d=0.02R$, shrinking as $d^2$
(`test_p17_shaved_magnet_rim_current`).

**Solution.** *Route 1 (effective currents).* Uniform $\vec M$ has
$\vec J_{\rm eff}=c\vec\nabla\times\vec M=0$ in the bulk. On the two faces
$\hat n'=\pm\hat n\parallel\vec M$, so $\vec K_{\rm eff}=c\vec M\times\hat n'=0$
there; only the rim (outward normal $\hat\nu\perp\hat n$) carries
$\vec K_{\rm eff}=cM_0\,\hat n\times\hat\nu$ — a current of surface density
$cM_0$ circulating around $C$ (right-handed about $\vec M$). Integrated over
the thickness it is a line current $I=|\vec K|\,d=cM_0d$. Hence, by (6.42)
restricted to a line current (6.22),
$\vec A=\frac{I}{c}\oint_C d\vec\ell'/|\vec x-\vec x'|=M_0d\oint_Cd\vec\ell'/g$. ✓
*Route 2 (dipole superposition, the Ex. 6.13.1 result).* From P33,
$\vec A=\int(\vec\nabla'\times\vec M)/g\,-\oint(\hat n'\times\vec M)/g$: the
volume term dies, the face terms die ($\hat n'\parallel\vec M$), and the rim
term is the same line integral.
*Route 3 (Stokes).* For the thin wafer,
$\vec A=\int d^3x'\,\vec M\times\vec\nabla'(1/g)
= M_0d\int_S da'\,\hat n\times\vec\nabla'(1/g)$, and the surface-curl
corollary of Stokes' theorem, $\int_S(\hat n\times\vec\nabla')f\,da'=\oint_Cf\,d\vec\ell'$,
lands on the same answer — this route shows the *curved* wafer works too,
since only $\vec M\parallel\hat n'$ (locally) was used. The check compares
fields, not potentials: outside the material $\vec B=\vec H$ of the two
$\pm M_0$ charged faces, which converges to the rim-loop Biot–Savart field
quadratically in $d$.

### P18.  Exercise 6.8.3 — Two magnetic moments by $\oint\vec x\times d\vec\ell$  *(Wilcox 2e §6.15, p.324)*
(a) Find the magnetic moment of the saddle circuit of Fig. 6.30(a): two
semicircular arcs of radius $R$ standing in parallel vertical planes a
distance $L$ apart (one bulging up, the other down), joined by two straight
legs of length $L$; concretely (our parametrization of the figure, current
$I$): semicircle in the $y$–$z$ plane at $x=0$ from the origin to $(0,2R,0)$
bulging $+z$; leg to $(-L,2R,0)$; semicircle at $x=-L$ bulging $-z$; leg back
to the origin.
(b) A circular loop of radius $R$ is bent by $90^\circ$ along a diameter
(the $x$ axis, Fig. 6.30(b)); find its moment.
*Answer:* (a) $\vec m=\frac{I}{c}\bigl(-\pi R^2\,\hat x+2RL\,\hat z\bigr)$,
$|\vec m|=\frac{IR}{c}\sqrt{\pi^2R^2+4L^2}$ — the two arc projections
combine into one full circle ($\pi R^2$) perpendicular to the legs, the legs
and arc chords into a $2R\times L$ rectangle in the plane.
(b) $\vec m=\frac{I\pi R^2}{2c}(\hat y+\hat z)$ for the $y<0$ half folded up
about the $x$ axis (the opposite fold flips the $\hat y$ sign);
$|\vec m|=\pi IR^2/(\sqrt2\,c)$, at $45^\circ$ between the two half-disk
normals.
*Check:* `circuit_moment` (the $\frac{1}{2c}\oint\vec x\times d\vec\ell$
quadrature) vs both closed forms, plus origin-independence of the quadrature
(`test_p18_saddle_and_bent_moments`).

**Solution.** For a line current (6.131),
$\vec m=\frac{I}{2c}\oint\vec x\times d\vec\ell$, equivalently the directed
area $\vec m=\frac Ic\vec S$ (6.133): $S_i$ = signed area of the circuit's
projection onto the plane $\perp\hat e_i$.
(a) *Projection on the $x$–$y$ plane* ($S_z$): the arcs project onto the two
segments $y\in[0,2R]$ at $x=0,-L$; the circuit projects to the
$2R\times L$ rectangle traversed once; with the parametrization above the
traversal is counterclockwise seen from $+z$… tracking the order
(origin $\to(0,2R)\to(-L,2R)\to(-L,0)\to$ origin) the loop runs
*clockwise* in the conventional $(x,y)$ orientation? Compute honestly:
$\frac12\oint(x\,dy-y\,dx)$ over that rectangle path gives $+2RL$ — the
quadrature settles the sign: $S_z=+2RL$.
*Projection on the $y$–$z$ plane* ($S_x$): the legs project to points; arc 1
(at $x=0$, bulging $+z$) traverses $(0,0)\to(R,R)_{\;(y,z)}\to(2R,0)$, arc 2
(at $x=-L$, bulging $-z$) traverses $(2R,0)\to(R,-R)\to(0,0)$: together a
*full circle* of radius $R$ traversed clockwise in the $(y,z)$ plane, i.e.
$S_x=-\pi R^2$. *Projection on $x$–$z$*: the two arcs trace the same
half-disk boundary in opposite senses — cancels; the legs are collinear
segments: $S_y=0$. Hence
$\vec m=\frac Ic(-\pi R^2,0,2RL)$. (The saddle geometry is exactly why the
arcs *add* in $S_x$: one bulges up traversed forward, the other bulges down
traversed backward.)
(b) Each half is a half-disk of area $\pi R^2/2$; the unbent half (in the
$x$–$y$ plane, traversed counterclockwise from $+z$) contributes
$\frac{I\pi R^2}{2c}\hat z$; the folded half lies in the $x$–$z$ plane and,
for the fold that lifts the $y<0$ half to $z>0$, its traversal
$(-R,0)\to(0,R)\to(R,0)$ in $(x,z)$ has directed area $+\frac{\pi R^2}{2}\hat y$
(verified by the quadrature). Total
$\vec m=\frac{I\pi R^2}{2c}(\hat y+\hat z)$, magnitude
$\pi IR^2/(\sqrt2c)$ — bending a loop by $90^\circ$ cuts its moment by
$1/\sqrt2$ and rotates it to bisect the fold.

### P19.  Exercise 6.8.4 — The point dipole's delta field and current  *(Wilcox 2e §6.15, p.325)*
(a) Show that $\vec A_m=\dfrac{\vec m\times\vec r}{r^3}$ implies
$$\vec B_m=\frac{8\pi}{3}\vec m\,\delta(\vec x)+\frac{3\vec r(\vec m\cdot\vec r)-\vec m r^2}{r^5}.$$
(b) Show $\vec\nabla\times\vec B_m=\frac{4\pi}{c}\vec J_m$ with
$\vec J_m=-c\,\vec m\times\vec\nabla\delta(\vec x)$.
[Hint: the identity for $\nabla_i\nabla_j\frac1r$, Eq. (6.139).]
*Answer:* as stated.
*Check:* the (6.139) box integrals: diagonal $=-4\pi/3$, off-diagonal $=0$
($10^{-6}$); $\int_{\rm ball}\vec B\,d^3x=\frac{8\pi}{3}\vec m$ by the
surface form $\oint\hat n\times\vec A\,da$; the smeared
$\vec J_m$ reproduces $\vec m$ through (6.129); the $r\ne0$ field is
curl-free (`test_p19_dipole_delta_field`).

**Solution.** (a) Write $(\vec m\times\vec r/r^3)_k
=-\varepsilon_{klm}m_l\partial_m\frac1r$ (since $\vec r/r^3=-\vec\nabla\frac1r$).
Then
$$B_i=\varepsilon_{ijk}\partial_j A_k
=-\varepsilon_{ijk}\varepsilon_{klm}\,m_l\,\partial_j\partial_m\frac1r
=-\bigl(\delta_{il}\delta_{jm}-\delta_{im}\delta_{jl}\bigr)m_l\partial_j\partial_m\frac1r
=-m_i\nabla^2\frac1r+\sum_j m_j\partial_j\partial_i\frac1r .$$
The first term is $+4\pi m_i\,\delta(\vec x)$. For the second use (6.139),
$\partial_i\partial_j\frac1r=\frac{3x_ix_j-r^2\delta_{ij}}{r^5}
-\frac{4\pi}{3}\delta_{ij}\delta(\vec x)$ (its diagonal delta weight
$-4\pi/3$ is the box-flux computation checked numerically; off-diagonal
terms carry no delta):
$$\vec B_m=4\pi\vec m\,\delta-\frac{4\pi}{3}\vec m\,\delta
+\frac{3\vec r(\vec m\cdot\vec r)-\vec m r^2}{r^5}
=\frac{8\pi}{3}\vec m\,\delta(\vec x)+\vec B_{\rm dip}. \checkmark$$
(The $\frac{8\pi}{3}\vec m$ weight — versus the electric dipole's
$-\frac{4\pi}{3}\vec p$ (6.147) — is what the ball-integral check measures:
$\int_{\rm ball}\vec\nabla\times\vec A=\oint\hat n\times\vec A\,da
=\frac{8\pi}{3}\vec m$ for any ball centered on the dipole, since the
traceless dipole term integrates to zero.)
(b) With $\vec\nabla\cdot\vec A_m=0$ (it is $-\vec m\cdot\vec\nabla\times\vec\nabla\frac1r$-type,
i.e. the divergence of a curl-like object: explicitly
$\vec\nabla\cdot(\vec m\times\vec F)=-\vec m\cdot\vec\nabla\times\vec F=0$ for
the gradient field $\vec F=-\vec\nabla\frac1r$),
$$\vec\nabla\times\vec B_m=\vec\nabla\times(\vec\nabla\times\vec A_m)
=-\nabla^2\vec A_m
=+\vec m\times\vec\nabla\bigl(\nabla^2\tfrac1r\bigr)
=\vec m\times\vec\nabla(-4\pi\delta)
=\frac{4\pi}{c}\bigl[-c\,\vec m\times\vec\nabla\delta(\vec x)\bigr],$$
identifying $\vec J_m=-c\,\vec m\times\vec\nabla\delta$. ✓ Its moment closes
the loop: $\frac1{2c}\int\vec x\times\vec J_m
=-\frac12\int\vec x\times(\vec m\times\vec\nabla\delta)
=\vec m$ after one integration by parts (checked with a Gaussian-smeared
delta). This is the magnetic twin of $\rho=-\vec p\cdot\vec\nabla\delta$
(6.150).

### P20.  Exercise 6.8.5 — Magnetic quadrupole moments $m_{ij}$  *(Wilcox 2e §6.15, pp.325–326)*
For a localized magnetostatic current $J_i(\vec x')$:
(a) Prove the cyclic identity
$0=\int d^3x'\,[\,x'_ix'_jJ_k+x'_iJ_jx'_k+J_ix'_jx'_k\,]$.
(b) Using (a), show
$$\frac1c\int d^3x'\,x'_ix'_jJ_k
=-\frac12\sum_r\bigl(\varepsilon_{kir}m_{rj}+\varepsilon_{kjr}m_{ri}\bigr),
\qquad
m_{ij}\equiv\frac2{3c}\int d^3x'\,\bigl(\vec x'\times\vec J\bigr)_i\,x'_j .$$
(c) With the third Taylor term of $1/|\vec x-\vec x'|$ (quadratic in
$\vec x'$, kernel $\frac{x'_ix'_j}{2r^5}(3x_ix_j-\delta_{ij}r^2)$), show the
next ("magnetic quadrupole") term of the expansion (6.123) is
$$A^{(q)}_k(\vec x)=-\frac{1}{2cr^5}\sum_{i,j,r}\varepsilon_{kir}\,Q_{ij}(\vec x)\,m_{rj},
\qquad Q_{ij}=3x_ix_j-r^2\delta_{ij}.$$
(With $m_{ij}$ defined as in (b) — which already carries the $1/c$ — the
prefactor is dimensionally $-\frac{1}{2r^5}$; the book's printed extra $1/c$
is redundant unless one works in $c=1$ units, as the code does.)
*Answer:* as stated.
*Check:* cyclic integrals vanish ($<10^{-5}$ of scale) for two exactly
divergence-free localized currents; the (b) relation verified component by
component; $\mathrm{tr}\,m_{ij}=0$ identically; $A_{\rm exact}-A_{\rm dipole}$
matches $A^{(q)}$ at large $r$ within 5% of the quadrupole term
(`test_p20_cyclic_identity_and_mij`, `test_p20_quadrupole_potential`).

**Solution.** (a) For static currents $\vec\nabla'\cdot\vec J=0$ (6.34), so
$$0=\int d^3x'\,\vec\nabla'\cdot\bigl(\vec J\,x'_ix'_jx'_k\bigr)
=\int(\vec\nabla'\cdot\vec J)\,x'_ix'_jx'_k
+\int\vec J\cdot\vec\nabla'(x'_ix'_jx'_k),$$
where the total-divergence integral vanishes for localized $\vec J$ (surface
at infinity) and $\vec J\cdot\vec\nabla'(x'_ix'_jx'_k)
=J_ix'_jx'_k+x'_iJ_jx'_k+x'_ix'_jJ_k$. ✓ (This generalizes (6.124) ($x'_i$
alone: $\int J_i=0$) and (6.126) (two coordinates: symmetric part).)
(b) Use (a) to remove the totally symmetric part:
$$\int x'_ix'_jJ_k=\tfrac13\int\bigl[2x'_ix'_jJ_k-x'_ix'_kJ_j-x'_jx'_kJ_i\bigr]
=\tfrac13\int\bigl[x'_i(x'_jJ_k-x'_kJ_j)+x'_j(x'_iJ_k-x'_kJ_i)\bigr].$$
Now $x'_jJ_k-x'_kJ_j=\sum_r\varepsilon_{jkr}(\vec x'\times\vec J)_r$
(contract two epsilons), so
$$\int x'_ix'_jJ_k=\tfrac13\sum_r\Bigl[\varepsilon_{jkr}\int(\vec x'\times\vec J)_rx'_i
+\varepsilon_{ikr}\int(\vec x'\times\vec J)_rx'_j\Bigr]
=\tfrac{c}{2}\sum_r\bigl[\varepsilon_{jkr}m_{ri}+\varepsilon_{ikr}m_{rj}\bigr],$$
using the definition of $m_{ij}$ ($\int(\vec x'\times\vec J)_rx'_i=\frac{3c}{2}m_{ri}$).
Flipping $\varepsilon_{jkr}=-\varepsilon_{kjr}$, $\varepsilon_{ikr}=-\varepsilon_{kir}$
gives the stated minus-sign form. ✓ Note
$\mathrm{tr}\,m=\frac2{3c}\int(\vec x'\times\vec J)\cdot\vec x'=0$ identically.
(c) The quadratic Taylor term of (6.123) is
$$A^{(q)}_k=\frac1c\sum_{ij}\frac{3x_ix_j-r^2\delta_{ij}}{2r^5}\int x'_ix'_jJ_k\,d^3x'
=\frac{Q_{ij}}{2r^5}\cdot\Bigl(-\frac12\Bigr)\sum_r\bigl(\varepsilon_{kir}m_{rj}+\varepsilon_{kjr}m_{ri}\bigr).$$
The two $\varepsilon$-terms contribute equally under the symmetric
$\sum_{ij}Q_{ij}$ (swap $i\leftrightarrow j$ in the second), so
$$A^{(q)}_k=-\frac{1}{2r^5}\sum_{i,j,r}\varepsilon_{kir}Q_{ij}m_{rj},$$
the stated formula (with the dimensional caveat on the printed $1/c$: the
dipole term is $\vec m\times\vec x/r^3$ with no extra $c$, and $m_{ij}$ has
dimensions [dipole]$\times$[length], so no further $1/c$ can appear).

### P21.  Exercise 6.8.6 — The magnetic quadrupole field  *(Wilcox 2e §6.15, p.326)*
(a) From P20, show the magnetic quadrupole field can be written
$$B^{(q)}_k=\frac{3}{2r^7}\sum_{i,j}s_{ij}
\bigl(5x_ix_jx_k-\delta_{ik}r^2x_j-\delta_{jk}r^2x_i\bigr),\qquad
s_{ij}\equiv\tfrac12(m_{ij}+m_{ji}).$$
(b) Show $s_{ij}$ has only 5 independent components, exactly like the
electric quadrupole tensor.
(c) By direct computation or by matching Exercise 6.7.5, find the $s_{ij}$
that reproduce P15's exterior field, confirming it is a pure magnetic
quadrupole.
*Answer:* (a) as stated (only the symmetric part of $m_{ij}$ survives the
curl); (b) symmetric ($6$) and traceless ($-1$) $\Rightarrow5$;
(c) $s_{11}=s_{22}=-\dfrac{8\pi\sigma_0a^5\omega}{45c}$,
$s_{33}=+\dfrac{16\pi\sigma_0a^5\omega}{45c}$ (diagonal, azimuthally
symmetric, traceless).
*Check:* $B^{(q)}$ equals $\vec\nabla\times A^{(q)}$ numerically (including
an $m_{ij}$ with antisymmetric part — which drops from the curl);
$\mathrm{tr}\,s\approx0$; the (c) tensor from the direct surface integral
matches the closed form to $10^{-8}$ and $B^{(q)}(s)$ equals P15's exterior
field to $10^{-10}$ (`test_p21_quadrupole_field`).

**Solution.** (a) Take the curl of P20's $A^{(q)}$. Two structural facts do
the work. First, split $m_{rj}=s_{rj}+a_{rj}$: the antisymmetric part
$a_{rj}=\frac12\varepsilon_{rjl}v_l$ turns
$-\frac{1}{2r^5}\varepsilon_{kir}Q_{ij}a_{rj}$ into
$\vec\nabla\times$-exact-free content — explicitly it reduces to a term
$\propto\vec\nabla(x_lv_l/r^3$-type$)$, i.e. a *gradient*, whose curl
vanishes: only $s_{ij}$ enters $\vec B$. Second, with
$\partial_l(x_ix_j/r^5)=\frac{\delta_{li}x_j+\delta_{lj}x_i}{r^5}-\frac{5x_ix_jx_l}{r^7}$
and $\partial_l r^{-3}=-3x_l/r^5$, the curl
$B^{(q)}_k=\varepsilon_{klm}\partial_lA^{(q)}_m$ contracts (two
$\varepsilon$'s again) to
$$B^{(q)}_k=\frac{3}{2r^7}\sum_{ij}s_{ij}
\bigl(5x_ix_jx_k-\delta_{ik}r^2x_j-\delta_{jk}r^2x_i\bigr)$$
after using $\mathrm{tr}\,s=0$ to drop the $\delta_{ij}$ contractions. (The
numeric identity check against $\vec\nabla\times A^{(q)}$, with a generic
non-symmetric $m_{ij}$, certifies both facts.)
(b) $s_{ij}=s_{ji}$ gives 6 components; $\mathrm{tr}\,s=\mathrm{tr}\,m=0$
(P20) removes one: **5**, matching the electric quadrupole's count — the
$\ell=2$ multiplicity $2\ell+1$.
(c) For the $\cos\theta$ shell, $\vec K=\omega a\sigma_0\cos\theta\sin\theta\,\hat e_\phi$
and $\vec x\times\vec K=-a|K|\hat e_\theta$ on the surface, so
$$m_{33}=\frac2{3c}\oint(\vec x\times\vec K)_3x_3\,da
=\frac2{3c}\,\omega a^5\sigma_0\,2\pi\int_0^\pi\cos^2\theta\sin^3\theta\,d\theta
=\frac2{3c}\,\omega a^5\sigma_0\,2\pi\cdot\frac4{15}
=\frac{16\pi\sigma_0a^5\omega}{45c},$$
and by azimuthal symmetry $+$ tracelessness
$s_{11}=s_{22}=-\frac12s_{33}=-\frac{8\pi\sigma_0a^5\omega}{45c}$
(off-diagonals vanish by the $\phi$ integrals). Plugging into (a): e.g. on
the axis $B^{(q)}_z=\frac{3}{2r^7}s_{33}\cdot3r^3=\frac{9s_{33}}{2r^4}
=\frac{8\pi\sigma_0a^5\omega}{5c\,r^4}$, exactly P15's exterior
$B_z(0,0,r)$. The full tensor match is the numeric check — P15's shell is a
pure quadrupole (no dipole, and the $\ell\ge3$ moments vanish for this
$K\propto P^1_2$ current).

### P22.  Exercise 6.9.1 — Dipole beside a straight wire  *(Wilcox 2e §6.15, p.326)*
A point magnetic dipole of arbitrary moment $\vec m$ sits at $(x_0,0,0)$
beside an infinite straight wire carrying current $I$ along the $z$ axis.
Find the force $\vec F$ and torque $\vec N$ on the dipole.
*Answer:*
$$\vec F=-\frac{2I}{c\,x_0^2}\,\bigl(m_y\,\hat x+m_x\,\hat y\bigr),\qquad
\vec N=\frac{2I}{c\,x_0}\,\bigl(-m_z\,\hat x+m_x\,\hat z\bigr).$$
*Check:* both vs quadrature over a small current loop of the same moment in
the exact wire field ($10^{-5}$ for $\vec F$; the torque agrees to the
loop's real $O(\varepsilon)$ finite-size term); $\vec N=\vec m\times\vec B$
exactly (`test_p22_wire_dipole_force_torque`).

**Solution.** The wire field is
$\vec B=\frac{2I}{c\rho^2}(-y,\,x,\,0)$, so
$$\vec m\cdot\vec B=\frac{2I}{c}\,\frac{-m_xy+m_yx}{x^2+y^2}.$$
Force (6.170): $\vec F=\vec\nabla(\vec m\cdot\vec B)$ at $(x_0,0,0)$:
$$\partial_x(\vec m\cdot\vec B)\Big|_{(x_0,0,0)}
=\frac{2I}{c}\Bigl[\frac{m_y}{x_0^2}-\frac{2x_0^2m_y}{x_0^4}\Bigr]=-\frac{2Im_y}{cx_0^2},\qquad
\partial_y(\cdots)\Big|=\frac{2I}{c}\Bigl[\frac{-m_x}{x_0^2}\Bigr]=-\frac{2Im_x}{cx_0^2},$$
and $\partial_z=0$: $\vec F=-\frac{2I}{cx_0^2}(m_y,m_x,0)$. ✓ (Note the
pattern: the $m_x$ part is pulled sideways, the $m_y$ part radially; an
$\vec m\parallel\hat z$ dipole feels *no* force — $\vec m\cdot\vec B=0$
everywhere — but does feel a torque.)
Torque (6.177): with $\vec B(x_0,0,0)=\frac{2I}{cx_0}\hat y$,
$$\vec N=\vec m\times\vec B=\frac{2I}{cx_0}\,\vec m\times\hat y
=\frac{2I}{cx_0}\,(-m_z,\,0,\,m_x). \checkmark$$
The torque tries to align $\vec m$ with the local $\hat e_\phi=\hat y$; the
force then pulls the aligned dipole toward the wire ($\vec m=m\hat y$:
$\vec F=-\frac{2Im}{cx_0^2}\hat x$, attraction — a small co-circulating loop
is drawn in, "likes attract").

### P23.  Exercise 6.9.2 — $\vec F=\vec\nabla(\vec m\cdot\vec B)$ from the loop force  *(Wilcox 2e §6.15, pp.326–327)*
Starting from $\vec F=\frac{I}{c}\oint d\vec x\times\vec B(\vec x)$ and the
first-order Taylor expansion
$B_i(\vec x)\approx B_i(0)+\vec x\cdot\vec\nabla'B_i(\vec x')|_{\vec x'=0}$,
re-derive $\vec F\approx\vec\nabla(\vec m\cdot\vec B)$ with
$\vec m=\frac{I}{2c}\oint\vec x\times d\vec x$.
*Answer:* derivation below (uses $\oint dx_j=0$, the antisymmetry
$\oint x_ldx_j=-\oint x_jdx_l$, and $\vec\nabla\cdot\vec B=0$).
*Check:* Biot–Savart quadrature of $\oint d\vec x\times\vec B$ for a small
tilted loop in a distant-dipole external field equals
$\vec\nabla(\vec m\cdot\vec B)$ by finite differences, $2\times10^{-5}$,
both for the parametrized circle and for a polygon
(`test_p23_force_is_grad_mB`).

**Solution.** Insert the expansion:
$$F_i=\frac Ic\,\varepsilon_{ijk}\oint dx_j\,B_k(\vec x)
\approx\frac Ic\,\varepsilon_{ijk}\Bigl[B_k(0)\underbrace{\oint dx_j}_{0}
+\partial'_lB_k\oint x_l\,dx_j\Bigr].$$
Around a closed loop $\oint d(x_lx_j)=0$ gives
$\oint x_ldx_j=-\oint x_jdx_l$: the object is antisymmetric in $(l,j)$, so
it is dual to the directed area,
$$\oint x_l\,dx_j=\sum_m\varepsilon_{ljm}\,S_m,\qquad
\vec S\equiv\tfrac12\oint\vec x\times d\vec x=\frac{c}{I}\,\vec m .$$
(Contract: $\sum_{lj}\varepsilon_{ljm}\oint x_ldx_j=2S_m$ ✓.) Then
$$F_i=\frac Ic\,\varepsilon_{ijk}\varepsilon_{ljm}\,S_m\,\partial_lB_k
=\frac Ic\bigl(\delta_{kl}\delta_{im}-\delta_{km}\delta_{il}\bigr)S_m\partial_lB_k
=\frac Ic\Bigl[S_i\,\partial_kB_k-S_k\,\partial_iB_k\Bigr]\cdot(-1)$$
— care with the contraction:
$\varepsilon_{ijk}\varepsilon_{ljm}=\varepsilon_{jki}\varepsilon_{jml}
=\delta_{km}\delta_{il}-\delta_{kl}\delta_{im}$, so
$$F_i=\frac Ic\bigl[S_k\partial_iB_k-S_i\partial_kB_k\bigr]
=m_k\partial_iB_k-m_i(\vec\nabla\cdot\vec B)
=\partial_i(\vec m\cdot\vec B),$$
using $\vec\nabla\cdot\vec B=0$ (6.27) and constant $\vec m$. ✓ This is
(6.170) re-derived at the level of a single rigid loop; no assumption
$\vec\nabla\times\vec B=0$ was needed (that would further convert it to
$(\vec m\cdot\vec\nabla)\vec B$, (6.171)).

### P24.  Exercise 6.10.1 — Surface torque $\Rightarrow\ \vec N=\vec m\times\vec B_0$; hemisphere  *(Wilcox 2e §6.15, pp.327–328)*
(a) Using the bound surface current $\vec K_{\rm eff}=c\vec M\times\hat n$
and the surface torque on a uniformly magnetized body in a uniform field,
$$\vec N=\oint_S da\;\vec x\times\Bigl(\frac1c\vec K_{\rm eff}\times\vec B_0\Bigr),$$
show $\vec N=\vec m\times\vec B_0$ with $\vec m=\int d^3x\,\vec M$
(consistent with (6.177) — but now showing *where on the body* the torque
acts).
(b) A hemisphere of radius $a$ with uniform $\vec M=M_0\hat k$ sits in
$\vec B_0=B_0\hat x$ (Fig. 6.31). Evaluate the torque.
*Answer:* (a) proved below; (b)
$\vec N=\frac{2\pi a^3M_0B_0}{3}\,\hat y$ (i.e. $\vec m\times\vec B_0$ with
$\vec m=\frac{2\pi a^3}{3}M_0\hat k$; only the curved face carries
$\vec K_{\rm eff}$).
*Check:* the surface-torque quadrature over the dome equals
$\vec m\times\vec B_0$ for both the given and a generic $\vec B_0$, $10^{-8}$
(`test_p24_hemisphere_torque`).

**Solution.** (a) With $\vec A\equiv\vec M$ (constant), $\hat n$ the outward
normal, expand the double cross product
$(\vec M\times\hat n)\times\vec B_0=\hat n\,(\vec M\cdot\vec B_0)-\vec M\,(\hat n\cdot\vec B_0)$:
$$\vec N=(\vec M\cdot\vec B_0)\oint da\,\vec x\times\hat n
-\oint da\,(\hat n\cdot\vec B_0)\,\vec x\times\vec M .$$
First integral: $\oint\vec x\times\hat n\,da=-\int\vec\nabla\times\vec x\,d^3x=0$.
Second: for constant $\vec B_0$ and $\vec f(\vec x)=\vec x\times\vec M$,
the divergence theorem componentwise gives
$\oint da\,(\hat n\cdot\vec B_0)f_i=\int d^3x\,(\vec B_0\cdot\vec\nabla)f_i$,
and $(\vec B_0\cdot\vec\nabla)(\vec x\times\vec M)=\vec B_0\times\vec M$.
Hence
$$\vec N=-\int d^3x\,\vec B_0\times\vec M=\Bigl(\int\vec M\,d^3x\Bigr)\times\vec B_0
=\vec m\times\vec B_0. \checkmark$$
So although the formula is the familiar dipole torque, it is delivered
entirely by the $\vec K_{\rm eff}\times\vec B_0$ stress on the *surface*
(for uniform $\vec M$ there is no volume current to push on).
(b) $\vec m=\vec M\,V=\frac{2\pi a^3}{3}M_0\hat k$. On the flat face
$\hat n=-\hat k\parallel\vec M$, so $\vec K_{\rm eff}=0$ there — the entire
torque comes from the dome, where
$\vec K_{\rm eff}=cM_0\sin\theta\,\hat e_\phi$. The quadrature over the dome
alone indeed returns
$$\vec N=\vec m\times\vec B_0=\frac{2\pi a^3M_0B_0}{3}\,(\hat k\times\hat x)
=\frac{2\pi a^3M_0B_0}{3}\,\hat y .$$

### P25.  Exercise 6.10.2 — Dipole centered in a spherical cavity / permeable sphere  *(Wilcox 2e §6.15, p.328)*
A point dipole $\vec m$ sits at the center of a vacuum sphere of radius $a$
carved out of an infinite medium of permeability $\mu$ (Fig. 6.32).
(a) With the ansatz
$$\vec A_{\rm in}=\frac{\vec m\times\vec r}{r^3}+\frac{C_1}{a^3}\,\vec m\times\vec r,\qquad
\vec A_{\rm out}=C_2\,\frac{\vec m\times\vec r}{r^3},$$
find $C_{1,2}$ and the fields.
(b) Same dipole at the center of a sphere of permeability $\mu$ surrounded
by vacuum: find $\vec B$ inside and outside. [Hint: get (b) from (a)
cheaply.]
(c) Find the bound surface current $\vec K_b$ in (a) and show it has the
same form as the free current of the rotating shell (Ex. 6.7.3), the two
problems mapping into each other under
$\sigma\omega a\leftrightarrow\frac{3c\,m}{4\pi a^3}\frac{\mu-1}{2\mu+1}$.
*Answer:* (a) $C_1=\dfrac{\mu-1}{2\mu+1}$, $C_2=\dfrac{3\mu}{2\mu+1}$:
$\vec B_{\rm in}=\vec B_{\rm dip}(\vec m)+\frac{2C_1}{a^3}\vec m$ (dipole
plus a uniform field), $\vec B_{\rm out}=C_2\vec B_{\rm dip}(\vec m)$.
(b) $C_1'=\dfrac{1-\mu}{2+\mu}$, $C_2'=\dfrac{3}{\mu+2}$ — the (a) result
with $\mu\to1/\mu$. (c) $\vec K_b=cM_\theta\,\hat e_\phi$ with
$M_\theta=\frac{\mu-1}{4\pi}\frac{C_2}{\mu}\frac{m}{a^3}\sin\theta$, i.e.
$K_b\propto\sin\theta\,\hat e_\phi$ exactly like $K_f=\sigma\omega a\sin\theta\,\hat e_\phi$,
with the stated correspondence (per unit $m$).
*Check:* the closed-form $C$'s satisfy both boundary conditions
algebraically and the assembled fields satisfy them numerically at many
angles ($B_r$ continuous, $H_\theta$ continuous, $10^{-4}$ by finite
differences); the $\mu\to1/\mu$ map verified; the $K_b$ coefficient formula
checked (`test_p25_dipole_cavity_and_sphere`).

**Solution.** (a) $\vec\nabla\times(\vec m\times\vec r)=2\vec m$, so the
ansatz fields are
$$\vec B_{\rm in}=\vec B_{\rm dip}+\frac{2C_1}{a^3}\vec m,\qquad
\vec B_{\rm out}=C_2\,\vec B_{\rm dip},$$
with $\vec B_{\rm dip}$ the point-dipole field (6.152, $r\ne0$). For
$\vec m=m\hat z$: $B_r=\frac{2m\cos\theta}{r^3}(\cdots)$,
$B_\theta=\frac{m\sin\theta}{r^3}(\cdots)$, and the uniform piece adds
$\frac{2C_1m}{a^3}(\cos\theta,-\sin\theta)$ in $(r,\theta)$.
Boundary conditions at $r=a$: $B_r$ continuous (6.204) and $H_\theta$
continuous (6.205, no free surface current), with
$\vec H_{\rm in}=\vec B_{\rm in}$ (vacuum), $\vec H_{\rm out}=\vec B_{\rm out}/\mu$:
$$\frac{2m}{a^3}(1+C_1)=\frac{2m}{a^3}C_2
\;\Rightarrow\;1+C_1=C_2;\qquad
\frac{m}{a^3}(1-2C_1)=\frac{m}{\mu a^3}C_2
\;\Rightarrow\;\mu(1-2C_1)=C_2 .$$
Solving: $C_1=\frac{\mu-1}{2\mu+1}$, $C_2=\frac{3\mu}{2\mu+1}$. ✓ For
$\mu>1$ the cavity field is *boosted* along $\vec m$ (the medium's
magnetization adds a uniform field), and the far dipole is enhanced by
$C_2>1$; $\mu\to\infty$: $C_1\to\frac12$, $C_2\to\frac32$.
(b) Swapping which side is vacuum exchanges the roles of $\vec B$ and
$\mu\vec H$: dividing both media's $\mu$'s by $\mu$ (allowed — only the
ratio enters the BCs) turns (medium $\mu$ outside, vacuum inside) into
(vacuum outside, $1/\mu$ inside)… run the same two conditions with
$\vec H_{\rm in}=\vec B_{\rm in}/\mu$, $\vec H_{\rm out}=\vec B_{\rm out}$:
$1+C_1'=C_2'$ and $\frac{1}{\mu}(1-2C_1')=C_2'$, whose solution is exactly
(a) with $\mu\to1/\mu$: $C_1'=\frac{1-\mu}{2+\mu}$, $C_2'=\frac{3}{\mu+2}$.
For $\mu>1$ the sphere now *screens*: $C_2'<1$, and the interior uniform
correction opposes $\vec m$.
(c) The medium's magnetization at $r=a^+$ is
$\vec M=\chi_m\vec H_{\rm out}=\frac{\mu-1}{4\pi}\frac{C_2}{\mu}\vec B_{\rm dip}(\vec m)/1$…
keeping the $\theta$ component (which is what survives in
$\vec M\times\hat n$):
$M_\theta=\frac{\mu-1}{4\pi}\frac{C_2}{\mu}\frac{m\sin\theta}{a^3}$. The
bound current on the cavity wall (outward normal of the *material* is
$-\hat r$) is
$$\vec K_b=c\,\vec M\times(-\hat r)=c\,M_\theta\,\hat e_\phi
=\frac{3c\,m}{4\pi a^3}\,\frac{\mu-1}{2\mu+1}\,\sin\theta\,\hat e_\phi,$$
using $\frac{\mu-1}{4\pi}\frac{C_2}{\mu}=\frac{3(\mu-1)}{4\pi(2\mu+1)}$.
This is precisely the rotating shell's $K_f=\sigma\omega a\sin\theta\,\hat e_\phi$
under $\sigma\omega a\leftrightarrow\frac{3cm}{4\pi a^3}\frac{\mu-1}{2\mu+1}$
— the cavity problem *is* Ex. 6.7.3's shell superposed on the bare dipole.

### P26.  Exercise 6.11.1 — Permeable sphere in a uniform field  *(Wilcox 2e §6.15, p.329)*
(a) Find $\Phi_m$ (hence $\vec B$, $\vec H$) for a sphere of permeability
$\mu$ and radius $a$ in a uniform external field $\vec B_0$ — the quick
route is electro/magnetostatic interchangeability applied to the dielectric
sphere (Ex. 5.7.3).
(b) Show the induced magnetization is
$\vec M=\frac{3}{4\pi}\frac{\mu-1}{\mu+2}\,\vec B_0$.
*Answer:* with $\vec B_0=B_0\hat z$,
$$\Phi_m=\begin{cases}-\dfrac{3}{\mu+2}B_0\,r\cos\theta, & r<a,\\[1ex]
-B_0\,r\cos\theta+\dfrac{\mu-1}{\mu+2}\,a^3B_0\,\dfrac{\cos\theta}{r^2}, & r>a,\end{cases}$$
so $\vec H_{\rm in}=\frac{3}{\mu+2}\vec B_0$ (uniform),
$\vec B_{\rm in}=\frac{3\mu}{\mu+2}\vec B_0$, and outside
$\vec B=\vec B_0+\vec B_{\rm dip}(m_{\rm ind})$ with
$m_{\rm ind}=\frac{\mu-1}{\mu+2}a^3B_0$; (b) as stated.
*Check:* interior uniformity and value, exterior dipole superposition, both
boundary conditions, and $\Phi_m$ continuity, all verified numerically from
the potential ($10^{-4}$ FD tolerance); the $M$ formula exact
(`test_p26_permeable_sphere`).

**Solution.** In the source-free region $\vec H=-\vec\nabla\Phi_m$ with
$\vec\nabla\cdot\vec B=0$, $\vec B=\mu\vec H$: mathematically identical to
the dielectric problem under $\vec H\leftrightarrow\vec E$,
$\vec B\leftrightarrow\vec D$, $\mu\leftrightarrow\epsilon$ (§6.11,
(6.210)–(6.211)). The dielectric sphere in $\vec E_0$ (Ex. 5.7.3) has
interior field $\frac{3}{\epsilon+2}E_0$ and exterior dipole
$\frac{\epsilon-1}{\epsilon+2}a^3E_0$; transcribing gives the stated
$\Phi_m$. Verify directly: both branches are harmonic; at $r=a$,
$\Phi_m$ continuous
($-\frac{3}{\mu+2}=-1+\frac{\mu-1}{\mu+2}$ ✓ — this is $H_\theta$
continuity), and $B_r=\mu H_r$ inside vs $H_r$ outside:
$\mu\frac{3}{\mu+2}B_0\cos\theta
=\bigl[1+2\frac{\mu-1}{\mu+2}\bigr]B_0\cos\theta=\frac{3\mu}{\mu+2}B_0\cos\theta$ ✓.
(b) $\vec M=\frac{\vec B-\vec H}{4\pi}$ inside:
$$\vec M=\frac{1}{4\pi}\Bigl(\frac{3\mu}{\mu+2}-\frac{3}{\mu+2}\Bigr)\vec B_0
=\frac{3}{4\pi}\,\frac{\mu-1}{\mu+2}\,\vec B_0. \checkmark$$
Sanity: $\mu\to\infty$ gives $B_{\rm in}\to3B_0$, $M\to\frac{3B_0}{4\pi}$
(the "perfectly permeable" saturation of the sphere geometry, demagnetizing
factor $4\pi/3$); $\mu<1$ gives $M$ opposing $B_0$ (diamagnetic screening).

### P27.  Exercise 6.12.1 — Image currents: source in vacuum over a permeable half-space  *(Wilcox 2e §6.15, pp.329–330)*
A current distribution $\vec J(\vec x)$ sits in vacuum ($z>0$) above a
semi-infinite slab of permeability $\mu\ne1$ filling $z<0$ (Fig. 6.33). Show
that for $z>0$ the field is that of $\vec J$ plus an image current
$$\vec J^*(\vec x)=\bigl(a\,J_x(x,y,-z),\;a\,J_y(x,y,-z),\;b\,J_z(x,y,-z)\bigr),
\qquad a=-b=\frac{\mu-1}{\mu+1},$$
and that for $z<0$ the field appears to come from
$\vec J^{**}=c'\,\vec J$ at the source location, $c'=\dfrac{2\mu}{\mu+1}$
(vacuum kernel).
*Answer:* as stated.
*Check:* for a tilted circular loop, the boundary-condition residuals
($B_z$ jump and $H_\parallel$ jump at $z=0$) vanish to $10^{-10}$ of the
local field at several stations; the image force on a parallel loop
(Eq. 6.237 form) is attractive for $\mu>1$, repulsive for $\mu<1$
(`test_p27_image_source_in_vacuum`).

**Solution.** Ansatz (mirroring the electrostatic (6.214)–(6.221)):
$\vec B_{z>0}={\rm BS}[\vec J]+{\rm BS}[\vec J^*]$ and
$\vec B_{z<0}={\rm BS}[c'\vec J]$, with BS the vacuum Biot–Savart operator
(6.24). The mirrored current with coefficients $(a,a,b)$, $b=-a$, is
geometrically the *mirror image* of the circuit (current path reflected in
$z=0$, which flips $dl_z$) scaled by $a$: for a planar horizontal loop this
is a coaxial loop at $-z_0$ circulating in the same sense.
Key mirror-symmetry facts at the plane $z=0$: the field of the mirror image
of a current satisfies $B^*_z(x,y,0)=+a\,B^J_z(x,y,0)$ and
$\vec B^*_\parallel(x,y,0)=-a\,\vec B^J_\parallel(x,y,0)$ (reflect the
Biot–Savart integrand; a mirror current's field is the mirror of the field
with the pseudovector flip). Then the conditions:
normal $\vec B$ continuous, and tangential $\vec H$ continuous with
$\vec H_{z<0}=\vec B_{z<0}/\mu$:
$$(1+a)\,B^J_z=c'\,B^J_z,\qquad (1-a)\,B^J_\parallel=\frac{c'}{\mu}\,B^J_\parallel$$
$$\Rightarrow\quad 1+a=c',\qquad \mu(1-a)=c'
\quad\Rightarrow\quad a=\frac{\mu-1}{\mu+1},\quad c'=\frac{2\mu}{\mu+1},$$
and $b=-a$ is forced by consistency for currents with vertical segments
(the mirror flip of $J_z$ is what keeps $\vec\nabla\cdot\vec J^*=0$ and
makes the parallel/normal field symmetries hold simultaneously). Limits:
$\mu\to1$: no image ($a\to0$, $c'\to1$); $\mu\to\infty$: $a\to1$ (the
"magnetic conductor" image, field lines forced normal to the interface);
$\mu\to0$: $a\to-1$ (superconductor limit — see P31's boundary condition).

### P28.  Exercise 6.12.2 — Image currents: source embedded in the medium  *(Wilcox 2e §6.15, p.330)*
Now the free current $\vec J(\vec x)$ is embedded *inside* the permeable
half-space ($z>0$, permeability $\mu$), with vacuum at $z<0$. Assuming
$z>0$ fields = (real $\vec J$ + image $\vec J^*$, both in the medium) and
$z<0$ fields = $\vec J^{**}$ at the source location in vacuum, find the
image coefficients. [Hint: adapt Exercise 6.12.1.]
*Answer:* $\vec J^*=\bigl(a'J_x,\,a'J_y,\,-a'J_z\bigr)(x,y,-z)$ with
$$a'=-\frac{\mu-1}{\mu+1},\qquad \vec J^{**}=\frac{2\mu}{\mu+1}\,\vec J,$$
where the $z>0$ fields carry the medium factor
($\vec B={\mu}\,{\rm BS}[\vec J+\vec J^*]$) and the $z<0$ field is the plain
vacuum ${\rm BS}[\vec J^{**}]$.
*Check:* BC residuals at $z=0$ for a tilted loop vanish to $10^{-10}$
(`test_p28_image_source_embedded`).

**Solution.** In an infinite medium $\mu$, a free current's field is
$\mu$ times its vacuum field ($\vec\nabla\times\vec B=\frac{4\pi\mu}{c}\vec J_{\rm free}$
from (6.203)), so write
$\vec B_{z>0}=\mu\bigl({\rm BS}[\vec J]+{\rm BS}[\vec J^*]\bigr)$,
$\vec B_{z<0}={\rm BS}[c''\vec J]$. The same mirror relations as P27 now
give, at $z=0$:
$$\text{(normal }B\text{):}\quad \mu(1+a')=c'';\qquad
\text{(tangential }H\text{):}\quad \frac{\mu(1-a')}{\mu}=c''\;\Rightarrow\;1-a'=c''.$$
Solving: $a'=\frac{1-\mu}{1+\mu}=-\frac{\mu-1}{\mu+1}$,
$c''=\frac{2\mu}{\mu+1}$. ✓ So the embedded source sees an image of the
*opposite* sign relative to P27 (a co-circulating loop buried in iron is
*repelled* from the surface toward the bulk), while the transmitted-side
strength happens to be the same $2\mu/(\mu+1)$ — though evaluated with the
vacuum kernel rather than the medium's. Both P27 and P28 reduce to the
same physical field when $\mu\to1$.

### P29.  Exercise 6.12.3 — Dipole layer → current loop: the solid-angle image answer  *(Wilcox 2e §6.15, pp.330–331)*
Two coincident (spacing $\Delta d\to0$) flat circular sheets carrying
$\pm\sigma$ form an electric dipole layer of strength $D=\sigma\Delta d$,
parallel to and a distance $d$ above a semi-infinite dielectric $\epsilon$
(Fig. 6.34). Using the appropriate Green function, find $\vec E$ and
$\vec D$ in both half-spaces (off the sheets), and show that
$$\epsilon\Rightarrow\mu,\qquad D\Rightarrow\frac{I}{c}$$
turns the result into the $\vec B$ field of a current loop bounding the same
circle above a permeable interface:
$$\vec B=\frac Ic\Bigl[\vec\nabla\Omega_{\rm source}
+\frac{\mu-1}{\mu+1}\vec\nabla\Omega_{\rm image}\Bigr]\ (z>0),\qquad
\vec B=\frac Ic\,\frac{2\mu}{1+\mu}\,\vec\nabla\Omega_{\rm source}\ (z<0),$$
$\Omega_{\rm source/image}$ = solid angles of the source disk (at $z=d$) and
its mirror (at $z=-d$), both with $\hat n'=+\hat z$.
*Answer:* electrostatic side:
$\Phi=-D[\Omega_{\rm src}+\lambda\Omega_{\rm img}]$ for $z>0$
($\lambda=\frac{\epsilon-1}{\epsilon+1}$),
$\Phi=-\frac{2}{\epsilon+1}D\,\Omega_{\rm src}$ for $z<0$; then
$\vec E=-\vec\nabla\Phi=D\vec\nabla[\Omega_{\rm src}+\lambda\Omega_{\rm img}]$
above and $\vec E=\frac{2D}{\epsilon+1}\vec\nabla\Omega_{\rm src}$,
$\vec D=\epsilon\vec E=\frac{2\epsilon D}{\epsilon+1}\vec\nabla\Omega_{\rm src}$
below. The substitution ($\vec E\to\vec H$, $\vec D\to\vec B$) gives the
stated $\vec B$ — magnetostatics in source-free regions is
electrostatics.
*Check:* $\frac Ic[\vec\nabla\Omega_{\rm src}+\lambda\vec\nabla\Omega_{\rm img}]$
(numerical solid-angle gradients) equals the direct Biot–Savart field of the
real + image loops for $z>0$, and the transmitted form matches the $c'$-loop
field for $z<0$, $2\times10^{-4}$ (`test_p29_solid_angle_representation`).

**Solution.** *Potential of a uniform dipole layer.* A layer of moment
density $D\hat n'$ on $S'$ has
$\Phi(\vec x)=\int_{S'}da'\,D\,\hat n'\cdot\frac{\vec x-\vec x'}{|\vec x-\vec x'|^3}
=-D\,\Omega(\vec x)$ in the book's sign convention (6.67) — e.g. just above
a large layer $\Omega=-2\pi$ and $\Phi=+2\pi D$ ✓ (the standard layer jump
$4\pi D$).
*Images.* The dielectric half-space images a charge $q$ at height $h$ as
$q^*=-\lambda q$ at $-h$ ($\lambda=\frac{\epsilon-1}{\epsilon+1}$), and
transmits $\frac{2}{\epsilon+1}q$. Image the layer sheet by sheet: the $+$
sheet (upper) maps to a $-\lambda\sigma$ sheet at the mirrored (lower)
position, the $-$ sheet to $+\lambda\sigma$ *above* it — mirroring swaps the
stacking, so the image layer has moment $+\lambda D$ along $+\hat z$
(two sign flips cancel). Hence for $z>0$,
$\Phi=-D\Omega_{\rm src}-\lambda D\,\Omega_{\rm img}$, and below,
$\Phi=-\frac{2D}{\epsilon+1}\Omega_{\rm src}$. Gradients give the stated
$\vec E$; multiplying by $\epsilon$ below gives
$\vec D=\frac{2\epsilon}{\epsilon+1}D\,\vec\nabla\Omega_{\rm src}$.
*Magnetic transcription.* In the source-free regions
$\vec H=-\vec\nabla\Phi_m$ with the same boundary mathematics
($\vec H\leftrightarrow\vec E$, $\vec B\leftrightarrow\vec D$,
$\mu\leftrightarrow\epsilon$). A current loop $I$ is the magnetic twin of a
dipole layer of strength $D=I/c$ on any spanning surface (§6.5:
$\vec B=\frac Ic\vec\nabla\Omega$ off the surface). Substituting:
$$z>0:\ \vec B=\vec H\,(\text{vacuum})=\frac Ic\vec\nabla\bigl[\Omega_{\rm src}+\tfrac{\mu-1}{\mu+1}\Omega_{\rm img}\bigr];
\qquad
z<0:\ \vec B=\mu\vec H=\frac Ic\,\frac{2\mu}{1+\mu}\vec\nabla\Omega_{\rm src},$$
which is exactly P27's image system (image loop $\lambda I$, same
circulation sense; transmitted loop $\frac{2\mu}{\mu+1}I$) — the numeric
check closes that triangle.

### P30.  Exercise 6.12.4 — General Green-function representation of $\Phi_m$  *(Wilcox 2e §6.15, p.331)*
Let $G(\vec x,\vec x';\epsilon)$ be the open-space electrostatic Green
function in the presence of dielectrics,
$\Phi(\vec x)=\int d^3x'\,G(\vec x,\vec x';\epsilon)\rho(\vec x')$. Introduce
an electric dipole surface $S'$ with the dipole sources of Eq. (6.150)
integrated over $S'$, and use P29's interchangeability
($\epsilon\Rightarrow\mu$, $D\Rightarrow I/c$) to argue
$$\Phi_m(\vec x)=\frac Ic\int_{S'}da'\,\frac{\partial}{\partial n'}G(\vec x,\vec x';\mu),
\qquad \vec H=-\vec\nabla\Phi_m,$$
for a loop of current $I$ bounding $S'$ (right-hand rule tying $\hat n'$ to
$I$; valid in source-free regions, i.e. off $S'$).
*Answer:* as stated.
*Check:* with the half-space Green function
($G=\frac1g-\lambda\frac1{g_{\rm im}}$ above, $\frac{2}{\mu+1}\frac1g$
below), $-\vec\nabla\Phi_m$ reproduces the real+image loop field for $z>0$
and $\vec B=\mu\vec H$ matches the transmitted-loop field for $z<0$,
$2\times10^{-4}$ (`test_p30_green_function_representation`).

**Solution.** A point dipole $\vec p$ at $\vec x'$ is the charge density
$\rho=-\vec p\cdot\vec\nabla'\delta(\vec x-\vec x')$ (6.150). Feeding it
through the linear relation $\Phi=\int G\rho$ and integrating by parts moves
the gradient onto $G$:
$$\Phi_{\rm dip}(\vec x)=\vec p\cdot\vec\nabla'G(\vec x,\vec x') .$$
A dipole *surface* of density $D\hat n'$ then superposes to
$$\Phi(\vec x)=D\int_{S'}da'\,\hat n'\cdot\vec\nabla'G(\vec x,\vec x';\epsilon)
=D\int_{S'}da'\,\frac{\partial G}{\partial n'},$$
the general-$G$ version of P29's $-D\Omega$ (for free space
$G=1/|\vec x-\vec x'|$ and $\int\partial_{n'}(1/g)\,da'=-\Omega$ by (6.68) —
signs consistent). Now transcribe: in regions with no free current the
magnetostatic problem is the $\mu\leftrightarrow\epsilon$ electrostatic one
(§6.11), a current loop is a dipole layer of strength $I/c$ on any spanning
surface $S'$ (P29), so
$$\Phi_m(\vec x)=\frac Ic\int_{S'}da'\,\frac{\partial}{\partial n'}G(\vec x,\vec x';\mu),\qquad
\vec H=-\vec\nabla\Phi_m,$$
with $\hat n'$ right-handed about the current. The payoff: *any* dielectric
image/Green construction (plane, sphere, layered media, …) instantly
generates the magnetostatic loop solution in matched permeable geometry —
one scalar quadrature instead of three vector ones. The representation fails
only on $S'$ itself, where the layer discontinuity ($\Phi_m$ jumps by
$4\pi I/c$) encodes the multivaluedness of the loop's scalar potential —
crossing $S'$ is how Ampère's law survives $\vec H=-\vec\nabla\Phi_m$.

### P31.  Exercise 6.12.5 — Image current in a superconducting sphere  *(Wilcox 2e §6.15, pp.331–332)*
Define a perfect electric conductor by $\vec E=\vec B=0$ inside (limits
$\epsilon\to\infty$, $\mu\to0$). A magnetostatic current $\vec J(r,\theta,\phi)$
flows outside a perfectly conducting sphere of radius $a$ (Fig. 6.35). Show
that adding the image current (defined for $r<a$)
$$\vec J^*(r,\theta,\phi)=-\Bigl(\frac ar\Bigr)^5\vec J\Bigl(\frac{a^2}{r},\theta,\phi\Bigr),
\quad\text{equivalently}\quad
\vec J^*\Bigl(\frac{a^2}{r},\theta,\phi\Bigr)=-\Bigl(\frac ra\Bigr)^5\vec J(r,\theta,\phi),$$
makes $\vec B\cdot\hat n|_{r=a}=0$ — the magnetostatic analog of the
grounded-sphere image (Ex. 3.3.3).
*Answer:* as stated. For a coaxial ring at $(r_0,\theta_0)$ carrying $I$,
the image is a ring at $(a^2/r_0,\theta_0)$ carrying $I^*=-(r_0/a)\,I$.
*Check:* $\vec B\cdot\hat r$ on $r=a$ from ring + image ring vanishes to
$10^{-6}$ of the local field at 8 surface stations; the coefficient map
ring$\to$image verified from the $(a/r)^5$ density rule
(`test_p31_conducting_sphere_image`).

**Solution.** *Ring reduction.* Decompose $\vec J$ into coaxial rings (the
$\phi$-components; poloidal pieces follow the same scaling — see below). A
ring at $(r_0,\theta_0)$ has, in spherical coordinates, only
$A_\phi(r,\theta)$, and
$$\vec B\cdot\hat r=\frac{1}{r\sin\theta}\,\partial_\theta\bigl(\sin\theta\,A_\phi\bigr),$$
so $\vec B\cdot\hat r|_{r=a}=0\iff A_\phi(a,\theta)$ is $\theta$-independent
$\iff A_\phi(a,\theta)=0$ (it must vanish at the poles). The ring potential
expands as
$$A_\phi=\frac{2\pi I\,r_0\sin\theta_0}{c}\sum_\ell\frac{P^1_\ell(\cos\theta_0)P^1_\ell(\cos\theta)}{\ell(\ell+1)}\,
\frac{r_<^\ell}{r_>^{\ell+1}},$$
(the (6.113) machinery with the source at $\theta_0$). Add an interior image
ring at $r_1<a$, same $\theta_0$, current $I^*$: for $r=a$ (outside both),
each $\ell$ term of the *sum* must vanish:
$$I\,r_0\sin\theta_0\,\frac{a^\ell}{r_0^{\ell+1}}\cdot\frac{1}{a^{\ell+1}}\Big/(\dots)
+I^*\,r_1\sin\theta_0\,\frac{r_1^\ell}{a^{\ell+1}}\cdot\frac{1}{a^{\ell}}\Big/(\dots)=0
\;\Longrightarrow\;
I^*\,r_1^{\ell+1}=-I\,\frac{a^{2\ell+1}}{r_0^{\ell}} .$$
An $\ell$-independent solution requires $r_1=a^2/r_0$ (then
$r_1^{\ell+1}=a^{2\ell+2}/r_0^{\ell+1}$), giving
$$I^*=-\frac{r_0}{a}\,I \qquad\text{at } \Bigl(\frac{a^2}{r_0},\,\theta_0\Bigr)$$
— one image ring kills *every* multipole at once, exactly like the
electrostatic sphere image. ✓
*Density form.* Write the ring as
$\vec J=\frac{I}{r_0}\delta(r-r_0)\delta(\theta-\theta_0)\hat e_\phi$ and
demand $\vec J^*(r)=-(a/r)^5\vec J(a^2/r)$: the delta transforms as
$\delta(a^2/r-r_0)=\frac{r^2}{a^2}\delta(r-a^2/r_0)$, and collecting factors
returns precisely $I^*=-(r_0/a)I$ at $r_1=a^2/r_0$ — the $(a/r)^5$ is the
Jacobian bookkeeping $(a/r)^{2}$ (delta) $\times(a/r)^{3}$ (Kelvin scaling
of a current density) that makes the rule ring-consistent and, applied
componentwise, extends it to arbitrary $\vec J$ (same fifth power as the
electrostatic image *charge density* $\rho^*=-(a/r)^5\rho(a^2/r)$ of
Ex. 3.3.3). Physically: $\mu\to0$ expels flux (P27's $a\to-1$ image in the
plane limit), and $\vec B\cdot\hat n=0$ is the superconductor (Type-1,
Meissner) boundary condition.

### P32.  Exercise 6.12.6 — Force on a dipole near a permeable slab  *(Wilcox 2e §6.15, p.332)*
A point dipole $\vec m$ sits a distance $d$ above an infinite slab of
permeability $\mu$ filling $z<0$ (Fig. 6.36); $\vec m$ points along
$(\theta,\phi)$ measured from the surface normal $\hat z$. Find the force.
Attractive or repulsive for $\mu>1$?
*Answer:*
$$\vec F=-\hat z\;\frac{3m^2\,(1+\cos^2\theta)}{16\,d^4}\;\frac{\mu-1}{\mu+1}:$$
independent of $\phi$, attractive (toward the slab) for $\mu>1$, repulsive
for $\mu<1$.
*Check:* closed form vs quadrature ($\oint d\vec l\times\vec B^*$ over a
small loop realizing $\vec m$, against its P27 image loop), $2\times10^{-4}$
at several $\theta$; sign flip across $\mu=1$ and $\phi$-independence
verified (`test_p32_dipole_slab_force`).

**Solution.** By P27, the field above the slab due to the slab is that of an
image dipole: mirror the small current loop ($z\to-z$ flips the moment's
parallel components — a pseudovector — and the image coefficient $a=\lambda$
scales it):
$$\vec m^*=\lambda\,\bigl(-m_x,\,-m_y,\,+m_z\bigr),\qquad
\lambda=\frac{\mu-1}{\mu+1},$$
located at $(0,0,-d)$. The force on $\vec m$ is exact (no factor-$\frac12$
subtlety for *forces*: differentiate the field of the *fixed* image):
$\vec F=\vec\nabla(\vec m\cdot\vec B^*)$, with $\vec B^*$ the image's dipole
field. Along the axis joining them ($\hat z$, separation $s=z+d$):
$$\vec m\cdot\vec B^*(z)=\frac{3(\vec m\cdot\hat z)(\vec m^*\cdot\hat z)-\vec m\cdot\vec m^*}{(z+d)^3}.$$
With $\vec m=m(\sin\theta\cos\phi,\sin\theta\sin\phi,\cos\theta)$:
$\vec m\cdot\vec m^*=\lambda m^2(\cos^2\theta-\sin^2\theta)$ and
$(\vec m\cdot\hat z)(\vec m^*\cdot\hat z)=\lambda m^2\cos^2\theta$, so the
numerator is $\lambda m^2(3\cos^2\theta-\cos^2\theta+\sin^2\theta)
=\lambda m^2(1+\cos^2\theta)$ — $\phi$ drops out (rotational symmetry about
the normal). Then
$$F_z=\partial_z\Bigl[\frac{\lambda m^2(1+\cos^2\theta)}{(z+d)^3}\Bigr]_{z=d}
=-\frac{3\lambda m^2(1+\cos^2\theta)}{(2d)^4}
=-\frac{3m^2(1+\cos^2\theta)}{16d^4}\,\frac{\mu-1}{\mu+1},$$
and the transverse components vanish on axis by symmetry (checked
numerically). For $\mu>1$, $F_z<0$: attraction — likes attract, and the
image co-circulates (P27). The pull is strongest for $\vec m\perp$ surface
($\theta=0$, factor 2) and weakest, but still attractive, for
$\vec m\parallel$ surface (factor 1); a magnet never hangs repelled above
iron, but does above a superconductor ($\mu\to0$: $F_z=+3m^2(1+\cos^2\theta)/16d^4$).

### P33.  Exercise 6.13.1 — Magnetization potential: volume + surface split  *(Wilcox 2e §6.15, pp.332–333)*
A small dipole $d\vec m$ at $\vec x'$ contributes
$d\vec A=\dfrac{d\vec m\times(\vec x-\vec x')}{|\vec x-\vec x'|^3}$. Show
that for a volume magnetization ($d\vec m=\vec M\,d^3x'$)
$$\vec A(\vec x)=\int_V d^3x'\,\frac{\vec\nabla'\times\vec M}{|\vec x-\vec x'|}
-\oint_S da'\,\frac{\hat n'\times\vec M}{|\vec x-\vec x'|},$$
the volume and surface pieces being the effective currents
$\vec J_{\rm eff}=c\vec\nabla\times\vec M$, $\vec K_{\rm eff}=c\vec M\times\hat n$
of (6.195)–(6.196).
*Answer:* as stated.
*Check:* the two sides agree for a smooth compactly supported $\vec M$
(surface term $\to0$; $10^{-5}$); for the uniformly magnetized sphere the
surface-only form equals the closed-form $A_\phi$, and its curl gives
$\frac{8\pi}{3}\vec M$ inside / the $m=\frac{4\pi a^3M_0}{3}$ dipole outside
(`test_p33_magnetization_potential_split`).

**Solution.** Superpose:
$$\vec A=\int_Vd^3x'\,\vec M(\vec x')\times\frac{\vec x-\vec x'}{|\vec x-\vec x'|^3}
=\int_Vd^3x'\,\vec M\times\vec\nabla'\frac{1}{|\vec x-\vec x'|},$$
since $\vec\nabla'(1/g)=+(\vec x-\vec x')/g^3$. Use the product rule
$\vec\nabla'\times\bigl(\vec M/g\bigr)
=\frac{1}{g}\vec\nabla'\times\vec M+\vec\nabla'(1/g)\times\vec M$, i.e.
$$\vec M\times\vec\nabla'\frac1g
=\frac{\vec\nabla'\times\vec M}{g}-\vec\nabla'\times\Bigl(\frac{\vec M}{g}\Bigr).$$
Integrate; the second term is a total curl, converted by the curl theorem
$\int_V\vec\nabla\times\vec F\,d^3x=\oint_S\hat n\times\vec F\,da$:
$$\vec A=\int_V\frac{\vec\nabla'\times\vec M}{g}\,d^3x'
-\oint_S\frac{\hat n'\times\vec M}{g}\,da'. \checkmark$$
Reading through (6.42): the first term is $\frac1c\int\vec J_{\rm eff}/g$
with $\vec J_{\rm eff}=c\vec\nabla\times\vec M$; the second is
$\frac1c\oint\vec K_{\rm eff}/g$ with
$\vec K_{\rm eff}=c\vec M\times\hat n=-c\,\hat n\times\vec M$ ✓ — the dipole
picture and the bound-current picture are the same object, split by one
integration by parts. The two numeric regimes probe each piece separately:
a smooth interior $\vec M$ (only the volume term) and the uniform sphere
(only the surface term, $\vec K_{\rm eff}=cM_0\sin\theta\,\hat e_\phi$,
whose field P13 already established).

### P34.  Exercise 6.13.2 — Split-sphere magnet (hemispheres magnetized $\pm\hat z$)  *(Wilcox 2e §6.15, pp.333–334)*
A sphere of radius $a$ is magnetized $+M_0\hat z$ in its upper half and
$-M_0\hat z$ in its lower half (Fig. 6.37).
(a) Using the scalar-potential expression (6.255), find $\vec B$ far away
($r\gg a$).
(b) Find $\Phi_m$ everywhere as a Legendre expansion (via the Coulomb
expansion (4.225) and the explicit Legendre values of Ex. 4.9.1), of the
form
$$\Phi_m(r,\theta)=4\pi M_0a^2\sum_{n\ge0}\frac{r_<^{2n}}{r_>^{2n+1}}\,C_n\,P_{2n}(\cos\theta),$$
finding $C_n$ and checking consistency with (a).
*Answer:* (a) leading far field is the pure $\ell=2$ (quadrupole) term
$$\Phi_m\simeq\frac{\pi M_0a^4}{r^3}P_2(\cos\theta),\qquad \vec H=\vec B=-\vec\nabla\Phi_m$$
(no monopole, no dipole — the configuration is even under $z\to-z$).
(b) $C_0=0$ and
$$C_n=(-1)^{n+1}\,\frac{2n\,(2n-3)!!}{(2n+2)!!}\qquad(n\ge1),\quad
C_1=\tfrac14,\ C_2=-\tfrac1{12},\dots$$
**Caveat (book form):** the sources are the outer-shell charge
$\sigma_m=\vec M\cdot\hat n=M_0|\cos\theta'|$ *plus the equatorial disk*
$\sigma_m=-2M_0$ (the jump of $M_z$ across $z=0$). The quoted
$r_<^{2n}/r_>^{2n+1}$ form with these $C_n$ is exact **outside** ($r\ge a$),
but its literal $r\le a$ branch is *not* the interior potential — the disk's
sources extend from $r'=0$ to $a$, so the interior is only piecewise of
power-law form. (E.g. $\Phi_m(0)=-2\pi M_0a\ne0$, while the book's form
gives 0.) The corrected interior expansion is given below.
*Check:* exterior series vs direct quadrature (shell $|\cos|$ + disk),
$10^{-8}$; $C_1=\frac14$, $C_2=-\frac1{12}$ exact; corrected interior form vs
quadrature ($2\times10^{-3}$, quadrature-limited); $\Phi_m(0)=-2\pi M_0a$;
far field $=$ the $P_2$ term (`test_p34_split_sphere`).

**Solution.** *Sources.* $\vec\nabla\cdot\vec M=0$ within each hemisphere,
but (6.255) needs *all* of $\vec M$'s divergence: across the equatorial
plane $M_z$ jumps from $-M_0$ to $+M_0$, a magnetic surface charge
$\sigma_m^{\rm disk}=-(M_z^+-M_z^-)=-2M_0$ on the disk $\rho'\le a$, $z'=0$;
on the outer shell $\sigma_m^{\rm shell}=\vec M\cdot\hat n=M_0|\cos\theta'|$
(positive at *both* poles). Total magnetic charge:
$2\pi a^2M_0-2M_0\pi a^2=0$ ✓.
(a) Multipoles: both sources are even in $\cos\theta'$ → only even $\ell$;
$\ell=0$ vanishes (zero net charge); the first survivor is $\ell=2$:
$$q_2=\underbrace{2\pi M_0a^4\int_{-1}^{1}P_2(x)|x|\,dx}_{\pi M_0a^4/2}
+\underbrace{P_2(0)(-2M_0)\,2\pi\!\int_0^a\rho'^3d\rho'}_{+\pi M_0a^4/2}
=\pi M_0a^4,$$
so $\Phi_m\simeq q_2P_2(\cos\theta)/r^3$ and
$\vec B=-\vec\nabla\Phi_m$: $B_r=3\pi M_0a^4P_2/r^4$,
$B_\theta=-\frac{\pi M_0a^4}{r^4}\partial_\theta P_2$ — a pure quadrupole
falloff $1/r^4$ (compare P15/P21: same multipole order, different source).
(b) *Exterior.* Expand each source with (4.225) ($r_>=r$, $r_<=r'$).
Shell: $\int_0^1xP_{2n}(x)dx=(-1)^{n+1}\frac{(2n-3)!!}{(2n+2)!!}$
(Ex. 4.9.1 values) gives the coefficient
$4\pi M_0a^2\,(-1)^{n+1}\frac{(2n-3)!!}{(2n+2)!!}\,\frac{a^{2n}}{r^{2n+1}}$.
Disk: with $P_{2n}(0)=(-1)^n\frac{(2n-1)!!}{(2n)!!}$,
$$\Phi^{\rm disk}_{2n}
=\frac{P_{2n}(\cos\theta)}{r^{2n+1}}\,P_{2n}(0)\,(-2M_0)\,\frac{2\pi a^{2n+2}}{2n+2}
=4\pi M_0a^2\,(-1)^{n+1}\frac{(2n-1)!!}{(2n+2)!!}\,\frac{a^{2n}}{r^{2n+1}}P_{2n}.$$
Sum: $(2n-3)!!+(2n-1)!!=(2n-3)!!\,[1+(2n-1)]=2n\,(2n-3)!!$, hence
$$C_n=(-1)^{n+1}\frac{2n\,(2n-3)!!}{(2n+2)!!},$$
zero at $n=0$ and $C_1=2\cdot1/4!!\cdot(-1)^2\cdot(-1)!!=2/8=\frac14$ —
matching (a): $4\pi M_0a^2C_1a^2/r^3=\pi M_0a^4/r^3$ ✓.
*Interior (corrected).* The shell is still a pure $r^{2n}$ series inside
(all its sources at $r'=a$), coefficient
$2\pi M_0a^2\,I_{2n}\,r^{2n}/a^{2n+1}$ with $I_0=1$,
$I_{2n}=C_n/n$ ($n\ge1$); but the disk potential at $r<a$ must be split at
$\rho'=r$:
$$\Phi^{\rm disk}_{2n}(r)=-4\pi M_0P_{2n}(0)\,g_{2n}(r)P_{2n}(\cos\theta),\qquad
g_\ell(r)=\frac{r}{\ell+2}+\frac{r}{\ell-1}\Bigl[1-\Bigl(\frac ra\Bigr)^{\ell-1}\Bigr]
\ (\ell\ge2),\ \ g_0=a-\frac r2 .$$
At the center only $n=0$ survives: $\Phi_m(0)=2\pi M_0a-4\pi M_0a=-2\pi M_0a$
(shell pulls up, the stronger disk pulls down) — the direct-quadrature check
confirms the corrected interior everywhere, and confirms that the book's
$r\leftrightarrow a$ swap of the exterior form does not reproduce it.

### P35.  Exercise 6.13.3 — Bar magnet as two magnetic monopoles  *(Wilcox 2e §6.15, pp.334–335)*
(a) A long straight rod of arbitrary uniform cross-section has constant
$\vec M=M_0\hat k$ and ends on a flat face $S$ (area $S$) in the $xy$-plane
(Fig. 6.38). Show that far from that end (origin anywhere near it)
$$\vec H(\vec x)\approx (M_0S)\,\frac{\vec x-\vec x''}{|\vec x-\vec x''|^3},$$
$\vec x''$ a representative point of $S$.
(b) For a thin circular bar (radius $R$, length $L\gg R$, $\vec M=M_0\hat k$),
find $\vec H$ valid far from both ends.
*Answer:* (a) the face acts as a point "magnetic charge" $q_m=M_0S$;
(b) $\vec H=M_0\pi R^2\Bigl[\dfrac{\vec x-\vec x_+}{|\vec x-\vec x_+|^3}
-\dfrac{\vec x-\vec x_-}{|\vec x-\vec x_-|^3}\Bigr]$, $\vec x_\pm$ the face
centers — the classic north/south monopole pair.
*Check:* exact two-charged-disk $\vec H$ vs the monopole pair: agreement
within the $O(R^2/s^2)$ finite-face residual (1%), with the residual
falling faster than $1/3$ per distance doubling; near-face single-pole
$1/s^2$ axis law exact (`test_p35_bar_magnet_monopoles`).

**Solution.** (a) In (6.255) the volume term dies
($\vec\nabla\cdot\vec M=0$ for uniform $\vec M$), leaving surface charges
$\sigma_m=\vec M\cdot\hat n$: zero on the sides ($\hat n\perp\hat k$),
$+M_0$ on the end face $S$, $-M_0$ on the far face. Near (but a few
face-diameters away from) the near end, the far face's contribution is
negligible, and
$$\Phi_m(\vec x)=M_0\int_S\frac{da'}{|\vec x-\vec x'|}
\;\xrightarrow[\;|\vec x-\vec x''|\gg\sqrt S\;]{}\;\frac{M_0S}{|\vec x-\vec x''|},$$
the monopole term of the face's multipole expansion about any interior
point $\vec x''$ (corrections are the face's dipole/quadrupole moments about
$\vec x''$, down by powers of $\sqrt S/|\vec x-\vec x''|$). Hence
$\vec H=-\vec\nabla\Phi_m=M_0S\,(\vec x-\vec x'')/|\vec x-\vec x''|^3$. ✓
This is how "magnetic poles" emerge from a pole-free theory: the end of a
uniformly magnetized rod carries an effective surface charge $M_0$ whose far
field is Coulombic in $\vec H$ (not in $\vec B$: inside the rod
$\vec B=\vec H+4\pi\vec M$ carries the return flux).
(b) Both ends visible: superpose $q_m=\pm M_0\pi R^2$ at
$\vec x_\pm=(0,0,\pm L/2)$:
$$\vec H(\vec x)=M_0\pi R^2\Bigl[\frac{\vec x-\vec x_+}{|\vec x-\vec x_+|^3}
-\frac{\vec x-\vec x_-}{|\vec x-\vec x_-|^3}\Bigr],$$
valid whenever the distance to each face $\gg R$. At $r\gg L$ this pair
merges into a dipole $m=q_mL=M_0\pi R^2L=M_0V$ ✓ (the total moment).

### P36.  Exercise 6.13.4 — $H_z=-M_0\,\Omega$; magnetized cube  *(Wilcox 2e §6.15, p.335)*
(a) A very long magnetized rod of arbitrary cross-section
($\vec M=M_0\hat k$, uniform) ends on a flat top face $S$ in the $xy$-plane
(Fig. 6.39). Show that both inside and outside the material
$$H_z(\vec x)=-M_0\,\Omega(\vec x),$$
$\Omega$ the solid angle subtended by $S$ at $\vec x$ (book convention
(6.67)–(6.69)).
(b) Apply (a) to find $H_z$ and $B_z$ at the center of a cube of side $b$
with uniform $\vec M=M_0\hat k$.
*Answer:* (a) as stated; (b) each face subtends $|\Omega|=2\pi/3$ from the
center, so $H_z=-\frac{4\pi M_0}{3}$ and
$B_z=H_z+4\pi M_0=+\frac{8\pi M_0}{3}$ — at its exact center a cube
demagnetizes like a sphere (factor $\frac{4\pi}{3}$, forced by the
three-axis symmetry $\sum_i N_i=4\pi$).
*Check:* $H_z$ from the arctan closed form of the square's solid angle vs
direct two-face charged-sheet quadrature at interior and exterior points
($10^{-6}$); center values exact to $10^{-8}$; the face solid angle
$2\pi/3$ from the closed form (`test_p36_cube_solid_angle`).

**Solution.** (a) As in P35, the only sources are $\sigma_m=+M_0$ on the top
face (the sides carry none; the bottom is at $-\infty$), so
$\Phi_m(\vec x)=M_0\int_S da'/|\vec x-\vec x'|$ and
$$H_z=-\partial_z\Phi_m=-M_0\,\partial_z\!\int_S\frac{da'}{|\vec x-\vec x'|}
=-M_0\,\Omega(\vec x)$$
by exactly the identity (6.69) that defined $\Omega$. Nothing in the step
distinguished inside from outside — the formula holds in both regions, with
$\Omega$ jumping from $-2\pi$ (just above the face) to $+2\pi$ (just below,
inside the material): $H_z$ jumps from $+2\pi M_0$ to $-2\pi M_0$ across the
charged sheet, while $B_z=H_z+4\pi M_0$ (inside) stays continuous ✓.
(b) The cube's two faces carry $\sigma_m=\pm M_0$ at $z=\pm b/2$;
superposing two copies of (a):
$$H_z(\vec x)=-M_0\bigl[\Omega_{\rm top}(\vec x)-\Omega_{\rm bot}(\vec x)\bigr].$$
From the center, each of the six faces subtends the same magnitude, and a
closed surface seen from inside subtends $4\pi$ total: $|\Omega|=4\pi/6=2\pi/3$
per face (the arctan closed form gives
$4\arctan\frac{1}{\sqrt3}=\frac{2\pi}{3}$ ✓). Signs: viewed from below,
$\Omega_{\rm top}=+2\pi/3$; from above, $\Omega_{\rm bot}=-2\pi/3$; so
$$H_z(0)=-M_0\Bigl(\frac{2\pi}{3}+\frac{2\pi}{3}\Bigr)=-\frac{4\pi M_0}{3},
\qquad B_z(0)=\frac{8\pi M_0}{3}.$$
The sphere gives the same $-\frac{4\pi}{3}\vec M$ *everywhere* inside
((6.263)); the cube only at special points — away from the center its
$H_z=-M_0[\Omega_t-\Omega_b]$ varies (the checked quadrature shows it).

### P37.  Exercise 6.13.5 — Rod magnet in Bessel form; solenoid harmonization  *(Wilcox 2e §6.15, pp.335–336)*
A rod magnet: uniform $\vec M=M_0\hat z$, circular cross-section of radius
$a$, length $d$, origin at the center.
(a) Via the magnetic scalar potential, show that for $-d/2<z<d/2$
$$H_\rho=4\pi M_0a\int_0^\infty dk\,J_1(ka)J_1(k\rho)\,e^{-kd/2}\sinh(kz),\qquad
H_z=-4\pi M_0a\int_0^\infty dk\,J_1(ka)J_0(k\rho)\,e^{-kd/2}\cosh(kz).$$
(b) Harmonize with the solenoid of Ex. 6.6.1 through
$\vec K_{\rm eff}=c\vec M\times\hat n$.
*Answer:* (a) as stated; (b) the rod is the solenoid with $nI=cM_0$:
$B_\rho^{\rm sol}=H_\rho^{\rm rod}$ and
$B_z^{\rm sol}=H_z^{\rm rod}+4\pi M_0H(a-\rho)$, i.e.
$\vec B=\vec H+4\pi\vec M$ holds integral-for-integral.
*Check:* Bessel forms vs the two-charged-disk quadrature ($2\times10^{-4}$);
the solenoid identification verified componentwise to $2\times10^{-6}$
including the step term (`test_p37_rod_magnet_bessel`).

**Solution.** (a) Sources: $\sigma_m=\pm M_0$ on the end disks at
$z=\pm d/2$ (sides clean, volume clean). The charged-disk potential in
Bessel form follows from the cylindrical Green expansion (6.70) and the disk
integral (6.72):
$$\int_{\rm disk}\frac{da'}{|\vec x-\vec x'|}
=2\pi a\int_0^\infty\frac{dk}{k}\,J_1(ka)J_0(k\rho)\,e^{-k|z-z_0|},$$
so
$$\Phi_m=2\pi M_0a\int_0^\infty\frac{dk}{k}J_1(ka)J_0(k\rho)
\bigl[e^{-k|z-d/2|}-e^{-k|z+d/2|}\bigr].$$
For $|z|<d/2$: $e^{-k(d/2-z)}-e^{-k(d/2+z)}=2e^{-kd/2}\sinh(kz)$, giving
$$\Phi_m=4\pi M_0a\int_0^\infty\frac{dk}{k}J_1(ka)J_0(k\rho)\,e^{-kd/2}\sinh(kz).$$
Then $H_\rho=-\partial_\rho\Phi_m$ with $\partial_\rho J_0(k\rho)=-kJ_1(k\rho)$
gives the first stated integral, and $H_z=-\partial_z\Phi_m$ the second. ✓
(b) On the curved side, $\vec K_{\rm eff}=c\vec M\times\hat\rho
=cM_0\,\hat e_\phi$: a solenoid sheet of strength $nI\leftrightarrow cM_0$.
Ex. 6.6.1's field with that substitution:
$$B_\rho=4\pi M_0a\!\int\!J_1J_1e^{-kd/2}\sinh(kz)\,dk=H_\rho\ \checkmark,\qquad
B_z=4\pi M_0H(a-\rho)-4\pi M_0a\!\int\!J_1J_0e^{-kd/2}\cosh(kz)\,dk
=4\pi M_z+H_z\ \checkmark$$
— the two computations are the same field seen through the two
decompositions: bound *currents* give $\vec B$ directly; magnetic *charges*
give $\vec H$; they differ inside the material by exactly $4\pi\vec M$
(6.199), here visible as the Weber–Schafheitlin step term.

### P38.  Exercise 6.13.6 — Closed shell magnetized along its normal  *(Wilcox 2e §6.15, p.336)*
An extremely thin closed hollow shell (uniform thickness) has constant
*area* magnetization $M_A$ ($M_A=M\,d$ for volume magnetization $M$ and
thickness $d$) directed everywhere along the outward normal $\hat n'$
(Fig. 6.40). Show
$$\Phi_m(\vec x)=\begin{cases}0 & \text{outside},\\ -4\pi M_A & \text{inside}.\end{cases}$$
(Alternative: argue $\vec B=0$ everywhere from the $\vec A$ field.)
*Answer:* as stated; consequently $\vec H=-\vec\nabla\Phi_m=0$ on both sides
and $\vec B=0$ everywhere ($\vec B=\vec H$ outside; inside the cavity
$\vec B=\vec H=0$; within the thin shell material
$\vec H=-4\pi\vec M$ normal to the wall, so $\vec B=\vec H+4\pi\vec M=0$
there too). The shell is magnetically invisible.
*Check:* $\Phi_m$ quadrature over a sphere and over a cube: $-4\pi M_A$
inside, $0$ outside, to $10^{-6}$
(`test_p38_closed_shell_normal_magnetization`).

**Solution.** *Route 1 (scalar potential).* In (6.254) replace
$\vec M\,d^3x'\to M_A\hat n'\,da'$:
$$\Phi_m(\vec x)=M_A\oint_S da'\,\hat n'\cdot\frac{\vec x-\vec x'}{|\vec x-\vec x'|^3}.$$
This is Gauss's-law geometry: the integrand is (minus) the closed-surface
solid-angle density, and for a *closed* surface with outward normals
$$\oint_S da'\,\hat n'\cdot\frac{\vec x-\vec x'}{|\vec x-\vec x'|^3}
=\begin{cases}0,&\vec x\ \text{outside}\\ -4\pi,&\vec x\ \text{inside}\end{cases}$$
(outside, the pierced cone contributions cancel in pairs; inside, the
surface wraps the observation point once; the sign follows the book's
(6.67) orientation — from inside, $\hat n'\cdot(\vec x-\vec x')<0$ over the
whole shell). Hence $\Phi_m=0$ outside, $-4\pi M_A$ inside — constant in
each region, so $\vec H=0$ in both. ✓ (Equivalently: the shell is a closed
*dipole layer*, across which $\Phi_m$ drops by $4\pi M_A$; a closed
constant-strength layer shifts the interior potential and nothing else.)
*Route 2 (vector potential).* $\vec M\parallel\hat n'$ makes
$\vec K_{\rm eff}=c\vec M\times\hat n'=0$ on both wall faces, and within the
thin wall $\vec\nabla\times\vec M$ integrates to zero across the thickness
for normal magnetization of a uniform shell (no net tangential circulation
— all the "dipole needles" stand on end, and side-by-side needles carry
counter-circulating molecular currents that cancel). With no effective
currents anywhere, $\vec A=0$ and $\vec B=\vec\nabla\times\vec A=0$
everywhere; then $\vec H=\vec B-4\pi\vec M$ is $0$ outside and in the
cavity, and $-4\pi M_A/d\cdot\hat n\cdot d$-worth across the wall —
integrating $-\vec H\cdot d\vec\ell$ through the wall reproduces the
$-4\pi M_A$ potential step. Both routes agree with the quadrature on the
sphere *and* the cube — the shape never entered.
