# 13.2 — Supersonic Compressible Flow (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. Area change reverses past M = 1
The area–velocity relation `dA/A = −(dV/V)(1−M²)` (Eq. 9.45) changes character at the
sonic point [M §9.13.1, p.573]:
- **Supersonic nozzle (case 2):** `dV>0`, `M>1` ⇒ `dA>0` — duct **diverges**.
- **Supersonic diffuser (case 3):** `dV<0`, `M>1` ⇒ `dA<0` — duct **converges**.

Since `M=1` can occur only where the area is a minimum, accelerating a gas from subsonic
to supersonic requires a **converging–diverging** passage with a **throat** at `M=1`.

## 2. The isentropic area–Mach relation
For an ideal gas with constant `k`, equating mass flow at a section to that at the sonic
throat (`A*`) gives [M §9.14.1, p.578]:
$$\frac{A}{A^*}=\frac{1}{M}\left[\Big(\frac{2}{k+1}\Big)\Big(1+\frac{k-1}{2}M^2\Big)\right]^{\frac{k+1}{2(k-1)}}\ (9.52).$$
A given `A/A* > 1` has **two** solutions — one subsonic, one supersonic — which is why a
C–D nozzle is needed to cross `M=1`. *Check:* `A/A*(M=0.5)=1.3398`,
`A/A*(M=2.0)=1.6875`, `A/A*(M=2.4)=2.4031` (Table 9.2, `k=1.4`).

## 3. Choking
Lowering the back pressure `pB` on a converging nozzle raises the exit Mach number until
`M=1` at the exit, where `p = p*` (the **critical pressure**) [M §9.13.2, p.574]:
$$\frac{p^*}{p_o}=\Big(\frac{2}{k+1}\Big)^{k/(k-1)}=0.528\ (k=1.4),\qquad
\frac{T^*}{T_o}=\frac{2}{k+1}.$$
For `pB ≤ p*` the nozzle is **choked**: the mass flow is the maximum possible for the
given stagnation state, and further reductions in `pB` do not change it.

## Bridge
*Check (M Ex 9.14a):* `po=1.0 MPa`, `To=360 K`, `k=1.4`. `p*=0.528·1000=528 kPa`, so a
back pressure of 500 kPa (`<p*`) chokes the nozzle: `M2=1`, `T2=T*=300 K`,
`V2=√(kRT2)=347.2 m/s`, `ṁ=p2A2V2/(RT2)=2.13 kg/s`. *Check (M Ex 9.15c):* a C–D nozzle
with `A2/A*=2.4` has a supersonic exit `M2=2.4`, `p2/po=0.0684`, so `p2=6.84 lbf/in²`.
If the back pressure does not match this design value, a **normal shock** can appear in
the diverging section — module `13.3`.
