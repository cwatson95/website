# MACRO_EM-01 — Problems (all exercises of Wilcox Ch. 1 + Appendix A)

Every exercise of §1.7 (printed pp.21–22) and §A.1 (printed p.862), statements
condensed from the PDF with all given equations kept, then solved **step by
step** and machine-checked by `code/test_intro_perspectives.py`. **Gaussian
units** throughout: Maxwell's equations as in Table 1.1 (p.2), Lorentz force
$\vec F=q(\vec E+\frac{\vec v}{c}\times\vec B)$. Identities cited as
"(glossary, p.23/24/25)" are the §1.8 list — see `../notes.md` §7.

---

### P1.  Exercise 1.1.1 — three vector/Laplacian identities  *(Wilcox 2e §1.7, p.21)*

Verify explicitly:

**(a)** $\ \vec A\times(\vec B\times\vec C)+\vec B\times(\vec C\times\vec A)+\vec C\times(\vec A\times\vec B)=0.$

**(b)** $\ \nabla^2(\phi\psi)=\phi\nabla^2\psi+\psi\nabla^2\phi+2\vec\nabla\phi\cdot\vec\nabla\psi.$

**(c)** $\ \displaystyle\sum_i A_i\vec\nabla B_i=\vec\nabla(\vec A\cdot\vec B)-(\vec B\cdot\vec\nabla)\vec A-\vec B\times(\vec\nabla\times\vec A).$

*Answer:* all three hold identically — (a) is the Jacobi identity (three
BAC-CABs cancel in pairs), (b) is the Leibniz rule applied twice, (c) follows
from one ε–δ contraction.
*Check:* `test_bac_cab_and_jacobi` (500 random triples, residual $\sim10^{-16}$);
`test_laplacian_product_poly/_trig` and `test_grad_dot_expansion_poly/_trig`
(4th-order FD on polynomial fields — exact to rounding — and on trig fields).

**Solution.**

**(a)** The tool is the BAC-CAB rule (glossary, p.23),
$$\vec A\times(\vec B\times\vec C)=\vec B(\vec A\cdot\vec C)-\vec C(\vec A\cdot\vec B),$$
itself provable by one index computation: with
$[\vec B\times\vec C]_k=\epsilon_{klm}B_lC_m$,
$$[\vec A\times(\vec B\times\vec C)]_i=\epsilon_{ijk}A_j\epsilon_{klm}B_lC_m
=(\delta_{il}\delta_{jm}-\delta_{im}\delta_{jl})A_jB_lC_m
=B_i(A_mC_m)-C_i(A_lB_l),$$
using $\epsilon_{ijk}\epsilon_{klm}=\epsilon_{kij}\epsilon_{klm}=\delta_{il}\delta_{jm}-\delta_{im}\delta_{jl}$
(ε–δ identity, glossary p.24). Now write BAC-CAB three times, cycling
$\vec A\to\vec B\to\vec C\to\vec A$:
$$\vec A\times(\vec B\times\vec C)=\vec B(\vec A\cdot\vec C)-\vec C(\vec A\cdot\vec B),$$
$$\vec B\times(\vec C\times\vec A)=\vec C(\vec B\cdot\vec A)-\vec A(\vec B\cdot\vec C),$$
$$\vec C\times(\vec A\times\vec B)=\vec A(\vec C\cdot\vec B)-\vec B(\vec C\cdot\vec A).$$
Add: the $\vec B$-terms cancel ($\vec B(\vec A\cdot\vec C)-\vec B(\vec C\cdot\vec A)=0$,
dot products commute), likewise the $\vec C$-terms and the $\vec A$-terms.
Sum $=0$. $\blacksquare$ (This is the Jacobi identity: the cross product, like
a commutator or Poisson bracket, is an — anticommutative, non-associative —
Lie bracket.)

**(b)** Work in components, $\nabla^2=\sum_i\partial_i\partial_i$, and apply the
Leibniz rule twice:
$$\partial_i(\phi\psi)=\psi\,\partial_i\phi+\phi\,\partial_i\psi,$$
$$\partial_i\partial_i(\phi\psi)=\partial_i\!\left(\psi\,\partial_i\phi\right)+\partial_i\!\left(\phi\,\partial_i\psi\right)
=(\partial_i\psi)(\partial_i\phi)+\psi\,\partial_i\partial_i\phi+(\partial_i\phi)(\partial_i\psi)+\phi\,\partial_i\partial_i\psi.$$
Summing over $i$ and collecting,
$$\nabla^2(\phi\psi)=\phi\nabla^2\psi+\psi\nabla^2\phi+2\vec\nabla\phi\cdot\vec\nabla\psi.\qquad\blacksquare$$

**(c)** Take the $j$-th component of each right-hand-side piece and reduce all
three to $\partial_j$'s and $\partial_i$'s:

1. $\bigl[\vec\nabla(\vec A\cdot\vec B)\bigr]_j=\partial_j(A_iB_i)=A_i\,\partial_jB_i+B_i\,\partial_jA_i$ (Leibniz).
2. $\bigl[(\vec B\cdot\vec\nabla)\vec A\bigr]_j=B_i\,\partial_iA_j$.
3. For the cross term, ε–δ again:
$$\bigl[\vec B\times(\vec\nabla\times\vec A)\bigr]_j=\epsilon_{jkl}B_k(\vec\nabla\times\vec A)_l
=\epsilon_{jkl}\epsilon_{lmn}B_k\,\partial_mA_n
=(\delta_{jm}\delta_{kn}-\delta_{jn}\delta_{km})B_k\,\partial_mA_n
=B_i\,\partial_jA_i-B_i\,\partial_iA_j.$$

Assemble the right side:
$$\underbrace{A_i\partial_jB_i+B_i\partial_jA_i}_{1.}
-\underbrace{B_i\partial_iA_j}_{2.}
-\underbrace{\bigl(B_i\partial_jA_i-B_i\partial_iA_j\bigr)}_{3.}
=A_i\,\partial_jB_i=\Bigl[\sum_iA_i\vec\nabla B_i\Bigr]_j.\qquad\blacksquare$$
(Symmetrizing this result under $\vec A\leftrightarrow\vec B$ and adding
reproduces the glossary's $\vec\nabla(\vec A\cdot\vec B)$ identity, p.24 —
a free consistency check.)

*Numerics.* (a) needs no calculus: 500 random triples give
$|\vec A\times(\vec B\times\vec C)+\text{cyc.}|\lesssim10^{-15}$. For (b) and
(c) the code differentiates *nothing by hand*: both sides are built from
5-point 4th-order finite-difference stencils. On fields polynomial of degree
$\le2$ per variable the stencils are exact, so the residuals are pure rounding
($\sim10^{-12}$); trig/exponential fields confirm generality at the stencil's
truncation level ($\sim10^{-8}$).

---

### P2.  Exercise 1.1.2 — potentials: two Maxwell equations become identities  *(Wilcox 2e §1.7, p.21)*

Given the definitions
$$\vec E\equiv-\vec\nabla\Phi-\frac1c\frac{\partial\vec A}{\partial t},\qquad
\vec B\equiv\vec\nabla\times\vec A,$$
with $\Phi$ the scalar and $\vec A$ the vector potential, show that two of the
Maxwell equations of Table 1.1 are satisfied identically, and that the other
two become coupled differential equations for $\Phi$ and $\vec A$; compute and
simplify those equations.

*Answer:* Faraday and no-monopole hold identically. Coulomb and
Ampère–Maxwell become
$$\nabla^2\Phi+\frac1c\frac{\partial}{\partial t}\bigl(\vec\nabla\cdot\vec A\bigr)=-4\pi\rho,\qquad
\nabla^2\vec A-\frac{1}{c^2}\frac{\partial^2\vec A}{\partial t^2}
-\vec\nabla\Bigl(\vec\nabla\cdot\vec A+\frac1c\frac{\partial\Phi}{\partial t}\Bigr)=-\frac{4\pi}{c}\vec J.$$
*Check:* `test_potentials_no_monopole_identity`, `test_potentials_faraday_identity`
(nested-FD residuals $\sim10^{-14}$ on polynomial potentials, and at the true
Gaussian $c$), `test_potentials_coulomb_pde`, `test_potentials_ampere_pde`
(LHS = RHS of each derived PDE, evaluated independently).

**Solution.**

**Step 1 — the two identities behind everything.** For any twice-differentiable
$\Phi$ and $\vec A$ (glossary, p.24):
$$\vec\nabla\times\vec\nabla\Phi=0:\quad
[\vec\nabla\times\vec\nabla\Phi]_i=\epsilon_{ijk}\partial_j\partial_k\Phi=0,$$
because $\partial_j\partial_k$ is symmetric in $(j,k)$ while $\epsilon_{ijk}$ is
antisymmetric — a symmetric–antisymmetric contraction vanishes. Identically,
$$\vec\nabla\cdot(\vec\nabla\times\vec A)=\partial_i\epsilon_{ijk}\partial_jA_k=\epsilon_{ijk}\partial_i\partial_jA_k=0.$$

**Step 2 — no-monopole is automatic.** Substituting $\vec B=\vec\nabla\times\vec A$,
$$\vec\nabla\cdot\vec B=\vec\nabla\cdot(\vec\nabla\times\vec A)=0$$
by Step 1 — for *every* $\vec A$, with no condition imposed. Identity #1. ✔

**Step 3 — Faraday is automatic.** Substituting both definitions and commuting
$\partial_t$ with spatial curls (fields are smooth),
$$\vec\nabla\times\vec E+\frac1c\frac{\partial\vec B}{\partial t}
=-\underbrace{\vec\nabla\times\vec\nabla\Phi}_{=0}-\frac1c\frac{\partial}{\partial t}(\vec\nabla\times\vec A)
+\frac1c\frac{\partial}{\partial t}(\vec\nabla\times\vec A)=0 .$$
Identity #2. ✔ So the two *sourceless* equations of Table 1.1 are used up in
defining $(\Phi,\vec A)$ — exactly the four-equations-for-a-4-potential
counting of p.3.

**Step 4 — Coulomb becomes a PDE.** $\vec\nabla\cdot\vec E=4\pi\rho$ with the
definition of $\vec E$:
$$\vec\nabla\cdot\vec E=-\vec\nabla\cdot\vec\nabla\Phi-\frac1c\frac{\partial}{\partial t}(\vec\nabla\cdot\vec A)
=-\nabla^2\Phi-\frac1c\frac{\partial}{\partial t}(\vec\nabla\cdot\vec A)=4\pi\rho,$$
i.e.
$$\boxed{\ \nabla^2\Phi+\frac1c\frac{\partial}{\partial t}\bigl(\vec\nabla\cdot\vec A\bigr)=-4\pi\rho\ }.$$

**Step 5 — Ampère–Maxwell becomes a PDE.** Substitute both definitions into
$\vec\nabla\times\vec B-\frac1c\partial_t\vec E=\frac{4\pi}{c}\vec J$:
$$\vec\nabla\times(\vec\nabla\times\vec A)
-\frac1c\frac{\partial}{\partial t}\Bigl(-\vec\nabla\Phi-\frac1c\frac{\partial\vec A}{\partial t}\Bigr)=\frac{4\pi}{c}\vec J .$$
Expand the double curl with the glossary identity (p.24)
$\vec\nabla\times(\vec\nabla\times\vec A)=\vec\nabla(\vec\nabla\cdot\vec A)-\nabla^2\vec A$:
$$\vec\nabla(\vec\nabla\cdot\vec A)-\nabla^2\vec A
+\frac1c\vec\nabla\frac{\partial\Phi}{\partial t}+\frac{1}{c^2}\frac{\partial^2\vec A}{\partial t^2}=\frac{4\pi}{c}\vec J .$$

**Step 6 — simplify by grouping the gradient terms.** The first and third terms
are both gradients; pull them into one:
$$\boxed{\ \nabla^2\vec A-\frac{1}{c^2}\frac{\partial^2\vec A}{\partial t^2}
-\vec\nabla\Bigl(\vec\nabla\cdot\vec A+\frac1c\frac{\partial\Phi}{\partial t}\Bigr)
=-\frac{4\pi}{c}\vec J\ }.$$
Together with Step 4 this is the promised *coupled* pair: $\Phi$'s equation
contains $\vec\nabla\cdot\vec A$, and $\vec A$'s equation contains
$\partial_t\Phi$. $\blacksquare$

*Remark (why "coupled" is not forever).* The potentials are not unique
($\Phi\to\Phi-\frac1c\partial_t\chi$, $\vec A\to\vec A+\vec\nabla\chi$ leaves
$\vec E,\vec B$ untouched, by Step 1's identities); choosing $\chi$ so that
$\vec\nabla\cdot\vec A+\frac1c\partial_t\Phi=0$ decouples the pair into two
wave equations $\bigl(\nabla^2-\frac{1}{c^2}\partial_t^2\bigr)(\Phi,\vec A)=
-(4\pi\rho,\frac{4\pi}{c}\vec J)$ — the book develops this in the
time-varying-fields chapters; here only the *coupled* form is asked for.

*Numerics.* The code takes concrete low-degree polynomial potentials
$\Phi(\vec r,t)$, $\vec A(\vec r,t)$, builds $\vec E,\vec B$ by finite
differences, and (i) confirms $\vec\nabla\cdot\vec B$ and
$\vec\nabla\times\vec E+\frac1c\partial_t\vec B$ vanish to rounding at random
space–time points — for the toy $c=2$ *and* for
$c=2.9979\times10^{10}$ cm/s — and (ii) evaluates
$\vec\nabla\cdot\vec E$ against $-\nabla^2\Phi-\frac1c\partial_t(\vec\nabla\cdot\vec A)$
and $\vec\nabla\times\vec B-\frac1c\partial_t\vec E$ against
$-$[LHS of Step 6] independently, confirming the simplification algebra.

---

### P3.  Exercise 1.1.3 — charge conservation for a rigidly moving blob  *(Wilcox 2e §1.7, p.21)*

For charge and current densities of the form
$$\rho(\vec r,t)=e\,f\bigl(\vec r-\vec R(t)\bigr),\qquad
\vec J(\vec r,t)=e\,\frac{d\vec R}{dt}\,f\bigl(\vec r-\vec R(t)\bigr),$$
with $f(\cdots)$ an arbitrary (differentiable) function, verify charge
conservation:
$$\frac{\partial\rho(\vec r,t)}{\partial t}+\vec\nabla\cdot\vec J(\vec r,t)=0 .$$

*Answer:* the two terms are $\mp\,e\,\dot{\vec R}\cdot(\vec\nabla f)$ and cancel
exactly, for any profile $f$ and any trajectory $\vec R(t)$.
*Check:* `test_continuity_moving_blob` and `test_continuity_second_trajectory`
— Gaussian blob on the curved trajectories $\vec R=(\cos t,\sin 2t,0.3t)$ and
$\vec R=(t^2,-t,\sin t)$; $\partial_t\rho$ and $\vec\nabla\cdot\vec J$ built by
finite differences (nothing cancels symbolically), residual $\lesssim10^{-9}$
against term size $\sim1$.

**Solution.**

**Step 1 — the time derivative, by the chain rule.** Write
$\vec u\equiv\vec r-\vec R(t)$, so $\rho=e f(\vec u)$ with
$\partial u_i/\partial t=-\dot R_i(t)$. Then
$$\frac{\partial\rho}{\partial t}
=e\sum_i\frac{\partial f}{\partial u_i}\frac{\partial u_i}{\partial t}
=-e\sum_i\dot R_i\,\frac{\partial f}{\partial u_i}
=-e\,\dot{\vec R}\cdot(\vec\nabla f)\bigl(\vec r-\vec R(t)\bigr),$$
where $(\vec\nabla f)(\vec r-\vec R)$ means the gradient of $f$ evaluated at
the shifted argument; note $\partial f(\vec r-\vec R)/\partial x_i=
(\partial f/\partial u_i)$ since $\partial u_j/\partial x_i=\delta_{ij}$.

**Step 2 — the divergence.** $\dot{\vec R}(t)$ depends on $t$ only, so it
passes through the spatial derivatives (glossary $\vec\nabla\cdot(\phi\vec A)$
identity with $\vec A=\dot{\vec R}$ constant in $\vec r$):
$$\vec\nabla\cdot\vec J
=e\,\vec\nabla\cdot\bigl(\dot{\vec R}\,f(\vec r-\vec R)\bigr)
=e\sum_i\dot R_i\,\frac{\partial}{\partial x_i}f(\vec r-\vec R)
=+\,e\,\dot{\vec R}\cdot(\vec\nabla f)\bigl(\vec r-\vec R(t)\bigr).$$

**Step 3 — add.**
$$\frac{\partial\rho}{\partial t}+\vec\nabla\cdot\vec J
=-e\,\dot{\vec R}\cdot\vec\nabla f+e\,\dot{\vec R}\cdot\vec\nabla f=0 .\qquad\blacksquare$$

*Remark.* Physically: the blob translates rigidly with velocity
$\dot{\vec R}$, so the current is purely convective,
$\vec J=\rho\,\dot{\vec R}/\,$(per unit charge)$\,=\rho\vec v$, and a rigid
translation conserves the charge in every co-moving volume. The limit
$f\to\delta^3$ (`~MA-15`) makes this the point charge of §1.2 with
$\vec J=e\dot{\vec R}\,\delta^3(\vec r-\vec R)$ — continuity is what makes the
point-charge idealization consistent with Maxwell's equations, which *imply*
Eq. (1.2) (notes §2; WT pp.3–4).

*Numerics.* $f$ = unit-width Gaussian, $e=1.3$: at 40 random $(\vec r,t)$ the
FD-computed $\partial_t\rho+\vec\nabla\cdot\vec J$ is $\lesssim10^{-9}$ while
each term separately is $O(1)$ — the cancellation is real, not small terms.

---

### P4.  Exercise 1.4.1 — $\oint\vec v\cdot d\vec\ell=2A$ and the area of an ellipse  *(Wilcox 2e §1.7, pp.21–22)*

**(a)** A planar surface $S$ of area $A$ with boundary $C$ lies in the
$xy$-plane. For the coplanar vector field
$$\vec v=-y\,\hat i+x\,\hat j,$$
prove that
$$\oint_C\vec v\cdot d\vec\ell=\oint_C(\hat i\,dx+\hat j\,dy)\cdot\vec v=2A .$$
**(b)** Using the ellipse $\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1$ and part (a),
find the area of the ellipse. *(The book credits the problem as adapted from
B. DiBartolo, Classical Theory of Electromagnetism, 2nd edn., Ex. 1.14.)*

*Answer:* (a) $\vec\nabla\times\vec v=2\hat z$, so Stokes gives $2A$ for *any*
planar contour; (b) $A_{\rm ellipse}=\pi ab$.
*Check:* `test_circulation_circle` ($2\pi r^2$ for circles),
`test_ellipse_area` ($\pi ab$ by quadrature, several $(a,b)$),
`test_star_curve_area` (the same functional on $r(\theta)=1+0.3\cos3\theta$
reproduces $\tfrac12\oint r^2d\theta=\pi(1+0.045)$ — "any $C$", not just
ellipses).

**Solution.**

**(a) Step 1 — the curl is constant.** With $v_x=-y,\ v_y=x,\ v_z=0$
(rectangular curl, glossary p.25):
$$\vec\nabla\times\vec v
=\Bigl(\frac{\partial v_z}{\partial y}-\frac{\partial v_y}{\partial z}\Bigr)\hat i
+\Bigl(\frac{\partial v_x}{\partial z}-\frac{\partial v_z}{\partial x}\Bigr)\hat j
+\Bigl(\frac{\partial v_y}{\partial x}-\frac{\partial v_x}{\partial y}\Bigr)\hat k
=\bigl(1-(-1)\bigr)\hat k=2\hat k .$$

**Step 2 — Stokes' theorem (Eq. 1.10, p.9).** Take $S$ itself as the open
surface spanning $C$; for a counterclockwise $C$ (right-hand rule) the normal
is $\hat n=\hat k$:
$$\oint_C\vec v\cdot d\vec\ell
=\int_Sda\,(\vec\nabla\times\vec v)\cdot\hat n
=\int_Sda\,(2\hat k)\cdot\hat k
=2\int_Sda=2A .\qquad\blacksquare$$
Since $d\vec\ell=\hat i\,dx+\hat j\,dy$ in the plane, the middle expression of
the problem statement is the same integral written out,
$\oint_C(-y\,dx+x\,dy)$. (Clockwise orientation flips the sign: $-2A$.
Equivalently, without Stokes: Green's theorem with $P=-y$, $Q=x$ gives
$\oint(P\,dx+Q\,dy)=\iint(\partial_xQ-\partial_yP)\,dA=2A$ — the 2-D Stokes
theorem of Eq. (1.38) that P7b will show is also 2-D Gauss.)

**(b) Step 1 — parameterize the ellipse** counterclockwise by
$$x=a\cos\theta,\qquad y=b\sin\theta,\qquad\theta:0\to2\pi,$$
which satisfies $x^2/a^2+y^2/b^2=\cos^2\theta+\sin^2\theta=1$. Then
$$dx=-a\sin\theta\,d\theta,\qquad dy=b\cos\theta\,d\theta .$$

**Step 2 — evaluate the circulation.**
$$\oint_C(-y\,dx+x\,dy)
=\int_0^{2\pi}\bigl[(-b\sin\theta)(-a\sin\theta)+(a\cos\theta)(b\cos\theta)\bigr]d\theta
=ab\int_0^{2\pi}(\sin^2\theta+\cos^2\theta)\,d\theta=2\pi ab .$$

**Step 3 — apply (a).** $2A=2\pi ab$, so
$$\boxed{\ A_{\rm ellipse}=\pi ab\ }$$
(circle check: $a=b=r$ gives $\pi r^2$). $\blacksquare$

*Numerics.* Periodic trapezoid quadrature (spectrally accurate) of
$\oint\vec v\cdot d\vec\ell$: circles $r=0.7,1,2.5$ give $2\pi r^2$ to
$10^{-12}$; ellipses $(a,b)=(3,1.5),(2,0.4)$ give $2\pi ab$; the star contour
$r(\theta)=1+0.3\cos3\theta$ gives $2\times\pi(1+0.3^2/2)$, confirming the
result holds for an arbitrary planar boundary.

---

### P5.  Exercise 1.4.2 — two more faces of Gauss' theorem  *(Wilcox 2e §1.7, p.22)*

Show that the following are equivalent expressions of Gauss' theorem:
$$\textbf{(a)}\quad\int_Vd^3x\,\vec\nabla\varphi=\oint_Sda\,\hat n\,\varphi,\qquad\qquad
\textbf{(b)}\quad\int_Vd^3x\,\vec\nabla\times\vec A=\oint_Sda\,\hat n\times\vec A .$$

*Answer:* both follow from the divergence theorem (Eq. 1.9) applied to the
auxiliary fields $\varphi\,\vec c$ and $\vec A\times\vec c$ with $\vec c$ an
arbitrary *constant* vector, then stripping $\vec c$; conversely (a) with
$\varphi\to A_i$ per component rebuilds the divergence theorem, so all three
statements are equivalent.
*Check:* `test_gradient_theorem_box`, `test_curl_volume_theorem_box` —
Gauss–Legendre quadrature of both sides (volume vs six faces of a box) for
trig/polynomial fields; agreement $\sim10^{-10}$ componentwise.

**Solution.**

**(a) Step 1 — auxiliary field.** Let $\vec c$ be constant and set
$\vec F=\varphi\,\vec c$. The glossary product rule (p.24) with
$\vec\nabla\cdot\vec c=0$:
$$\vec\nabla\cdot\vec F=\vec\nabla\cdot(\varphi\,\vec c)
=\vec c\cdot\vec\nabla\varphi+\varphi\,\underbrace{\vec\nabla\cdot\vec c}_{=0}
=\vec c\cdot\vec\nabla\varphi .$$

**Step 2 — divergence theorem on $\vec F$** (Eq. 1.9):
$$\int_Vd^3x\,\vec c\cdot\vec\nabla\varphi=\oint_Sda\,(\varphi\,\vec c)\cdot\hat n
=\vec c\cdot\oint_Sda\,\hat n\,\varphi .$$
Pull the constant $\vec c$ out of the volume integral too:
$$\vec c\cdot\Bigl[\int_Vd^3x\,\vec\nabla\varphi-\oint_Sda\,\hat n\,\varphi\Bigr]=0 .$$

**Step 3 — strip $\vec c$.** The bracket is a fixed vector and $\vec c$ is
arbitrary; choosing $\vec c=\hat i,\hat j,\hat k$ in turn kills each component,
so the bracket vanishes:
$$\int_Vd^3x\,\vec\nabla\varphi=\oint_Sda\,\hat n\,\varphi .\qquad\blacksquare$$

**(b) Step 1 — auxiliary field.** Set $\vec F=\vec A\times\vec c$, $\vec c$
constant. The glossary identity
$\vec\nabla\cdot(\vec A\times\vec B)=\vec B\cdot(\vec\nabla\times\vec A)-\vec A\cdot(\vec\nabla\times\vec B)$
with $\vec B=\vec c$ (so $\vec\nabla\times\vec c=0$):
$$\vec\nabla\cdot(\vec A\times\vec c)=\vec c\cdot(\vec\nabla\times\vec A).$$

**Step 2 — surface side.** The cyclic triple product (glossary p.23 / Eq. 1.27):
$$(\vec A\times\vec c)\cdot\hat n=\hat n\cdot(\vec A\times\vec c)
=\vec c\cdot(\hat n\times\vec A),$$
using $\vec a\cdot(\vec b\times\vec c\,')=\vec c\,'\cdot(\vec a\times\vec b)$
with $(\vec a,\vec b,\vec c\,')=(\hat n,\vec A,\vec c)$.

**Step 3 — divergence theorem and strip.**
$$\vec c\cdot\int_Vd^3x\,\vec\nabla\times\vec A
=\int_Vd^3x\,\vec\nabla\cdot(\vec A\times\vec c)
=\oint_Sda\,(\vec A\times\vec c)\cdot\hat n
=\vec c\cdot\oint_Sda\,\hat n\times\vec A,$$
for every constant $\vec c$, hence
$$\int_Vd^3x\,\vec\nabla\times\vec A=\oint_Sda\,\hat n\times\vec A .\qquad\blacksquare$$

**Equivalence, not just consequence.** Conversely, apply (a) to
$\varphi=A_x,A_y,A_z$ and take the $x$-, $y$-, $z$-components respectively:
summing $\partial_iA_i$ rebuilds $\int_V\vec\nabla\cdot\vec A=\oint_S da\,\hat n\cdot\vec A$.
So (a) ⇒ divergence theorem ⇒ (b), and each of the three implies the others:
they are one theorem in three costumes — "replace $\cdot$ by nothing or by
$\times$" (the general pattern: $\int_Vd^3x\,\vec\nabla\circ(\ )=\oint_Sda\,\hat n\circ(\ )$).

*Numerics.* Box $[-1,1.3]\times[-0.7,1.1]\times[-1.2,0.9]$ (asymmetric, no
accidental cancellations); $\varphi=\sin x\cos y+z^2 e^{x/3}$ and a mixed
trig/polynomial $\vec A$. Volume side: 3-D Gauss–Legendre ($24^3$ nodes) of the
FD gradient/curl; surface side: 2-D Gauss–Legendre on each of the six faces
with the exact outward $\hat n$. All three components match to $\sim10^{-10}$
(the residue is the FD truncation of the volume-side integrand, scaling as $h^4$).

---

### P6.  Exercise 1.4.3 — the surface-gradient face of Stokes' theorem  *(Wilcox 2e §1.7, p.22)*

Show that the following is an equivalent expression of Stokes' theorem:
$$\int_Sda\,\hat n\times\vec\nabla\varphi=\oint_Cd\vec\ell\,\varphi .$$

*Answer:* apply Stokes' theorem (Eq. 1.10) to $\vec A=\varphi\,\vec c$,
constant $\vec c$, use $\vec\nabla\times(\varphi\vec c)=\vec\nabla\varphi\times\vec c$
and the cyclic triple product, then strip $\vec c$; applying the result to
$\varphi\to A_i$ componentwise runs the argument backwards, so the two
statements are equivalent.
*Check:* `test_stokes_gradient_disc` (unit disc vs boundary circle, agreement
$\sim10^{-14}$) and `test_stokes_gradient_hemisphere_matches` (the *hemisphere*
spanning the same circle gives the same vector — surface-independence, the
Stokes hallmark).

**Solution.**

**Step 1 — auxiliary field.** $\vec A=\varphi\,\vec c$ with $\vec c$ constant.
Glossary curl product rule (p.24), $\vec\nabla\times\vec c=0$:
$$\vec\nabla\times(\varphi\,\vec c)=\vec\nabla\varphi\times\vec c+\varphi\,\underbrace{\vec\nabla\times\vec c}_{=0}
=\vec\nabla\varphi\times\vec c .$$

**Step 2 — Stokes' theorem on $\vec A$** (Eq. 1.10):
$$\int_Sda\,(\vec\nabla\varphi\times\vec c)\cdot\hat n=\oint_Cd\vec\ell\cdot(\varphi\,\vec c)
=\vec c\cdot\oint_Cd\vec\ell\,\varphi .$$

**Step 3 — cycle the triple product on the left.**
$(\vec\nabla\varphi\times\vec c)\cdot\hat n=\vec c\cdot(\hat n\times\vec\nabla\varphi)$
— same cyclic identity as P5b Step 2, with
$(\vec a,\vec b,\vec c\,')=(\hat n,\vec\nabla\varphi,\vec c)$. Hence
$$\vec c\cdot\Bigl[\int_Sda\,\hat n\times\vec\nabla\varphi-\oint_Cd\vec\ell\,\varphi\Bigr]=0
\quad\text{for all constant }\vec c,$$
and stripping $\vec c$ (components $\hat i,\hat j,\hat k$) gives the result.
$\blacksquare$

**Equivalence.** Conversely, assume the new identity for all scalars and run
Steps 1–3 backwards: dot it with a constant $\vec c$,
$$\vec c\cdot\int_Sda\,\hat n\times\vec\nabla\varphi
=\int_Sda\,(\vec\nabla\varphi\times\vec c)\cdot\hat n
=\int_Sda\,\bigl(\vec\nabla\times(\varphi\vec c)\bigr)\cdot\hat n,
\qquad
\vec c\cdot\oint_Cd\vec\ell\,\varphi=\oint_Cd\vec\ell\cdot(\varphi\vec c),$$
which is Stokes' theorem for the field $\varphi\,\vec c$; sums of such fields
($\vec A=\sum_iA_i\hat e_i$ with $\varphi=A_i$, $\vec c=\hat e_i$) span all
vector fields, and Stokes' theorem is linear in the field — so the identity
implies Stokes in full. The book's "equivalent expression" is this two-way
derivability.

*Remark (orientation and surface-independence).* $(\hat n,d\vec\ell)$ are
right-hand related as in Fig. 1.1(b) (p.9). Nothing in Steps 1–3 used *which*
surface spans $C$: any $S$ with $\partial S=C$ gives the same left side — the
numerics check exactly that with a flat disc and a hemisphere. Note also the
component count: for $S$ = unit disc in the $z=0$ plane, $\hat n=\hat z$ makes
the left side's $z$-component vanish pointwise, while on the hemisphere it
vanishes only after integration — a nontrivial internal check.

*Numerics.* $\varphi=x^2y-3z+\cos y$ with hand-coded $\vec\nabla\varphi$
(itself validated against FD): polar Gauss–Legendre × trapezoid over the unit
disc, and $(\theta,\phi)$ quadrature over the unit upper hemisphere, both equal
the boundary integral $\oint d\vec\ell\,\varphi$ (trapezoid on the unit circle)
to $\sim10^{-14}$, componentwise.

---

### P7.  Exercise 1.5.1 — the 2-D point charge, and 2-D Gauss ⇔ Stokes  *(Wilcox 2e §1.7, p.22)*

**(a)** Use Gauss' theorem to derive the radial dependence of the electric
field of a point charge $q$ in two dimensions.
**(b)** Show that in two dimensions Gauss' theorem and Stokes' theorem are
equivalent.

*Answer:* (a) $\vec E=\dfrac{2q}{\rho}\hat\rho$ — the flux
$\oint\vec E\cdot\hat n\,d\ell$ through any enclosing contour is $4\pi q$
(Table 1.5 normalization $\vec\nabla\cdot\vec E=4\pi\sigma$, vacuum), and
symmetry puts all of it on $2\pi\rho\,E(\rho)$; the field falls as $1/\rho$.
(b) the 90°-rotation $\vec A\mapsto\vec A'=\vec A\times\hat z$ turns
$\vec\nabla\cdot\vec A'$ into $(\vec\nabla\times\vec A)\cdot\hat z$ and
$\hat n\cdot\vec A'\,d\ell$ into $\vec A\cdot d\vec\ell$, so 2-D Gauss applied
to $\vec A'$ *is* 2-D Stokes applied to $\vec A$, and vice versa.
*Check:* `test_e2d_flux_circles`, `test_e2d_flux_square` ($4\pi q$ for circles
of several radii, an offset charge, and a square contour),
`test_e2d_nonenclosing_zero`, `test_e2d_only_inverse_r` (power-law fields
$\rho^s\hat\rho$ have radius-*dependent* flux unless $s=-1$),
`test_e2d_div_free_away` ($\vec\nabla\cdot\vec E=0$ off the charge),
`test_2d_gauss_stokes_pointwise` and `test_2d_gauss_stokes_integral` (the
rotation map, differentially and integrally).

**Solution.**

**(a) Step 1 — the 2-D field equation.** In the 2-D electrodynamics of §1.5
(sources = $z$-independent line charges), the surviving electrostatic equation
is the first row of Table 1.5 with vacuum $\vec D=\vec E$:
$$\vec\nabla\cdot\vec E=4\pi\sigma,$$
$\sigma$ = 2-D charge density; a point charge $q$ at the origin is
$\sigma=q\,\delta^2(\vec r)$ (`~MA-15`).

**Step 2 — integral form via the 2-D Gauss theorem** (Eq. 1.37, p.16). For any
closed curve $C$ enclosing the origin, with region $S$:
$$\oint_Cd\ell\,\hat n\cdot\vec E=\int_Sdx\,dy\,(\vec\nabla\cdot\vec E)
=4\pi\int_Sdx\,dy\,\sigma=4\pi q .$$

**Step 3 — symmetry.** A point source in a plane is invariant under rotations
about it and under reflections through any line containing it; the reflections
kill the azimuthal component, the rotations make the magnitude a function of
distance only:
$$\vec E=E(\rho)\,\hat\rho,\qquad\rho=\sqrt{x^2+y^2}.$$

**Step 4 — evaluate on a circle.** Take $C$ = circle of radius $\rho$ centered
on the charge; there $\hat n=\hat\rho$ and $E(\rho)$ is constant along $C$:
$$\oint_Cd\ell\,\hat n\cdot\vec E=E(\rho)\oint_Cd\ell=E(\rho)\,2\pi\rho=4\pi q
\quad\Longrightarrow\quad
\boxed{\ \vec E=\frac{2q}{\rho}\,\hat\rho\ }.$$
The radial dependence is $1/\rho$ — one inverse power less than 3-D's
$1/r^2$, because the same flux is spread over a circumference
$\propto\rho$ rather than an area $\propto r^2$. $\blacksquare$

*Remarks.* (i) This is precisely the 3-D infinite line charge with
$\lambda=q$ ($E=2\lambda/\rho$), which is footnote 10's point (p.19): the
$4\pi$ in Table 1.5 treats 2-D charge as line charge per unit $z$; a
"geometrically 2-D" convention would write $\vec\nabla\cdot\vec E=2\pi\sigma$
and get $E=q/\rho$. The book's normalization is used here.
(ii) The potential is logarithmic, $\Phi=-2q\ln(\rho/\rho_0)$ — no reference
point at infinity exists in 2-D.
(iii) Uniqueness of the power: for a trial $E\propto\rho^s\hat\rho$ the circle
flux is $2\pi\rho^{s+1}$, radius-independent (as Step 2 demands of *every*
enclosing contour) only for $s=-1$ — this is what `test_e2d_only_inverse_r`
measures.

**(b) Step 1 — the two theorems side by side** (Eqs. 1.37–1.38, p.16), for a
planar region $S$ with counterclockwise boundary $C$, outward normal $\hat n$,
tangent $\hat t$ ($d\vec\ell=\hat t\,d\ell$):
$$\text{(G)}\ \int_Sdx\,dy\,(\vec\nabla\cdot\vec A)=\oint_Cd\ell\,\hat n\cdot\vec A,
\qquad
\text{(S)}\ \int_Sdx\,dy\,(\vec\nabla\times\vec A)\cdot\hat z=\oint_Cd\vec\ell\cdot\vec A .$$

**Step 2 — the rotation map.** For a planar field
$\vec A=(A_x,A_y,0)$ define the in-plane 90°-rotated field
$$\vec A'\equiv\vec A\times\hat z=(A_y,\,-A_x,\,0)$$
(rotation by $-90^\circ$; note $\hat z\times\vec A'=\vec A$, so the map is
invertible).

**Step 3 — the map swaps the area integrands.**
$$\vec\nabla\cdot\vec A'=\partial_xA_y+\partial_y(-A_x)
=\partial_xA_y-\partial_yA_x=(\vec\nabla\times\vec A)\cdot\hat z .$$
(Equivalently from the glossary $\vec\nabla\times(\vec P\times\vec Q)$
identity with $\vec P=\hat z$ constant:
$\vec\nabla\times(\hat z\times\vec A)=\hat z(\vec\nabla\cdot\vec A)-\partial_z\vec A
=\hat z(\vec\nabla\cdot\vec A)$ in 2-D — the same statement read backwards.)

**Step 4 — the map swaps the boundary integrands.** On $C$,
$\hat n=\hat t\times\hat z$ (check at the rightmost point of a
counterclockwise circle: $\hat t=\hat j$, $\hat j\times\hat k=\hat i=\hat n$ ✔).
Then, by the cyclic triple product,
$$\hat n\cdot\vec A'=(\hat t\times\hat z)\cdot(\vec A\times\hat z)
=\vec A\cdot\bigl[\hat z\times(\hat t\times\hat z)\bigr]
=\vec A\cdot\hat t,$$
where BAC-CAB gives $\hat z\times(\hat t\times\hat z)=\hat t(\hat z\cdot\hat z)-\hat z(\hat z\cdot\hat t)=\hat t$
(planar $\hat t\perp\hat z$). So $\hat n\cdot\vec A'\,d\ell=\vec A\cdot d\vec\ell$.

**Step 5 — conclude both directions.** Substituting Steps 3–4 into (G) applied
to $\vec A'$:
$$\int_Sdx\,dy\,(\vec\nabla\times\vec A)\cdot\hat z
=\int_Sdx\,dy\,(\vec\nabla\cdot\vec A')
\overset{\text{(G)}}{=}\oint_Cd\ell\,\hat n\cdot\vec A'
=\oint_Cd\vec\ell\cdot\vec A,$$
which is (S) for $\vec A$. Since $\vec A\mapsto\vec A\times\hat z$ is a
bijection of planar fields (inverse $\hat z\times{}$), the same computation
run on $\vec A''=\hat z\times\vec A$ derives (G) from (S):
$\vec\nabla\cdot\vec A=(\vec\nabla\times\vec A'')\cdot\hat z$ and
$\hat n\cdot\vec A\,d\ell=d\vec\ell\cdot\vec A''$. Each theorem is the other
one, stated for the rotated field: **in two dimensions Gauss and Stokes are
equivalent.** $\blacksquare$
(That is exactly why the 2-D boundary-condition derivation of §1.5 needed only
loops and line integrals where 3-D needed pillboxes *and* loops.)

*Numerics.* Pointwise: FD confirms
$\vec\nabla\cdot(\vec A\times\hat z)=(\vec\nabla\times\vec A)\cdot\hat z$ and
$(\vec\nabla\times(\hat z\times\vec A))\cdot\hat z=\vec\nabla\cdot\vec A$ at
random points ($\sim10^{-11}$). Integrally, on the unit disc: each theorem's
two sides agree to $\sim10^{-9}$, while the *rotated* boundary and area
quadratures ($\oint\hat n\cdot\vec A'\,d\ell$ vs $\oint\vec A\cdot d\vec\ell$,
$\iint\vec\nabla\cdot\vec A'$ vs $\iint(\vec\nabla\times\vec A)\cdot\hat z$)
coincide to the last bit — 2-D Gauss on the rotated field *is* 2-D Stokes,
operation for operation.

---

### P8.  Exercise A.1.1 — how the amount-conversion factors are determined  *(Wilcox 2e §A.1, p.862)*

Explain how the amount conversion factor in column 4 of Tables A.1 and A.2 is
determined.

*Answer:* column 4 converts *numerical values*: $\{Q\}_{\rm SI}=F_Q\,\{Q\}_{\rm G}$.
$F_Q$ is fixed by requiring both systems to describe the same physics: write
one physical relation for $Q$ (Coulomb force for charge, energy density for
fields, …) in both systems and equate the physical quantities. The mechanical
content converts by powers of $\alpha=10^2$ (cm/m) and $\beta=10^7$ (erg/J);
the electrical mismatch is carried by exactly the $\sqrt{4\pi\epsilon_0}$-type
factor of the symbol conversion (column 3), evaluated with the SI numbers
$4\pi\epsilon_0=10^7/c^2$, $\mu_0=4\pi\times10^{-7}$, $c=299{,}792{,}458$.
Column 5 is column 4's numerical value.
*Check:* `test_table_a1_values`, `test_table_a2_values` (all **30 rows**
recomputed from the Factor formulas and matched to the quoted Values, rel.
$10^{-12}$), `test_known_unit_conversions` (statC→C, statvolt→V, G→T, Mx→Wb,
Oe→A/m, cm→F, s·cm⁻¹→Ω against their known SI sizes).

**Solution.**

**Step 1 — what the two conversion pairs mean.** Columns 2–3 ("symbol
conversion") rewrite *equations*: substituting the column-3 expression for
every Gaussian symbol in a Gaussian equation yields the correct SI equation
(e.g. $q\to q/\sqrt{4\pi\epsilon_0}$ and $\vec E\to\sqrt{4\pi\epsilon_0}\vec E$
turn $\vec\nabla\cdot\vec E=4\pi\rho$ into $\vec\nabla\cdot\vec E=\rho/\epsilon_0$,
Table 1.1). Columns 4–5 ("amount conversion") rescale *numbers*: if a physical
quantity has numerical value $\{Q\}_{\rm G}$ in its Gaussian unit and
$\{Q\}_{\rm SI}$ in its SI unit, then
$$\{Q\}_{\rm SI}=F_Q\cdot\{Q\}_{\rm G},\qquad F_Q=\text{column 4, evaluated}=\text{column 5}.$$
Equivalently $F_Q$ = the size of one Gaussian unit of $Q$, expressed in SI
units (e.g. charge row: $F_q=10^{-1}c^{-1}=3.336\times10^{-10}$ = one
statcoulomb in coulombs).

**Step 2 — mechanical rows: pure $\alpha,\beta$ dimensional bookkeeping.**
Every Gaussian unit is a product of powers of (g, cm, s); regroup it into
powers of (erg, cm, s) using $\text{erg}=\text{g}\,\text{cm}^2\text{s}^{-2}$.
The two base amount conversions are (p.860)
$$1\ \text{cm}=\alpha^{-1}\,\text{m}\ (\alpha=10^2),\qquad
1\ \text{erg}=\beta^{-1}\,\text{J}\ (\beta=10^7),\qquad 1\ \text{s}=1\ \text{s}.$$
So a quantity whose Gaussian unit is $\text{erg}^{\,b}\,\text{cm}^{\,a}\,\text{s}^{\,c}$
has $F_Q=\beta^{-b}\alpha^{-a}$. Examples: energy $F_W=\beta^{-1}=10^{-7}$;
length $F_l=\alpha^{-1}$; force = erg/cm ⇒ $F_F=\alpha\beta^{-1}=10^{-5}$;
mass = erg·s²/cm² ⇒ $F_m=\alpha^2\beta^{-1}=10^{-3}$ — the first eight rows of
Table A.1 exactly.

**Step 3 — electrical rows: one physical law bridges the unit systems.**
A statcoulomb ($\text{g}^{1/2}\text{cm}^{3/2}\text{s}^{-1}=(\text{erg}\cdot\text{cm})^{1/2}$,
Table A.3) and a coulomb (A·s) are dimensionally incommensurate, so no pure
$\alpha,\beta$ power connects them. The bridge is physics. Take one and the
same physical pair of charges at one distance and write the *same force* both
ways:
$$F=\frac{q^2}{r^2}\ (\text{Gaussian})\qquad\text{and}\qquad
F=\frac{q^2}{4\pi\epsilon_0 r^2}\ (\text{SI}).$$
Equate the physical combinations $q^2_{\rm G}=F r^2$ and
$q^2_{\rm SI}/(4\pi\epsilon_0)=F r^2$ — both equal the same physical
energy×length. Numerically,
$$\{q\}_{\rm G}^2\ \text{erg\,cm}=\frac{\{q\}_{\rm SI}^2}{4\pi\epsilon_0}\ \text{J\,m}
\ \Longrightarrow\
\{q\}_{\rm SI}^2=4\pi\epsilon_0\,\{q\}_{\rm G}^2\,\frac{\text{erg\,cm}}{\text{J\,m}}
=\frac{4\pi\epsilon_0}{\alpha\beta}\{q\}_{\rm G}^2,$$
$$\boxed{\ F_q=\Bigl(\frac{4\pi\epsilon_0}{\alpha\beta}\Bigr)^{1/2}\ }
=\Bigl(\frac{10^7/c^2}{10^9}\Bigr)^{1/2}=10^{-1}c^{-1}
=3.33564\times10^{-10},$$
which is precisely the Table A.1 charge row (Factor *and* Value), using the SI
statements (p.860) $4\pi\epsilon_0=10^7/c^2$ with $c=299{,}792{,}458$ as a pure
number. The same recipe with the energy density $u=E^2/8\pi=\epsilon_0E^2/2$
gives the field rows, e.g.
$$\{E\}_{\rm G}^2\,\frac{\text{erg}}{\text{cm}^3}\cdot\frac1{8\pi}
=\frac{\epsilon_0}{2}\{E\}_{\rm SI}^2\,\frac{\text{J}}{\text{m}^3}
\ \Longrightarrow\
F_E=\Bigl(\frac{\alpha^3}{4\pi\epsilon_0\,\beta}\Bigr)^{1/2}=10^{-4}c,$$
and with $u=B^2/8\pi=B^2/2\mu_0$:
$F_B=(\mu_0\alpha^3/4\pi\beta)^{1/2}=10^{-4}$ (one gauss = $10^{-4}$ tesla).

**Step 4 — the general pattern.** Comparing Steps 2–3 with column 3 shows the
rule the tables are built on:
$$F_Q=\underbrace{\kappa_Q^{-1}}_{\substack{\text{inverse of the }\epsilon_0/\mu_0\\ \text{coefficient in column 3}}}
\times\underbrace{\alpha^{-a}\beta^{-b}}_{\substack{\text{erg}^b\text{cm}^a\text{s}^c\ \text{content}\\ \text{of the Gaussian unit}}},$$
where column 3 reads "Gaussian symbol $\leftrightarrow\kappa_Q\times$ SI
symbol" ($\kappa_q=1/\sqrt{4\pi\epsilon_0}$,
$\kappa_E=\sqrt{4\pi\epsilon_0}$, $\kappa_B=\sqrt{4\pi/\mu_0}$, …). The
$\epsilon_0/\mu_0$ structure of column 4 is the *inverse* of column 3's
because column 3 converts symbols in equations while column 4 converts the
numbers those symbols stand for — the two conversions compose to the identity
on physical quantities. Column 5 then follows from
$4\pi\epsilon_0=10^7/c^2$, $\mu_0/4\pi=10^{-7}$, $\alpha=10^2$, $\beta=10^7$.
$\blacksquare$

*Worked spot-checks (all reproduced in code).*
potential: $F_\Phi=(\alpha/4\pi\epsilon_0\beta)^{1/2}=10^{-6}c=299.79$
(1 statvolt = 299.79 V); H-field: $F_H=(\alpha^3/4\pi\mu_0\beta)^{1/2}=\frac{10^3}{4\pi}=79.58$
(1 oersted = $1000/4\pi$ A/m); capacitance: $F_C=4\pi\epsilon_0/\alpha=10^5c^{-2}
=1.11\times10^{-12}$ (1 cm = 1.11 pF); resistance:
$F_R=\alpha/4\pi\epsilon_0=10^{-5}c^2=8.99\times10^{11}$ (1 s/cm ≈ 899 GΩ).

*Remark (an internal anomaly worth knowing).* The Table A.2/A.4
**vector-potential** row carries Factor $(\mu_0\alpha^5/4\pi\beta)^{1/2}=10^{-2}$
with unit designation "G cm⁻¹ → T m⁻¹", i.e. it converts a *B-field per
length*: indeed $1\ \text{G/cm}=10^{-4}\,\text{T}/10^{-2}\,\text{m}
=10^{-2}\ \text{T/m}$, matching the row's $10^{-2}$. But the potential of
Ex 1.1.2 ($\vec B=\vec\nabla\times\vec A$) has units of B-field × *length*
(G·cm), whose amount factor is
$1\ \text{G·cm}=10^{-4}\,\text{T}\times10^{-2}\,\text{m}=10^{-6}\ \text{T·m}$
(as in Jackson's units appendix). The book's row is
internally consistent (its Factor matches its own G cm⁻¹ designation) but the
designation looks like an erratum for the quantity named. The code checks the
row as printed.

---

### P9.  Exercise A.1.2 — Gaussian conventions on MKS base units  *(Wilcox 2e §A.1, p.862)*

The Gaussian system is not necessarily tied to CGS units. Discuss the effects
of adopting MKS units within the Gaussian system. Are there advantages? Are
there any new disadvantages?

*Answer:* nothing in the Gaussian *structure* (unit-coefficient Coulomb law,
no $\epsilon_0,\mu_0$, $\vec E$ and $\vec B$ of equal dimension, explicit
$4\pi$ and $c$ in Table 1.1) refers to the centimeter or gram, so an
"MKS-Gaussian" system is perfectly consistent: every equation of the book
survives verbatim with $c=2.998\times10^8$ m/s. The units rescale by pure
$\alpha,\beta$ powers — the charge unit becomes
$\sqrt{\alpha\beta}\,\text{statC}=10^{4.5}\,\text{statC}\approx10.5\,\mu$C, the
field unit $\sqrt{10}$ gauss $\approx3.16\times10^{-4}$ T — and conversions to
SI collapse to pure $\sqrt{4\pi\epsilon_0}$ / $\sqrt{\mu_0/4\pi}$ factors
(no $\alpha,\beta$ residue). Advantages: SI-scale mechanics (newtons, joules)
with Gaussian-clean equations. New disadvantages: it orphans the entire
CGS-Gaussian data ecosystem (every tabulated constant, and unit names like
gauss/statvolt/oersted), for unit sizes that match neither tradition; the
half-integer dimensions remain.
*Check:* `test_mks_gaussian_unit_sizes` (the $\sqrt{\alpha\beta}$,
$\sqrt{\beta/\alpha^3}$, $\sqrt{4\pi\epsilon_0}$, $\sqrt{\mu_0/4\pi}$ relations
close consistently both ways), `test_electron_charge_roundtrip`
($e=4.80320450\times10^{-10}$ statC → MKS-Gaussian → $1.6022\times10^{-19}$ C,
matching CODATA through a path that never uses the direct statC→C factor).

**Solution.**

**Step 1 — what "Gaussian" actually fixes.** The system is defined by
*conventions*, not by base-unit sizes: (i) charge is derived, with Coulomb's
law $F=q_1q_2/r^2$ carrying coefficient 1 (no $\epsilon_0$); (ii) $\vec B$ is
normalized so the Lorentz force is $q(\vec E+\frac{\vec v}{c}\times\vec B)$,
making $\vec E$ and $\vec B$ dimensionally identical; (iii) the factors $4\pi$
and $c$ sit explicitly in Maxwell's equations (Table 1.1, Gaussian column).
None of (i)–(iii) mentions the gram or centimeter — they work over *any*
mechanical base. (This is the Appendix's own point, p.859: Gaussian units are
"combinations of" mass, length, time; CGS is the traditional choice, not a
logical necessity.)

**Step 2 — build MKS-Gaussian and size its units.** Keep (i)–(iii), take
(kg, m, s). The unit charge is the charge for which two of them 1 m apart repel
with 1 N: $[q]=\sqrt{\text{N}\cdot\text{m}^2}=\sqrt{\text{J}\cdot\text{m}}
=\text{kg}^{1/2}\text{m}^{3/2}\text{s}^{-1}$. Its size in the two neighboring
systems:
$$1\ \sqrt{\text{J\,m}}=\sqrt{\beta\,\text{erg}\cdot\alpha\,\text{cm}}
=\sqrt{\alpha\beta}\ \sqrt{\text{erg\,cm}}=10^{4.5}\ \text{statC}
\approx3.16\times10^4\ \text{statC},$$
and in SI, by the P8 Step-3 bridge with the $\alpha,\beta$ factors now absent
(both sides use J·m):
$$\{q\}_{\rm SI}=\sqrt{4\pi\epsilon_0}\,\{q\}_{\rm MKSG}
\ \Longrightarrow\ 1\ \text{MKS-G charge unit}=\sqrt{10^7/c^2}\ \text{C}
=\frac{10^{3.5}}{c}\,\text{C}\approx1.05\times10^{-5}\ \text{C}\ (\approx10.5\ \mu\text{C}).$$
Fields ($E$ or $B$, same dimension, $\sim\sqrt{\text{energy/volume}}$):
$$1\ \sqrt{\text{J/m}^3}=\sqrt{\beta/\alpha^3}\ \sqrt{\text{erg/cm}^3}
=\sqrt{10}\ \text{gauss}\approx3.162\ \text{G},\qquad
1\ \text{MKS-G B unit}=\sqrt{\mu_0/4\pi}\ \text{T}=\sqrt{10^{-7}}\ \text{T}
=3.162\times10^{-4}\ \text{T},$$
and the two routes agree ($\sqrt{10}\times10^{-4}=\sqrt{10^{-7}}$ ✔) — the
consistency the code checks. Mechanical quantities are simply SI (N, J, W).
All equations of the text hold unchanged with $c=2.99792458\times10^8$ m/s.

**Step 3 — advantages.** (i) *Mechanical compatibility with the lab:* forces,
energies, powers come out in newtons/joules/watts — no $\alpha,\beta$
housekeeping every time an EM calculation meets a mechanical one. (ii) *The
Gaussian virtues survive intact:* no $\epsilon_0\mu_0$ clutter, $E$ and $B$
comparable (relativity- and QM-friendly, the book's own argument for Gaussian,
p.859). (iii) *Cleaner SI dictionary:* every electrical amount conversion is a
pure $\sqrt{4\pi\epsilon_0}$-type factor — the entire $\alpha^p\beta^q$ column
of P8 collapses to 1, so the Appendix tables would shrink to their
$\epsilon_0/\mu_0$ skeletons.

**Step 4 — new disadvantages.** (i) *It orphans the data.* The Gaussian
literature — every handbook value ($e=4.803\times10^{-10}$ statC), every named
unit (gauss, oersted, statvolt, the "cm" of capacitance) — is CGS-Gaussian;
MKS-Gaussian numbers match *neither* that corpus *nor* SI (the charge unit is
$10.5\,\mu$C, the field unit 3.16 G ≈ $3.16\times10^{-4}$ T), so every
tabulated constant must be re-derived and the familiar magnitudes
(Earth's field ≈ 0.5 G) lose their round numbers. (ii) *No names, no
instruments:* nothing measures in these units, and none have standard names —
a pure communication cost. (iii) *What does not improve:* the half-integer
dimensions ($\text{kg}^{1/2}\text{m}^{3/2}\text{s}^{-1}$)
are a property of convention (i), not of CGS, so they persist — anyone hoping
MKS would cure them gains nothing. Net: MKS-Gaussian is internally flawless
(Step 2's numbers close on the CODATA electron charge), mildly attractive in
principle, and priced out by the network effects of the two entrenched
systems — which is presumably why it is a discussion exercise and not a
proposal. $\blacksquare$

*Numerics.* `test_electron_charge_roundtrip`:
$e_{\rm MKSG}=4.80320450\times10^{-10}/\sqrt{\alpha\beta}=1.5189\times10^{-14}$
MKS-G units, then $e_{\rm SI}=\sqrt{4\pi\epsilon_0}\,e_{\rm MKSG}
=1.60218\times10^{-19}$ C — CODATA to $10^{-8}$ relative, and algebraically
identical to the direct Table A.1 route
($\tfrac1{\sqrt{\alpha\beta}}\cdot\sqrt{4\pi\epsilon_0}=\sqrt{4\pi\epsilon_0/\alpha\beta}=10^{-1}c^{-1}$).
