# EM-04 — Boundary-Value Problems (notes)

A boundary-value problem is **Laplace's equation with the answer pinned at the
edges**. In a charge-free region the potential of `~EM-03` satisfies
$\nabla^2 V = 0$, and the physics is reduced to: given the potential (or the
total charge) on the bounding surfaces, find $V$ inside. This module is the
toolbox — uniqueness, images, separation of variables, relaxation.

Citation key (full details + PDF pages in `refs.md`): **Gr** = Griffiths 4e.
Page numbers are the *printed* book pages; everything here is in **Chapter 3**.

## 1. Laplace's equation and the harmonic property
With no charge present, Poisson's equation $\nabla^2 V=-\rho/\varepsilon_0$
(Gr Eq. 2.24, `~EM-03`) collapses to **Laplace's equation** (Gr Eq. 2.25):
$$\nabla^2 V=\frac{\partial^2V}{\partial x^2}+\frac{\partial^2V}{\partial y^2}+\frac{\partial^2V}{\partial z^2}=0 .$$
Its solutions are **harmonic functions**, with two properties that drive the
whole chapter: $V$ at a point is the **average** of $V$ over any surrounding
sphere (or, in 2-D, circle), and $V$ has **no local maxima or minima** in the
interior — every extremum sits on the boundary. The mean-value property is what
the relaxation solver in §5 turns into an algorithm.

## 2. The uniqueness theorems (Gr §3.1.5–3.1.6, pp.119–123)
**First uniqueness theorem** (Gr §3.1.5, pp.119–120): *the solution of Laplace's
equation in a volume $\mathcal V$ is uniquely determined once $V$ is specified
on the boundary $\mathcal S$.* The proof, every step (Gr p.120):

1. **Suppose two solutions.** Let $V_1$ and $V_2$ both satisfy
   $\nabla^2V_1=\nabla^2V_2=0$ in $\mathcal V$ and take the *same* specified
   values on $\mathcal S$. Look at their difference,
   $$V_3\equiv V_1-V_2 .$$
2. **$V_3$ is harmonic.** Laplace's equation is *linear*, so
   $\nabla^2V_3=\nabla^2V_1-\nabla^2V_2=0-0=0$.
3. **$V_3$ vanishes on the boundary,** since $V_1$ and $V_2$ are equal there:
   $V_3\big|_{\mathcal S}=0$.
4. **No interior extrema** (§1): a harmonic function equals the average of its
   values over any sphere around the point, so it "allows no local maxima or
   minima — all extrema occur on the boundaries" (Gr p.120). The maximum and the
   minimum of $V_3$ over $\overline{\mathcal V}$ are therefore both boundary
   values — both $0$.
5. **Squeeze.** $0\le V_3\le 0$ everywhere, so $V_3\equiv0$, i.e.
   $V_1=V_2$. $\blacksquare$

**Poisson corollary** (Gr p.121). Throw charge in: with
$\nabla^2V_{1,2}=-\rho/\varepsilon_0$ for the *same* $\rho$, the difference
*still* obeys $\nabla^2V_3=-\rho/\varepsilon_0+\rho/\varepsilon_0=0$ and the
same five steps run unchanged: *the potential in $\mathcal V$ is unique once
(a) $\rho$ throughout the region and (b) $V$ on all boundaries are specified.*

**Second uniqueness theorem** (Gr §3.1.6, pp.121–123): in a region bounded by
conductors and containing a fixed charge density $\rho$, the **field** is
uniquely determined once the **total charge on each conductor** is given. The
proof needs a different tool, because on a conductor we know $Q_i$, not $V$
(Gr pp.122–123):

1. **Suppose two fields.** $\mathbf E_1$ and $\mathbf E_2$ both satisfy Gauss's
   law with the same $\rho$ in the region and the same totals on every
   conductor: $\nabla\!\cdot\!\mathbf E_{1,2}=\rho/\varepsilon_0$, and
   $\oint\mathbf E_{1,2}\!\cdot d\mathbf a=Q_i/\varepsilon_0$ over the $i$-th
   conducting surface (and $Q_{\rm tot}/\varepsilon_0$ over the outer boundary).
2. **Difference field.** $\mathbf E_3\equiv\mathbf E_1-\mathbf E_2$ obeys
   $\nabla\!\cdot\!\mathbf E_3=0$ in the region (Gr Eq. 3.7) and
   $\oint\mathbf E_3\!\cdot d\mathbf a=0$ over *each* boundary surface (Gr Eq. 3.8).
3. **Conductors are equipotentials,** so $V_3$ is a *constant* on each
   conducting surface — not necessarily zero, and not necessarily the same
   constant on different conductors (only its constancy is known).
4. **The trick** (product rule 5, with $\mathbf E_3=-\nabla V_3$ and Eq. 3.7):
   $$\nabla\!\cdot\!(V_3\mathbf E_3)=V_3(\nabla\!\cdot\!\mathbf E_3)+\mathbf E_3\!\cdot\!(\nabla V_3)=-(E_3)^2 .$$
5. **Integrate and convert.** Over the region $\mathcal V$, the divergence
   theorem turns the left side into a surface integral over all boundaries:
   $$\int_{\mathcal V}\nabla\!\cdot\!(V_3\mathbf E_3)\,d\tau=\oint_{\mathcal S}V_3\,\mathbf E_3\!\cdot d\mathbf a=-\int_{\mathcal V}(E_3)^2\,d\tau .$$
6. **The surface integral dies.** On each surface $V_3$ is constant (step 3), so
   it comes outside — leaving $V_3^{(i)}\oint\mathbf E_3\!\cdot d\mathbf a=0$ by
   step 2 (if the outer boundary is at infinity, $V_3=0$ there anyway). Hence
   $$\int_{\mathcal V}(E_3)^2\,d\tau=0 .$$
7. **Positivity.** The integrand $(E_3)^2\ge0$; a non-negative integrand with
   zero integral must vanish identically, so $\mathbf E_3=\mathbf 0$ and
   $\mathbf E_1=\mathbf E_2$ everywhere. $\blacksquare$

Griffiths' warning stands: "there is a real danger that the theorem itself will
seem more plausible to you than the proof" (p.123, with Purcell's
four-conductor counterexample to intuition).

These are not bookkeeping — they are the **method**: *any* potential that
satisfies $\nabla^2V=0$ in the region, has the right singularities (the real
charges), and matches the boundary, is guaranteed to be **the** answer. That
licence is what makes the next two tricks legitimate. (§6 runs the first
theorem as an algorithm: relaxation from *any* interior guess converges to the
one harmonic function the boundary allows.)

## 3. The method of images — the classic image problem (Gr §3.2.1, p.124)
A point charge $q$ sits a height $d$ above an infinite **grounded** ($V=0$)
conducting plane $z=0$. Solving Poisson's equation directly is hard: the induced
surface charge is unknown. Instead, **forget the conductor** and place an *image*
charge $-q$ at the mirror point $(0,0,-d)$. For $z>0$ (Gr Eq. 3.9):
$$V(x,y,z)=\frac{1}{4\pi\varepsilon_0}\left[\frac{q}{\sqrt{x^2+y^2+(z-d)^2}}-\frac{q}{\sqrt{x^2+y^2+(z+d)^2}}\right].$$
On the plane $z=0$ the two denominators are equal, so $V=0$ — exactly the
required boundary condition. This $V$ also obeys $\nabla^2V=0$ for $z>0$ (away
from $q$), has the correct $1/r$ singularity at the real charge, and $\to 0$ at
infinity. By the **first uniqueness theorem** it **is** the potential in the
upper half-space. (Below the plane the real field is zero; the image is a
fiction valid only for $z>0$.) Code: `image_potential_plane`, and
`image_field_plane` for $\mathbf E=-\nabla V$.

## 4. Induced surface charge and the force (Gr §3.2.2–3.2.3, p.125 / p.126)
The induced charge on the plane follows from the field just outside a conductor,
$\sigma=-\varepsilon_0\,\partial V/\partial n=-\varepsilon_0\,\partial V/\partial z\big|_{z=0}$
(Gr Eq. 3.10):
$$\sigma(x,y)=\frac{-q\,d}{2\pi\,(x^2+y^2+d^2)^{3/2}} .$$
It is largest (most negative) **directly under** the charge and falls off as the
distance cubed. Integrating over the whole plane returns
$$Q_{\text{ind}}=\int\sigma\,da=-q ,$$
so the *entire* image charge materializes as real induced surface charge — a
satisfying consistency check. Code: `induced_surface_charge`,
`total_induced_charge` (polar-ring quadrature → $-q$).

The **force** on $q$ is just its Coulomb attraction to the image charge a
distance $2d$ away — attractive, toward the plane (Gr Eq. 3.12):
$$\mathbf F=-\frac{1}{4\pi\varepsilon_0}\frac{q^2}{(2d)^2}\,\hat{\mathbf z}.$$
The *energy*, however, is **half** the energy of a genuine $q,-q$ pair, because
only the half-space $z>0$ contains field. Code: `image_force` (returns the
signed $z$-component, negative = toward the conductor).

## 5. Separation of variables — the semi-infinite slot (Gr §3.3.1, p.131)
When no image is available, try **product solutions** $V(x,y)=X(x)\,Y(y)$.
Laplace's equation becomes $X''/X+Y''/Y=0$; each term must be a constant, giving
$X''=k^2X$, $Y''=-k^2Y$ — a separation that is the EM face of `~MA-08`.

The **semi-infinite slot**: grounded plates at $y=0$ and $y=a$, extending to
$x\to\infty$, closed at $x=0$ by a strip held at $V_0$. The boundary conditions
$V(x,0)=V(x,a)=0$ and $V(\infty,y)=0$ select $Y=\sin(n\pi y/a)$ and the decaying
$X=e^{-n\pi x/a}$, so
$$V(x,y)=\sum_{n=1}^{\infty}C_n\,e^{-n\pi x/a}\sin\frac{n\pi y}{a}.$$
Matching the remaining condition $V(0,y)=V_0$ is a **Fourier sine expansion**:
sine orthogonality (the Sturm–Liouville completeness of `~MA-11`) gives
$C_n=4V_0/n\pi$ for odd $n$ and $0$ for even $n$, hence (Gr Eq. 3.34)
$$V(x,y)=\frac{4V_0}{\pi}\sum_{n=1,3,5,\dots}\frac{1}{n}\,e^{-n\pi x/a}\sin\frac{n\pi y}{a}.$$
Remarkably this series sums to a **closed form** (Gr Eq. 3.36):
$$\boxed{\,V(x,y)=\frac{2V_0}{\pi}\,\arctan\!\left(\frac{\sin(\pi y/a)}{\sinh(\pi x/a)}\right)\,}$$
Code carries both: `slot_potential_series` (truncated sum) and
`slot_potential_closed` (the arctan); they agree to $\sim10^{-4}$, a direct
numerical confirmation that the Fourier series really does collapse to Eq. 3.36.
The spherical analogue (Gr §3.3.2, p.141) replaces sines by **Legendre**
polynomials, $V=\sum(A_\ell r^\ell+B_\ell r^{-\ell-1})P_\ell(\cos\theta)$ — the
$r^{-\ell-1}$ terms are the multipole expansion of `~EM-05` / `~MA-12`.

## 6. Uniqueness, made numerical — relaxation
The mean-value property of §1 discretizes to: on a grid, the interior value at a
node is the **average of its four neighbours**,
$V_{i,j}=\tfrac14(V_{i+1,j}+V_{i-1,j}+V_{i,j+1}+V_{i,j-1})$. Sweeping this update
(Gauss–Seidel **relaxation**) from *any* interior guess converges to the single
potential consistent with the boundary — the **first uniqueness theorem**, run as
an algorithm. Code: `solve_laplace_2d`; with the boundary set to $V=V_0\,x/L$
(linear, hence harmonic) the relaxed interior reproduces $V_0\,x/L$ exactly,
confirming that the boundary alone fixes the interior.

## Where this goes
- `~EM-05` — the spherical separation of §3.3.2 ($P_\ell$, $r^{-\ell-1}$) **is**
  the multipole expansion; the far field of any localized cloud lives there.
- `~EM-06` — conductors, capacitance and electrostatic energy lean on the same
  boundary conditions and the **second** uniqueness theorem.
- `~MA-08` supplies the general PDE separation; `~MA-11` the orthogonal-function
  completeness that makes the Fourier coefficients $C_n$ unique; `~MA-12` the
  Legendre/special functions of the spherical case.
- Images generalize to arbitrary boundaries as **Green's functions** (`~MA-14`):
  the image construction is the Dirichlet Green's function for the half-space.
