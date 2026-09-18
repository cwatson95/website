# 4.5 — Gibbs phase rule (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. Counting degrees of freedom
At equilibrium, a nonreacting system of `N` components distributed over `P` phases
has a **variance** (degrees of freedom) [M §14.6.2, p.913]:
$$F=2+N-P\quad(14.68),$$
i.e. the classic `F = C − P + 2` with Moran's `N = C`. `F` is the number of intensive
properties you can fix independently before the state is fully determined. It comes
from equating each component's chemical potential across all phases,
`μᵢ¹ = μᵢ² = … = μᵢᴾ` (Eq. 14.67) — a set of constraints that uses up otherwise-free
variables.

## 2. Single component and the phase limit
For one component (`N=1`) [M §14.6.2, p.913]:
$$F=3-P\quad(14.69).$$
- one phase (`P=1`): `F=2` — fix any two of `T, p, v` (the basis of the steam tables);
- two phases (`P=2`): `F=1` — only **one** of `T, p` is free along the saturation line;
- three phases (`P=3`): `F=0` — the **triple point** is fully fixed (water: 0.01 °C,
  0.6113 kPa).

The most phases a substance can show at once is `P = N + 2` (3 for a pure substance).

## 3. Why quality exists (link to 4.4)
The `F=1` result for a pure two-phase mixture is the rigorous reason `T` and `p` are
**not independent** inside the vapor dome: specifying `T` fixes `p` (and vice versa),
so neither pins down the state. A *second* property is required — the **quality** `x`
(module `4.4`). This is the phase rule made concrete.

*Checks (Moran review questions 19–24, p.916):* water vapor (1,1)→`F=2`; water+ammonia
liquid solution (2,1)→`F=3`; water vapor + ice (1,2)→`F=1`; liquid water (1,1)→`F=2`;
ammonia–water liquid + vapor (2,2)→`F=2`; water + lithium-bromide solution (2,1)→`F=3`.

## Bridge
The phase rule rests on the **Gibbs function** `g = h − Ts` (modules `4.1`, `4.2`) and
chemical potential; for **reacting** systems it extends to `F = 2 + N − P − R` (R =
independent reactions), the foundation of chemical-equilibrium analysis (Topic 12).
