# 09.2 — Problems

Check with `code/otto_cycle.py`. Citations in `../refs.md`. Cold air-standard `k=1.4`.

### P1.  Efficiency from compression ratio  *(Moran 8e Eq. 9.8, p.515)*
Find the cold air-standard Otto efficiency at compression ratios `r = 6, 8, 10`.
*Answer:* `η = 1 − 1/r^0.4` = **0.512, 0.565, 0.602**. Efficiency rises with `r`.
*Check:* `otto_efficiency(6)` ≈ 0.512, `otto_efficiency(8)` ≈ 0.565, `otto_efficiency(10)` ≈ 0.602.

### P2.  State temperatures, Example 9.1  *(Moran 8e Ex 9.1, Eqs. 9.6–9.7, p.516)*
An Otto cycle has `r = 8`, `T₁ = 540 °R`, and a maximum temperature `T₃ = 3600 °R`.
On a cold air-standard basis find `T₂` and `T₄`.
*Answer:* `T₂ = 540·8^0.4 = 1241 °R`, `T₄ = 3600/8^0.4 = 1567 °R`. *Check:*
`temp_after_isentropic_compression(540, 8)` ≈ 1241; `temp_after_isentropic_expansion(3600, 8)` ≈ 1567.

### P3.  Air-table vs cold air-standard  *(Moran 8e Ex 9.1(b), Eq. 9.3, p.517)*
Using air-table internal energies `u₁ = 92.04`, `u₂ = 211.3`, `u₃ = 721.44`,
`u₄ = 342.2 Btu/lb`, find `η`. Compare with the cold-air value from P1.
*Answer:* `η = 1 − (342.2−92.04)/(721.44−211.3) = 0.51`, below the cold-air 0.565 —
constant `c_v` overpredicts. *Check:* `otto_efficiency_air_table(92.04, 211.3, 721.44, 342.2)` ≈ 0.51.

### P4.  Carnot ceiling check  *(cross-ref `09.1`, Eq. 5.9)*
The Otto cycle of P2/P3 spans roughly `T₃ = 3600 °R` (2000 K) to `T₁ = 540 °R` (300 K).
Is `η = 0.565` below the Carnot ceiling?
*Answer:* Carnot `η_max = 1 − 540/3600 = 0.85`; `0.565 < 0.85`, so yes — the real cycle
falls well short of reversible. *Check (in `09.1`):* `carnot_efficiency(540, 3600)` = 0.85.

### P5.  Net work and mep  *(Moran 8e Ex 9.1(c), p.515)*
For `r = 8`, `T₁ = 300 K`, `T₃ = 1500 K`, `c_v = 0.718 kJ/kg·K`, find the net work per
unit mass (cold air-standard).
*Answer:* `T₂ = 300·8^0.4 = 689.2 K`; `q₂₃ = 0.718(1500−689.2) = 582.2 kJ/kg`;
`w = η·q₂₃ = 0.5647·582.2 = 328.8 kJ/kg`. *Check:* `net_work_cold(8, 300, 1500)` ≈ 328.8.
