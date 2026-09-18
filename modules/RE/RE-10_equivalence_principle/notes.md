# RE-10 — The Equivalence Principle (notes)

Conventions for this module (a **deliberate departure** from the trunk's `c = 1`):
all constants kept explicit in **SI** — `c = 2.99792458×10⁸ m/s`, `g = 9.80665 m/s²`,
`G = 6.674×10⁻¹¹`. Newtonian potential `Φ` in J/kg, with `Φ→0` at infinity and
`Φ<0` (more negative) deeper in a well. We use realistic numbers because their
*magnitudes* (a 22.5 m tower, a 1-g horizon at 0.97 ly) are the lesson.

## 1. The weak equivalence principle — universality of free fall (UFF)
Newton's second law `F = m_inertial a` and gravity `F = m_grav g` give
`a = (m_grav/m_inertial) g`. The **weak EP** is the empirical fact that
`m_grav = m_inertial` for every body, so **all bodies fall with the same `a`,
independent of mass or composition** (Galileo's leaning-tower/inclined-plane
result; Apollo 15's feather-and-hammer on the Moon). The figure of merit is the
**Eötvös ratio**
$$\eta=\frac{2\,|a_1-a_2|}{a_1+a_2}\qquad(\texttt{eotvos\_parameter}),$$
which UFF requires to vanish for all material pairs. Eötvös's torsion balance
(1890s–1922) reached `η≲10⁻⁹`; modern torsion balances (Eöt-Wash) and
lunar-laser-ranging give `η≲10⁻¹³`, and the MICROSCOPE satellite (2017–2022)
reached `~10⁻¹⁵` (Will §2.4, Table 2.2). No violation has ever been seen — this
universality is what lets gravity be reinterpreted as geometry.

## 2. Einstein's equivalence principle — "the happiest thought"
Because **everything** falls the same way, free fall is special. Einstein's 1907
insight (Zee, *Prologue to Book Two*): *"If a person falls freely he will not feel
his own weight."* Sharpened:

> A **uniformly accelerated frame** is **locally indistinguishable** from a
> **uniform gravitational field**. Equivalently, in a freely falling cabin the
> gravitational field is **locally removed** — the falling frame is *locally
> inertial* (a local Lorentz frame).

"Locally" is essential (§6): the cancellation is exact only at a point / over a
region small enough that the field's *variation* is negligible. The strong/Einstein
EP elevates this to *all* non-gravitational physics: in a local inertial frame the
laws reduce to those of special relativity (Will §2.3).

## 3. Gravitational redshift — from the EP **alone**, no field equations
Put a photon source on the floor of a box accelerating upward at `a` and a receiver
on the ceiling a height `h` higher. The light takes `t=h/c` to arrive; in that time
the receiver has gained speed `v=at=ah/c` *away* from the emission event, so by the
(first-order) Doppler formula
$$\frac{\Delta f}{f}=-\frac{v}{c}=-\frac{a\,h}{c^2}\qquad(\texttt{accelerated\_frame\_redshift}).$$
By the EP a real field `g=a` must do **exactly** the same, and writing `gh=ΔΦ`,
$$\boxed{\ \frac{\Delta f}{f}=-\frac{\Delta\Phi}{c^2}\ }\qquad(\texttt{grav\_redshift},\ \texttt{redshift\_uniform\_field}).$$
A photon **climbing out** of a well (`ΔΦ>0`) loses frequency — a **redshift**;
falling in, a blueshift. Equivalently **clocks deeper in a potential run slow**:
the proper rate is `dτ/dt ≈ 1+Φ/c²`, so
$$\frac{d\tau_\text{lower}}{d\tau_\text{upper}}\approx 1+\frac{\Phi_\text{lower}-\Phi_\text{upper}}{c^2}<1\qquad(\texttt{grav\_time\_dilation}).$$
Redshift and time dilation are **one phenomenon**: the redshift just *is* the lower
clock falling behind the upper one (`test_redshift_timedilation_consistency`).
**Pound & Rebka (1959)** measured `|Δf/f| = gh/c² ≈ 2.45×10⁻¹⁵` up the 22.5 m
Harvard tower (`pound_rebka`) — the first lab confirmation. GPS satellites must
correct for the same effect (net `~38 μs/day`).

## 4. The accelerating elevator — light bends in gravity
Same box, now a light ray crossing **horizontally** through width `L`. In the
crossing time `L/c` the floor accelerates up by `½g(L/c)²`, so the ray is deflected:
$$\text{drop}=\tfrac12 g\Big(\frac{L}{c}\Big)^2,\qquad
\theta\approx\frac{gL}{c^2}\qquad(\texttt{light\_deflection\_elevator}).$$
By the EP, light must bend in a real gravitational field. **Caveat (the factor of
two):** this uniform-field argument gives only **half** the true bending of starlight
grazing the Sun — Einstein's 1911 value `0.87″` versus the 1915 GR (and Eddington
1919) value `1.75″`. The missing half comes from **spatial curvature**, which the
EP alone cannot see; the EP fixes the *time* part of the metric, RE-11 supplies the
*space* part.

## 5. Rindler observers and horizons
An observer with constant **proper acceleration** `a` moves on the hyperbola
`x² − (ct)² = (c²/a)²` in spacetime (a "Rindler" trajectory). A light signal sent
from a distance greater than
$$d=\frac{c^2}{a}\qquad(\texttt{rindler\_horizon})$$
*behind* the observer can **never catch up** — there is an **acceleration horizon**.
As `a→0` it recedes to infinity (an inertial observer has none); for a 1-g rocket,
`c²/g ≈ 9.2×10¹⁵ m ≈ 0.97 light-years`. This Rindler horizon is the **local model**
of a black-hole event horizon (RE-14), and quantizing fields across it gives the
**Unruh temperature** `T = ℏa/2πck_B` — the accelerated-observer cousin of Hawking
radiation (QF-05).

## 6. Tidal forces — the **real**, non-removable field (= curvature)
Free fall removes the *uniform* part of gravity but never its *variation*. Two test
masses separated radially by `dr` at distance `r` from mass `M` feel different pulls;
their **relative** acceleration is the gradient of the field,
$$a_\text{tidal}=\frac{d}{dr}\!\Big(\frac{GM}{r^2}\Big)dr=\frac{2GM}{r^3}\,dr\qquad(\texttt{tidal\_acceleration}),$$
a **stretch** along `r` (with compression sideways — the trace `∇²Φ=0` in vacuum).
Crucially: `a_tidal→0` as `dr→0` (so any *single* point can be made locally inertial),
yet it is **nonzero for any finite separation** and **cannot be transformed away by
any change of frame**. In terms of the potential, the irreducible object is the
matrix of **second** derivatives `∂_i∂_j Φ` — the local field `∂_iΦ` is killed by
free fall, the **tidal tensor `∂_i∂_jΦ` is not**. This is exactly **geodesic
deviation**, and the tidal tensor is (the Newtonian limit of) the **Riemann
curvature tensor**: the precise statement is RE-11.

## 7. Why "gravity = geometry" follows
Stack the pieces. (i) UFF means a gravitational field affects *all* bodies
identically — like a property of spacetime itself, not a force with charges.
(ii) The EP says free fall is locally inertial, so freely falling worldlines are the
natural "straight lines." (iii) Clocks run at rates set by `Φ` (§3) — the *metric*
of spacetime is position-dependent. (iv) What survives free fall is the tidal tensor
(§6) — genuine **curvature**. So gravity is not a force on top of flat spacetime; it
is the **curvature of spacetime**, freely falling bodies follow its **geodesics**,
and "acceleration due to gravity" is the artifact of refusing to fall. The EP is the
hinge between special relativity (RE-03–RE-08) and the geometric theory (RE-11–RE-14).
