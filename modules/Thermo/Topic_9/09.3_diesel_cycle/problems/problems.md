# 09.3 — Problems

Check with `code/diesel_cycle.py`. Citations in `../refs.md`. Cold air-standard `k=1.4`.

### P1.  Air-table efficiency, Example 9.2  *(Moran 8e Ex 9.2, Eq. 9.11, p.521)*
A Diesel cycle has `r = 18`, `rc = 2`, `T₁ = 300 K`. Air-table properties:
`u₁ = 214.07`, `h₂ = 930.98`, `h₃ = 1999.1`, `u₄ = 664.3 kJ/kg`. Find `η`.
*Answer:* `η = 1 − (664.3−214.07)/(1999.1−930.98) = 0.578` (57.8%). *Check:*
`diesel_efficiency_air_table(214.07, 664.3, 930.98, 1999.1)` ≈ 0.578.

### P2.  Cold air-standard closed form  *(Moran 8e Eq. 9.13, p.519)*
For the same `r = 18`, `rc = 2`, compute `η` from Eq. 9.13 and compare with P1.
*Answer:* `η = 1 − (1/18^0.4)·(2^1.4−1)/(1.4·1) = 0.632`, above the air-table 0.578 —
constant `c_p` overpredicts. *Check:* `diesel_efficiency(18, 2)` ≈ 0.632.

### P3.  Diesel vs Otto at equal r  *(Moran 8e §9.3, p.520)*
Compare the cold air-standard Diesel (`r = 18`, `rc = 2`) with the Otto cycle at the
same `r = 18`.
*Answer:* Otto `η = 1 − 1/18^0.4 = 0.685`; Diesel `η = 0.632 < 0.685`. At equal `r` the
constant-pressure burn costs efficiency. *Check:* `diesel_efficiency(18, 2)` ≈ 0.632 <
`1 − 1/18**0.4` ≈ 0.685.

### P4.  Cutoff-ratio limit  *(Moran 8e Eq. 9.13 → 9.8, p.519)*
Show that as the cutoff ratio `rc → 1` the Diesel efficiency reduces to the Otto value.
*Answer:* As `rc → 1` the bracket `(rc^k−1)/(k(rc−1)) → 1`, so
`η → 1 − 1/r^(k−1)` (Eq. 9.8). At `r = 18`: `diesel(18, 1+ε) = 0.685 = otto(18)`.
*Check:* `diesel_efficiency(18, 1.000000001)` ≈ `1 − 1/18**0.4` ≈ 0.685.

### P5.  State temperatures  *(Moran 8e Ex 9.2, p.520)*
For `r = 18`, `rc = 2`, `T₁ = 300 K` (cold air-standard), find `T₂`, `T₃`, `T₄`.
*Answer:* `T₂ = 300·18^0.4 = 953.3 K`; `T₃ = rc·T₂ = 1906.6 K`;
`T₄ = T₃·(rc/r)^0.4 = 1906.6·(2/18)^0.4 = 760.9 K`. *Check:*
`temp_after_isentropic_compression(300,18)` ≈ 953.3; `temp_after_constant_pressure_heat(953.3,2)` ≈ 1906.6;
`temp_after_isentropic_expansion(1906.6,18,2)` ≈ 760.9. (Cold-air values differ from the
book's air-table 898.3/1796.6/887.7 K.)
