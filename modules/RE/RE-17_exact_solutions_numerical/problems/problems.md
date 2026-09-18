# RE-17 — Problems

Work them by hand, then check with `code/exact_solutions.py`. Sources in `../refs.md`.
Geometrized units `G = c = 1`, signature mostly-plus.

### P1. Kerr horizons and the ergosphere  *(Zee §VII.5; Stephani §20.5)*
From `Δ = r² − 2Mr + a² = 0` find the Boyer–Lindquist horizons, and from
`g_{tt}=0` the equatorial static-limit radius. For what `a` is there a horizon?
*Answer:* `r_± = M ± √(M²−a²)`, real iff `a ≤ M` (`a=M` extremal, `a>M` naked).
Static limit at the equator: `r_E = 2M > r_+` — the ergoregion.
*Check:* `kerr_horizons(1, 0.6)` → `(0.2, 1.8)`; `kerr_ergosphere(1, 0.6, math.pi/2)`
→ `2.0`; `kerr_horizons(1, 1.5)` raises `ValueError` (naked singularity).

**Solution.** The horizons are the roots of $\Delta=r^2-2Mr+a^2=0$. The quadratic formula gives
$$r_\pm=\frac{2M\pm\sqrt{4M^2-4a^2}}{2}=M\pm\sqrt{M^2-a^2},$$
real iff $M^2-a^2\ge0$, i.e. $a\le M$ ($a=M$ extremal, $a>M$ a naked ring singularity). For $M=1,a=0.6$: $\sqrt{1-0.36}=0.8$, so $r_\pm=1\pm0.8=(0.2,\,1.8)$. The static limit is $g_{tt}=-(1-2Mr/\Sigma)=0\Rightarrow\Sigma=r^2+a^2\cos^2\theta=2Mr$; at the equator $\cos\theta=0$ gives $r^2=2Mr$, so $r_E=2M=2>r_+$ — the gap is the ergoregion. These match `kerr_horizons(1,0.6)`$=(0.2,1.8)$, `kerr_ergosphere(1,0.6,\pi/2)`$=2.0$, and `kerr_horizons(1,1.5)` raising `ValueError` since $M^2-a^2<0$.

### P2. Kerr is a vacuum solution, and reduces to Schwarzschild  *(notes §2)*
Argue `R_{μν}=0` for Kerr (it is a vacuum metric), and show `a→0` returns
Schwarzschild. Why does feeding the metric to `ricci` *test* the components?
*Answer:* a wrong term breaks `R_{μν}=0`, so `verify_vacuum` (= `max|R_{μν}|`) is a
componentwise validator. At `a=0`: `Σ→r²`, `Δ→r²−2Mr`, `g_{tφ}→0`, giving
`diag(−(1−2M/r), 1/(1−2M/r), r², r²sin²θ)`.
*Check:* `verify_vacuum(kerr_metric(1,0.5), [0,8,1.0,0.7])` ≈ `1e-6` (≈0);
`kerr_metric(1,0)` matches `curvature.schwarzschild_metric(1)` componentwise.

**Solution.** Kerr was built to solve the *vacuum* equations $R_{\mu\nu}=0$ (equivalently $G_{\mu\nu}=0$, since $R=0$ in vacuum). The code never assumes this — it *checks* it: handing $g_{\mu\nu}$ to RE-11's finite-difference `ricci` returns the actual Ricci tensor, so `verify_vacuum` $=\max_{\mu\nu}|R_{\mu\nu}|$ is a componentwise validator — one mistyped term (say the cross term $g_{t\phi}$) would leave a non-zero residual and fail the gate. Setting $a=0$ collapses $\Sigma=r^2+a^2\cos^2\theta\to r^2$, $\Delta=r^2-2Mr+a^2\to r^2-2Mr$, and the frame-dragging term $g_{t\phi}=-2Mar\sin^2\theta/\Sigma\to0$, leaving
$$ds^2\to-\Big(1-\tfrac{2M}{r}\Big)dt^2+\Big(1-\tfrac{2M}{r}\Big)^{-1}dr^2+r^2d\theta^2+r^2\sin^2\theta\,d\phi^2,$$
exactly Schwarzschild. Numerically `verify_vacuum(kerr_metric(1,0.5),[0,8,1.0,0.7])`$\approx9.9\times10^{-7}\approx0$ (pure finite-difference noise), and `kerr_metric(1,0)` matches `curvature.schwarzschild_metric(1)` componentwise.

### P3. Reissner–Nordström: curved, sourced, yet scalar-flat  *(Stephani §15.4; notes §3)*
With `f = 1 − 2M/r + Q²/r²`, RN is sourced by the EM field. Show `R_{μν} ≠ 0` but
the Ricci *scalar* `R = 0`. Why is `R=0`?
*Answer:* the electromagnetic stress-energy is **trace-free** in 4-D (`T^μ_μ=0`),
and `R = −8πT^μ_μ = 0`; but `T_{μν}≠0`, so individual `R_{μν}=O(Q²/r⁴)≠0`.
*Check:* `verify_vacuum(reissner_nordstrom_metric(1,0.9), [0,3,1,0.7])` ≈ `0.09`
(≠0); `curvature.ricci_scalar(...)` ≈ `1e-7` (≈0). `Q→0` ⇒ both → Schwarzschild.

**Solution.** Trace Einstein's equation $G_{\mu\nu}=8\pi T_{\mu\nu}$: in 4-D $g^{\mu\nu}G_{\mu\nu}=-R$, so $R=-8\pi T^{\mu}{}_{\mu}$. The electromagnetic stress-energy $T^{\rm EM}_{\mu\nu}\propto F_{\mu\alpha}F_{\nu}{}^{\alpha}-\tfrac14 g_{\mu\nu}F_{\alpha\beta}F^{\alpha\beta}$ is **trace-free** in four dimensions, $T^{\mu}{}_{\mu}=0$, hence
$$R=-8\pi T^{\mu}{}_{\mu}=0$$
even though $T_{\mu\nu}\neq0$. So the Ricci *scalar* vanishes while individual components survive: since $R=0$ the mixed Ricci equals the mixed Einstein tensor, $R^{\mu}{}_{\nu}=G^{\mu}{}_{\nu}$, giving $G^{t}{}_{t}=G^{r}{}_{r}=-Q^2/r^4$ and $G^{\theta}{}_{\theta}=G^{\phi}{}_{\phi}=+Q^2/r^4$; the covariant components are then $O(Q^2/r^2)$, e.g. $R_{\theta\theta}=r^2R^{\theta}{}_{\theta}=Q^2/r^2$. At $r=3,\,Q=0.9$ this is $0.81/9=0.09$ — exactly `verify_vacuum(reissner_nordstrom_metric(1,0.9),[0,3,1,0.7])`$\approx0.09\neq0$ — while `curvature.ricci_scalar(...)`$\approx10^{-7}\approx0$; sending $Q\to0$ takes both to zero (Schwarzschild, Ricci-flat again).

### P4. de Sitter and the cosmological constant  *(Zee §IX.10; notes §4)*
For `f = 1 − Λr²/3`, show de Sitter solves `G_{μν} + Λg_{μν} = 0` and hence
`R = 4Λ` in 4-D. Where is the cosmological horizon?
*Answer:* taking the trace of `G_{μν}+Λg_{μν}=0` gives `−R + 4Λ = 0`, so `R = 4Λ`
(and `R_{μν}=Λg_{μν}`). Horizon at `f=0`, i.e. `r = √(3/Λ)`.
*Check:* `verify_einstein_lambda(de_sitter_metric(0.03), [0,3,1,0.7], 0.03)` ≈ `6e-7`;
`curvature.ricci_scalar(de_sitter_metric(0.03), [0,3,1,0.7])` ≈ `0.12 = 4·0.03`.

**Solution.** With a cosmological constant the vacuum equation reads $G_{\mu\nu}+\Lambda g_{\mu\nu}=0$. Contract with $g^{\mu\nu}$, using $g^{\mu\nu}G_{\mu\nu}=-R$ and $g^{\mu\nu}g_{\mu\nu}=4$ in 4-D:
$$-R+4\Lambda=0\quad\Longrightarrow\quad R=4\Lambda.$$
Substituting back, $R_{\mu\nu}=\tfrac12 R\,g_{\mu\nu}-\Lambda g_{\mu\nu}=(2\Lambda-\Lambda)g_{\mu\nu}=\Lambda g_{\mu\nu}$ — constant curvature, the Ricci tensor proportional to the metric. The cosmological horizon sits where the metric function degenerates, $f=1-\Lambda r^2/3=0$, i.e. $r=\sqrt{3/\Lambda}$. For $\Lambda=0.03$ everything matches: `verify_einstein_lambda(de_sitter_metric(0.03),[0,3,1,0.7],0.03)`$\approx6\times10^{-7}\approx0$, and `curvature.ricci_scalar(de_sitter_metric(0.03),[0,3,1,0.7])`$\approx0.12=4\cdot0.03$, confirming $R=4\Lambda$.

### P5. The ADM split and the lapse  *(Baumgarte–Shapiro Ch. 2; notes §5)*
Define the lapse `α`, shift `β^i`, and spatial metric `γ_{ij}` of a `t=const`
slice. Compute them for Minkowski (inertial) and for a static `g_{tt}=−f`.
*Answer:* `α = 1/√(−g^{tt})`, `β^i = γ^{ij}g_{0j}`, `γ_{ij}=g_{ij}`. Minkowski:
`α=1, β=0, γ=δ_{ij}`. Static diagonal: `g^{tt}=−1/f`, so `α=√f`, `β=0`.
*Check:* `adm_decompose(curvature.minkowski_metric(), [0,1,1,0.5])` → `(1.0, [0,0,0], I₃)`;
`adm_decompose(curvature.schwarzschild_metric(1), [0,8,1,0.7])[0]` ≈ `√(1−2/8)=0.866`.

**Solution.** Foliate spacetime on $t=x^0=\text{const}$. The intrinsic (spatial) metric is just the lower block $\gamma_{ij}=g_{ij}$; the lapse and shift carry the time information via
$$ds^2=-\alpha^2dt^2+\gamma_{ij}\big(dx^i+\beta^i dt\big)\big(dx^j+\beta^j dt\big),\qquad \alpha=\frac{1}{\sqrt{-g^{tt}}},\quad \beta^i=\gamma^{ij}g_{0j}.$$
The lapse is read from the *inverse* metric because $g^{tt}=-1/\alpha^2$. For inertial Minkowski $g=\mathrm{diag}(-1,1,1,1)$: $g^{tt}=-1\Rightarrow\alpha=1$, no off-diagonal $g_{0i}\Rightarrow\beta^i=0$, and $\gamma=\delta_{ij}$ — flat space sliced flatly. For any static diagonal metric with $g_{tt}=-f$ the inverse gives $g^{tt}=-1/f$, so $\alpha=\sqrt{f}$ and again $\beta=0$. These reproduce `adm_decompose(curvature.minkowski_metric(),[0,1,1,0.5])`$=(1.0,[0,0,0],I_3)$ and the Schwarzschild lapse `adm_decompose(curvature.schwarzschild_metric(1),[0,8,1,0.7])[0]`$\approx\sqrt{1-2/8}=0.866$.

### P6. The Hamiltonian constraint on a Schwarzschild slice  *(Baumgarte–Shapiro Ch. 3; notes §5)*
A `t=const` Schwarzschild slice is a *moment of time symmetry* (`K_{ij}=0`). What
must its intrinsic scalar curvature `R^{(3)}` be, and why? Is the slice flat?
*Answer:* the Hamiltonian constraint `R^{(3)}+K²−K_{ij}K^{ij}=16πρ` with `K_{ij}=0`,
`ρ=0` forces `R^{(3)}=0` — the slice is **scalar-flat**. It is *not* flat: the
spatial metric is `γ_{rr}=1/(1−2M/r)≠1` (the Flamm paraboloid), with nonzero
3-Riemann/3-Ricci. Scalar-flat ⇏ flat.
*Check:* `hamiltonian_constraint_flat(curvature.schwarzschild_metric(1), [0,6,1,0.7])`
≈ `2e-8` (≈0); but `spatial_slice_metric(...)([6,1,0.7])[0][0]` = `1/(1−1/3) = 1.5 ≠ 1`.

**Solution.** The Hamiltonian constraint is $R^{(3)}+K^2-K_{ij}K^{ij}=16\pi\rho$. A *moment of time symmetry* means the slice is instantaneously at rest, $K_{ij}=0$ (so $K=0$), and the Schwarzschild exterior is vacuum, $\rho=0$; every term but the first drops:
$$R^{(3)}+0-0=0\quad\Longrightarrow\quad R^{(3)}=0.$$
The slice must be **scalar-flat**. That is *not* the same as flat: the induced 3-metric has $\gamma_{rr}=1/(1-2M/r)\neq1$ (the Flamm paraboloid), with non-zero 3-Riemann and 3-Ricci — only the particular contraction $R^{(3)}=\gamma^{ij}R^{(3)}_{ij}$ cancels. The code confirms both at once: `hamiltonian_constraint_flat(curvature.schwarzschild_metric(1),[0,6,1,0.7])`$\approx2.5\times10^{-8}\approx0$ (so $R^{(3)}=0$), while `spatial_slice_metric(...)([6,1,0.7])[0][0]`$=1/(1-1/3)=1.5\neq1$ — curved, yet scalar-flat, exactly the identity a numerical-relativity code enforces on its initial data.
