# 6.EP — Topic 6 Example Problems (Moran Ch.4 & Ch.6)

Moran 8e's worked **Examples** for the Topic-6 idealizations — steady-state control volumes
(Ch.4) and entropy/reversibility/isentropic processes (Ch.6) — reproduced from their
*given* data and verified in `code/examples.py` (`test_examples.py`). Each regenerates the
book's published answer. Citations in `refs.md`.

## Control volumes at steady state (Ch.4)
| Moran Ex. | concept | given → find | book answer | function |
|-----------|---------|--------------|-------------|----------|
| **4.1** Feedwater heater | mass balance (`6.5`) | (AV)₃=0.06 m³/s, v₃=1.108e-3, ṁ₁=40 kg/s | ṁ₃=54.15, ṁ₂=14.15 kg/s, V₂=5.7 m/s | `ex_4_1` |
| **4.2** Barrel filling | transient→steady (`6.5`) | ṁᵢ=30, ṁₑ=9L lb/s | L=3.33 ft | `ex_4_2` |
| **4.4** Steam turbine | energy balance (`6.4`) | ṁ=4600 kg/h, Ẇ=1000 kW, Δh, ΔKE | Q̇cv=−62.3 kW | `ex_4_4` |

## Entropy, reversibility, isentropic (Ch.6)
| Moran Ex. | concept | given → find | book answer | function |
|-----------|---------|--------------|-------------|----------|
| **6.1** Int. rev. water | `Q=∫T dS` (`6.1`) | sat-liq→sat-vap, 150 °C, int. rev. | W/m=186.38, Q/m=2114.1 kJ/kg | `ex_6_1` |
| **6.2** Irrev. water | entropy bal. (`6.2`) | same states, adiabatic paddle stir | W/m=−1927.82, σ/m=4.9961 | `ex_6_2` |
| **6.3** Min. comp. work | σ≥0 (`6.2`/`6.3`) | R-134a adiabatic, u₁=94.68, u₂s=107.46 | (−W/m)_min=12.78 Btu/lb | `ex_6_3` |
| **6.4** Gearbox σ̇ | rate bal. (`6.2`) | Q̇=−1.2 kW, T_b=300, T_f=293 K | σ̇=4.0e-3, 4.1e-3 kW/K | `ex_6_4` |
| **6.5** Quench bar | increase principle (`6.2`) | 0.8 lb @1900°R in 20 lb water @530°R | T_f=535 °R, σ=0.0864 Btu/°R | `ex_6_5` |
| **6.9** Isentropic air | `T₂/T₁=(p₂/p₁)^((k−1)/k)` (`6.3`) | 1 atm/540°R → 1160°R | p₂=15.28 atm (p_r), 15.26 (k=1.39) | `ex_6_9` |
| **6.10** Air leak from tank | isentropic (`6.3`) | 5 kg, 5 bar/500 K → 1 bar | m₂=1.58 kg, T₂=317 K | `ex_6_10` |
| **6.11** Turbine work from η | `η_t` (`6.3`) | 5 bar/320 °C → 1 bar, η_t=0.75 | W/m=271.95 kJ/kg | `ex_6_11` |
| **6.12** Evaluating η_t | `η_t` (`6.3`) | air 3 bar/390 K → 1 bar, W/m=74 | η_t=0.70 | `ex_6_12` |

**Key lessons:** in an *internally reversible* process σ = 0 and `Q = ∫T dS` (the T–s area);
in any *irreversible* process σ > 0, and σ is **not a property** (Ex 6.1 vs 6.2, same end
states). An *adiabatic + internally reversible* process is **isentropic** — the basis of
`p_r`/constant-`k` relations (Ex 6.9, 6.10) and of isentropic efficiency (Ex 6.11, 6.12).
Carnot/entropy temperatures must be **absolute**.

## Run
```bash
cd code
python3 examples.py          # all 12 examples vs the book answers
python3 test_examples.py     # -> "All 22 tests passed."
```
