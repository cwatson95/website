# 4.3 — Problems

Check with `code/exergy.py`. Citations in `../refs.md`. `T₀,p₀` = dead state; keep
energy units consistent (kJ or Btu).

### P1.  Exergy destroyed = T₀ × entropy produced  *(Moran 8e Eq. 7.7, p.380)*
A metal sphere is quenched in water; the process produces `σ = 0.15959 Btu/°R`. With
`T₀ = 537 °R`, find the exergy destroyed (HW 7.36).
*Answer:* `E_d = T₀σ = 537(0.15959) = 85.7 Btu`. *Check:* `exergy_destruction(537, 0.15959)` ≈ 85.7.

### P2.  Exergy of heat depends on its temperature  *(Moran 8e Eq. 7.5, p.380)*
Equal heat `Q = 0.2 kW/m²` enters a wall at 575 K and leaves at 310 K, with `T₀ = 293 K`.
How much exergy is destroyed in the wall (Ex 7.3)?
*Answer:* `E_q,in = (1−293/575)(0.2) = 0.098`, `E_q,out = (1−293/310)(0.2) = 0.011`, so
`E_d/A = 0.098 − 0.011 = 0.087 kW/m²`. Heat is "worth more" at higher T; crossing a
finite ΔT destroys exergy. *Check:* `exergy_transfer_heat(0.2,293,575) −
exergy_transfer_heat(0.2,293,310)` ≈ 0.087.

### P3.  Reversible process destroys no exergy (Ex 7.2)  *(Moran 8e §7.4, p.381)*
Water evaporates reversibly at 150 °C (from Ex 6.1: `Q/m=2114.1`, `W/m=186.38 kJ/kg`,
`v_g−v_f=0.3917`); `T₀=293.15 K`, `p₀=100 kPa`. Find `E_q/m`, `E_w/m`, `E_d/m`, and `Δe`.
*Answer:* `E_q/m = (1−293.15/423.15)(2114.1) = 649.49`; `E_w/m = 186.38 − 100(0.3917) =
147.21`; `E_d = 0` (reversible); `Δe = 649.49 − 147.21 = 502.4 kJ/kg`. *Check:*
`exergy_transfer_heat(2114.1,293.15,423.15)` ≈ 649.49; `exergy_transfer_work(186.38,100,0.39171)` ≈ 147.21.

### P4.  Exergy of a warmed solid (HW 7.21)  *(Moran 8e §7.3, p.417)*
A concrete slab (`m=16560 kg`, `c=0.88 kJ/kg·K`) is warmed from 298 K to 301 K;
`T₀=298 K`. Find the exergy increase and the height to which it could lift a 1000-kg mass.
*Answer:* `ΔE = mc[(T₂−T₁) − T₀·ln(T₂/T₁)] = 14572.8(3 − 298·ln(301/298)) = 218.6 kJ`;
`z = ΔE/(m_load·g) = 218600/(1000·9.81) = 22.3 m`. (Only a little of the 43,700 kJ of
energy added is *exergy*, since the warming is barely above `T₀`.) *Check:*
`exergy_change_incompressible(16560, 0.88, 298, 301, 298)` ≈ 218.6.
