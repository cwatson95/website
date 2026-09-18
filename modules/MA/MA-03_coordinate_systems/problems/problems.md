# MA-03 — Problems

Work by hand, then check with `code/coordinates.py`. Citations in `../refs.md`.

### P1.  Spherical unit vectors  *(Griffiths 4e §1.4.1, p.38)*
Derive **ê_r**, **ê_θ**, **ê_φ** in Cartesian components and show they are
orthonormal and right-handed (**ê_r×ê_θ = ê_φ**).
*Check:* `sph_basis(theta, phi)` then MA-01 `dot`/`cross`/`norm`.

**Solution.** Each unit vector is the normalized derivative of $\mathbf r=r(s_\theta c_\phi,\,s_\theta s_\phi,\,c_\theta)$ along its coordinate, $\hat{\mathbf e}_i=\tfrac1{h_i}\partial\mathbf r/\partial q_i$ (s,c = sin,cos):
$$\partial_r\mathbf r=(s_\theta c_\phi,s_\theta s_\phi,c_\theta),\quad
\partial_\theta\mathbf r=r(c_\theta c_\phi,c_\theta s_\phi,-s_\theta),\quad
\partial_\phi\mathbf r=r s_\theta(-s_\phi,c_\phi,0),$$
with magnitudes $h_r=1,\,h_\theta=r,\,h_\phi=rs_\theta$, giving exactly the notes' $\hat{\mathbf e}_r,\hat{\mathbf e}_\theta,\hat{\mathbf e}_\phi$. Orthonormal: $|\hat{\mathbf e}_r|^2=s_\theta^2(c_\phi^2+s_\phi^2)+c_\theta^2=1$, and $\hat{\mathbf e}_r\!\cdot\!\hat{\mathbf e}_\theta=s_\theta c_\theta(c_\phi^2+s_\phi^2)-c_\theta s_\theta=0$ (similarly the other pairs vanish). Right-handed:
$$\hat{\mathbf e}_r\times\hat{\mathbf e}_\theta=(s_\theta s_\phi(-s_\theta)-c_\theta c_\theta s_\phi,\;c_\theta c_\theta c_\phi+s_\theta s_\theta c_\phi,\;0)=(-s_\phi,c_\phi,0)=\hat{\mathbf e}_\phi.$$
So `sph_basis` returns three vectors with `norm` $=1$, pairwise `dot` $=0$, and `cross(e_r,e_th)` $=$ `e_ph`.

### P2.  Volume of a sphere from the Jacobian  *(Boas 3e §5.4, p.258)*
Using dV = r² sinθ dr dθ dφ, integrate to get V = (4/3)πR³.
*Check:* `sph_jacobian(r, theta)` is the integrand factor; numerically integrate
it over r∈[0,R], θ∈[0,π], φ∈[0,2π].

**Solution.** With $dV=r^2\sin\theta\,dr\,d\theta\,d\phi$ the integrand separates, so the triple integral is a product of three one-dimensional integrals:
$$V=\int_0^R r^2\,dr\int_0^\pi\sin\theta\,d\theta\int_0^{2\pi}d\phi
=\frac{R^3}{3}\cdot\big[-\cos\theta\big]_0^\pi\cdot 2\pi
=\frac{R^3}{3}\cdot 2\cdot 2\pi=\frac{4}{3}\pi R^3.$$
The factor $r^2\sin\theta$ is precisely `sph_jacobian(r, theta)`. Numerically integrating it over the box for $R=1$ gives $V\approx 4.18878\approx \tfrac43\pi(1)^3=4.18879$.

### P3.  Scale factors ↔ Jacobian  *(Boas 3e Ch.10 §8, p.521)*
Show that for any orthogonal system the volume element factor equals the product
of the scale factors, J = h₁h₂h₃, and verify for cylindrical (J=ρ) and spherical
(J=r²sinθ). *Check:* compare `*_scale_factors` product to `*_jacobian`.

**Solution.** An orthogonal coordinate change spans a small box with edge vectors $h_i\,dq_i\,\hat{\mathbf e}_i$ along the orthonormal directions $\hat{\mathbf e}_i$. Its volume is the scalar triple product
$$dV=\big|h_1\hat{\mathbf e}_1\cdot(h_2\hat{\mathbf e}_2\times h_3\hat{\mathbf e}_3)\big|\,dq_1dq_2dq_3
=h_1h_2h_3\,\big|\hat{\mathbf e}_1\cdot(\hat{\mathbf e}_2\times\hat{\mathbf e}_3)\big|\,dq_1dq_2dq_3=h_1h_2h_3\,dq_1dq_2dq_3,$$
since for a right-handed orthonormal triad $\hat{\mathbf e}_1\cdot(\hat{\mathbf e}_2\times\hat{\mathbf e}_3)=1$. Hence $J=h_1h_2h_3$. Cylindrical $(1,\rho,1)$ gives $J=\rho$; spherical $(1,r,r\sin\theta)$ gives $J=r^2\sin\theta$ — exactly why the product of `*_scale_factors` equals `*_jacobian`.

### P4.  A vector in two bases  *(Griffiths 4e §1.4.1, p.38)*
The constant Cartesian vector **ẑ** has spherical components (cosθ, −sinθ, 0).
Confirm, and check that converting to spherical and back is the identity.
*Check:* `vector_to_spherical(0,0,1, theta, phi)` then `vector_from_spherical(...)`.

**Solution.** Components in the spherical basis are projections, $v_i=\hat{\mathbf z}\cdot\hat{\mathbf e}_i$. With $\hat{\mathbf z}=(0,0,1)$ and the basis from P1,
$$v_r=\hat{\mathbf z}\cdot\hat{\mathbf e}_r=c_\theta,\quad
v_\theta=\hat{\mathbf z}\cdot\hat{\mathbf e}_\theta=-s_\theta,\quad
v_\phi=\hat{\mathbf z}\cdot\hat{\mathbf e}_\phi=0,$$
so $\hat{\mathbf z}\to(\cos\theta,-\sin\theta,0)$. Reassembling, the $z$-component is $c_\theta\,c_\theta+(-s_\theta)(-s_\theta)=c_\theta^2+s_\theta^2=1$ and the $x,y$ parts cancel, returning $\hat{\mathbf z}$. At $\theta=50^\circ$, `vector_to_spherical(0,0,1,…)` gives $(0.642788,-0.766044,0)$ and `vector_from_spherical` returns $(0,0,1)$.

### P5.  Position is purely radial
Show that any point's position vector has spherical components (r, 0, 0), i.e.
**ê_r** points along **r**. *Check:* for random p, `sph_basis(theta, phi)[0]`
equals `unit(p)` from MA-01 (this is a test in the suite).

**Solution.** The Cartesian position of a point at $(r,\theta,\phi)$ is, by the spherical map,
$$\mathbf p=(r s_\theta c_\phi,\,r s_\theta s_\phi,\,r c_\theta)=r\,(s_\theta c_\phi,\,s_\theta s_\phi,\,c_\theta)=r\,\hat{\mathbf e}_r.$$
Projecting onto the basis: $v_r=\mathbf p\cdot\hat{\mathbf e}_r=r\,|\hat{\mathbf e}_r|^2=r$, while $v_\theta=r\,\hat{\mathbf e}_r\cdot\hat{\mathbf e}_\theta=0$ and $v_\phi=r\,\hat{\mathbf e}_r\cdot\hat{\mathbf e}_\phi=0$ by orthonormality — so the components are $(r,0,0)$. Equivalently $\hat{\mathbf e}_r=\mathbf p/|\mathbf p|=$ `unit(p)`; e.g. for $\mathbf p=(1.3,-0.7,2.1)$ both equal $(0.50641,-0.27268,0.81804)$, matching `sph_basis(theta, phi)[0]`.
