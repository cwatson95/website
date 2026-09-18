# 1.4 — Problems

Check with `code/intensive.py`. Citations in `../refs.md`.

### P1.  Specific volume and density  *(Moran 8e §1.5, Eq. 1.6, p.13)*
A tank holds `m = 3 kg` of gas in `V = 1.5 m³`. Find the specific volume `v` and
density `ρ`, and verify `vρ = 1`.
*Answer:* `v = V/m = 0.5 m³/kg`; `ρ = 1/v = 2.0 kg/m³`; `vρ = 1`.
*Check:* `specific_volume(1.5,3)` = 0.5; `density(3,1.5)` = 2.0; product = 1.0.

### P2.  Size-independence  *(Moran 8e §1.3.3, p.9)*
Double the system (`6 kg`, `3 m³`). Does `v` change?
*Answer:* `v = 3/6 = 0.5 m³/kg` — unchanged; intensive properties don't scale.
*Check:* `is_size_independent(0.5, specific_volume(3,6))` → True.

### P3.  Mixing — intensive properties average  *(Moran 8e §1.3.3, p.9)*
Combine `3 kg` at `v=0.5 m³/kg` with `1 kg` at `v=2.0 m³/kg`. Find `v_mix`.
*Answer:* `v_mix = (3·0.5 + 1·2.0)/4 = 0.875 m³/kg` (= `V_total/m_total = 3.5/4`).
*Check:* `mass_average([0.5,2.0],[3,1])` = 0.875 — note the **extensive** volume
adds to 3.5 m³ (module `1.3`) while the **intensive** `v` mass-averages.
