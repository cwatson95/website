Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`)

# 11.1 — Dry-Bulb Temperature & the Moist-Air Model (notes)

## 1. What the dry-bulb temperature is
The **dry-bulb temperature** $T$ is simply the temperature an ordinary thermometer
reads when placed in the air [M §12.6, p.764]. It is one of the two readings of a
**psychrometer** (the other is the wet-bulb temperature, module `11.2`) and it is the
**abscissa of the psychrometric chart** [M §12.7, p.766]. By itself it says nothing
about moisture; to fix the moist-air *state* we pair it with a second property
($\phi$, $\omega$, or the dew point).

## 2. The moist-air model: a binary ideal-gas mixture
Moist air is dry air (a) + water vapor (v) treated as **independent ideal gases**
obeying the Dalton model [M §12.5.1, p.754], so the mixture pressure splits into
partial pressures
$$p = p_a + p_v .$$
A typical state of the vapor (fixed by $p_v$ and $T$) is *superheated*; when
$p_v = p_g(T)$ — the saturation pressure at the mixture temperature — the air is
**saturated** [M Fig. 12.4, p.754].

## 3. Composition: humidity ratio and relative humidity
The **humidity ratio** (specific humidity) is the mass of vapor per mass of dry air
[M §12.5.2, p.754]:
$$\omega = \frac{m_v}{m_a}\quad(12.42).$$
Eliminating masses with the ideal-gas law and $M_v/M_a \approx 0.622$, and using
$p_a = p - p_v$, gives the working form [M Eq. 12.43, p.755]:
$$\boxed{\;\omega = 0.622\,\frac{p_v}{p - p_v}\;}\quad(12.43).$$
The **relative humidity** compares the vapor mole fraction to its saturated value at
the same $T,p$; since $p_v = y_v p$ and $p_g = y_{v,\text{sat}}\,p$ [M Eq. 12.44, p.755]:
$$\phi = \left.\frac{p_v}{p_g(T)}\right|_{T,p}\quad(12.44),$$
with $p_g(T)$ from the steam table (link to module `4.4` / Table A-2). Inverting (12.43),
$p_v = \omega p/(0.622+\omega)$, lets you move between $\omega$, $\phi$, and $p_v$.

## 4. Energy: mixture enthalpy per unit dry air
Enthalpy is additive over components [M Eq. 12.45, p.755], so
$$H = m_a h_a + m_v h_v,\qquad
\frac{H}{m_a} = h_a + \omega\,h_v \quad(12.46),$$
the **mixture enthalpy per unit mass of dry air** — the natural per-unit basis because
$m_a$ is conserved through conditioning processes. At low vapor pressure the vapor
enthalpy is the saturated value at the dry-bulb temperature [M Eq. 12.47, p.755]:
$$h_v \approx h_g(T)\quad(12.47).$$
On the psychrometric chart the dry-air enthalpy uses the $0\,^\circ$C datum
$h_a = c_{pa}\,T(^\circ\text{C})$ (Eq. 12.51), $c_{pa}=1.005\;$kJ/kg·K (see `11.2`).

## 5. The dew point — cooling at constant pressure
Cool moist air at constant $p$ and the composition (hence $p_v$) holds until the vapor
**saturates** at the **dew point**, $T_{dp} = T_{sat}(p_v)$ [M §12.5.4, p.757]. Cool
below $T_{dp}$ and vapor condenses; the remaining vapor stays saturated at the new $T$,
so $\omega$ *drops*. On the chart the dew point is reached by following a horizontal
(constant-$\omega$, constant-$p_v$) line left to the $\phi=100\%$ curve.

## Bridge — Example 12.7 (M p.758)
A 1-lb sample at $70\,^\circ$F, $14.7\;\text{lbf/in.}^2$, $\phi=70\%$:
$p_{v1}=\phi\,p_g(70^\circ\text{F})=0.70(0.3632)=0.2542\;\text{lbf/in.}^2$, then
$\omega_1=0.622(0.2542)/(14.7-0.2542)=0.011$, dew point $T_{sat}(0.2542)=60\,^\circ$F.
The dry-bulb temperature supplied the saturation-pressure lookup $p_g(70^\circ\text{F})$
and is the abscissa of the chart point. Pairing it with the **wet-bulb** temperature
(module `11.2`) fixes $\omega$ when $\phi$ is not given.
