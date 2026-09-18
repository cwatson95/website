# 4.EP — Topic 4 Example Problems (Moran Ch.3/6/7)

Six Moran 8e worked **Examples** spanning Topic 4, reproduced from their *given* data
and verified in `code/examples.py` (`test_examples.py`). Each regenerates the book's
published answer. Citations in `refs.md`.

| Moran Ex. | concept (module) | given → find | book answer | function |
|-----------|------------------|--------------|-------------|----------|
| **3.1** Heating Ammonia at Constant Pressure | enthalpy/work (`4.1`) | 0.1 lb NH₃, sat. vapor @20 psi → 77 °F | V₁=1.35, V₂=1.67 ft³, W=+1.18 Btu | `ex_3_1` |
| **3.2** Heating Water at Constant Volume | quality (`4.4`) | 0.5 m³ rigid, x₁=0.5 @1 bar → 1.5 bar | T:99.63→111.4 °C, m=0.59 kg, mg1=0.295, x₂=0.731, mg2=0.431, p₃=2.11 bar | `ex_3_2` |
| **6.1** Reversible evaporation @150 °C | entropy (`4.2`) | sat. liq → sat. vap, int. reversible | W/m=186.38, Q/m=2114.1 kJ/kg, σ=0 | `ex_6_1` |
| **6.2** Adiabatic paddle, same states | entropy production (`4.2`) | sat. liq → sat. vap, adiabatic | W/m=−1927.82 kJ/kg, σ/m=4.9961 kJ/kg·K | `ex_6_2` |
| **7.1** Exergy of exhaust gas | exergy (`4.3`) | air model, 1140 K, 7 bar; T₀=300 K | e=368.91 kJ/kg | `ex_7_1` |
| **7.2** Exergy of the 6.1 process | exergy balance (`4.3`) | T₀=293.15 K, p₀=100 kPa | Eq/m=649.49, Ew/m=147.21, Ed=0, Δe=502.4 | `ex_7_2` |

**Key thread:** Examples 6.1 → 6.2 → 7.2 follow the *same* water process three ways —
reversible (σ=0), irreversible (σ>0, same Δs), and through the exergy lens
(`E_d = T₀σ`). Same states, different production.

## Run
```bash
cd code
python3 examples.py          # all six examples vs the book answers
python3 test_examples.py     # -> "All 16 tests passed."
```
