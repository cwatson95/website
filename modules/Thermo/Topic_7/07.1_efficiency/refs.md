# 07.1 — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Topic (code symbol) | Section № & title | Eq. № | Printed p. | PDF p. |
|---|---|---|---|---|
| cycle energy balance `W=Q_in−Q_out` | §2.6.1–2.6.2 *Cycle Energy Balance / Power Cycles* | **2.41** | 73 | 91 |
| thermal efficiency `η=W/Q_in` (`thermal_efficiency`) | §2.6.2 *Power Cycles* | **2.42** | 74 | 92 |
| thermal efficiency `η=1−Q_out/Q_in` (`thermal_efficiency_from_heat`) | §2.6.2 | **2.43** | 74 | 92 |
| refrig./heat-pump balance `W=Q_out−Q_in` | §2.6.3 *Refrigeration and Heat Pump Cycles* | **2.44** | 74 | 92 |
| COP refrig. `β=Q_C/W` (`cop_refrigerator`) | §2.6.3 *Refrigeration Cycles* | **2.45** | 75 | 93 |
| COP refrig. `β=Q_C/(Q_H−Q_C)` (`cop_refrigerator_from_heat`) | §2.6.3 | **2.46** | 75 | 93 |
| COP heat pump `γ=Q_H/W` (`cop_heat_pump`) | §2.6.3 *Heat Pump Cycles* | **2.47** | 75 | 93 |
| COP heat pump `γ=Q_H/(Q_H−Q_C)` (`cop_heat_pump_from_heat`) | §2.6.3 | **2.48** | 75 | 93 |
| Carnot efficiency `η_max=1−T_C/T_H` (`carnot_efficiency`) | §5.9.1 *Power Cycles* | **5.9** | 265 | 283 |
| max COP refrig. `β_max=T_C/(T_H−T_C)` (`carnot_cop_refrigerator`) | §5.9.2 *Refrigeration and Heat Pump Cycles* | **5.10** | 267 | 285 |
| max COP heat pump `γ_max=T_H/(T_H−T_C)` (`carnot_cop_heat_pump`) | §5.9.2 | **5.11** | 267 | 285 |
| isentropic turbine `η_t=(h1−h2)/(h1−h2s)` (`isentropic_turbine_efficiency`) | §6.12.1 *Isentropic Turbine Efficiency* | **6.46** | 333 | 351 |
| isentropic nozzle `η_n=(V₂²/2)/(V₂²/2)_s` (`isentropic_nozzle_efficiency`) | §6.12.2 *Isentropic Nozzle Efficiency* | **6.47** | 335 | 353 |
| isentropic compressor `η_c=(h2s−h1)/(h2−h1)` (`isentropic_compressor_efficiency`) | §6.12.3 *Isentropic Compressor and Pump Efficiencies* | **6.48** | 338 | 356 |

**Note on equation numbers.** In Moran **8e** the device efficiencies are numbered
turbine **6.46**, nozzle **6.47**, compressor/pump **6.48** (the pump uses the
compressor form, Eq. 6.48, and is not separately numbered). The COP definitions are
β **2.45** / **2.46** and γ **2.47** / **2.48**; Eq. 2.44 is the refrigeration/heat-pump
*energy balance*, not a COP. All read directly from the page text.

## See also
`2.x` (cycle energy balance), `3.3` (second law & Carnot corollaries — same
`carnot_*` functions), Topic 6 (isentropic / reversible-adiabatic ideal), `4.3`
(exergy, the work lost to irreversibility), `7.EQ`/`7.EP`/`7.HP`,
Topic 8 (devices), Topic 9 (power & refrigeration cycles).
