# RE-15 — Problems

Work them by hand, then check with `code/cosmology.py`. Sources in `../refs.md`.

### P1. Redshift and the scale factor  *(Dodelson §2.2)*
A quasar is observed at redshift `z = 3`. By what factor has the universe expanded
since the light was emitted? What was the scale factor `a_emit` (with `a₀ = 1`)?
*Answer:* `1+z = a₀/a_emit = 4`, so the universe has expanded by a factor **4** and
`a_emit = 1/(1+z) = 0.25`.
*Check:* `redshift(0.25)` → `3.0`; `redshift(0.5)` → `1.0` (the canonical `a=½ ⇒ z=1`).

**Solution.** Wavelengths stretch with the scale factor, so the observed-to-emitted
ratio is $1+z = a_{\rm obs}/a_{\rm emit}$. With $a_0=1$ today,
$$1+z = \frac{1}{a_{\rm emit}}\;\Longrightarrow\; a_{\rm emit}=\frac{1}{1+z}.$$
For $z=3$: $1+z=4$, so every comoving length — and the universe — has grown by a
factor $\mathbf{4}$, and $a_{\rm emit}=1/4=0.25$. The check inverts this: `redshift`
returns $z=a_{\rm obs}/a_{\rm emit}-1$, so `redshift(0.25)`$=1/0.25-1=3.0$ and the
canonical half-size universe `redshift(0.5)`$=1/0.5-1=1.0$.

### P2. Friedmann I from the Einstein tensor  *(Dodelson §2.1.3; the headline)*
For the flat FLRW metric, the time–time Einstein component is `G₀₀ = 3(ȧ/a)²`
(add `+3k/a²` when `k≠0`). Setting `G₀₀ = 8πT₀₀ = 8πρ` gives Friedmann I. Verify the
**coefficient is exactly 3** by feeding the metric to RE-11’s curvature engine.
*Answer:* `G₀₀ = 3[(ȧ/a)² + k/a²] = 3(ȧ²+k)/a²` ⇒ `(ȧ/a)² = 8πρ/3 − k/a²`.
*Check:* de Sitter `a=e^{Ht}`: `G00_from_flrw(de_sitter_scale_factor(1.0), 0, t)` ≈
`3H² = 3`; matter `a=t^{2/3}`: `G00_from_flrw(power_law_scale_factor(2/3), 0, 1.0)` ≈
`3·(2/3)² = 4/3` (`test_flrw_implies_friedmann_*`, loose FD tol).

**Solution.** Hand the flat FLRW metric to the curvature engine and its time–time Einstein
component comes back as
$$G_{00}=3\Big[\Big(\frac{\dot a}{a}\Big)^2+\frac{k}{a^2}\Big]=\frac{3(\dot a^2+k)}{a^2}.$$
The source is a comoving perfect fluid, whose energy density is $T_{00}=\rho$ (with
$g_{00}=-1$, $u_0=-1$, so $T_{00}=(\rho+p)u_0^2+p\,g_{00}=\rho$). The $00$ field equation
$G_{00}=8\pi T_{00}$ is therefore
$$3\Big[\Big(\frac{\dot a}{a}\Big)^2+\frac{k}{a^2}\Big]=8\pi\rho\;\Longrightarrow\;\Big(\frac{\dot a}{a}\Big)^2=\frac{8\pi}{3}\rho-\frac{k}{a^2},$$
the first Friedmann equation — the coefficient $3$ is not assumed but *read off* $G_{00}$.
The finite-difference curvature confirms it: for de Sitter $a=e^{Ht}$ ($H=1$, $k=0$)
`G00_from_flrw` $\to3.00\approx3H^2$, and for matter $a=t^{2/3}$ at $t=1$ it gives
$1.34\approx3(2/3)^2=4/3$.

### P3. The three eras  *(Zee §VIII.1; notes §5–6)*
For a flat universe with one fluid `p = wρ`, integrate the fluid equation to get
`ρ(a)`, then use Friedmann I to get `a(t)`. Specialise to radiation (`w=⅓`), matter
(`w=0`), and a cosmological constant (`w=−1`).
*Answer:* `ρ ∝ a^{−3(1+w)}`, `a ∝ t^{2/(3(1+w))}` (for `w≠−1`).
Radiation `ρ∝a⁻⁴, a∝t^{1/2}`; matter `ρ∝a⁻³, a∝t^{2/3}`; `Λ`: `ρ=const, a∝e^{Ht}`.
*Check:* `era_density(2.0, 1/3)=2⁻⁴`, `era_density(2.0, 0)=2⁻³`, `era_density(2.0,−1)=1`;
each era zeroes **both** Friedmann residuals (`test_three_eras_satisfy_both_friedmann`).

**Solution.** For $p=w\rho$ the fluid equation $\dot\rho=-3H(\rho+p)$ becomes
$\dot\rho/\rho=-3(1+w)\,\dot a/a$, which integrates to
$$\rho\propto a^{-3(1+w)} .$$
Feed this into flat Friedmann I, $(\dot a/a)^2=\tfrac{8\pi}{3}\rho\propto a^{-3(1+w)}$.
Trying $a\propto t^q$ gives $\dot a/a=q/t\propto a^{-3(1+w)/2}\propto t^{-3q(1+w)/2}$, so
matching powers of $t$ requires $-1=-3q(1+w)/2$, i.e.
$$q=\frac{2}{3(1+w)}\qquad(w\neq-1).$$
**Radiation** $w=\tfrac13$: $\rho\propto a^{-4}$, $a\propto t^{1/2}$; **matter** $w=0$:
$\rho\propto a^{-3}$, $a\propto t^{2/3}$; the **$\Lambda$** case $w=-1$ is special ($1+w=0$),
giving $\rho=$ const and exponential $a\propto e^{Ht}$. The density scalings are exactly
`era_density`: `era_density(2.0, 1/3)`$=2^{-4}$, `era_density(2.0, 0)`$=2^{-3}$,
`era_density(2.0,−1)`$=1$, and each $a(t)$ zeroes **both** Friedmann residuals
(`test_three_eras_satisfy_both_friedmann`).

### P4. Critical density and the geometry trichotomy  *(Dodelson Eqs. 2.39–2.40)*
Define `ρ_c = 3H²/8π` and `Ω = ρ/ρ_c`. From Friedmann I (Λ=0) show that the **sign of
`Ω−1` is the sign of `k`**, i.e. the universe is closed/flat/open according as
`Ω ≷ 1`.
*Answer:* `Ω − 1 = k/(a²H²)`, so `Ω>1 ⇔ k=+1` (closed), `Ω=1 ⇔ k=0` (flat),
`Ω<1 ⇔ k=−1` (open).
*Check:* `omega(critical_density(H), H)` → `1.0`; on-shell closed/open densities give
`Ω>1`/`Ω<1` (`test_omega_trichotomy_matches_curvature_sign`).

**Solution.** Friedmann I with $\Lambda=0$ is $H^2=\tfrac{8\pi}{3}\rho-\tfrac{k}{a^2}$.
Divide through by $H^2$ and use $\rho_c=3H^2/8\pi$, $\Omega=\rho/\rho_c=8\pi\rho/3H^2$:
$$1=\frac{8\pi\rho}{3H^2}-\frac{k}{a^2H^2}=\Omega-\frac{k}{a^2H^2}\;\Longrightarrow\;\Omega-1=\frac{k}{a^2H^2}.$$
Since $a^2H^2>0$, the sign of $\Omega-1$ is exactly the sign of $k$:
$$\Omega>1\iff k=+1\ (\text{closed}),\quad \Omega=1\iff k=0\ (\text{flat}),\quad \Omega<1\iff k=-1\ (\text{open}).$$
The density is its own geometer — weigh the universe and you know whether space curls back on
itself. The check sets $\rho=\rho_c$: `omega(critical_density(H), H)` $\to1.0$ (flat), while
the on-shell closed/open densities of `test_omega_trichotomy_matches_curvature_sign` give
$\Omega>1$ and $\Omega<1$ respectively.

### P5. The fluid equation is `∇_μTᵘᵛ=0`  *(notes §6; RE-11 §3)*
Show the fluid equation `ρ̇ = −3H(ρ+p)` is the `ν=0` part of `∇_μTᵘᵛ=0`, and explain
why it is **not** an independent equation. Interpret it as `dE = −p dV` for a comoving
volume `V ∝ a³`.
*Answer:* `∇_μGᵘᵛ=0` (contracted Bianchi, RE-11 §3) forces `∇_μTᵘᵛ=0`, so the fluid
equation follows from the two Friedmann equations — a consistency relation. `d(ρa³) =
−p d(a³)` is exactly `Ė = −pV̇`.
*Check:* `fluid_equation_residual` ≈ 0 to machine precision for `ρ∝a⁻³` (matter) and
`ρ∝a⁻⁴` (radiation) (`test_fluid_equation_matter_and_radiation`).

**Solution.** In FLRW a comoving perfect fluid has $u^\mu=(1,0,0,0)$ and
$T^\mu{}_\nu=\mathrm{diag}(-\rho,p,p,p)$. The $\nu=0$ component of $\nabla_\mu T^{\mu\nu}=0$ is
$$\dot\rho+\Gamma^\mu{}_{\mu0}\,\rho+\Gamma^0{}_{ij}T^{ij}=0,\qquad \Gamma^\mu{}_{\mu0}=\partial_0\ln\sqrt{-g}=3\frac{\dot a}{a},$$
where the last term supplies the pressure piece $3Hp$, giving $\dot\rho=-3H(\rho+p)$. It is
**not** an independent law: the contracted Bianchi identity $\nabla_\mu G^{\mu\nu}=0$ (RE-11
§3) makes $\nabla_\mu T^{\mu\nu}=0$ automatic, so once the two Friedmann equations (from
$G_{00}$ and $G_{ij}$) hold, this one follows — a consistency relation. Its meaning is the
first law $dE=-p\,dV$ for a comoving patch $V\propto a^3$: with $E=\rho V$ and $\dot V=3HV$,
$\dot E=-p\dot V$ reads $\dot\rho V+\rho(3HV)=-p(3HV)$, i.e. $\dot\rho=-3H(\rho+p)$.
Numerically `fluid_equation_residual` vanishes to machine precision for matter
$\rho\propto a^{-3}$ and radiation $\rho\propto a^{-4}$
(`test_fluid_equation_matter_and_radiation`).

### P6. Cosmic acceleration needs negative pressure  *(notes §3; Zee §VIII.1)*
From Friedmann II, `ä/a = −(4π/3)(ρ+3p) + Λ/3`, find the condition on the equation of
state for the expansion to **accelerate** (`ä>0`) with `Λ=0`. Why does de Sitter
(`p=−ρ`) accelerate?
*Answer:* `ä>0 ⇔ ρ+3p<0 ⇔ w<−1/3`. Dark energy `w=−1` (`p=−ρ`) satisfies it; then
`ä/a = (8π/3)ρ = H² > 0` and `a ∝ e^{Ht}`.
*Check:* `friedmann_2_residual(e^{H}, H²e^{H}, 3H²/8π, −3H²/8π)` ≈ 0 — de Sitter solves
Friedmann II with `p=−ρ` (`test_de_sitter_satisfies_both_friedmann_two_ways`).

**Solution.** With $\Lambda=0$ the acceleration equation is
$\ddot a/a=-\tfrac{4\pi}{3}(\rho+3p)$. Since $a>0$ and, for ordinary matter, $\rho>0$, the
expansion accelerates iff the bracket is negative:
$$\ddot a>0\iff \rho+3p<0\iff p<-\tfrac13\rho\iff w<-\tfrac13 .$$
So **pressure gravitates** — it is $\rho+3p$, not $\rho$, that sources deceleration — and only
a sufficiently negative pressure overturns the pull. Dark energy with $w=-1$ ($p=-\rho$)
clears the bar: then $\rho+3p=-2\rho$, and using flat Friedmann I ($H^2=\tfrac{8\pi}{3}\rho$),
$$\frac{\ddot a}{a}=-\frac{4\pi}{3}(-2\rho)=\frac{8\pi}{3}\rho=H^2>0,$$
a constant — so $a\propto e^{Ht}$, de Sitter. The check confirms it:
`friedmann_2_residual(e^{H}, H²e^{H}, 3H²/8π, −3H²/8π)` $\approx0$, de Sitter solving
Friedmann II with $p=-\rho$ (`test_de_sitter_satisfies_both_friedmann_two_ways`).
