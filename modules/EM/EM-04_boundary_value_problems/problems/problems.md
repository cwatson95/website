# EM-04 — Problems

Work by hand, then check with `code/boundary_value.py`. Citations in `../refs.md`;
**Gr** = Griffiths 4e (printed pages). All five sit in Chapter 3, §3.1–3.3.

### P1.  Grounded plane by the method of images  *(Gr §3.2.1, p.124, Eq. 3.9)*
A point charge $q$ is held a height $d$ above an infinite grounded conducting
plane $z=0$. Replace the conductor by an image $-q$ at $(0,0,-d)$ and write the
potential for $z>0$,
$$V(x,y,z)=\frac{1}{4\pi\varepsilon_0}\left[\frac{q}{\sqrt{x^2+y^2+(z-d)^2}}-\frac{q}{\sqrt{x^2+y^2+(z+d)^2}}\right].$$
Show $V=0$ everywhere on $z=0$, that $\nabla^2V=0$ for $z>0$ (off the charge),
and argue from the **first uniqueness theorem** that this is *the* potential.
*Check:* `image_potential_plane(q, d)` evaluated at several $(x,y,0)$ returns $0$;
`image_field_plane` gives the matching $\mathbf E=-\nabla V$.

**Solution.** On the plane $z=0$ both radicals reduce to the same value
$\sqrt{x^2+y^2+d^2}$, so the bracket is $q/\sqrt{x^2+y^2+d^2}-q/\sqrt{x^2+y^2+d^2}=0$
and $V\equiv0$ there. Each term is a Coulomb potential $\propto1/r$, satisfying
$\nabla^2(1/r)=0$ away from its source; the image sits at $(0,0,-d)$, *outside* the
region $z>0$, so $\nabla^2V=0$ everywhere in the upper half-space except at the real
charge. This candidate has the correct $1/r$ singularity at $q$, solves Laplace's
equation, vanishes on $z=0$, and $\to0$ at infinity. By the **first uniqueness
theorem** the boundary data fix the solution, so this *is* the potential for $z>0$.
Hence `image_potential_plane(q, d)` returns $0$ at every $(x,y,0)$ and
`image_field_plane` gives the matching $\mathbf E=-\nabla V$.

### P2.  Induced surface charge and its total  *(Gr §3.2.2, p.125, Eq. 3.10)*
From the solution of P1, compute the induced density
$\sigma=-\varepsilon_0\,\partial V/\partial z\big|_{z=0}$ and obtain
$$\sigma(x,y)=\frac{-q\,d}{2\pi\,(x^2+y^2+d^2)^{3/2}} .$$
Show $|\sigma|$ peaks directly beneath the charge and decays as the cube of the
distance, then integrate over the whole plane to prove $\int\sigma\,da=-q$ (use
polar coordinates, $da=2\pi s\,ds$). *Check:* `induced_surface_charge(q, d)` is
most negative at the origin and shrinks outward, and
`total_induced_charge(q, d)` $\approx -q$.

**Solution.** Differentiate the P1 potential in $z$; with $r_\mp^2=x^2+y^2+(z\mp d)^2$ the
distances to the real ($-$) and image ($+$) charges,
$$\frac{\partial V}{\partial z}=\frac{q}{4\pi\varepsilon_0}\left[-\frac{z-d}{r_-^3}+\frac{z+d}{r_+^3}\right]\ \xrightarrow{\ z=0\ }\ \frac{q}{4\pi\varepsilon_0}\frac{2d}{(x^2+y^2+d^2)^{3/2}}.$$
Then $\sigma=-\varepsilon_0\,\partial V/\partial z|_{z=0}=-qd\big/\bigl[2\pi(x^2+y^2+d^2)^{3/2}\bigr]$,
most negative directly under $q$ (at $s=0$) and dying as $s^{-3}$. Integrating over the plane in
polar rings $da=2\pi s\,ds$ (with $s^2=x^2+y^2$),
$$\int\sigma\,da=-qd\int_0^\infty\frac{s\,ds}{(s^2+d^2)^{3/2}}=-qd\left[\frac{-1}{\sqrt{s^2+d^2}}\right]_0^\infty=-qd\cdot\frac1d=-q,$$
so the entire image charge reappears as real induced charge. Numerically `induced_surface_charge`
peaks at $\sigma(0,0)=-1.59\times10^{-8}$ C/m² and shrinks outward, while
`total_induced_charge` $=-1.006\times10^{-9}\approx-q$.

### P3.  Force and energy of the image charge  *(Gr §3.2.3, p.126, Eq. 3.12)*
Show that the conductor attracts $q$ exactly as the image charge would — a force
toward the plane,
$$\mathbf F=-\frac{1}{4\pi\varepsilon_0}\frac{q^2}{(2d)^2}\,\hat{\mathbf z},$$
the Coulomb attraction of $q$ and $-q$ across separation $2d$. Then explain why
the *energy* is **half** that of a real $q,-q$ pair (only $z>0$ holds field).
*Check:* `image_force(q, d)` is negative (attractive) and equals
$-\,$`K_E`$\,q^2/(2d)^2$.

**Solution.** In the region $z>0$ the real field is identical to that of $q$ at $+d$ together with
the image $-q$ at $-d$, so the force on $q$ is simply its Coulomb attraction to that image, a
distance $2d$ away:
$$\mathbf F=\frac{1}{4\pi\varepsilon_0}\frac{q(-q)}{(2d)^2}\,\hat{\mathbf z}=-\frac{1}{4\pi\varepsilon_0}\frac{q^2}{(2d)^2}\,\hat{\mathbf z},$$
directed toward the plane. The **energy** is *not* that of a real pair, however: the image field
exists only in $z>0$, which holds just half of the $q$–image field energy. Integrating this force
in from infinity (equivalently, halving the pair energy $-kq^2/2d$) gives
$$W=-\frac{1}{4\pi\varepsilon_0}\frac{q^2}{4d},$$
half of $-kq^2/2d$. Numerically `image_force(q, d)` $=-2.247\times10^{-7}$ N $=-k\,q^2/(2d)^2$
(with $k=$ `K_E`) — negative, i.e. attractive toward the conductor.

### P4.  The semi-infinite slot — series vs closed form  *(Gr §3.3.1, p.131, Eqs. 3.34, 3.36)*
Grounded plates lie at $y=0$ and $y=a$; the strip at $x=0$ is held at $V_0$ and
the slot runs to $x\to\infty$. By separation of variables and a Fourier sine
expansion of the $x=0$ condition, derive
$$V(x,y)=\frac{4V_0}{\pi}\sum_{n=1,3,5,\dots}\frac1n\,e^{-n\pi x/a}\sin\frac{n\pi y}{a}
=\frac{2V_0}{\pi}\arctan\!\left(\frac{\sin(\pi y/a)}{\sinh(\pi x/a)}\right).$$
Verify the closed form vanishes on $y=0,a$, dies as $x\to\infty$, and tends to
$V_0$ at the mouth. *Check:* `slot_potential_series(V0, a)` and
`slot_potential_closed(V0, a)` agree to $\sim10^{-4}$ across the interior, and the
closed form returns $0$ on the grounded plates.

**Solution.** Separating $V=X(x)Y(y)$ turns $\nabla^2V=0$ into $X''/X=-Y''/Y=k^2$. The grounded
plates $V(x,0)=V(x,a)=0$ select $Y=\sin(n\pi y/a)$ with $k=n\pi/a$, and decay as $x\to\infty$
picks $X=e^{-n\pi x/a}$. Imposing the mouth condition $V(0,y)=V_0$ is a Fourier sine problem; sine
orthogonality gives $C_n=\tfrac2a\int_0^a V_0\sin\tfrac{n\pi y}{a}\,dy=4V_0/n\pi$ for odd $n$ and
$0$ for even, so
$$V(x,y)=\frac{4V_0}{\pi}\sum_{n=1,3,5,\dots}\frac1n\,e^{-n\pi x/a}\sin\frac{n\pi y}{a}.$$
Summing with $\sum_{n\,\text{odd}}\tfrac{w^n}{n}=\tfrac12\ln\tfrac{1+w}{1-w}$ at $w=e^{-\pi(x-iy)/a}$
and taking the imaginary part collapses this to
$$V(x,y)=\frac{2V_0}{\pi}\arctan\!\frac{\sin(\pi y/a)}{\sinh(\pi x/a)}.$$
On $y=0,a$ the numerator vanishes so $V=0$; as $x\to\infty$, $\sinh\to\infty$ so $V\to0$; as
$x\to0^+$ the ratio $\to\infty$ and $\arctan\to\tfrac\pi2$, giving $V\to V_0$. The two forms agree
to $\sim10^{-4}$ (e.g. $V(0.3,0.5)=4.731$ both ways), and `slot_potential_closed` returns $0$ on
$y=0$ and $\sim10^{-16}$ on $y=a$ — the grounded plates.

### P5.  Uniqueness via relaxation  *(Gr §3.1.5, p.119)*
A harmonic function equals the average of its neighbours, so on a grid each
interior node satisfies $V_{i,j}=\tfrac14(V_{i+1,j}+V_{i-1,j}+V_{i,j+1}+V_{i,j-1})$.
Argue that iterating this update from *any* starting guess converges to the
single potential fixed by the boundary (the first uniqueness theorem). Take the
boundary potential $V=V_0\,x/L$, which is linear and therefore harmonic, and
predict the interior. *Check:* `solve_laplace_2d(lambda x, y: 10.0*x)` relaxes to
$V=10x$ at every interior node, independent of the initial interior values.

**Solution.** Discretizing $\nabla^2V=0$ with the 5-point Laplacian gives
$V_{i+1,j}+V_{i-1,j}+V_{i,j+1}+V_{i,j-1}-4V_{i,j}=0$, i.e. the mean-value property
$$V_{i,j}=\tfrac14\bigl(V_{i+1,j}+V_{i-1,j}+V_{i,j+1}+V_{i,j-1}\bigr).$$
Each Gauss–Seidel sweep overwrites every interior node with its neighbour-average while the
boundary stays pinned. Any error field is itself discrete-harmonic and zero on the boundary, so by
the discrete maximum principle it can have no interior extremum and must vanish — the iteration
contracts to the *one* interior consistent with the boundary, exactly the **first uniqueness
theorem**. For boundary data $V=V_0x/L$, the linear $V=V_0x/L$ is harmonic
($\partial_x^2=\partial_y^2=0$) and already obeys the averaging, so it *is* that unique interior.
Hence `solve_laplace_2d(lambda x, y: 10.0*x)` relaxes to $V(0.65,0.35)=6.500=10\times0.65$ at every
node, independent of the zeroed initial guess.
