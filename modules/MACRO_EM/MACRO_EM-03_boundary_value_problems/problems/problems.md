# MACRO_EM-03 — Problems (Wilcox Ch. 3, all 33 exercises)

Every exercise of Wilcox & Thron 2e §3.13 (printed pp. 120–133), worked in
full. Statements are paraphrased (all given data kept); the book prints no
solutions — everything below is module-authored and machine-checked in
`code/bvp_greens.py` / `code/test_bvp_greens.py`. Sources in `../refs.md`.

**Conventions (the book's, Gaussian units).** Unit-charge potential
$G_f=1/|\vec x-\vec x'|$ (3.1); Green equation $\nabla^2G=-4\pi\delta$ (3.14);
Dirichlet representation (2.98)
$$\Phi(\vec x)=\int d^3x'\,\rho\,G_D-\frac1{4\pi}\oint da'\,\Phi\,\frac{\partial G_D}{\partial n'};$$
conductor surface charge $\sigma=\frac1{4\pi}\partial\Phi/\partial n$ (2.92);
2-D (line-charge) free Green function $G_f=-2\ln(\rho/L)$ (3.11). Reduced
Green functions are normalized by
$G=4\pi\int\!\frac{d^2k}{(2\pi)^2}e^{i\vec k\cdot(\vec x-\vec x')_\perp}g(k;z,z')$
(3.23/3.31). Griffiths-level background: `~EM-04`.

---

### P1.  Exercise 3.1.1 — Image ladder between parallel grounded plates  *(Wilcox 2e §3.13, p.120)*
A unit point charge sits at height $z'$ between two infinite grounded
conducting plates $z=0$ and $z=a$ (the book's Fig. 3.16). Locate and value
every image charge needed for the Dirichlet Green function, write $G_D$ as the
sum over them, and show the sum converges absolutely.
*Answer:* charges $+1$ at $z=2na+z'$ and $-1$ at $z=2na-z'$ for all
$n\in\mathbb Z$ (transverse position that of the source);
$$G_D=\sum_{n=-\infty}^{\infty}\left[\frac1{\sqrt{\rho^2+(z-2na-z')^2}}-\frac1{\sqrt{\rho^2+(z-2na+z')^2}}\right],\quad \rho=|(\vec x-\vec x')_\perp|,$$
and each bracketed pair is $O(1/n^2)$, so the grouped series converges
absolutely.
*Check:* `green_plates_images` vanishes on both plates and matches the
independent $k$-space form of P8 to $3\times10^{-7}$
(`test_p1_plate_images_boundary`, `test_p1_plate_images_absolute_convergence`,
`test_p1_vs_p8_kspace`).

**Solution.** Reflection in $z=0$ sends a charge $q$ at height $h$ to $-q$ at
$-h$; reflection in $z=a$ sends it to $-q$ at $2a-h$. Starting from $+1$ at
$z'$ and iterating the two reflections until the set closes generates
$$\{+1\ \text{at}\ 2na+z'\}\cup\{-1\ \text{at}\ 2na-z'\},\qquad n\in\mathbb Z$$
(only the $n=0$, $+$ member is the physical charge; all others lie outside the
gap). *Boundary check:* at $z=0$ the $+$ charge labelled $n$ and the $-$
charge labelled $-n$ are mirror partners through the plate, so their terms
cancel pairwise and $G_D|_{z=0}=0$ exactly; at $z=a$ the
partners are $(+,n)$ and $(-,1-n)$ — again pairwise cancellation. Uniqueness
(§2.7) then makes this *the* Green function.
*Absolute convergence:* group the two $n$-labelled terms. With
$f(s)=(\rho^2+s^2)^{-1/2}$, $s_\pm=z\mp z'-2na$, the mean value theorem gives
$$|f(s_+)-f(s_-)|=|f'(\bar s)|\,|s_+-s_-|=\frac{|\bar s|\,2z'}{(\rho^2+\bar s^2)^{3/2}}\le\frac{2z'}{(2|n|a-2a)^2}=O(n^{-2}),$$
so $\sum_n|{\rm pair}_n|$ converges by comparison with $\sum1/n^2$. (The
*ungrouped* $\pm1/r$ terms decay only like $1/n$ — the grouping is what makes
the convergence absolute.) Numerically the grouped tail is
$\sim zz'/(2N^2a^3)$: the test measures $n^2|{\rm pair}_n|\to$ const and the
$1/N^2$ approach of $G|_{z=a}\to0$ under symmetric truncation.

### P2.  Exercise 3.1.2 — Right-angle corner: Green function, extraction work, walls at ±V  *(Wilcox 2e §3.13, pp.120–121)*
Two grounded conducting half-planes meet at a right angle, bounding the
quadrant $x>0$, $y>0$ (translationally invariant along $z$; the book's
Fig. 3.17). A unit point charge sits at $(x',y',z')$ in the quadrant.
(a) Build $G_D(\vec x,\vec x')$ in Cartesian coordinates by images.
(b) Find the work $W$ to remove the charge to infinity.
(c) Using $G_D$, find $\Phi$ when the vertical wall ($x=0$) is held at $-V$
and the horizontal wall ($y=0$) at $+V$.
*Answer:* (a) three images: $-1$ at $(-x',y',z')$, $+1$ at $(-x',-y',z')$,
$-1$ at $(x',-y',z')$;
(b) $W=\tfrac14\left(1/x'+1/y'-1/\sqrt{x'^2+y'^2}\right)$;
(c) $\Phi=V\left(1-\tfrac{4\phi}{\pi}\right)$, $\phi=\arctan(y/x)$ — the
$\beta=\pi/2$ case of the book's Eq. (3.152).
*Check:* `green_corner` vanishes on both walls; `corner_work` equals the
numerically integrated $-\int\vec F\cdot d\vec l$; `corner_wall_phi_quad`
(Green-function surface quadrature) matches $V(1-4\phi/\pi)$ to $2\times10^{-4}$
(`test_p2_corner_green`, `test_p2_corner_work`, `test_p2_corner_wall_potential`).

**Solution.** (a) Reflection in $x=0$ and in $y=0$ closes after the double
reflection (the group is $\mathbb Z_2\times\mathbb Z_2$):
$$G_D=\frac1{|\vec x-\vec x'_{++}|}-\frac1{|\vec x-\vec x'_{-+}|}+\frac1{|\vec x-\vec x'_{--}|}-\frac1{|\vec x-\vec x'_{+-}|},$$
with $\vec x'_{\pm\pm}=(\pm x',\pm y',z')$. On $x=0$ the $++/-+$ and $--/+-$
terms cancel in pairs; on $y=0$ the $++/+-$ and $-+/--$ pairs cancel. Both
walls at zero, correct $-4\pi\delta$ source, $G\to0$ at infinity: uniqueness
does the rest.
(b) The energy of the charge in the presence of the *conductor* is **half**
the naive charge–image Coulomb sum, $U=\tfrac12 q\,\Phi_{\rm ind}(\vec x')$
— the factor $\tfrac12$ because the induced charge builds up proportionally
as the source is brought in (equivalently: images move when the charge moves,
so $\int\vec F\cdot d\vec l$ picks up half). The image distances are $2x'$,
$2y'$, $2\sqrt{x'^2+y'^2}$, so
$$U=\frac12\left[-\frac1{2x'}-\frac1{2y'}+\frac1{2\sqrt{x'^2+y'^2}}\right],\qquad
W=-U=\frac14\left(\frac1{x'}+\frac1{y'}-\frac1{\sqrt{x'^2+y'^2}}\right)>0.$$
The test verifies the factor of $\tfrac12$ the honest way: it integrates the
*full* image force along a radial escape path and reproduces exactly this $W$.
(c) With no volume charge, (2.98) leaves the wall term
$\Phi=-\frac1{4\pi}\oint\Phi_s\,\partial G_D/\partial n'\,da'$. Because the
geometry is a wedge, the answer must be the bounded harmonic function of the
polar angle alone that interpolates the two wall values: $\nabla^2\phi=0$, so
$\Phi=A+B\phi$ with $\Phi(\phi{=}0)=V$, $\Phi(\phi{=}\pi/2)=-V$ gives
$$\Phi=V\left(1-\frac{4\phi}{\pi}\right).$$
The quadrature route confirms it: reduce the two wall integrals with the 2-D
corner Green function of P3 (the $z'$ integration is already absorbed), i.e.
$\Phi=-\frac1{4\pi}\sum_{\rm walls}\int_0^\infty d\rho'\,\Phi_{\rm wall}\,
(\pm\tfrac1{\rho'})\partial_{\phi'}G$, with
$\partial_{\phi'}G|_{\phi'=0}=8\rho^2\rho'^2\sin2\phi/(\rho^4+\rho'^4-2\rho^2\rho'^2\cos2\phi)$
and its $\phi'=\pi/2$ mirror — the code does exactly this integral.

### P3.  Exercise 3.1.3 — Line charge in a right-angle corner (2-D Green function)  *(Wilcox 2e §3.13, p.121)*
An infinite unit line charge runs parallel to the intersection line of two
perpendicular grounded conducting planes, at cylindrical position
$(\rho',\phi')$ in the quadrant (the book's Fig. 3.18). Construct $G_D$ by
images and show it can be written
$$G_D(\vec x,\vec x')=\ln\!\left[\frac{\rho^4+\rho'^4-2\rho^2\rho'^2\cos(2(\phi+\phi'))}{\rho^4+\rho'^4-2\rho^2\rho'^2\cos(2(\phi-\phi'))}\right].$$
*Answer:* four image lines with alternating sign (as in P2 but 2-D); the log
ratio above is exactly that image sum.
*Check:* closed form $=$ image sum ($-2\sum q\ln d$) on random points; zero on
both walls (`test_p3_perp_planes`).

**Solution.** In 2-D each line charge contributes $-2\ln d$ (Eq. 3.11; the
$1/L$ scale cancels in the alternating sum). With the same $\mathbb Z_2\times\mathbb Z_2$
image set as P2,
$$G_D=-2\ln\frac{d_{++}\,d_{--}}{d_{-+}\,d_{+-}},$$
where $d_{\pm\pm}$ is the transverse distance from $\vec x_\perp$ to
$(\pm x',\pm y')$. Now use complex notation $w=\rho e^{i\phi}$,
$w'=\rho'e^{i\phi'}$: the four image positions are $w',-w',\bar w',-\bar w'$
and
$$d_{++}d_{--}=|w-w'||w+w'|=|w^2-w'^2|,\qquad
d_{-+}d_{+-}=|w-(-\bar w')||w-\bar w'|=|w^2-\bar w'^2|.$$
Squaring, $|w^2-w'^2|^2=\rho^4+\rho'^4-2\rho^2\rho'^2\cos2(\phi-\phi')$ and
$|w^2-\bar w'^2|^2=\rho^4+\rho'^4-2\rho^2\rho'^2\cos2(\phi+\phi')$, so
$$G_D=-2\ln\frac{|w^2-w'^2|}{|w^2-\bar w'^2|}
=\ln\frac{\rho^4+\rho'^4-2\rho^2\rho'^2\cos2(\phi+\phi')}{\rho^4+\rho'^4-2\rho^2\rho'^2\cos2(\phi-\phi')}.$$
On $\phi=0$ ($w$ real) and on $\phi=\pi/2$ ($w$ imaginary, $w^2$ real) the
numerator and denominator coincide, so $G_D=0$ — the walls are grounded.
(The $w\mapsto w^2$ structure is the conformal unfolding of the quadrant into
a half-plane; compare P32/P33 and `~MA-06`.)

### P4.  Exercise 3.1.4 — Charged pendulum over a grounded plane  *(Wilcox 2e §3.13, pp.121–122)*
A particle of charge $e$ (mass $m$) hangs from a massless string of length $L$
whose anchor sits a distance $D>L$ above an infinite grounded conducting plane
(gravity-free; the book's Fig. 3.19). Using the image potential energy
expanded to lowest order in the swing angle $\theta$, find the small-oscillation
frequency.
*Answer:* $\displaystyle\omega=\frac{e}{2(D-L)\sqrt{mL}}$.
*Check:* numeric $U''(0)$ of the exact image energy equals
$e^2L/4(D-L)^2$, and `pendulum_omega` $=\sqrt{U''(0)/mL^2}$
(`test_p4_pendulum`).

**Solution.** At swing angle $\theta$ the charge sits a height
$h(\theta)=D-L\cos\theta$ above the plane. The conductor interaction energy is
half the charge–image Coulomb energy (image $-e$ at depth $h$, separation
$2h$; same $\tfrac12$ as P2b):
$$U(\theta)=\frac12\cdot\frac{(-e^2)}{2h}=-\frac{e^2}{4\,(D-L\cos\theta)}.$$
Expand with $\cos\theta\simeq1-\theta^2/2$:
$h\simeq(D-L)+L\theta^2/2$, so
$$U\simeq-\frac{e^2}{4(D-L)}\left[1-\frac{L\theta^2}{2(D-L)}\right]
=U_0+\frac{e^2L}{8(D-L)^2}\,\theta^2 .$$
The string constrains the motion to a circle, so the generalized coordinate is
$\theta$ with inertia $I=mL^2$, and the quadratic term gives the torque
constant $k_\theta=U''(0)=e^2L/4(D-L)^2$. Hence
$$\omega=\sqrt{\frac{k_\theta}{I}}=\sqrt{\frac{e^2}{4mL(D-L)^2}}
=\frac{e}{2(D-L)\sqrt{mL}}.$$
(Because gravity is absent, the *only* restoring force is the image
attraction: the equilibrium is the string hanging straight down toward the
plane, where $h$ is minimal and $U$ lowest.) The code takes the exact
$U(\theta)$, differentiates numerically, and recovers both $k_\theta$ and
$\omega$.

### P5.  Exercise 3.1.5 — Patch at potential V: the solid-angle formula  *(Wilcox 2e §3.13, p.122)*
On the plane $z=0$ an arbitrary patch is held at constant potential $V$; the
remainder of the plane is at $V=0$ (the book's Fig. 3.20). Using the Dirichlet
Green function of the half-space, show
$$\Phi(\vec x)=\frac{V}{2\pi}\,|\Omega(\vec x)|,$$
$\Omega(\vec x)$ the solid angle the patch subtends at $\vec x$ (either side of
the plane).
*Answer:* as stated; e.g. on a disk's axis
$|\Omega|=2\pi\bigl(1-|z|/\sqrt{z^2+R^2}\bigr)$.
*Check:* patch quadrature of $\int z\,da'/r^3$ equals the disk and rectangle
closed forms on both sides of the plane; under the patch
$\Phi\to V$ (`test_p5_solid_angle`).

**Solution.** For $z>0$ the half-space Green function is (3.36), and its
inward-normal derivative on the plane is (3.37) with field/source roles
exchanged (use symmetry $G_D(\vec x,\vec x')=G_D(\vec x',\vec x)$):
$$\frac{\partial G_D}{\partial n'}\Big|_{z'=0}=-\frac{\partial G_D}{\partial z'}\Big|_{z'=0}
=-\frac{2z}{\left[(x-x')^2+(y-y')^2+z^2\right]^{3/2}}.$$
With no volume charge, (2.98) gives
$$\Phi(\vec x)=-\frac1{4\pi}\oint\Phi(\vec x')\frac{\partial G_D}{\partial n'}da'
=\frac{V}{2\pi}\int_{\rm patch}\frac{z\,da'}{|\vec x-\vec x'|^3},$$
the integrand being nonzero only on the patch. Now recognize the geometry:
$z\,da'/r^3=(\hat r\cdot\hat z)\,da'/r^2=d\Omega$ is precisely the projection
of the patch element onto the unit sphere around $\vec x$ — the solid-angle
element. Hence $\Phi=(V/2\pi)\,\Omega(\vec x)$ for $z>0$. For $z<0$ run the
identical argument with the lower half-space Green function (normal $+\hat z$):
the sign of $z$ flips twice, leaving $\Phi=(V/2\pi)|\Omega|$ on both sides.
Sanity limits: point just above the patch interior, $\Omega\to2\pi$, so
$\Phi\to V$ (continuity with the boundary data); far away $\Omega\to({\rm
area})\,z/r^3$, a dipole-sheet falloff. The code checks the disk axis value
$2\pi(1-z/\sqrt{z^2+R^2})$, the rectangle closed form
$4\arctan\!\bigl[w_xw_y/(z\sqrt{w_x^2+w_y^2+z^2})\bigr]$, and the
$\Phi\to V$ limit.

### P6.  Exercise 3.2.1 — The free Green function integral, regulated  *(Wilcox 2e §3.13, p.122)*
Evaluate the angular/radial Fourier representation of the free Green function,
Eq. (3.19),
$$G_f(\vec x,\vec x')=\frac1\pi\int_0^\infty dk\int_{-1}^{1}d\cos\theta\,
e^{ik|\vec x-\vec x'|\cos\theta},$$
by (i) inserting a convergence factor $e^{-k\epsilon}$, (ii) doing the $k$
integral first, and (iii) letting $\epsilon\to0^+$.
*Answer:* $G_f=1/R$ with $R=|\vec x-\vec x'|$; at finite $\epsilon$ the
regulated integral is $\frac{2}{\pi R}\arctan(R/\epsilon)$.
*Check:* $\mu$-quadrature of the $k$-first result matches
$\frac2{\pi R}\arctan(R/\epsilon)$ to $10^{-10}$ and tends to $1/R$
(`test_p6_convergence_factor`).

**Solution.** With $\mu=\cos\theta$ and the regulator in place, the $k$
integral is elementary because $\mathrm{Re}(\epsilon-iR\mu)>0$:
$$\int_0^\infty dk\,e^{k(iR\mu-\epsilon)}=\frac1{\epsilon-iR\mu}.$$
Then
$$G_f^{(\epsilon)}=\frac1\pi\int_{-1}^{1}\frac{d\mu}{\epsilon-iR\mu}
=\frac1\pi\int_{-1}^{1}\frac{\epsilon+iR\mu}{\epsilon^2+R^2\mu^2}\,d\mu
=\frac1\pi\int_{-1}^{1}\frac{\epsilon\,d\mu}{\epsilon^2+R^2\mu^2},$$
the imaginary part vanishing by oddness in $\mu$ (as it must — $G$ is real).
The remaining integral is an arctangent:
$$G_f^{(\epsilon)}=\frac{1}{\pi}\cdot\frac{2}{R}\arctan\frac{R\mu}{\epsilon}\Big|_{\mu=0}^{1}\cdot\frac{\epsilon}{\epsilon}\Big.^{\!\!}
=\frac{2}{\pi R}\arctan\frac{R}{\epsilon}
\;\xrightarrow[\epsilon\to0^+]{}\;\frac{2}{\pi R}\cdot\frac\pi2=\frac1R .$$
This is the $\epsilon$-regularized route to (3.1); the book's in-text
derivation (3.20)–(3.21) instead does the $\mu$ integral first and uses
$\int_0^\infty\sin x/x\,dx=\pi/2$ — the regulator makes the interchange of
integration order legitimate (dominated convergence), which is the point of
the exercise.

### P7.  Exercise 3.2.2 — Neumann Green function of the half-space; the surface delta  *(Wilcox 2e §3.13, pp.122–123)*
For the half-space $z>0$ (the book's Fig. 3.21):
(a) obtain the Neumann Green function by the reduced-Green-function method
(an integral representation suffices);
(b) confirm the surface delta function in
$\partial G_N(\vec x,\vec x')/\partial n\,|$ as asserted by Eq. (2.115).
*Answer:* (a) $g_N(k;z,z')=\frac1{2k}\bigl(e^{-k|z-z'|}+e^{-k(z+z')}\bigr)$,
whose inversion is the image form (3.5), $G_N=1/|\vec x-\vec x'|+1/|\vec x-\vec x''|$;
(b) with the source moved onto the plane, $G_N=2/|\vec x-\vec x'_S|$ and
$\frac1{4\pi}\partial G_N/\partial n\to\delta^{(S)}(\vec x_\perp-\vec x'_\perp)$
as $z\to0^+$ (the $-4\pi/S$ of (2.106) vanishes for the infinite plane).
*Check:* $k$-integral $=$ image form to $10^{-8}$; wall-normal derivative
vanishes; the family $\frac1{4\pi}\,2z/(\rho^2+z^2)^{3/2}$ integrates to $1$
for every $z$ and concentrates as $z\to0^+$
(`test_p7_neumann_halfspace`, `test_p7_surface_delta`).

**Solution.** (a) Transverse Fourier transform of $\nabla^2G_N=-4\pi\delta$
gives the reduced equation (3.22), $\left(k^2-\partial_z^2\right)g=\delta(z-z')$,
now with the *Neumann* wall condition $\partial_z g|_{z=0}=0$ and boundedness
as $z\to\infty$. For $z\ne z'$ the solutions are $e^{\pm kz}$; boundedness
picks $C_1e^{-kz}$ above the source, and the wall condition picks the *even*
combination $C_2\cosh kz$ below it. Continuity at $z'$ and the jump
$-\partial_zg\,|^{z'^+}_{z'^-}=1$ (integrate the ODE across the source) give
$C_1=\cosh(kz')/k\,e^{-kz'}\cdot$… solving the $2\times2$ system,
$$g_N=\frac1{2k}\left(e^{-k|z-z'|}+e^{-k(z+z')}\right),$$
which is the Dirichlet result (3.30) with the image sign flipped. Fourier
inversion term by term is the same $I_1$ integral as (3.32)–(3.34), giving
$G_N=1/|\vec x-\vec x'|+1/|\vec x-\vec x''|$, $\vec x''=(x',y',-z')$: the
image method result (3.5), recovered from the ODE side.
(b) Equation (2.115) instructs: *first* put the source on the boundary, *then*
evaluate the normal field as the field point approaches it. With $z'=0$ the
charge and its image coincide, $G_N=2/\sqrt{\rho^2+z^2}$, and with the outward
normal $\hat n=-\hat z$,
$$\frac1{4\pi}\frac{\partial G_N}{\partial n}
=-\frac1{4\pi}\frac{\partial}{\partial z}\frac{2}{\sqrt{\rho^2+z^2}}
=\frac1{4\pi}\frac{2z}{(\rho^2+z^2)^{3/2}}
\;\xrightarrow[z\to0^+]{}\;\delta^{(S)}(\vec x_\perp-\vec x'_\perp),$$
by the delta-family identity (3.38) (the book's Ex. 2.2.2b): the expression
integrates to exactly $1$ over the plane for *every* $z>0$ (the code shows
this analytically-sharp normalization numerically) while its support shrinks
like $z$. Since the plane has infinite area, the $-4\pi/S$ constant of (2.106)
is zero here, so (2.115) reads pure surface delta — confirmed.

### P8.  Exercise 3.2.3 — Parallel plates: reduced Green function, induced charges, capacitance  *(Wilcox 2e §3.13, p.123)*
For the two grounded plates of P1:
(a) show
$$G_D(\vec x,\vec x')=4\pi\!\int\!\frac{d^2k}{(2\pi)^2}\,e^{i\vec k\cdot(\vec x-\vec x')_\perp}\,g(k;z,z'),\qquad
g=\frac{\sinh(kz_<)\,\sinh[k(a-z_>)]}{k\,\sinh(ka)},$$
with $z_<$ ($z_>$) the lesser (greater) of $z,z'$;
(b) use it to show the plate charges induced by a unit charge at height $z'$
are $Q|_{z=0}=-(1-z'/a)$ and $Q|_{z=a}=-z'/a$ (also obtainable from the
reciprocation theorem, the book's Ex. 2.7.2);
(c) combine with Chapter 2's capacitance definition to get $C=A/(4\pi a)$ for
plate area $A$.
*Answer:* as stated; the two induced charges sum to $-1$.
*Check:* $k$-integral $=$ P1 image sum; radial quadrature of
$\sigma=\frac1{4\pi}\partial G/\partial n$ over each plate returns
$-(1-z'/a)$ and $-z'/a$ (sum $-1$); the wall integral gives
$\Phi=V(1-z/a)$, hence $C=A/4\pi a$
(`test_p1_vs_p8_kspace`, `test_p8_induced_charges`, `test_p8_capacitance`).

**Solution.** (a) As in §3.2, transverse translation invariance reduces (3.14)
to $\left(k^2-\partial_z^2\right)g=\delta(z-z')$ with $g=0$ at *both* $z=0$
and $z=a$. Build $g$ from homogeneous solutions vanishing at the near wall:
$g=A\sinh(kz)$ for $z<z'$ and $g=B\sinh[k(a-z)]$ for $z>z'$. Continuity at
$z=z'$ and the unit jump $-\partial_zg|^{+}_{-}=1$ give
$A\sinh(kz')=B\sinh[k(a-z')]$ and $kB\cosh[k(a-z')]+kA\cosh(kz')=1$; solving,
$A=\sinh[k(a-z')]/(k\sinh ka)$, $B=\sinh(kz')/(k\sinh ka)$ — i.e. the quoted
$z_<,z_>$ form (its $a\to\infty$ limit is (3.30), and the code checks it
against P1's image ladder — two independent constructions of the same $G$).
(b) The total charge on the bottom plate is
$Q|_{z=0}=\oint\sigma\,da=-\frac1{4\pi}\oint\partial_zG|_{z=0}\,da$ (outward
normal $-\hat z$). The area integral of $e^{i\vec k\cdot(\vec x-\vec x')_\perp}$
produces $(2\pi)^2\delta^2(\vec k)$, so only the $k\to0$ limit of $g$
survives:
$$g(k\to0;z,z')=\frac{z_<\,(a-z_>)}{a}.$$
For the bottom plate ($z\to0$, so $z=z_<$): $\partial_z g|_{z=0}=(a-z')/a$,
giving $Q|_{z=0}=-(1-z'/a)$; for the top ($z=z_>$):
$\partial_z g|_{z=a}=-z'/a$ with normal $+\hat z$, giving $Q|_{z=a}=-z'/a$.
They sum to $-1$: every field line from the unit charge ends on a plate, and
the *shares* are the linear interpolation weights of the source height — the
Green-reciprocity statement (weight $=$ the linear potential each plate would
create at $z'$), which is the Ex. 2.7.2 route the book mentions.
(c) Hold the bottom plate at $V$, top at $0$, no interior charge. By (b) plus
symmetry of $G_D$, the surface integral of (2.98) evaluates to
$\Phi(z)=V\,[-Q|_{z=0}(z'{=}z)]=V(1-z/a)$ — verified by quadrature in the
code — i.e. the uniform field $E=V/a$. Then $\sigma=\frac1{4\pi}E=V/4\pi a$
uniformly, and restricting to area $A$ (the book's hint): $Q=\sigma A=AV/4\pi a$,
so
$$C=\frac{Q}{V}=\frac{A}{4\pi a},$$
the Gaussian parallel-plate capacitance.

### P9.  Exercise 3.2.4 — Robin boundary conditions on the half-space  *(Wilcox 2e §3.13, p.124)*
Robin conditions blend Dirichlet and Neumann:
$\bigl(G_R+h\,\partial G_R/\partial n\bigr)\big|_S=0$ with $h\neq0$ a constant
and $n$ the outward normal. Starting from
$G_R=4\pi\int\frac{d^2k}{(2\pi)^2}e^{i\vec k\cdot(\vec x-\vec x')_\perp}g(k;z,z')$,
solve for the reduced Green function in $z>0$ (source at $z'>0$) with Robin
conditions on $z=0$.
*Answer:* $\displaystyle g_R=\frac1{2k}\left[e^{-k|z-z'|}+\beta(k)\,e^{-k(z+z')}\right],
\qquad\beta(k)=\frac{hk-1}{hk+1},$
interpolating Dirichlet ($h\to0$, $\beta=-1$) and Neumann ($h\to\infty$,
$\beta=+1$).
*Check:* closed form matches a finite-difference solve of the Robin BVP to
$3\times10^{-3}$; satisfies $g(0)=h\,g'(0)$; reproduces the D/N limits
(`test_p9_robin`).

**Solution.** The reduced equation is again $\left(k^2-\partial_z^2\right)g=\delta(z-z')$,
bounded as $z\to\infty$. The outward normal of the region $z>0$ is
$\hat n=-\hat z$, so $\partial G/\partial n=-\partial G/\partial z$ and the
Robin condition $\left(g+h\,\partial g/\partial n\right)|_{z=0}=0$ becomes
$$g(0)=h\,g'(0).$$
Make the ansatz
$$g=\frac1{2k}\left[e^{-k|z-z'|}+\beta\,e^{-k(z+z')}\right],$$
which already solves the ODE with the correct unit jump (the first term is
the free 1-D Green function; the second is a source-free homogeneous solution
decaying at $\infty$). At the wall,
$$g(0)=\frac{(1+\beta)e^{-kz'}}{2k},\qquad
g'(0)=\frac{(1-\beta)e^{-kz'}}{2},$$
so $g(0)=h\,g'(0)$ forces $(1+\beta)=hk\,(1-\beta)$, i.e.
$$\beta(k)=\frac{hk-1}{hk+1}.$$
Unlike the pure D/N cases, the "image strength" is now $k$-dependent: in real
space the image is a point charge *plus* a continuum tail (an image line
charge extending below the plane) — the price of the mixed condition. The
code solves the BVP independently on a grid with the Robin row
$g_0-h(g_1-g_0)/\Delta z=0$ and confirms the closed form, plus both limits.

### P10.  Exercise 3.3.1 — Charge inside a grounded / neutral spherical shell  *(Wilcox 2e §3.13, p.124)*
(a) A unit point charge sits *inside* a hollow grounded conducting shell of
radius $a$. Find the Dirichlet Green function by images and the potential both
inside and outside.
(b) The same shell, but thin, **neutral** and isolated, with charge $q$ inside.
Find $\Phi$ everywhere.
(c) Can an outside observer locate the interior charge from the exterior
field? Generalize to a neutral hollow conductor of arbitrary shape.
*Answer:* (a) inside, Eq. (3.48) with $r'<a$ (image $-a/r'$ at $a^2/r'^2\,\vec r\,'$);
outside, $\Phi=0$. (b) inside $\Phi=q\,G_D+q/a$; outside $\Phi=q/r$.
(c) No: the exterior field is exactly central Coulomb, wherever the charge
sits; for an arbitrary neutral hollow conductor the exterior field depends
only on the outer-surface geometry and the total charge — never on the
interior arrangement.
*Check:* $G_D=0$ on $r=a$; total induced charge $=-1$; neutral-shell $\Phi$
continuous at $r=a$ and exterior $1/r$ unchanged when the interior charge
moves (`test_p10_sphere_green`, `test_p10_neutral_shell`).

**Solution.** (a) The image algebra of §3.3 never used $r'>a$: demanding
$\Phi(a\hat n)=0$ for a charge $q$ at $\vec r\,'$ and an image $q'$ at
$\vec r\,''\parallel\vec r\,'$ again factors as (3.45), giving
$$q'=-\frac{a}{r'}q,\qquad r''=\frac{a^2}{r'},$$
now with $r'<a$ so the image lies *outside* — outside the physical region, as
an image must. So the interior Green function is exactly (3.48). For the
grounded shell the exterior is a charge-free region bounded by an
equipotential at zero and vanishing at infinity, so $\Phi_{\rm out}\equiv0$
(uniqueness): the ground wire supplies a net $-1$; integrating
$\sigma=\frac1{4\pi}\partial G/\partial n$ over the inner surface indeed gives
$-1$ (test).
(b) Cut the wire and demand neutrality: the inner surface must still carry
$-q$ (Gauss on a surface inside the metal), so the outer surface carries $+q$.
The outer problem — conductor surface $r=a$, total charge $q$, nothing
outside — has the uniformly distributed solution $\Phi_{\rm out}=q/r$,
*regardless of where $q$ sits inside*: the metal screens the interior
asymmetry (the inner-surface density is nonuniform, the outer is exactly
uniform). Inside, the grounded solution $qG_D$ vanishes at $r=a$, while the
true shell potential is $\Phi(a)=q/a$; adding a constant (harmonic, no new
sources) fixes it:
$$\Phi_{\rm in}=q\,G_D(\vec r,\vec r\,')+\frac qa .$$
Continuity at $r=a$ is then automatic (test).
(c) From outside one sees $q/r$ exactly — no information about $\vec r\,'$.
Generally: for a neutral hollow conductor of any shape, the interior problem
(cavity walls + enclosed charge) and the exterior problem decouple; the outer
surface charge arranges itself as the solution of "isolated conductor of this
shape carrying total charge $q$", which is unique and independent of the
cavity contents. Exterior measurements determine only $q$ and the conductor's
shape — the position of the enclosed charge is unobservable. (This is
electrostatic shielding run in reverse; compare `~EM-04`'s Faraday-cage
discussion.)

### P11.  Exercise 3.3.2 — Grounded plane with a hemispherical boss  *(Wilcox 2e §3.13, pp.124–125)*
A grounded conducting hemisphere of radius $a$ sits on top of a grounded
infinite plane $z=0$ (the book's Fig. 3.22).
(a) Find the Dirichlet Green function for the region above plane and boss by
images. (b) Find the Green function for the vacuum inside the hemispherical
dome (this needs Exercise 3.3.1a).
*Answer:* both regions use the same four charges: unit source at $\vec r\,'$;
sphere image $-a/r'$ at $(a^2/r'^2)\vec r\,'$; plane image $-1$ at the mirror
point $\vec r\,'_m$; and $+a/r'$ at $(a^2/r'^2)\vec r\,'_m$ (the sphere image
of the plane image).
*Check:* the four-charge $G$ vanishes on the plane (outside the boss) and on
the hemisphere, for sources outside the boss and inside the dome
(`test_p11_hemisphere_boss`).

**Solution.** Two mirror operations are in play: inversion in the sphere
($q\mapsto-\frac{a}{r}q$ at $a^2\vec r/r^2$) and reflection in the plane
($q\mapsto-q$ at $\vec r_m$, $z\to-z$). Because $\vec r\,'_m$ has the same
radius $r'$ and mirrored polar angle, the two operations *commute* on this
configuration, and the group closes with four members:
$$G_D=\frac1{|\vec r-\vec r\,'|}
-\frac{a/r'}{\bigl|\vec r-\frac{a^2}{r'^2}\vec r\,'\bigr|}
-\frac1{|\vec r-\vec r\,'_m|}
+\frac{a/r'}{\bigl|\vec r-\frac{a^2}{r'^2}\vec r\,'_m\bigr|}.$$
On the *sphere* $r=a$: the 1st+2nd terms cancel (that is the grounded-sphere
identity for $\vec r\,'$) and the 3rd+4th cancel (same identity for
$\vec r\,'_m$, whose radius is also $r'$). On the *plane*: the 1st+3rd cancel
(mirror pair) and the 2nd+4th cancel (their positions are mirror images with
equal strengths $a/r'$). All four boundary pieces at zero, one physical
singularity in the region: uniqueness certifies $G_D$.
(a) For a source above the plane and outside the boss, all three images lie
either below the plane or inside the sphere — outside the physical region ✓.
(b) For a source *inside the dome* ($r'<a$, $z'>0$) the same formula works:
the sphere image now sits outside the sphere (P10a), its mirror below the
plane, and the plane mirror below the plane — again all images outside the
dome region. The code checks both cases on random boundary points. (The
region below the plane is field-free in both problems; the images are
fictions valid only in the vacuum region, as in `~EM-04`.)

### P12.  Exercise 3.3.3 — The image charge *density* for a sphere  *(Wilcox 2e §3.13, p.125)*
An arbitrary charge density $\rho(\vec x)$ lies outside a grounded conducting
sphere of radius $a$. Show that the exterior field is that of $\rho$ plus an
image density $\rho^*$ inside the sphere, related in spherical coordinates
about the center by
$$\rho^*(r,\theta,\phi)=-\Bigl(\frac ar\Bigr)^{5}\rho\Bigl(\frac{a^2}{r},\theta,\phi\Bigr)
\quad\Longleftrightarrow\quad
\rho^*\Bigl(\frac{a^2}{r},\theta,\phi\Bigr)=-\Bigl(\frac ra\Bigr)^{5}\rho(r,\theta,\phi),$$
the combination satisfying $\vec E\times\hat n|_{r=a}=0$. Then (b) check the
point-charge limit reproduces the standard image charge and location.
*Answer:* as stated — the per-element image rule $dq^*=-(a/r')\,dq$ at
$a^2/r'$, converted to a density by the inversion Jacobian $(a/r')^6$.
*Check:* $\int\rho^*d^3x$ by quadrature equals $-\int(a/r)\rho\,d^3x$ for a
smooth blob (Jacobian identity), and a random point-charge cloud plus its
image cloud zeroes $\Phi$ on the sphere (`test_p12_rho_star`).

**Solution.** Superpose the point-image rule (3.46) over the elements of
$\rho$: the element $dq=\rho(\vec x')\,d^3x'$ at radius $r'$ acquires an image
$$dq^*=-\frac{a}{r'}\,dq\qquad\text{at}\qquad \vec x''=\frac{a^2}{r'^2}\vec x'.$$
The image element occupies the inverted volume: with $r''=a^2/r'$ and angles
fixed, $d^3x''=r''^2dr''\,d\Omega=\bigl(\frac{a^2}{r'}\bigr)^2\frac{a^2}{r'^2}dr'\,d\Omega
=(a/r')^6\,d^3x'$. Therefore
$$\rho^*(\vec x'')=\frac{dq^*}{d^3x''}
=-\frac{a}{r'}\Bigl(\frac{r'}{a}\Bigr)^{6}\rho(\vec x')
=-\Bigl(\frac{r'}{a}\Bigr)^{5}\rho(\vec x'),$$
and eliminating $r'=a^2/r''$ in favor of the image-point radius gives the
first stated form; reading the same equation at the direct point gives the
second. On the surface each $dq$–$dq^*$ pair separately produces zero
potential (that is what (3.46) was built to do), so $\Phi|_{r=a}=0$ for the
superposition; a surface of constant potential has no tangential field, i.e.
$\vec E\times\hat n|_{r=a}=0$ — the stated boundary condition.
(b) For $\rho(\vec x)=q\,\delta^3(\vec x-d\hat z)$, the element rule gives a
single image $-\,(a/d)\,q$ at $a^2/d\,\hat z$ — precisely (3.46). Totals:
$Q^*=\int\rho^*d^3x=-\int\frac{a}{r'}\rho\,d^3x'$ (each element weighted by
$a/r'$) — the code verifies this integral identity by two independent
quadratures for a Gaussian shell density, and verifies the surface condition
with a random point cloud.

### P13.  Exercise 3.3.4 — Two distant conducting spheres: capacitance coefficients  *(Wilcox 2e §3.13, pp.125–126)*
Two small conducting spheres, radii $a$ and $b$, are separated by $d\gg a,b$.
(a) Show the coefficient of capacitance $C_{ab}\simeq-ab/d$.
(b) With charges $Q$ and $-Q$ on the spheres, show the system capacitance
$C\equiv|Q/\Delta V|$ obeys
$$C\simeq\frac{ab}{a+b-\dfrac{2ab}{d}}.$$
*Answer:* as stated; corrections enter at relative order $(ab/d^2)$-type
terms.
*Check:* iterated-image capacitance matrix: $C_{ab}\to-ab/d$ (ratio improves
$\propto d^{-2}$…, measured), $C_{ab}=C_{ba}$, and the exact
$C=1/(p_{11}-2p_{12}+p_{22})$ matches the formula to $2\times10^{-3}$ at
$d=30$ (`test_p13_two_spheres`).

**Solution.** Work with the *potential* coefficients $p_{ij}$
($V_i=\sum_jp_{ij}Q_j$), which are transparent at large separation:
$p_{11}=1/a$, $p_{22}=1/b$ (isolated spheres), and $p_{12}=p_{21}\simeq1/d$
— exactly $1/d$ at leading order because an *uncharged* sphere in the field
of a distant point charge takes the potential of its center (mean-value
theorem; this is the reciprocation-theorem result the book flags via its
Ex. 2.12.5, and the "prove it first" it demands).
(a) Invert the $2\times2$ matrix:
$$C=P^{-1}=\frac{1}{p_{11}p_{22}-p_{12}^2}
\begin{pmatrix}p_{22}&-p_{12}\\-p_{12}&p_{11}\end{pmatrix}
\;\Rightarrow\;
C_{ab}=\frac{-1/d}{\frac1{ab}-\frac1{d^2}}
=-\frac{ab}{d}\,\frac{1}{1-\frac{ab}{d^2}}\simeq-\frac{ab}{d}.$$
(b) With $(Q_1,Q_2)=(Q,-Q)$:
$$\Delta V=V_1-V_2=(p_{11}-2p_{12}+p_{22})\,Q
=\Bigl(\frac1a+\frac1b-\frac2d\Bigr)Q,$$
so
$$C=\frac{Q}{\Delta V}=\frac{1}{\frac1a+\frac1b-\frac2d}
=\frac{ab}{a+b-\frac{2ab}{d}}.$$
The neglected physics is polarization: each sphere sees the other's field
gradient and grows an induced dipole, shifting $p_{12}$ at $O(1/d^3)$ and the
self terms at $O(ab^2/d^3)$-type order. The code builds the *exact* answer by
the classical iterated-image ladder (charge $a$ at the center of sphere 1,
image $-b\,q/(d-x)$ at $d-b^2/(d-x)$, image back in sphere 1, …), sums the
charge series to machine precision, and confirms both asymptotics and their
$d^{-2}$-rate of approach.

### P14.  Exercise 3.3.5 — Line charge and a conducting cylinder  *(Wilcox 2e §3.13, p.126)*
A unit-density line charge runs parallel to the axis of a hollow conducting
cylinder of radius $a$, at distance $\rho'$ from it.
(a) Show a parallel image line of density $-1$ at $\rho''=a^2/\rho'$ (on the
ray through the source) makes the cylinder an equipotential.
(b) Using (a) and the freedom to add a constant, obtain the interior Green
function
$$G_D(\rho,\phi;\rho',\phi')
=\ln\!\left[\frac{a^4+\rho^2\rho'^2-2a^2\rho\rho'\cos(\phi-\phi')}{a^2\,(\rho^2+\rho'^2-2\rho\rho'\cos(\phi-\phi'))}\right].$$
(c) Argue the exterior Green function is the *same* expression.
*Answer:* as stated.
*Check:* image construction $=$ closed form; $G=0$ on $\rho=a$ from either
side; symmetric in $(\rho,\phi)\leftrightarrow(\rho',\phi')$; harmonic away
from the source (`test_p14_cylinder_green`).

**Solution.** (a) With line charges, $G=-2\ln d_1+2\ln d_2+{\rm const}$,
where $d_1,d_2$ are transverse distances to source and trial image at
$\rho''$ on the same ray. On the cylinder ($\rho=a$, angle difference
$\Delta$):
$$d_2^2\big|_{\rho=a}=a^2+\frac{a^4}{\rho'^2}-2a\frac{a^2}{\rho'}\cos\Delta
=\frac{a^2}{\rho'^2}\Bigl(\rho'^2+a^2-2a\rho'\cos\Delta\Bigr)
=\Bigl(\frac{a}{\rho'}\Bigr)^2 d_1^2\big|_{\rho=a}.$$
So $-2\ln d_1+2\ln d_2=2\ln(a/\rho')$ — *constant* on the surface: the
cylinder is equipotential. This is the cylindrical twin of the sphere image,
same inversion point $a^2/\rho'$, but the image strength is exactly $-1$
(not $-a/\rho'$): logarithms trade the sphere's strength rescaling for an
additive constant.
(b) A potential plus a constant is still a potential; subtract the surface
value by adding $2\ln(\rho'/a)$:
$$G_D=-2\ln d_1+2\ln d_2+2\ln\frac{\rho'}{a}
=\ln\frac{d_2^2\,\rho'^2}{d_1^2\,a^2},$$
and $d_2^2\rho'^2=\rho^2\rho'^2+a^4-2a^2\rho\rho'\cos\Delta$ gives the boxed
form. It vanishes identically at $\rho=a$, has the correct $-2\ln$
singularity at the source, and is manifestly symmetric (the numerator and
denominator are symmetric polynomials in $\rho\leftrightarrow\rho'$) —
consistent with $G_D(\vec x,\vec x')=G_D(\vec x',\vec x)$.
(c) Read the same formula for $\rho>a$ with an exterior source $\rho'>a$: it
still solves the 2-D Green equation with the right singularity (the image
point $a^2/\rho'$ now lies *inside* the cylinder — outside the physical
region, as required), still vanishes on $\rho=a$, and matches the interior
form continuously there. Since the Dirichlet data and source structure fix
the solution up to the 2-D large-$\rho$ freedom (a constant — logs need not
vanish at infinity), the exterior Green function is the identical expression;
the code checks boundary zero and harmonicity with an exterior source. (This
$G$ feeds P27's Poisson integral.)

### P15.  Exercise 3.3.6 — Uniform charged shell around a grounded sphere  *(Wilcox 2e §3.13, p.126)*
A thin spherical shell of radius $b$, uniformly charged with total $Q$ (it is
**not** a conductor), is concentric with a grounded conducting sphere of
radius $a<b$ (a thin wire through the shell grounds the inner sphere). Find
$\Phi(\vec x)$ everywhere.
*Answer:*
$$\Phi=\begin{cases}0,&r\le a,\\[2pt]
\dfrac{Q}{b}\Bigl(1-\dfrac ar\Bigr),&a\le r\le b,\\[6pt]
\dfrac{Q\,(1-a/b)}{r},&r\ge b,\end{cases}$$
with induced charge $-Qa/b$ on the grounded sphere.
*Check:* quadrature of $\sigma_b\,G_D$ over the shell reproduces the closed
form in both regions; $\Phi(a)=0$ (`test_p15_shell_around_grounded_sphere`).

**Solution.** Everything is spherically symmetric, so
$\Phi=A_i+B_i/r$ region by region. Let $q_a$ be the induced charge on the
grounded sphere. Gauss: for $a<r<b$, $E_r=q_a/r^2$; for $r>b$,
$E_r=(q_a+Q)/r^2$. Integrate inward from infinity:
$$\Phi(r\ge b)=\frac{q_a+Q}{r},\qquad
\Phi(a\le r\le b)=\frac{q_a}{r}+C,$$
with $C$ fixed by continuity at $b$: $C=Q/b$. Grounding pins
$\Phi(a)=0$:
$$\frac{q_a}{a}+\frac{Q}{b}=0\;\Longrightarrow\;q_a=-\frac{a}{b}\,Q,$$
which plugged back gives exactly the three-region answer (and $\Phi\equiv0$
for $r\le a$, the field-free grounded interior). Green-function route (the
module's check): each shell element $dq$ at radius $b$ has grounded-sphere
weight $G_D$ of (3.48), so $\Phi(\vec x)=\oint\sigma_b\,G_D(\vec x,\vec x')\,da'$
with $\sigma_b=Q/4\pi b^2$; the code does this quadrature and lands on the
closed form — including the exterior region, where the image content of
$G_D$ automatically supplies the $-Qa/b$. Notice $q_a$ is exactly the sum of
the per-element images $-(a/b)\,dq$ (P12's rule with $r'=b$ for every
element).

### P16.  Exercise 3.3.7 — Charged ring around a grounded sphere  *(Wilcox 2e §3.13, pp.126–127)*
A circular ring of radius $b$, uniform line density $\lambda$, lies in the
equatorial plane $z=0$ of a grounded conducting sphere of radius $a<b$,
concentric with it (the book's Fig. 3.23).
(a) Find the induced charge on the sphere.
(b) Find $\Phi(z)$ on the symmetry axis outside the sphere, and confirm
$\Phi(\pm a)=0$.
*Answer:* (a) $q_{\rm ind}=-2\pi a\lambda=-(a/b)\,Q_{\rm ring}$;
(b) $\displaystyle\Phi(z)=\frac{2\pi b\lambda}{\sqrt{z^2+b^2}}
-\frac{2\pi a\lambda}{\sqrt{z^2+a^4/b^2}}$, which vanishes at $z=\pm a$.
*Check:* Green-function quadrature around the ring equals the closed form;
$\Phi(\pm a)=0$; far field $(Q_{\rm ring}+q_{\rm ind})/z$
(`test_p16_ring_around_grounded_sphere`).

**Solution.** (a) Every ring element sits at radius $b$, so each $dq$ has
image $-(a/b)\,dq$ at radius $a^2/b$ (the image of a concentric equatorial
ring is a concentric equatorial ring of radius $a^2/b$). Summing,
$$q_{\rm ind}=-\frac ab\,Q_{\rm ring}=-\frac ab\,(2\pi b\lambda)=-2\pi a\lambda.$$
(b) On the axis every point of a ring of radius $R$ is at distance
$\sqrt{z^2+R^2}$, so a ring of charge $q$ contributes $q/\sqrt{z^2+R^2}$.
Direct ring: $Q_{\rm ring}=2\pi b\lambda$ at radius $b$. Image ring:
$-2\pi a\lambda$ at radius $a^2/b$. Therefore
$$\Phi(z)=\frac{2\pi b\lambda}{\sqrt{z^2+b^2}}-\frac{2\pi a\lambda}{\sqrt{z^2+a^4/b^2}} .$$
At $z=\pm a$: $\sqrt{a^2+a^4/b^2}=\frac ab\sqrt{a^2+b^2}$, so the second term
is $2\pi a\lambda\cdot\frac{b}{a\sqrt{a^2+b^2}}=2\pi b\lambda/\sqrt{a^2+b^2}$
— exactly the first: $\Phi(\pm a)=0$, the axis meeting the grounded surface.
Far away, $\Phi\to(2\pi b\lambda-2\pi a\lambda)/|z|$: the monopole is the
*total* (ring + induced) charge, as it must be. The code integrates
$\lambda\,b\,d\phi'\,G_D$ around the ring with (3.48) and matches the closed
form at $10^{-10}$.

### P17.  Exercise 3.3.8 — Force from a held-at-V sphere; force from a neutral sphere  *(Wilcox 2e §3.13, p.127)*
A point charge $q$ sits at distance $d>a$ from the center of a conducting
sphere of radius $a$.
(a) The sphere is held at potential $V\neq0$. Show the force on $q$ can be
made zero by tuning $V$, and find that $V$ in terms of $q,a,d$.
(b) The sphere is instead neutral and isolated. Find the force on $q$.
*Answer:* (a) $\displaystyle F=\frac{qVa}{d^2}-\frac{q^2ad}{(d^2-a^2)^2}$,
zero at $\displaystyle V_0=\frac{q\,d^3}{(d^2-a^2)^2}$;
(b) $\displaystyle F=q^2a\left[\frac1{d^3}-\frac{d}{(d^2-a^2)^2}\right]
=-\frac{q^2a^3(2d^2-a^2)}{d^3(d^2-a^2)^2}<0$ (always attractive), with
$U=-\dfrac{q^2a^3}{2d^2(d^2-a^2)}$.
*Check:* $F(V_0)=0$; the neutral force equals the two-image Coulomb sum;
$F=-dU/dd$ numerically; far field $-2q^2a^3/d^5$ (`test_p17_sphere_forces`).

**Solution.** The exterior solution (3.53) is $q\,G_D+Va/r$: i.e. the field
of *three* point charges — the source $q$; the grounded-sphere image
$q'=-qa/d$ at $r''=a^2/d$; and a fictitious center charge $Va$ carrying the
$Va/r$ term. The force on $q$ is $q$ times the field of the other two at
$r=d$ (its own field exerts nothing):
$$F=q\left[\frac{Va}{d^2}+\frac{q'}{(d-r'')^2}\right]
=\frac{qVa}{d^2}-\frac{q^2 a d}{(d^2-a^2)^2},$$
using $d-a^2/d=(d^2-a^2)/d$. (a) The image term is always attractive; a $V$
of the same sign as $q$ repels. Setting $F=0$:
$$\frac{qVa}{d^2}=\frac{q^2ad}{(d^2-a^2)^2}
\;\Longrightarrow\;
V_0=\frac{q\,d^3}{(d^2-a^2)^2}\, .$$
(Near contact $V_0$ diverges — the image attraction is too singular to beat;
far away $V_0\to q/d$, the value that just cancels the induced-dipole pull.)
(b) Neutral isolated sphere: (3.55) with $Q=0$ replaces $Va$ by $+qa/d$ at
the center (the compensating charge that restores neutrality against the
image $-qa/d$). Then
$$F=q\left[\frac{qa/d}{d^2}-\frac{qad}{(d^2-a^2)^2}\right]
=q^2a\left[\frac1{d^3}-\frac{d}{(d^2-a^2)^2}\right]<0\quad(d>a),$$
attraction always: the sphere polarizes, the near (opposite-sign) induced
charge is closer than the far one. Combining over a common denominator gives
the $-q^2a^3(2d^2-a^2)/[d^3(d^2-a^2)^2]$ form; integrating $-F$ from $d$ to
$\infty$ gives $U=-q^2a^3/[2d^2(d^2-a^2)]$ (the code checks $F=-dU/dd$
numerically), and expanding for $d\gg a$:
$$F\simeq-\frac{2q^2a^3}{d^5},$$
the induced-dipole law — the sphere's polarizability is $a^3$, the induced
moment $p=a^3E=a^3q/d^2$, and $F=-2pq/d^3$. All four statements are asserted
numerically.

### P18.  Exercise 3.5.1 — 2-D box by separation of variables  *(Wilcox 2e §3.13, pp.127–128)*
Solve $\partial_x^2\Phi+\partial_y^2\Phi=0$ by separation of variables inside
the rectangle $0<x<a$, $0<y<b$, with $\Phi=0$ on all sides except $y=b$, where
$\Phi=V$ (constant). Express $\Phi$ as an infinite series.
*Answer:* with $m=2n-1$ running over odd integers,
$$\Phi(x,y)=\frac{4V}{\pi}\sum_{n=1}^{\infty}\frac1m\,
\frac{\sinh(m\pi y/a)}{\sinh(m\pi b/a)}\,\sin\frac{m\pi x}{a}.$$
*Check:* series matches a sparse finite-difference Laplace solve at interior
points to $4\times10^{-3}$; exact zeros on the three grounded sides; numeric
Laplacian $\approx0$ (`test_p18_box_series_vs_fd`).

**Solution.** Insert $\Phi=X(x)Y(y)$: $X''/X=-Y''/Y=-\alpha^2$ constant. The
homogeneous conditions steer the split: $\Phi(0,y)=\Phi(a,y)=0$ wants
oscillation in $x$, so $X=\sin\alpha x$ with $\sin\alpha a=0$, i.e.
$\alpha_m=m\pi/a$, $m=1,2,\dots$ — the Fourier sine family of `~MA-11`; then
$Y''=\alpha^2Y$ gives $\sinh/\cosh$, and $\Phi(x,0)=0$ kills the $\cosh$:
$Y_m=\sinh(m\pi y/a)$. Superpose and match the last side:
$$\Phi(x,b)=\sum_mB_m\sinh\frac{m\pi b}{a}\sin\frac{m\pi x}{a}=V .$$
Sine orthogonality ($\int_0^a\sin\frac{m\pi x}{a}\sin\frac{m'\pi x}{a}dx=\frac a2\delta_{mm'}$,
Eq. 3.83) projects out
$$B_m\sinh\frac{m\pi b}{a}=\frac2a\int_0^aV\sin\frac{m\pi x}{a}dx
=\frac{2V}{m\pi}\bigl[1-(-1)^m\bigr]
=\begin{cases}\dfrac{4V}{m\pi},&m\ \text{odd},\\0,&m\ \text{even},\end{cases}$$
giving the quoted series. (Even $m$ vanish by the symmetry
$x\to a-x$ of the data.) This is the same slot expansion as `~EM-04` §5, with
$\sinh$ replacing the decaying exponential because the box is finite. The
finite-difference cross-check is the uniqueness theorem run numerically: two
utterly different constructions, one harmonic function.

### P19.  Exercise 3.5.2 — Semi-infinite slot with a charged side wall  *(Wilcox 2e §3.13, p.128)*
In the strip $0<x<a$, $y>0$ (the book's Fig. 3.24) the wall $x=0$ is at
constant potential $V$ while $y=0$ and $x=a$ are grounded; the $y$-dependent
part of the solution must die off as $y\to+\infty$. Writing
$$\Phi=\Phi_1+\Phi_2,\qquad
\Phi_1=\sum_{n\ge1}A_n\sin\frac{n\pi x}{a}\,e^{-n\pi y/a},\qquad
\Phi_2=V\Bigl(1-\frac xa\Bigr),$$
determine the coefficients $A_n$.
*Answer:* $A_n=-\dfrac{2V}{n\pi}$ for every $n\ge1$.
*Check:* Fourier quadrature reproduces $A_7$; $\Phi(0,y)=V$ exactly,
$\Phi(a,y)=0$, $\Phi(x,0)\to0$ (partial sums), $\Phi\to V(1-x/a)$ as
$y\to\infty$; numeric Laplacian $\approx0$ (`test_p19_strip`).

**Solution.** The decomposition does the bookkeeping: $\Phi_2$ is harmonic
(linear), matches $V$ at $x=0$ and $0$ at $x=a$ *for all* $y$, and is the
$y\to\infty$ limit (far up the slot the problem is one-dimensional between
the two vertical walls, so the potential cannot vanish there — it tends to
the linear profile; what decays is $\Phi_1$). $\Phi_1$, built from the
grounded-wall modes $\sin(n\pi x/a)e^{-n\pi y/a}$, vanishes on $x=0,a$ and at
large $y$; its job is the remaining condition at the floor:
$$0=\Phi(x,0)=\Phi_2(x)+\sum_nA_n\sin\frac{n\pi x}{a}
\;\Longrightarrow\;
\sum_nA_n\sin\frac{n\pi x}{a}=-V\Bigl(1-\frac xa\Bigr).$$
Project with sine orthogonality:
$$A_n=-\frac{2V}{a}\int_0^a\Bigl(1-\frac xa\Bigr)\sin\frac{n\pi x}{a}\,dx
=-\frac{2V}{a}\cdot\frac{a}{n\pi}=-\frac{2V}{n\pi},$$
using $\int_0^a(1-x/a)\sin(n\pi x/a)\,dx=a/n\pi$ (integrate the two pieces;
the $(-1)^n$ terms cancel between them). Every $n$ contributes — the sawtooth
$V(1-x/a)$ has no parity to kill alternate terms. So
$$\Phi=V\Bigl(1-\frac xa\Bigr)-\frac{2V}{\pi}\sum_{n=1}^\infty
\frac1n\,e^{-n\pi y/a}\sin\frac{n\pi x}{a},$$
whose $y=0$ trace is the familiar Fourier sawtooth identity
$\frac{2V}{\pi}\sum\frac1n\sin\frac{n\pi x}{a}=V(1-x/a)$ — P20(b) meets it
again from the Green-function side.

### P20.  Exercise 3.5.3 — Dirichlet Green function of the slot  *(Wilcox 2e §3.13, pp.128–129)*
Same region as P19, all three walls now grounded.
(a) Show that the Green function obeying
$\nabla^2G_D=-4\pi\delta(x-x')\delta(y-y')$ inside and $G_D=0$ on the walls is
$$G_D=8\sum_{n=1}^{\infty}\frac1n\,\sin\frac{n\pi x}{a}\sin\frac{n\pi x'}{a}\,
\sinh\frac{n\pi y_<}{a}\,e^{-n\pi y_>/a},$$
$y_<$ ($y_>$) the lesser (greater) of $y,y'$.
(b) Use it to re-solve P19 (a telling Fourier series appears for $\Phi_2$).
*Answer:* as stated; the wall integral gives
$\Phi=\frac{2V}{\pi}\sum\frac1n\sin\frac{n\pi x}{a}\bigl(1-e^{-n\pi y/a}\bigr)$,
identical to P19 via the sawtooth series.
*Check:* wall zeros; symmetry; flux $\oint\partial_nG\,dl=-4\pi$ around the
source; recovered $\Phi$ equals P19's to $3\times10^{-4}$ (60000-term sawtooth
tail) (`test_p20_green_strip`).

**Solution.** (a) Expand both $G_D$ and $\delta(x-x')$ in the wall-adapted
sine basis (Eq. 3.89): $\delta(x-x')=\frac2a\sum_n\sin\frac{n\pi x}{a}\sin\frac{n\pi x'}{a}$.
Writing $G_D=\sum_n\sin\frac{n\pi x}{a}\sin\frac{n\pi x'}{a}\,h_n(y,y')$ and
matching term by term,
$$h_n''-\Bigl(\frac{n\pi}{a}\Bigr)^2h_n=-\frac{8\pi}{a}\,\delta(y-y'),$$
with $h_n(0)=0$ and decay as $y\to\infty$. Below the source take
$A\sinh(k_ny)$, above take $Be^{-k_ny}$ ($k_n=n\pi/a$); continuity and the
jump $-h_n'\,|^+_-=8\pi/a$ give $A=\frac{8\pi}{ak_n}e^{-k_ny'}$,
$B=\frac{8\pi}{ak_n}\sinh(k_ny')$, i.e.
$h_n=\frac{8}{n}\sinh(k_ny_<)e^{-k_ny_>}$ — the quoted $G_D$. The code's flux
integral around the source verifies the $-4\pi$ normalization the ODE jump
encodes.
(b) Only the charged wall $x'=0$ contributes to (2.98):
$\partial G/\partial n'=-\partial G/\partial x'|_{x'=0}
=-\frac{8\pi}{a}\sum_n\sin\frac{n\pi x}{a}\sinh\frac{n\pi y_<}{a}e^{-n\pi y_>/a}$.
The $y'$ integral splits at $y$ and is elementary:
$$\int_0^\infty\!dy'\,\sinh(k y_<)e^{-k y_>}
=\frac{e^{-ky}\bigl(\cosh ky-1\bigr)}{k}+\frac{\sinh(ky)\,e^{-ky}}{k}
=\frac{1-e^{-ky}}{k},$$
(the $e^{-ky}\cosh ky+e^{-ky}\sinh ky=1$ collapse). Hence
$$\Phi(x,y)=-\frac{V}{4\pi}\int_0^\infty dy'\,\Bigl(-\frac{8\pi}{a}\Bigr)\sum_n(\cdots)
=\frac{2V}{\pi}\sum_{n=1}^\infty\frac1n\sin\frac{n\pi x}{a}\Bigl(1-e^{-n\pi y/a}\Bigr).$$
The "$1$" part is the sawtooth series summing to $\Phi_2=V(1-x/a)$ — the
Fourier series the exercise advertises — and the exponential part is exactly
$\Phi_1$ with $A_n=-2V/n\pi$: P19 recovered wholesale. (Numerically the
sawtooth converges only like $1/N$, which is why the test compares with a
$6\times10^4$-term partial sum.)

### P21.  Exercise 3.5.4 — Neumann Green function of the slot  *(Wilcox 2e §3.13, p.129)*
Same strip, but the three walls are now Neumann surfaces:
$\nabla^2G_N=-4\pi\delta^2$ inside and $\partial G_N/\partial n=0$ on the
walls. Use the even (cosine) representation of the delta function,
$$\delta(x-x')=\frac2a\sum_{n=0}^\infty\delta_n\cos\frac{n\pi x}{a}\cos\frac{n\pi x'}{a},
\qquad\delta_n=\begin{cases}1/2,&n=0\\1,&n>0\end{cases}$$
(its terms have vanishing normal *derivative* on the walls), and find $G_N$.
*Answer:* up to an additive constant,
$$G_N=8\sum_{n=1}^{\infty}\frac1n\cos\frac{n\pi x}{a}\cos\frac{n\pi x'}{a}
\cosh\frac{n\pi y_<}{a}\,e^{-n\pi y_>/a}\;-\;\frac{4\pi y_>}{a}.$$
*Check:* one-sided normal differences vanish $\propto h$ on all three walls;
symmetry; the flux through the cross-section $y=3a$ is exactly $-4\pi$
(Gauss/Eq. 2.102) (`test_p21_green_strip_neumann`).

**Solution.** Expand $G_N=\sum_{n\ge0}\cos\frac{n\pi x}{a}\cos\frac{n\pi x'}{a}h_n(y,y')$.
The $n\ge1$ modes obey $h_n''-k_n^2h_n=-\frac{8\pi}{a}\delta(y-y')$ as before,
but with the *Neumann* floor condition $h_n'(0)=0$: even solution
$\cosh(k_ny)$ below the source, decay above, so
$h_n=\frac8n\cosh(k_ny_<)e^{-k_ny_>}$.
The $n=0$ mode is where Neumann problems earn their keep: with $\delta_0=1/2$,
$$h_0''=-\frac{4\pi}{a}\,\delta(y-y'),\qquad h_0'(0)=0 .$$
Integrating: $h_0'$ is $0$ below the source (floor condition) and jumps to
$-4\pi/a$ above it, so $h_0=-\frac{4\pi}{a}y_>+{\rm const}$ — the secular
term. It *cannot* decay: Gauss's theorem (2.102) demands
$\oint\partial_nG_N\,da=-4\pi$, and with rigid walls the only exit is the open
end. Indeed the flux there is $a\cdot\partial_y(-4\pi y/a)=-4\pi$ ✓ (the
oscillatory modes integrate to zero across the section — the code measures
exactly $-4\pi$ at $y=3a$). Equivalently: for this unbounded surface the
$-4\pi/S$ of (2.106) is zero on the walls, and the "charge outflow" is
carried by the secular mode. The additive constant is the usual Neumann
gauge freedom ((2.103) defines $\Phi$ only up to $\langle\Phi\rangle_S$).

### P22.  Exercise 3.5.5 — Line charge between two grounded planes (2-D)  *(Wilcox 2e §3.13, p.130)*
Two infinite parallel grounded plates $x=0$ and $x=a$ extend to $y\to\pm\infty$
(the book's Fig. 3.25); a long line charge, parallel to the plates, makes the
problem $z$-independent, so
$\left(\partial_x^2+\partial_y^2\right)G_D=-4\pi\delta(x-x')\delta(y-y')$.
Assuming
$$G_D=\sum_{n\ge1}\sin\frac{n\pi x}{a}\sin\frac{n\pi x'}{a}\,g_n(y,y'),$$
find the reduced Green function $g_n$.
*Answer:* $\displaystyle g_n(y,y')=\frac4n\,e^{-n\pi|y-y'|/a}$; the sum has
the closed form
$$G_D=\ln\!\left[\frac{\cosh\frac{\pi(y-y')}{a}-\cos\frac{\pi(x+x')}{a}}
{\cosh\frac{\pi(y-y')}{a}-\cos\frac{\pi(x-x')}{a}}\right],$$
also expressible as the image ladder of line charges at $2na\pm x'$.
*Check:* series $=$ closed form $=$ Richardson-extrapolated image sum; zeros
on both plates (`test_p22_two_plates_2d`).

**Solution.** The sine projection gives
$g_n''-k_n^2g_n=-\frac{8\pi}{a}\delta(y-y')$ with decay in *both* directions
($k_n=n\pi/a$): the symmetric decaying solution is
$$g_n=\frac{8\pi}{a}\cdot\frac{e^{-k_n|y-y'|}}{2k_n}=\frac4n\,e^{-n\pi|y-y'|/a},$$
(check the jump: $-\partial_yg_n$ jumps by $\frac{8\pi}{a}$ across $y'$ ✓).
To sum, write $\sin\sin'=\tfrac12[\cos\theta_--\cos\theta_+]$ with
$\theta_\pm=\pi(x\pm x')/a$, and use
$\sum_{n\ge1}\frac{t^n}{n}\cos n\theta=-\tfrac12\ln(1-2t\cos\theta+t^2)$ with
$t=e^{-\pi|y-y'|/a}$:
$$G_D=\ln\frac{1-2t\cos\theta_++t^2}{1-2t\cos\theta_-+t^2}
=\ln\frac{\cosh\frac{\pi\Delta y}{a}-\cos\theta_+}{\cosh\frac{\pi\Delta y}{a}-\cos\theta_-},$$
dividing through by $2t$. As $x\to x',y\to y'$ the denominator vanishes
quadratically, reproducing the $-2\ln$ line-charge singularity; on $x=0$ or
$x=a$, $\cos\theta_+=\cos\theta_-$ and $G_D=0$. The same $G_D$ is the 2-D
image ladder (P1's picture with line charges): $-2\sum_n[\ln d_n^+-\ln d_n^-]$
with images at $2na\pm x'$ — symmetric truncations converge $\sim1/N$, so the
code Richardson-extrapolates before comparing all three representations.

### P23.  Exercise 3.5.6 — 2-D box with a linear top potential  *(Wilcox 2e §3.13, p.130)*
Same rectangle as P18 ($0<x<a$, $0<y<b$) with $V=0$ on $x=0$, $x=a$, $y=0$,
but now $V(x)=-Ex$ ($E$ constant) on $y=b$. Find $\Phi$ inside.
*Answer:*
$$\Phi(x,y)=\frac{2Ea}{\pi}\sum_{m=1}^{\infty}\frac{(-1)^m}{m}\,
\frac{\sinh(m\pi y/a)}{\sinh(m\pi b/a)}\,\sin\frac{m\pi x}{a}.$$
*Check:* matches the finite-difference solve with boundary $-Ex$ to
$5\times10^{-3}$ (`test_p23_box_Ex`).

**Solution.** The machinery of P18 carries over unchanged until the last
projection, which now meets the data $-Ex$:
$$B_m\sinh\frac{m\pi b}{a}=\frac2a\int_0^a(-Ex)\sin\frac{m\pi x}{a}\,dx .$$
With $\int_0^ax\sin\frac{m\pi x}{a}dx=\frac{a^2}{m\pi}(-1)^{m+1}$ (integrate
by parts; the boundary term at $x=a$ carries the sign),
$$B_m=-\frac{2E}{a}\cdot\frac{a^2(-1)^{m+1}}{m\pi\,\sinh(m\pi b/a)}
=\frac{2Ea\,(-1)^m}{m\pi\,\sinh(m\pi b/a)},$$
giving the stated series — all $m$ present and alternating, the signature of
data that is odd about the box midline ($-Ex$ has no $x\to a-x$ symmetry, but
its sawtooth extension alternates). Sanity: at $y=b$ the series is the
standard Fourier expansion $x=\sum_m\frac{2a(-1)^{m+1}}{m\pi}\sin\frac{m\pi x}{a}$
times $-E$ ✓; and term by term each summand is harmonic, so the sum is the
solution (uniqueness against the FD solver in the test).

### P24.  Exercise 3.6.1 — The Madelung constant from the box Green function  *(Wilcox 2e §3.13, pp.130–131)*
Reproduce numerically the NaCl Madelung constant (Na$^+$ reference),
$$M=\mathop{{\sum}'}_{i,j,k}\frac{(-1)^{i+j+k}}{\sqrt{i^2+j^2+k^2}}=-1.747564594\ldots,$$
from the box eigenfunction Green function (3.98). Setting
$x=x'=y=y'=z=z'=a/2$ outright diverges — the reference charge's self-energy —
so remove that energy approximately and obtain $M$ to at least three decimal
places.
*Answer:* $M=a\cdot\lim_{\vec x'\to\vec x}\bigl[G_D(\vec x,\vec x')-1/|\vec x-\vec x'|\bigr]$
at the cube center; the module's $\epsilon$-extrapolation gives $-1.747563$,
matching the lattice value to $1\times10^{-6}$.
*Check:* `madelung_from_box_green()` within $5\times10^{-4}$ of
$-1.747564594$ (actually $\sim10^{-6}$); Evjen lattice sum within
$2\times10^{-6}$ (`test_p24_madelung`); (3.98) also passes reciprocity and
short-distance $1/|\vec x-\vec x'|$ tests (`test_p24_box_green_reciprocity`,
`test_p24_box_green_point_charge`).

**Solution.** The bridge is §3.6's image-lattice reading of the box Green
function: for a unit charge at the center of a grounded cube of side $a$, the
images are unit charges of sign $(-1)^{i+j+k}$ at the points
$({\rm center})+a\,(i,j,k)$ — precisely the NaCl arrangement with lattice
spacing $a$. Therefore
$$G_D(\vec x,\vec x')\;\xrightarrow{\ \vec x'\to\vec x={\rm center}\ }\;
\underbrace{\frac1{|\vec x-\vec x'|}}_{\text{self}}\;+\;\underbrace{\frac Ma}_{\text{all images}}\;+\;O(|\vec x-\vec x'|^2),$$
so the Madelung energy is the *regularized* Green function at coincidence —
remove the self term and take the limit. (Interpreting $M$ through $G_D$ also
dissolves the conditional-convergence worry the book raises about (3.108):
the grounded box fixes the summation order physically.) Numerically (unit
cube): put the two arguments at ${\rm center}\pm(\epsilon/2)\hat z$, sum
(3.98) — at the center only odd $n,m$ survive since $\sin^2(n\pi/2)$ selects
them — with the exp-stable reduced factor, and form
$$S(\epsilon)=G_D(\epsilon)-\frac1\epsilon=M+c_2\epsilon^2+c_4\epsilon^4+\cdots$$
($\epsilon$-even by the symmetry of the split). Two Richardson steps on
$\epsilon=(0.2,\,0.1,\,0.05)$ annihilate $c_2$ and $c_4$:
$$M\simeq\frac{16B-A}{15},\qquad
A=\frac{4S(0.1)-S(0.2)}{3},\quad B=\frac{4S(0.05)-S(0.1)}{3},$$
yielding $-1.7475635$ — five good decimals, comfortably beyond the requested
three. Cross-check: the Evjen summation (expanding cubes with $1/2$-weighted
faces, the standard cure for the conditional convergence) gives
$-1.7475646$ at $N=14$. The interaction energy per reference ion is then
$W=M/a$, as the book notes below (3.108).

### P25.  Exercise 3.7.1 — Cylinder with a point (delta) surface potential  *(Wilcox 2e §3.13, p.131)*
A charge-free conducting cylinder of radius $b$ has surface potential
$\Phi(b,\phi)=V_0\,\delta(\phi)$ on $-\pi<\phi<\pi$ (no other sources). Using
polar separation of variables, find the Fourier series for $\Phi$ everywhere
inside.
*Answer:*
$$\Phi(\rho,\phi)=\frac{V_0}{2\pi}+\frac{V_0}{\pi}\sum_{m=1}^{\infty}
\Bigl(\frac\rho b\Bigr)^{m}\cos(m\phi).$$
*Check:* partial sums agree with the Poisson-kernel closed form of P31 to
$10^{-10}$; $\Phi(0)=V_0/2\pi$, the surface average
(`test_p25_cylinder_delta_series`).

**Solution.** The full-azimuth interior solution (3.118) keeps only the terms
regular at $\rho=0$: $\Phi=a_0+\sum_m\rho^m(A_m\cos m\phi+B_m\sin m\phi)$
(the $\ln\rho$ and $\rho^{-m}$ members would blow up at the axis). Match at
$\rho=b$ against the Fourier expansion of the data: for $\delta(\phi)$ on
$(-\pi,\pi)$,
$$\delta(\phi)=\frac1{2\pi}+\frac1\pi\sum_{m=1}^\infty\cos m\phi$$
(all cosine coefficients equal $\frac1\pi\int\delta\cos m\phi\,d\phi=\frac1\pi$;
no sines, $\delta$ being even). Termwise identification gives
$a_0=V_0/2\pi$, $A_mb^m=V_0/\pi$, $B_m=0$ — the quoted series. Physical
readings: $\Phi(0)=V_0/2\pi$ is the surface average (mean-value theorem, the
$m=0$ term); each higher multipole of the pinprick data decays inward as
$(\rho/b)^m$ — the cylinder is a low-pass filter in harmonic content, which
is why relaxation methods smooth from the boundary in (`~EM-04` §6). P31
sums this series to the 2-D Poisson kernel, closing the loop with the Green
function of P27.

### P26.  Exercise 3.8.1 — Cylindrical pie wedge with given end data  *(Wilcox 2e §3.13, p.131)*
A conducting "pie" of opening angle $\beta$ (the book's Fig. 3.26) has its two
straight sides held at the constant potential $V$, while the curved end at
$\rho=b$ carries a given profile $\Phi(b,\phi)$; discontinuities at the
corners $\phi=0,\beta$ are allowed. Find the Fourier representation of $\Phi$
in the interior.
*Answer:*
$$\Phi(\rho,\phi)=V+\sum_{m=1}^\infty a_m\,\rho^{m\pi/\beta}\sin\frac{m\pi\phi}{\beta},
\qquad
a_m=\frac{2}{\beta\,b^{m\pi/\beta}}\int_0^\beta\bigl[\Phi(b,\phi')-V\bigr]
\sin\frac{m\pi\phi'}{\beta}\,d\phi' .$$
*Check:* single-mode manufactured data is recovered exactly; generic data is
reproduced at $\rho\to b$; the sides sit at $V$; the corner field scales as
$\rho^{\pi/\beta-1}$ (log-slope fit) (`test_p26_wedge`).

**Solution.** This is §3.8's corner solution (3.119) promoted to a full
boundary-value problem. The angular range is restricted to $(0,\beta)$, so
single-valuedness no longer quantizes $\nu$; instead the *side conditions* do.
Keep the members of (3.114)–(3.115) regular at $\rho=0$ (drop $\rho^{-\nu}$
and $\ln\rho$). The $\nu=0$ piece $A_0+B_0\phi$ must satisfy $\Phi=V$ at both
$\phi=0$ and $\phi=\beta$: $A_0=V$, $B_0=0$. The $\nu\ne0$ pieces must vanish
at both sides (their job is the *deviation* from $V$): $\sin(\nu\phi)$ with
$\sin(\nu\beta)=0$, i.e.
$$\nu_m=\frac{m\pi}{\beta},\qquad m=1,2,\dots$$
— generally non-integer powers of $\rho$; nothing is wrong with that away
from the axis' full neighborhood. Superpose and match the end data:
$\Phi(b,\phi)-V=\sum_ma_mb^{m\pi/\beta}\sin(m\pi\phi/\beta)$ is an ordinary
Fourier sine series on $(0,\beta)$ (the Sturm–Liouville family of `~MA-11`);
orthogonality delivers the quoted $a_m$. Endpoint mismatches
($\Phi(b,0^+)\neq V$ etc.) are fine — sine series converge to the data in the
open interval and to the mean at jumps. Near the tip the $m=1$ term dominates
(Eq. 3.120): $\Phi-V\approx a_1\rho^{\pi/\beta}\sin(\pi\phi/\beta)$ and
$|\vec E|=\frac{\pi|a_1|}{\beta}\rho^{\pi/\beta-1}$ (3.123): field
*concentration* at a reentrant tip ($\beta>\pi$), *shielding* in a slot
($\beta<\pi$) — the lightning-rod exponent, which the test extracts from the
series by a log-log fit. (If the two sides carry different constants
$V_1,V_2$, add the extra harmonic wedge term $(V_2-V_1)\phi/\beta$ — P2(c) is
exactly that case with $\Phi(b,\phi)$ absent.)

### P27.  Exercise 3.9.1 — Poisson's integral for the cylinder  *(Wilcox 2e §3.13, p.131)*
Using the cylinder Green function of P14, show that the interior potential of
a cylinder of radius $b$ with surface data $\Phi(b,\phi)$ is
$$\Phi(\rho,\phi)=\frac1{2\pi}\int_0^{2\pi}d\phi'\,\Phi(b,\phi')\,
\frac{b^2-\rho^2}{\rho^2+b^2-2b\rho\cos(\phi-\phi')}$$
— Poisson's integral.
*Answer:* as stated; the kernel is positive, has unit angular integral, and
peaks at $\phi'=\phi$ as $\rho\to b$.
*Check:* unit normalization to $10^{-12}$; reproduces $\cos\phi'$ data as
$(\rho/b)\cos\phi$; numerically harmonic for step data
(`test_p27_poisson_integral`).

**Solution.** With no interior charge, (2.98) keeps only the surface term
$\Phi=-\frac1{4\pi}\oint\Phi\,\partial G_D/\partial n'\,dl'$ (2-D: a line
integral, the $z'$ length already absorbed in the line-charge normalization).
Differentiate P14's closed form radially at $\rho'=b$; writing
$D=\rho^2+b^2-2b\rho\cos\Delta$, $\Delta=\phi-\phi'$:
$$\frac{\partial G_D}{\partial\rho'}\Big|_{\rho'=b}
=\frac{2\rho^2b-2b^2\rho\cos\Delta}{b^2\,D}-\frac{2b-2\rho\cos\Delta}{D}
=\frac{2}{b}\,\frac{\rho^2-b^2}{D}.$$
The outward normal of the interior region is $+\hat\rho'$, so
$\partial G/\partial n'=\partial G/\partial\rho'|_{\rho'=b}$ and, with
$dl'=b\,d\phi'$,
$$\Phi=-\frac1{4\pi}\int_0^{2\pi}\Phi(b,\phi')\,\frac2b\frac{\rho^2-b^2}{D}\,b\,d\phi'
=\frac1{2\pi}\int_0^{2\pi}d\phi'\,\Phi(b,\phi')\,\frac{b^2-\rho^2}{D}\, .$$
Properties worth logging (all tested): setting $\Phi(b,\cdot)\equiv1$ must
return $1$ (an equipotential cylinder has a constant interior), so the kernel
has unit angular integral; at $\rho=0$ it is
uniform — the mean-value theorem again; and as $\rho\to b^-$ it becomes a
delta family in $\phi'-\phi$, reproducing the boundary data pointwise where
it is continuous. This kernel is the 2-D twin of the sphere's (3.50).

### P28.  Exercise 3.9.2 — Split cylinder by Poisson's integral  *(Wilcox 2e §3.13, p.132)*
Use P27 to re-derive the interior potential (3.131) of a long cylinder of
radius $b$ whose half-surfaces are at $V_1$ ($-\pi/2<\phi<\pi/2$) and $V_2$
($\pi/2<\phi<3\pi/2$) (the book's Fig. 3.12).
*Answer:*
$$\Phi(\rho,\phi)=\frac{V_1+V_2}{2}+\frac{V_1-V_2}{\pi}
\arctan\!\left[\frac{2(\rho/b)\cos\phi}{1-(\rho/b)^2}\right].$$
*Check:* Poisson quadrature (panels split at the data jumps) matches the
closed form to $10^{-9}$ over the interior (`test_p28_halves_via_poisson`).

**Solution.** Split the data as the mean plus an odd square wave:
$\Phi(b,\phi')=\frac{V_1+V_2}2+\frac{V_1-V_2}2\,{\rm sq}(\phi')$, with
${\rm sq}=+1$ on the right half, $-1$ on the left. The mean passes through
the unit-normalized kernel untouched. For the square-wave part, the needed
antiderivative is standard:
$$\int\frac{d\phi'}{\rho^2+b^2-2b\rho\cos(\phi-\phi')}
=\frac{2}{b^2-\rho^2}\arctan\!\left[\frac{b+\rho}{b-\rho}\tan\frac{\phi'-\phi}{2}\right],$$
(differentiate to verify; $t=\tan\frac{\phi'-\phi}2$ substitution). Evaluate
between the jump points $\phi'=\pm\pi/2$ for the two halves and combine the
four arctangents with the addition law
$\arctan u-\arctan v=\arctan\frac{u-v}{1+uv}$; after the trigonometric dust
settles (the $\tan\frac{\pm\pi/2-\phi}2$ pairs combine to
$2(\rho/b)\cos\phi/(1-\rho^2/b^2)$) one lands exactly on the boxed (3.131).
The module takes the complementary route: it *verifies* the identity by
high-accuracy quadrature of the Poisson integral against the closed form —
and P29 gets (3.131) a third way, by summing the Fourier series, so the three
derivations (series, Green function, complex sum) triangulate the result.

### P29.  Exercise 3.9.3 — Summing the split-cylinder series  *(Wilcox 2e §3.13, p.132)*
Fill in the derivation of (3.131) by summing the series (3.130). Hint: set
$Z=(\rho/b)e^{i(\phi-\pi/2)}$ and note
$(\rho/b)^{2n+1}\sin[(2n+1)(\phi-\pi/2)]={\rm Im}\,Z^{2n+1}$.
*Answer:* $\displaystyle\sum_{n\ge0}\frac{Z^{2n+1}}{2n+1}={\rm arctanh}\,Z
=\tfrac12\ln\frac{1+Z}{1-Z}$, whose imaginary part gives
$\sum_{n\ge0}\frac{t^{2n+1}\sin[(2n+1)\psi]}{2n+1}
=\tfrac12\arctan\frac{2t\sin\psi}{1-t^2}$; with $\psi=\phi-\pi/2$ this turns
(3.130) into (3.131). On the symmetry axis $\phi=0$ the closed form collapses
to $\frac{V_1+V_2}2+\frac{2(V_1-V_2)}{\pi}\arctan\frac{\rho}{b}$.
*Check:* the lemma on random $(t,\psi)$ to $10^{-10}$; series (3.130) $=$
closed form (3.131); the axis double-angle collapse (`test_p29_sum_the_series`).

**Solution.** Term by term, for $|Z|<1$,
$$\sum_{n=0}^{\infty}\frac{Z^{2n+1}}{2n+1}
=\frac12\left[\sum_{k\ge1}\frac{Z^k}{k}-\sum_{k\ge1}\frac{(-Z)^k}{k}\right]
=\frac12\left[-\ln(1-Z)+\ln(1+Z)\right]=\frac12\ln\frac{1+Z}{1-Z}.$$
Take the imaginary part with $Z=te^{i\psi}$:
$${\rm Im}\,\frac12\ln\frac{1+Z}{1-Z}=\frac12\arg\frac{1+Z}{1-Z},\qquad
\frac{1+Z}{1-Z}=\frac{(1+Z)(1-\bar Z)}{|1-Z|^2}
=\frac{1-t^2+2it\sin\psi}{|1-Z|^2},$$
so the argument is $\arctan\bigl[2t\sin\psi/(1-t^2)\bigr]$ (the real part
$1-t^2>0$ keeps the principal branch honest for $t<1$). Now insert
$t=\rho/b$, $\psi=\phi-\pi/2$, $\sin\psi=-\cos\phi$ into (3.130):
$$\Phi=\frac{V_1+V_2}2-\frac{2(V_1-V_2)}{\pi}\cdot
\frac12\arctan\frac{-2t\cos\phi}{1-t^2}
=\frac{V_1+V_2}2+\frac{V_1-V_2}{\pi}\arctan\frac{2t\cos\phi}{1-t^2},$$
which is (3.131). On the symmetry axis ($\phi=0$, toward the $V_1$ half) the
double-angle identity $\arctan\frac{2t}{1-t^2}=2\arctan t$ ($t<1$) collapses
it further to
$$\Phi(\rho,0)=\frac{V_1+V_2}{2}+\frac{2(V_1-V_2)}{\pi}\arctan\frac{\rho}{b},$$
a clean arctangent ramp from the mean at the center to $V_1$ at the wall —
the form the code checks the series against point by point.

### P30.  Exercise 3.9.4 — Split cylinder: the exterior solution  *(Wilcox 2e §3.13, p.132)*
(a) By Fourier methods, find $\Phi_{\rm out}(\rho,\phi)$ for the split
cylinder in the exterior region $\rho>b$. (b) Produce a closed form (by
summing as in P29 or otherwise). Given the interior and exterior series, how
does one map one onto the other?
*Answer:* (a) replace $(\rho/b)^{2n+1}\to(b/\rho)^{2n+1}$ in (3.130);
(b) $$\Phi_{\rm out}=\frac{V_1+V_2}{2}+\frac{V_1-V_2}{\pi}
\arctan\!\left[\frac{2(b/\rho)\cos\phi}{1-(b/\rho)^2}\right]
=\Phi_{\rm in}\!\left(\frac{b^2}{\rho},\phi\right)$$
— the interior solution evaluated at the inversion point: swap
$\rho/b\leftrightarrow b/\rho$.
*Check:* exterior series $=$ closed form; the $\rho\to b^2/\rho$ identity to
$10^{-12}$; $\rho\to\infty$ average; boundary values recovered
(`test_p30_exterior_halves`).

**Solution.** (a) Outside, regularity at infinity replaces regularity at the
axis: from (3.118) keep the constant and the $\rho^{-n}$ terms (the $\ln\rho$
term is absent because the cylinder carries zero *net* line charge — the
potential must stay bounded). The boundary matching at $\rho=b$ is the same
Fourier computation as the interior one — identical coefficients — so every
$(\rho/b)^{2n+1}$ simply becomes $(b/\rho)^{2n+1}$:
$$\Phi_{\rm out}=\frac{V_1+V_2}2-\frac{2(V_1-V_2)}{\pi}\sum_{n\ge0}
\Bigl(\frac b\rho\Bigr)^{2n+1}\frac{\sin[(2n+1)(\phi-\pi/2)]}{2n+1}.$$
(b) The P29 lemma applies verbatim with $t=b/\rho<1$, giving the boxed
arctangent. The structural answer to the last question: interior and exterior
are exchanged by the *inversion* $\rho\mapsto b^2/\rho$ — in 2-D, inversion
maps harmonic functions to harmonic functions with **no** radial prefactor
(unlike the 3-D Kelvin transform's $a/r$ weight), because
$w\mapsto b^2/\bar w$… more plainly, $b^2/z$ is analytic (P33) and harmonicity
is conformally invariant. Both series are the same function of the variable
$t=\min(\rho,b^2/\rho)/b$; the boundary data (and the $\rho$-independent
average $\tfrac{V_1+V_2}2$ at the two extremes $\rho\to0,\infty$) match
automatically. P33 rederives exactly this by the conformal map $w=b^2/z$.

### P31.  Exercise 3.9.5 — Summing the delta-data series  *(Wilcox 2e §3.13, p.132)*
The point-surface-potential series of P25 can be summed in closed form. Do so
(and compare with the expected P27 answer).
*Answer:*
$$\Phi(\rho,\phi)=\frac{V_0}{2\pi}\,
\frac{b^2-\rho^2}{\rho^2+b^2-2b\rho\cos\phi}$$
— i.e. $V_0$ times the Poisson kernel: the P25 series *is* the P27 integral
with $\Phi(b,\phi')=V_0\delta(\phi')$.
*Check:* $\tfrac12+\sum t^m\cos m\phi=\tfrac12(1-t^2)/(1+t^2-2t\cos\phi)$ on
random inputs to $10^{-10}$; P25 partial sums vs this closed form
(`test_p31_sum_delta_series`, `test_p25_cylinder_delta_series`).

**Solution.** With $t=\rho/b$, sum the geometric cosine series through
$W=te^{i\phi}$:
$$\sum_{m=1}^\infty t^m\cos m\phi={\rm Re}\sum_{m\ge1}W^m
={\rm Re}\,\frac{W}{1-W}=\frac{t\cos\phi-t^2}{1-2t\cos\phi+t^2}.$$
Then
$$\frac{\Phi}{V_0/\pi}=\frac12+\sum_mt^m\cos m\phi
=\frac{(1-2t\cos\phi+t^2)+2t\cos\phi-2t^2}{2(1-2t\cos\phi+t^2)}
=\frac{1-t^2}{2\,(1-2t\cos\phi+t^2)},$$
so $\Phi=\frac{V_0}{2\pi}\frac{1-t^2}{1-2t\cos\phi+t^2}$, and multiplying
numerator and denominator by $b^2$ gives the boxed form. Consistency with
P27 is immediate: putting $\Phi(b,\phi')=V_0\,\delta(\phi')$ under Poisson's
integral just evaluates the kernel at $\phi'=0$. So the three objects — the
separation-of-variables series (P25), the Green-function kernel (P27), and
this closed form — are one function; the delta-data problem is the cylinder's
own Green identity read backwards (the kernel is the boundary "response
function"). This is also the generating identity behind P29: integrating the
present formula over half the circle reproduces the split-cylinder
arctangent.

### P32.  Exercise 3.11.1 — Conformal map of the box onto a half-annulus  *(Wilcox 2e §3.13, pp.132–133; adapted by the book from Brown & Churchill)*
The P18 box problem is mapped to the region between two concentric
semicircles (the book's Fig. 3.27); every boundary is at zero potential
except the segment $v=0$, $-r_0<u<-1$, which is at $V$.
(a) Show $w=e^{\pi z/b}$ maps the P18 geometry and boundary data onto that
region. (b) Deduce that the potential in the half-annulus is (with $m=2n-1$)
$$\Phi(r,\theta)=\frac{4V}{\pi}\sum_{n=1}^{\infty}\frac1m\,
\frac{\sinh\!\bigl(\tfrac{m\pi\theta}{\ln r_0}\bigr)}{\sinh\!\bigl(\tfrac{m\pi^2}{\ln r_0}\bigr)}\,
\sin\!\Bigl(\tfrac{m\pi\ln r}{\ln r_0}\Bigr),$$
$(r,\theta)$ polar coordinates in the $w$-plane.
*Answer:* the map sends $x=0\to$ unit semicircle, $x=a\to$ radius-$r_0$
semicircle ($r_0=e^{\pi a/b}$), $y=0\to(1,r_0)$, and the $V$-side $y=b\to(-r_0,-1)$;
pulling P18 back through $x=\frac b\pi\ln r$, $y=\frac b\pi\theta$ gives the
series.
*Check:* Cauchy–Riemann residual numerically zero and $f'\neq0$ at interior
points; all four boundary images verified; the half-annulus series equals
the box series under the substitution to $10^{-9}$; polar-Laplacian
$\approx0$; boundary data reproduced (`test_p32_map_and_boundaries`,
`test_p32_semicircle_potential`).

**Solution.** (a) Write $w=e^{\pi z/b}$, $z=x+iy$: then $|w|=e^{\pi x/b}$ and
$\arg w=\pi y/b$. The box $0<x<a$, $0<y<b$ therefore maps to
$1<|w|<e^{\pi a/b}\equiv r_0$, $0<\arg w<\pi$: the upper half-annulus. The
exponential is entire with $f'=\frac\pi be^{\pi z/b}\neq0$, so the map is
conformal on the closed box, and the conformal-mapping theorem (§3.11: pulled
back through an analytic map, constant-Dirichlet data stays constant-Dirichlet)
transfers the boundary values piece by piece:
$x=0$ (grounded) $\to$ the inner arc $|w|=1$; $x=a$ (grounded) $\to$ the outer
arc $|w|=r_0$; $y=0$ (grounded) $\to$ $\arg w=0$, the segment $(1,r_0)$; and
the charged side $y=b$ ($\Phi=V$) $\to$ $\arg w=\pi$, i.e. $v=0$ with
$-r_0<u<-1$ — exactly the advertised layout.
(b) Solving in the $w$-plane is *not* necessary — invert the map. A point
$(r,\theta)$ in the half-annulus pulls back to
$$x=\frac{b}{\pi}\ln r\in(0,a),\qquad y=\frac{b}{\pi}\theta\in(0,b),$$
and harmonicity survives the pullback, so $\Phi_{\rm ann}(r,\theta)=
\Phi_{\rm box}(x,y)$ with P18's series. Substituting (and using
$a=\frac b\pi\ln r_0$):
$$\frac{m\pi x}{a}=\frac{m\pi\ln r}{\ln r_0},\qquad
\frac{m\pi y}{a}=\frac{m\pi\theta}{\ln r_0},\qquad
\frac{m\pi b}{a}=\frac{m\pi^2}{\ln r_0},$$
which turns the box series exactly into the quoted half-annulus series. Note
the effective coordinates: $\ln r$ and $\theta$ are the real and imaginary
parts of $\log w$ — the map's inverse — so the "curvilinear rectangle"
$(\ln r,\theta)$ is the box again; conformal mapping never did anything but
relabel the harmonics (`~MA-06`). The code verifies the map numerically
(Cauchy–Riemann residuals at interior points, boundary tracing of all four
sides) and the potential identity on random interior points.

### P33.  Exercise 3.11.2 — Exterior of the split cylinder by inversion  *(Wilcox 2e §3.13, p.133)*
Using the conformal map $w=b^2/z$, obtain the exterior potential
$\Phi_{\rm out}(\rho,\phi)$ of the split cylinder of §3.9 from the interior
solution (3.131).
*Answer:* $w=b^2/z$ maps $\rho>b$ onto $\rho_w<b$ (boundary to boundary,
$\phi_w=-\phi$), and since (3.131) is even in $\phi$,
$$\Phi_{\rm out}(\rho,\phi)=\Phi_{\rm in}\Bigl(\frac{b^2}{\rho},\phi\Bigr)
=\frac{V_1+V_2}{2}+\frac{V_1-V_2}{\pi}
\arctan\!\left[\frac{2(b/\rho)\cos\phi}{1-(b/\rho)^2}\right],$$
in agreement with P30.
*Check:* pullback equals the P30 closed form to $10^{-12}$; harmonic outside;
Cauchy–Riemann residual of $b^2/z$ numerically zero
(`test_p33_inversion_map`).

**Solution.** $f(z)=b^2/z$ is analytic for $z\neq0$ with
$f'=-b^2/z^2\neq0$, hence conformal on the exterior $\rho>b$ (the puncture at
$\infty$ maps to the regular point $w=0$). Writing $z=\rho e^{i\phi}$:
$$w=\frac{b^2}{\rho}\,e^{-i\phi}\;\Longrightarrow\;
\rho_w=\frac{b^2}{\rho}<b,\qquad \phi_w=-\phi,$$
so the exterior maps onto the punctured interior disk, and the circle
$\rho=b$ maps onto itself with $\phi\to-\phi$. Crucially the boundary *data*
survive: reflection $\phi\to-\phi$ maps the right half-cylinder to itself and
the left to itself ($\cos\phi$ even), so the $V_1/V_2$ split is preserved.
By the conformal-mapping theorem, $H(z)\equiv\Phi_{\rm in}(w(z))$ is harmonic
in $\rho>b$ and takes the correct boundary values; it is also bounded at
infinity ($w\to0$ gives the average $\tfrac{V_1+V_2}2$ — the right physical
limit for a neutral boundary). Uniqueness (bounded exterior Dirichlet
problem) then forces $\Phi_{\rm out}=H$:
$$\Phi_{\rm out}(\rho,\phi)
=\frac{V_1+V_2}{2}+\frac{V_1-V_2}{\pi}
\arctan\!\left[\frac{2(b/\rho)\cos(-\phi)}{1-(b/\rho)^2}\right],$$
and $\cos(-\phi)=\cos\phi$ gives the stated form — precisely P30's closed
form, now obtained in three lines. The inversion trick is the 2-D
image-in-a-circle statement one level up: P14's image point $a^2/\rho'$ *is*
$w=a^2/z$ acting on the source.
