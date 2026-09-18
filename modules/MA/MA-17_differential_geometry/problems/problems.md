# MA-17 — Problems

Work by hand, then check with `code/diffgeo.py`. Citations in `../refs.md`.

### P1.  d² = 0 = the two vector identities  *(Warner p.65; de Rham §4 p.17)*
Show that, in R³, d on a 0/1/2-form is grad/curl/div, so d²=0 means curl(grad f)=0
and div(curl V)=0. Verify both at a point. *Check:* `curl(gradient(f))(p)`,
`divergence(curl(V))(p)` ≈ 0.

**Solution.** Realize forms in $\mathbb R^3$: a 0-form $f$ has $df=\partial_i f\,dx^i$ (components $\nabla f$); a 1-form $\omega=V_i\,dx^i$ has $d\omega$ dual to $\nabla\times V$; a 2-form's $d$ is $\nabla\cdot V$. Nilpotency $d^2=0$ then reads
$$d(df)=0\Rightarrow\nabla\times(\nabla f)=0,\qquad d(d\omega)=0\Rightarrow\nabla\cdot(\nabla\times V)=0.$$
Both hold because $\varepsilon$ is antisymmetric while mixed partials are symmetric: $[\nabla\times\nabla f]_i=\varepsilon_{ijk}\partial_j\partial_k f=0$ and $\nabla\cdot(\nabla\times V)=\varepsilon_{ijk}\partial_i\partial_j V_k=0$ (antisymmetric $\times$ symmetric $=0$). At $p=(0.6,-0.4,0.9)$ the code gives `curl(gradient(f))(p)` $=[0,0,0]$ and `divergence(curl(V))(p)` $=0$, both $\approx 0$.

### P2.  Wedge product antisymmetry  *(Warner §2, p.56)*
Show dx∧dy = −dy∧dx and hence dx∧dx = 0. Why does this force a p-form to vanish
when p exceeds the dimension? (Pen-and-paper.)

**Solution.** The wedge is antisymmetric on 1-forms *by definition*: $dx^i\wedge dx^j=-dx^j\wedge dx^i$. Setting $j=i$ gives $dx^i\wedge dx^i=-dx^i\wedge dx^i$, hence $dx^i\wedge dx^i=0$ — a repeated differential annihilates. A basis $p$-form $dx^{i_1}\wedge\cdots\wedge dx^{i_p}$ is therefore nonzero only when the indices $i_1,\dots,i_p$ are all **distinct**. On an $n$-dimensional manifold each index runs over only $n$ values, so for $p>n$ the pigeonhole principle forces a repeat in every term ⇒ every $p$-form vanishes (the top nonzero form is the $n$-form, the volume form). This is the same antisymmetry that makes $\varepsilon_{ij\ldots}=0$ on a repeated index in `~MA-16`.

### P3.  Christoffel symbols of the sphere  *(Boas §10 p.529; ~RE-09)*
From g=diag(a², a²sin²θ) compute Γᶿ_φφ=−sinθcosθ and Γᶲ_θφ=cotθ by the formula
Γᵏ_ij=½gᵏˡ(∂ᵢg_jl+∂ⱼg_il−∂ₗg_ij). *Check:* `christoffel(sphere_metric(1), [theta, phi])`.

**Solution.** With $(\theta,\phi)$ and $g=\operatorname{diag}(a^2,\,a^2\sin^2\theta)$, the only nonzero metric derivative is $\partial_\theta g_{\phi\phi}=2a^2\sin\theta\cos\theta$, and $g^{\theta\theta}=1/a^2,\ g^{\phi\phi}=1/(a^2\sin^2\theta)$. Then
$$\Gamma^\theta_{\phi\phi}=\tfrac12 g^{\theta\theta}(-\partial_\theta g_{\phi\phi})=\tfrac12\frac1{a^2}(-2a^2\sin\theta\cos\theta)=-\sin\theta\cos\theta,$$
$$\Gamma^\phi_{\theta\phi}=\tfrac12 g^{\phi\phi}(\partial_\theta g_{\phi\phi})=\tfrac12\frac1{a^2\sin^2\theta}\,2a^2\sin\theta\cos\theta=\cot\theta.$$
At $\theta=0.9$ these are $-0.48692$ and $0.79355$ — exactly the `Gam[0][1][1]` and `Gam[1][0][1]` entries returned by `christoffel(sphere_metric(1), [theta, phi])`.

### P4.  Gaussian curvature of the sphere  *(Theorema Egregium; ~RE-11)*
Compute the Riemann tensor of the unit sphere and show Rᶿ_φθφ=sin²θ, hence the
scalar curvature R=2 and K=1. Repeat for radius a → K=1/a². *Check:*
`gaussian_curvature_2d(sphere_metric(a), [theta, phi])` ≈ 1/a².

**Solution.** Using the unit-sphere Christoffels $\Gamma^\theta_{\phi\phi}=-\sin\theta\cos\theta,\ \Gamma^\phi_{\theta\phi}=\Gamma^\phi_{\phi\theta}=\cot\theta$ (P3 with $a=1$),
$$R^\theta{}_{\phi\theta\phi}=\partial_\theta\Gamma^\theta_{\phi\phi}-\partial_\phi\Gamma^\theta_{\theta\phi}+\Gamma^\theta_{\theta\lambda}\Gamma^\lambda_{\phi\phi}-\Gamma^\theta_{\phi\lambda}\Gamma^\lambda_{\theta\phi}.$$
Only two terms survive: $\partial_\theta(-\sin\theta\cos\theta)=\sin^2\theta-\cos^2\theta$ and $-\Gamma^\theta_{\phi\phi}\Gamma^\phi_{\theta\phi}=-(-\sin\theta\cos\theta)\cot\theta=\cos^2\theta$, so $R^\theta{}_{\phi\theta\phi}=\sin^2\theta$. Contracting gives $R_{\phi\phi}=\sin^2\theta,\ R_{\theta\theta}=1$, hence $R=g^{\theta\theta}R_{\theta\theta}+g^{\phi\phi}R_{\phi\phi}=1+\frac1{\sin^2\theta}\sin^2\theta=2$ and $K=R/2=1$. A radius-$a$ sphere scales $g$ by $a^2$, dividing $R$ by $a^2$, so $K=1/a^2$. `gaussian_curvature_2d(sphere_metric(2), …)` returns $0.25000=1/2^2$, matching $1/a^2$.

### P5.  The plane is flat in any coordinates  *(Theorema Egregium)*
Show the polar metric g=diag(1, r²) has all Christoffel symbols arranged so that
R=0 — the r² is a coordinate artifact, not curvature. *Check:*
`gaussian_curvature_2d(plane_polar_metric(), [r, 0])` ≈ 0.

**Solution.** For $g=\operatorname{diag}(1,r^2)$ in $(r,\theta)$ the only nonzero metric derivative is $\partial_r g_{\theta\theta}=2r$, giving
$$\Gamma^r_{\theta\theta}=\tfrac12 g^{rr}(-\partial_r g_{\theta\theta})=-r,\qquad \Gamma^\theta_{r\theta}=\Gamma^\theta_{\theta r}=\tfrac12 g^{\theta\theta}\partial_r g_{\theta\theta}=\frac1{2r^2}\,2r=\frac1r.$$
The curvature component is then
$$R^r{}_{\theta r\theta}=\partial_r\Gamma^r_{\theta\theta}-\partial_\theta\Gamma^r_{r\theta}+\Gamma^r_{r\lambda}\Gamma^\lambda_{\theta\theta}-\Gamma^r_{\theta\lambda}\Gamma^\lambda_{r\theta}=\partial_r(-r)-\Gamma^r_{\theta\theta}\Gamma^\theta_{r\theta}=-1-(-r)\tfrac1r=0.$$
Every component vanishes, so $R=0$ and $K=0$: the $r^2$ merely records that $\partial_\theta$ lengthens with $r$ — a coordinate artifact, not curvature. `gaussian_curvature_2d(plane_polar_metric(), [r, 0])` $\approx 0$, matching.

### P6.  Intrinsic vs extrinsic  *(Theorema Egregium; ~RE-10)*
Argue why a sheet of paper (K=0) can be rolled into a cylinder (still K=0) without
stretching, but cannot be wrapped on a sphere (K=1/a²) without tearing — and why
this is the reason every flat map of the Earth distorts areas. (Pen-and-paper.)

**Solution.** Theorema Egregium states that $K$ is an *isometry invariant* — computable from the metric (intrinsic distances) alone, independent of the embedding. Rolling a flat sheet ($K=0$) into a cylinder bends it in space but changes no in-surface distance, so the cylinder is also intrinsically flat, $K=0$; the map is an isometry and needs no stretching. A sphere has $K=1/a^2\ne0$; since an isometry must preserve $K$, no distance-preserving map exists between a $K=0$ sheet and a $K\ne0$ sphere — wrapping must stretch or tear. The same obstruction means no planar chart of the Earth can preserve all distances and areas at once: every flat map distorts (Mercator inflates polar areas; equal-area projections shear shapes). This intrinsic-curvature fact is why "gravity is geometry" in `~RE-10`.
