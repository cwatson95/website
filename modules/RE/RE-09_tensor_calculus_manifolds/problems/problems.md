# RE-09 — Problems

Work them by hand, then check with `code/covariant_derivative.py`. Sources in
`../refs.md` (Zee §V.5–V.6; cpope §4–5; the connection itself is MA-17).
All sphere problems use the unit round sphere `g = diag(1, sin²θ)`.

### P1. Christoffel symbols of the sphere  *(cpope §4.4, Eq. 4.47; Zee §V.6)*
From `Γ^k_{ij} = ½ g^{kl}(∂_i g_{jl}+∂_j g_{il}−∂_l g_{ij})` and `g=diag(1,sin²θ)`,
the only nonzero derivative is `∂_θ g_{φφ}=2\sinθ\cosθ`. Show
`Γ^θ_{φφ}=−\sinθ\cosθ`, `Γ^φ_{θφ}=Γ^φ_{φθ}=\cotθ`, and that **all other**
components vanish.
*Answer:* at `θ=1.0`: `Γ^θ_{φφ}=−\sin1\cos1=−0.4546`, `Γ^φ_{θφ}=\cot1=0.6421`.
*Check:* `christoffel(diffgeo.sphere_metric(1.0),[1.0,0.4])` → `Gam[0][1][1]≈−0.4546`,
`Gam[1][0][1]≈0.6421`.

**Solution.** The inverse metric is $g^{\theta\theta}=1$, $g^{\phi\phi}=1/\sin^2\theta$, and the only nonzero derivative is $\partial_\theta g_{\phi\phi}=2\sin\theta\cos\theta$. Substituting into $\Gamma^k_{ij}=\tfrac12 g^{kl}(\partial_i g_{jl}+\partial_j g_{il}-\partial_l g_{ij})$,
$$\Gamma^\theta_{\phi\phi}=\tfrac12 g^{\theta\theta}\big(-\partial_\theta g_{\phi\phi}\big)=-\sin\theta\cos\theta,$$
$$\Gamma^\phi_{\theta\phi}=\tfrac12 g^{\phi\phi}\big(\partial_\theta g_{\phi\phi}\big)=\frac{2\sin\theta\cos\theta}{2\sin^2\theta}=\cot\theta.$$
The lower pair is symmetric so $\Gamma^\phi_{\phi\theta}=\Gamma^\phi_{\theta\phi}$, and any component needing a derivative other than $\partial_\theta g_{\phi\phi}$ is zero. At $\theta=1$: $-\sin1\cos1=-0.4546$ and $\cot1=0.6421$, matching `christoffel(...)` with `Gam[0][1][1]` $\approx-0.4546$ and `Gam[1][0][1]` $\approx0.6421$.

### P2. Flat space in curvy coordinates  *(cpope §4.3–4.4)*
The plane in polar coordinates has `g=diag(1,r²)` — flat, yet its Christoffels are
**not** zero. Compute them and explain why nonzero `Γ` does not mean curvature.
*Answer:* `Γ^r_{φφ}=−r`, `Γ^φ_{rφ}=Γ^φ_{φr}=1/r`, others 0. The `Γ` encode how the
polar basis vectors `(\hat r,\hatφ)` rotate as you move — a property of the
*coordinates*, not the space. Curvature is the connection's *derivative* (Riemann),
which is zero here (RE-11). *Check:* `christoffel(diffgeo.plane_polar_metric(),
[1.5,0.0])` → `Gam[0][1][1]≈−1.5`, `Gam[1][0][1]≈0.667`.

**Solution.** With $g_{rr}=1$, $g_{\phi\phi}=r^2$, the lone nonzero derivative is $\partial_r g_{\phi\phi}=2r$ and $g^{\phi\phi}=1/r^2$. The same Christoffel formula gives
$$\Gamma^r_{\phi\phi}=-\tfrac12 g^{rr}\partial_r g_{\phi\phi}=-r,\qquad \Gamma^\phi_{r\phi}=\tfrac12 g^{\phi\phi}\partial_r g_{\phi\phi}=\frac{2r}{2r^2}=\frac1r,$$
all others zero. They are nonzero even though the plane is flat: they merely record how the polar basis $(\hat r,\hat\phi)$ swings as you move - a property of the *coordinates*, not the space. Genuine curvature is the *derivative* of $\Gamma$ (the Riemann tensor), which vanishes here (RE-11). At $r=1.5$: $\Gamma^r_{\phi\phi}=-1.5$ and $\Gamma^\phi_{r\phi}=1/1.5=0.667$, matching `christoffel(...)` $\to$ `Gam[0][1][1]` $\approx-1.5$, `Gam[1][0][1]` $\approx0.667$.

### P3. Metric compatibility is the defining property  *(cpope §4.4; conceptual)*
Show that the Levi-Civita connection satisfies `∇_i g_{jk}=0` identically, by
expanding `∇_i g_{jk}=∂_i g_{jk}−Γ^l_{ij}g_{lk}−Γ^l_{ik}g_{jl}` and substituting the
Christoffel formula. Why does this guarantee that parallel transport preserves
lengths and angles, and that `∇` commutes with raising/lowering indices?
*Answer:* the three terms cancel term by term; metric-compatibility means
`d/dλ⟨V,W⟩=⟨∇V,W⟩+⟨V,∇W⟩=0` along a transport, so inner products (hence lengths and
angles) are invariant. *Check:* `metric_compatibility(diffgeo.sphere_metric(1.0),
[1.0,0.4])` and `…(diffgeo.plane_polar_metric(),[1.5,0.0])` → both `≈ 0`.

**Solution.** Lower the connection index, $\Gamma_{kij}\equiv g_{kl}\Gamma^l_{ij}=\tfrac12(\partial_i g_{jk}+\partial_j g_{ik}-\partial_k g_{ij})$, so that
$$\nabla_i g_{jk}=\partial_i g_{jk}-\Gamma^l_{ij}g_{lk}-\Gamma^l_{ik}g_{jl}=\partial_i g_{jk}-\Gamma_{kij}-\Gamma_{jik}.$$
Adding the two lowered symbols, the cross terms cancel and
$$\Gamma_{kij}+\Gamma_{jik}=\tfrac12\big(\partial_i g_{jk}+\partial_i g_{kj}\big)=\partial_i g_{jk},$$
so $\nabla_i g_{jk}=0$ identically. Metric-compatibility means $\tfrac{d}{d\lambda}\langle V,W\rangle=\langle\nabla V,W\rangle+\langle V,\nabla W\rangle=0$ along a transport, so lengths and angles are preserved and $\nabla$ commutes with raising/lowering. Confirmed: `metric_compatibility(...)` on the sphere and on the plane-polar metric both return $\approx0$ (the demo gives $0$ to machine precision).

### P4. Great circle vs circle of latitude  *(cpope §5; bridge to RE-12)*
A geodesic has zero covariant acceleration `ẍ^k=−Γ^k_{ij}ẋ^iẋ^j`. For a curve at
fixed colatitude `θ_0` traversed in `φ` at rate `\dotφ=ω` (so `ẋ=(0,ω)`), show
`ẍ^θ=\sinθ_0\cosθ_0\,ω²`. Deduce that the **equator** (`θ_0=π/2`) is a geodesic but
**every other latitude is not** — you must accelerate ("steer") to hold a latitude.
*Answer:* `ẍ^θ=−Γ^θ_{φφ}ω²=\sinθ_0\cosθ_0\,ω²`, which is 0 only at `θ_0=π/2` (or the
poles). *Check:* `geodesic_acceleration(g,[3.14159/2,0],[0,1])≈[0,0]` (equator);
`geodesic_acceleration(g,[1.0,0],[0,1])≈[0.4546,0]` (latitude — nonzero).

**Solution.** For a curve at fixed $\theta=\theta_0$ swept in $\phi$ at rate $\omega$, the tangent is $\dot x=(0,\omega)$, so in $\ddot x^k=-\Gamma^k_{ij}\dot x^i\dot x^j$ only the $(\phi,\phi)$ term survives:
$$\ddot x^\theta=-\Gamma^\theta_{\phi\phi}\,\omega^2=-(-\sin\theta_0\cos\theta_0)\,\omega^2=\sin\theta_0\cos\theta_0\,\omega^2,$$
while $\ddot x^\phi=-\Gamma^\phi_{\phi\phi}\omega^2=0$. This vanishes only when $\sin\theta_0\cos\theta_0=0$, i.e. at the equator $\theta_0=\pi/2$ (or the poles): the equator is a geodesic, every other latitude is not - you must supply $\ddot x^\theta$ ("steer") to hold it. Confirmed: `geodesic_acceleration(g,[3.14159/2,0],[0,1])` $\approx[0,0]$ versus `geodesic_acceleration(g,[1.0,0],[0,1])` $\approx[0.4546,0]$.

### P5. Holonomy = enclosed area  *(cpope §4.5–4.6, Eq. 4.117; Gauss–Bonnet)*
Parallel-transport a vector around the closed lat–long rectangle
`[θ_0,θ_0+Δθ]×[φ_0,φ_0+Δφ]` on the unit sphere. It returns **rotated** by an angle
equal to the enclosed area `\iint\sinθ\,dθ\,dφ=(\cosθ_0−\cos(θ_0{+}Δθ))Δφ` (because
`∫K\,dA` with `K=1`). For `θ_0=1.0, Δθ=Δφ=0.3` compute the predicted angle.
*Answer:* `(\cos1.0−\cos1.3)·0.3 = (0.5403−0.2675)·0.3 ≈ 0.0818` rad. *Check:*
transport `[1,0]` round `[[1,0],[1,0.3],[1.3,0.3],[1.3,0],[1,0]]` with
`parallel_transport(g,[1.0,0.0],loop,steps=400)`; the rotation of the returned
vector (measured in the local orthonormal frame) is `≈0.0818`. The **sign** flips if
you traverse the loop the other way; a zero-area (out-and-back) path leaves the
vector unchanged.

**Solution.** By Gauss-Bonnet the holonomy from transport round the loop equals the curvature integrated over the enclosed cap, $\Delta\alpha=\iint K\,dA$; on the unit sphere $K=1$, so it is simply the area:
$$\Delta\alpha=\int_{\phi_0}^{\phi_0+\Delta\phi}\!\!\int_{\theta_0}^{\theta_0+\Delta\theta}\sin\theta\,d\theta\,d\phi=\big(\cos\theta_0-\cos(\theta_0+\Delta\theta)\big)\,\Delta\phi.$$
For $\theta_0=1.0$, $\Delta\theta=\Delta\phi=0.3$ this is $(\cos1.0-\cos1.3)\cdot0.3=(0.5403-0.2675)\cdot0.3\approx0.0818$ rad. Transporting `[1,0]` around the rectangle and reading the rotation in the orthonormal frame gives $\approx0.0818$ (the demo measures $0.0818$); reversing the loop flips the sign, and a zero-area out-and-back path leaves the vector unchanged.

### P6. The equivalence principle, mathematically  *(cpope §4.7; → RE-10)*
The `Γ^k_{ij}` are **not** tensor components — their transformation law has an
inhomogeneous `∂²x'/∂x∂x` piece. Argue that one can therefore always choose
coordinates (geodesic normal / locally inertial) in which **`Γ=0` at a single chosen
point**, while what *cannot* be removed is `∂Γ` (the Riemann tensor). State the
physical content.
*Answer:* a free-falling observer can pick coordinates in which the connection
vanishes at their location — gravity is locally transformed away — but tidal
effects (`∂Γ ∼` Riemann) remain. This is the equivalence principle: gravitation is
the curvature of spacetime, not a force on a fixed background. *Check (conceptual):*
`metric_compatibility` and the flat-`η` tests show that when `g` is constant every
`Γ=0` — the local-inertial-frame limit at every point at once.

**Solution.** Under a coordinate change the connection picks up an inhomogeneous piece,
$$\Gamma'^k_{ij}=\frac{\partial x'^k}{\partial x^c}\frac{\partial x^a}{\partial x'^i}\frac{\partial x^b}{\partial x'^j}\,\Gamma^c_{ab}+\frac{\partial x'^k}{\partial x^c}\frac{\partial^2 x^c}{\partial x'^i\,\partial x'^j},$$
whose second term is not tensorial - so $\Gamma$ is not a tensor. At any chosen point $p$ one can pick coordinates (geodesic-normal / locally inertial) that make that term cancel $\Gamma(p)$, giving $\Gamma'^k_{ij}(p)=0$. What cannot be removed is $\partial\Gamma$ - the Riemann tensor, which transforms homogeneously. Physically a free-faller transforms gravity away *at their location* (the connection) but never the tidal field (the curvature): gravity is curvature, not a force on a fixed background. The flat-$\eta$ tests show the limiting case - when $g$ is constant every $\Gamma=0$, the locally inertial frame realised everywhere at once.
