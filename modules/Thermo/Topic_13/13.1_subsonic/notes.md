# 13.1 — Subsonic Compressible Flow (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. Speed of sound and Mach number
A sound wave is a weak pressure disturbance; its speed depends on `(∂p/∂ρ)_s`
[M §9.12.2, p.569]. For an ideal gas (`pv^k = const` at fixed `s`) this reduces to
$$c=\sqrt{kRT}\quad(9.37),$$
with `R` the *specific* gas constant (`R̄/M`). The **Mach number** compares the local
flow speed to the local sound speed [M §9.12.2, p.570]:
$$M=\frac{V}{c}\quad(9.38).$$
`M<1` subsonic, `M=1` sonic, `M>1` supersonic. *Check:* air at 300 K (`k=1.4`,
`R=287 J/kg·K`) gives `c = √(1.4·287·300) = 347 m/s` — Moran's in-text value (p.570).

## 2. Stagnation state
The **stagnation state** is what the stream would reach if decelerated to rest
isentropically [M §9.12.3, p.571]. An energy balance gives the stagnation enthalpy
$$h_o=h+\frac{V^2}{2}\quad(9.39).$$
For an ideal gas with constant `cp` this becomes the **isentropic flow functions**
[M §9.14.1, p.578]:
$$\frac{T_o}{T}=1+\frac{k-1}{2}M^2\ (9.50),\quad
\frac{p_o}{p}=\Big(1+\frac{k-1}{2}M^2\Big)^{k/(k-1)}\ (9.51).$$
The density ratio follows from `p v^k = const`: `ρo/ρ = (To/T)^{1/(k−1)}`.

## 3. Area change in subsonic flow
Combining mass, energy, and the isentropic property relations gives the
**area–velocity relation** [M §9.13.1, p.573]:
$$\frac{dA}{A}=-\frac{dV}{V}\,(1-M^2)\quad(9.45).$$
For `M<1`, `(1−M²)>0`, so `dA` and `dV` have *opposite* signs:
- **Subsonic nozzle (case 1):** `dV>0`, `M<1` ⇒ `dA<0` — duct **converges**.
- **Subsonic diffuser (case 4):** `dV<0`, `M<1` ⇒ `dA>0` — duct **diverges**.

`M=1` can occur only where the area is a minimum — the **throat** (module `13.2`).

## Bridge
*Check (M Ex 9.14b):* a converging nozzle with `po=1.0 MPa`, `To=360 K` and back
pressure `pB=784 kPa > p*` stays subsonic to its exit. Inverting Eq. 9.51,
`M2 = {2/(k−1)[(po/p2)^{(k−1)/k} − 1]}^{1/2} = 0.6`; then `T2 = To/(1+0.2·0.36) = 336 K`
and `V2 = M2·√(kRT2) = 220.5 m/s`. When `pB` is lowered to `p*` the exit reaches `M=1`
and the nozzle **chokes** — the subject of `13.2`.
