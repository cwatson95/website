# RE-17 — Exact solutions & numerical relativity (notes)

Conventions: geometrized units `G = c = 1`; signature **mostly-plus** `(−,+,+,+)`;
a metric is a callable `x → g(x)` (matching RE-11). Curvature is evaluated by
handing each metric to RE-11's finite-difference `ricci` / `einstein_tensor`
(which import MA-17's `diffgeo`), so an "exact solution" here is **a metric we
write down and then verify** satisfies its field equation. The field-equation
residual is the correctness gate: a wrong component makes `ricci` non-zero.

## 1. The exact-solution landscape beyond Schwarzschild
Einstein's equations `G_{μν} = 8πT_{μν}` (RE-13) are ten coupled nonlinear PDEs;
closed-form solutions exist only with enough symmetry. Past Schwarzschild
(RE-14, static + spherical + vacuum) the three canonical exact metrics relax one
assumption each:

| metric | relaxes | field equation it solves | code |
|---|---|---|---|
| **Kerr** | drops spherical → axial; rotating, *vacuum* | `R_{μν}=0` | `kerr_metric(M,a)` |
| **Reissner–Nordström** | adds a *source* (charge `Q`) | `R_{μν}=8π(T^{EM})_{μν}≠0` | `reissner_nordstrom_metric(M,Q)` |
| **de Sitter** | adds `Λ`; maximally symmetric, *vacuum* | `G_{μν}+Λg_{μν}=0` | `de_sitter_metric(Λ)` |

Each degenerates back to Schwarzschild in a limit (`a→0`, `Q→0`, `Λ→0`), which
`test_*_reduces_to_schwarzschild` checks componentwise against
`curvature.schwarzschild_metric`.

## 2. Kerr — the rotating black hole (Boyer–Lindquist)
With `Σ = r² + a²cos²θ` and `Δ = r² − 2Mr + a²`, and spin per unit mass
`a = J/M`,
$$ds^2 = -\Big(1-\frac{2Mr}{\Sigma}\Big)dt^2
 - \frac{4Mar\sin^2\theta}{\Sigma}\,dt\,d\phi
 + \frac{\Sigma}{\Delta}dr^2 + \Sigma\,d\theta^2
 + \Big(r^2+a^2+\frac{2Ma^2r\sin^2\theta}{\Sigma}\Big)\sin^2\theta\,d\phi^2 .$$
It is a **vacuum** solution (`verify_vacuum(kerr_metric(1,a), x) ≈ 0` for any
`a`, well outside the horizon — `test_kerr_is_ricci_flat_vacuum`). Key structure:

- **Frame dragging.** The off-diagonal `g_{tφ} = −2Mar\sin^2θ/Σ` is non-zero iff
  `a≠0` (`test_kerr_frame_dragging_is_present`): the geometry itself rotates, so
  a zero-angular-momentum particle is dragged in `φ`. No static, diagonal
  coordinates exist inside the ergosphere.
- **Horizons.** `g^{rr}∝Δ=0` gives `r_± = M ± √(M²−a²)` (`kerr_horizons`). They
  are real iff `a ≤ M`; `a = M` is **extremal** (`r_+ = r_- = M`); `a > M` is a
  **naked singularity** (no horizon — the code raises). Roots satisfy
  `r_+ + r_- = 2M`, `r_+ r_- = a²`.
- **Ergosphere.** `g_{tt}=0` at the static-limit surface
  `r_E(θ) = M + √(M²−a²cos²θ)` (`kerr_ergosphere`). At the equator `r_E = 2M`,
  strictly **outside** `r_+` for `a>0` (`test_kerr_ergosphere_outside_horizon`);
  it touches `r_+` at the poles. In the ergoregion `r_+ < r < r_E` no observer
  can stay still (`∂_t` is spacelike) yet escape is still possible — the basis of
  the Penrose process.
- **Ring singularity.** `Σ=0` requires `r=0` *and* `θ=π/2`: the true (Kretschmann-
  divergent) singularity is a **ring**, not a point. `a→0` shrinks the ring to the
  Schwarzschild point and the metric reduces to Schwarzschild exactly (§1).

## 3. Reissner–Nordström — charge as a source
$$f(r) = 1 - \frac{2M}{r} + \frac{Q^2}{r^2},\qquad
  ds^2 = -f\,dt^2 + f^{-1}dr^2 + r^2 d\Omega^2 .$$
This is **not** Ricci-flat: it is sourced by the electromagnetic stress-energy of
the central charge (forward-ref EM-14), so `R_{μν} ≠ 0`
(`verify_vacuum > 0`, `test_reissner_nordstrom_is_not_ricci_flat`). The EM field
is **trace-free** in 4-D (`T^{EM}\,^μ_μ = 0`), hence the Ricci *scalar* still
vanishes, `R = −8πT = 0` — the code finds `ricci_scalar ≈ 0` while individual
`R_{μν}` components are `O(Q²/r²)`. Mixed components `G^t_t = G^r_r = −Q²/r^4`,
`G^θ_θ = G^φ_φ = +Q²/r^4`. Horizons at `f=0`: `r_± = M ± √(M²−Q²)`, real iff
`|Q| ≤ M`. `Q→0` recovers Schwarzschild and Ricci-flatness
(`test_reissner_nordstrom_reduces_to_schwarzschild`). This is the cleanest
demonstration that "curved ⇏ vacuum": the *same* `curvature.ricci` returns ≈0 for
Kerr and ≠0 for RN, reading off whether matter is present.

## 4. de Sitter — constant-curvature Λ-vacuum
The static patch, `f(r) = 1 − Λr²/3`, `ds² = −f\,dt² + f^{-1}dr² + r²dΩ²`, is the
**maximally symmetric** solution of the vacuum equations *with* a cosmological
constant. Adding `Λ` to RE-13's equations, `G_{μν} + Λg_{μν} = 8πT_{μν}`, the
vacuum (`T=0`) case is
$$\boxed{\,G_{\mu\nu} + \Lambda g_{\mu\nu} = 0\,}\quad\Longrightarrow\quad
  R_{\mu\nu} = \Lambda g_{\mu\nu},\qquad R = 4\Lambda \ \text{(4-D)} .$$
(Trace `G+Λg=0`: `−R + 4Λ = 0`.) `verify_einstein_lambda` returns
`max|G_{μν}+Λg_{μν}| ≈ 0` and `ricci_scalar ≈ 4Λ`
(`test_de_sitter_solves_lambda_vacuum`); without the `Λ` term de Sitter is *not*
plain-vacuum (`R_{μν}=Λg_{μν}≠0`). A **cosmological horizon** sits at
`r = √(3/Λ)`; `Λ<0` (anti-de Sitter) has none. de Sitter is the constant-`+`
curvature member of the same family whose spatial slices are the FLRW cosmologies
of RE-15 (`k=+1,0,−1`).

## 5. Going numerical — the 3+1 / ADM decomposition
A binary merger has *no* closed form, so we solve Einstein's equations as an
**initial-value (Cauchy) problem**: pick a spacelike slice, give data on it,
evolve. Foliate spacetime into slices `Σ_t` (`t = x⁰ = const`) and write
$$ds^2 = -\alpha^2 dt^2 + \gamma_{ij}\big(dx^i+\beta^i dt\big)\big(dx^j+\beta^j dt\big),$$
i.e. `g_{μν}` splits into

- **lapse** `α = 1/\sqrt{-g^{tt}}` — proper time per unit `t` between slices;
- **shift** `β^i = γ^{ij}g_{0j}` — how spatial coordinates slide slice-to-slice;
- **spatial metric** `γ_{ij} = g_{ij}` — the intrinsic geometry of `Σ_t`.

`adm_decompose(metric, x)` returns `(α, β^i, γ_{ij})`; for Minkowski in inertial
coordinates `α=1, β=0, γ=δ_{ij}` (`test_adm_minkowski_slice`), and for any static
diagonal metric `g_{tt}=−f` the lapse is `α=√f` with `β=0`
(`test_adm_lapse_from_inverse_metric`). The extrinsic curvature
`K_{ij} = −\tfrac1{2\alpha}(\partial_t γ_{ij} − D_iβ_j − D_jβ_i)` measures how
`Σ_t` bends in the embedding (how the unit normal turns).

**The split of Einstein's equations.** Gauss–Codazzi projects `G_{μν}=8πT_{μν}`
into pieces with no second time-derivative — the **constraints**, which every
slice must satisfy —
$$\underbrace{R^{(3)} + K^2 - K_{ij}K^{ij} = 16\pi\rho}_{\text{Hamiltonian}},
  \qquad
  \underbrace{D_j\!\big(K^{ij}-\gamma^{ij}K\big) = 8\pi S^i}_{\text{momentum}},$$
(`K = γ^{ij}K_{ij}`, `R^{(3)}` the intrinsic scalar curvature of `γ`), plus the
**evolution** equations `∂_t γ_{ij}`, `∂_t K_{ij}` that march the data forward.
`hamiltonian_constraint_flat(metric, x)` computes the Hamiltonian residual
`R^{(3)} + K² − K_{ij}K^{ij} − 16πρ`, taking `R^{(3)}` from `curvature.ricci_scalar`
on `spatial_slice_metric`, with the time-symmetric default `K_{ij}=0`.

**Initial data must satisfy the constraints.** Two checks make this concrete:
a flat Minkowski slice gives `R^{(3)}=0, K=0 ⇒ H=0`
(`test_adm_minkowski_slice`); and the `t=const` **Schwarzschild** slice — a
*curved* 3-geometry (`γ_{rr}=1/(1−2M/r)≠1`, the Flamm paraboloid) — is
nonetheless **scalar-flat**, `R^{(3)}=0`, so as a moment-of-time-symmetry
(`K_{ij}=0`) vacuum slice it satisfies `H=0` exactly
(`test_schwarzschild_slice_is_scalar_flat`). That `R^{(3)}=0` is not an accident:
it *is* the Hamiltonian constraint for a `K=0` vacuum slice, the same identity a
numerical-relativity code must enforce on its initial data.
