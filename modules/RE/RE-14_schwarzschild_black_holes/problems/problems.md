# RE-14 — Problems

Work them by hand, then check with `code/schwarzschild.py`. Sources in `../refs.md`.
Geometrized units `G=c=1` throughout; `M_⊙ = 1.477 km`.

### P1. Horizon vs singularity  *(Zee §VII.2; cpope §10)*
Schwarzschild is a vacuum solution, so `R_{μν}=0` and every Ricci-based scalar
vanishes. Using the Kretschmann scalar `K = 48M²/r⁶`, decide which of `r=2M` and
`r=0` is a *real* (curvature) singularity and which is a coordinate artefact.
*Answer:* `r=0` is real (`K→∞`); `r=2M` is only a coordinate singularity —
`K(2M)=48M²/(2M)⁶ = 3/(4M⁴)` is finite. The horizon is a regular one-way surface.
*Check:* `kretschmann_formula(2, 1)` → `0.75`; RE-11's `curvature.kretschmann(schwarzschild_metric(1), [0,r,1,0.9])` ≈ `48/r⁶` for `r>2M` (`test_kretschmann_matches_formula_and_horizon_is_finite`).

**Solution.** In vacuum $R_{\mu\nu}=0$, so the Ricci scalar and every invariant built from $R_{\mu\nu}$ vanishes; the first surviving curvature scalar is the Kretschmann invariant
$$K = R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma} = \frac{48M^2}{r^6}.$$
At $r=0$, $K\to\infty$: tidal forces diverge and no coordinate change removes it — a **real** curvature singularity, where geodesics end. At the horizon,
$$K(2M)=\frac{48M^2}{(2M)^6}=\frac{48M^2}{64M^6}=\frac{3}{4M^4},$$
which is *finite*, so spacetime there is perfectly regular — only the $(t,r)$ chart fails (like a map's pole). Hence $r=2M$ is a **coordinate** singularity (the one-way event horizon) and $r=0$ the physical one. For $M=1$, $K(2M)=3/4$, matching `kretschmann_formula(2, 1)` → `0.75`.

### P2. The ISCO from the effective potential  *(Zee §VII.1, Eq. 8)*
For a massive particle, `V(r)=(1−2M/r)(1+L²/r²)`. Solve `V'(r)=0` and show circular
orbits exist only for `L ≥ 2√3 M`, the two roots merging at the **innermost stable
circular orbit**. Find its radius.
*Answer:* `V'(r)=0 ⇒ Mr²−L²r+3ML²=0`; real roots need `L⁴≥12M²L² ⇒ L≥2√3 M`; at
equality `r = L²/2M = 6M`. So `r_ISCO = 6M`.
*Check:* `isco(1)` → `6`; `isco_from_potential(1)` → `6.000`;
`circular_orbit_radius(2*3**0.5, 1)` → `6` and `circular_orbit_radius(0.99*2*3**0.5, 1)` → `None` (`test_isco_is_marginal_circular_orbit`).

**Solution.** Expand $V(r)=(1-2M/r)(1+L^2/r^2)=1-\dfrac{2M}{r}+\dfrac{L^2}{r^2}-\dfrac{2ML^2}{r^3}$ and differentiate:
$$V'(r)=\frac{2M}{r^2}-\frac{2L^2}{r^3}+\frac{6ML^2}{r^4}=0\;\Longrightarrow\; Mr^2-L^2r+3ML^2=0$$
(after multiplying by $r^4/2$). The roots $r_\pm=\big[L^2\pm\sqrt{L^4-12M^2L^2}\big]/(2M)$ are real only when $L^4\ge12M^2L^2$, i.e. $L\ge 2\sqrt3\,M$. At equality the discriminant vanishes and the stable minimum ($r_+$) and unstable maximum ($r_-$) **merge** at
$$r=\frac{L^2}{2M}=\frac{12M^2}{2M}=6M.$$
So $r_\text{ISCO}=6M$ — inside it no stable circular orbit exists. This is why `isco(1)` → `6`, `isco_from_potential(1)` → `6.000`, and `circular_orbit_radius(2*3**0.5, 1)` → `6`, while $L$ a hair below $2\sqrt3\,M$ returns `None`.

### P3. The photon sphere  *(Zee §VII.1, Eq. 12)*
For light, `V_γ(r)=(1−2M/r)L²/r²`. Show it has a single maximum, independent of
`L`, and locate the unstable circular photon orbit (the "photon sphere").
*Answer:* `V_γ'(r)=L²(−2/r³+6M/r⁴)=0 ⇒ r=3M`, a maximum (unstable). Hence
`r_photon = 3M`, independent of `L`.
*Check:* `photon_sphere(1)` → `3`; `photon_sphere_from_potential(1)` → `3.000`
(`test_photon_sphere_is_maximum_of_massless_potential`).

**Solution.** For light $V_\gamma(r)=(1-2M/r)L^2/r^2=L^2\big(r^{-2}-2Mr^{-3}\big)$, so
$$V_\gamma'(r)=L^2\Big(-\frac{2}{r^3}+\frac{6M}{r^4}\Big)=\frac{2L^2}{r^4}\,(3M-r)=0\;\Longrightarrow\; r=3M,$$
independent of $L$, which factors out entirely. The nature is a maximum: $V_\gamma''=L^2(6r^{-4}-24Mr^{-5})$ evaluated at $r=3M$ is $-6L^2/(243M^4)<0$, so the circular photon orbit is **unstable** — a light ray there can circle but the slightest nudge sends it spiralling in or out. Hence $r_\text{photon}=3M$, matching `photon_sphere(1)` → `3` and `photon_sphere_from_potential(1)` → `3.000`.

### P4. Mercury's perihelion precession  *(Zee §VI.3)*
The relativistic `−2ML²/r³` term advances the perihelion by
`Δφ = 6πM/(a(1−e²))` per orbit. With Mercury's `a, e` and `M=M_⊙`, convert to
arcseconds per century and compare with the historic anomaly.
*Answer:* `≈ 42.98″/century` (the famous `43″`). Newtonian ellipses are closed:
set `M→0` and `Δφ→0`.
*Check:* `perihelion_precession(M_SUN, A_MERCURY, E_MERCURY) * (100*365.25/T_MERCURY_DAYS) * ARCSEC_PER_RAD` → `42.98` (`test_mercury_perihelion_precession`).

**Solution.** The semi-latus rectum is $a(1-e^2)$, so the per-orbit advance is $\Delta\varphi=6\pi M/[a(1-e^2)]$. With $M=M_\odot=1476.6\,$m, $a=5.79\times10^{10}\,$m, $e=0.20563$,
$$\Delta\varphi=\frac{6\pi M_\odot}{a(1-e^2)}\approx 5.019\times10^{-7}\ \text{rad/orbit}.$$
Mercury completes $100\times365.25/87.9691\approx 415.2$ orbits per century; converting radians with $1\,\text{rad}=206264.8''$,
$$\Delta\varphi\cdot\frac{100\cdot365.25}{T}\cdot 206264.8''\approx 42.98''/\text{century}.$$
This is the famous $43''$ anomaly Einstein recovered. Setting $M\to0$ removes the GR $-2ML^2/r^3$ term and $\Delta\varphi\to0$ — Newtonian ellipses close. The check returns `42.98`.

### P5. Light deflection and the factor of two  *(Zee §VI.3; RE-10 §4)*
A ray grazing the Sun bends by `4M/b`. Evaluate for `b=R_⊙`, and explain why it is
**twice** the equivalence-principle value `2M/b` (`0.87″`) of RE-10.
*Answer:* `4M_⊙/R_⊙ = 8.49×10⁻⁶ rad = 1.75″` (Eddington 1919). The EP "accelerating
elevator" captures only the time-dilation half; the spatial curvature `g_{rr}=1/f`
supplies the missing half — exactly doubling the bend.
*Check:* `light_deflection(M_SUN, R_SUN)*ARCSEC_PER_RAD` → `1.751`; and it equals
`2 * (2*M_SUN/R_SUN)` (`test_solar_light_deflection`).

**Solution.** The full Schwarzschild deflection is $\Delta\varphi=4M/b$. Grazing the Sun, $b=R_\odot$:
$$\Delta\varphi=\frac{4M_\odot}{R_\odot}=\frac{4(1476.6\,\text{m})}{6.957\times10^{8}\,\text{m}}=8.49\times10^{-6}\ \text{rad}=1.75''.$$
The equivalence-principle "falling photon" of RE-10 gives only $2M/b=0.88''$: that is the contribution of gravitational time dilation ($g_{tt}$) alone. The spatial curvature $g_{rr}=1/f=(1-2M/r)^{-1}$ — which a uniformly accelerating elevator cannot mimic — supplies an equal second half, **doubling** the bend to $4M/b$. Hence `light_deflection(M_SUN, R_SUN)*ARCSEC_PER_RAD` → `1.751`, exactly `2 * (2*M_SUN/R_SUN)`.

### P6. Gravitational redshift — two limits  *(Zee §VI.3; RE-10 §3)*
From `1+z = √((1−2M/r_obs)/(1−2M/r_emit))`, recover (a) the weak-field Pound–Rebka
result for `r≫M`, and (b) the behaviour as the emitter approaches the horizon.
*Answer:* (a) `z ≈ M/r_emit − M/r_obs = ΔΦ/c²` — RE-10's `gh/c²`. (b) as
`r_emit→2M`, `z→∞`: infinite redshift, the emitter freezes and fades to a distant
observer.
*Check:* `gravitational_redshift(1e6, 1e9, 1)` ≈ `1e-6 − 1e-9`
(`test_redshift_weak_field_limit`); `gravitational_redshift(2.0001, 1e9, 1)` ≈ `140`
and grows (`test_redshift_diverges_at_horizon`).

**Solution.** Write $1+z=\sqrt{(1-2M/r_\text{obs})/(1-2M/r_\text{emit})}$. **(a)** For $r\gg M$ expand each root: $\sqrt{1-2M/r_\text{obs}}\approx1-M/r_\text{obs}$ and $(1-2M/r_\text{emit})^{-1/2}\approx1+M/r_\text{emit}$, so
$$1+z\approx 1+\frac{M}{r_\text{emit}}-\frac{M}{r_\text{obs}}\;\Longrightarrow\; z\approx\frac{M}{r_\text{emit}}-\frac{M}{r_\text{obs}}=\frac{\Delta\Phi}{c^2},$$
RE-10's Pound–Rebka $gh/c^2$; for $(10^6,10^9,1)$ this is $10^{-6}-10^{-9}=9.99\times10^{-7}$, the returned $z$. **(b)** As $r_\text{emit}\to2M$ the denominator $1-2M/r_\text{emit}\to0^+$ while the numerator stays finite, so $1+z\to\infty$: light from just above the horizon is infinitely redshifted and the emitter appears to freeze and fade to black. At $r_\text{emit}=2.0001M$, `gravitational_redshift(2.0001, 1e9, 1)` ≈ `140` and climbs without bound.

### P7. Falling in — whose clock?  *(cpope §10.2; conceptual)*
An observer falls radially from rest at `r_0`. Argue that they reach `r=2M` (and
`r=0`) in **finite proper time**, yet a distant observer using Schwarzschild `t`
**never** sees them cross. Reconcile the two.
*Answer:* `dτ` stays finite through `r=2M`, but `dt/dr ∝ 1/f → ∞` there, so
`t ~ −2M ln(r−2M) → ∞`. Both are correct: `t` is a bad coordinate at the horizon
(P1), while the infaller's proper time is physical. The distant image asymptotes to
the horizon, redshifting to black (P6).
*(No single code check — this is the global statement behind the redshift divergence.)*

**Solution.** For radial infall from rest at $r_0$ the conserved energy is $E=\sqrt{1-2M/r_0}$, and the radial equation gives $(dr/d\tau)^2=E^2-(1-2M/r)=\dfrac{2M}{r}-\dfrac{2M}{r_0}$ — finite and *nonzero* at $r=2M$. Integrating $d\tau=dr/\sqrt{2M/r-2M/r_0}$ converges right through the horizon down to $r=0$ in **finite** proper time $\sim\pi M(r_0/2M)^{3/2}$. But the bookkeeper's clock obeys $dt/d\tau=E/f$ with $f=1-2M/r$, so
$$\frac{dt}{dr}=\frac{dt/d\tau}{dr/d\tau}\propto\frac1f\xrightarrow{r\to2M}\infty,\qquad t\sim-2M\ln(r-2M)\to\infty.$$
Both statements hold because $t$ is a bad coordinate at $r=2M$ (the coordinate singularity of P1): it diverges even though the infaller's proper time — the physical clock — is finite. The distant image therefore asymptotes to the horizon, redshifting to black (P6).
