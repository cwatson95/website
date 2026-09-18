# 4.3 — Exergy (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. The dead state and the idea of exergy
Energy is conserved but not all of it is *useful*: a system in equilibrium with its
surroundings can do no work. **Exergy** measures the departure from that reference
**dead state** `(T₀, p₀)` — the maximum theoretical work obtainable as the system is
brought to it [M §7.2–7.3, p.371–376]:
$$E=(U-U_0)+p_0(V-V_0)-T_0(S-S_0)+KE+PE\quad(7.1),$$
and per unit mass `e` (Eq. 7.2). Exergy is ≥ 0 and zero only at the dead state. The
`p₀(V−V₀)` term is the work spent pushing aside the environment; the `T₀(S−S₀)` term
is the part of the energy unavailable because of the second law.

## 2. The closed-system exergy balance
Combining the energy and entropy balances [M §7.4, p.379]:
$$E_2-E_1=\underbrace{\int_1^2\!\Big(1-\tfrac{T_0}{T_b}\Big)\delta Q}_{E_q}-\underbrace{\big[W-p_0(V_2-V_1)\big]}_{E_w}-\underbrace{T_0\sigma}_{E_d}\quad(7.4).$$
- `E_q = (1−T₀/T_b)Q` — heat carries exergy weighted by the Carnot factor of its boundary temperature (Eq. 7.5).
- `E_w = W − p₀ΔV` — only the work beyond pushing back the atmosphere counts (Eq. 7.6).
- `E_d = T₀σ ≥ 0` — exergy **destroyed** by irreversibility (Eq. 7.7).

**`E_d = T₀σ`** is the heart of the chapter: the entropy production `σ` of module `4.2`
becomes destroyed work potential, scaled by `T₀`.

## 3. Worked anchors
- **Ex 7.1** (exhaust gas, air model, 1140 K, 7 bar; `T₀=300 K`, `p₀=1.013 bar`):
  `e = (u−u₀) + p₀(v−v₀) − T₀(s−s₀) = 666.28 − 38.75 − 258.62 = 368.91 kJ/kg`.
- **Ex 7.2** *reworks* the reversible water process of Ex 6.1 (`T₀=293.15 K`): `E_q/m =
  (1−293.15/423.15)(2114.1) = 649.49`, `E_w/m = 186.38 − p₀(v_g−v_f) = 147.21`, `E_d = 0`
  (reversible), so `Δe = 649.49 − 147.21 = 502.4 kJ/kg`.
- **Ex 7.3** (oven wall, steady conduction 575 K→310 K, `T₀=293 K`): `Q̇/A = 0.2 kW/m²`,
  `E_q1/A = 0.098`, `E_q2/A = 0.011`, so `E_d/A = 0.087 kW/m²` — exergy destroyed simply
  by heat crossing a finite ΔT (book rounds to 0.09).

## Bridge
Exergy turns the second law into an accounting of *lost work*. It grades real devices
against the reversible ideal (second-law efficiency, Topic 7), localizes losses in
plants (Topic 8), and guides cycle improvements (Topic 9). Its engine is `σ` (`4.2`).
