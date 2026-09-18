# 09.6 — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Topic (code symbol) | Section № & title | Eq. № | Printed p. | PDF p. |
|---|---|---|---|---|
| Rankine cycle = the vapor power cycle (Table 8.2 plants) | Ch. 8 intro / §8.2 *The Rankine Cycle* | — | 439, 445 | 457, 463 |
| turbine work `Ẇ_t/ṁ = h₁−h₂` (`turbine_work`) | §8.2.1 *Modeling the Rankine Cycle* | **8.1** | 446 | 464 |
| condenser heat `Q̇_out/ṁ = h₂−h₃` (`condenser_heat`) | §8.2.1 | **8.2** | 447 | 465 |
| pump work `Ẇ_p/ṁ = h₄−h₃` (`pump_work`) | §8.2.1 | **8.3** | 447 | 465 |
| boiler heat `Q̇_in/ṁ = h₁−h₄` (`boiler_heat`) | §8.2.1 | **8.4** | 447 | 465 |
| thermal efficiency (`rankine_efficiency`, `_from_heat`) | §8.2.1 *Performance Parameters* | **8.5a, 8.5b** | 447 | 465 |
| back work ratio, ~1–2% (`back_work_ratio`) | §8.2.1 | **8.6** | 447 | 465 |
| ideal cycle: isentropic turbine/pump, 4 processes | §8.2.2 *Ideal Rankine Cycle* | — | 449 | 467 |
| pump work `(Ẇ_p/ṁ)_s ≈ v₃(p₄−p₃)` (`pump_work_approx`) | §8.2.2 | **8.7a, 8.7b** | 449 | 467 |
| `x₂ = (s−s_f)/(s_g−s_f)`, `h = h_f + x·h_fg` (`quality_from_entropy`, `enthalpy_two_phase`) | Ex 8.1 analysis | — | 451 | 469 |
| pressure effects `η_ideal = 1 − T̄_out/T̄_in` (`ideal_efficiency_avg_temps`) | §8.2.3 *Effects of Boiler and Condenser Pressures* | **8.8** | 453–454 | 471–472 |
| Carnot comparison (why Carnot is a poor plant model) | §8.2.3 *Comparison with Carnot Cycle* | — | 454–455 | 472–473 |
| isentropic turbine efficiency (`turbine_exit_actual`) | §8.2.4 *Principal Irreversibilities and Losses* | **8.9** | 455 | 473 |
| isentropic pump efficiency (`pump_work_actual`) | §8.2.4 | **8.10a, 8.10b** | 455–456 | 473–474 |
| superheat, reheat, x ≳ 0.9 guideline, supercritical (`reheat_efficiency`) | §8.3 *Improving Performance—Superheat, Reheat, and Supercritical* | — | 459–460 | 477–478 |

## Worked Examples used
| Example | Title | Printed p. | PDF p. |
|---|---|---|---|
| **8.1** | Analyzing an Ideal Rankine Cycle (η=0.371, bwr=8.37×10⁻³, ṁ=3.77×10⁵ kg/h, Q̇_in=269.77 MW, Q̇_out=169.75 MW, ṁ_cw=7.3×10⁶ kg/h) | 450–452 | 468–470 |
| **8.2** | Analyzing a Rankine Cycle with Irreversibilities (η_t=η_p=0.85; η=0.314, ṁ=4.449×10⁵ kg/h, Q̇_in=318.2 MW, Q̇_out=218.2 MW) | 456–458 | 474–476 |
| **8.3** | Evaluating Performance of an Ideal Reheat Cycle (8.0 MPa/480 °C, reheat 0.7 MPa/440 °C; η=0.403, x₄=0.9382, ṁ=2.363×10⁵ kg/h, Q̇_out=148 MW) | 461–463 | 479–481 |
| **8.4** | Evaluating Performance of a Reheat Cycle with Turbine Irreversibility (η_t=0.85 per stage; η=0.351) — cited in notes | 463–464 | 481–482 |

Moran's quoted steam-table states (h₁=2758.0/s₁=5.7432 at 8.0 MPa; s_f=0.5926,
s_g=8.2287, h_f=173.88, h_fg=2403.1, v_f=1.0084×10⁻³ at 0.008 MPa; h=3348.4/s=6.6586 at
8.0 MPa, 480 °C; h=3353.3/s=7.7571 at 0.7 MPa, 440 °C; h_f=62.99/146.68 at 15/35 °C)
are **embedded** per convention and cross-checked against
`modules/Thermo/steam_tables/A2/A3/A4` CSVs in `test_rankine_cycle.py`.

## See also
`09.1` (Carnot ceiling; §8.2.3 comparison), `09.5` (Brayton — gas counterpart, bwr
40–80%), `07.1` (η_t/η_p), `05.1` (saturation-table machinery), Topic 8 modules
(compressor/condenser/heat exchanger), `9.EQ`/`9.EP`/`9.HP`.
