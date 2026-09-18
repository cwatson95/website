# 1.4 — Intensive Properties (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 17; `refs.md`).

The complement of module `1.3` [M §1.3.3 *Extensive and Intensive Properties*,
p.9]:

> A property is **intensive** if its value is **not** additive and may vary from
> place to place within the system at any moment. Intensive properties may be
> functions of both position and time.

Temperature `T`, pressure `p`, density `ρ` are intensive, and so is every
**specific** (per-unit-mass) property.

## 1. Specific properties
A specific property is an extensive property **per unit mass**:
$$v=\frac{V}{m}\ (\text{specific volume}),\qquad u=\frac{U}{m},\qquad h=\frac{H}{m},\dots$$
The **density** is the reciprocal of specific volume [M §1.5 *Specific Volume*,
Eq. 1.6, p.13–14]:
$$\rho=\frac{1}{v}=\frac{m}{V}\quad\Longleftrightarrow\quad v\rho=1 .$$
On a molar basis $\bar v = M v$ with `n = m/M` [M Eqs. 1.8–1.9, p.14]. Code:
`specific(X, m)`, `molar(X, n)`, `density(m, V)`, `specific_volume(V, m)`.

Pressure (force per unit area, with the gauge/absolute distinction) is §1.6,
Eq. 1.10/1.14 [M p.14, 17]; temperature and the Kelvin scale are §1.7, with
`T(K) = T(°C) + 273.15` [M Eq. 1.17, p.20].

## 2. Intensive properties don't add — they mass-average
Combine two subsystems and the **extensive** volume adds, `V=V_1+V_2`, but the
**intensive** specific volume of the mixture is the mass-weighted mean:
$$v_\text{mix}=\frac{\sum_i m_i v_i}{\sum_i m_i}=\frac{V_\text{total}}{m_\text{total}} .$$
Code: `mass_average(values, masses)`. *Check (ties to `1.3`):* 3 kg at `v=0.5`
plus 1 kg at `v=2.0` gives `v_mix = (3·0.5 + 1·2.0)/4 = 0.875 m³/kg` — equal to
`V_total/m_total = 3.5/4`, where `3.5` is the **extensive** sum from module `1.3`.

## 3. Why this matters
Property tables (group `5`, and the `steam_tables/` already built) tabulate
**intensive** properties `v, u, h, s` precisely because they fix the state
independent of how much substance is present — two independent intensive
properties pin down the intensive state of a simple compressible system, and
`is_size_independent` checks that scaling the system leaves them unchanged.
