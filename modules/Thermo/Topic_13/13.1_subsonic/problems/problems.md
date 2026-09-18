# 13.1 — Problems

Check with `code/subsonic.py`. Citations in `../refs.md`. `c,V` [m/s], `T` [K],
`R` [J/kg·K], `k` dimensionless.

### P1.  Speed of sound in air (Moran in-text example)  *(Moran 8e Eq. 9.37, p.570)*
Find the speed of sound in air (`k=1.4`, `R=287 J/kg·K`) at 300 K and at 650 K
(`k=1.37`).
*Answer:* `c(300) = √(1.4·287·300) = 347 m/s`; `c(650) = √(1.37·287·650) = 506 m/s`
(sound speed rises with temperature). *Check:* `speed_of_sound_ideal_gas(1.4, 287, 300)`
≈ 347; `speed_of_sound_ideal_gas(1.37, 287, 650)` ≈ 506.

### P2.  Mach number and regime  *(Moran 8e Eq. 9.38, p.570)*
A stream of air at 300 K moves at 200 m/s. Find `M` and state the regime.
*Answer:* `c = 347 m/s`, `M = 200/347 = 0.576 < 1` ⇒ **subsonic**. *Check:*
`mach_number(200, speed_of_sound_ideal_gas(1.4, 287, 300))` ≈ 0.576.

### P3.  Stagnation properties (Ex 9.14b exit)  *(Moran 8e Eqs. 9.50–9.51, p.578)*
A subsonic air stream has `M = 0.6` (`k=1.4`) with stagnation `To = 360 K`,
`po = 1.0 MPa`. Find the static `T` and `p`.
*Answer:* `To/T = 1 + 0.2·0.36 = 1.072` ⇒ `T = 336 K`; `po/p = 1.072^3.5 = 1.276` ⇒
`p = 784 kPa`. *Check:* `static_temperature_from_stagnation(360, 0.6, 1.4)` ≈ 336;
`static_pressure_from_stagnation(1.0e6, 0.6, 1.4)` ≈ 7.84e5.

### P4.  Why a subsonic nozzle converges (Eq. 9.45)  *(Moran 8e Sec. 9.13.1, p.573)*
Using the area–velocity relation, explain the duct shape needed to (a) accelerate and
(b) decelerate a subsonic gas (`M=0.6`).
*Answer:* `dA/A = −(dV/V)(1−M²)` with `1−M² = 0.64 > 0`. (a) accelerate, `dV>0` ⇒
`dA<0` **converging** (nozzle); (b) decelerate, `dV<0` ⇒ `dA>0` **diverging**
(diffuser). *Check:* `duct_shape(+0.01, 0.6)` = `"converging"`;
`duct_shape(-0.01, 0.6)` = `"diverging"`.
