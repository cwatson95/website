# 6.1 — Reversible & Internally Reversible Processes (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. Reversible vs. irreversible
A process is **reversible** if, after it occurs, *both* the system **and all parts of its
surroundings** can be exactly restored to their initial states [M §5.3.3, p.252]. A
process is **irreversible** if they cannot. All actual processes are irreversible; a
reversible process is **purely hypothetical** — a limiting ideal approached as
irreversibilities (friction, finite-ΔT heat transfer, unrestrained expansion, mixing, …)
are reduced further and further. Examples that nearly reach it: a frictionless pendulum
in vacuum, a gas slowly compressed/expanded in a frictionless piston–cylinder.

## 2. Internally reversible
A process is **internally reversible** if **no irreversibilities occur within the system**;
irreversibilities may still reside in the surroundings [M §5.3.4, p.253]. At every
intermediate state all intensive properties (`T`, `p`, `v`, …) are **uniform throughout
each phase** — so it is a **quasi-equilibrium** (series-of-equilibrium-states) process.
*Example:* water condensing at 100 °C inside a tube whose outer wall sees 20 °C ambient —
the water is internally reversible, but the tube-wall ΔT is an **external** irreversibility.

## 3. Heat transfer = area under the T–s curve
For a closed system in an internally reversible process, entropy and heat are linked
[M §6.6, p.302]:
$$dS=\left(\frac{\delta Q}{T}\right)_{\!\text{int rev}}\;(6.2b),\qquad
Q_{\text{int rev}}=\int_1^2 T\,dS\;(6.23).$$
Thus **heat transfer is the area under the process path on a temperature–entropy diagram**
(T in **kelvin/rankine**, whole area under the curve). Heat *in* ⇒ entropy *up*; heat *out*
⇒ entropy *down*; an **adiabatic** internally reversible process has `dS = 0` — it is
**isentropic** (constant entropy). For any internally reversible process the entropy
production is **σ = 0**.

For an **isothermal** internally reversible process, `Q = T(S₂−S₁)`; the Carnot-cycle
T–s rectangle then gives `η = 1 − T_C/T_H` directly [M §6.6.2, p.303], agreeing with Eq. 5.9.

**Area-under-T–s = heat (int. rev. only).** *Check (M Ex 6.1, water at 150 °C = 423.15 K,
sat-liquid → sat-vapor, internally reversible, constant p,T):* from Table A-2, `p = 4.758
bar`, `v₁ = 1.0905×10⁻³`, `v₂ = 0.3928 m³/kg`, `s₁ = 1.8418`, `s₂ = 6.8379 kJ/kg·K`. The
constant-pressure work is `W/m = p(v₂−v₁) = 475.8(0.3917) = 186.38 kJ/kg`; the heat is the
T–s area `Q/m = T(s₂−s₁) = 423.15(4.9961) = 2114.1 kJ/kg` (= `h₂−h₁` by the energy balance).

## Bridge
σ = 0 here is the **reversible limit** of the entropy balance `ΔS = ∫δQ/T + σ` whose
σ > 0 (irreversible) side is module `6.2`. Adiabatic internally reversible ⇒ isentropic
is the workhorse of module `6.3`. The area-under-T–s idea drives every cycle in Topics 8–9.
