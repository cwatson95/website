# RE-12 — Problems

Work them by hand, then check with `code/geodesics.py`. Sources in `../refs.md`.

### P1. Geodesics of flat spacetime  *(Zee §V.4; cpope §5.1)*
Show that in Minkowski space (`Γ = 0`) the geodesic equation reduces to
`ẍ^μ = 0`, so geodesics are straight lines `x^μ(λ) = x_0^μ + λ\,\dot x_0^μ` traced
at constant 4-velocity. Why does this *have* to be true given the equivalence
principle?
*Answer:* `Γ` vanishes for a constant metric, leaving `ẍ^μ=0`; a free particle in
an inertial frame moves uniformly — special relativity is the local limit of GR.
*Check:* `geodesic_rhs(minkowski_metric(), x, v)` `→ [0,0,0,0]` for any `x,v`;
`integrate_geodesic(...)` keeps `v` constant (`test_flat_geodesic_is_a_straight_line`).

**Solution.** The geodesic equation is $\ddot x^\mu + \Gamma^\mu{}_{\nu\rho}\,\dot x^\nu\dot x^\rho = 0$.
For the constant Minkowski metric $\eta_{\mu\nu}=\mathrm{diag}(-1,1,1,1)$ every derivative
$\partial_\lambda\eta_{\mu\nu}=0$, so each Christoffel symbol
$\Gamma^\mu{}_{\nu\rho}=\tfrac12\eta^{\mu\lambda}(\partial_\nu\eta_{\lambda\rho}+\partial_\rho\eta_{\lambda\nu}-\partial_\lambda\eta_{\nu\rho})=0$
vanishes. The equation collapses to $\ddot x^\mu=0$, which integrates twice to
$$x^\mu(\lambda)=x_0^\mu+\lambda\,\dot x_0^\mu,$$
a straight line traced at constant 4-velocity. This *must* hold because the equivalence
principle says a freely falling frame is locally inertial — there special relativity applies
and a free particle moves uniformly, so GR has to reduce to $\ddot x^\mu=0$ in that limit.
Hence `geodesic_rhs(minkowski_metric(), x, v)` returns `[0,0,0,0]` for any `x,v`.

### P2. Read Γ off the action  *(Zee §II.2; cpope §5.1)*
For the 2-sphere `g = diag(a², a²sin²θ)`, write the geodesic Lagrangian
`L = ½a²(θ̇² + sin²θ\,φ̇²)` and apply the Euler–Lagrange equations to read off
`Γ^θ_{φφ}` and `Γ^φ_{θφ}`. Hence the `θ`-equation `θ̈ − sinθcosθ\,φ̇² = 0`.
*Answer:* `Γ^θ_{φφ} = −sinθcosθ`, `Γ^φ_{θφ} = cotθ`; so `θ̈ = sinθcosθ\,φ̇²`.
*Check:* `geodesic_rhs(sphere_metric(1), [1.0,0], [0,1])[0]` `= sin1·cos1 ≈ 0.45465`,
and `euler_lagrange_gives_christoffel(...)` returns the same — the variational route
reproduces `Γ` (`test_variational_equation_reproduces_christoffel`).

**Solution.** With $L=\tfrac12 a^2(\dot\theta^2+\sin^2\theta\,\dot\varphi^2)$, the Euler–Lagrange
equation for $\theta$ uses $\partial L/\partial\dot\theta=a^2\dot\theta$ and
$\partial L/\partial\theta=a^2\sin\theta\cos\theta\,\dot\varphi^2$:
$$\frac{d}{d\lambda}\big(a^2\dot\theta\big)-a^2\sin\theta\cos\theta\,\dot\varphi^2=0
\;\Longrightarrow\;\ddot\theta-\sin\theta\cos\theta\,\dot\varphi^2=0.$$
Matching $\ddot\theta+\Gamma^\theta{}_{\varphi\varphi}\dot\varphi^2=0$ gives
$\Gamma^\theta{}_{\varphi\varphi}=-\sin\theta\cos\theta$. The $\varphi$-equation
$\frac{d}{d\lambda}(a^2\sin^2\theta\,\dot\varphi)=0$ expands to
$\ddot\varphi+2\cot\theta\,\dot\theta\dot\varphi=0$, so $\Gamma^\varphi{}_{\theta\varphi}=\cot\theta$.
At $\theta=1,\dot\varphi=1$ the acceleration is $\ddot\theta=\sin1\cos1\approx0.45465$ — exactly
what `geodesic_rhs(sphere_metric(1), [1.0,0], [0,1])[0]` and `euler_lagrange_gives_christoffel`
both return.

### P3. Which circle is a geodesic?  *(cpope §5)*
On the sphere, the equator `θ = π/2` and a circle of latitude `θ = θ_0 ≠ π/2` are
both "circles." Show only the equator is a geodesic. *(Hint: evaluate the
`θ`-equation from P2 on each.)*
*Answer:* On the equator `cosθ = 0` ⟹ `θ̈ = 0`, consistent with `θ ≡ π/2`. On a
latitude `θ̈ = sinθ_0cosθ_0\,φ̇² ≠ 0`, so staying at `θ_0` requires an external
(non-geodesic) force — it is *not* free fall.
*Check:* `is_geodesic(sphere_metric(1), equator, dtau)` `→ True`;
`is_geodesic(..., latitude, dtau)` `→ False` (`test_sphere_equator_is_geodesic_latitude_is_not`).

**Solution.** From P2 the $\theta$-equation of a geodesic is $\ddot\theta=\sin\theta\cos\theta\,\dot\varphi^2$.
On the **equator** $\theta=\pi/2$, $\cos(\pi/2)=0$, so the right side vanishes: $\ddot\theta=0$,
consistent with holding $\theta\equiv\pi/2$ (where $\dot\theta=\ddot\theta=0$) — the equator
solves the geodesic equation and is a great circle. On a **latitude** $\theta=\theta_0\ne\pi/2$,
staying put forces $\dot\theta=\ddot\theta=0$, yet the equation demands
$$\ddot\theta=\sin\theta_0\cos\theta_0\,\dot\varphi^2\ne0,$$
a contradiction: maintaining that circle needs a non-geodesic (external) force, so it is not
free fall. Hence `is_geodesic(...)` returns `True` on the equator and `False` on the latitude.

### P4. Maximal aging / the twin paradox  *(RE-05 §3; Zee §V.4)*
Between `A=(0,0,0,0)` and `B=(10,0,0,0)`, compare the proper time of the inertial
(straight) worldline with a "tent" worldline that detours to `x=3` at the midpoint
and back. Which twin is older?
*Answer:* straight `τ = √(10²) = 10`; tent `τ = 2√(5² − 3²) = 2·4 = 8`. The
inertial twin ages **most** — the geodesic maximises proper time (reversed
triangle inequality).
*Check:* `action_length(minkowski_metric(), straight) = 10.0` vs
`action_length(..., tent) = 8.0` (`test_maximal_aging…`).

**Solution.** Proper time is $\tau=\int ds=\int\sqrt{\lvert -dt^2+dx^2\rvert}$ (mostly-plus,
timelike branch). The straight worldline keeps $\Delta x=0$, so $\tau=\sqrt{\Delta t^2}=\sqrt{10^2}=10$.
The tent is two legs, each with $\Delta t=5,\ \Delta x=3$, giving $ds^2=-25+9=-16$ and
$\sqrt{\lvert-16\rvert}=4$ per leg:
$$\tau_{\text{tent}}=2\sqrt{5^2-3^2}=2\cdot4=8.$$
The lone minus sign reverses the triangle inequality, so the inertial (straight) twin ages
**most** — maximal aging — while the bent twin returns younger ($8<10$). This matches
`action_length(...) = 10.0` (straight) vs `8.0` (tent).

### P5. Conserved energy & angular momentum  *(notes §5)*
Schwarzschild has Killing vectors `∂_t` and `∂_φ`. Write the conserved
`E = −g_{tt}\dot t = (1−2M/r)\dot t` and `L = g_{φφ}\dot φ = r²sin²θ\,\dot φ`.
For `M=1`, a particle at `r=10`, `θ=π/2` with `\dot t = 1.2`, compute `E`.
*Answer:* `E = (1 − 2/10)·1.2 = 0.96` (the code returns `g_{tt}\dot t = −0.96`,
i.e. `−E`, since `killing_conserved` reports `ξ·p = g_{tt}\dot t`).
*Check:* `killing_conserved(schwarzschild_metric(1), [1,0,0,0], [0,10,π/2,0],
[1.2,0.2,0,0.04]) = −0.96`; both `E` and `L` stay constant along an integrated
orbit whose `r` swings 10→12.5 (`test_killing_energy_and_momentum…`).

**Solution.** For the Killing vector $\xi=\partial_t=(1,0,0,0)$ the conserved projection is
$\xi\cdot p=g_{\mu\nu}\xi^\mu\dot x^\nu=g_{tt}\dot t=-(1-2M/r)\dot t\equiv-E$. With $M=1,\ r=10,\ \dot t=1.2$:
$$E=(1-2/10)\cdot1.2=0.8\cdot1.2=0.96.$$
Likewise $\xi=\partial_\varphi$ gives $L=g_{\varphi\varphi}\dot\varphi=r^2\sin^2\theta\,\dot\varphi$.
Each is constant along any geodesic because
$\frac{dQ}{d\lambda}=(\nabla_\mu\xi_\nu)\dot x^\mu\dot x^\nu+\xi_\nu\,\dot x^\mu\nabla_\mu\dot x^\nu=0$
(first term: the symmetric $\dot x^\mu\dot x^\nu$ contracted with the antisymmetric Killing
tensor $\nabla_{(\mu}\xi_{\nu)}=0$; second term: the geodesic equation). The code reports
$\xi\cdot p=g_{tt}\dot t=-0.96=-E$, matching `killing_conserved(...) = −0.96`.

### P6. Light rays stay light  *(notes §2,§4; cpope §5.1 affine parameter)*
Argue that along an *affine* geodesic the tangent norm `g_{μν}\dot x^μ\dot x^ν` is
constant, so a null tangent (`= 0`, a photon) stays null and a timelike tangent
stays timelike. Why can a geodesic therefore never turn light into matter?
*Answer:* `d/dλ(g_{μν}\dot x^μ\dot x^ν) = 2\dot x_ν(\dot x^μ\nabla_μ\dot x^ν) = 0`
by the geodesic equation; the norm — hence the causal character — is conserved.
*Check:* a null ray in Schwarzschild keeps `2L ≈ 0` as it climbs `r=10→14`
(`test_null_geodesic_stays_null`); a sphere great circle keeps `2L` constant
(`test_affine_parameter_gives_constant_speed`).

**Solution.** Let $N=g_{\mu\nu}\dot x^\mu\dot x^\nu=\dot x_\nu\dot x^\nu$ be the tangent norm.
Differentiating along the curve and using metric compatibility ($\nabla_\mu g_{\alpha\beta}=0$),
$$\frac{dN}{d\lambda}=\dot x^\mu\nabla_\mu(\dot x_\nu\dot x^\nu)=2\dot x_\nu\,(\dot x^\mu\nabla_\mu\dot x^\nu)=0$$
by the geodesic equation $\dot x^\mu\nabla_\mu\dot x^\nu=0$. So $N$ is constant: a null tangent
($N=0$) stays null and a timelike tangent ($N<0$ in mostly-plus) stays timelike — the causal
character is frozen. A geodesic can therefore never convert a photon (null) into matter
(timelike). This is exactly why a Schwarzschild null ray keeps $2L\approx0$ from $r=10\to14$
and a sphere great circle keeps $2L=g_{\mu\nu}\dot x^\mu\dot x^\nu$ constant.
