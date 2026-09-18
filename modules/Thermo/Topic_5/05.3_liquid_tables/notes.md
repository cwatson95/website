# 5.3 — Compressed Liquid Table + Saturated-Liquid Approximation (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. The compressed-liquid table A-5
A compressed (subcooled) liquid is a single phase at `p > psat(T)` (equivalently
`T < Tsat(p)`). It is fixed by two properties, so A-5 is a two-way table of `v, u, h, s`
versus `(p, T)`, in the same format as the superheated table A-4 — except each pressure
block **ends** at the saturated-liquid row [M §3.5.1, p.105]. Compressed-liquid data are
provided **only for water** (Tables A-5), and only on a coarse grid (25–300 bar).
*Check (M p.105):* `v(10.0 MPa, 100 °C) = 1.0385×10⁻³ m³/kg`.

## 2. Why a saturated-liquid approximation works
A-5 shows that `v` and `u` of a liquid change **very little with pressure** at fixed
temperature [M §3.10.1, p.123]. So evaluate them at the saturated-liquid state at the
*same temperature*:
$$v(T,p)\approx v_f(T)\quad(3.11),\qquad u(T,p)\approx u_f(T)\quad(3.12).$$
For enthalpy, substitute these into `h = u + pv`:
$$h(T,p)\approx u_f(T)+p\,v_f(T)=h_f(T)+v_f(T)\,[\,p-p_{\text{sat}}(T)\,]\quad(3.13),$$
using `hf = uf + psat·vf`. When the underlined pressure term is small (low `p`, or `p`
near `psat`),
$$h(T,p)\approx h_f(T)\quad(3.14).$$
Interactive Thermodynamics itself returns liquid `v, u, h` via Eqs. 3.11, 3.12, 3.14 —
it carries **no** compressed-liquid tables.

## 3. How good is it?
*Check (water at 100 bar, 100 °C):* the table gives `v=1.0385×10⁻³`, `u=416.12`,
`h=426.50 kJ/kg`. The saturated-liquid reference at `100 °C` (A-2) is `vf=1.0435×10⁻³`,
`uf=418.94`, `hf=419.04`, `psat=1.014 bar`. So `v_approx` and `u_approx` are within
**~0.5–0.7 %** of the table, while Eq. 3.13 with the pressure correction gives
`h ≈ 419.04 + 1.0435×10⁻³·(10000 − 101.4) = 429.4 kJ/kg`, within `~3 kJ/kg` of the
table value (the bare `hf = 419.0` is ~1.7 % low — the correction matters at high `p`).

## Bridge
The same "evaluate at the saturated state at `T`" idea extends to **entropy**:
`s(T,p) ≈ sf(T)` [M Eq. 6.5, §6.2.3, p.293], used in `5.5`. When greater accuracy than
these approximations is needed, consult fuller property compilations (or the actual A-5
grid). The incompressible-substance model (`u = u(T)`, `v = const`, `cp = cv = c`;
M §3.10.2) builds on the same observations.
