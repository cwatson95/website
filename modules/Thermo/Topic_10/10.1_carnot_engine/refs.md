# 10.1 — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Topic (code symbol) | Section № & title | Eq. № | Printed p. | PDF p. |
|---|---|---|---|---|
| Carnot cycle: 4 reversible processes (`cycle_status`) | §5.10 *Carnot Cycle* | — | 270 | 288 |
| Carnot power cycle 1–2–3–4 (p–v / T–s) | §5.10.1 *Carnot Power Cycle* | — | 270–272 | 288–290 |
| Carnot refrig./heat-pump cycle (reversed) | §5.10.2 *Carnot Refrigeration and Heat Pump Cycles* | — | 272 | 290 |
| Carnot cycle summary (3 invariants) | §5.10.3 *Carnot Cycle Summary* | — | 272–273 | 290–291 |
| Carnot efficiency `η_max=1−T_C/T_H` (`carnot_efficiency`) | §5.9.1 *Power Cycles* | **5.9** | 265 | 283 |
| thermal efficiency `η=W_cycle/Q_H` (`thermal_efficiency`) | §2.6 *Cycles* | **2.42** | 74 | 92 |
| efficiency from heat `η=1−Q_C/Q_H` (`efficiency_from_heats`) | §5.4 | **5.4** | 256 | 274 |
| reversible heat ratio `(Q_C/Q_H)_rev=T_C/T_H` (`kelvin_heat_ratio`, `carnot_heat_rejected`) | §5.7 *Defining the Kelvin Temperature Scale* | **5.7** | 262 | 280 |
| corollary classification (`cycle_status`) | §5.9.1 + Example **5.1** | — | 265–266 | 283–284 |
| max COP refrig. `β_max=T_C/(T_H−T_C)` (`carnot_cop_refrigerator`) | §5.9.2 *Refrigeration and Heat Pump Cycles* | **5.10** | 267 | 285 |
| max COP heat pump `γ_max=T_H/(T_H−T_C)` (`carnot_cop_heat_pump`) | §5.9.2 | **5.11** | 267 | 285 |
| Example 5.1 *Evaluating Power Cycle Performance* | §5.9.1 | (5.4, 5.9) | 266–267 | 284–285 |

The Carnot efficiency / COP *expressions* live in §5.9 (Maximum Performance Measures);
§5.10 then realizes them as an actual reversible **cycle** (the engine). The Carnot
**corollaries** that make Eq. 5.9 a ceiling are derived in module `3.3`.

## See also
`3.3` (second law, Carnot corollaries), `10.2` (Stirling — same ceiling via
regeneration), `10.EP` (Examples 5.1–5.3), `10.EQ`, `10.HP`. Topic 9 (`09.1` …)
applies the ceiling to Otto/Diesel/Brayton/Rankine cycles; Topic 8 to refrigerators
& heat pumps.
