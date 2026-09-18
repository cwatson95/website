# 1.1 — References

All page numbers were verified by **reading the actual page text** in the PDF
(not inferred from a table of contents). **Printed** = the number printed on the
page; **PDF** = the 0-based page index in a viewer.

| Book (edition) | File | Printed → PDF offset |
|---|---|---|
| Moran, Shapiro, Boettner & Bailey, *Fundamentals of Engineering Thermodynamics*, **8th ed.** (Wiley, 2014) | `modules/Thermo/thermodynamics.pdf` | PDF = printed **+ 17** (constant through the body) |

The same book supplies the embedded property data in `../../steam_tables/` (Tables
A‑2 … A‑6, printed pp. 927–936).

## Topic → location

| Topic (code symbol) | Section № & title | Eq. № | Printed p. | PDF p. |
|---|---|---|---|---|
| system, surroundings, boundary, **closed system**, **control volume**, open system, control surface | §1.2 *Defining Systems* | — | 4 | 22 |
| closed & **isolated** systems | §1.2.1 *Closed Systems* | — | 6 | 24 |
| control volume / open system | §1.2.2 *Control Volumes* | — | 6 | 24 |
| selecting the control surface (Fig. 1.2) | §1.2.3 *Selecting the System Boundary* | — | 7 | 25 |
| mass rate balance (`mass_rate_residual`) | §4.1 *Conservation of Mass for a Control Volume* | 4.1, **4.2** | 170 | 188 |
| 1-D mass flow rate ṁ = AV/v = ρAV (`mass_flow_rate`) | §4.2.1 *One-Dimensional Flow Form of the Mass Rate Balance* | **4.4b** (AV/v), 4.4a (ρAV) | 172 | 190 |
| steady-state mass balance (`is_steady_mass`) | §4.2.2 *Steady-State Form of the Mass Rate Balance* | **4.6** | 173 | 191 |
| CV energy rate balance, u-form | §4.4.1 *Conservation of Energy for a Control Volume* | 4.9 | 178 | 196 |
| **flow work** pv; why enthalpy appears (`flow_energy`) | §4.4.2 *Evaluating Work for a Control Volume* | 4.12, **4.13** | 179 | 197 |
| CV energy rate balance with h (`energy_rate_residual`) | §4.4.3 *One-Dimensional Flow Form of the Control Volume Energy Rate Balance* | 4.14 (1 in/1 out), **4.15** (Σ, most general) | 180 | 198 |
| steady-state energy balance (`shaft_power`, `turbine_power`, `compressor_power`) | §4.5.1 *Steady-State Forms of the Mass and Energy Rate Balances* | **4.18** (=0 form), 4.20a/b | 181 | 199 |
| nozzles & diffusers (`nozzle_exit_velocity`, `diffuser_exit_enthalpy`) | §4.6 *Nozzles and Diffusers* | **4.21** | 183 / 184 | 200 / 201 |
| turbines (`turbine_power`) | §4.7 *Turbines* | Ẇ_cv = ṁ(h₁−h₂), reducing 4.20a | 186 / 188 | 203 / 205 |
| compressors & pumps (`compressor_power`) | §4.8 *Compressors and Pumps* | Ẇ_cv = ṁ(h₁−h₂), reducing 4.20a | 190 | 208 |
| heat exchangers (`heat_exchanger_flow_ratio`, `mixing_exit_enthalpy`) | §4.9 *Heat Exchangers* | 0 = Q̇_cv + Σṁ_i h_i − Σṁ_e h_e, reducing 4.18 | 195 / 196 | 212 / 213 |
| throttling devices (`throttle_exit_enthalpy`) | §4.10 *Throttling Devices* | **4.22** (h₂ = h₁) | 200 / 201 | 217 / 218 |

## Notes on the citations
- §§4.7–4.9 (turbines, compressors/pumps, heat exchangers) state their working
  equations as **locally-lettered** relations (a), (b) that explicitly *reduce*
  the numbered steady-state balances (Eq. 4.20a, Eq. 4.18); the only **numbered**
  application equations in §§4.6–4.10 are **4.21** (nozzles/diffusers) and
  **4.22** (throttling).
- Some section headings begin at the foot of the previous printed page (e.g. §4.7
  opens on p. 186, but its modeling assumptions and equation are on p. 188); both
  pages are listed where they differ.
- The chapter roadmap (printed p. 168) confirms the structure: mass & energy
  balances are introduced in §§4.1 and 4.4 and applied in §§4.5–4.11.

## See also
- `../../steam_tables/README.md` — provenance/validation of the A‑2 … A‑6 water
  tables used by `code/steam_lookup.py`.
- Closely related leaves to be built: `1.2` closed systems, `4.1` enthalpy,
  `6.4` steady-state, `6.5` conservation of mass flow, and the device/cycle
  modules in groups `8` and `9` (see `modules/Thermo/list.txt`).
