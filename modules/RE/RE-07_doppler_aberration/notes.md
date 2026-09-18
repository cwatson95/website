# RE-07 — Relativistic Doppler Effect & Aberration (notes)

Conventions: `c = 1`, event `x = (ct, x, y, z)`, η = diag(−1,+1,+1,+1),
`β = v/c`, `γ = 1/√(1−β²)`. Boosts are along **+x** by the active RE-03 boost
`ct' = γ(ct − βx)`, `x' = γ(x − βct)` — into a frame S′ moving at `+β x̂`.

## 0. The one idea — it's all one 4-vector
A plane light wave `∝ cos(ωt − 𝐤·𝐱) = cos(ηₘₙ kᵐxⁿ)` has a phase that is a Lorentz
**scalar** (every observer agrees how many wave crests have passed). Since `xᵐ` is
a 4-vector and the phase `kₘxᵐ` is invariant, the **4-wavevector**

$$k^\mu=\Big(\frac{\omega}{c},\,\mathbf k\Big)=(\omega,\ \mathbf k)\quad[c=1]$$

must itself be a 4-vector. For light the phase speed is `c`, so `|𝐤| = ω` and `k`
is **null**:
$$k\cdot k=\eta_{\mu\nu}k^\mu k^\nu=-\omega^2+|\mathbf k|^2=0 .$$
Write `𝐤 = ω n̂` with `n̂` the propagation direction, `θ` its angle from the boost
axis. Then **Doppler and aberration are not two effects** — they are the time part
and the space part of one transformation `k' = Λk`. (Zee derives exactly this from
`k = (ω, 𝐤)`, requiring `k'x' = kx`; printed 185, PDF 208.)

Boosting `k^μ = (ω, ω cosθ, ω sinθ, 0)` along `+x` with `Λ(β)` (RE-03):
$$\omega' = \gamma(\omega-\beta\,\omega\cos\theta)=\gamma\,\omega\,(1-\beta\cos\theta),\qquad
k_x' = \gamma\,\omega(\cos\theta-\beta),\qquad k_y'=\omega\sin\theta .$$
The first equation is **Doppler**; the ratio `k_x'/|\mathbf k'| = k_x'/\omega'` is
**aberration**. (`transform_wavevector` literally runs this `Λ` and reads both off.)

## 1. Longitudinal Doppler (motion along the line of sight)
Put `θ = π` (ray travelling −x, i.e. **receding** observer): `ω'/ω = γ(1+β)`… but it
is cleaner to quote the **observed/source** ratio `f_obs/f_src` for a source and
observer separating at speed `β`:
$$\boxed{\ \frac{f_{\rm obs}}{f_{\rm src}}=\sqrt{\frac{1-\beta}{1+\beta}}\ }\quad(\text{receding: redshift}<1),
\qquad \sqrt{\frac{1+\beta}{1-\beta}}\quad(\text{approaching: blueshift}>1).$$
(`doppler_longitudinal`.) The blueshift factor is the **Bondi k-factor**
`k = √((1+β)/(1−β))` (`bondi_k`), and the receding factor is `1/k`. Radar echoes
off a moving mirror multiply k-factors — Bondi's "k-calculus" rebuilds the whole
Lorentz transformation from this one number.

## 2. The general angular Doppler formula
For a ray at angle `θ` (propagation direction from the boost axis, measured in the
**observer's** frame),
$$\boxed{\ \frac{f_{\rm obs}}{f_{\rm src}}=\frac{1}{\gamma\,(1-\beta\cos\theta)}\ }$$
(`doppler_general`). It contains the two effects multiplied together: the classical
directional factor `1/(1−β cosθ)` **and** the relativistic time-dilation factor
`1/γ`. Limits:
- `θ = 0` → `1/(γ(1−β)) = √((1+β)/(1−β))` — head-on **blueshift**;
- `θ = π` → `1/(γ(1+β)) = √((1−β)/(1+β))` — receding **redshift**;
- `θ = π/2` → `1/γ` — the transverse effect below.

Zee writes the equivalent **emitter-angle** form `ω' = γω(1 + β cosθₑ)` (his Eq. 9,
printed 185–186): same physics, with `θ` measured in the other frame — aberration
(§4) converts between the two angles. The two forms agree exactly at `θ = 0, π`
(where there is nothing to aberrate) and differ only in how the *same* shift is
labelled by angle in between.

## 3. The transverse Doppler effect — a pure time dilation
At `θ = π/2` the source has **no radial velocity** at the instant of reception, so a
*classical* Doppler theory predicts **no** shift. Relativity predicts
$$\boxed{\ \frac{f_{\rm obs}}{f_{\rm src}}=\frac{1}{\gamma}<1\ }$$
(`doppler_transverse`) — a redshift with no line-of-sight motion at all. It is
**nothing but time dilation**: the moving source's clock (and hence its emitted
frequency) runs slow by `γ`. This is the cleanest experimental signature that
special relativity is more than the classical Doppler effect (Ives–Stilwell 1938;
later Mössbauer-rotor experiments). It has no non-relativistic analogue.

> Aside on the angle convention: "transverse" must specify *whose* `π/2`. At the
> observer-frame angle `θ_obs = π/2` one gets exactly `1/γ` (used here). At the
> *source*-frame angle `π/2` one instead gets the blueshift `γ`; the two differ by
> the aberration that tilts `π/2` between frames. We fix `θ` in the observer frame
> throughout, which is what a detector actually measures.

## 4. Relativistic aberration — the direction transforms too
Dividing `k_x' = γω(cosθ−β)` by `ω' = γω(1−β cosθ)`:
$$\boxed{\ \cos\theta'=\frac{\cos\theta-\beta}{1-\beta\cos\theta}\ },\qquad
\sin\theta'=\frac{\sin\theta}{\gamma\,(1-\beta\cos\theta)}$$
(`aberration`). Here `θ` is the ray's angle in S and `θ'` its angle in S′ (moving at
`+β`). This is a *bigger* effect than the classical "raindrops on a moving car"
picture because of the extra `γ` in `sinθ'`.

- **Aberration of starlight.** As Earth orbits the Sun (β ≈ 10⁻⁴), a star's apparent
  position swings annually toward Earth's instantaneous direction of motion by up to
  `≈ β` rad ≈ 20.5″. Bradley measured this in 1727 — direct evidence that light has a
  finite speed *and* that the observer's motion matters (Griffiths notes it,
  historically, alongside Michelson–Morley; printed 505, PDF 523).
- **Sign of the swing.** Under the `+β` boost a ray bends toward `θ = π` (the
  direction the *source* appears to move in S′): `θ' > θ` for `0 < θ < π`. The
  familiar forward **headlight/beaming** picture — a source moving in `+x` bunching
  its light toward `+x` — is the *same* formula taken the other way (rest-frame →
  lab is a `−β` boost), giving `θ' < θ`. Code: `aberration(θ, +β) > θ` and
  `aberration(θ, −β) < θ`.

### The headlight (beaming) effect
A source radiating **isotropically in its rest frame** and moving at `β` in the lab
has its light swept forward. The rest-frame transverse ray `θ_rest = π/2` aberrates
to the lab angle `cosθ_lab = β`, so **half** the photons (the rest-frame forward
hemisphere) fall inside the lab-frame cone of half-angle
$$\boxed{\ \theta_c=\arccos\beta\ }$$
(`headlight_halfangle` `= aberration(π/2, −β)`). As `β → 1`, `θ_c → 0`: the emission
collapses into a tight forward pencil of order `1/γ`. This is why relativistic jets,
synchrotron sources, and colliding-beam final states are so sharply forward-peaked,
and why `γ⁶` beaming dominates synchrotron power (cf. `~EM-18`).

## 5. Why one boost suffices (the cross-check)
The module's headline test boosts `k = four_wavevector(ω, θ)` with the **same** RE-03
`Λ(β)` used everywhere in the trunk and reads off:
- `ω/ω' = doppler_general(β, θ)` (Doppler from the time component), and
- `atan2(k_y', k_x') = aberration(θ, β)` (aberration from the spatial direction),

with `k'·k' = 0` preserved. (`ω/ω'` rather than `ω'/ω` because, with `θ` the
*observer*-frame angle, the boost carries the observer-frame ray into the source
frame; the observed-over-emitted ratio is `ω_obs/ω_src = ω/ω'`. Boost the other way
and it reads `ω'/ω` — a labelling choice, not new physics.) That single `Λ` *is* the
relativistic Doppler effect and aberration, simultaneously and exactly.

## 6. Penrose–Terrell rotation (conceptual)
A subtle, separate point: aberration is about **frequency and direction of rays**;
what a fast object *looks like* in a snapshot is governed by the photons that arrive
**simultaneously** at the camera, which left the object at different times. Penrose
and Terrell (1959) showed the net effect on a moving sphere is that it still presents
a **circular** outline — it is not "length-contracted into an ellipse" as naive
contraction suggests; instead the body appears **rotated** (Terrell rotation). A
small sphere subtends the same angular size and looks undistorted; extended objects
look turned by an angle set by the same aberration `cosθ' = (cosθ−β)/(1−β cosθ)`.
Length contraction is still real (it is what you *measure* with simultaneous rulers);
it is just not what a single camera *photographs*. We note this only conceptually —
no code — to keep "what is measured" distinct from "what is seen."
