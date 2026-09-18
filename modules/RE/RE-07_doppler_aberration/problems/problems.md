# RE-07 — Problems

Work them by hand, then check with `code/doppler_aberration.py`. Sources in
`../refs.md` (Zee §III.3–III.4; Griffiths Ch. 12). Convention: `c=1`, `θ` is the
ray's propagation angle from the boost axis in the observer's frame; `θ=0` blueshift,
`θ=π` redshift.

### P1. Longitudinal redshift & the Bondi k-factor  *(Zee §III.3, printed 185–186)*
A galaxy recedes from us at `β = 0.6`. By what factor is an emission line's
frequency shifted, and by what factor does its wavelength stretch?
*Answer:* `f_obs/f_src = √((1−0.6)/(1+0.6)) = √(0.25) = 0.5` — the frequency halves,
the wavelength **doubles**. The blueshift for the time-reversed approach is the Bondi
`k = √(1.6/0.4) = 2`, and `0.5 = 1/k`.
*Check:* `doppler_longitudinal(0.6) → 0.5`, `bondi_k(0.6) → 2.0`, product `= 1`.

**Solution.** For a source receding along the line of sight the longitudinal factor is
$$\frac{f_{\rm obs}}{f_{\rm src}}=\sqrt{\frac{1-\beta}{1+\beta}}=\sqrt{\frac{1-0.6}{1+0.6}}=\sqrt{\frac{0.4}{1.6}}=\sqrt{0.25}=0.5 .$$
The frequency halves, and since $\lambda\propto1/f$ the wavelength **doubles**. The approaching
(time-reversed) case is the reciprocal — the Bondi factor $k=\sqrt{(1+\beta)/(1-\beta)}=\sqrt{1.6/0.4}=2$
— so the receding shift is exactly $1/k=0.5$. Hence `doppler_longitudinal(0.6)`→`0.5`,
`bondi_k(0.6)`→`2.0`, and their product is `1`.

### P2. The transverse Doppler effect is time dilation  *(Zee §III.3, printed 186)*
A source flies past at `β = 0.5`; you record its frequency at the instant it is
exactly abeam (`θ = 90°`, zero radial velocity). Classical theory predicts no shift —
what does relativity predict?
*Answer:* a **redshift** `f_obs/f_src = 1/γ = √(1−0.25) = 0.8660`, purely the moving
clock running slow. This is the Ives–Stilwell signature of SR.
*Check:* `doppler_transverse(0.5) → 0.86603`, equal to `doppler_general(0.5, π/2)`.

**Solution.** At the abeam instant ($\theta=90^\circ$) there is no line-of-sight velocity, so
classical theory predicts no shift. The relativistic factor at $\theta=\pi/2$ retains only the
time-dilation piece:
$$\frac{f_{\rm obs}}{f_{\rm src}}=\frac{1}{\gamma(1-\beta\cos90^\circ)}=\frac{1}{\gamma}=\sqrt{1-\beta^2}=\sqrt{1-0.25}=0.8660 .$$
It is a pure **redshift**: the moving source's clock runs slow by $\gamma$, so its frequency
arrives lowered even with zero radial motion. This transverse effect (Ives–Stilwell, 1938) has
no classical analogue. Numerically `doppler_transverse(0.5)`→`0.86603`, equal to
`doppler_general(0.5, π/2)`.

### P3. One boost = Doppler **and** aberration  *(Zee §III.3 "The relativistic Doppler shift", printed 185)*
A ray of frequency `ω = 1` heads off at `θ = 60°` (observer frame). Boost to the
frame moving at `β = 0.6` along `+x`. Find the new frequency ratio and the new
direction *two ways*: from the Doppler/aberration formulas, and by transforming the
4-wavevector `kᵘ = (ω, ω cosθ, ω sinθ, 0)`.
*Answer:* `γ = 1.25`; Doppler `f_obs/f_src = 1/(1.25·(1−0.6·0.5)) = 1/0.875 = 1.142857`;
aberration `cosθ' = (0.5−0.6)/(0.7) = −1/7 ⇒ θ' = 98.21°`. The boosted `kᵘ` reproduces
both, and stays null.
*Check:* `k = four_wavevector(1, math.radians(60)); kp = transform_wavevector(0.6, k)`;
then `wavevector_frequency(k)/wavevector_frequency(kp) → 1.142857 = doppler_general(0.6, 60°)`
and `math.degrees(wavevector_angle(kp)) → 98.2132 = math.degrees(aberration(60°, 0.6))`,
with `_mink2(kp) ≈ 0`.

**Solution.** With $\beta=0.6$, $\gamma=1/\sqrt{1-0.36}=1.25$ and $\cos60^\circ=\tfrac12$. The
angular Doppler factor is
$$\frac{f_{\rm obs}}{f_{\rm src}}=\frac{1}{\gamma(1-\beta\cos\theta)}=\frac{1}{1.25\,(1-0.6\cdot0.5)}=\frac{1}{1.25\cdot0.7}=\frac{1}{0.875}=1.142857,$$
and the aberration angle obeys
$$\cos\theta'=\frac{\cos\theta-\beta}{1-\beta\cos\theta}=\frac{0.5-0.6}{0.7}=-\frac{1}{7}\ \Rightarrow\ \theta'=98.21^\circ .$$
Boosting the null wavevector $k^\mu=(1,\tfrac12,\tfrac{\sqrt3}{2},0)$ with the RE-03 $\Lambda(0.6)$
reproduces both — Doppler is its time component, aberration its spatial direction — and keeps
$k'\cdot k'=0$. So `wavevector_frequency(k)/wavevector_frequency(kp)`→`1.142857`, equal to
`doppler_general(0.6, 60°)`, and `math.degrees(wavevector_angle(kp))`→`98.2132`, the aberration
angle, with `_mink2(kp)`$\approx0$.

### P4. Aberration of starlight  *(Griffiths §12.1, printed 505 — named; formula Zee §III.3)*
Earth orbits the Sun at `v ≈ 29.8 km/s`, so `β ≈ 9.93×10⁻⁵`. A star seen broadside
(`θ = 90°`) is displaced by aberration. Estimate the annual swing.
*Answer:* for small `β`, `θ' − 90° ≈ β` rad `= 9.93×10⁻⁵ rad ≈ 20.5″` — Bradley's
1727 "constant of aberration." The apparent position shifts toward the apex (Earth's
direction of motion); over a year it traces a small ellipse. (Note: `θ` here is the
ray's propagation angle; the *line of sight to the star* is the opposite direction,
which is why the apparent star moves toward, not away from, the apex.)
*Check:* `math.degrees(aberration(math.pi/2, 9.93e-5) - math.pi/2)*3600 → 20.49`
(arcseconds).

**Solution.** For a broadside ray $\theta=90^\circ$ ($\cos\theta=0$) the aberration law gives
$$\cos\theta'=\frac{\cos\theta-\beta}{1-\beta\cos\theta}=\frac{-\beta}{1}=-\beta\ \Rightarrow\ \theta'=\arccos(-\beta)=\frac{\pi}{2}+\arcsin\beta .$$
For tiny $\beta$, $\arcsin\beta\approx\beta$, so the swing is
$\theta'-\tfrac{\pi}{2}\approx\beta=9.93\times10^{-5}$ rad. Converting, $\beta\cdot206265\approx20.5$
arcsec — Bradley's 1727 constant of aberration. The apparent star shifts toward the apex
(Earth's instantaneous direction of motion), tracing a small ellipse over the year. Indeed
`math.degrees(aberration(math.pi/2, 9.93e-5) - math.pi/2)*3600`→`20.49` arcseconds.

### P5. The relativistic headlight  *(Zee §III.3; cf. EM-18 beaming)*
A source radiates isotropically in its rest frame and moves at `β = 0.99` in the lab.
Inside what forward half-angle does **half** of its light emerge?
*Answer:* the rest-frame transverse ray aberrates to `cosθ_c = β`, so
`θ_c = arccos(0.99) = 8.11° ≈ √(2(1−β)) = 0.141 rad`. Half the photons fall in this
tight forward cone — the beaming that makes relativistic jets look one-sided.
*Check:* `headlight_halfangle(0.99) → 0.14155 rad` `(8.110°)`, and it equals
`aberration(math.pi/2, -0.99)`; `cos(that) → 0.99`.

**Solution.** A source isotropic in its rest frame emits half its photons into the rest-frame
forward hemisphere ($\theta_{\rm rest}<90^\circ$). Its boundary ray $\theta_{\rm rest}=90^\circ$
aberrates (rest$\to$lab is a $-\beta$ boost) to the lab cone half-angle $\theta_c$ with
$\cos\theta_c=\beta$:
$$\theta_c=\arccos(0.99)=0.14155\ \text{rad}=8.11^\circ .$$
As $\beta\to1$ this collapses: $\theta_c\approx\sqrt{2(1-\beta)}=\sqrt{0.02}=0.141$ rad, a forward
pencil of order $1/\gamma$. Half the light is beamed into this tight cone — the relativistic
headlight effect that makes jets look one-sided. So `headlight_halfangle(0.99)`→`0.14155` rad
($8.110^\circ$), equal to `aberration(math.pi/2, -0.99)`, with $\cos\theta_c\to0.99$.

### P6. What you *see* vs what you *measure* — Terrell rotation  *(conceptual; refs P–T 1959)*
A sphere flies past at `β` close to 1. Length contraction says it is squashed to an
ellipsoid along the motion. Yet Penrose and Terrell showed a photograph still shows a
**circular** outline. Resolve the apparent contradiction.
*Answer:* a camera records photons arriving **simultaneously**, which left the sphere
at **different** times; combined with aberration, the far side becomes visible and the
net effect is an apparent **rotation**, not a squash — the circular silhouette is
preserved. Length contraction is what *simultaneous rulers measure*, not what one
lens *photographs*; both are correct answers to different questions. The outline-ray
directions transform by the very same `cosθ' = (cosθ−β)/(1−β cosθ)` used throughout
this module.
*Check:* conceptual — no code. See `notes.md` §6; contrast with the *measured*
contraction in `~RE-04`.

**Solution.** Length contraction and a photograph answer *different* questions. Contraction is
what **simultaneous** lab rulers measure: the sphere's extent along $\mathbf v$ is genuinely
$1/\gamma$ shorter. A camera instead records photons that **arrive together** but **left at
different times** — light from the receding far side departed earlier, when the sphere was
elsewhere, so that side becomes visible. Combined with aberration of the outline rays — which
transform by the same $\cos\theta'=(\cos\theta-\beta)/(1-\beta\cos\theta)$ used throughout this
module — the net optical effect is an apparent **rotation** (Penrose–Terrell, 1959), not a
squash, and a sphere's silhouette stays exactly **circular**. No contradiction: the *measured*
contraction (`~RE-04`) and the *photographed* rotation are both right, answering the distinct
questions "what do simultaneous rulers read?" versus "what does one lens capture?". Conceptual —
no code; see `notes.md` §6.
