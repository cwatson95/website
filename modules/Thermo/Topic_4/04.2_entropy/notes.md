# 4.2 — Entropy (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. Why entropy is a property
The Clausius inequality `∮(δQ/T) ≤ 0` (with equality for internally reversible
cycles) shows `∫(δQ/T)_int,rev` is path-independent, so it defines a property
[M §6.1, p.292]:
$$dS=\left(\frac{\delta Q}{T}\right)_{int,rev}\quad(6.2).$$
In the two-phase region `s = sf + x·sfg` (Eq. 6.4) — the same `x`-weighting as `v,u,h`
(module `4.4`).

## 2. Evaluating entropy change
The **T dS equations** connect `Δs` to ordinary property data [M §6.3, p.297]:
$$T\,ds=du+p\,dv\quad(6.10a),\qquad T\,ds=dh-v\,dp\quad(6.10b).$$
Integrating for common models:
- **Incompressible:** `Δs = c·ln(T₂/T₁)` (Eq. 6.13).
- **Ideal gas, gas tables:** `Δs = s°(T₂)−s°(T₁) − R·ln(p₂/p₁)` (Eq. 6.20a).
- **Ideal gas, constant `cp`:** `Δs = cp·ln(T₂/T₁) − R·ln(p₂/p₁)` (Eq. 6.22);
  **constant `cv`:** `Δs = cv·ln(T₂/T₁) + R·ln(v₂/v₁)` (Eq. 6.21).

On a `T-S` diagram, area under an internally reversible path is heat:
`Q = ∫T dS` (Eq. 6.23) — module `5.5`.

## 3. The entropy balance and entropy production
For a closed system [M §6.7, p.305]:
$$S_2-S_1=\int_1^2\left(\frac{\delta Q}{T}\right)_b+\sigma,\qquad \sigma\ge 0\quad(6.24).$$
`σ` is the entropy **produced** inside the system by irreversibilities. `σ = 0` only
for an internally reversible process; `σ < 0` is impossible (the 2nd law). The
control-volume rate form adds the flow terms `Σṁᵢsᵢ − Σṁₑsₑ` (Eq. 6.34/6.36, Topic 6).

**`σ` is not a property.** *Check (M Ex 6.1 vs 6.2):* water from saturated liquid to
saturated vapor at 150 °C (`Δs = 6.8379−1.8418 = 4.9961 kJ/kg·K`, the same for both):
- **Ex 6.1**, internally reversible at constant `T,p`: `Q/m = T·Δs = 423.15(4.9961) =
  2114.1 kJ/kg`, `W/m = p(v_g−v_f) = +186.38 kJ/kg`, `σ = 0`.
- **Ex 6.2**, adiabatic with a paddle wheel (same end states): `Q = 0`, so the balance
  gives `σ/m = Δs = 4.9961 kJ/kg·K > 0`, and `W/m = −(u₂−u₁) = −1927.82 kJ/kg` (work in).

Same `Δs`, different `σ` — entropy is a property, entropy production is not.

## Bridge
`σ` reappears as exergy destruction `E_d = T₀σ` (module `4.3`); `Δs = 0` (isentropic)
is the ideal for turbines/pumps and defines isentropic efficiency (Topics 6, 7); and
`s` columns drive the `T-S` cycle analyses of Topic 9.
