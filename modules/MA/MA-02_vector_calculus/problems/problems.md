# MA-02 — Problems

Work by hand, then check with `code/vector_calculus.py`. Citations in `../refs.md`.

### P1.  The two second-derivative identities  *(Griffiths 4e §1.2.7, p.23)*
Prove for any smooth f and **F** that ∇×(∇f) = **0** and ∇·(∇×**F**) = 0.
*Check:* `curl(gradient(f))` and `divergence(curl(F))` return ~0 for any fields.

**Solution.** Both follow from equality of mixed partials, $\partial_i\partial_j=\partial_j\partial_i$. The $x$-component of $\nabla\times(\nabla f)$ is
$$[\nabla\times(\nabla f)]_x=\partial_y(\partial_z f)-\partial_z(\partial_y f)=\frac{\partial^2 f}{\partial y\,\partial z}-\frac{\partial^2 f}{\partial z\,\partial y}=0,$$
and the $y,z$ components vanish the same way, so $\nabla\times(\nabla f)=\mathbf 0$. For the divergence of a curl,
$$\nabla\cdot(\nabla\times\mathbf F)=\partial_x(\partial_yF_z-\partial_zF_y)+\partial_y(\partial_zF_x-\partial_xF_z)+\partial_z(\partial_xF_y-\partial_yF_x),$$
and the six terms cancel in pairs (e.g. $\partial_x\partial_yF_z-\partial_y\partial_xF_z=0$), giving $0$. This is why `curl(gradient(f))` and `divergence(curl(F))` return $\sim0$ (to finite-difference roundoff) for any smooth fields.

### P2.  Gradient of a radial function  *(Boas 3e §6, p.290)*
For f = r = √(x²+y²+z²) show ∇r = **r̂** = **r**/r, and for f = rⁿ show ∇(rⁿ) = n r^{n−1} **r̂**.
*Check:* `gradient(lambda x,y,z: (x*x+y*y+z*z)**0.5)(1,2,2)` ≈ (1,2,2)/3.

**Solution.** With $r=\sqrt{x^2+y^2+z^2}$, differentiate $r^2=x^2+y^2+z^2$: $\,2r\,\partial_x r=2x$, so $\partial_x r=x/r$ (likewise $y/r,\,z/r$). Hence
$$\nabla r=\Big(\frac xr,\frac yr,\frac zr\Big)=\frac{\mathbf r}{r}=\hat{\mathbf r}.$$
By the chain rule $\nabla(r^n)=n\,r^{n-1}\nabla r=n\,r^{n-1}\hat{\mathbf r}$. At $(1,2,2)$, $r=\sqrt{1+4+4}=3$, so $\nabla r=(1,2,2)/3=(0.3333,0.6667,0.6667)$ — exactly what `gradient(...)(1,2,2)` returns.

### P3.  Stokes' theorem on a disk  *(Boas 3e §11, p.324; Griffiths 4e §1.3.5, p.34)*
For **F** = (−y, x, 0) compute ∇×**F**, then verify ∮**F**·d**l** around the unit
circle equals ∬(∇×**F**)·d**S** over the disk. *(Both = 2π.)*
*Check:* `line_integral(F, circle, 0, 2*pi)` ≈ `curl(F)(0,0,0)[2] * pi`.

**Solution.** The curl is
$$\nabla\times\mathbf F=\big(\partial_y0-\partial_z x,\ \partial_z(-y)-\partial_x0,\ \partial_x x-\partial_y(-y)\big)=(0,0,2).$$
Parametrize the circle by $\mathbf l(t)=(\cos t,\sin t,0)$, so $d\mathbf l=(-\sin t,\cos t,0)\,dt$ and $\mathbf F\cdot d\mathbf l=(\sin^2t+\cos^2t)\,dt=dt$; thus $\oint\mathbf F\cdot d\mathbf l=\int_0^{2\pi}dt=2\pi$. The surface side, with $d\mathbf S=\hat{\mathbf z}\,dA$, is $\iint(0,0,2)\cdot\hat{\mathbf z}\,dA=2\,(\pi\cdot1^2)=2\pi$. Both equal $2\pi$, matching `line_integral` $=6.28319=$ `curl(F)(0,0,0)[2]*pi`.

### P4.  Divergence theorem on a sphere  *(Boas 3e §10, p.314; Griffiths 4e §1.3.4, p.31)*
For **F** = **r** = (x, y, z) show ∇·**F** = 3, hence the flux through a sphere of
radius R is 3·(4/3)πR³ = 4πR³. *(For R=1, 4π.)*
*Check:* `surface_flux(F, sphere, 0, pi, 0, 2*pi)` ≈ 4π.

**Solution.** The divergence is
$$\nabla\cdot\mathbf r=\frac{\partial x}{\partial x}+\frac{\partial y}{\partial y}+\frac{\partial z}{\partial z}=1+1+1=3.$$
By the divergence theorem the outward flux through the sphere of radius $R$ equals the volume integral
$$\oint_{\partial V}\mathbf r\cdot d\mathbf S=\int_V(\nabla\cdot\mathbf r)\,dV=3\int_V dV=3\cdot\tfrac43\pi R^3=4\pi R^3.$$
For $R=1$ this is $4\pi\approx12.566$. The midpoint-rule `surface_flux` returns $\approx12.568$, agreeing with $4\pi$ to grid resolution.

### P5.  A conservative field  *(Griffiths 4e §1.3.3, p.29)*
Show **F** = (yz, xz, xy) is conservative (curl = 0) with potential f = xyz, and
that ∫**F**·d**l** from (0,0,0) to (1,1,1) is path-independent and equals 1.
*Check:* `curl(F)` ≈ 0; `line_integral(gradient(lambda x,y,z: x*y*z), path, 0, 1)` ≈ 1.

**Solution.** Compute the curl of $\mathbf F=(yz,xz,xy)$:
$$\nabla\times\mathbf F=\big(\partial_y(xy)-\partial_z(xz),\ \partial_z(yz)-\partial_x(xy),\ \partial_x(xz)-\partial_y(yz)\big)=(x-x,\,y-y,\,z-z)=\mathbf 0,$$
so $\mathbf F$ is conservative. The scalar $f=xyz$ has $\nabla f=(yz,xz,xy)=\mathbf F$, so it is the potential. By the fundamental theorem for gradients the integral is path-independent:
$$\int_{(0,0,0)}^{(1,1,1)}\mathbf F\cdot d\mathbf l=f(1,1,1)-f(0,0,0)=1-0=1.$$
Hence `curl(F)` $\approx\mathbf0$ and `line_integral(gradient(...), path, 0, 1)` $=1.0$.
