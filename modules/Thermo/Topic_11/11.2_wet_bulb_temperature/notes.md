Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`)

# 11.2 — Wet-Bulb Temperature & Adiabatic Saturation (notes)

## 1. The wet-bulb thermometer
The **wet-bulb temperature** $T_{wb}$ is read from a thermometer whose bulb is wrapped in
a water-soaked wick [M §12.6, p.764]. When unsaturated air flows past, water evaporates
into it, and the energy of vaporization is drawn from the wick, so its steady temperature
falls **below the dry-bulb temperature** — an *evaporative-cooling* reading. Mounted
beside a dry-bulb thermometer it forms a **psychrometer** (Fig. 12.8). The two readings
together **fix the moist-air state** and locate it on the chart [M §12.7, p.766]:
dry-bulb on the abscissa, constant-$T_{wb}$ lines running upper-left to lower-right. The
**wet-bulb depression** $T - T_{wb}$ grows as the air gets drier (zero at saturation).

> $T_{wb}$ is *not* a mixture property — it depends on geometry, air speed, supply-water
> temperature [M §12.6, p.765]. Its usefulness is that, for normal psychrometric
> conditions, it closely approximates the **adiabatic-saturation temperature** $T_{as}$.

## 2. The adiabatic saturator → humidity ratio from $T_{as}$
An **adiabatic saturator** is an insulated, steady, two-inlet/one-exit duct: unsaturated
air ($p, T, \omega$) enters, contacts a water pool, and leaves **saturated** at $T_{as}$,
with makeup water added at $T_{as}$ [M §12.5.5, p.763]. Mass + energy balances per unit
dry air give [M Eq. 12.50, p.764]:
$$(h_a + \omega h_g)_T + (\omega' - \omega)\,h_f(T_{as}) = (h_a + \omega' h_g)_{T_{as}},$$
which solves for the unknown humidity ratio [M Eq. 12.48, p.763]:
$$\boxed{\;\omega = \dfrac{h_a(T_{as}) - h_a(T) + \omega'\,[h_g(T_{as}) - h_f(T_{as})]}
{h_g(T) - h_f(T_{as})}\;}\quad(12.48),$$
where the *exit* (saturated) humidity ratio is [M Eq. 12.49, p.763]:
$$\omega' = 0.622\,\frac{p_g(T_{as})}{p - p_g(T_{as})}\quad(12.49).$$
Thus three measurable quantities — $p$, $T$, and $T_{as}$ — determine $\omega$. The
dry-air enthalpy difference may use $h_a(T_{as})-h_a(T)=c_{pa}(T_{as}-T)$.

## 3. Wet-bulb $\approx$ adiabatic-saturation temperature
For moist air in the normal pressure/temperature range, $T_{wb}\approx T_{as}$, so the
**wet-bulb temperature may be substituted for $T_{as}$ in Eqs. 12.48–12.49** [M §12.6,
p.765]. This is why a sling psychrometer reading is enough to get $\omega$ (and then $\phi$,
the dew point, etc.). Close agreement breaks down well away from normal conditions.

## 4. Chart datum and the constant-$T_{wb}$ ≈ constant-$h$ property
On the psychrometric chart $h_a$ uses the $0\,^\circ$C reference [M Eq. 12.51, p.767]:
$$h_a = \int_{273.15}^{T} c_{pa}\,dT = c_{pa}\,T(^\circ\text{C}),\qquad c_{pa}=1.005\ \tfrac{\text{kJ}}{\text{kg·K}}.$$
Because the makeup-water energy in Eq. 12.50 is small, **lines of constant $T_{wb}$ are
nearly lines of constant mixture enthalpy** $h_a+\omega h_g$ [M §12.7, p.767].

## Bridge — psychrometer reading (M p.767)
A classroom psychrometer reads dry-bulb $68\,^\circ$F, wet-bulb $60\,^\circ$F. The two
temperatures fix the state: from Fig. A-9E, $\omega = 0.0092\;\text{lb/lb}$ and
$\phi = 63\%$. With the wet-bulb temperature in place of $T_{as}$, Eqs. 12.48–12.49
reproduce the same $\omega$ analytically — the calculation module `11.HP` problem 12.77
carries out for $82/68\,^\circ$F. The dew point then follows as $T_{sat}(p_v)$ with
$p_v=\omega p/(0.622+\omega)$.
