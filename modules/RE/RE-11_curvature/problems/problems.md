# RE-11 — Problems

Work them by hand, then check with `code/curvature.py`. Sources in `../refs.md`.

### P1. Gaussian curvature of the sphere  *(Zee §I.6; cpope §4.6)*
From the 2-sphere metric `g = diag(a², a²sin²θ)`, compute the scalar curvature and
hence `K = R/2`. Confirm it is constant `= 1/a²`.
*Answer:* `R = 2/a²`, `K = 1/a²`.
*Check:* `ricci_scalar(sphere_metric(2.0), [1.0, 0.5])` → 0.5; `gaussian_curvature_2d` → 0.25.

**Solution.** The round 2-sphere $g=\mathrm{diag}(a^2,\,a^2\sin^2\theta)$ has nonzero Christoffel
symbols $\Gamma^\theta{}_{\phi\phi}=-\sin\theta\cos\theta$ and $\Gamma^\phi{}_{\theta\phi}=\cot\theta$.
In the notes' convention the single independent Riemann component is
$$R^\theta{}_{\phi\theta\phi}=\partial_\theta\Gamma^\theta{}_{\phi\phi}-\Gamma^\theta{}_{\phi\phi}\,\Gamma^\phi{}_{\theta\phi}=-\cos2\theta+\cos^2\theta=\sin^2\theta.$$
Contracting gives $R_{\theta\theta}=1$, $R_{\phi\phi}=\sin^2\theta$, so the scalar curvature is
$$R=g^{\theta\theta}R_{\theta\theta}+g^{\phi\phi}R_{\phi\phi}=\frac1{a^2}+\frac{\sin^2\theta}{a^2\sin^2\theta}=\frac{2}{a^2},\qquad K=\frac R2=\frac1{a^2},$$
both constant. For $a=2$: $R=2/4=0.5$, $K=0.25$ — matching `ricci_scalar(sphere_metric(2.0), [1.0, 0.5])` → 0.5 and `gaussian_curvature_2d` → 0.25.

### P2. Horizon vs singularity  *(Zee §VII.2)*
Schwarzschild has `R_{μν}=0`, so all Ricci-based scalars vanish. Show the
Kretschmann scalar `K = 48M²/r⁶` is finite at `r = 2M` but diverges at `r = 0`.
Which is a *real* singularity?
*Answer:* only `r = 0` (K → ∞); `r = 2M` is a coordinate artefact (K finite).
*Check:* `kretschmann(schwarzschild_metric(1), [0, r, 1, 0.9])` ≈ `48/r⁶`; compare
`ricci(...)` ≈ 0.

**Solution.** Schwarzschild is a *vacuum* solution, $R_{\mu\nu}=0$, so every scalar built
from Ricci — including $R$ and $R_{\mu\nu}R^{\mu\nu}$ — vanishes identically. The full
Riemann tensor does **not** vanish, and the lowest invariant that sees it is the
Kretschmann scalar
$$K=R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}=\frac{48M^2}{r^6}.$$
At the horizon $r=2M$ this is $K=48M^2/(2M)^6=3/(4M^4)$, perfectly **finite** — and since
$K$ is a *scalar*, no coordinate change can make the curvature blow up there. The trouble
the metric shows at $r=2M$ lives only in the chart $(t,r)$: a **coordinate** singularity.
At $r=0$, by contrast, $K\to\infty$, an invariant divergence no chart can remove — the
**true physical** singularity. Numerically `kretschmann(schwarzschild_metric(1), [0,r,1,0.9])`
returns $1.17\times10^{-2}\approx48/4^6$ at $r=4$ while `ricci(...)` $\approx0$: Ricci-flat
yet genuinely curved.

### P3. Counting curvature  *(conceptual; notes §2)*
Use `n²(n²−1)/12` to count the independent components of Riemann in 2, 3, 4
dimensions. How many are *not* captured by the Ricci tensor in 4-D?
*Answer:* 1, 6, 20. In 4-D, Ricci is 10 components; the remaining **10** are the
Weyl tensor (the free gravitational field → RE-16).

**Solution.** The symmetry-reduced count is $N(n)=n^2(n^2-1)/12$. Plugging in,
$$N(2)=\frac{4\cdot3}{12}=1,\qquad N(3)=\frac{9\cdot8}{12}=6,\qquad N(4)=\frac{16\cdot15}{12}=20.$$
The Ricci tensor is symmetric, so it carries $n(n+1)/2$ numbers: $3$ in 2-D, $6$ in 3-D,
$10$ in 4-D. Comparing the two counts: in 2-D Riemann's single component is the Gaussian
curvature, fixed by $R$ alone; in 3-D Ricci's $6$ exactly matches Riemann's $6$, so **Ricci
determines Riemann completely** — no free field. In 4-D Riemann has $20$ but Ricci only
$10$, leaving
$$20-10=10$$
components untouched by Ricci — the **Weyl tensor**, the trace-free part of curvature that
survives in vacuum ($R_{\mu\nu}=0$ yet $R_{\mu\nu\rho\sigma}\neq0$, as in Schwarzschild) and
propagates as gravitational waves (RE-16).

### P4. Tidal focusing on the sphere  *(Zee §IX.3)*
For a geodesic moving in `φ` on the unit sphere, with separation `ξ = (1,0)` in
`θ`, compute the geodesic-deviation acceleration `A^θ`. Show positive curvature
focuses (`A·ξ < 0`).
*Answer:* `A^θ = −sin²θ` (toward the fiducial geodesic).
*Check:* `geodesic_deviation(sphere_metric(1), [1.0,0], [0,1], [1,0])` → `[-sin²(1), 0] ≈ [-0.708, 0]`.

**Solution.** On the unit 2-sphere $g=\mathrm{diag}(1,\sin^2\theta)$ the one independent
Riemann component is $R^\theta{}_{\phi\theta\phi}=\sin^2\theta$ (P1). The fiducial geodesic
runs in $\phi$, $u=(u^\theta,u^\phi)=(0,1)$, with neighbour separation $\xi=(1,0)$ in
$\theta$. The deviation equation keeps only the term with $b=d=\phi$, $c=\theta$:
$$A^\theta=-R^\theta{}_{bcd}\,u^b\xi^c u^d=-R^\theta{}_{\phi\theta\phi}\,(u^\phi)^2\xi^\theta=-\sin^2\theta .$$
Its sign is the physics: $A\cdot\xi=g_{\theta\theta}A^\theta\xi^\theta=-\sin^2\theta<0$, so the
neighbour accelerates **back toward** the fiducial worldline — positive curvature
**focuses** geodesics (the geometric engine of the singularity theorems). At $\theta=1$ this
is $A^\theta=-\sin^2(1)\approx-0.708$, matching
`geodesic_deviation(sphere_metric(1), [1.0,0], [0,1], [1,0])` $\to[-0.708,\,0]$.

### P5. The Einstein trace identity  *(notes §3)*
Show `g^{μν}G_{μν} = (1 − n/2)R`. Verify on the 3-sphere (`R = 6/a²`) that the
trace is `−R/2`.
*Check:* on `_three_sphere(1.0)`, `ricci_scalar ≈ 6` and the contracted Einstein
tensor trace ≈ `−3` (see `test_einstein_trace_identity`).

**Solution.** Contract the Einstein tensor with the inverse metric, using
$g^{\mu\nu}R_{\mu\nu}=R$ and $g^{\mu\nu}g_{\mu\nu}=\delta^\mu{}_\mu=n$:
$$g^{\mu\nu}G_{\mu\nu}=g^{\mu\nu}\!\left(R_{\mu\nu}-\tfrac12 R\,g_{\mu\nu}\right)=R-\tfrac12 R\,n=\Big(1-\tfrac n2\Big)R .$$
So the trace flips sign relative to $R$ above $n=2$, and vanishes exactly at $n=2$ (where
$G_{\mu\nu}\equiv0$). On the unit 3-sphere ($n=3$, maximally symmetric with $R=6/a^2=6$),
$$g^{\mu\nu}G_{\mu\nu}=\Big(1-\tfrac32\Big)R=-\tfrac R2=-3 ,$$
the value `test_einstein_trace_identity` confirms: `ricci_scalar` $\approx6$ on
`_three_sphere(1.0)` and the contracted Einstein tensor trace $\approx-3$.

### P6. Why the Einstein tensor?  *(conceptual; bridge to RE-13)*
The contracted Bianchi identity gives `∇_μ G^{μν} = 0` automatically. Argue that
this is *why* the field equations must read `G_{μν} = 8πT_{μν}` (not `R_{μν} ∝
T_{μν}`): it forces `∇_μ T^{μν} = 0`, local energy–momentum conservation.
*(No code check — this is the structural argument RE-13 builds on.)*

**Solution.** Local energy–momentum conservation, $\nabla_\mu T^{\mu\nu}=0$, is
non-negotiable — it is the curved-space promotion of $\partial_\mu T^{\mu\nu}=0$. So
whatever curvature tensor sits on the left of the field equation must be **identically**
divergence-free; otherwise setting it $\propto T^{\mu\nu}$ would impose an extra, unphysical
constraint on the matter. The contracted Bianchi identity hands exactly one such object for
free:
$$\nabla_\mu G^{\mu\nu}=\nabla_\mu\!\left(R^{\mu\nu}-\tfrac12 R\,g^{\mu\nu}\right)\equiv0 .$$
Neither $R^{\mu\nu}$ nor $R\,g^{\mu\nu}$ is separately conserved — only the combination
$G^{\mu\nu}$ is, because $\nabla_\mu R^{\mu\nu}=\tfrac12\nabla^\nu R$. Hence the law reads
$G_{\mu\nu}=8\pi T_{\mu\nu}$: picking $R_{\mu\nu}\propto T_{\mu\nu}$ instead would force
$\nabla^\nu R=0$ (constant scalar curvature), far too rigid for a general source. With $G$ on
the left, $\nabla_\mu T^{\mu\nu}=0$ is automatic — the structural reason the Einstein
equation of RE-13 takes this form.
