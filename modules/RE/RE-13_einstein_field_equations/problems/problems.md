# RE-13 — Problems

Work them by hand, then check with `code/einstein_equations.py`. Sources in `../refs.md`.

### P1. Schwarzschild is a vacuum solution  *(Zee §VI.1; cpope §6.1)*
Outside a static spherical mass `T_{μν}=0`, so the field equation is `G_{μν}=0`,
equivalently `R_{μν}=0`. Confirm the Schwarzschild metric satisfies it for `r>2M`,
and note this is *not* flat space (RE-11: `K=48M²/r⁶≠0`).
*Answer:* `R_{μν}=0` is the vacuum equation; Schwarzschild solves it.
*Check:* `field_equation_residual(schwarzschild_metric(1), 0, [0,r,1.2,0.7])` ≈ 0 for
`r = 4,6,10`.

**Solution.** With $T_{\mu\nu}=0$ the field equation is $G_{\mu\nu}=0$. Tracing with
$g^{\mu\nu}$ in $n=4$ gives $g^{\mu\nu}G_{\mu\nu}=(1-\tfrac n2)R=-R=0$, so $R=0$ and
the equation collapses to the plain **vacuum** condition
$$R_{\mu\nu}=G_{\mu\nu}+\tfrac12 R\,g_{\mu\nu}=0 .$$
The Schwarzschild metric $g=\mathrm{diag}\!\big(-(1-\tfrac{2M}{r}),(1-\tfrac{2M}{r})^{-1},r^2,r^2\sin^2\theta\big)$
has $R_{\mu\nu}=0$ for $r>2M$ (Birkhoff: the unique spherically-symmetric vacuum). It is
**not** flat — the Kretschmann scalar $K=R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}=48M^2/r^6\neq0$
(RE-11), so the trace-free Weyl/tidal curvature survives where Ricci vanishes. Numerically
`field_equation_residual` returns $\max|G_{\mu\nu}|\approx7\times10^{-7}\approx0$ at $r=4,6,10$
(finite-difference noise), confirming the vacuum equation.

### P2. The trace of a perfect fluid  *(Zee §III.6)*
From `T_{μν}=(ρ+p)u_μu_ν+pg_{μν}` with `u·u=−1`, compute `g^{μν}T_{μν}` in 4-D. Then
specialise to dust (`p=0`) and to radiation (`p=ρ/3`).
*Answer:* `g^{μν}T_{μν}=−ρ+3p`; dust → `−ρ`; **radiation → 0** (the EM/conformal
source is traceless). The trace is the same in every frame and every metric.
*Check:* with `u=_boosted_u(0.6)`, `trace(minkowski_metric(), T, x)` → `−ρ+3p`;
radiation `p=ρ/3` → `0` (`test_dust_and_radiation_traces`).

**Solution.** Contract $T_{\mu\nu}=(\rho+p)u_\mu u_\nu+p\,g_{\mu\nu}$ with $g^{\mu\nu}$:
$$g^{\mu\nu}T_{\mu\nu}=(\rho+p)\,g^{\mu\nu}u_\mu u_\nu+p\,g^{\mu\nu}g_{\mu\nu}.$$
The first contraction is the norm $g^{\mu\nu}u_\mu u_\nu=u\cdot u=-1$; the second is
$g^{\mu\nu}g_{\mu\nu}=\delta^\mu{}_\mu=n=4$. Hence
$$g^{\mu\nu}T_{\mu\nu}=-(\rho+p)+4p=-\rho+3p .$$
**Dust** $p=0\Rightarrow$ trace $=-\rho$; **radiation** $p=\rho/3\Rightarrow-\rho+3\cdot\tfrac\rho3=0$
(the conformal/EM source is traceless). The result is a scalar, so it is identical in every
frame and on every background — only $u\cdot u=-1$ entered. For $\rho=2.5,\,p=0.4$ the code
returns `trace` $=-1.3=-\rho+3p$ even with the boosted $u$, and $0$ for radiation.

### P3. Trace-reverse the field equation  *(cpope §6.1)*
Take the trace of `G_{μν}=8πT_{μν}` with `g^{μν}` (use `g^{μν}G_{μν}=−R` in 4-D) to
get `R=−8πT`, then substitute back to derive the trace-reversed form
`R_{μν}=8π(T_{μν}−½Tg_{μν})`. Why is this the convenient form in vacuum?
*Answer:* its left side is plain Ricci, so `T_{μν}=0 ⇒ R_{μν}=0` immediately. The two
forms are algebraically identical.
*Check:* build `R = trace_reversed_ricci(metric, T, x)`, rebuild
`G = R − ½(g^{ab}R_{ab})g`, and confirm `G = 8πT`
(`test_trace_reversed_equivalent_to_einstein`).

**Solution.** Trace $G_{\mu\nu}=8\pi T_{\mu\nu}$ with $g^{\mu\nu}$. In $n=4$,
$g^{\mu\nu}G_{\mu\nu}=(1-\tfrac n2)R=-R$, so with $T\equiv g^{\mu\nu}T_{\mu\nu}$,
$$-R=8\pi T\;\Longrightarrow\; R=-8\pi T .$$
Now substitute this back into $R_{\mu\nu}-\tfrac12 R\,g_{\mu\nu}=8\pi T_{\mu\nu}$:
$$R_{\mu\nu}=8\pi T_{\mu\nu}+\tfrac12 R\,g_{\mu\nu}=8\pi T_{\mu\nu}-4\pi T\,g_{\mu\nu}=8\pi\!\left(T_{\mu\nu}-\tfrac12 T\,g_{\mu\nu}\right).$$
The two forms are the *same* equation, the trace merely moved from the geometry side onto
the source. This **trace-reversed** form is the convenient one in vacuum: its left side is
plain Ricci, so $T_{\mu\nu}=0$ gives $R_{\mu\nu}=0$ in one line, with no need to first argue
$R=0$. The round trip is exact — `trace_reversed_ricci(metric, T, x)`, then rebuilding
$G=R-\tfrac12(g^{ab}R_{ab})g$, returns $8\pi T$ to machine precision
(`test_trace_reversed_equivalent_to_einstein`).

### P4. The Newtonian limit fixes 8π  *(Zee §V.4 & §VI.5; cpope §5.5)*
For the static weak field `g_{00}=−(1+2Φ)`, `g_{ij}=(1−2Φ)δ_{ij}`, show the geodesic
equation gives `\ddot x^i=−∂_iΦ` (Newton) and the linearised field equation gives
`G_{00}=2∇²Φ`. Hence `G_{00}=8πρ` reproduces `∇²Φ=4πρ` **only** if the constant is
`8π`.
*Answer:* matching to Poisson `∇²Φ=4πρ` forces `κ=8π` (in `G=c=1`).
*Check:* for a Gaussian `Φ`, `newtonian_poisson_residual(Phi, x)` `= G_{00}−2∇²Φ ≈ 0`
to ~0.5% (loose FD tol; `test_newtonian_limit_fixes_8pi`).

**Solution.** *Geodesics → Newton.* For slow motion in a static field the geodesic equation
reduces to $\ddot x^i=-\Gamma^i{}_{00}$, with
$\Gamma^i{}_{00}=-\tfrac12 g^{ij}\partial_j g_{00}\approx-\tfrac12\partial_i g_{00}$. With
$g_{00}=-(1+2\Phi)$,
$$\ddot x^i=\tfrac12\partial_i g_{00}=-\partial_i\Phi ,$$
i.e. Newton's $\ddot{\mathbf x}=-\nabla\Phi$ — this *defines* $\Phi$ as the gravitational
potential. *Field equation → Poisson.* Linearising $G_{00}$ for the isotropic metric
$g_{00}=-(1+2\Phi),\ g_{ij}=(1-2\Phi)\delta_{ij}$ gives $G_{00}\simeq2\nabla^2\Phi$ (the
spatial perturbation is essential — $g_{00}$ alone yields only $\nabla^2\Phi$). The $00$
equation $G_{00}=\kappa T_{00}=\kappa\rho$ is then
$$2\nabla^2\Phi=\kappa\rho\quad\Longleftrightarrow\quad\nabla^2\Phi=\tfrac{\kappa}{2}\rho ,$$
which is Poisson's $\nabla^2\Phi=4\pi\rho$ **only** if $\kappa=8\pi$. Numerically
`newtonian_poisson_residual` returns $G_{00}-2\nabla^2\Phi\approx-1\times10^{-5}$ against a
signal $\approx-3\times10^{-3}$ (~0.4%), confirming $G_{00}=2\nabla^2\Phi$.

### P5. de Sitter and the cosmological constant  *(cpope §7, Eq. 7.15)*
Add `Λg_{μν}` to the left side: `G_{μν}+Λg_{μν}=8πT_{μν}`. For a Λ-vacuum (`T=0`),
show a maximally-symmetric solution needs `R_{μν}=Λg_{μν}`, and that de Sitter
(`R_{μν}=3/L²\,g_{μν}`) works with `Λ=3/L²`.
*Answer:* `Λ=3/L²`; de Sitter is the positive-curvature Λ-vacuum (cosmic horizon at
`r=L`).
*Check:* `field_equation_residual(de_sitter_metric(10), 0, x, Lambda=3/10**2)` ≈ 0,
while `Lambda=0` gives a residual `>10⁻³` (`test_de_sitter_is_a_lambda_vacuum`).

**Solution.** With the $\Lambda$ term the vacuum ($T_{\mu\nu}=0$) equation is
$G_{\mu\nu}+\Lambda g_{\mu\nu}=0$, i.e. $R_{\mu\nu}-\tfrac12 R\,g_{\mu\nu}+\Lambda g_{\mu\nu}=0$.
Trace it in $n=4$ ($g^{\mu\nu}G_{\mu\nu}=-R$, $g^{\mu\nu}g_{\mu\nu}=4$):
$$-R+4\Lambda=0\;\Longrightarrow\; R=4\Lambda .$$
Substituting back, $R_{\mu\nu}=\tfrac12 R\,g_{\mu\nu}-\Lambda g_{\mu\nu}=(2\Lambda-\Lambda)g_{\mu\nu}=\Lambda g_{\mu\nu}$
— a maximally-symmetric **Einstein space**, curvature alike in every direction. de Sitter
realises this with $R_{\mu\nu}=(3/L^2)g_{\mu\nu}$, so matching $\Lambda g_{\mu\nu}$ to
$(3/L^2)g_{\mu\nu}$ fixes
$$\Lambda=\frac{3}{L^2}.$$
It is the positive-curvature $\Lambda$-vacuum, with a cosmic horizon at $r=L$. The code
agrees: `field_equation_residual(de_sitter_metric(10), 0, x, Lambda=3/10**2)`
$\approx6\times10^{-7}$, while `Lambda=0` leaves a residual $>10^{-3}$ — the wrong $\Lambda$
is genuinely not a solution.

### P6. Why the Einstein tensor?  *(conceptual; RE-11 §3 → RE-13)*
Local energy–momentum conservation demands `∇_μT^{μν}=0`, so the curvature on the
left of the field equation must be divergence-free. Argue from the contracted
Bianchi identity `∇_μG^{μν}=0` that the left side must be `G_{μν}` (up to `Λg_{μν}`),
**not** `R_{μν}` — and that this is what makes `∇_μT^{μν}=0` automatic.
*Answer:* only `G_{μν}=R_{μν}−½Rg_{μν}` (plus `Λg_{μν}`) is identically conserved;
`R_{μν}∝T_{μν}` would force `∂_νR=0`, i.e. constant scalar curvature — far too
restrictive. *(No code check — this is the structural argument the whole module rests
on; see `notes.md` §2.)*

**Solution.** Conservation $\nabla_\mu T^{\mu\nu}=0$ forces the curvature tensor on the left
of the field equation to be identically divergence-free. The candidates built from $g$ and
its first two derivatives are $R^{\mu\nu}$, $R\,g^{\mu\nu}$, and $g^{\mu\nu}$ itself. The
contracted Bianchi identity (RE-11 §3) says
$$\nabla_\mu R^{\mu\nu}=\tfrac12\nabla^\nu R ,$$
so $R^{\mu\nu}$ alone is **not** conserved unless $R$ is constant; the unique divergence-free
combination is $G^{\mu\nu}=R^{\mu\nu}-\tfrac12 R\,g^{\mu\nu}$, and since
$\nabla_\mu g^{\mu\nu}=0$ one may freely add any $\Lambda g^{\mu\nu}$. Hence the left side must
be $G_{\mu\nu}$ (up to $\Lambda g_{\mu\nu}$), giving $G_{\mu\nu}+\Lambda g_{\mu\nu}=8\pi T_{\mu\nu}$.
Choosing $R_{\mu\nu}\propto T_{\mu\nu}$ instead would impose $\nabla^\nu R=0$ — constant
scalar curvature everywhere, far too rigid for a general source — whereas with $G$ the
conservation law $\nabla_\mu T^{\mu\nu}=0$ is automatic. This is the structural argument the
whole module rests on (notes §2).
