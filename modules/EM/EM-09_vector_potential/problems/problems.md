# EM-09 — Problems

Work by hand, then check with `code/vector_potential.py`. Citations in
`../refs.md`; **Gr** = Griffiths 4e (printed pages).

### P1.  The vector potential of an infinite wire  *(Gr §5.4.1, p.243)*
A straight wire on the $z$-axis carries steady current $I$. Its vector potential
can be taken parallel to the current,
$$\mathbf A=-\frac{\mu_0 I}{2\pi}\ln\!\frac{s}{s_0}\,\hat{\mathbf z},\qquad
  s=\sqrt{x^2+y^2}.$$
Show that $\nabla\times\mathbf A=\dfrac{\mu_0 I}{2\pi s}\,\hat{\boldsymbol\varphi}$,
the EM-08 wire field, and that changing the reference radius $s_0$ only adds a
constant to $\mathbf A$ — a gauge transformation $\mathbf A\to\mathbf A+\nabla\lambda$
with $\lambda$ linear in $z$ — leaving $\mathbf B$ untouched. *Check:*
`wire_vector_potential(I)` then `B_from_A` reproduces `infinite_wire_field`
(`~EM-08`); re-run with a different `s0` and confirm `B_from_A` is unchanged.

**Solution.** For $\mathbf A=A_z(s)\hat{\mathbf z}$ the only surviving curl component is
azimuthal, $\nabla\times\mathbf A=-\partial_s A_z\,\hat{\boldsymbol\varphi}$. With
$A_z=-\frac{\mu_0 I}{2\pi}\ln(s/s_0)$,
$$\nabla\times\mathbf A=-\frac{\partial}{\partial s}\!\Big[-\frac{\mu_0 I}{2\pi}\ln\frac{s}{s_0}\Big]\hat{\boldsymbol\varphi}
  =\frac{\mu_0 I}{2\pi s}\,\hat{\boldsymbol\varphi},$$
the EM-08 wire field. Replacing $s_0\to s_0'$ shifts $A_z$ by the *constant*
$\frac{\mu_0 I}{2\pi}\ln(s_0'/s_0)$, i.e. $\mathbf A\to\mathbf A+\nabla\lambda$ with
$\lambda=\big[\tfrac{\mu_0 I}{2\pi}\ln(s_0'/s_0)\big]z$ linear in $z$; since
$\nabla\times\nabla\lambda=0$, $\mathbf B$ is untouched. At $(0.05,0,0)$ with $I=10$ A,
`B_from_A(wire_vector_potential(I))` returns $(0,\,4.0\times10^{-5},\,0)$ T, matching
`infinite_wire_field` for every `s0`.

### P2.  The magnetic moment of a current loop  *(Gr §5.4.3, p.252)*
A planar loop carrying current $I$ has magnetic moment $\mathbf m=I\int d\mathbf a
=I\,\mathbf a$ (Eq. 5.86), where $\mathbf a$ is the oriented area it bounds. Compute
$\mathbf m$ for (a) a circle of radius $R$ and (b) a square of side $L$, both in the
$xy$-plane, and confirm $\mathbf m$ depends only on the enclosed area, not the
shape. *Check:* `magnetic_dipole_moment(I, (0,0,math.pi*R**2))` for the circle
versus `magnetic_dipole_moment(I, (0,0,L**2))` for the square give the same
$\hat{\mathbf z}$-moment when $\pi R^2=L^2$.

**Solution.** Since $\mathbf m=I\int d\mathbf a=I\mathbf a$ is current times the *oriented
area*, only the enclosed area enters — the boundary shape is irrelevant. (a) Circle:
$\mathbf a=\pi R^2\hat{\mathbf z}$, so $\mathbf m=I\pi R^2\hat{\mathbf z}$. (b) Square:
$\mathbf a=L^2\hat{\mathbf z}$, so $\mathbf m=IL^2\hat{\mathbf z}$. Imposing $\pi R^2=L^2$
makes the two areas equal, hence $\mathbf m$ identical. For $I=3$ A, $R=0.02$ m (so
$L=\sqrt\pi\,R$), both `magnetic_dipole_moment` calls return
$m_z=3.770\times10^{-3}$ A·m² — equal to machine precision, confirming the moment depends
on area alone.

### P3.  The dipole potential and its $1/r^2$ falloff  *(Gr §5.4.3, Eq. 5.85, p.252)*
For $\mathbf m=m\,\hat{\mathbf z}$, write the dipole vector potential
$$\mathbf A_{\text{dip}}=\frac{\mu_0}{4\pi}\frac{\mathbf m\times\hat{\mathbf r}}{r^{2}}
  =\frac{\mu_0}{4\pi}\frac{m\sin\theta}{r^{2}}\,\hat{\boldsymbol\varphi},$$
purely azimuthal, and show $|\mathbf A|\propto 1/r^{2}$ along any fixed direction.
*Check:* `dipole_vector_potential(m)`; evaluate the magnitude at $(r,0,0)$ and
$(2r,0,0)$ and confirm the ratio is $2^2=4$.

**Solution.** For $\mathbf m=m\hat{\mathbf z}$ use $\hat{\mathbf z}\times\hat{\mathbf r}=\sin\theta\,\hat{\boldsymbol\varphi}$:
$$\mathbf A_{\text{dip}}=\frac{\mu_0}{4\pi}\frac{\mathbf m\times\hat{\mathbf r}}{r^2}
  =\frac{\mu_0}{4\pi}\frac{m\sin\theta}{r^2}\,\hat{\boldsymbol\varphi},$$
purely azimuthal. Along a fixed direction $\theta=\text{const}$ the magnitude
$|\mathbf A|=\frac{\mu_0}{4\pi}\frac{m\sin\theta}{r^2}\propto r^{-2}$, so doubling $r$
divides $|\mathbf A|$ by $2^2=4$. On the equatorial line $(r,0,0)$, $\theta=\pi/2$ and
$\sin\theta=1$. With $m=1$, `dipole_vector_potential` gives $|\mathbf A|=1.0\times10^{-5}$
at $(0.1,0,0)$ and $2.5\times10^{-6}$ at $(0.2,0,0)$, ratio exactly $4.0$.

### P4.  $\mathbf B=\nabla\times\mathbf A$ reproduces the dipole field  *(Gr §5.4.3, p.252)*
Take the curl of $\mathbf A_{\text{dip}}$ and obtain the magnetic dipole field
$$\mathbf B_{\text{dip}}=\frac{\mu_0}{4\pi}\frac{1}{r^{3}}
  \big[\,3(\mathbf m\cdot\hat{\mathbf r})\hat{\mathbf r}-\mathbf m\,\big].$$
Show the on-axis field ($\theta=0$) is $2(\mu_0/4\pi)m/r^{3}$ and the equatorial
field ($\theta=\pi/2$) is $-(\mu_0/4\pi)m/r^{3}$ — twice as large and opposite, the
same $2{:}1$ ratio as the *electric* dipole (`~EM-05`, Eq. 3.104) under
$(1/4\pi\varepsilon_0,\mathbf p)\to(\mu_0/4\pi,\mathbf m)$. *Check:*
`B_from_A(dipole_vector_potential(m))` matches `dipole_B_field_closed(m)`
pointwise; verify the axis value $\mathbf B(0,0,d)$ and the bisector value
$\mathbf B(d,0,0)$.

**Solution.** On axis ($\theta=0$) $\hat{\mathbf r}=\hat{\mathbf z}$ and $\mathbf m\cdot\hat{\mathbf r}=m$, so
$$\mathbf B=\frac{\mu_0}{4\pi}\frac{1}{r^3}\big[3m\hat{\mathbf z}-m\hat{\mathbf z}\big]
  =\frac{2\mu_0 m}{4\pi r^3}\,\hat{\mathbf z}.$$
On the equator ($\theta=\pi/2$) $\mathbf m\cdot\hat{\mathbf r}=0$, leaving
$\mathbf B=-\frac{\mu_0 m}{4\pi r^3}\hat{\mathbf z}$ — half as large and antiparallel, the
same $2{:}1$ ratio the electric dipole shows under $(1/4\pi\varepsilon_0,\mathbf p)\to(\mu_0/4\pi,\mathbf m)$.
With $m=1$, $d=0.1$, `dipole_B_field_closed` gives $\mathbf B(0,0,d)=(0,0,2.0\times10^{-4})$
and $\mathbf B(d,0,0)=(0,0,-1.0\times10^{-4})$, reproduced pointwise by
`B_from_A(dipole_vector_potential(m))`.

### P5.  The Coulomb gauge of the dipole potential  *(Gr §5.4.1, p.243)*
Verify directly that the dipole potential already satisfies the Coulomb gauge,
$\nabla\cdot\mathbf A_{\text{dip}}=0$, so no further fixing is needed. Then argue
that a gauge shift $\mathbf A\to\mathbf A+\nabla\lambda$ preserves $\mathbf B$ for
*any* $\lambda$, but preserves the Coulomb gauge only when $\lambda$ is harmonic,
$\nabla^2\lambda=0$ (e.g. $\lambda\propto z$). *Check:*
`coulomb_gauge_residual(dipole_vector_potential(m), point)` returns a normalized
value $\approx 0$ at several off-axis points.

**Solution.** Write $\mathbf A_{\text{dip}}=\frac{\mu_0}{4\pi}\frac{\mathbf m\times\mathbf r}{r^3}$
and apply $\nabla\cdot(f\mathbf F)=f\,\nabla\cdot\mathbf F+\mathbf F\cdot\nabla f$ with
$f=r^{-3}$, $\mathbf F=\mathbf m\times\mathbf r$. The first term vanishes because
$\nabla\cdot(\mathbf m\times\mathbf r)=\mathbf r\cdot(\nabla\times\mathbf m)-\mathbf m\cdot(\nabla\times\mathbf r)=0$
(both curls are zero); the second vanishes because
$(\mathbf m\times\mathbf r)\cdot\nabla r^{-3}=-3r^{-5}(\mathbf m\times\mathbf r)\cdot\mathbf r=0$
(the cross product is $\perp\mathbf r$). Hence $\nabla\cdot\mathbf A_{\text{dip}}=0$
identically — the Coulomb gauge already holds. A shift $\mathbf A\to\mathbf A+\nabla\lambda$
leaves $\mathbf B=\nabla\times\mathbf A$ unchanged for *any* $\lambda$, but preserves
$\nabla\cdot\mathbf A=0$ only when $\nabla^2\lambda=0$ — harmonic $\lambda$, e.g.
$\lambda\propto z$. Accordingly `coulomb_gauge_residual` returns $\sim10^{-8}$ at the
off-axis points $(0.1,0.05,0.08)$ etc., numerically zero.
