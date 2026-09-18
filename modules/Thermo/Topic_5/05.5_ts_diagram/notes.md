# 5.5 — The T–s Diagram (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. Diagrams with entropy as a coordinate
Two charts carry entropy on an axis [M §6.2.5, p.295]:
- **Temperature–entropy (T–s)** diagram (Fig. 6.2): the dome with saturated-liquid and
  saturated-vapor borders; constant-`p` and constant-`v` lines in the superheat region
  (constant-`v` steeper); lines of constant quality `x` inside the dome. Steam tables
  supply the `s` data (`5.1`); inside the dome `s = sf + x(sg − sf)` [M Eq. 6.4].
- **Enthalpy–entropy (h–s)**, the **Mollier diagram** (Fig. 6.3): constant-`T` and
  constant-`p` lines; constant-`x` lines in the dome. Built for superheated vapor and
  two-phase states (liquid data are seldom shown). *Check (M p.296):* water at `240 °C`,
  `0.10 MPa` expanded isentropically (`s₂ = s₁`) to `0.01 MPa` reaches `x₂ ≈ 0.98`,
  `h₂ ≈ 2537 kJ/kg` (drop a vertical line into the dome).

## 2. Heat is the area under a reversible T–s path
For an internally reversible process, entropy is defined so that [M Eq. 6.2b, §6.6, p.302]
$$dS=\Big(\frac{\delta Q}{T}\Big)_{\text{int,rev}}\ \Rightarrow\ (\delta Q)_{\text{int,rev}}=T\,dS,$$
and integrating from state 1 to 2 [M Eq. 6.23, §6.6.1, p.302]:
$$Q_{\text{int,rev}}=\int_1^2 T\,dS .$$
This is the **entire area under the path** on a T–s diagram. **`T` must be absolute**
(K or °R). As with `∫p dV`, the area is path-dependent and is **not valid for irreversible
processes**. Heat *in* raises entropy (`dS>0`); an adiabatic reversible process is
**isentropic** (`dS = 0`).

*Check (M Ex 6.1):* water vaporized reversibly at constant `T = 150 °C = 423.15 K`:
`Q/m = T(s₂ − s₁) = 423.15(6.8379 − 1.8418) = 2114.1 kJ/kg` (a rectangle of height `T`,
width `sg − sf`).

## 3. The Carnot cycle on T–s
A Carnot power cycle is two isotherms (`T_H`, `T_C`) joined by two isentropes — a
**rectangle** [M §6.6.2, p.303]. Heat in `Q_in = T_H ΔS`, heat out `Q_out = T_C ΔS`. The
enclosed area is the **net heat = net work**:
$$W_{\text{net}}=(T_H-T_C)\,\Delta S,\qquad
\eta=\frac{W_{\text{net}}}{Q_{\text{in}}}=\frac{(T_H-T_C)\Delta S}{T_H\Delta S}=1-\frac{T_C}{T_H},$$
recovering the Carnot efficiency (Eq. 5.9) directly from the T–s areas.

## Bridge
The p–v diagram (`5.4`) and the T–s diagram are the two work/heat "area" pictures: `∫p dV`
is reversible work, `∫T dS` is reversible heat. Together they underlie every cycle diagram
(Rankine, Brayton, refrigeration) built in later topics. For liquid states the entropy
obeys the same saturated-state approximation as `v, u, h`: `s(T,p) ≈ sf(T)` [M Eq. 6.5].
