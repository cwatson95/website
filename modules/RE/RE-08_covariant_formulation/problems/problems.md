# RE-08 — Problems

Work them by hand, then check with `code/covariant_sr.py`. Sources in `../refs.md`.
Take the standard boost `L = lorentz.general_boost((0.3, -0.4, 0.5))` where one is
needed.

### P1. The contraction `V^μW_μ` is invariant  *(Griffiths 4e, §12.1.4, p.525)*
Let `V^μ = (2, 5, −1, 3)` (contravariant) and `W_μ = (1, 0, 2, −2)` (covariant).
Compute `V^μW_μ`, then boost `V` with the contravariant law and `W` with the
covariant (inverse-transpose) law and recompute. Explain why the two agree.
*Answer:* `V^μW_μ = 2 − 0 − 2 − 6 = −6`, unchanged by the boost, because
`Λ^μ_ν (Λ⁻¹)^ρ_μ = δ^ρ_ν` collapses the two transformations.
*Check:* `sum(V[i]*W[i] …)` vs `sum(transform_vector(L,V)[i]*transform_covector(L,W)[i] …)` → both `−6`.

**Solution.** Direct evaluation gives $V^\mu W_\mu = 2\cdot1 + 5\cdot0 + (-1)\cdot2 + 3\cdot(-2) = -6$. Under a boost the contravariant $V$ gains a factor $\Lambda$ and the covariant $W$ the inverse-transpose, and the two collapse:
$$\bar V^\mu\bar W_\mu=\big(\Lambda^\mu{}_\nu V^\nu\big)\big((\Lambda^{-1})^\rho{}_\mu W_\rho\big)=\underbrace{\Lambda^\mu{}_\nu(\Lambda^{-1})^\rho{}_\mu}_{\delta^\rho_\nu}\,V^\nu W_\rho=V^\nu W_\nu.$$
The covariant law is *defined* as the inverse-transpose precisely so this product is frame-independent - the $\Lambda$ and $\Lambda^{-1}$ annihilate into $\delta^\rho_\nu$. Hence the boosted contraction returns the same value, matching `sum(transform_vector(L,V)[i]*transform_covector(L,W)[i])` $=-6$.

### P2. η is an invariant tensor  *(Griffiths 4e, §12.1.4, p.525)*
Show `Λ^μ_α Λ^ν_β η^{αβ} = η^{μν}` for every Lorentz Λ, i.e. `ΛηΛᵀ = η`. Start from
the defining property `ΛᵀηΛ = η` and use `η² = I`.
*Answer:* From `ΛᵀηΛ = η`, left-multiply by `η` and right-multiply by `Λ⁻¹`:
`ηΛᵀη = Λ⁻¹`, hence `ΛηΛᵀη = I`, so `ΛηΛᵀ = η⁻¹ = η`.
*Check:* `transform_tensor2(L, ETA)` equals `ETA` to machine precision.

**Solution.** Start from the defining Lorentz condition $\Lambda^{\mathsf T}\eta\Lambda=\eta$. Left-multiply by $\eta$ and use $\eta^2=I$, then right-multiply by $\Lambda^{-1}$:
$$\eta\Lambda^{\mathsf T}\eta\Lambda=I\ \Rightarrow\ \eta\Lambda^{\mathsf T}\eta=\Lambda^{-1}.$$
Now form the rank-2 transform of $\eta$ and insert $\eta\eta=I$ at the right:
$$\Lambda\eta\Lambda^{\mathsf T}=\Lambda\big(\eta\Lambda^{\mathsf T}\eta\big)\eta=\Lambda\Lambda^{-1}\eta=\eta.$$
In index form $\Lambda^\mu{}_\alpha\Lambda^\nu{}_\beta\,\eta^{\alpha\beta}=\eta^{\mu\nu}$: the metric has the same components in every frame. This is exactly `transform_tensor2(L, ETA)` equalling `ETA` to machine precision (the demo reports a maximum difference $\sim 2\times10^{-16}$).

### P3. Symmetry survives a boost  *(Griffiths 4e, Prob. 12.50, p.564)*
Prove: if `T^{μν}` is symmetric then so is `T̄^{μν} = Λ^μ_α Λ^ν_β T^{αβ}` (and the
same for antisymmetric).
*Answer:* `T̄^{νμ} = Λ^ν_α Λ^μ_β T^{αβ} = Λ^ν_β Λ^μ_α T^{βα}` (relabel `α↔β`)
`= Λ^μ_α Λ^ν_β T^{αβ} = T̄^{μν}` using `T^{βα}=T^{αβ}`. The minus sign carries
through for the antisymmetric case. So *symmetry type is a Lorentz-invariant label*
— which is why decomposing `T = T^{(μν)} + T^{[μν]}` is frame-independent.
*Check:* `transform_tensor2(L, symmetric_part(T))` is symmetric;
`transform_tensor2(L, antisymmetric_part(T))` is antisymmetric.

**Solution.** Apply the rank-2 law to $\bar T^{\nu\mu}$ and rename the dummy indices $\alpha\leftrightarrow\beta$:
$$\bar T^{\nu\mu}=\Lambda^\nu{}_\alpha\Lambda^\mu{}_\beta T^{\alpha\beta}=\Lambda^\nu{}_\beta\Lambda^\mu{}_\alpha T^{\beta\alpha}=\Lambda^\mu{}_\alpha\Lambda^\nu{}_\beta\,T^{\beta\alpha}.$$
If $T^{\beta\alpha}=+T^{\alpha\beta}$ this equals $+\bar T^{\mu\nu}$; if $T^{\beta\alpha}=-T^{\alpha\beta}$ it equals $-\bar T^{\mu\nu}$. So a boost sends symmetric $\to$ symmetric and antisymmetric $\to$ antisymmetric - symmetry type is a Lorentz-invariant label, which is why the split $T=T^{(\mu\nu)}+T^{[\mu\nu]}$ is frame-independent. This is what `transform_tensor2(L, symmetric_part(T))` (stays symmetric) and `transform_tensor2(L, antisymmetric_part(T))` (stays antisymmetric) confirm.

### P4. Invariants by contraction  *(Griffiths 4e, Prob. 12.51, p.565)*
For `T^{μν}` formed from `T^{(μν)}` (symmetric) and `T^{[μν]}` (antisymmetric):
(a) show the cross-contraction `S_{μν}A^{μν}` vanishes for symmetric `S`,
antisymmetric `A`; (b) show the trace `T^μ_μ = η_{μν}T^{μν}` is a Lorentz scalar.
*Answer:* (a) `S_{μν}A^{μν} = S_{νμ}A^{μν} = −S_{νμ}A^{νμ} = −S_{μν}A^{μν}` (relabel)
⇒ it equals its own negative ⇒ `0`. (b) `T^μ_μ` has every index tied off, so it
transforms as a scalar; explicitly `η_{μν}T̄^{μν} = η_{μν}Λ^μ_αΛ^ν_βT^{αβ} =
η_{αβ}T^{αβ}` by P2.
*Check:* `double_contract(symmetric_part(T), antisymmetric_part(T))` → `0`;
`trace(transform_tensor2(L, T))` equals `trace(T)`.

**Solution.** (a) Rename $\mu\leftrightarrow\nu$ and use the two symmetries $S_{\nu\mu}=S_{\mu\nu}$, $A^{\nu\mu}=-A^{\mu\nu}$:
$$S_{\mu\nu}A^{\mu\nu}=S_{\nu\mu}A^{\nu\mu}=S_{\mu\nu}\big(-A^{\mu\nu}\big)=-S_{\mu\nu}A^{\mu\nu},$$
so the cross-contraction equals its own negative and must vanish. (b) The trace ties off both indices with the invariant metric, so by P2 ($\eta_{\mu\nu}\Lambda^\mu{}_\alpha\Lambda^\nu{}_\beta=\eta_{\alpha\beta}$):
$$\eta_{\mu\nu}\bar T^{\mu\nu}=\eta_{\mu\nu}\Lambda^\mu{}_\alpha\Lambda^\nu{}_\beta T^{\alpha\beta}=\eta_{\alpha\beta}T^{\alpha\beta}=T^\mu{}_\mu,$$
a Lorentz scalar. These confirm `double_contract(symmetric_part(T), antisymmetric_part(T))` $=0$ and `trace(transform_tensor2(L, T))` $=$ `trace(T)` (the demo holds it at $30.0$ before and after the boost).

### P5. The 4-gradient is covariant; the d'Alembertian is a scalar  *(Griffiths 4e, §12.3.5, Eq. 12.138, p.570)*
(a) Compute `∂_μ(x·x)` and show it equals `2x_μ` (a *lower*-index 4-vector, with
`∂_0 = −2x^0`). (b) Evaluate the d'Alembertian `□ = −∂_t² + ∇²` on `f = (x^0)²`, on
`f = (x^1)²`, and on `f = x·x`.
*Answer:* (a) `∂_ν(η_{αβ}x^αx^β) = 2η_{νβ}x^β = 2x_ν`. (b) `□(x^0)² = −2`,
`□(x^1)² = +2`, and `□(x·x) = −(−2)+2+2+2 = 8` (= `2η^{μν}η_{μν} = 2·4`).
*Check:* `four_gradient(lambda x: mdot(x,x), x)` ≈ `[2c for c in lower(x)]`;
`dalembertian(...)` returns `−2`, `+2`, `8`.

**Solution.** (a) With $x\cdot x=\eta_{\alpha\beta}x^\alpha x^\beta$ and $\partial x^\alpha/\partial x^\nu=\delta^\alpha_\nu$, the product rule gives
$$\partial_\nu(\eta_{\alpha\beta}x^\alpha x^\beta)=\eta_{\nu\beta}x^\beta+\eta_{\alpha\nu}x^\alpha=2\eta_{\nu\beta}x^\beta=2x_\nu,$$
a *lower*-index vector whose time slot carries the metric's sign, $\partial_0(x\cdot x)=2x_0=-2x^0$. (b) For a single quadratic only the matching second derivative survives, $\Box(x^0)^2=\eta^{00}\cdot2=-2$ and $\Box(x^i)^2=\eta^{ii}\cdot2=+2$. Since $x\cdot x$ carries a minus on its time term, $\Box(x\cdot x)=-(-2)+2+2+2=8=2\,\eta^{\mu\nu}\eta_{\mu\nu}$. These match `four_gradient(...)` $=[-2,4,-2,1]=2\cdot$`lower(x)` and `dalembertian(...)` returning $-2,\,+2,\,8$.

### P6. A null plane wave solves the wave equation  *(bridge to EM-18; Griffiths §12.3.5)*
A plane wave is `f(x) = cos(k_μx^μ)` with constant wavevector `k`. Show
`□f = −(k·k) f`, so `f` solves the homogeneous wave equation `□f = 0` **iff** `k`
is null (`k·k = 0`). Take `k^μ = (1, 1, 0, 0)`.
*Answer:* `∂_μf = −sin(k·x)k_μ`, `∂_ν∂_μf = −cos(k·x)k_μk_ν`, so
`□f = η^{μν}∂_μ∂_νf = −(η^{μν}k_μk_ν)f = −(k·k)f`. For `k=(1,1,0,0)`,
`k·k = −1+1 = 0`, hence `□f = 0` — the seed of `□A^μ = −μ₀J^μ` (covariant Maxwell,
EM-18) and of the dispersion relation `E² = 𝐩²` for massless quanta.
*Check:* `mdot([1,1,0,0],[1,1,0,0])` → `0`; `dalembertian(lambda x: cos(klow·x), x)` ≈ `0`.

**Solution.** With $k$ constant, each derivative of $f=\cos(k_\mu x^\mu)$ brings down a factor of $k$:
$$\partial_\mu f=-\sin(k\cdot x)\,k_\mu,\qquad \partial_\mu\partial_\nu f=-\cos(k\cdot x)\,k_\mu k_\nu.$$
Contracting with $\eta^{\mu\nu}$ to build the d'Alembertian,
$$\Box f=\eta^{\mu\nu}\partial_\mu\partial_\nu f=-(\eta^{\mu\nu}k_\mu k_\nu)\,f=-(k\cdot k)\,f,$$
so $\Box f=0$ **iff** $k\cdot k=0$ (a null wavevector). For $k^\mu=(1,1,0,0)$, $k\cdot k=-1+1=0$, hence $\Box f=0$ - the seed of $\Box A^\mu=-\mu_0 J^\mu$ (EM-18) and of $E^2=\mathbf p^2$ for massless quanta. This matches `mdot([1,1,0,0],[1,1,0,0])` $=0$ and `dalembertian` $\approx 0$.
